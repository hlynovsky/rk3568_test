import logging
import serial as pyserial

class Console:
    def __init__(self, port='/dev/ttyUSB0', speed=1500000):
        self.port = port
        self.speed = speed

    def screen_test(self):
        try:
            with pyserial.Serial(self.port, self.speed, timeout=1) as ser:
                if ser.is_open:
                    logging.info(f"Connection to {self.port} at {self.speed} baud is successful")
                    return 0
                else:
                    logging.error(f"Failed to open connection to {self.port}")
                    return 1

        except pyserial.SerialException as e:
            logging.error(f"Serial connection to {self.port} failed: {e}")
            return 1

        except FileNotFoundError:
            logging.error(f"Device {self.port} not found. Check the connection.")
            return 1

