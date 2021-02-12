from src.ParameterHandler import *

neuron_parameter = ("Random chance",
                    "Random activation value",
                    "Influenced transmitter",
                    "Transmitter influence direction")


class Neuron:
    def __init__(self, id, posx, posy, image):
        self.posx = posx
        self.posy = posy
        self.img_width = image.width()
        self.img_height = image.height()

        self.id = id

        self.param = ParameterHandler()

        self.specific_parameter = {}
        for idx, name in enumerate(neuron_parameter):
            self.specific_parameter[name] = 0.0
