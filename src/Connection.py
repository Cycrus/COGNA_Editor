try:
    import numpy as np
except:
    print("[ERROR] Missing package. Install package <numpy> first.")

from src.ParameterHandler import *

connection_parameter = ("Activation type",
                        "Activation function",
                        "Learning type",
                        "Transmitter type",
                        "Base weight",
                        "Short weight",
                        "Long weight",
                        "Long learning weight",
                        "Presynaptic potential")

class Connection:
    def __init__(self, id, source_neuron):
        self.id = id
        self.vertices = []
        self.prev_neuron = source_neuron.id
        self.vertices.append(np.array([source_neuron.posx, source_neuron.posy]))

        self.next_neuron = None
        self.next_connection = None

        self.param = ParameterHandler()

        self.specific_parameter = {}
        for idx, name in enumerate(connection_parameter):
            self.specific_parameter[name] = 0.0
