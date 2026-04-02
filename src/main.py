import os
import logging
import subprocess

from typing import Optional, List, Dict, Any
from datetime import datetime
from network import Network
from usb import Usb
from can import Can
from i2c import I2C
from rtc import Rtc
from console import Console
from rs232 import RS232
from gpio import GPIO

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(filename)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("test.log", mode='w'),
        logging.StreamHandler()
    ]
)

RESULTS_FILE = '/opt/rk3568_test/src/results.log'
STATUS_WIDTH = 15
NETWORK_INTERFACES = ['eth0', 'eth1']
USB_PATHS = ['/media/sda1']

class TestResults:
    @staticmethod
    def write(text: str) -> bool:
        try:
            with open(RESULTS_FILE, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"[{timestamp}] {text}\n")
                f.flush()
                os.fsync(f.fileno())
            return True
        except Exception as e:
            logging.error(f"Error writing to results file: {e}")
            return False

    @staticmethod
    def read() -> Optional[str]:
        try:
            with open(RESULTS_FILE, 'r') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Error reading results file: {e}")
            return None

    @staticmethod
    def clear() -> bool:
        try:
            if os.path.exists(RESULTS_FILE):
                os.remove(RESULTS_FILE)
            return True
        except Exception as e:
            logging.error(f"Error clearing results file: {e}")
            return False

    @staticmethod
    def exists() -> bool:
        return os.path.exists(RESULTS_FILE)

def test_watchdog() -> None:
    try:
        subprocess.run(["cat", "/dev/watchdog"], check=True)
        logging.info("Watchdog activated")
        logging.info("System will reboot in 30 seconds...")
    except subprocess.CalledProcessError as e:
        logging.error(f"Watchdog test failed: {e}")

def run_hardware_tests() -> Dict[str, Any]:
    network = Network(NETWORK_INTERFACES)
    usb = Usb(USB_PATHS)
    i2c = I2C()
    can = Can("can0", "can1")
    rtc = Rtc()
    console = Console()
    rs232 = RS232()
    gpio = GPIO()

    return {
        'network': network.ping(),
        'usb': usb.run(),
        'can': can.test_channels(),
        'i2c': i2c.run(),
        'rtc': rtc.read_rtc(),
        'console': console.screen_test(),
        'rs232': rs232.send_and_receive(),
        'gpio': gpio.run(),
        'watchdog': subprocess.run(["ls", "/dev/watchdog"], capture_output=True, text=True)
    }

def log_test_results(results: Dict[str, Any]) -> None:
    TestResults.write("Hardware Test Results")
    TestResults.write("=" * 50)
    status_map = {
        'network': ('Network', results['network'] == 0),
        'usb': ('USB', results['usb'] == 0),
        'can': ('CAN', results['can'] == 0),
        'i2c': ('I2C', results['i2c'] is True),
        'rtc': ('RTC', results['rtc'] is not None),
        'console': ('USB Console', results['console'] == 0),
        'rs232': ('RS232', results['rs232'] is not None),
        'gpio': ('GPIO', results['gpio'] is not None)
    }
    for test_name, (display_name, status) in status_map.items():
        result = "[OK]" if status else "[FAILED]"
        TestResults.write(f"{display_name:<{STATUS_WIDTH}} {result}")
    logging.info(f"Watchdog status: {results['watchdog'].stdout}")

def main() -> None:
    if TestResults.exists():
        TestResults.write(f"{'Watchdog':<{STATUS_WIDTH}} [OK]")
        if content := TestResults.read():
            logging.info("\n" + content)
        TestResults.clear()
    else:
        results = run_hardware_tests()
        log_test_results(results)
        test_watchdog()

if __name__ == "__main__":
    main()
