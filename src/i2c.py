import logging
import subprocess
import re

class I2C:
    def __init__(self):
        self.devices_example = """
            i2c-0   i2c             rk3x-i2c                                I2C adapter
            i2c-3   i2c             rk3x-i2c                                I2C adapter
            i2c-4   i2c             rk3x-i2c                                I2C adapter
            i2c-5   i2c             rk3x-i2c                                I2C adapter
            i2c-6   i2c             DP-AUX                                  I2C adapter
            i2c-7   i2c             DesignWare HDMI                         I2C adapter
        """

    def read_devices(self) -> str:
        result = subprocess.run(["i2cdetect", "-l"], capture_output=True, text=True)
        return result.stdout.strip()

    def normalize_set(self, text: str) -> set:
        return set(
            re.sub(r'\s+', ' ', line.strip()) for line in text.strip().splitlines() if line.strip()
        )

    def run(self) -> bool:
        current_devices = self.read_devices()
        current_set = self.normalize_set(current_devices)
        example_set = self.normalize_set(self.devices_example)

        if current_set == example_set:
            logging.debug("I2C devices match the expected configuration.")
            return True
        else:
            logging.warning("I2C device mismatch detected.")
            logging.debug("Expected devices:")
            for line in sorted(example_set):
                logging.debug(f"  {line}")
            logging.debug("Current devices:")
            for line in sorted(current_set):
                logging.debug(f"  {line}")
            missing = example_set - current_set
            extra = current_set - example_set
            if missing:
                logging.warning("Missing devices:")
                for line in sorted(missing):
                    logging.warning(f"  {line}")
            if extra:
                logging.warning("Unexpected devices:")
                for line in sorted(extra):
                    logging.warning(f"  {line}")
            return False
