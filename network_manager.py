#!/usr/bin/python3

null_neuron_correcter = 1

class Neuron:
    activation_threshold = None
    random_chance = None
    random_activation_value = None
    activation_backfall_curvature = None
    activation_backfall_steepness = None
    short_habituation_curvature = None
    short_habituation_steepness = None
    short_sensitization_curvature = None
    short_sensitization_steepness = None
    short_dehabituation_curvature = None
    short_dehabituation_steepness = None
    short_desensitization_curvature = None
    short_desensitization_steepness = None
    long_habituation_curvature = None
    long_habituation_steepness = None
    long_sensitization_curvature = None
    long_sensitization_steepness = None
    long_dehabituation_curvature = None
    long_dehabituation_steepness = None
    long_desensitization_curvature = None
    long_desensitization_steepness = None
    presynaptic_potential_curvature = None
    presynaptic_potential_steepness = None
    presynaptic_backfall_curvature = None
    presynaptic_backfall_steepness = None
    long_learning_weight_reduction_curvature = None
    long_learning_weight_reduction_steepness = None
    long_learning_weight_backfall_curvature = None
    long_learning_weight_backfall_steepness = None
    influenced_transmitter = None
    transmitter_influence_direction = None
    habituation_threshold = None
    sensitization_threshold = None

    def __init__(self, id, posx, posy, image):
        self.id = id
        self.posx = posx
        self.posy = posy
        self.image = image
        self.img_width = image.width()
        self.img_height = image.height()


class Network:
    neurons = []
    global_activation_threshold = 0.0
    transmitter_count = 1
    global_max_activation = 0.0
    global_min_activation = 0.0
    global_max_weight = 0.0
    global_min_weight = 0.0
    global_backfall_curvature = 0.0
    global_backfall_steepness = 0.0
    global_max_transmitter_weight = 0.0
    global_min_transmitter_weight = 0.0
    global_short_habituation_curvature = 0.0
    global_short_habituation_steepness = 0.0
    global_short_sensitization_curvature = 0.0
    global_short_sensitization_steepness = 0.0
    global_short_dehabituation_curvature = 0.0
    global_short_dehabituation_steepness = 0.0
    global_short_desensitization_curvature = 0.0
    global_short_desensitization_steepness = 0.0
    global_long_habituation_curvature = 0.0
    global_long_habituation_steepness = 0.0
    global_long_sensitization_curvature = 0.0
    global_long_sensitization_steepness = 0.0
    global_long_dehabituation_curvature = 0.0
    global_long_dehabituation_steepness = 0.0
    global_long_desensitization_curvature = 0.0
    global_long_desensitization_steepness = 0.0
    global_presynaptic_potential_curvature = 0.0
    global_presynaptic_potential_steepness = 0.0
    global_presynaptic_backfall_curvature = 0.0
    global_presynaptic_backfall_steepness = 0.0
    global_long_learning_weight_reduction_curvature = 0.0
    global_long_learning_weight_reduction_steepness = 0.0
    global_long_learning_weight_backfall_curvature = 0.0
    global_long_learning_weight_backfall_steepness = 0.0
    global_habituation_threshold = 0.0
    global_sensitization_threshold = 0.0
    transmitter_change_curvature = 0.0
    transmitter_change_steepness = 0.0
    transmitter_backfall_curvature = 0.0
    transmitter_backfall_steepness = 0.0


class NetworkManager:
    networks = []

    def __init__(self):
        self.networks.append(Network())

    def add_neuron(self, posx, posy, image, network_id=0):
        self.networks[network_id].neurons.append(Neuron(len(self.networks[network_id].neurons)+null_neuron_correcter,
                                                        posx, posy, image))

    def delete_neuron(self, id, network_id=0):
        self.networks[network_id].neurons.pop(id-1)
        for neuron in self.networks[network_id].neurons:
            if neuron.id > id:
                neuron.id = neuron.id - 1
