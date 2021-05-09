try:
    import numpy as np
except:
    print("[ERROR] Missing package. Install package <numpy> first.")

from src.ParameterHandler import *


class Connection:
    def __init__(self, id, source_neuron, network_id):
        self.id = id
        self.vertices = []
        self.prev_neuron = source_neuron.id
        self.prev_subnet = source_neuron.subnet_id
        self.vertices.append(np.array([source_neuron.posx, source_neuron.posy]))
        self.network_id = network_id

        self.next_neuron = None
        self.next_subnet = None
        self.next_connection = None

        self.param = ParameterHandler()
