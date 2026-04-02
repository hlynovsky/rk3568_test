import serial
import time
import logging
from typing import Optional


class RS232:
    def __init__(self, port: str = '/dev/ttyS8', baudrate: int = 9600, timeout: float = 1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial: Optional[serial.Serial] = None

    def connect(self) -> bool:
        try:
            if self.serial and self.serial.is_open:
                self.serial.close()

            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout
            )
            logging.info(f"Connected to {self.port} at {self.baudrate} baud")
            return True
        except Exception as e:
            logging.error(f"Connection error to {self.port}: {e}")
            return False

    def is_connected(self) -> bool:
        return self.serial is not None and self.serial.is_open

    def send(self, data: str) -> bool:
        if not self.is_connected():
            logging.error("Cannot send data: port is not connected.")
            return False
        try:
            self.serial.reset_output_buffer()
            self.serial.write(data.encode())
            logging.info(f"Sent: {data}")
            return True
        except Exception as e:
            logging.error(f"Error sending data: {e}")
            return False

    def receive(self, expected_len: int) -> str:
        received = b''
        start_time = time.time()
        try:
            while time.time() - start_time < self.timeout and len(received) < expected_len:
                waiting = self.serial.in_waiting
                if waiting:
                    logging.debug(f"in_waiting = {waiting}")
                    chunk = self.serial.read(waiting)
                    logging.debug(f"Read chunk: {repr(chunk)}")
                    received += chunk

            duration = time.time() - start_time
            result = received.decode(errors='replace')
            logging.info(f"Received: {result}")
            logging.debug(f"Receive duration: {duration:.3f} seconds")
            logging.debug(f"Received (raw): {repr(received)}")
            return result
        except Exception as e:
            logging.error(f"Error receiving data: {e}")
            return ""

    def send_and_receive(self, data: str = "1") -> int:
        """
        Отправка и прием данных в режиме loopback.
        Возвращает:
            0 - успех
            1 - ошибка
        """
        if not self.is_connected():
            if not self.connect():
                return 1

        self.serial.reset_input_buffer()
        self.send(data)
        response = self.receive(len(data))

        if not response:
            logging.error("No data received (loopback connection failed)")
            return 1

        if response == data:
            logging.info("RS232 loopback test PASSED")
            return 0
        else:
            logging.error(f"RS232 loopback test FAILED - expected '{data}', got '{response}'")
            return 1

    def close(self) -> None:
        try:
            if self.is_connected():
                self.serial.close()
                logging.info(f"Port {self.port} closed")
        except Exception as e:
            logging.error(f"Error closing port: {e}")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
