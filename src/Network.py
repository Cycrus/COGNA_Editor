from src.ParameterHandler import *

network_parameter = ("Transmitter count",
                     "Transmitter change curvature",
                     "Transmitter change steepness",
                     "Transmitter backfall curvature",
                     "Transmitter backfall steepness")


class Network:
    def __init__(self):
        self.neurons = []
        self.connections = []

        self.param = ParameterHandler()

        self.specific_parameter = {}
        for idx, name in enumerate(network_parameter):
            if idx == 0:
                self.specific_parameter[name] = 1
            else:
                self.specific_parameter[name] = 0.0
