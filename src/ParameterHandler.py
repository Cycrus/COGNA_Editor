neuron_activation_parameter = ("Activation threshold", #numeric
                               "Max activation", #numeric
                               "Min activation", #numeric
                               "Activation Backfall curvature", #numeric
                               "Activation Backfall steepness") #numeric

neuron_transmitter_parameter = ("Transmitter change curvature", #numeric
                                "Transmitter change steepness", #numeric
                                "Influenced transmitter", #int<Possible transmitters:?>
                                "Transmitter influence direction") #int<Positive influence:1, Negative influence:-1>

neuron_random_parameter = ("Random chance", #integer
                           "Random activation value") #numeric

connection_habituation_parameter = ("Habituation threshold", #numeric
                                    "Short habituation curvature", #numeric
                                    "Short habituation steepness", #numeric
                                    "Short dehabituation curvature", #numeric
                                    "Short dehabituation steepness", #numeric
                                    "Long habituation curvature", #numeric
                                    "Long habituation steepness", #numeric
                                    "Long dehabituation curvature", #numeric
                                    "Long dehabituation steepness") #numeric

connection_sensitization_parameter = ("Sensitization threshold", #numeric
                                      "Short sensitization curvature", #numeric
                                      "Short sensitization steepness", #numeric
                                      "Short desensitization curvature", #numeric
                                      "Short desensitizationsteepness", #numeric
                                      "Long sensitization curvature", #numeric
                                      "Long sensitization steepness", #numeric
                                      "Long desensitization curvature", #numeric
                                      "Long desensitization steepness") #numeric

connection_presynaptic_parameter = ("Presynaptic potential curvature", #numeric
                                    "Presynaptic potential steepness", #numeric
                                    "Presynaptic backfall curvature", #numeric
                                    "Presynaptic backfall steepness") #numeric

connection_special_parameter = ("Base weight", #numeric
                                "Max weight", #numeric
                                "Min weight", #numeric
                                "Activation type", #int<Excitatory:1, Inhibitory:-1, Nondirectional:0>
                                "Activation function", #int<1:Sigmoid, 2:Linear, 3:relu>
                                "Learning type", #int<None:1, Habituation:2, Sensitization:3, Habisens:4>
                                "Transmitter type") #int<Std transmitter:0, Possible transmitters:?>

network_parameter = ("Transmitter Number",
                     "Transmitter backfall curvature",
                     "Transmitter backfall steepness",
                     "Max transmitter weight",
                     "Min transmitter weight")

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
