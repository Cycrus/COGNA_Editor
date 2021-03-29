from src.ParameterHandler import *


class Neuron:
    def __init__(self, id, posx, posy, size, network_id):
        self.posx = posx
        self.posy = posy
        self.size = size
        self.network_id = network_id

        self.id = id

        self.param = ParameterHandler()
