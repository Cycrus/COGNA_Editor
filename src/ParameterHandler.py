"""
ParameterHandler.py

Contains all information and methods required for using and changing COGNA parameter.

Author: Cyril Marx
Date: 09.09.2021
"""

from src.GlobalLibraries import *

neuron_activation_parameter = ["neuron_type", #String<Possible neuron types:?>
                               "activation_threshold", #numeric
                               "max_activation", #numeric
                               "min_activation", #numeric
                               "activation_backfall_curvature", #numeric
                               "activation_backfall_steepness"] #numeric

neuron_transmitter_parameter = ["influences_transmitter", #String<No:0, Yes:1>
                                "influenced_transmitter", #String<Possible transmitters:?>
                                "transmitter_change_curvature", #numeric
                                "transmitter_change_steepness", #numeric
                                "transmitter_influence_direction"] #String<Positive influence:1, Negative influence:-1>

neuron_random_parameter = ["random_chance", #integer
                           "random_activation_value"] #numeric

connection_habituation_parameter = ["habituation_threshold", #numeric
                                    "short_habituation_curvature", #numeric
                                    "short_habituation_steepness", #numeric
                                    "short_dehabituation_curvature", #numeric
                                    "short_dehabituation_steepness", #numeric
                                    "long_habituation_curvature", #numeric
                                    "long_habituation_steepness", #numeric
                                    "long_dehabituation_curvature", #numeric
                                    "long_dehabituation_steepness"] #numeric

connection_sensitization_parameter = ["sensitization_threshold", #numeric
                                      "short_sensitization_curvature", #numeric
                                      "short_sensitization_steepness", #numeric
                                      "short_desensitization_curvature", #numeric
                                      "short_desensitization_steepness", #numeric
                                      "long_sensitization_curvature", #numeric
                                      "long_sensitization_steepness", #numeric
                                      "long_desensitization_curvature", #numeric
                                      "long_desensitization_steepness"] #numeric

connection_presynaptic_parameter = ["presynaptic_potential_curvature", #numeric
                                    "presynaptic_potential_steepness", #numeric
                                    "presynaptic_backfall_curvature", #numeric
                                    "presynaptic_backfall_steepness"] #numeric

connection_special_parameter = ["base_weight", #numeric
                                "max_weight", #numeric
                                "min_weight", #numeric
                                "activation_type", #String<Excitatory:1, Inhibitory:-1, Nondirectional:0>
                                "activation_function", #String<1:Sigmoid, 2:Linear, 3:relu>
                                "learning_type", #String<None:1, Habituation:2, Sensitization:3, Habisens:4>
                                "transmitter_type", #String<Possible transmitters:?>
                                "long_learning_weight_reduction_curvature",
                                "long_learning_weight_reduction_steepness",
                                "long_learning_weight_backfall_curvature",
                                "long_learning_weight_backfall_steepness"]

network_parameter = ["transmitter_backfall_curvature",
                     "transmitter_backfall_steepness",
                     "max_transmitter_weight",
                     "min_transmitter_weight",
                     "input_nodes",
                     "output_nodes"]

interface_parameter = ["ip_address",
                       "port",
                       "channel"]

subnet_parameter = ["node_id"]

influences_transmitter_options = ["No", "Yes"]
transmitter_influence_direction_options = ["Positive Influence", "Negative Influence"]
activation_type_options = ["Excitatory", "Inhibitory", "Nondirectional"]
activation_function_options = ["Relu", "Linear", "Sigmoid"]
learning_type_options = ["None", "Habituation", "Sensitization", "HabiSens"]


class ParameterHandler:
    param_drop_options_all = ["Connection Specific",
                              "Connection Habituation",
                              "Connection Sensitization",
                              "Connection Presynaptic",
                              "Neuron Activation",
                              "Neuron Transmitter",
                              "Neuron Random",
                              "Network",
                              "Interface Node Settings",
                              "Subnet Node Settings"]
    param_drop_options_connection = ["Connection Specific",
                                     "Connection Habituation",
                                     "Connection Sensitization",
                                     "Connection Presynaptic"]
    param_drop_options_neuron = ["Neuron Activation",
                                 "Neuron Transmitter",
                                 "Neuron Random",
                                 "Connection Specific",
                                 "Connection Habituation",
                                 "Connection Sensitization",
                                 "Connection Presynaptic"]
    param_drop_options_network = ["Network"]

    param_drop_options_interface = ["Interface Node Settings"]
    param_drop_options_subnet = ["Subnet Node Settings"]

    def __init__(self):
        """
        Constructor.
        :return:    None
        """
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
        for idx, name in enumerate(interface_parameter):
            self.list[name] = None
        for idx, name in enumerate(subnet_parameter):
            self.list[name] = None

    def fill_in_params(self):
        """
        Fills in the parameters with a set of default parameters.
        :return:    None
        """
        self.list["neuron_type"] = "Default"
        self.list["activation_threshold"] = 1.0
        self.list["used_transmitter"] = "Default"
        self.list["max_activation"] = 50.0
        self.list["min_activation"] = 0.0
        self.list["activation_backfall_curvature"] = 1.0
        self.list["activation_backfall_steepness"] = 0.04

        self.list["transmitter_change_curvature"] = 1.02
        self.list["transmitter_change_steepness"] = 0.02
        self.list["influenced_transmitter"] = "Default"
        self.list["influences_transmitter"] = "No"
        self.list["transmitter_influence_direction"] = "Positive Influence"

        self.list["random_chance"] = 0
        self.list["random_activation_value"] = 0.0

        self.list["habituation_threshold"] = 0.001
        self.list["short_habituation_curvature"] = 0.65
        self.list["short_habituation_steepness"] = 0.07
        self.list["short_dehabituation_curvature"] = 1.0
        self.list["short_dehabituation_steepness"] = 0.00000005
        self.list["long_habituation_curvature"] = 0.35
        self.list["long_habituation_steepness"] = 0.00005
        self.list["long_dehabituation_curvature"] = 1.0
        self.list["long_dehabituation_steepness"] = 0.000000000001

        self.list["sensitization_threshold"] = 5.0
        self.list["short_sensitization_curvature"] = 0.65
        self.list["short_sensitization_steepness"] = 0.07
        self.list["short_desensitization_curvature"] = 1.0
        self.list["short_desensitization_steepness"] = 0.00000005
        self.list["long_sensitization_curvature"] = 1.02
        self.list["long_sensitization_steepness"] = 0.0001
        self.list["long_desensitization_curvature"] = 1.0
        self.list["long_desensitization_steepness"] = 0.000000000001

        self.list["presynaptic_potential_curvature"] = 0.60
        self.list["presynaptic_potential_steepness"] = 0.3
        self.list["presynaptic_backfall_curvature"] = 1.00
        self.list["presynaptic_backfall_steepness"] = 0.0000002

        self.list["long_learning_weight_reduction_curvature"] = 0.5
        self.list["long_learning_weight_reduction_steepness"] = 0.5
        self.list["long_learning_weight_backfall_curvature"] = 1.0
        self.list["long_learning_weight_backfall_steepness"] = 0.00000006

        self.list["base_weight"] = 1.0
        self.list["max_weight"] = 5.0
        self.list["min_weight"] = 0.0
        self.list["activation_type"] = "Excitatory"
        self.list["activation_function"] = "Relu"
        self.list["learning_type"] = "None"

        self.list["transmitter_type"] = "Default"

    def is_equal(self, other):
        """
        Checks if two parameter objects are equal.
        :param other:   The parameter handler object to campare this one.
        :return:        A boolean. True if both are equal.
        """
        return self.__dict__ == other.__dict__

    def load_by_dict(self, loading_dict):
        """
        Loads a parameter list based on a loaded dictionary.
        :param loading_dict:    The dictionary to load into the parameter list.
        :return:                None
        """
        keylist = loading_dict.keys()
        for idx, key in enumerate(keylist):
            if key in self.list:
                try:
                    if ParameterHandler.is_menu(key) or key == "ip_address" or key == "port" or key == "channel":
                        raise ValueError
                    self.list[key] = float(loading_dict[key])
                except ValueError:
                    self.list[key] = loading_dict[key]

    @staticmethod
    def is_menu(name):
        """
        Determines if a parameter is accessed with a drop down menu or an entry box.
        :param name:    Parameter name to check.
        :return:        A boolean which determines whether the parameter is a dropdown parameter.
        """
        if name == "transmitter_type" or name == "used_transmitter" or name == "learning_type" or \
                name == "activation_function" or name == "activation_type" or name == "transmitter_influence_direction" or \
                name == "influences_transmitter" or name == "influenced_transmitter" or name == "neuron_type" or \
                name == "node_id":
            return True
        return False

    @staticmethod
    def get_option_menu_list(name, network_manager, neuron_function=None, entity=None):
        """
        Returns the list of options for a dropdown parameter.
        :param name:            The name of the parameter in question.
        :param network_manager: The network manager object of the program.
        :param neuron_function: The function of the neuron, if it is relevant. Can sometimes change what a dropdown menu
                                contains.
        :param entity:          The type of entity of the entity the parameter is stored in. Can sometimes change what
                                a dropdown menu ontains.
        :return:                A list of strings representing the list of options for the dropdown menu.
        """
        menu = None
        if name == "influences_transmitter":
            menu = copy.copy(influences_transmitter_options)
        elif name == "influenced_transmitter":
            menu = copy.copy(network_manager.transmitters)
        elif name == "transmitter_influence_direction":
            menu = copy.copy(transmitter_influence_direction_options)
        elif name == "activation_type":
            menu = copy.copy(activation_type_options)
            try:
                if entity is not None:
                    if entity.next_neuron is not None:
                        menu.remove("Nondirectional")
            except AttributeError:
                pass
        elif name == "activation_function":
            menu = copy.copy(activation_function_options)
        elif name == "learning_type":
            menu = copy.copy(learning_type_options)
        elif name == "transmitter_type":
            menu = copy.copy(network_manager.transmitters)
        elif name == "used_transmitter":
            menu = copy.copy(network_manager.transmitters)
        elif name == "neuron_type":
            neuron_type_list = []
            for neuron in network_manager.neuron_types:
                neuron_type_list.append(neuron[0])
            menu = copy.copy(neuron_type_list)
        elif name == "node_id":
            menu = []
            if "input" in neuron_function:
                try:
                    node_number = int(network_manager.networks[network_manager.curr_network].param.list["input_nodes"])+1
                except TypeError:
                    node_number = 0
            elif "output" in neuron_function:
                try:
                    node_number = int(network_manager.networks[network_manager.curr_network].param.list["output_nodes"])+1
                except TypeError:
                    node_number = 0
            for i in range(1, node_number):
                menu.append(str(i))
            if not menu:
                menu = None

        return menu

    @staticmethod
    def get_paramter_list(parameter_selector, type, neuron_function="neuron"):
        """
        Based on the type of entity returns what parameter list can be accessed by the user.
        :param parameter_selector:  The currently chosen option of the dropdown menu.
        :param type:                The type of entity as a string.
        :param neuron_function:     The function of a neuron, if the entity is a neuron.
        :return:                    The parameter list.
        """
        param_list = None

        if type == "Connection":
            param_drop_options = ParameterHandler.param_drop_options_connection
            if parameter_selector.get() == param_drop_options[0]:
                param_list = copy.copy(connection_special_parameter)
            elif parameter_selector.get() == param_drop_options[1]:
                param_list = copy.copy(connection_habituation_parameter)
            elif parameter_selector.get() == param_drop_options[2]:
                param_list = copy.copy(connection_sensitization_parameter)
            elif parameter_selector.get() == param_drop_options[3]:
                param_list = copy.copy(connection_presynaptic_parameter)
            else:
                parameter_selector.set(param_drop_options[0])
                param_list = copy.copy(connection_special_parameter)

        elif type == "Neuron" or type == "NeuronType":
            if neuron_function == "neuron":
                param_drop_options = ParameterHandler.param_drop_options_neuron
                if parameter_selector.get() == param_drop_options[0]:
                    param_list = copy.copy(neuron_activation_parameter)
                elif parameter_selector.get() == param_drop_options[1]:
                    param_list = copy.copy(neuron_transmitter_parameter)
                elif parameter_selector.get() == param_drop_options[2]:
                    param_list = copy.copy(neuron_random_parameter)
                elif parameter_selector.get() == param_drop_options[3]:
                    param_list = copy.copy(connection_special_parameter)
                elif parameter_selector.get() == param_drop_options[4]:
                    param_list = copy.copy(connection_habituation_parameter)
                elif parameter_selector.get() == param_drop_options[5]:
                    param_list = copy.copy(connection_sensitization_parameter)
                elif parameter_selector.get() == param_drop_options[6]:
                    param_list = copy.copy(connection_presynaptic_parameter)
                else:
                    parameter_selector.set(param_drop_options[0])
                    param_list = copy.copy(neuron_activation_parameter)
                if type == "NeuronType":
                    try:
                        param_list.remove("neuron_type")
                    except ValueError:
                        pass
            elif "interface" in neuron_function:
                param_drop_options = ParameterHandler.param_drop_options_interface
                parameter_selector.set(param_drop_options[0])
                param_list = copy.copy(interface_parameter)
            elif "subnet" in neuron_function:
                param_drop_options = ParameterHandler.param_drop_options_subnet
                parameter_selector.set(param_drop_options[0])
                param_list = copy.copy(subnet_parameter)

        elif type == "Network":
            param_drop_options = ParameterHandler.param_drop_options_network
            if parameter_selector.get() == param_drop_options[0]:
                param_list = copy.copy(network_parameter)
            else:
                parameter_selector.set(param_drop_options[0])
                param_list = copy.copy(network_parameter)

        return param_list

    @staticmethod
    def get_base_neuron(neuron_type_list, entity_param):
        """
        Returns the parameter list of the neuron type of a neuron.
        :param neuron_type_list:    The list of all neuron types in the project.
        :param entity_param:        The parameter list which should be checked for a neuron type.
        :return:                    The parameter list of the neuron type.
        """
        neuron_type = neuron_type_list[0][1]
        for n_type in neuron_type_list:
            if n_type[0] == entity_param.list["neuron_type"]:
                neuron_type = n_type[1]
        return neuron_type

    @staticmethod
    def deny_scientific_notation(param):
        """
        Forces floating point notation for floats. Otherwise python always tries to print those in scientific notations.
        :param param:   The value of the parameter to change to floating point notation.
        :return:        The float as a string.
        """
        try:
            regex = re.compile("(-?[0-9]*(\.[0 -9]*[1-9])?)", re.IGNORECASE)
            param_str = regex.findall(format(param, ".15f"))
            string_value = param_str[0][0]
        except ValueError:
            return param

        return string_value
