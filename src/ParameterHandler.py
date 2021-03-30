neuron_activation_parameter = ("activation_threshold", #numeric
                               "max_activation", #numeric
                               "min_activation", #numeric
                               "activation_backfall_curvature", #numeric
                               "activation_backfall_steepness") #numeric

neuron_transmitter_parameter = ("influences_transmitter", #int<No:0, Yes:1>
                                "influenced_transmitter", #int<Possible transmitters:?>
                                "transmitter_change_curvature", #numeric
                                "transmitter_change_steepness", #numeric
                                "transmitter_influence_direction") #int<Positive influence:1, Negative influence:-1>

neuron_random_parameter = ("random_chance", #integer
                           "random_activation_value") #numeric

connection_habituation_parameter = ("habituation_threshold", #numeric
                                    "short_habituation_curvature", #numeric
                                    "short_habituation_steepness", #numeric
                                    "short_dehabituation_curvature", #numeric
                                    "short_dehabituation_steepness", #numeric
                                    "long_habituation_curvature", #numeric
                                    "long_habituation_steepness", #numeric
                                    "long_dehabituation_curvature", #numeric
                                    "long_dehabituation_steepness") #numeric

connection_sensitization_parameter = ("sensitization_threshold", #numeric
                                      "short_sensitization_curvature", #numeric
                                      "short_sensitization_steepness", #numeric
                                      "short_desensitization_curvature", #numeric
                                      "short_desensitization_steepness", #numeric
                                      "long_sensitization_curvature", #numeric
                                      "long_sensitization_steepness", #numeric
                                      "long_desensitization_curvature", #numeric
                                      "long_desensitization_steepness") #numeric

connection_presynaptic_parameter = ("presynaptic_potential_curvature", #numeric
                                    "presynaptic_potential_steepness", #numeric
                                    "presynaptic_backfall_curvature", #numeric
                                    "presynaptic_backfall_steepness") #numeric

connection_special_parameter = ("base_weight", #numeric
                                "max_weight", #numeric
                                "min_weight", #numeric
                                "activation_type", #int<Excitatory:1, Inhibitory:-1, Nondirectional:0>
                                "activation_function", #int<1:Sigmoid, 2:Linear, 3:relu>
                                "learning_type", #int<None:1, Habituation:2, Sensitization:3, Habisens:4>
                                "transmitter_type") #int<Std transmitter:0, Possible transmitters:?>

network_parameter = ("transmitter_number",
                     "transmitter_backfall_curvature",
                     "transmitter_backfall_steepness",
                     "max_transmitter_weight",
                     "min_transmitter_weight")

class ParameterHandler:
    def __init__(self):
        self.list = {}
        for idx, name in enumerate(connection_special_parameter):
            self.list[name] = None
        for idx, name in enumerate(connection_habituation_parameter):
            self.list[name] = None
        for idx, name in enumerate(connection_sensitization_parameter):
            self.list[name] = None
        for idx, name in enumerate(connection_presynaptic_parameter):
            self.list[name] = None
        for idx, name in enumerate(neuron_activation_parameter):
            self.list[name] = None
        for idx, name in enumerate(neuron_transmitter_parameter):
            self.list[name] = None
        for idx, name in enumerate(neuron_random_parameter):
            self.list[name] = None
        for idx, name in enumerate(network_parameter):
            self.list[name] = None