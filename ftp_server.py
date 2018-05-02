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
        print("Server started thread for client {} on port {}".format(self.ip, self.port))

    def run(self):
        while True:
            data = self.socket.recv(1024)
            print("Server received data: {}".format(data))
            if data:
                print("Server sending data back to client...")
                self.socket.sendall(data)
            else:
                print("No more data from client...")
                break


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

            # once we get a connection just spawn a thread and deal with it
            thread = ClientThread(client_socket, client_ip, port)
            thread.start()
            created_threads.append(thread)

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
