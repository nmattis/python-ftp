"""
ftp_client.py
Nick Mattis

Connects to a specified ftp_server, allows for the downloading
or uploading of files.
"""

class FTPClient():
    def __init__(self):
        pass

    def connect_to_server(self, ip_address, user_name, user_password):
        """
        If the provided user name and password are correct than access to the
        FTPServer is granted, otherwise throws an error.

        Params:
            ip_address (int): ip address of the running FTPServer instance
            user_name (str): user name of the user trying to connect
            user_password(str): password associated with the user name to connect

        Returns if a successful connection was established, errors out otherwise.
        """
        pass

    def get_file(self, file_name):
        """
        If connected to an FTPServer instance and the file exists then it
        instantiates a download of that file from the server to client.

        Params:
            file_name (str): name of the file to download

        Returns success of the file download, if file doesn't exist errors out.
        """
        pass
    
    def put_file(self, file_name):
        """
        If connected to an FTPServer instance and the file exists on the client
        it instantiates an upload of the file to the FTPServer.

        Params:
            file_name (str): name of the file to download
        
        Returns success of the file upload, if file doesn't exist errors out.
        """
        pass

    def run_client_process(self):
        """
        Runs a prompt for interacting with the FTPClient so you can perform
        the various specified commands.
        """
        pass
