import argparse
import os

def parse_argumnets():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', default='server', help='the mode to run (server/client)')
    parser.add_argument('-a', '--address', default='localhost', help='address for connection')
    parser.add_argument('-p', '--port', default='8081', help='port for connection')
    parser.add_argument('-l', '--log', default=os.getcwd(), help='path for the log file')

    args = parser.parse_args()
    return args