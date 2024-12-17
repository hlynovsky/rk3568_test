import logging
import subprocess
import re

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('logs/test.log'),
#         logging.StreamHandler()
#     ]
# )

class I2C():


    def __init__(self):
        self.devices_example = """
                            i2c-3   i2c             rk3x-i2c                                I2C adapter
                            i2c-6   i2c             DP-AUX                                  I2C adapter
                            i2c-4   i2c             rk3x-i2c                                I2C adapter
                            i2c-0   i2c             rk3x-i2c                                I2C adapter
                            i2c-7   i2c             DesignWare HDMI                         I2C adapter
                            i2c-5   i2c             rk3x-i2c                                I2C adapter
                            """
        self.eeprom_example =  """
                                0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f    0123456789abcdef
                            00: 28 ac 80 80 01 80 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    (?????++++++++++
                            10: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            20: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            30: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            40: 28 ac 80 80 01 80 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    (?????++++++++++
                            50: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            60: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            70: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            80: 28 ac 80 80 01 80 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    (?????++++++++++
                            90: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            a0: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            b0: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            c0: 28 ac 80 80 01 80 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    (?????++++++++++
                            d0: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            e0: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            f0: 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b 2b    ++++++++++++++++
                            """
        
    def read_devices(self):
        devices = subprocess.run(["i2cdetect", "-l"], capture_output=True, text=True)
        return devices.stdout

    def read_eeprom(self):
        eeprom = subprocess.run(["i2cdump", "-y", "0", "0x60"], capture_output=True, text=True)
        return eeprom.stdout

    def normalize(self, text):
        return "\n".join(
            re.sub(r'\s+', ' ', line.strip()) for line in text.strip().splitlines()
        )

    def run(self):
        current_devices = self.read_devices()
        current_eeprom = self.read_eeprom()

        if self.normalize(self.devices_example) == self.normalize(current_devices):
            logging.debug("i2c devices are the same")
            logging.debug("Current: \n" + self.normalize(current_devices))
            logging.debug("Example: \n" + self.normalize(self.devices_example))
            i2c_status = True
        else:
            logging.debug("Devices are different")
            logging.debug("Current: \n" + self.normalize(current_devices))
            logging.debug("Example: \n" + self.normalize(self.devices_example))
            return 1

        if self.normalize(current_eeprom) == self.normalize(self.eeprom_example):
            logging.debug("EEPROM is the same")
            logging.debug("Current: \n" + self.normalize(self.eeprom_example))
            logging.debug("Example: \n" + self.normalize(current_eeprom))
            eeprom_status = True
            return i2c_status, eeprom_status
        else:
            logging.debug("EEPROM is different")
            logging.debug("Current: \n" + self.normalize(self.eeprom_example))
            logging.debug("Example: \n" + self.normalize(current_eeprom))
            return 1