# Color inverter: https://colorinverter.imageonline.co/


class Design:
    def __init__(self):
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
        self.dark_blue = ["#14405a", "#278fcd"]
        self.white = ["#FFFFFF", "#FFFFFF"]
        self.black = ["#000000", "#000000"]
        self.connection_width = 3
        self.selected_connection_width = self.connection_width+3
        self.editbutton_size_relation = 3

        self.button_padding_x = 5
        self.button_padding_y = 5

        self.zoom_widget_width = 8
        self.zoom_widget_padx = 20
        self.top_button_width = 4
        self.top_button_padx = 0
        self.top_button_pady = 2
        self.splash_width = 800
        self.splash_height = 300

        self.ui_scaling_factor = 1.0


design = Design()