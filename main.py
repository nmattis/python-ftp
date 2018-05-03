"""
main.py
Nick Mattis

Runs either an ftp server or client depending on the command
line argument specified.
"""

import argparse
import sys

from ftp_client import FTPClient
from ftp_server import FTPServer


def main():
    """
    Takes in args, either creates and runs a server instance or client instance.
    """
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--server", help="Create and run a FTP server instance", action="store_true")
    ap.add_argument("-c", "--client", help="Create and run a FTP client instance", action="store_true")
    args = ap.parse_args()

    if args.server:
        # create and run the server
        server = FTPServer()
        server.run_server()

    if args.client:
        # create and run client
        client = FTPClient()
        client.cmdloop()

    if not args.server and not args.client:
        # none specified so exit
        sys.exit("You must specify to start and create either a client or server")


if __name__ == '__main__':
    main()
