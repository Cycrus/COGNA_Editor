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

        self.project_path = None
        self.project_name = None
        try:
            self.open_project(os.getcwd() + os.sep + "Projects" + os.sep + "DefaultProject")
        except:
            self.new_project("DefaultProject")

        self.curr_network = 0
        try:
            self.load_network(self.project_path + os.sep + "networks" + os.sep + "network-1.cogna")
        except Exception as e:
            print(e)
            self.add_network()

    def new_project(self, project_name):
        default_neuron_params = ParameterHandler()
        default_neuron_params.fill_in_params()

        try:
            os.mkdir(os.getcwd() + os.sep + "Projects")
        except:
            pass

        self.transmitters = ["Default"]
        self.neuron_types = [["Default", default_neuron_params]]

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
        self.save_transmitters()
        self.save_neuron_types()

    def open_project(self, path):
        if path[-1] == os.sep:
            path = path[:len(path)-1]
        self.project_name = path.split(os.sep)[-1]
        self.project_path = path
        self.load_transmitters(path)
        self.load_neuron_types(path)

    def save_meta_info(self):
        with open(self.project_path + os.sep + self.project_name + ".project", "w") as file:
            file.write("Valid COGNA Project\n")
            file.write(self.project_name)

    def save_transmitters(self):
        dict_obj = {"transmitters": self.transmitters}
        json_obj = json.dumps(dict_obj, indent=4)
        with open(self.project_path + os.sep + "transmitters.config", "w") as file:
            file.write(json_obj)

    def load_transmitters(self, project_path):
        with open(project_path + os.sep + "transmitters.config", "r") as file:
            transmitter_dict = json.loads(file.read())
            self.transmitters = transmitter_dict["transmitters"]

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

    def add_network(self, params=None):
        self.networks.append(Network(params))
        self.curr_network = len(self.networks)-1
        temp_filename = self.network_default_name(1)
        self.filename.append(temp_filename)
        self.locations.append(self.project_path + os.sep + "networks" + os.sep)
        self.fixed_location.append(False)
        self.camera_x.append(0.0)
        self.camera_y.append(0.0)
        self.zoom_factor.append(1.0)

    def add_neuron(self, posx, posy, size, network_id=0, function="neuron"):
        temp_neuron = Neuron(len(self.networks[network_id].neurons)+null_neuron_correcter,
                             posx, posy, size, network_id, function=function)
        self.networks[network_id].neurons.append(temp_neuron)

    def delete_subnet(self, id, network_id=0):
        for connection in reversed(self.networks[self.curr_network].connections):
            if connection.prev_subnet == id or connection.next_subnet == id:
                self.delete_connection(connection.id, self.curr_network)

        self.networks[network_id].subnets.pop(id)
        for subnet in reversed(self.networks[network_id].subnets):
            if subnet.id > id:
                subnet.id = subnet.id - 1

    def delete_neuron(self, id, network_id=0):
        for connection in reversed(self.networks[network_id].connections):
            if connection.prev_neuron == id or connection.next_neuron == id:
                self.delete_connection(connection.id, network_id)

        for connection in self.networks[network_id].connections:
            if connection.prev_neuron > id-1:
                connection.prev_neuron = connection.prev_neuron - 1
            if connection.next_neuron is not None:
                if connection.next_neuron > id-1:
                    connection.next_neuron = connection.next_neuron - 1

        self.networks[network_id].neurons.pop(id - 1)
        for neuron in reversed(self.networks[network_id].neurons):
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

    def store_network_param_in_dict(self, network_id):
        temp_dict = {}
        self.convert_parameter_to_dict(temp_dict, self.networks[network_id].param.list)
        return temp_dict

    def store_neurons_in_dict(self, target_dict, network_id):
        for neuron in self.networks[network_id].neurons:
            temp_dict = {}
            temp_dict["id"] = neuron.id
            temp_dict["posx"] = neuron.posx
            temp_dict["posy"] = neuron.posy
            self.convert_parameter_to_dict(temp_dict, neuron.param.list)
            target_dict["neurons"].append(temp_dict)

    def store_connections_in_dict(self, target_dict, network_id):
        for connection in self.networks[network_id].connections:
            temp_dict = {}
            temp_dict["id"] = connection.id
            temp_dict["vertices"] = []
            temp_dict["prev_neuron"] = connection.prev_neuron
            for vert in connection.vertices:
                temp_dict["vertices"].append([vert[0], vert[1]])
            if connection.next_neuron is not None:
                temp_dict["next_neuron"] = connection.next_neuron
            if connection.next_connection is not None:
                temp_dict["next_connection"] = connection.next_connection
            self.convert_parameter_to_dict(temp_dict, connection.param.list)
            target_dict["connections"].append(temp_dict)

    def store_network_in_json(self, network_id):
        network_dict = {}
        network_dict["network"] = self.store_network_param_in_dict(network_id)

        network_dict["neurons"] = []
        self.store_neurons_in_dict(network_dict, network_id)

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
            neuron_list = self.networks[self.curr_network].neurons
            self.add_neuron(neuron["posx"], neuron["posy"], 25, self.curr_network)
            neuron_list[len(neuron_list)-1].param = self.read_parameter_list(neuron)

    def read_connections_from_dict(self, connections_dict):
        for connection in connections_dict:
            connection_list = self.networks[self.curr_network].connections
            source_neuron = self.networks[self.curr_network].neurons[connection["prev_neuron"]-1]
            self.add_connection(source_neuron, self.curr_network)
            connection_list[len(connection_list)-1].vertices = connection["vertices"]
            
            if "next_neuron" in connection:
                connection_list[len(connection_list)-1].next_neuron = connection["next_neuron"]
            elif "next_connection" in connection:
                connection_list[len(connection_list)-1].next_connection = connection["next_connection"]

            connection_list[len(connection_list)-1].param = self.read_parameter_list(connection)

    def load_network(self, filename=None):
        if filename is None:
            file = filedialog.askopenfile(initialdir=self.project_path + os.sep + "networks", title="Save Network",
                                          filetypes=(("cogna network", "*.cogna"),))
        else:
            file = open(filename, "r")

        if not file:
            return Globals.ERROR
        if not self.project_path + os.sep + "networks" in file.name:
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
        self.read_connections_from_dict(network_dict["connections"])
        self.filename[self.curr_network] = network_name

        file.close()

        return Globals.SUCCESS

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
        if not (self.project_path + os.sep + "networks") in file.name:
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
