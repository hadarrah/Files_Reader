from Utils import logger, flow_parser
import socket
import json
import time
import random

NUMBER_OF_FILES_PER_REQUEST = 10
INTERVAL = 5


class Client():
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.counter = 0
        self.logger = logger.get_logger(__name__)

    def run(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = (self.address, int(self.port))
        self.logger.info('connecting to %s port %s' % server_address)
        sock.connect(server_address)

        try:
            while True:
                files_array = self.randomized_json_files()

                # Send data
                msg = json.dumps(files_array).encode()
                sock.sendall(msg)
                time.sleep(INTERVAL)
        finally:
            sock.close()

    def randomized_json_files(self):
        array_to_send = {}
        for i in range(NUMBER_OF_FILES_PER_REQUEST):
            file_name = "file_{idx}".format(idx=self.counter)
            rand_num = random.randint(1, 10)
            if rand_num == 1:
                array_to_send[file_name] = "corrupt"
            else:
                array_to_send[file_name] = "not-corrupt"
            self.counter += 1
        return array_to_send


if __name__ == '__main__':
    args = flow_parser.parse_arguments()

    logger.setup()
    log = logger.get_logger(__name__)
    log.info("Starting Files Reader Client Process")

    Client(args.address, args.port).run()