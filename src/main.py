from network import Network
from usb import Usb
from can import CanTest
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test.log'),
        logging.StreamHandler()
    ]
)

network_interfaces = ['eth0', 'eth1']
usb_paths = ['/media/sda1'] 

network = Network(network_interfaces)
usb = Usb(usb_paths)
can_test = CanTest("can0", "can1")

def run_tests():
    network_status = network.ping()
    usb_status = usb.run()
    can_status = can_test.test_channels()

    if network_status == 0:
        logging.info("Network tests passed.")
    else:
        logging.error("Network tests failed.")

    if usb_status == 0:
        logging.info("USB tests passed.")
    else:
        logging.error("USB tests failed.")

    if can_status == 0:
        logging.info("CAN tests passed.")
    else:
        logging.error("CAN tests failed.")

def exit_code():
    return 0 if all(status == 0 for status in [network.ping(), usb.run(), can_test.test_channels()]) else 1

if __name__ == "__main__":
    exit_code = run_tests()
    exit(exit_code)
