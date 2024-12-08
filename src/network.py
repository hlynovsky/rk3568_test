import logging
import subprocess

logging.basicConfig(filename='logs/network.log', level=logging.DEBUG)
logging.BASIC_FORMAT = '%(levelname)s: %(asctime)s - %(message)s'

class Network():

    def __init__(self, interface):
        self.interface = interface

    def ping(self):

        try:
            ip = subprocess.check_output(['ip', 'addr', 'show', self.interface]).decode('utf-8').split('inet ')[1].split('/')[0]
        except Exception as e:
            logging.error(e)
        
        try:
            result = subprocess.call(['ping', '-c', '3', ip])
        except Exception as e:
            logging.error(e)

        if result == 0:
            logging.info(f"Interface {self.interface} OK")
            return 0
        else:
            logging.error(f"Interface {self.interface} is down")
            return 1