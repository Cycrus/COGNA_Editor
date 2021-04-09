from src.GlobalLibraries import *

neuron_activation_parameter = ("activation_threshold", #numeric
                               "used_transmitter", #String<Possible transmitter:?>
                               "max_activation", #numeric
                               "min_activation", #numeric
                               "activation_backfall_curvature", #numeric
                               "activation_backfall_steepness") #numeric

neuron_transmitter_parameter = ("influences_transmitter", #String<No:0, Yes:1>
                                "influenced_transmitter", #String<Possible transmitters:?>
                                "transmitter_change_curvature", #numeric
                                "transmitter_change_steepness", #numeric
                                "transmitter_influence_direction") #String<Positive influence:1, Negative influence:-1>

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
                                "activation_type", #String<Excitatory:1, Inhibitory:-1, Nondirectional:0>
                                "activation_function", #String<1:Sigmoid, 2:Linear, 3:relu>
                                "learning_type", #String<None:1, Habituation:2, Sensitization:3, Habisens:4>
                                "transmitter_type") #String<Possible transmitters:?>

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

    @staticmethod
    def correct_parameter_print(entity, name):
        if name == "transmitter_type" or name == "used_transmitter" or name == "learning_type" or \
                name == "activation_function" or name == "activation_type" or name == "transmitter_influence_direction" or \
                name == "influences_transmitter" or name == "influenced_transmitter":
            string_value = entity.list[name]
        else:
            regex = re.compile("(-?[0-9]*(\.[0 -9]*[1-9])?)", re.IGNORECASE)
            param_str = regex.findall(format(entity.list[name], ".15f"))
            string_value = param_str[0][0]

        return string_value
