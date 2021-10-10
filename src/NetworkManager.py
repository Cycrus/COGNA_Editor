"""
NetworkManager.py

This class handles most aspects of the networks and their entities.

Author: Cyril Marx
Date: 09.09.2021
"""

from src.GlobalLibraries import *
from src.Network import *
from src.Neuron import *
from src.Connection import *
from src.Subnetwork import *
from src.ParameterHandler import ParameterHandler
from src.Globals import *
import os

null_neuron_correcter = 1


class NetworkManager:
    def __init__(self):
        """
        Constructor.
        :return:    None
        """
        self.networks = []
        self.filename = []
        self.locations = []
        self.fixed_location = []
        self.camera_x = []
        self.camera_y = []
        self.zoom_factor = []

        self.transmitters = []
        self.neuron_types = []
        self.frequency = "10"
        self.main_network = "main.cogna"

        self.root_path = ""
        self.projects_folder = ""
        self.get_root_path()
        self.project_path = None
        self.project_name = None

        load_error = self.open_project(self.root_path + os.sep + self.projects_folder + os.sep + "DefaultProject",
                                       show_warnings=False)
        if load_error == Globals.ERROR:
            self.new_project("DefaultProject")

        self.curr_network = 0
        try:
            self.load_network(filename=self.project_path + os.sep + "networks" + os.sep + self.main_network)
        except:
            self.add_network(name="main.cogna")

    def get_root_path(self):
        """
        Finds the path of the program and its projects.
        Every value is returned implicitly in a member variable.
        :return:    None
        """
        with open(os.getcwd() + os.sep + "COGNA_PATH.config", "r") as file:
            path = file.read().rstrip("\n")
            if not path:
                self.root_path = os.getcwd()
                self.projects_folder = "Projects"
            elif os.path.exists(path):
                self.root_path = path.rsplit(os.sep, 1)[0]
                self.projects_folder = path.rsplit(os.sep, 1)[1]
            else:
                messagebox.showwarning("Project Error", "Path set in COGNA_PATH.config does not exist.")
                self.root_path = os.getcwd()
                self.projects_folder = "Projects"

    def default_neuron_types(self):
        """
        Generates the default parameters for neurons and stores them in the Default neuron type.
        :return:    None
        """
        default_neuron_params = ParameterHandler()
        default_neuron_params.fill_in_params()
        self.neuron_types = [["Default", default_neuron_params]]

    def default_transmitters(self):
        """
        Generates the Default neurotransmitter.
        :return:    None
        """
        self.transmitters = ["Default"]

    def default_global_info(self):
        """
        Generates the default global values for the project.
        :return:    None
        """
        self.frequency = "10"
        self.main_network = "main.cogna"

    def new_project(self, project_name):
        """
        Creates a new project and sets it as the current project.
        :param project_name:    The name of the new project.
        :return:                None
        """
        try:
            os.mkdir(self.root_path + os.sep + self.projects_folder)
        except:
            pass

        self.default_transmitters()
        self.default_neuron_types()
        self.default_global_info()

        new_path = self.root_path + os.sep + self.projects_folder + os.sep + project_name
        self.project_path = new_path
        self.project_name = project_name
        try:
            os.mkdir(new_path)
        except:
            pass
        try:
            os.mkdir(self.project_path + os.sep + "networks")
        except:
            pass
        self.save_meta_info()
        self.save_global_info()
        self.save_transmitters()
        self.save_neuron_types()

    def open_project(self, path, show_warnings=True):
        """
        Opens a saved project and sets it as the current project.
        :param path:            The path to the project description file.
        :param show_warnings:   A boolean. If set to true warnings are shown if they happen.
        :return:                None
        """
        if path[-1] == os.sep:
            path = path[:len(path)-1]
        self.project_name = path.split(os.sep)[-1]
        self.project_path = path

        try:
            self.load_global_info(path)
        except:
            self.default_global_info()
            if show_warnings:
                messagebox.showwarning("Invalid Global Info", "global.config is invalid. Loading default values.")
            return Globals.ERROR

        try:
            self.load_transmitters(path)
        except:
            self.default_transmitters()
            if show_warnings:
                messagebox.showwarning("Invalid Transmitters", "transmitters.config is invalid. Loading default values.")
            return Globals.ERROR

        try:
            self.load_neuron_types(path)
        except:
            self.default_neuron_types()
            if show_warnings:
                messagebox.showwarning("Invalid Neuron Types", "neuron_type.config is invalid. Loading default values.")
            return Globals.ERROR

        return Globals.SUCCESS

    def save_meta_info(self):
        """
        Saves the description file with the meta info about the current project.
        :return:    None
        """
        with open(self.project_path + os.sep + self.project_name + ".project", "w") as file:
            file.write("Valid COGNA Project\n")
            file.write(self.project_name)

    def save_global_info(self):
        """
        Saves the global information about the current project in a file.
        :return:    None
        """
        dict_obj = {}
        dict_obj["frequency"] = self.frequency
        dict_obj["main_network"] = self.main_network
        json_obj = json.dumps(dict_obj, indent=4)
        with open(self.project_path + os.sep + "global.config", "w") as file:
            file.write(json_obj)

    def save_transmitters(self):
        """
        Saves the neurotransmitter list of the current project in a file.
        :return:    None
        """
        dict_obj = {"transmitters": self.transmitters}
        json_obj = json.dumps(dict_obj, indent=4)
        with open(self.project_path + os.sep + "transmitters.config", "w") as file:
            file.write(json_obj)

    def load_transmitters(self, project_path, override_project_transmitters=True):
        """
        Loads the transmitter list of a project into the memory.
        :param project_path:                    The path of the target project.
        :param override_project_transmitters:   A boolean. If set true, there is no return value, but the project
                                                transmitter list is overridden implicitly.
        :return:                                transmitter list as a dictionary
        """
        with open(project_path + os.sep + "transmitters.config", "r") as file:
            transmitter_dict = json.loads(file.read())
            if override_project_transmitters:
                self.transmitters = transmitter_dict["transmitters"]
                return None
            else:
                return transmitter_dict["transmitters"]

    def load_global_info(self, path):
        """
        Loads the global parameters of a project into memory.
        :param path:    The path of the target project.
        :return:        None
        """
        with open(path + os.sep + "global.config", "r") as file:
            global_dict = json.loads(file.read())
            self.frequency = global_dict["frequency"]
            self.main_network = global_dict["main_network"]

    def save_neuron_types(self):
        """
        Saves the neuron types of the current project to a file.
        :return:    None
        """
        dict_obj = {}
        for neuron in self.neuron_types:
            dict_obj[neuron[0]] = {}
            for param in neuron[1].list:
                if neuron[1].list[param] is not None:
                    try:
                        dict_obj[neuron[0]][param] = "{:f}".format(neuron[1].list[param])
                    except:
                        dict_obj[neuron[0]][param] = neuron[1].list[param]
        json_obj = json.dumps(dict_obj, indent=4)
        with open(self.project_path + os.sep + "neuron_type.config", "w") as file:
            file.write(json_obj)

    def load_neuron_types(self, project_path, override_project_neurons=True):
        """
        Loads the neuron types of a project into the memory.
        :param project_path:    The path of the target project.
        :param override_project_neurons:    A boolean. If set to true, there is no return value, but the project
                                            neuron type list is overridden implicitly.
        :return:                            The list of neuron types.
        """
        with open(project_path + os.sep + "neuron_type.config", "r") as file:
            neuron_dict = json.loads(file.read())
            if override_project_neurons:
                self.neuron_types.clear()
            temp_neuron_list = []
            for idx, neuron in enumerate(neuron_dict.keys()):
                neuron_params = ParameterHandler()
                neuron_params.load_by_dict(neuron_dict[neuron])
                temp_neuron_list.append([neuron, neuron_params])

            if override_project_neurons:
                self.neuron_types = temp_neuron_list
                return None
            else:
                return temp_neuron_list

    def network_default_name(self, name_nr):
        """
        Generates the default names for new networks.
        :param name_nr: The current number of the network.
        :return:    The generated default name.
        """
        name = "network-" + str(name_nr) + ".cogna"
        for file in self.filename:
            if name == file:
                name_nr = name_nr+1
                name = self.network_default_name(name_nr)
                break
        return name


    def add_network(self, params=None, name=None):
        """
        Adds a new network to the project and puts the focus on it.
        :param params:  The parameter list given to the new network.
        :param name:    The name of the new network.
        :return:        None
        """
        self.networks.append(Network(params))
        self.curr_network = len(self.networks)-1
        if name is None:
            temp_filename = self.network_default_name(1)
        else:
            temp_filename = name
        self.filename.append(temp_filename)
        self.locations.append(self.project_path + os.sep + "networks" + os.sep)
        self.fixed_location.append(False)
        self.camera_x.append(0.0)
        self.camera_y.append(0.0)
        self.zoom_factor.append(1.0)


    def add_neuron(self, posx, posy, size, network_id=0, function="neuron"):
        """
        Adds a new neuron to a network.
        :param posx:        The x position of the neuron.
        :param posy:        The y position of the neuron.
        :param size:        The size of the neuron.
        :param network_id:  The ID of the network where the neuron should be placed in.
        :param function:    The function the neuron is supposed to have.
        :return:            None
        """
        if function == "neuron":
            temp_neuron = Neuron(len(self.networks[network_id].neurons) + null_neuron_correcter,
                                 posx, posy, size, network_id, function=function)
            self.networks[network_id].neurons.append(temp_neuron)
        else:
            temp_neuron = Neuron(len(self.networks[network_id].nodes) + null_neuron_correcter,
                                 posx, posy, size, network_id, function=function)
            self.networks[network_id].nodes.append(temp_neuron)


    def delete_subnet(self, id, network_id=0):
        """
        Deletes a subnetwork from a network.
        :param id:          The id of the subnetwork to delete.
        :param network_id:  The id of the network where the subnetwork is in.
        :return:            None
        """
        for connection in reversed(self.networks[self.curr_network].connections):
            if connection.prev_subnet == id or connection.next_subnet == id:
                self.delete_connection(connection.id, self.curr_network)

        self.networks[network_id].subnets.pop(id)
        for subnet in reversed(self.networks[network_id].subnets):
            if subnet.id > id:
                subnet.id = subnet.id - 1


    def delete_neuron(self, id, function, network_id=0):
        """
        Deletes a neuron from a network.
        :param id:          The id of the neuron to delete.
        :param function:    The function of the neuron to delete.
        :param network_id:  The id of the network the neuron is in.
        :return:            None
        """
        for connection in reversed(self.networks[network_id].connections):
            if connection.prev_neuron == id and connection.prev_neuron_function == function \
                    or connection.next_neuron == id and connection.next_neuron_function == function:
                self.delete_connection(connection.id, network_id)

        if function == "neuron":
            neuron_type = ["neuron"]
        elif "subnet" in function or "interface" in function:
            neuron_type = ["interface_input", "interface_output", "subnet_input", "subnet_output"]
        else:
            neuron_type = ["no change"]

        for connection in self.networks[network_id].connections:
            if connection.prev_neuron > id-1 and connection.prev_neuron_function in neuron_type:
                connection.prev_neuron = connection.prev_neuron - 1
            if connection.next_neuron is not None:
                if connection.next_neuron > id-1 and connection.next_neuron_function in neuron_type:
                    connection.next_neuron = connection.next_neuron - 1

        if "neuron" in function:
            self.networks[network_id].neurons.pop(id - 1)
            for neuron in reversed(self.networks[network_id].neurons):
                if neuron.id > id:
                    neuron.id = neuron.id - 1
        else:
            self.networks[network_id].nodes.pop(id - 1)
            for neuron in reversed(self.networks[network_id].nodes):
                if neuron.id > id:
                    neuron.id = neuron.id - 1

    def add_connection(self, source_neuron, network_id=0):
        """
        Adds a new connection to a network. Only defines where the connection stems from.
        :param source_neuron:   The neuron where the connection stems from.
        :param network_id:      The id of the network where the connection should be placed.
        :return:                None
        """
        self.networks[network_id].connections.append(Connection(len(self.networks[network_id].connections),
                                                                source_neuron, network_id))

    def delete_connection(self, id, network_id=0):
        """
        Deletes a connection from a network.
        :param id:          The id of the connection to delete.
        :param network_id:  The id of the network the connection is in.
        :return:            None
        """
        for connection in reversed(self.networks[network_id].connections):
            if connection.next_connection == id:
                self.delete_connection(connection.id, network_id)
        self.networks[network_id].connections.pop(id)
        for connection in reversed(self.networks[network_id].connections):
            if connection.id > id:
                connection.id = connection.id - 1

    def get_network_dict(self, network_name):
        """
        Loads the json dictionary of a network from the current project.
        :param network_name:    The name of the network.
        :return:                The json file of the network as a dictionary.
        """
        with open(self.project_path + os.sep + "networks" + os.sep + network_name, "r") as file:
            network_dict = json.loads(file.read())
        return network_dict

    def get_neuron_types(self):
        """
        Loads the neuron type file of the project.
        :return:    The neuron type file as a dictionary.
        """
        with open(self.project_path + os.sep + "neuron_type.config", "r") as file:
            neuron_dict = json.loads(file.read())
        return neuron_dict

    def save_neuron_types_by_dict(self, dict):
        """
        Saves the neuron types from a dictionary to a file.
        :param dict:    The dictionary to save.
        :return:        None
        """
        with open(self.project_path + os.sep + "neuron_type.config", "w") as file:
            neuron_json = json.dumps(dict, indent=4)
            file.write(neuron_json)

    def load_network_nodes(self, network_name):
        """
        Loads the input/output nodes of a certain network.
        :param network_name:    The name of the network from which the nodes should be loaded.
        :return:                A tuple with the input node list at index 0 and the output node list at index 1.
        """
        input_nodes = 0
        output_nodes = 0
        with open(self.project_path + os.sep + "networks" + os.sep + network_name, "r") as file:
            network_dict = json.loads(file.read())

            network_parameter = self.read_parameter_list(network_dict["network"])
            try:
                input_nodes = int(network_parameter.list["input_nodes"])
                output_nodes = int(network_parameter.list["output_nodes"])
            except TypeError:
                input_nodes = 0
                output_nodes = 0

        return input_nodes, output_nodes

    def add_subnet(self, network_name, posx, posy, network_id=0):
        """
        Adds a subnetwork to a certain opened network.
        :param network_name:    The name of the network the new subnet refers to.
        :param posx:            The x position of the subnetwork.
        :param posy:            The y position of the subnetwork.
        :param network_id:      The ID of the opened network the new subnet is added to.
        :return:                None
        """
        input_nodes, output_nodes = self.load_network_nodes(network_name)
        temp_subnet = Subnetwork(len(self.networks[network_id].subnets), network_name, posx, posy, network_id,
                                 input_nodes, output_nodes)
        self.networks[network_id].subnets.append(temp_subnet)

    def clear_all_networks(self):
        """
        Clears all opened networks and deletes them from the opened networks.
        Adds one new empty network at the end of the procedure.
        :return:    None
        """
        for network_id, network in enumerate(self.networks):
            network.connections.clear()
            network.neurons.clear()
            self.filename.clear()
            self.locations.clear()
            self.fixed_location.clear()
            self.camera_x.clear()
            self.camera_y.clear()
            self.zoom_factor.clear()
        self.networks.clear()
        self.add_network()

    def clear_single_network(self, network_id):
        """
        Clears every entity of a single network and removes it from the opened networks.
        If 0 networks are left one empty network is added.
        :param network_id:  The network which should be deleted.
        :return:            None
        """
        for idx, network in enumerate(self.networks):
            if idx > network_id:
                for neuron in chain(*network.all_nodes):
                    neuron.network_id = neuron.network_id - 1
                for subnet in network.subnets:
                    subnet.network_id = subnet.network_id - 1
                    for node in chain(subnet.input_node_list, subnet.output_node_list):
                        node.network_id = node.network_id - 1
                for connection in network.connections:
                    connection.network_id = connection.network_id - 1

        self.networks[network_id].connections.clear()
        self.networks[network_id].neurons.clear()
        self.networks.pop(network_id)
        self.filename.pop(network_id)
        self.locations.pop(network_id)
        self.fixed_location.pop(network_id)
        self.camera_x.pop(network_id)
        self.camera_y.pop(network_id)
        self.zoom_factor.pop(network_id)
        self.curr_network = self.curr_network - 1
        if self.curr_network < 0:
            self.curr_network = 0
        if len(self.networks) < 1:
            self.add_network()
            return Globals.WARNING
        return Globals.SUCCESS

    def convert_parameter_to_dict(self, target_dict, parameter):
        """
        Converts the parameters of an entity to a dictionary. Return value is implicit to a function parameter.
        :param target_dict: The dictionary all parameters should be added to.
        :param parameter:   The parameter list of the entity which should be converted.
        :return:            None
        """
        for idx, param in enumerate(parameter):
            if parameter[param] is not None:
                target_dict[param] = ParameterHandler.deny_scientific_notation(parameter[param])

    def store_single_parameter(self, target_dict, param, value):
        """
        Append a single parameter of a parameter list of an entity to a dictionary.
        Return value is implicit to a function parameter.
        :param target_dict: The dictionary the parameter should be added to.
        :param param:       The name of the parameter which should be added to the dictionary.
        :param value:       The value of the parameter which should be added to the dictionary.
        """
        if value is not None:
            target_dict[param] = value

    def store_network_param_in_dict(self, network_id):
        """
        Stores all network-parameters of an opened network to a dictionary.
        :param network_id:  The ID of the opened network to be stored in a dictionary.
        :return:            None
        """
        temp_dict = {}
        self.convert_parameter_to_dict(temp_dict, self.networks[network_id].param.list)
        return temp_dict

    def store_neurons_in_dict(self, target_dict, network_id):
        """
        Stores parameters of all neurons of a single opened network in a dictionary.
        Return value is implicit to a function parameter.
        :param target_dict: The dictionary where the parameters should be stored in.
        :param network_id:  The ID of the opened network which should be stored.
        :return:            None
        """
        for neuron in self.networks[network_id].neurons:
            temp_dict = {}
            self.store_single_parameter(temp_dict, "id", neuron.id)
            self.store_single_parameter(temp_dict, "posx", neuron.posx)
            self.store_single_parameter(temp_dict, "posy", neuron.posy)
            self.convert_parameter_to_dict(temp_dict, neuron.param.list)
            target_dict["neurons"].append(temp_dict)

    def store_nodes_in_dict(self, target_dict, network_id):
        """
        Stores parameters of all input/output nodes of a single opened network in a dictionary.
        Return value is implicit to a function parameter.
        :param target_dict: The dictionary where the parameters should be stored in.
        :param network_id:  The ID of the opened network which should be stored.
        :return:            None
        """
        for node in self.networks[network_id].nodes:
            temp_dict = {}
            self.store_single_parameter(temp_dict, "id", node.id)
            self.store_single_parameter(temp_dict, "posx", node.posx)
            self.store_single_parameter(temp_dict, "posy", node.posy)
            self.store_single_parameter(temp_dict, "function", node.function)
            self.convert_parameter_to_dict(temp_dict, node.param.list)
            target_dict["nodes"].append(temp_dict)

    def store_subnets_in_dict(self, target_dict, network_id):
        """
        Stores parameters of all subnets of a single opened network in a dictionary.
        Return value is implicit to a function parameter.
        :param target_dict: The dictionary where the parameters should be stored in.
        :param network_id:  The ID of the opened network which should be stored.
        :return:            None
        """
        for subnet in self.networks[network_id].subnets:
            temp_dict = {}
            self.store_single_parameter(temp_dict, "id", subnet.id)
            self.store_single_parameter(temp_dict, "network_name", subnet.network_name)
            self.store_single_parameter(temp_dict, "posx", subnet.posx)
            self.store_single_parameter(temp_dict, "posy", subnet.posy)
            target_dict["subnetworks"].append(temp_dict)

    def get_subnet_node_ids(self, connection):
        """
        Finds and returns the IDs of the subnetwork related input/output nodes connected to a single connection.
        :param connection:  The connection object which should be searched in.
        :return:            A tuple with the prev node ID at index 0 and next node ID at index 1.
                            If a prev or next node is not subnetwork input/output related, it stores a None value.
        """
        temp_prev_node_id = None
        temp_next_node_id = None
        if connection.prev_neuron_function == "input":
            temp_prev_node_id = int(connection.prev_neuron)

        elif connection.prev_neuron_function == "subnet_input":
            for node in self.networks[self.curr_network].nodes:
                if node.function == "subnet_input" and node.id == connection.prev_neuron:
                    try:
                        temp_prev_node_id = int(node.param.list["node_id"])
                    except TypeError:
                        temp_prev_node_id = -1

        if connection.next_neuron_function == "output":
            temp_next_node_id = int(connection.next_neuron)

        elif connection.next_neuron_function == "subnet_output":
            for node in self.networks[self.curr_network].nodes:
                if node.function == "subnet_output" and node.id == connection.next_neuron:
                    try:
                        temp_next_node_id = int(node.param.list["node_id"])
                    except TypeError:
                        temp_prev_node_id = -1

        return temp_prev_node_id, temp_next_node_id

    def store_connections_in_dict(self, target_dict, network_id):
        """
        Stores parameters of all connections of a single opened network in a dictionary.
        Return value is implicit to a function parameter.
        :param target_dict: The dictionary where the parameters should be stored in.
        :param network_id:  The ID of the opened network which should be stored.
        :return:            None
        """
        for connection in self.networks[network_id].connections:
            temp_dict = {}
            self.store_single_parameter(temp_dict, "id", connection.id)
            self.store_single_parameter(temp_dict, "prev_neuron", connection.prev_neuron)
            self.store_single_parameter(temp_dict, "prev_neuron_function", connection.prev_neuron_function)
            self.store_single_parameter(temp_dict, "next_neuron_function", connection.next_neuron_function)
            self.store_single_parameter(temp_dict, "prev_subnetwork", connection.prev_subnet)
            self.store_single_parameter(temp_dict, "next_subnetwork", connection.next_subnet)
            self.store_single_parameter(temp_dict, "next_neuron", connection.next_neuron)
            self.store_single_parameter(temp_dict, "next_connection", connection.next_connection)

            temp_prev_node_id, temp_next_node_id = self.get_subnet_node_ids(connection)

            self.store_single_parameter(temp_dict, "prev_subnet_node_id", temp_prev_node_id)
            self.store_single_parameter(temp_dict, "next_subnet_node_id", temp_next_node_id)

            temp_dict["vertices"] = []
            for vert in connection.vertices:
                temp_dict["vertices"].append([vert[0], vert[1]])
            self.convert_parameter_to_dict(temp_dict, connection.param.list)
            target_dict["connections"].append(temp_dict)

    def store_network_in_json(self, network_id):
        """
        Stores a whole opened network and all its entities in a json format.
        :param network_id:  The ID of the saved network which should be saved.
        :return:            The json formatted network.
        """
        network_dict = {}
        network_dict["network"] = self.store_network_param_in_dict(network_id)

        network_dict["neurons"] = []
        self.store_neurons_in_dict(network_dict, network_id)

        network_dict["nodes"] = []
        self.store_nodes_in_dict(network_dict, network_id)

        network_dict["subnetworks"] = []
        self.store_subnets_in_dict(network_dict, network_id)

        network_dict["connections"] = []
        self.store_connections_in_dict(network_dict, network_id)

        network_json = json.dumps(network_dict, indent=4)
        return network_json

    def read_parameter_list(self, param_dict):
        """
        Reads a parameter dictionary into a parameter object which can be addressed to an entity.
        :param param_dict:  The dictionary where the parameters are stored.
        :return:            The finished parameter object.
        """
        parameter = ParameterHandler()
        parameter.load_by_dict(param_dict)
        return parameter

    def read_neurons_from_dict(self, neurons_dict):
        """
        Reads all neurons of a network from a neuron list dictionary into neuron entity objects.
        :param neurons_dict:    The dictionary where the neurons are saved.
        :return:                None
        """
        for neuron in neurons_dict:
            try:
                neuron_list = self.networks[self.curr_network].neurons
                self.add_neuron(neuron["posx"], neuron["posy"], 25, self.curr_network)
                neuron_list[len(neuron_list)-1].param = self.read_parameter_list(neuron)
            except:
                pass

    def read_nodes_from_dict(self, nodes_dict):
        """
        Reads all input/output nodes of a node list dictionary into neuron entity objects.
        :param nodes_dict:      The dictionary where the nodes are saved.
        :return:                None
        """
        for node in nodes_dict:
            try:
                node_list = self.networks[self.curr_network].nodes
                self.add_neuron(node["posx"], node["posy"], 25, self.curr_network,
                                node["function"])
                node_list[len(node_list)-1].param = self.read_parameter_list(node)
            except:
                pass

    def read_subnets_from_dict(self, subnet_dict):
        """
        Reads all subnetworks of a subnetwork list dictionary into subnetwork entity objects.
        :param subnet_dict:     The dictionary where the subnetworks are saved.
        :return:                A list of error codes.
        """
        error_ids = []
        for subnet in subnet_dict:
            try:
                self.add_subnet(subnet["network_name"], subnet["posx"], subnet["posy"], self.curr_network)
            except:
                error_ids.append(subnet["id"])
        return error_ids

    def read_connections_from_dict(self, connections_dict, error_subnets):
        """
        Reads all connections of a connection list dictionary into connection entity objects.
        :param connection_dict:     The dictionary where the connections are saved.
        :param error_subnets:       List of subnetworks in the network where the connections are in.
                                    Checks if the connection is associated with a stored subnetwork of the network.
        :return:                    None
        """
        for connection in connections_dict:
            try:
                if connection["next_subnetwork"] in error_subnets or \
                        connection["prev_subnetwork"] in error_subnets:
                    raise ValueError
                connection_list = self.networks[self.curr_network].connections
                if "neuron" in connection["prev_neuron_function"]:
                    source_neuron = self.networks[self.curr_network].neurons[connection["prev_neuron"]-1]
                else:
                    source_neuron = self.networks[self.curr_network].nodes[connection["prev_neuron"] - 1]
                self.add_connection(source_neuron, self.curr_network)
                temp_connection = connection_list[len(connection_list)-1]
                temp_connection.vertices = connection["vertices"]
                temp_connection.prev_neuron_function = connection["prev_neuron_function"]
                temp_connection.next_subnet = connection["next_subnetwork"]
                temp_connection.prev_subnet = connection["prev_subnetwork"]

                if "next_neuron" in connection:
                    temp_connection.next_neuron_function = connection["next_neuron_function"]
                    connection_list[len(connection_list) - 1].next_neuron = connection["next_neuron"]
                elif "next_connection" in connection:
                    connection_list[len(connection_list)-1].next_connection = connection["next_connection"]

                connection_list[len(connection_list)-1].param = self.read_parameter_list(connection)
            except:
                pass

    def load_network(self, filename=None):
        """
        Loads a whole network into the project and adds it to the opened networks.
        :param filename:    The name of the network.
        :return:            Error Code.
        """
        if filename is None:
            file = filedialog.askopenfile(initialdir=self.project_path + os.sep + "networks", title="Save Network",
                                          filetypes=(("cogna network", "*.cogna"),))
        else:
            file = open(filename, "r")

        if not file:
            return Globals.ERROR

        check_path = (self.project_path + os.sep + "networks").replace("\\", "/")
        corrected_filename = file.name.replace("\\", "/")

        if not check_path in corrected_filename:
            messagebox.showerror("Load Error", "Can only load networks out of correct project path.")
            file.close()
            return Globals.ERROR

        network_name = file.name.split(os.sep)[-1]
        for idx, name in enumerate(self.filename):
            if network_name == name:
                self.curr_network = idx
                file.close()
                return Globals.ERROR

        network_dict = json.loads(file.read())

        network_parameter = self.read_parameter_list(network_dict["network"])
        self.add_network(network_parameter)
        self.read_neurons_from_dict(network_dict["neurons"])
        self.read_nodes_from_dict(network_dict["nodes"])
        error_subnets = self.read_subnets_from_dict(network_dict["subnetworks"])
        self.read_connections_from_dict(network_dict["connections"], error_subnets)
        self.filename[self.curr_network] = network_name
        self.fixed_location[self.curr_network] = True

        file.close()

        return Globals.SUCCESS

    def check_if_networkfile_exists(self, file):
        """
        Checks if the asked network-name already exists in the project. If it does, it will be renamed by adding a
        number at the end.
        :param file:    The filename which should be checked.
        :return:        The old or new name as a String.
        """
        network_name = file.name.split(os.sep)[-1]
        temp_network_name = network_name.rsplit('.', 1)[0]
        name_iterator = 2
        while True:
            is_duplicate = False
            for idx, name in enumerate(self.get_network_list()):
                if temp_network_name == name.rsplit('.', 1)[0]:
                    temp_network_name = network_name.rsplit('.', 1)[0] + "_" + str(name_iterator)
                    is_duplicate = True
                    break
            name_iterator = name_iterator + 1
            if not is_duplicate:
                break

        return temp_network_name + ".cogna"

    def import_network(self):
        """
        Imports a whole network from another project into the currently open project. Adds the network, its neuron types,
        and its neurotransmitters as well.
        :return:    Error Code
        """
        file = filedialog.askopenfile(initialdir=self.project_path + os.sep + "..", title="Save Network",
                                      filetypes=(("cogna network", "*.cogna"),))

        if not file:
            return Globals.ERROR

        check_path = (self.project_path + os.sep + "networks").replace("\\", "/")
        corrected_filename = file.name.replace("\\", "/")

        if check_path in corrected_filename:
            messagebox.showerror("Load Error", "Cannot import networks from same project.")
            file.close()
            return Globals.ERROR

        network_name = self.check_if_networkfile_exists(file)
        network_dict = json.loads(file.read())

        if network_dict["subnetworks"]:
            messagebox.showerror("Load Error", "Cannot import networks referencing other networks.")
            file.close()
            return Globals.ERROR

        file_project_name = file.name.rsplit(os.sep, 2)[0]

        neuron_types = self.load_neuron_types(project_path=file_project_name, override_project_neurons=False)
        transmitter_types = self.load_transmitters(project_path=file_project_name, override_project_transmitters=False)

        for transmitter in transmitter_types:
            if transmitter not in self.transmitters:
                self.transmitters.append(transmitter)

        old_neuron_names = []
        new_neuron_names = []
        for new_neuron in neuron_types:
            is_contained = False
            for old_neuron in self.neuron_types:
                if new_neuron[0] == old_neuron[0]:
                    if new_neuron[1].is_equal(old_neuron[1]):
                        is_contained = True
                    else:
                        old_neuron_names.append(new_neuron[0])
                        new_neuron[0] = new_neuron[0] + "_" + network_name.rsplit('.', 1)[0]
                        new_neuron_names.append(new_neuron[0])
            if not is_contained:
                self.neuron_types.append(new_neuron)

        self.save_transmitters()
        self.save_neuron_types()

        messagebox.showinfo("Import Info", "Imported other network's neuron types and neurotransmitters.")

        network_parameter = self.read_parameter_list(network_dict["network"])
        self.add_network(network_parameter)
        self.read_neurons_from_dict(network_dict["neurons"])
        for neuron in self.networks[self.curr_network].neurons:
            if neuron.param.list["neuron_type"] in old_neuron_names:
                neuron.param.list["neuron_type"] = new_neuron_names[old_neuron_names.index(neuron.param.list["neuron_type"])]
            elif not neuron.param.list["neuron_type"] and "Default" in old_neuron_names:
                neuron.param.list["neuron_type"] = new_neuron_names[
                    old_neuron_names.index("Default")]

        self.read_nodes_from_dict(network_dict["nodes"])
        self.read_connections_from_dict(network_dict["connections"], [])
        self.filename[self.curr_network] = network_name
        self.fixed_location[self.curr_network] = False

        file.close()

        return Globals.SUCCESS

    def save_network_by_dict(self, network_name, network_dict):
        """
        Saves a complete and prepared network dictionary to a file.
        :param network_name:    The name under which the network should be saved.
        :param network_dict:    The dictionary which should be saved under the filename.
        :return:                None
        """
        network_json = json.dumps(network_dict, indent=4)
        with open(self.project_path + os.sep + "networks" + os.sep + network_name, "w") as file:
            file.write(network_json)

    def save_network(self, save_as):
        """
        Saves the currently active network to a file.
        :param save_as: The filename under which the network should be saved.
        :return:        None
        """
        file = None

        if not save_as:
            if not self.fixed_location[self.curr_network]:
                save_as = True
            else:
                file = open(self.locations[self.curr_network] + self.filename[self.curr_network], "w")

        if save_as:
            file = filedialog.asksaveasfile(initialdir=self.project_path + os.sep + "networks", title="Save Network",
                                            initialfile=self.filename[self.curr_network],
                                            filetypes=(("cogna network", "*.cogna"),))

        if not file:
            return

        check_path = (self.project_path + os.sep + "networks").replace("\\", "/")
        corrected_filename = file.name.replace("\\", "/")

        if not check_path in corrected_filename:
            os.remove(file.name)
            messagebox.showerror("Save Error", "Can only save networks in correct project path.")
            return

        network_json = self.store_network_in_json(self.curr_network)
        name_split = file.name.split("/")
        new_name = name_split[len(name_split)-1]
        self.filename[self.curr_network] = new_name
        self.fixed_location[self.curr_network] = True
        file.write(network_json)
        file.close()

    def get_network_list(self):
        """
        Returns the whole list of all networks in the currently opened project.
        :return:    The list of network names.
        """
        path = self.project_path + os.sep + "networks"
        return os.listdir(path)

    def save_storing(self, parameter_names, prev_values, new_values):
        """
        Checks conditions of saving a certain parameter list and changes all networks based on the changes.
        E.g. used in NeuronConfigurator.py and TransmitterConfigurator.py.
        :param parameter_names: The names of all parameters.
        :param prev_values:     The values of the parameters in parameter_names before changing.
        :param new_values:      The values of the parameters in parameter_names after changing.
        :return:                Error Code
        """
        if len(new_values) == 1:
            temp_value = new_values[0]
            new_values = []
            for idx, param in enumerate(prev_values):
                new_values.append(temp_value)
        elif len(new_values) != len(prev_values):
            return Globals.ERROR

        for idx, prev_value in enumerate(prev_values):
            if new_values[idx] is not None:
                for network in self.networks:
                    for neuron in network.neurons:
                        for param in parameter_names:
                            if param in neuron.param.list:
                                if neuron.param.list[param] == prev_value:
                                    neuron.param.list[param] = new_values[idx]

                for neuron in self.neuron_types:
                    for param in parameter_names:
                        if param in neuron[1].list:
                            if neuron[1].list[param] == prev_value:
                                neuron[1].list[param] = new_values[idx]

                network_list = self.get_network_list()
                for filename in network_list:
                    is_changed = False
                    network_dict = self.get_network_dict(filename)
                    for neuron in network_dict["neurons"]:
                        for param in parameter_names:
                            if param in neuron:
                                if neuron[param] == prev_value:
                                    neuron[param] = new_values[idx]
                                    is_changed = True
                    if is_changed:
                        self.save_network_by_dict(filename, network_dict)

                neuron_dict = self.get_neuron_types()
                is_changed = False
                for neuron in neuron_dict:
                    for param in parameter_names:
                        if param in neuron:
                            if neuron[param] == prev_value:
                                neuron[param] = new_values[idx]
                                is_changed = True
                if is_changed:
                    self.save_neuron_types_by_dict(neuron_dict)

        return Globals.SUCCESS
