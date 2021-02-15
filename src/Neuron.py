from src.ParameterHandler import *


class Neuron:
    def __init__(self, id, posx, posy, image):
        self.posx = posx
        self.posy = posy
        self.img_width = image.width()
        self.img_height = image.height()

        self.id = id

        self.param = ParameterHandler()
