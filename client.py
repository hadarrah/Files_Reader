import socket
import json
import time
import random
from Utils import logger, flow_parser, configuration


class Client:
    """
    This class represent a demo client side.
    It demonstrates the sending process by creating the files array based on json,
    there is a chance of CHANCE_OF_CORRUPTED (10%) to send a corrupted file and it implemented by randomization.
    The size of the packet depend on NUMBER_OF_FILES_PER_REQUEST and between each request
    the client wait REQUEST_INTERVAL seconds.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.counter = 0
        self.logger = logger.get_logger(__name__)

    def run(self):
        """
        Start the client  process.
        :return:
        """
        try:
            self.sock = self.create_sock_connection()
        except Exception as e:
            self.logger.error("There is a problem to create the socket connection")
            self.logger.error("The error message is: \n" + str(e))
            exit(1)

        # create and send data
        self.logger.info("Create and send data")
        try:
            while True:
                # create data
                files_array = self.randomized_data()
                msg = json.dumps(files_array).encode()
                self.logger.debug("Data to send: \n" + str(msg))

                # Send data
                self.sock.sendall(msg)
                time.sleep(configuration.REQUEST_INTERVAL)
        except:
            self.logger.info("Connection with the server is ended")
        finally:
            self.sock.close()

    def create_sock_connection(self):
        """
        Establish new socket connection for self.host and self.port
        :return:
        """
        self.logger.info("Create socket connection")
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_host = (self.host, int(self.port))
        self.logger.info('Connecting to %s port %s' % server_host)
        sock.connect(server_host)

        return sock

    def randomized_data(self):
        """
        Create array of files (dictionary) and randomized the chance to generate a corrupted file.
        The size of the array based on NUMBER_OF_FILES_PER_REQUEST.
        :return:
        """
        array_to_send = {}
        for i in range(configuration.NUMBER_OF_FILES_PER_REQUEST):
            file_name = "file_{idx}".format(idx=self.counter)
            rand_num = random.randint(1, 100)
            if rand_num <= configuration.CHANCE_OF_CORRUPTED:
                array_to_send[file_name] = "corrupt"
            else:
                array_to_send[file_name] = "not-corrupt"
            self.counter += 1
        return array_to_send


if __name__ == '__main__':
    # parse the cmd's arguments
    args = flow_parser.parse_arguments()

    # initialize the logger
    logger.setup()
    log = logger.get_logger(__name__)
    log.info("Starting Files Reader Client Process")

    # trigger the client
    Client(args.host, args.port).run()

    exit(1)
