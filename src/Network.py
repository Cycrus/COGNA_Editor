from src.ParameterHandler import *


class Network:
    def __init__(self, default_params=None):
        self.neurons = []
        self.connections = []

        self.param = ParameterHandler()

        if default_params is not None:
            self.param = default_params
        else:
            self.param.list["activation_threshold"] = 1.0
            self.param.list["used_transmitter"] = "Default"
            self.param.list["max_activation"] = 50.0
            self.param.list["min_activation"] = 0.0
            self.param.list["activation_backfall_curvature"] = 1.0
            self.param.list["activation_backfall_steepness"] = 0.04

            self.param.list["transmitter_change_curvature"] = 1.02
            self.param.list["transmitter_change_steepness"] = 0.02
            self.param.list["influenced_transmitter"] = "None"
            self.param.list["influences_transmitter"] = "No"
            self.param.list["transmitter_influence_direction"] = "Positive Influence"

            self.param.list["random_chance"] = 0
            self.param.list["random_activation_value"] = 0.0

            self.param.list["habituation_threshold"] = 0.001
            self.param.list["short_habituation_curvature"] = 0.65
            self.param.list["short_habituation_steepness"] = 0.07
            self.param.list["short_dehabituation_curvature"] = 1.0
            self.param.list["short_dehabituation_steepness"] = 0.00000005
            self.param.list["long_habituation_curvature"] = 0.35
            self.param.list["long_habituation_steepness"] = 0.00005
            self.param.list["long_dehabituation_curvature"] = 1.0
            self.param.list["long_dehabituation_steepness"] = 0.000000000001

            self.param.list["sensitization_threshold"] = 5.0
            self.param.list["short_sensitization_curvature"] = 0.65
            self.param.list["short_sensitization_steepness"] = 0.07
            self.param.list["short_desensitization_curvature"] = 1.0
            self.param.list["short_desensitization_steepness"] = 0.00000005
            self.param.list["long_sensitization_curvature"] = 1.02
            self.param.list["long_sensitization_steepness"] = 0.0001
            self.param.list["long_desensitization_curvature"] = 1.0
            self.param.list["long_desensitization_steepness"] = 0.000000000001

            self.param.list["presynaptic_potential_curvature"] = 0.60
            self.param.list["presynaptic_potential_steepness"] = 0.3
            self.param.list["presynaptic_backfall_curvature"] = 1.00
            self.param.list["presynaptic_backfall_steepness"] = 0.0000002

            self.param.list["base_weight"] = 1.0
            self.param.list["max_weight"] = 5.0
            self.param.list["min_weight"] = 0.0
            self.param.list["activation_type"] = "Excitatory"
            self.param.list["activation_function"] = "Relu"
            self.param.list["learning_type"] = "None"

            self.param.list["transmitter_type"] = "Default"
            self.param.list["transmitter_number"] = 1
            self.param.list["transmitter_backfall_curvature"] = 1.0
            self.param.list["transmitter_backfall_steepness"] = 0.0000001
            self.param.list["max_transmitter_weight"] = 5.0
            self.param.list["min_transmitter_weight"] = 0.0
