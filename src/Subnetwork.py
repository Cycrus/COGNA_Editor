from src.GlobalLibraries import *


class SubnetNode:
    def __init__(self, id, posx, posy):
        self.id = id
        self.posx = posx
        self.posy = posy


class Subnetwork:
    def __init__(self, id, network_name, posx, posy, network_id, input_nodes, output_nodes):
        self.id = id
        self.network_name = network_name
        self.posx = posx
        self.posy = posy
        self.input_node_number = input_nodes
        self.output_node_number = output_nodes
        self.size_x = 200
        self.size_y = 100

        self.input_node_list = []
        self.output_node_list = []
        self.generate_node_lists()

        self.network_id = network_id

    def generate_node_lists(self):
        loop_number = (self.size_x * 4 + self.size_y * 4) // 50
        direction = "right"

        min_x = self.posx - self.size_x
        min_y = self.posy - self.size_y
        max_x = self.posx + self.size_x
        max_y = self.posy + self.size_y

        x_pos = min_x
        y_pos = min_y

        input_count = self.input_node_number
        output_count = self.output_node_number

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
                temp_node = SubnetNode(node_id, x_pos, y_pos)
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