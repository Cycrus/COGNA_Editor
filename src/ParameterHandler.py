activation_parameter = ("Activation threshold",
                        "Max activation",
                        "Min activation",
                        "Backfall curvature",
                        "Backfall steepness")

weight_parameter = ("Max weight",
                    "Min weight",
                    "Long learning weight reduction curvature",
                    "Long learning weight reduction steepness",
                    "Long learning weight backfall curvature",
                    "Long learning weight backfall steepness"
                    "Max transmitter weight",
                    "Min transmitter weight")

habituation_parameter = ("Habituation threshold",
                         "Short habituation curvature",
                         "Short habituation steepness",
                         "Short dehabituation curvature",
                         "Short dehabituation steepness",
                         "Long habituation curvature",
                         "Long habituation steepness",
                         "Long dehabituation curvature",
                         "Long dehabituation steepness")

sensitization_parameter = ("Sensitization threshold",
                           "Short sensitization curvature",
                           "Short sensitization steepness",
                           "Short desensitization curvature",
                           "Short desensitization steepness",
                           "Long sensitization curvature",
                           "Long sensitization steepness",
                           "Long desensitization curvature",
                           "Long desensitization steepness")

presynaptic_parameter = ("Presynaptic potential curvature",
                         "Presynaptic potential steepness",
                         "Presynaptic backfall curvature",
                         "Presynaptic backfall steepness")


class ParameterHandler:
    def __init__(self):
        self.list = {}
        for idx, name in enumerate(activation_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(weight_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(habituation_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(sensitization_parameter):
            self.list[name] = 0.0
        for idx, name in enumerate(presynaptic_parameter):
            self.list[name] = 0.0
