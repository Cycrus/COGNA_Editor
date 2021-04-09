from src.Network import *
from src.Neuron import *
from src.Connection import *
from src.GlobalLibraries import *

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
        self.transmitters = ["Default"]
        self.neuron_types = [["Default", ParameterHandler()]]
        self.curr_network = 0
        self.add_network()

    def network_default_name(self, name_nr):
        name = "network-" + str(name_nr) + ".json"
        for file in self.filename:
            if name == file:
                name_nr = name_nr+1
                name = self.network_default_name(name_nr)
                break
        return name

    def add_network(self):
        self.networks.append(Network())
        self.curr_network = len(self.networks)-1
        temp_filename = self.network_default_name(1)
        self.filename.append(temp_filename)
        self.locations.append("networks/")
        self.fixed_location.append(False)
        self.camera_x.append(0.0)
        self.camera_y.append(0.0)
        self.zoom_factor.append(1.0)

    def add_neuron(self, posx, posy, size, network_id=0):
        self.networks[network_id].neurons.append(Neuron(len(self.networks[network_id].neurons)+null_neuron_correcter,
                                                        posx, posy, size, network_id))

    def delete_neuron(self, id, network_id=0):
        for connection in reversed(self.networks[network_id].connections):
            if connection.prev_neuron == id or connection.next_neuron == id:
                self.delete_connection(connection.id, network_id)

        for connection in self.networks[network_id].connections:
            if connection.prev_neuron > id-1:
                connection.prev_neuron = connection.prev_neuron - 1
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
        for connection in self.networks[network_id].connections:
            if connection.next_connection == id:
                self.delete_connection(connection.id, network_id)
        self.networks[network_id].connections.pop(id)
        for connection in reversed(self.networks[network_id].connections):
            if connection.id > id:
                connection.id = connection.id - 1

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

    def convert_network_to_json(self, network_id):
        print(f"Converting network {network_id} to json.")

    def save_network(self, save_as):
        file = None

        if not save_as:
            if not self.fixed_location[self.curr_network]:
                save_as = True
            else:
                file = open(self.locations[self.curr_network] + self.filename[self.curr_network], "w")

        if save_as:
            file = filedialog.asksaveasfile(initialdir=self.locations[self.curr_network], title="test",
                                            initialfile=self.filename[self.curr_network],
                                            filetypes=(("json files", "*.json"),("all files", "*")))
        if file:
            self.convert_network_to_json(self.curr_network)
            name_split = file.name.split("/")
            new_name = name_split[len(name_split)-1]
            self.filename[self.curr_network] = new_name
            new_location = ""
            for word in name_split:
                if word != new_name:
                    new_location = new_location + word + "/"
            self.locations[self.curr_network] = new_location
            self.fixed_location[self.curr_network] = True
            file.write("placeholder")
            file.close()
