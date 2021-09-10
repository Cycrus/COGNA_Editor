"""
Neuron.py

A class containing the neuron entities.

Author: Cyril Marx
Date: 09.09.2021
"""

from src.ParameterHandler import *

class Neuron:
    def __init__(self, id, posx, posy, size, network_id, subnet_id=-1, function="neuron"):
        """
        Constructor. Creates a neuron entity.
        :param id:          The ID of the new neuron.
        :param posx:        The x position of the new neuron.
        :param posy:        The y position of the new neuron.
        :param network_id:  The ID of the opened network where the neuron should be inserted.
        :param subnet_id:   The ID of the subnetwork the neuron belongs to. Is -1 if it belongs to the network itself
                            and not to a subnetwork.
        :param function:    The function of the new neuron.
        :return:            None
        """
        self.posx = posx
        self.posy = posy
        self.size = size
        self.network_id = network_id

        self.id = id

        self.subnet_id = subnet_id
        self.function = function

        if function == "neuron" or function == "interface_input" or function == "interface_output" or \
                function == "subnet_input" or function == "subnet_output":
            self.param = ParameterHandler()
        else:
            self.param = None

        if function == "interface_input":
            self.param.list["port"] = 40001
            self.param.list["ip_address"] = "0.0.0.0"
        elif function == "interface_output":
            self.param.list["port"] = 40002
