import logging
import subprocess

class Rtc():
    def __init__(self):
        self.rtc_path = "/dev/rtc1"

    def read_rtc(self):
        try: 
            result = subprocess.run(["sudo", "hwclock", "--show", "--rtc", self.rtc_path], check=True, capture_output=True)
            logging.info(f"RTC time from {self.rtc_path}: {result.stdout}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.error(f"Error reading RTC: {e}")
            return None