"""
ftp_client.py
Nick Mattis

Connects to a specified ftp_server, allows for the downloading
or uploading of files.
"""

import errno
import os
import socket
import sys
from cmd import Cmd
from socket import error as socket_error


class FTPClient(Cmd):
    def __init__(self):
        Cmd.__init__(self)
        Cmd.intro = "Starting FTPClient. Type help or ? to list commands.\n"
        Cmd.prompt = ">>> "
        self.socket = None 
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
            if self.connected:
                print("Client already connected to server (ip, port) : {}".format(self.socket.getpeername()))
            else:
                server_ip, user_name, password = vals
                print("Trying to connect to server {} with user:password -> {}:{}".format(server_ip, user_name, password))
                print()
                try:
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket.connect((server_ip, self.ftp_port))
                    packet = "rftp,user:{},passwd:{}".format(user_name, password)
                    print("Sending message: {}".format(packet))
                    self.socket.sendall(packet.encode('utf-8'))

                    while True:
                        recv_data = self.socket.recv(1024)
                        recv_data = recv_data.decode('utf-8').strip().split(",")

                        if recv_data[0] == 'Success':
                            self.connected = True
                            print("Successfully Authenticated!")
                            break

                        if recv_data[0] == 'Unknown':
                            self.connected = False
                            print("User name and password incorrect, connection refused.")
                            self.socket.shutdown(socket.SHUT_RDWR)
                            self.socket.close()
                            break

                        if recv_data[0] == 'Expected':
                            self.connected = False
                            print("The client did not send the correct information, connection refused.")
                            self.socket.shutdown(socket.SHUT_RDWR)
                            self.socket.close()
                            break
                        
                except socket_error as serr:
                    if serr.errno != errno.ECONNREFUSED:
                        # if it isn't a connection refused reraise to deal with somewhere else
                        raise serr
                    # else deal with it
                    message = (
                        "Looks something happened to server {}. "
                        "Check and ensure you have the right address "
                        "and the server is running.".format(server_ip)
                    )
                    print(message)
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
        if self.connected:
            vals = args.split()
            if len(vals) == 1:
                file_name = vals[0]
                print("Trying to upload file {} from client to server.".format(file_name))
                print()

                try:
                    packet = "rput,{},{}".format(file_name, os.path.getsize(file_name))
                    self.socket.sendall(packet.encode('utf-8'))
                    
                    while True:
                        recv_data = self.socket.recv(1024)
                        packet_info = recv_data.decode('utf-8').strip().split(",")

                        if packet_info[0] == "Ready":
                            print("Sending file {} to server {}".format(file_name, self.socket.getpeername()))

                            with open(file_name, mode="rb") as file:
                                self.socket.sendfile(file)
                        elif packet_info[0] == "Received":
                            if int(packet_info[1]) == os.path.getsize(file_name):
                                print("{} successfully uploaded to server {}".format(file_name, self.socket.getpeername()))
                                break
                            else:
                                print("Something went wrong trying to upload to server {}. Try again".format(self.socket.getpeername()))
                                break
                        else:
                            print("Something went wrong trying to upload to server {}. Try again.".format(self.socket.getpeername()))
                            break
                except IOError:
                    print("File doesn't exist on the system!")
            else:        
                print("rput requires exactly 1 arguments...")
                print()
        else:
            print("You must use the 'rftp' command to first connect to a server before uploading a file.")

    def do_quit(self, args):
        """
        Exits the command loop of the client program.
        """
        if self.socket is not None:
            if self.socket.fileno() != -1:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
        sys.exit("Quitting FTPClient...")
