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
        self.networks = []
        self.filename = []
        self.locations = []
        self.fixed_location = []
        self.camera_x = []
        self.camera_y = []
        self.zoom_factor = []

        self.transmitters = []
        self.neuron_types = []
        self.frequency = 10
        self.main_network = "main.cogna"

        self.project_path = None
        self.project_name = None
        try:
            self.open_project(os.getcwd() + os.sep + "Projects" + os.sep + "DefaultProject")
        except:
            self.new_project("DefaultProject")

        self.curr_network = 0
        try:
            self.load_network(filename=self.project_path + os.sep + "networks" + os.sep + self.main_network)
        except Exception as e:
            print(e)
            self.add_network(name="main.cogna")

    def default_neuron_types(self):
        default_neuron_params = ParameterHandler()
        default_neuron_params.fill_in_params()
        self.neuron_types = [["Default", default_neuron_params]]

    def default_transmitters(self):
        self.transmitters = ["Default"]

    def default_global_info(self):
        self.frequency = 10
        self.main_network = "main.cogna"

    def new_project(self, project_name):
        try:
            os.mkdir(os.getcwd() + os.sep + "Projects")
        except:
            pass

        self.default_transmitters()
        self.default_neuron_types()
        self.default_global_info()

        new_path = os.getcwd() + os.sep + "Projects" + os.sep + project_name
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

    def open_project(self, path):
        if path[-1] == os.sep:
            path = path[:len(path)-1]
        self.project_name = path.split(os.sep)[-1]
        self.project_path = path
        try:
            self.load_global_info(path)
        except:
            self.default_global_info()
            messagebox.showwarning("Invalid Global Info", "global.config is invalid. Loading default values.")
        try:
            self.load_transmitters(path)
        except:
            self.default_transmitters()
            messagebox.showwarning("Invalid Transmitters", "transmitters.config is invalid. Loading default values.")
        try:
            self.load_neuron_types(path)
        except:
            self.default_neuron_types()
            messagebox.showwarning("Invalid Neuron Types", "neuron_type.config is invalid. Loading default values.")

    def save_meta_info(self):
        with open(self.project_path + os.sep + self.project_name + ".project", "w") as file:
            file.write("Valid COGNA Project\n")
            file.write(self.project_name)

    def save_global_info(self):
        dict_obj = {}
        dict_obj["frequency"] = self.frequency
        dict_obj["main_network"] = self.main_network
        json_obj = json.dumps(dict_obj, indent=4)
        with open(self.project_path + os.sep + "global.config", "w") as file:
            file.write(json_obj)

    def save_transmitters(self):
        dict_obj = {"transmitters": self.transmitters}
        json_obj = json.dumps(dict_obj, indent=4)
        with open(self.project_path + os.sep + "transmitters.config", "w") as file:
            file.write(json_obj)

    def load_transmitters(self, project_path):
        with open(project_path + os.sep + "transmitters.config", "r") as file:
            transmitter_dict = json.loads(file.read())
            self.transmitters = transmitter_dict["transmitters"]

    def load_global_info(self, path):
        with open(self.project_path + os.sep + "global.config", "r") as file:
            global_dict = json.loads(file.read())
            self.frequency = global_dict["frequency"]
            self.main_network = global_dict["main_network"]

    def save_neuron_types(self):
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

    def load_neuron_types(self, project_path):
        with open(project_path + os.sep + "neuron_type.config", "r") as file:
            neuron_dict = json.loads(file.read())
            self.neuron_types.clear()
            for idx, neuron in enumerate(neuron_dict.keys()):
                neuron_params = ParameterHandler()
                neuron_params.load_by_dict(neuron_dict[neuron])
                self.neuron_types.append([neuron, neuron_params])

    def network_default_name(self, name_nr):
        name = "network-" + str(name_nr) + ".cogna"
        for file in self.filename:
            if name == file:
                name_nr = name_nr+1
                name = self.network_default_name(name_nr)
                break
        return name

    def add_network(self, params=None, name=None):
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
        if function == "neuron":
            temp_neuron = Neuron(len(self.networks[network_id].neurons) + null_neuron_correcter,
                                 posx, posy, size, network_id, function=function)
            self.networks[network_id].neurons.append(temp_neuron)
        else:
            temp_neuron = Neuron(len(self.networks[network_id].nodes) + null_neuron_correcter,
                                 posx, posy, size, network_id, function=function)
            self.networks[network_id].nodes.append(temp_neuron)

    def delete_subnet(self, id, network_id=0):
        for connection in reversed(self.networks[self.curr_network].connections):
            if connection.prev_subnet == id or connection.next_subnet == id:
                self.delete_connection(connection.id, self.curr_network)

        self.networks[network_id].subnets.pop(id)
        for subnet in reversed(self.networks[network_id].subnets):
            if subnet.id > id:
                subnet.id = subnet.id - 1

    def delete_neuron(self, id, function, network_id=0):
        for connection in reversed(self.networks[network_id].connections):
            if connection.prev_neuron == id and connection.prev_neuron_function == function \
                or connection.next_neuron == id and connection.next_neuron_function == function:
                self.delete_connection(connection.id, network_id)

        for connection in self.networks[network_id].connections:
            if connection.prev_neuron > id-1:
                connection.prev_neuron = connection.prev_neuron - 1
            if connection.next_neuron is not None:
                if connection.next_neuron > id-1:
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
        self.networks[network_id].connections.append(Connection(len(self.networks[network_id].connections),
                                                                source_neuron, network_id))

    def delete_connection(self, id, network_id=0):
        for connection in reversed(self.networks[network_id].connections):
            if connection.next_connection == id:
                self.delete_connection(connection.id, network_id)
        self.networks[network_id].connections.pop(id)
        for connection in reversed(self.networks[network_id].connections):
            if connection.id > id:
                connection.id = connection.id - 1

    def get_network_dict(self, network_name):
        with open(self.project_path + os.sep + "networks" + os.sep + network_name, "r") as file:
            network_dict = json.loads(file.read())
        return network_dict

    def get_neuron_types(self):
        with open(self.project_path + os.sep + "neuron_type.config", "r") as file:
            neuron_dict = json.loads(file.read())
        return neuron_dict

    def save_neuron_types_by_dict(self, dict):
        with open(self.project_path + os.sep + "neuron_type.config", "w") as file:
            neuron_json = json.dumps(dict, indent=4)
            file.write(neuron_json)

    def load_network_nodes(self, network_name):
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
        input_nodes, output_nodes = self.load_network_nodes(network_name)
        temp_subnet = Subnetwork(len(self.networks[network_id].subnets), network_name, posx, posy, network_id,
                                 input_nodes, output_nodes)
        self.networks[network_id].subnets.append(temp_subnet)

    def clear_all_networks(self):
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

    def convert_parameter_to_dict(self, target_dict, parameter):
        for idx, param in enumerate(parameter):
            if parameter[param] is not None:
                target_dict[param] = ParameterHandler.deny_scientific_notation(parameter[param])

    def store_single_parameter(self, target_dict, param, value):
        if value is not None:
            target_dict[param] = value

    def store_network_param_in_dict(self, network_id):
        temp_dict = {}
        self.convert_parameter_to_dict(temp_dict, self.networks[network_id].param.list)
        return temp_dict

    def store_neurons_in_dict(self, target_dict, network_id):
        for neuron in self.networks[network_id].neurons:
            temp_dict = {}
            self.store_single_parameter(temp_dict, "id", neuron.id)
            self.store_single_parameter(temp_dict, "posx", neuron.posx)
            self.store_single_parameter(temp_dict, "posy", neuron.posy)
            self.convert_parameter_to_dict(temp_dict, neuron.param.list)
            target_dict["neurons"].append(temp_dict)

    def store_nodes_in_dict(self, target_dict, network_id):
        for node in self.networks[network_id].nodes:
            temp_dict = {}
            self.store_single_parameter(temp_dict, "id", node.id)
            self.store_single_parameter(temp_dict, "posx", node.posx)
            self.store_single_parameter(temp_dict, "posy", node.posy)
            self.store_single_parameter(temp_dict, "function", node.function)
            self.convert_parameter_to_dict(temp_dict, node.param.list)
            target_dict["nodes"].append(temp_dict)

    def store_subnets_in_dict(self, target_dict, network_id):
        for subnet in self.networks[network_id].subnets:
            temp_dict = {}
            self.store_single_parameter(temp_dict, "id", subnet.id)
            self.store_single_parameter(temp_dict, "network_name", subnet.network_name)
            self.store_single_parameter(temp_dict, "posx", subnet.posx)
            self.store_single_parameter(temp_dict, "posy", subnet.posy)
            target_dict["subnetworks"].append(temp_dict)

    def store_connections_in_dict(self, target_dict, network_id):
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
            temp_dict["vertices"] = []
            for vert in connection.vertices:
                temp_dict["vertices"].append([vert[0], vert[1]])
            self.convert_parameter_to_dict(temp_dict, connection.param.list)
            target_dict["connections"].append(temp_dict)

    def store_network_in_json(self, network_id):
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
        parameter = ParameterHandler()
        parameter.load_by_dict(param_dict)
        return parameter

    def read_neurons_from_dict(self, neurons_dict):
        for neuron in neurons_dict:
            try:
                neuron_list = self.networks[self.curr_network].neurons
                self.add_neuron(neuron["posx"], neuron["posy"], 25, self.curr_network)
                neuron_list[len(neuron_list)-1].param = self.read_parameter_list(neuron)
            except:
                pass

    def read_nodes_from_dict(self, nodes_dict):
        for node in nodes_dict:
            try:
                node_list = self.networks[self.curr_network].nodes
                self.add_neuron(node["posx"], node["posy"], 25, self.curr_network,
                                node["function"])
                node_list[len(node_list)-1].param = self.read_parameter_list(node)
            except:
                pass

    def read_subnets_from_dict(self, subnet_dict):
        error_ids = []
        for subnet in subnet_dict:
            try:
                self.add_subnet(subnet["network_name"], subnet["posx"], subnet["posy"], self.curr_network)
            except:
                error_ids.append(subnet["id"])
        return error_ids

    def read_connections_from_dict(self, connections_dict, error_subnets):
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

                if "next_neuron" in connection:
                    temp_connection.next_neuron_function = connection["next_neuron_function"]
                    temp_connection.next_subnet = connection["next_subnetwork"]
                    connection_list[len(connection_list) - 1].next_neuron = connection["next_neuron"]
                elif "next_connection" in connection:
                    connection_list[len(connection_list)-1].next_connection = connection["next_connection"]

                connection_list[len(connection_list)-1].param = self.read_parameter_list(connection)
            except:
                pass

    def load_network(self, filename=None):
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

    def save_network_by_dict(self, network_name, network_dict):
        network_json = json.dumps(network_dict, indent=4)
        with open(self.project_path + os.sep + "networks" + os.sep + network_name, "w") as file:
            file.write(network_json)

    def save_network(self, save_as):
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
        path = self.project_path + os.sep + "networks"
        return os.listdir(path)
