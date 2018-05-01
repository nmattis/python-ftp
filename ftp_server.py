"""
ftp_server.py
Nick Mattis

Runs on the host, starts listening for incoming requests from clients.
Checks user name, password and allows for the getting and putting of
files from client to server.
"""

import csv
import socket


class FTPServer():
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (socket.gethostname(), 2121) 
        self.queue_max = 5
        self.allowed_users = self.__load_users()

    def run_server(self):
        """
        Starts an FTPServer listening for connections.
        """
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(self.queue_max)
        ip, port = self.server_socket.getsockname()
        print("Server has started listening... ip: {}, port: {}".format(ip, port))

        while True:
            # wait for connections
            client_socket, client_address = self.server_socket.accept()

            # dispatch thread to do work
            try:
                print("Connection accepted from {}".format(client_address))
            finally:
                # close the connection
                client_socket.close()

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
