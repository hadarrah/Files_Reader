import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--address', default='localhost', help='address for connection')
    parser.add_argument('-p', '--port', default='8081', help='port for connection')
    parser.add_argument('-dh', '--db-host', default='localhost', help='address for database connection')
    parser.add_argument('-dn', '--db-name', default='postgres', help='database name name')
    parser.add_argument('-du', '--db-user', default='postgres', help='name of the user\'s database')
    parser.add_argument('-dp', '--db-password', default='root', help='password for db connection')
    parser.add_argument('-l', '--log', default=os.getcwd(), help='path for the log file')

    args = parser.parse_args()
    return args
