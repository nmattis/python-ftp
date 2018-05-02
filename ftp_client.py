"""
ftp_client.py
Nick Mattis

Connects to a specified ftp_server, allows for the downloading
or uploading of files.
"""

import socket
import sys
from cmd import Cmd


class FTPClient(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        Cmd.intro = "Starting FTPClient. Type help or ? to list commands.\n"
        Cmd.prompt = ">>> "
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ftp_port = 2121
        self.connected = False

    def do_rftp(self, args):
        """
        Usage:
            rftp <FTP Server Address> <User> <Password>

        If the provided ip address, user name, and password are valid than access to the
        FTPServer is granted.
        """
        vals = args.split()
        if len(vals) == 3:
            ip_address, user_name, password = vals
            print("Trying to connect to server {} with user:password -> {}:{}".format(ip_address, user_name, password))
            print()
            self.socket.connect((ip_address, self.ftp_port))

            message = "Trying to connect."
            print("Sending message: {}".format(message))
            self.socket.sendall(message.encode('utf-8'))

            # wait and look for a response
            amount_received = 0
            amount_expected = len(message)

            while amount_received < amount_expected:
                info = self.socket.recv(1024)
                amount_received += len(info)
                print("Received from server: {}".format(info))
        else:
            print("rftp requires exactly 3 arguments...")
            print()

    def do_rget(self, args):
        """
        Usage:
            rget <File Name>

        If connected to an FTPServer instance and the file exists then it
        instantiates a download of that file from the server to client.
        """
        vals = args.split()
        if len(vals) == 1:
            file_name = vals[0]
            print("Trying to download file {} from server to client.".format(file_name))
            print()
        else:
            print("rget requires exactly 1 arguments...")
            print()
    
    def do_rput(self, args):
        """
        Usage:
            rput <File Name>

        If connected to an FTPServer instance and the file exists on the client
        it instantiates an upload of the file to the FTPServer.
        """
        vals = args.split()
        if len(vals) == 1:
            file_name = vals[0]
            print("Trying to upload file {} from client to server.".format(file_name))
            print()
        else:        
            print("rput requires exactly 1 arguments...")
            print()

    def do_quit(self, args):
        """
        Exits the command loop of the client program.
        """
        self.socket.close()
        sys.exit("Quitting FTPClient...")
