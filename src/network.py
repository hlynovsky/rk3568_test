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
                subprocess.run(f"echo 'Error getting IP for {interface}: {e}'", shell=True)
                logging.error(f"{interface} - not ok")
                subprocess.run(f"echo '{interface} - not ok'", shell=True)
                continue 

            try:
                result = subprocess.call(['ping', '-c', '3', ip])
            except Exception as e:
                logging.error(f"Ping failed for {interface}: {e}")
                subprocess.run(f"echo 'Ping failed for {interface}: {e}'", shell=True)
                continue 

            if result == 0:
                logging.info(f"{interface} - ok")
                subprocess.run(f"echo '{interface} - ok'", shell=True)
                return 0
            else:
                logging.error(f"{interface} - not ok")
                subprocess.run(f"echo '{interface} - not ok'", shell=True)
                return 1
