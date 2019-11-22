import logger
import logging
import parser
import server
import client

if __name__ == '__main__':
    args = parser.parse_argumnets()

    logger.setup(logging.DEBUG)
    log = logging.getLogger(__name__)
    log.info("Starting Files Reader Process")

    if args.mode == 'server':
        server.Server(args.address, args.port).run()
    if args.mode == 'client':
        client.Client(args.address, args.port).run()
    else:
        log.error("You choose incorrect mode, please select server/client")

    exit()
