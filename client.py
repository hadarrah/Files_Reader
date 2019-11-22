import logging
import socket

class Client():
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.logger = logging.getLogger(__name__)

    def run(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = (self.address, int(self.port))
        self.logger.info('connecting to %s port %s' % server_address)
        sock.connect(server_address)


        while True:
            try:
                # Send data
                message = 'This is the message.  It will be repeated.'
                sock.sendall(message)


            finally:
                sock.close()