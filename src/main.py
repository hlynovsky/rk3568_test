from network import Network

import logging

logging.basicConfig(filename='logs/main.log', level=logging.DEBUG)

eth0 = Network('eth0')
eth1 = Network('eth1')

try:
    eth0.ping()
    eth1.ping()
except Exception as e:
    logging.debug(e)
    logging.info("Network down")
