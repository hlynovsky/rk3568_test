import logging
import subprocess

logging.basicConfig(filename='logs/network.log', level=logging.DEBUG)
logging.BASIC_FORMAT = '%(levelname)s: %(asctime)s - %(message)s'

class Network:

    def __init__(self, interfaces):
        self.interfaces = interfaces

    def ping(self):
        for interface in self.interfaces:
            result = None
            try:
                ip = subprocess.check_output(['ip', 'addr', 'show', interface]).decode('utf-8').split('inet ')[1].split('/')[0]
            except Exception as e:
                logging.error(f"Error getting IP for {interface}: {e}")
                print(f"{interface} - not ok")
                continue 

            try:
                result = subprocess.call(['ping', '-c', '3', ip])
            except Exception as e:
                logging.error(f"Ping failed for {interface}: {e}")
                print(f"{interface} - not ok")
                continue 

            if result == 0:
                logging.info(f"Interface {interface} OK")
                print(f"{interface} - ok")
            else:
                logging.error(f"Interface {interface} is down")
                print(f"{interface} - not ok")
