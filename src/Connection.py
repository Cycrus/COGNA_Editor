"""
Connection.py

The class representing the connections between neurons and nodes.

Author: Cyril Marx
Date: 09.09.2021
"""

try:
    import numpy as np
except:
    print("[ERROR] Missing package. Install package <numpy> first.")

from src.ParameterHandler import *


class Connection:
    def __init__(self, id, source_neuron, network_id):
        """
        Constructor.
        :param id:              The id of the new connection. IDs should always be consecutive values.
        :param source_neuron:   The object of the neuron or node the connection stems from.
        :param network_id:      The ID of the network the connection is supposed to be in.
        :return:                None
        """
        self.id = id
        self.vertices = []
        self.prev_neuron = source_neuron.id
        self.prev_subnet = source_neuron.subnet_id
        self.prev_neuron_function = source_neuron.function
        self.vertices.append(np.array([source_neuron.posx, source_neuron.posy]))
        self.network_id = network_id

        self.next_neuron = None
        self.next_subnet = None
        self.next_neuron_function = None
        self.next_connection = None

        self.param = ParameterHandler()
