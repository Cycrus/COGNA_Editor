try:
    import numpy as np
except:
    print("[ERROR] Missing package. Install package <numpy> first.")

null_neuron_correcter = 1

class Neuron:
    def __init__(self, id, posx, posy, image):
        self.id = id
        self.posx = posx
        self.posy = posy
        self.image = image
        self.img_width = image.width()
        self.img_height = image.height()

        self.activation_threshold = None
        self.random_chance = None
        self.random_activation_value = None
        self.activation_backfall_curvature = None
        self.activation_backfall_steepness = None
        self.short_habituation_curvature = None
        self.short_habituation_steepness = None
        self.short_sensitization_curvature = None
        self.short_sensitization_steepness = None
        self.short_dehabituation_curvature = None
        self.short_dehabituation_steepness = None
        self.short_desensitization_curvature = None
        self.short_desensitization_steepness = None
        self.long_habituation_curvature = None
        self.long_habituation_steepness = None
        self.long_sensitization_curvature = None
        self.long_sensitization_steepness = None
        self.long_dehabituation_curvature = None
        self.long_dehabituation_steepness = None
        self.long_desensitization_curvature = None
        self.long_desensitization_steepness = None
        self.presynaptic_potential_curvature = None
        self.presynaptic_potential_steepness = None
        self.presynaptic_backfall_curvature = None
        self.presynaptic_backfall_steepness = None
        self.long_learning_weight_reduction_curvature = None
        self.long_learning_weight_reduction_steepness = None
        self.long_learning_weight_backfall_curvature = None
        self.long_learning_weight_backfall_steepness = None
        self.influenced_transmitter = None
        self.transmitter_influence_direction = None
        self.habituation_threshold = None
        self.sensitization_threshold = None


class Connection:
    def __init__(self, id, source_neuron):
        self.id = id
        self.vertices = []
        self.prev_neuron = source_neuron.id
        self.vertices.append(np.array([source_neuron.posx, source_neuron.posy]))

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


class Network:
    def __init__(self):
        self.neurons = []
        self.connections = []

        self.global_activation_threshold = 0.0
        self.transmitter_count = 1
        self.global_max_activation = 0.0
        self.global_min_activation = 0.0
        self.global_max_weight = 0.0
        self.global_min_weight = 0.0
        self.global_backfall_curvature = 0.0
        self.global_backfall_steepness = 0.0
        self.global_max_transmitter_weight = 0.0
        self.global_min_transmitter_weight = 0.0
        self.global_short_habituation_curvature = 0.0
        self.global_short_habituation_steepness = 0.0
        self.global_short_sensitization_curvature = 0.0
        self.global_short_sensitization_steepness = 0.0
        self.global_short_dehabituation_curvature = 0.0
        self.global_short_dehabituation_steepness = 0.0
        self.global_short_desensitization_curvature = 0.0
        self.global_short_desensitization_steepness = 0.0
        self.global_long_habituation_curvature = 0.0
        self.global_long_habituation_steepness = 0.0
        self.global_long_sensitization_curvature = 0.0
        self.global_long_sensitization_steepness = 0.0
        self.global_long_dehabituation_curvature = 0.0
        self.global_long_dehabituation_steepness = 0.0
        self.global_long_desensitization_curvature = 0.0
        self.global_long_desensitization_steepness = 0.0
        self.global_presynaptic_potential_curvature = 0.0
        self.global_presynaptic_potential_steepness = 0.0
        self.global_presynaptic_backfall_curvature = 0.0
        self.global_presynaptic_backfall_steepness = 0.0
        self.global_long_learning_weight_reduction_curvature = 0.0
        self.global_long_learning_weight_reduction_steepness = 0.0
        self.global_long_learning_weight_backfall_curvature = 0.0
        self.global_long_learning_weight_backfall_steepness = 0.0
        self.global_habituation_threshold = 0.0
        self.global_sensitization_threshold = 0.0
        self.transmitter_change_curvature = 0.0
        self.transmitter_change_steepness = 0.0
        self.transmitter_backfall_curvature = 0.0
        self.transmitter_backfall_steepness = 0.0


class NetworkManager:
    def __init__(self):
        self.networks = []
        self.networks.append(Network())

    def add_neuron(self, posx, posy, image, network_id=0):
        self.networks[network_id].neurons.append(Neuron(len(self.networks[network_id].neurons)+null_neuron_correcter,
                                                        posx, posy, image))

    def delete_neuron(self, id, network_id=0):
        for connection in reversed(self.networks[network_id].connections):
            if connection.prev_neuron == id or connection.next_neuron == id:
                self.delete_connection(connection.id, network_id)

        for connection in self.networks[network_id].connections:
            if connection.prev_neuron > id-1:
                connection.prev_neuron = connection.prev_neuron - 1
            if connection.next_neuron > id-1:
                connection.next_neuron = connection.next_neuron - 1

        self.networks[network_id].neurons.pop(id - 1)
        for neuron in reversed(self.networks[network_id].neurons):
            if neuron.id > id:
                neuron.id = neuron.id - 1

    def add_connection(self, source_neuron, network_id=0):
        self.networks[network_id].connections.append(Connection(len(self.networks[network_id].connections),
                                                                source_neuron))

    def delete_connection(self, id, network_id=0):
        self.networks[network_id].connections.pop(id)
        for connection in reversed(self.networks[network_id].connections):
            if connection.id > id:
                connection.id = connection.id - 1