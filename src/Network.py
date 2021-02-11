from src.ParameterHandler import *

class Network:
    def __init__(self):
        self.neurons = []
        self.connections = []

        self.param = ParameterHandler()

        self.transmitter_count = 1
        self.transmitter_change_curvature = 0.0
        self.transmitter_change_steepness = 0.0
        self.transmitter_backfall_curvature = 0.0
        self.transmitter_backfall_steepness = 0.0
