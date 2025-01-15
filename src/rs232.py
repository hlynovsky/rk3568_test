import serial
import time
import logging
from typing import Optional

class RS232:
    def __init__(self, port='/dev/ttyS8', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.connect()
    
    def connect(self) -> None:
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
        except Exception as e:
            logging.error(e)

    def is_connected(self) -> bool:
        return self.serial is not None and self.serial.is_open
    
    def send_and_receive(self, data: str = "123") -> Optional[str]:
        if not self.is_connected():
            logging.error("serial port not connected")
            return 1
        
        try:
            self.serial.write(data.encode())
            time.sleep(0.1)
            received = self.serial.read(len(data))
            logging.info(f"RS232 - Sent and received: {received.decode()} successfull!")

            if not received:
                logging.error("no data received (timeout)")
                return 1
            
            self.close()
            return 0
        
            
            
        except serial.SerialException as e:
            logging.error(f"serial port not connected: {e}")
            return 1
        except UnicodeError as e:
            logging.error(f"data encoding/decoding error: {e}")
            return 1
    
    def close(self) -> None:
        try:
            if self.is_connected():
                self.serial.close()
        except serial.SerialException as e:
            logging.error(f"error closing port: {e}")
            return 1

# if __name__ == "__main__":
#     try:
#         rs232 = RS232()
#         result = rs232.send_and_receive()
#         print(f"Sent and received: {result}")
#     except serial.SerialException as e:
#         print(f"Error: {str(e)}")
#     finally:
#         if 'rs232' in locals():
#             rs232.close()
