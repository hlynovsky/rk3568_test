import logging
import serial as pyserial

class Console:
    speed = 1500000

    def __init__(self):
        pass

    def screen_test(self):
        try:
            # Открываем соединение с устройством
            with pyserial.Serial('/dev/ttyUSB0', self.speed, timeout=1) as ser:
                if ser.is_open:
                    logging.info("Connection to USB console is successful")
                    return 0
                else:
                    logging.error("Failed to open connection to USB console")
                    return 1

        except pyserial.SerialException as e:
            logging.error(f"Serial connection failed: {e}")
            return 1

        except FileNotFoundError:
            logging.error("Device /dev/ttyUSB0 not found. Check the connection")
            return 1

