from Utils import logger, flow_parser
import socket
import parser
import json
import psycopg2


class Server():
    def __init__(self, address, port, db_host, db_name, db_usr, db_pass):
        self.address = address
        self.port = port
        self.db_host = db_host
        self.db_name = db_name
        self.db_usr = db_usr
        self.db_pass = db_pass
        self.logger = logger.get_logger(__name__)

    def run(self):
        sock = self.create_sock_connection()
        db_cur, db_con = self.create_db_connection()

        while True:
            # Wait for a connection
            self.logger.info('waiting for a connection')
            connection, client_address = sock.accept()
            try:
                self.logger.info('connection from ' + str(client_address))

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(512).decode()

                    if data:
                        files_array = json.loads(data)
                        for file in files_array:
                            self.logger.info('received file {file} with status {status}'.
                                             format(file=file, status=str(files_array[file])))
                            db_cur.execute("INSERT INTO files_reader Values ('{name}', '{status}');".format(name=file, status=files_array[file]))
                            db_con.commit()

            finally:
                # Clean up the connection
                db_cur.close()
                db_con.close()

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
