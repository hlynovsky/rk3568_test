from network import Network
from plyer import notification
import os

class Main:

    def __init__(self):
        self.eth0 = Network('eth0')
        self.eth1 = Network('eth1')
        self.log_file = '/home/e6aluga/Desktop/rk3568_test/logs/network_logs.txt'

    def check_network(self):
        eth0_status = self.ping_network(self.eth0, 'eth0')
        eth1_status = self.ping_network(self.eth1, 'eth1')
        self.show_notification('eth0', eth0_status)
        self.show_notification('eth1', eth1_status)

    def ping_network(self, network, interface):
        try:
            network.ping()
            return True
        except Exception as e:
            self.write_log(f'{interface} - Error: {e}')
            return False

    def write_log(self, message):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, 'a') as log:
            log.write(f'{message}\n')

    def show_notification(self, interface, status):
        if status:
            message = f'{interface} - OK'
        else:
            message = f'{interface} - Error, logs in {self.log_file}'

        notification.notify(
            title=f'Результат для {interface}',
            message=message,
            timeout=120
        )


main = Main()
main.check_network()
