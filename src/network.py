import os
import logging
import subprocess

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test.log'),
        logging.StreamHandler()
    ]
)

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
                logging.error(f"{interface} - not ok")
                continue 

            try:
                result = subprocess.call(['ping', '-c', '3', ip])
            except Exception as e:
                logging.error(f"Ping failed for {interface}: {e}")
                continue 

            if result == 0:
                logging.info(f"{interface} - ok")
            else:
                logging.error(f"{interface} - not ok")