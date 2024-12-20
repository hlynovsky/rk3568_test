import logging
import subprocess
import re

class I2C():


    def __init__(self):
        self.devices_example = """
                            i2c-0   i2c             rk3x-i2c                                I2C adapter
                            i2c-3   i2c             rk3x-i2c                                I2C adapter
                            i2c-4   i2c             rk3x-i2c                                I2C adapter
                            i2c-5   i2c             rk3x-i2c                                I2C adapter
                            i2c-6   i2c             DP-AUX                                  I2C adapter
                            i2c-7   i2c             DesignWare HDMI                         I2C adapter
                            """
        
    def read_devices(self):
        devices = subprocess.run(["i2cdetect", "-l"], capture_output=True, text=True)
        return devices.stdout

    def normalize(self, text):
        return "\n".join(
            re.sub(r'\s+', ' ', line.strip()) for line in text.strip().splitlines()
        )

    def run(self):
        current_devices = self.read_devices()

        if self.normalize(self.devices_example) == self.normalize(current_devices):
            logging.debug("i2c devices are the same")
            logging.debug("Current: \n" + self.normalize(current_devices))
            logging.debug("Example: \n" + self.normalize(self.devices_example))
            i2c_status = True
            return i2c_status
        else:
            logging.debug("Devices are different")
            logging.debug("Current: \n" + self.normalize(current_devices))
            logging.debug("Example: \n" + self.normalize(self.devices_example))
            return 1