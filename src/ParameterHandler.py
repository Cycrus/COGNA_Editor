neuron_activation_parameter = ("Activation threshold",
                               "Max activation",
                               "Min activation",
                               "Activation Backfall curvature",
                               "Activation Backfall steepness")

neuron_transmitter_parameter = ("Transmitter change curvature",
                                "Transmitter change steepness",
                                "Influenced transmitter",
                                "Transmitter influence direction")

neuron_random_parameter = ("Random chance",
                           "Random activation value")

connection_habituation_parameter = ("Habituation threshold",
                                    "Short habituation curvature",
                                    "Short habituation steepness",
                                    "Short dehabituation curvature",
                                    "Short dehabituation steepness",
                                    "Long habituation curvature",
                                    "Long habituation steepness",
                                    "Long dehabituation curvature",
                                    "Long dehabituation steepness")

connection_sensitization_parameter = ("Sensitization threshold",
                                      "Short sensitization curvature",
                                      "Short sensitization steepness",
                                      "Short desensitization curvature",
                                      "Short desensitizationsteepness",
                                      "Long sensitization curvature",
                                      "Long sensitization steepness",
                                      "Long desensitization curvature",
                                      "Long desensitization steepness")

connection_presynaptic_parameter = ("Presynaptic potential curvature",
                                    "Presynaptic potential steepness",
                                    "Presynaptic backfall curvature",
                                    "Presynaptic backfall steepness")

connection_special_parameter = ("Base weight",
                                "Max weight",
                                "Min weight",
                                "Activation type",
                                "Activation function",
                                "Learning type",
                                "Transmitter type")

network_parameter = ("Transmitter Number",
                     "Transmitter backfall curvature",
                     "Transmitter backfall steepness",
                     "Max transmitter weight",
                     "Min transmitter weight")


class ParameterHandler:
    def __init__(self):
        self.list = {}
        for idx, name in enumerate(connection_special_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(connection_habituation_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(connection_sensitization_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(connection_presynaptic_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(neuron_activation_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(neuron_transmitter_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(neuron_random_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(network_parameter):
            self.list[name] = 0.0
