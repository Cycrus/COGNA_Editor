"""
Subnetwork.py

The class containing all information of a subnetwork.

Author: Cyril Marx
Date: 09.09.2021
"""

from src.GlobalLibraries import *
from src.Neuron import *


class Subnetwork:
    def __init__(self, id, network_name, posx, posy, network_id, input_nodes, output_nodes):
        """
        Constructor.
        :param id:              The ID of the new subnetwork.
        :param network_name:    The name of the new subnetwork.
        :param posx:            x position of the new subnetwork.
        :param posy:            y position of the new subnetwork.
        :param network_id:      The ID of the network where the subnetwork should be added in.
        :param input_nodes:     The number of input nodes of the subnetwork.
        :param output_nodes:    The number of output nodes of the subnetwork.
        :return:                None
        """
        self.id = id
        self.network_name = network_name
        self.posx = posx
        self.posy = posy
        self.input_node_number = input_nodes
        self.output_node_number = output_nodes
        self.size_x = 200
        self.size_y = 100
        self.node_size = 18

        self.param = ParameterHandler()

        self.input_node_list = []
        self.output_node_list = []

        self.network_id = network_id

        self.generate_node_lists()

    def generate_node_lists(self):
        """
        Generates the input and output nodes which are drawn to the screen.
        :return:    None
        """
        loop_number = (self.size_x * 4 + self.size_y * 4) // 50
        direction = "right"

        min_x = self.posx - self.size_x
        min_y = self.posy - self.size_y
        max_x = self.posx + self.size_x
        max_y = self.posy + self.size_y

        x_pos = min_x
        y_pos = min_y

        output_count = self.input_node_number
        input_count = self.output_node_number

        for pos in range(0, loop_number):
            can_create = False
            node_id = 0
            type = "input"

            if output_count > 0 and input_count > 0:
                if pos % 2 == 0:
                    type = "input"
                    if input_count > 0:
                        can_create = True
                        node_id = len(self.input_node_list) + 1
                        input_count = input_count - 1
                else:
                    type = "output"
                    if output_count > 0:
                        can_create = True
                        node_id = len(self.output_node_list) + 1
                        output_count = output_count - 1
            else:
                if output_count == 0:
                    type = "input"
                    if input_count > 0:
                        can_create = True
                        node_id = len(self.input_node_list) + 1
                        input_count = input_count - 1
                elif input_count == 0:
                    type = "output"
                    if output_count > 0:
                        can_create = True
                        node_id = len(self.output_node_list) + 1
                        output_count = output_count - 1

            if can_create:
                temp_node = Neuron(node_id, x_pos, y_pos, self.node_size,
                                   network_id=self.network_id, subnet_id=self.id, function=type)
                if type == "input":
                    self.input_node_list.append(temp_node)
                elif type == "output":
                    self.output_node_list.append(temp_node)

                if x_pos == max_x and y_pos == min_y:
                    direction = "down"
                elif x_pos == max_x and y_pos == max_y:
                    direction = "left"
                elif x_pos == min_x and y_pos == max_y:
                    direction = "up"

                if direction == "right":
                    x_pos = x_pos + 50
                elif direction == "left":
                    x_pos = x_pos - 50
                if direction == "down":
                    y_pos = y_pos + 50
                elif direction == "up":
                    y_pos = y_pos - 50

    def set_node_position(self, prev_x, prev_y, new_x, new_y):
        """
        Resets the position of all nodes if the subnetwork moves.
        :param prev_x:  The previous x position of the subnetwork.
        :param prev_y:  The previous y position of the subnetwork.
        :param new_x:   The new x position of the subnetwork.
        :param new_y:   The new y position of the subnetwork.
        """
        for node in chain(self.input_node_list, self.output_node_list):
            node.posx = node.posx + (new_x - prev_x)
            node.posy = node.posy + (new_y - prev_y)
