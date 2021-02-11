from src.ParameterHandler import *

class Neuron:
    def __init__(self, id, posx, posy, image):
        self.posx = posx
        self.posy = posy
        self.img_width = image.width()
        self.img_height = image.height()

        self.param = ParameterHandler()

        self.id = id
        self.random_chance = None
        self.random_activation_value = None
        self.influenced_transmitter = None
        self.transmitter_influence_direction = None
