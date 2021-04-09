from src.GlobalLibraries import *
from src.NetworkManager import NetworkManager
from src.ParameterHandler import ParameterHandler


class NeuronConfigurator:
    def __init__(self, root, network_manager):
        self.root_frame = root
        self.neuron_list = network_manager.neuron_types
        self.network_manager = network_manager
        self.frame_number = 30
        self.curr_neuron = self.neuron_list[0][0]
        self.frame_number = 50

        self.width = int(self.root_frame.winfo_screenwidth() / 1.4)
        self.height = int(self.root_frame.winfo_screenheight() / 1.4)
        self.pos_x = self.root_frame.winfo_screenwidth() // 2 - self.width // 2
        self.pos_y = self.root_frame.winfo_screenheight() // 2 - self.height // 2
        self.top_frame = tk.Toplevel()
        self.top_frame.grab_set()
        self.top_frame.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")
        self.top_frame.overrideredirect(True)
        self.top_frame.configure(background=design.grey_4[design.theme], highlightthickness=4,
                                 highlightbackground=design.grey_2[design.theme])
        self.top_frame.update()

        self.param_drop_options = ["Connection Specific",
                                   "Connection Habituation",
                                   "Connection Sensitization",
                                   "Connection Presynaptic",
                                   "Neuron Activation",
                                   "Neuron Transmitter",
                                   "Neuron Random",
                                   "Network"]
        self.param_selection = tk.StringVar()
        self.param_selection.set(self.param_drop_options[0])

        self.label_frame = tk.Frame(master=self.top_frame, background=design.dark_blue[design.theme],
                                    borderwidth=0,
                                    highlightthickness=2,
                                    highlightbackground=design.grey_2[design.theme],
                                    height=self.top_frame.winfo_height() // 7,
                                    width=self.top_frame.winfo_width())
        self.label_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self.label = tk.Label(master=self.label_frame, background=design.dark_blue[design.theme],
                              text="Neuron Type Configuration",
                              fg=design.grey_c[design.theme])
        self.label.pack(pady=5)
        self.top_frame.update()

        self.editor = tk.Frame(master=self.top_frame, background=design.grey_4[design.theme],
                               borderwidth=0,
                               highlightthickness=0,
                               height=self.top_frame.winfo_height() - (self.label_frame.winfo_height() * 2),
                               width=self.top_frame.winfo_width())
        self.editor.pack(side=tk.TOP, fill=tk.BOTH, pady=20, padx=20)

        self.parameter_frame = tk.Frame(master=self.editor, background=design.grey_4[design.theme],
                                        borderwidth=0,
                                        highlightthickness=0,
                                        height=self.editor.winfo_height(),
                                        width=self.top_frame.winfo_width()/2)
        self.parameter_frame.pack(side=tk.LEFT, fill=tk.BOTH, pady=20, padx=20)

        self.param_frames = []
        for idx in range(0, self.frame_number):
            self.param_frames.append(tk.Frame(master=self.parameter_frame, background=design.grey_4[design.theme],
                                              borderwidth=0, highlightthickness=0))
            self.param_frames[idx].pack(side=tk.TOP)

        self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[0], self.param_selection, *self.param_drop_options,
                                            command=self.render_parameter)
        self.edit_drop_menu.config(bg=design.grey_4[design.theme], width=self.parameter_frame.winfo_width(),
                                   fg=design.grey_c[design.theme],
                                   borderwidth=0, highlightthickness=3, highlightbackground=design.grey_2[design.theme],
                                   activebackground=design.grey_7[design.theme])
        self.edit_drop_menu.pack(side=tk.TOP, pady=20)

        self.neuron_frame = tk.Frame(master=self.editor, background=design.grey_4[design.theme],
                                     borderwidth=0,
                                     highlightthickness=0,
                                     height=self.editor.winfo_height(),
                                     width= self.top_frame.winfo_width()/2)
        self.neuron_frame.pack(side=tk.RIGHT, fill=tk.BOTH, pady=20, padx=20)

        self.nbutton_frames = []
        for idx in range(0, self.frame_number):
            self.nbutton_frames.append(tk.Frame(master=self.neuron_frame, background=design.grey_4[design.theme],
                                                borderwidth=0, highlightthickness=0))
            self.nbutton_frames[idx].pack(side=tk.TOP)
        self.neuron_buttons = []

        self.button_frame = tk.Frame(master=self.top_frame, background=design.grey_4[design.theme],
                                     borderwidth=0,
                                     highlightthickness=0,
                                     height=self.top_frame.winfo_height() // 7,
                                     width=self.top_frame.winfo_width())
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        self.close_button = tk.Button(master=self.button_frame, text="Save & Close", background=design.grey_3[design.theme],
                                      fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                      command=self.close_window)
        self.close_button.pack(side=tk.TOP, padx=self.top_frame.winfo_width()/7, pady=5)

        self.render_buttons()
        self.render_parameter()

    def __del__(self):
        self.close_window()

    def render_buttons(self):
        for buttons in self.neuron_buttons:
            if buttons[0] is not None:
                buttons[0].forget()
            if buttons[1] is not None:
                buttons[1].forget()
        self.neuron_buttons.clear()

        for idx, neuron in enumerate(self.neuron_list):
            if self.curr_neuron == neuron[0]:
                background_col = design.dark_blue[design.theme]
            else:
                background_col = design.grey_3[design.theme]
            temp_n_button = tk.Button(master=self.nbutton_frames[idx+1], text=neuron[0],
                                      background=background_col, fg=design.grey_c[design.theme],
                                      activebackground=design.grey_7[design.theme],
                                      command=lambda i=neuron: self.switch_neuron(n=i))
            temp_del_button = tk.Button(master=self.nbutton_frames[idx+1], text="Delete",
                                        background=design.grey_3[design.theme], fg=design.grey_c[design.theme],
                                        activebackground=design.grey_7[design.theme],
                                        command=lambda i=neuron: self.del_neuron(n=i))
            self.neuron_buttons.append([temp_n_button, temp_del_button])

        add_button = tk.Button(master=self.nbutton_frames[len(self.neuron_list)+1], text="Add Neuron Type",
                               background=design.grey_3[design.theme], fg=design.grey_c[design.theme],
                               activebackground=design.grey_7[design.theme],
                               command=self.add_neuron_window)
        self.neuron_buttons.append([add_button, None])

        for idx, button in enumerate(self.neuron_buttons):
            if button[0] is not None:
                button[0].pack(side=tk.LEFT, pady=20, padx=20)
            if button[1] is not None and idx != 0:
                button[1].pack(side=tk.RIGHT, pady=20, padx=20)

    def render_parameter(self):
        print("rendered parameter")

    def switch_neuron(self, n):
        self.curr_neuron = n[0]
        self.render_buttons()

    def del_neuron(self, n):
        for idx, neuron in enumerate(self.neuron_list):
            if n == neuron:
                self.neuron_list.pop(idx)

        change_curr_neuron = True
        for idx, neuron in enumerate(self.neuron_list):
            if n == neuron:
                change_curr_neuron = False
        if change_curr_neuron:
            self.curr_neuron = self.neuron_list[len(self.neuron_list)-1][0]

        self.render_buttons()
        self.render_parameter()

    def add_neuron_window(self):
        def add_neuron():
            name = add_entry.get()
            if name:
                can_add = True
                for check_name in self.neuron_list:
                    if name == check_name[0]:
                        can_add = False
                if can_add:
                    self.neuron_list.append([name, ParameterHandler()])

            add_frame.destroy()
            self.render_buttons()

        add_width = int(self.top_frame.winfo_width() / 3)
        add_height = int(self.top_frame.winfo_height() / 8)
        add_pos_x = self.root_frame.winfo_screenwidth() // 2 - add_width // 2
        add_pos_y = self.root_frame.winfo_screenheight() // 2 - add_height // 2
        add_frame = tk.Toplevel()
        add_frame.geometry(f"{add_width}x{add_height}+{add_pos_x}+{add_pos_y}")
        add_frame.overrideredirect(True)
        add_frame.configure(background=design.grey_4[design.theme], highlightthickness=4,
                            highlightbackground=design.grey_2[design.theme])
        add_frame.update()

        add_entry = tk.Entry(master=add_frame, width=20, bg=design.grey_7[design.theme], borderwidth=0,
                             highlightthickness=2, highlightbackground=design.grey_2[design.theme])
        add_entry.pack(side=tk.TOP, pady=10)

        add_button = tk.Button(master=add_frame, background=design.grey_3[design.theme], fg=design.grey_c[design.theme],
                               activebackground=design.grey_7[design.theme], text="Confirm & Close",
                               command=add_neuron)
        add_button.pack(side=tk.BOTTOM, pady=10)

        add_frame.grab_set()

    def close_window(self):
        self.top_frame.destroy()
