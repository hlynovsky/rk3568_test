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

def write_result(text):
    with open('results.log', 'w') as f:
        f.write(text)

def remove_result():
    subprocess.run(["rm", "results.log"])

def check_result_file():
    try:
        result = subprocess.run(["ls", "/opt/rk3568_test/src/result.log"], capture_output=True, check=True)
        logging.info("Results file exists")
        return True
    except subprocess.CalledProcessError:
        logging.info("Results file does not exist") 
        return False
    
def test_watchdog():
    subprocess.run(["echo", "1", ">", "/dev/watchdog"])

    logging.info("Watchdog activated")
    logging.info("System will reboot in 30 seconds...")

    status_width = 10
    write_result(f"{'Watchdog':<{status_width}} [OK]")

def main():

    if check_result_file():
        subprocess.run(["cat", "/opt/rk3568_test/src/result.log"], capture_output=True, text=True)
        subprocess.run(["rm", "/opt/rk3568_test/src/result.log"])
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

        if wd_status.returncode == 0:
            write_result(f"{'Watchdog':<{status_width}} [OK]")
        else:
            write_result(f"{'Watchdog':<{status_width}} [FAILED]")
        write_result("=" * 50)
        test_watchdog()

if __name__ == "__main__":
    main()