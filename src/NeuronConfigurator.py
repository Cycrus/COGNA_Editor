from src.GlobalLibraries import *
from src.NetworkManager import NetworkManager


class NeuronConfigurator:
    def __init__(self, root, network_manager):
        self.root_frame = root
        self.neuron_list = network_manager.neuron_types
        self.network_manager = network_manager
        self.frame_number = 30

        self.width = int(self.root_frame.winfo_screenwidth() / 1.4)
        self.height = int(self.root_frame.winfo_screenheight() / 1.4)
        self.pos_x = self.root_frame.winfo_width() // 2 - self.width // 2 + self.root_frame.winfo_x()
        self.pos_y = self.root_frame.winfo_height() // 2 - self.height // 2 + self.root_frame.winfo_y()
        self.top_frame = tk.Toplevel()
        self.top_frame.grab_set()
        self.top_frame.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")
        self.top_frame.overrideredirect(True)
        self.top_frame.configure(background=design.grey_4, highlightthickness=4,
                                 highlightbackground=design.grey_2)
        self.top_frame.update()