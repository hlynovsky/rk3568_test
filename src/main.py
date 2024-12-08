from network import Network

interfaces = ['eth0', 'eth1']
network = Network(interfaces)
network.ping()