try:
    import numpy as np
except:
    print("[ERROR] Missing package. Install package <numpy> first.")

from src.ParameterHandler import *

class Connection:
    def __init__(self, id, source_neuron):
        self.id = id
        self.vertices = []
        self.prev_neuron = source_neuron.id
        self.vertices.append(np.array([source_neuron.posx, source_neuron.posy]))

        self.param = ParameterHandler()

        self.next_neuron = None
        self.next_connection = None
        self.activation_type = None
        self.activation_function = None
        self.learning_type = None
        self.transmitter_type = None
        self.base_weight = None
        self.short_weight = None
        self.long_weight = None
        self.long_learning_weight = None
        self.presynaptic_potential = None
