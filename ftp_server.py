"""
ftp_server.py
Nick Mattis

Runs on the host, starts listening for incoming requests from clients.
Checks user name, password and allows for the getting and putting of
files from client to server.
"""

import socket


class FTPServer():
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (socket.gethostname(), 2121) 
        self.queue_max = 5

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
