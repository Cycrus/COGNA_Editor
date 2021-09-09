"""
Design.py

The class containing all colors, sizes and positions of tkinter widgets and objects in the program.

Author: Cyril Marx
Date: 09.09.2021
"""

class Design:
    def __init__(self):
        """
        Constructor. Change values here to change the appearance of the editor.
        :return:    None
        """
        self.theme = 0

        self.grey_c = ["#CCCCCC", "#333333"]
        self.dark_red = ["#AA0000", "#ef0000"]
        self.grey_4 = ["#444444", "#aaaaaa"]
        self.grey_5 = ["#555555", "#aaaaaa"]
        self.grey_2 = ["#222222", "#dddddd"]
        self.grey_3 = ["#333333", "#cccccc"]
        self.grey_1 = ["#111111", "#222222"]
        self.grey_7 = ["#777777", "#cccccc"]
        self.light_blue = ["#1cd4d8", "#107F81"]
        self.light_red = ["#f03b3b", "#9a2020"]
        self.light_green = ["#3ddb38", "#2d9829"]
        self.dark_blue = ["#14405a", "#278fcd"]
        self.white = ["#FFFFFF", "#FFFFFF"]
        self.black = ["#000000", "#000000"]
        self.connection_width = 13
        self.selected_connection_width = self.connection_width+3
        self.editbutton_size_relation = 3

        self.button_padding_x = 5
        self.button_padding_y = 5

        self.zoom_widget_width = 8
        self.zoom_widget_padx = 20
        self.top_button_width = 4
        self.top_button_padx = 0
        self.top_button_pady = 2
        self.splash_width = 1200
        self.splash_height = 500

        self.ui_scaling_factor = 1.0

        self.neuron_size = 25


# Creates a global instance of the Design class all other classes can access.
design = Design()