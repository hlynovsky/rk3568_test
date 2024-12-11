from network import Network
from usb import Usb

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test.log'),
        logging.StreamHandler()
    ]
)

network_interfaces = ['eth0', 'eth1']
usb_paths = ['/media/sda1'] # '/media/sdb1'

network = Network(network_interfaces)
usb = Usb(usb_paths)

network.ping()
usb.run_tests()