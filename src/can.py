import time
import subprocess
import threading
import logging
from typing import Optional, Tuple

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("can_test.log", mode='w'),
        logging.StreamHandler()
    ]
)

class Can:
    def __init__(self, channel_0_name: str, channel_1_name: str, num_packets: int = 0):
        self.channel_0_name = channel_0_name
        self.channel_1_name = channel_1_name
        self.num_packets = num_packets
        self.sent_packets = 0
        self.received_packets = 0
        self._stop_event = threading.Event()
        self._receive_thread = None
        self._lock = threading.Lock()
        self._received_ids = set()

    def run_interfaces(self) -> bool:
        try:
            subprocess.run(["sudo", "ip", "link", "set", self.channel_0_name, "down"], 
                         stderr=subprocess.PIPE)
            subprocess.run(["sudo", "ip", "link", "set", self.channel_1_name, "down"],
                         stderr=subprocess.PIPE)

            commands = [
                ["sudo", "ip", "link", "set", self.channel_0_name, "up", "type", "can", "bitrate", "500000"],
                ["sudo", "ip", "link", "set", self.channel_1_name, "up", "type", "can", "bitrate", "500000"]
            ]
            for cmd in commands:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=2.0)
                if result.returncode != 0:
                    if "File exists" not in result.stderr:
                        logging.warning(f"Command failed: {' '.join(cmd)}\nError: {result.stderr.strip()}")
                        return False
            for interface in [self.channel_0_name, self.channel_1_name]:
                result = subprocess.run(["ip", "-d", "link", "show", interface], 
                                      capture_output=True, text=True)
                if "UP" not in result.stdout or "can" not in result.stdout:
                    logging.error(f"Interface {interface} not properly configured")
                    return False

            logging.info(f"CAN interfaces {self.channel_0_name} and {self.channel_1_name} configured successfully")
            return True
        except subprocess.TimeoutExpired:
            logging.error("Timeout while configuring CAN interfaces")
            return False
        except Exception as e:
            logging.error(f"Error setting up CAN interfaces: {e}")
            return False

    def send_packet(self, channel: str, data: str) -> bool:
        can_id = "123"
        can_frame = f"{can_id}#{data}"
        logging.debug(f"Sending packet to {channel}: {can_frame}")
        try:
            with self._lock:
                result = subprocess.run(
                    f"cansend {channel} {can_frame}",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=1.0
                )
                logging.debug(f"cansend stdout: {result.stdout.strip()}")
                logging.debug(f"cansend stderr: {result.stderr.strip()}")

                if result.returncode == 0:
                    self.sent_packets += 1
                    logging.debug(f"Successfully sent {can_frame} to {channel}")
                    return True
                else:
                    if "No such device" in result.stderr:
                        logging.error(f"CAN interface {channel} not found")
                    elif "Network is down" in result.stderr:
                        logging.error(f"CAN interface {channel} is down")
                    else:
                        logging.error(f"Failed to send packet to {channel}. Error: {result.stderr.strip()}")
                    return False
        except subprocess.TimeoutExpired:
            logging.error(f"Timeout while sending packet to {channel}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error sending packet to {channel}: {e}")
            return False

    def receive_packet(self, channel: str) -> Optional[str]:
        logging.debug(f"Attempting to receive packet on {channel}")
        try:
            result = subprocess.run(
                f"candump {channel} -n 1 -T 5000",
                shell=True,
                capture_output=True,
                text=True,
                timeout=6.0
            )

            logging.debug(f"candump stdout: {result.stdout.strip()}")
            logging.debug(f"candump stderr: {result.stderr.strip()}")

            if result.returncode == 0 and result.stdout.strip():
                output = result.stdout.strip()
                try:
                    packet_id = output.split()[1].split('#')[0]
                    with self._lock:
                        if packet_id not in self._received_ids:
                            self._received_ids.add(packet_id)
                            self.received_packets += 1
                            logging.debug(f"Received new packet from {channel}: {output}")
                        else:
                            logging.debug(f"Received duplicate packet from {channel}: {output}")
                            return None
                except (IndexError, AttributeError):
                    logging.warning(f"Malformed packet received: {output}")
                    return None
                return output
            else:
                logging.debug(f"candump returned no usable output on {channel}")
                return None
        except subprocess.TimeoutExpired:
            logging.debug(f"No packets received on {channel} within timeout")
            return None
        except Exception as e:
            logging.error(f"Error receiving packet on {channel}: {e}")
            return None

    def start_receiving(self) -> None:
        """Фоновый поток для приема пакетов."""
        logging.info(f"Starting receive thread for {self.channel_1_name}")
        while not self._stop_event.is_set():
            packet = self.receive_packet(self.channel_1_name)
            if packet:
                logging.debug(f"Processing packet: {packet}")
            time.sleep(0.05)

    def test_channels(self) -> int:
        self.sent_packets = 0
        self.received_packets = 0
        self._received_ids.clear()
        if not self.run_interfaces():
            logging.error("Failed to configure CAN interfaces")
            return 1

        logging.info(f"Testing packet transmission from {self.channel_0_name} to {self.channel_1_name}")

        self._stop_event.clear()
        self._receive_thread = threading.Thread(target=self.start_receiving)
        self._receive_thread.daemon = True
        self._receive_thread.start()

        time.sleep(1)
        data = "00"
        success = self.send_packet(self.channel_0_name, data)
        logging.info(f"Sent packet: {data}")
        time.sleep(3.0)
        self._stop_event.set()

        if self._receive_thread.is_alive():
            self._receive_thread.join(timeout=3.0)

        logging.info(f"\nTest results:")
        logging.info(f"Packets sent: {self.sent_packets}/1")
        logging.info(f"Unique packets received: {self.received_packets}/1")

        if self.sent_packets == 1 and self.received_packets == 1:
            logging.info("CAN channels are functioning correctly")
            return 0
        else:
            logging.warning("CAN channels test failed")
            return 1


