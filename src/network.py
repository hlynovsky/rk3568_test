import logging
import subprocess

logging.basicConfig(filename='logs/network.log', level=logging.DEBUG)
class Network():

    def __init__(self, interface):
        self.interface = interface

    def ping(self):
        result = subprocess.call(['ping', '-c', '3', self.interface])
        if result == 0:
            logging.debug(f"Ping to {self.interface} successful. Detailed info: 3 packets sent, 3 packets received.")
            logging.info(f"Interface {self.interface} OK")
            return 0
        else:
            logging.info(f"Interface {self.interface} is down")
            return 1