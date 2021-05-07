from src.GlobalLibraries import *


class Subnetwork:
    def __init__(self, id, network_name, posx, posy, network_id, input_nodes, output_nodes):
        self.id = id
        self.network_name = network_name
        self.posx = posx
        self.posy = posy
        self.input_nodes = input_nodes
        self.output_nodes = output_nodes
        self.size_x = 200
        self.size_y = 100

        self.network_id = network_id
