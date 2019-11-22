from Utils import logger, flow_parser
import socket
import json
import psycopg2
import queue
from threading import Thread
from Utils.timeout import Timeout
from datetime import datetime
import time

class Server():
    def __init__(self, address, port, db_host, db_name, db_usr, db_pass):
        self.address = address
        self.port = port
        self.db_host = db_host
        self.db_name = db_name
        self.db_usr = db_usr
        self.db_pass = db_pass
        self.requests_queue = queue.Queue()
        self.current_number_of_requests = 0
        self.logger = logger.get_logger(__name__)

    def run(self):
        self.sock = self.create_sock_connection()
        self.db_cur, self.db_con = self.create_db_connection()

        # create thread to handle the requests queue
        Thread(target=self.requests_handler).start()

        # create thread to handle the heartbeat
        Thread(target=self.heartbeat_handler).start()

        while True:
            # Wait for a connection
            # we allowed multiple connections but the server can handle up to 4 requests simultaneously
            self.logger.info('waiting for a connection')
            connection, client_address = self.sock.accept()
            self.logger.info('connection from ' + str(client_address))
            Thread(target=self.receive_from_connection, args=(connection, client_address,)).start()

        # Clean up the connection
        self.db_cur.close()
        self.db_con.close()

    def receive_from_connection(self, con, address):
        try:
            while True:
                data = con.recv(4096).decode()
                self.logger.info("data: " + str(data))
                self.requests_queue.put(data)
        except:
            self.logger.info("connection from {add} is end".format(add=address))

    def requests_handler(self):
        while True:
            if self.current_number_of_requests < 4 and not self.requests_queue.empty():
                self.current_number_of_requests += 1
                data = self.requests_queue.get()
                Thread(target=self.analyze_data, args=(data,)).start()

    @Timeout(40)
    def analyze_data(self, data):
        files_array = json.loads(data)
        for file in files_array:
            if files_array[file] == "not-corrupt":
                self.logger.info('received file {file}'.format(file=file))
                self.db_cur.execute("INSERT INTO files_reader Values ('{type}', '{name}');".format(type="file", name=file))
                self.db_con.commit()
            else:
                self.logger.warning('file {file} is corrupted!'.format(file=file))
        self.current_number_of_requests -= 1

    def heartbeat_handler(self):
        while True:
            # current date and time
            now = datetime.now()
            self.db_cur.execute("INSERT INTO files_reader Values ('{type}', '{name}');".format(type="heartbeat", name=now))
            self.db_con.commit()

            time.sleep(60)

    def create_sock_connection(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = (self.address, int(self.port))
        self.logger.info('starting up on %s port %s' % server_address)
        sock.bind(server_address)

        # Listen for incoming connections
        sock.listen(1)

        return sock

    def create_db_connection(self):
        conn = psycopg2.connect(host=self.db_host, database=self.db_name, user=self.db_usr, password=self.db_pass)
        cur = conn.cursor()
        return cur, conn


if __name__ == '__main__':
    args = flow_parser.parse_arguments()

    logger.setup()
    log = logger.get_logger(__name__)
    log.info("Starting Files Reader Server Process")

    Server(args.address, args.port, args.db_host, args.db_name, args.db_user, args.db_password).run()
