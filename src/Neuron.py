from src.ParameterHandler import *


class Neuron:
    def __init__(self, id, posx, posy, size, network_id, subnet_id=-1):
        self.posx = posx
        self.posy = posy
        self.size = size
        self.network_id = network_id

        self.id = id

        self.subnet_id = subnet_id

        if subnet_id == -1:
            self.param = ParameterHandler()
        else:
            self.param = None
