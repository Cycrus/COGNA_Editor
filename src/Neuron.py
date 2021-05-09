from src.ParameterHandler import *

class Neuron:
    def __init__(self, id, posx, posy, size, network_id, subnet_id=-1, function="neuron"):
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
