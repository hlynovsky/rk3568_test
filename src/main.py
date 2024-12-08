from network import Network

network_interfaces = ['eth0', 'eth1']
network = Network(network_interfaces)
network.ping()

