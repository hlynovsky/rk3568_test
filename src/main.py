from network import Network
from usb import Usb
from can import Can
from i2c import I2C
from rtc import Rtc

import logging

logging.basicConfig(
    level=logging.DEBUG,
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
i2c = I2C()
can = Can("can0", "can1")
rtc = Rtc()

def main():
    network_status = network.ping()
    usb_status = usb.run()
    can_status = can.test_channels()
    i2c_status, eeprom_status = i2c.run()
    rtc_status = rtc.read_rtc()

    status_width = 10

    if network_status == 0:
        logging.info(f"{'Network':<{status_width}} [OK]")
    else:
        logging.error(f"{'Network':<{status_width}} failed")

    if usb_status == 0:
        logging.info(f"{'USB':<{status_width}} [OK]")
    else:
        logging.error(f"{'USB':<{status_width}} failed")

    if can_status == 0:
        logging.info(f"{'CAN':<{status_width}} [OK]")
    else:
        logging.error(f"{'CAN':<{status_width}} failed")

    if i2c_status == True:
        logging.info(f"{'I2C':<{status_width}} [OK]")
    else:
        logging.error(f"{'I2C':<{status_width}} failed")
    if eeprom_status == True:
        logging.info(f"{'EEPROM':<{status_width}} [OK]")
    else:
        logging.error(f"{'EEPROM':<{status_width}} failed")

    if rtc_status != None:
        logging.info(f"{'RTC':<{status_width}} [OK]")
    else:
        logging.error(f"{'RTC':<{status_width}} failed")
if __name__ == "__main__":
    main()