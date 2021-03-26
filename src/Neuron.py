from src.ParameterHandler import *


class Neuron:
    def __init__(self, id, posx, posy, size):
        self.posx = posx
        self.posy = posy
        self.size = size

        self.id = id

        self.param = ParameterHandler()
