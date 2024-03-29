"""
Network.py

The class handling the informations and parameters for the network.

Author: Cyril Marx
Date: 09.09.2021
"""

from src.ParameterHandler import *


class Network:
    def __init__(self, default_params=None):
        """
        Constructor.
        :param default_params:  The default parameters stored in the networks parameter.
        :return:                None
        """
        self.neurons = []
        self.nodes = []
        self.all_nodes = [self.neurons, self.nodes]
        self.connections = []
        self.subnets = []

        self.param = ParameterHandler()

        if default_params is not None:
            self.param = default_params
        else:
            self.param.list["transmitter_backfall_curvature"] = 1.0
            self.param.list["transmitter_backfall_steepness"] = 0.0000001
            self.param.list["max_transmitter_weight"] = 5.0
            self.param.list["min_transmitter_weight"] = 0.0
            self.param.list["input_nodes"] = 0
            self.param.list["output_nodes"] = 0
