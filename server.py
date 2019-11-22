import logging
import socket

class Server():
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.logger = logging.getLogger(__name__)

    def run(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = (self.address, int(self.port))
        self.logger.info('starting up on %s port %s' % server_address)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

        while True:
            # Wait for a connection
            self.logger.info('waiting for a connection')
            connection, client_address = sock.accept()
            try:
                self.logger.info('connection from ' + client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(16)
                    self.logger.info('received "%s"' % data)
                    if data:
                        pass

            finally:
                # Clean up the connection
                connection.close()