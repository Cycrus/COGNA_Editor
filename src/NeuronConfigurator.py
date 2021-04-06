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

        self.label_frame = tk.Frame(master=self.top_frame, background=design.dark_blue,
                                    borderwidth=0,
                                    highlightthickness=2,
                                    highlightbackground=design.grey_2,
                                    height=self.top_frame.winfo_height() // 7,
                                    width=self.top_frame.winfo_width())
        self.label_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.label = tk.Label(master=self.label_frame, background=design.dark_blue,
                              text="Neuron Type Configuration",
                              fg=design.grey_c)
        self.label.pack(pady=5)
        self.top_frame.update()

        self.editor = tk.Frame(master=self.top_frame, background=design.grey_4,
                               borderwidth=0,
                               highlightthickness=0,
                               height=self.top_frame.winfo_height() - (self.label_frame.winfo_height() * 2),
                               width=self.top_frame.winfo_width())
        self.editor.pack(side=tk.TOP, fill=tk.BOTH)

        self.parameter_frame = tk.Frame(master=self.editor, background=design.dark_blue,
                                        borderwidth=0,
                                        highlightthickness=0,
                                        height=self.editor.winfo_height(),
                                        width=self.top_frame.winfo_width()/2)
        self.parameter_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        
        self.placeholder1 = tk.Label(master=self.parameter_frame, text="Placeholder")
        self.placeholder1.pack(side=tk.TOP, pady=40)

        self.neuron_frame = tk.Frame(master=self.editor, background=design.dark_red,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     height=self.editor.winfo_height(),
                                     width= self.top_frame.winfo_width()/2)
        self.neuron_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.placeholder2 = tk.Label(master=self.neuron_frame, text="Placeholder")
        self.placeholder2.pack(side=tk.TOP, pady=40)

        self.button_frame = tk.Frame(master=self.top_frame, background=design.grey_4,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     height=self.top_frame.winfo_height() // 7,
                                     width=self.top_frame.winfo_width())
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        self.close_button = tk.Button(master=self.button_frame, text="Save & Close", background=design.grey_3,
                                      fg=design.grey_c, activebackground=design.grey_7,
                                      command=self.close_window)
        self.close_button.pack(side=tk.TOP, padx=self.top_frame.winfo_width()/7, pady=5)

    def __del__(self):
        self.close_window()

    def close_window(self):
        self.top_frame.destroy()
