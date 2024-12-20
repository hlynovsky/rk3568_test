from network import Network
from usb import Usb
from can import Can
from i2c import I2C
from rtc import Rtc

import logging
import subprocess

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

import os

def write_result(text):
    try: 
        with open('/opt/rk3568_test/src/results.log', 'a') as f:
            f.write(text + '\n')
            f.flush()
            os.fsync(f.fileno()) 
    except Exception as e:
        logging.error(f"Error writing to results file: {e}")
        return False


def close_results():
    try:
        with open('/opt/rk3568_test/src/results.log', 'r') as f:
            f.close()
        return True
    except Exception as e:
        logging.error(f"Error closing results file: {e}")
        return False

def read_results():
    try:
        with open('/opt/rk3568_test/src/results.log', 'r') as f:
            content = f.read()
            logging.info("\n" + content)
            return True
    except Exception as e:
        logging.error(f"Error reading results file: {e}")
        return False


def check_result_file():
    try:
        subprocess.run(["sudo", "ls", "/opt/rk3568_test/src/results.log"], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    
def test_watchdog():
    subprocess.run(["cat", "/dev/watchdog"])
    logging.info("Watchdog activated")
    logging.info("System will reboot in 30 seconds...")

def main():

    if check_result_file():
        status_width = 10
        write_result(f"{'Watchdog':<{status_width}} [OK]")
        read_results()
        subprocess.run(["rm", "/opt/rk3568_test/src/results.log"])
    else: 
        network_status = network.ping()
        usb_status = usb.run()
        can_status = can.test_channels()
        i2c_status = i2c.run()
        rtc_status = rtc.read_rtc()

        wd_status = subprocess.run(["ls", "/dev/watchdog"], capture_output=True, text=True)
        logging.info(f"Watchdog status: {wd_status.stdout}")

        status_width = 10
        write_result("Results")
        write_result("=" * 50)

        if network_status == 0:
            write_result(f"{'Network':<{status_width}} [OK]")
        else:
            write_result(f"{'Network':<{status_width}} [FAILED]")

        if usb_status == 0:
            write_result(f"{'USB':<{status_width}} [OK]")
        else:
            write_result(f"{'USB':<{status_width}} [FAILED]")

        if can_status == 0:
            write_result(f"{'CAN':<{status_width}} [OK]")
        else:
            write_result(f"{'CAN':<{status_width}} [FAILED]")

        if i2c_status == True:
            write_result(f"{'I2C':<{status_width}} [OK]")
        else:
            write_result(f"{'I2C':<{status_width}} [FAILED]")

        if rtc_status != None:
            write_result(f"{'RTC':<{status_width}} [OK]")
        else:
            write_result(f"{'RTC':<{status_width}} [FAILED]")

        test_watchdog()
        close_results()

if __name__ == "__main__":
    main()