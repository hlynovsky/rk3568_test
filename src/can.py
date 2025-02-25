import time
import subprocess
import threading
import logging

# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('logs/test.log'),
#         logging.StreamHandler()
#     ]
# )

class Can:
    def __init__(self, channel_0_name, channel_1_name, num_packets=5):
        self.channel_0_name = channel_0_name
        self.channel_1_name = channel_1_name
        self.num_packets = num_packets
        self.sent_packets = 0
        self.received_packets = 0

    def run_interfaces(self):
        try: 
            subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate", "500000"], check=True)
            subprocess.run(["sudo", "ip", "link", "set", "can1", "up", "type", "can", "bitrate", "500000"], check=True)
        except Exception as e:
            logging.warning(f"Error setting up can0 or can1 to 500000 baudrate (Probably already configured): {e}")

    def send_packet(self, channel, data):
        self.sent_packets += 1
        can_id = "123"
        can_frame = f"{can_id}#{data}"
        
        command = f"cansend {channel} {can_frame}"
        try:
            subprocess.run(command, shell=True, check=True)
            logging.info(f"send {can_frame} to {channel}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error sending packet from {channel}: {e}")

    def receive_packet(self, channel):
        command = f"candump {channel} -n 1"
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.PIPE).decode()
            logging.info(f"{channel}: {output.strip()}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error receiving packet on {channel}: {e}")

    def start_receiving(self):
        while True:
            self.receive_packet(self.channel_1_name)

    def test_channels(self):
        self.run_interfaces()
        logging.info(f"Testing packet transmission from {self.channel_0_name}...")

        receive_thread = threading.Thread(target=self.start_receiving)
        receive_thread.daemon = True
        receive_thread.start()

        time.sleep(1)

        for i in range(self.num_packets):
            data = f"{i:02X}"
            self.send_packet(self.channel_0_name, data)
            time.sleep(0.5)

        receive_thread.join(2)

        if self.sent_packets == self.num_packets:
            return 0
        else:
            logging.error(f"\nError: The channels are not functioning correctly.\n")
            return 1
