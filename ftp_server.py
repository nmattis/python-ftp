"""
ftp_server.py
Nick Mattis

Runs on the host, starts listening for incoming requests from clients.
Checks user name, password and allows for the getting and putting of
files from client to server.
"""

import csv
import socket
from threading import Thread


class ClientThread(Thread):
    def __init__(self, client_socket, client_ip, client_port):
        Thread.__init__(self)
        self.socket = client_socket
        self.ip = client_ip
        self.port = client_port
        self.buffer_size = 1024
        print("Server started thread for client {} on port {}".format(self.ip, self.port))

    def run(self):
        while True:
            recv_data = self.socket.recv(self.buffer_size)
            print("Server received data: {}".format(recv_data))
            packet_info = recv_data.decode('utf-8').strip().split(",")

            if packet_info[0] == "rput" and len(packet_info[1:]) == 2:
                self.__read_file(*packet_info[1:])
            elif packet_info[0] == "rget" and len(packet_info[1:]) == 1:
                self.__send_file(*packet_info[1:])
            else:
                if packet_info[0] is not '':
                    print("Server does not support that check sent command")
                    self.socket.sendall("Invalid".encode('utf-8'))

            if not recv_data:
                print("Disconnecting from client {}:{}".format(self.ip, self.port))
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
                break

    def __read_file(self, file_name, length):
        self.socket.sendall("Ready".encode("utf-8"))
        print("Server ready to accept file: {} from client: {}:{}".format(file_name, self.ip, self.port))

        save_file = open("server_files/{}".format(file_name), "wb")

        amount_recieved_data = 0
        while amount_recieved_data < int(length):
            recv_data = self.socket.recv(self.buffer_size)
            amount_recieved_data += len(recv_data)
            save_file.write(recv_data)

        save_file.close()

        self.socket.sendall("Received,{}".format(amount_recieved_data).encode('utf-8'))
        print("Server done receiving from client {}:{}. File Saved.".format(self.ip, self.port))
    
    def __send_file(self, file_name):
        print(file_name)


class FTPServer():
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (socket.gethostname(), 2121) 
        self.queue_max = 5
        self.buffer_size = 1024
        self.allowed_users = self.__load_users()

    def run_server(self):
        """
        Starts an FTPServer listening for connections.
        """
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(self.queue_max)
        ip, port = self.server_socket.getsockname()
        created_threads = []
        print("Server has started listening... ip: {}, port: {}".format(ip, port))

        while True:
            # wait for connections
            client_socket, (client_ip, port) = self.server_socket.accept()
            print("Connection from {}".format(client_ip))

            # want to verify client user, password before spawing thread
            while True:
                auth_data = client_socket.recv(self.buffer_size)
                print("Recieved: {}".format(auth_data))
                recv_data = auth_data.decode('utf-8').strip().split(",")

                if len(recv_data) != 3:
                    print("The data recieved from client {} is wrong.".format(client_ip))
                    error = "Expected,'rftp','user:user','passwd:passwd'"
                    client_socket.sendall(error.encode('utf-8'))
                    client_socket.shutdown(socket.SHUT_RDWR)
                    client_socket.close()
                    break
                else:
                    user_info = recv_data[1].split(":")
                    pass_info = recv_data[2].split(":")
                    if self.__authenticate_user(user_info[1], pass_info[1]):
                        message = "Success"
                        client_socket.sendall(message.encode('utf-8'))

                        # once we get a connection just spawn a thread and deal with it
                        thread = ClientThread(client_socket, client_ip, port)
                        thread.start()
                        created_threads.append(thread)
                        break
                    else:
                        message = "Unknown"
                        client_socket.sendall(message.encode('utf-8'))
                        client_socket.shutdown(socket.SHUT_RDWR)
                        client_socket.close()
                        break

        for t in created_threads:
            t.join()

    def __authenticate_user(self, user_name, passwd):
        """
        Authenticates a user to the FTPServer instance.

        Params:
            user_name (str): name of the user
            passwd (str): password associated with user

        Returns True if valid user/password combo, False otherwise.
        """
        for user in self.allowed_users:
            if user_name == user["name"]:
                return user["passwd"] == passwd
        
        return False

    def __load_users(self):
        """
        Loads in valid users for this FTPServer instance.
        """
        users = []
        with open("allowed_users.txt", "r") as user_file:
            user_csv = csv.DictReader(user_file)
            for user in user_csv:
                users.append(user)

        return users
