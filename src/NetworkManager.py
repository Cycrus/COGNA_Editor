from src.Network import *
from src.Neuron import *
from src.Connection import *

null_neuron_correcter = 1


class NetworkManager:
    def __init__(self):
        self.networks = []
        self.networks.append(Network())

    def add_neuron(self, posx, posy, size, network_id=0):
        self.networks[network_id].neurons.append(Neuron(len(self.networks[network_id].neurons)+null_neuron_correcter,
                                                        posx, posy, size, network_id))

    def delete_neuron(self, id, network_id=0):
        for connection in reversed(self.networks[network_id].connections):
            if connection.prev_neuron == id or connection.next_neuron == id:
                self.delete_connection(connection.id, network_id)

        for connection in self.networks[network_id].connections:
            if connection.prev_neuron > id-1:
                connection.prev_neuron = connection.prev_neuron - 1
            if connection.next_neuron > id-1:
                connection.next_neuron = connection.next_neuron - 1

        self.networks[network_id].neurons.pop(id - 1)
        for neuron in reversed(self.networks[network_id].neurons):
            if neuron.id > id:
                neuron.id = neuron.id - 1

    def add_connection(self, source_neuron, network_id=0):
        self.networks[network_id].connections.append(Connection(len(self.networks[network_id].connections),
                                                                source_neuron, network_id))

    def delete_connection(self, id, network_id=0):
        for connection in self.networks[network_id].connections:
            if connection.next_connection == id:
                self.delete_connection(connection.id, network_id)
        self.networks[network_id].connections.pop(id)
        for connection in reversed(self.networks[network_id].connections):
            if connection.id > id:
                connection.id = connection.id - 1