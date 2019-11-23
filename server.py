import socket
import json
import psycopg2
import queue
import time
from Utils import logger, flow_parser, configuration
from Utils.timeout import timeout_decorator
from threading import Thread
from datetime import datetime


class Server:
    """
    This class represent the server side of files reader.
    It could handle with multiple connections but with MAX_REQUESTS (4) requests simultaneously.
    The requests get their priority by a queue.
    For each request TIMEOUT (40) seconds o be handled by the server.
    """
    def __init__(self, host, port, db_host, db_name, db_usr, db_pass):
        self.host = host
        self.port = port
        self.db_host = db_host
        self.db_name = db_name
        self.db_usr = db_usr
        self.db_pass = db_pass
        self.requests_queue = queue.Queue()
        self.current_number_of_requests = 0
        self.logger = logger.get_logger(__name__)

    def run(self):
        """
        Start the server  process.
        :return:
        """
        # initialize socket and db connection
        try:
            self.sock = self.create_sock_connection()
            self.db_cur, self.db_con = self.create_db_connection()
        except Exception as e:
            self.logger.error("There is a problem to create either the socket or db connection")
            self.logger.error("The error message is: \n" + str(e))
            exit(1)

        # create thread to handle the requests queue
        Thread(target=self.requests_handler).start()

        # create thread to handle the server's heartbeat
        Thread(target=self.heartbeat_handler).start()

        # start listening to new possible connections
        try:
            self.wait_for_connections()
        except Exception as e:
            self.logger.error("The server caught an exception...")

        # clean up the connection
        self.logger.error("Close socket connection")
        self.sock.close()

        self.logger.info("Close db connection")
        self.db_cur.close()
        self.db_con.close()

    def wait_for_connections(self):
        """
        Wait for possible connection to be link. For each connection open new channel for listening.
        :return:
        """
        while True:
            self.logger.info('Waiting for a connection')
            connection, client_address = self.sock.accept()
            self.logger.info('Connection from ' + str(client_address))
            Thread(target=self.receive_from_connection, args=(connection, client_address,)).start()

    def receive_from_connection(self, con, address):
        """
        Receive data from connection and add it into the requests queue.
        Listening until the connection ended.
        :param con:     socket connection
        :param address: client address
        :return:
        """
        try:
            while True:
                data = con.recv(configuration.BUFFER_SIZE).decode()
                self.requests_queue.put(data)
        except:
            self.logger.info("Connection from {add} is ended".format(add=address))

    def requests_handler(self):
        """
        The manager handle for the entire requests.
        As long as the request queue is not empty
        and if the current number of requests lower than the MAX_REQUESTS do the following.
        :return:
        """
        self.logger.info("Start request handler...")
        while True:
            if self.current_number_of_requests < configuration.MAX_REQUESTS and not self.requests_queue.empty():
                self.current_number_of_requests += 1
                data = self.requests_queue.get()
                Thread(target=self.analyze_data, args=(data,)).start()  # open new thread to handle the specific request

    @timeout_decorator(configuration.TIMEOUT)
    def analyze_data(self, data):
        """
        Load the data into the db and handle in case we get corrupted file.
        :param data:
        :return:
        """
        files_array = json.loads(data)
        for file in files_array:
            if files_array[file] == "not-corrupt":
                self.logger.info('Received file {file}'.format(file=file))

                # update db
                self.db_cur.execute("INSERT INTO files_reader Values ('{type}', '{name}');".format(type="file",
                                                                                                   name=file))
                self.db_con.commit()
            else:
                self.logger.warning('File {file} is corrupted!'.format(file=file))
        self.current_number_of_requests -= 1

    def heartbeat_handler(self):
        """
        Every HEARTBEAT_INTERVAL seconds send an heartbeat as timestamp into the db.
        :return:
        """
        self.logger.info("Start heartbeat handler...")
        while True:
            now = datetime.now()    # get current date and time

            # update db
            self.db_cur.execute("INSERT INTO files_reader Values ('{type}', '{name}');".format(type="heartbeat",
                                                                                               name=now))
            self.db_con.commit()

            time.sleep(configuration.HEARTBEAT_INTERVAL)

    def create_sock_connection(self):
        """
        Establish new socket connection for self.host and self.port
        :return:
        """
        self.logger.info("Create socket connection")
        # create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind the socket to the port
        server_address = (self.host, int(self.port))
        self.logger.info('Starting up on %s port %s' % server_address)
        sock.bind(server_address)

        # listen for incoming connections
        sock.listen(1)

        return sock

    def create_db_connection(self):
        """
        Establish the PostgresSQL db connection.
        :return:
        """
        self.logger.info("Create db connection")
        self.logger.debug("Host={host}".format(host=self.db_host))
        self.logger.debug("Database={db}".format(db=self.db_name))
        self.logger.debug("User={user}".format(user=self.db_usr))
        self.logger.debug("Password={pw}".format(pw=self.db_pass))
        conn = psycopg2.connect(host=self.db_host, database=self.db_name, user=self.db_usr, password=self.db_pass)
        cur = conn.cursor()
        return cur, conn


if __name__ == '__main__':
    # parse the cmd's arguments
    args = flow_parser.parse_arguments()

    # initialize the logger
    logger.setup()
    log = logger.get_logger(__name__)
    log.info("Starting Files Reader Server Process")

    # trigger the server
    Server(args.host, args.port, args.db_host, args.db_name, args.db_user, args.db_password).run()

    exit(1)
