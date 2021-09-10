"""
NeuronConfigurator.py

Controls the dialog box for configuring the neuron types of the current project.

Author: Cyril Marx
Date: 09.09.2021
"""

from src.GlobalLibraries import *
from src.NetworkManager import NetworkManager
from src.ParameterHandler import ParameterHandler


class NeuronConfigurator:
    def __init__(self, root, mainframe, network_manager):
        """
        Constructor. Creates the dialog box.
        :param root:            The tkinter root frame.
        :param mainframe:       The mainframe of the program.
        :param network_manager: The network manager object of the program.
        :return:                None
        """
        self.root_frame = root
        self.mainframe = mainframe
        self.neuron_list = copy.deepcopy(network_manager.neuron_types)
        self.deleted_neurons = []
        self.network_manager = network_manager
        self.frame_number = 30
        self.curr_neuron = self.neuron_list[0][0]

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

        self.param_selection = tk.StringVar()
        self.param_textbox = []
        self.param_info = []

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
            self.param_frames[idx].pack(side=tk.TOP, anchor="w")

        self.top_frame.update()

        self.param_drop_menu = tk.OptionMenu(self.param_frames[0], self.param_selection,
                                             *ParameterHandler.param_drop_options_neuron,
                                             command=self.render_parameter)
        self.param_drop_menu.config(bg=design.grey_4[design.theme], width=50,
                                    fg=design.grey_c[design.theme],
                                    borderwidth=0, highlightthickness=3, highlightbackground=design.grey_2[design.theme],
                                    activebackground=design.grey_7[design.theme])
        self.param_drop_menu.pack(side=tk.TOP, pady=20)

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
            self.nbutton_frames[idx].pack(side=tk.TOP, anchor="w")
        self.neuron_buttons = []

        self.button_frame = tk.Frame(master=self.top_frame, background=design.grey_4[design.theme],
                                     borderwidth=0,
                                     highlightthickness=0,
                                     height=self.top_frame.winfo_height() // 7,
                                     width=self.top_frame.winfo_width())
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        self.close_button = tk.Button(master=self.button_frame, text="Discard", background=design.grey_3[design.theme],
                                      fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                      command=lambda x=False: self.close_window(x))
        self.save_button = tk.Button(master=self.button_frame, text="Save & Close", background=design.grey_3[design.theme],
                                     fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                     command=lambda x=True: self.close_window(x))
        self.close_button.pack(side=tk.LEFT, padx=80, pady=5)
        self.save_button.pack(side=tk.RIGHT, padx=80, pady=5)

        self.render_buttons()
        self.render_parameter(store=False)

        self.top_frame.bind("<Return>", self.render_parameter)

    def __del__(self):
        """
        Destructor.
        """
        self.close_window(save=False)

    def render_buttons(self):
        """
        Renders all buttons on the dialog box.
        :return:    None
        """
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
            temp_n_button = tk.Button(master=self.nbutton_frames[idx], text=neuron[0],
                                      background=background_col, fg=design.grey_c[design.theme],
                                      activebackground=design.grey_7[design.theme],
                                      command=lambda i=neuron: self.switch_neuron(n=i))
            temp_del_button = tk.Button(master=self.nbutton_frames[idx], text="Delete",
                                        background=design.grey_3[design.theme], fg=design.grey_c[design.theme],
                                        activebackground=design.grey_7[design.theme],
                                        command=lambda i=neuron: self.del_neuron(n=i))
            self.neuron_buttons.append([temp_n_button, temp_del_button])

        add_button = tk.Button(master=self.nbutton_frames[len(self.neuron_list)], text="Add Neuron Type",
                               background=design.grey_3[design.theme], fg=design.grey_c[design.theme],
                               activebackground=design.grey_7[design.theme],
                               command=self.add_neuron_window)
        self.neuron_buttons.append([add_button, None])

        for idx, button in enumerate(self.neuron_buttons):
            if button[0] is not None:
                button[0].pack(side=tk.LEFT, pady=20, padx=20)
            if button[1] is not None and idx != 0:
                button[1].pack(side=tk.RIGHT, pady=20, padx=20)

    def print_parameter(self, entity, param_index, param_name):
        """
        Prints a parameter into its widget.
        :param entity:      The neuron type entity which is addressed for printing.
        :param param_index: The index of the printed parameter.
        :param param_name:  The name of the printed parameter.
        """
        if entity.list[param_name] is None:
            self.param_textbox[param_index][0].insert(tk.END, "Invalid")
            self.param_textbox[param_index][0].config(fg=design.dark_red[design.theme])
        else:
            param_string = ParameterHandler.deny_scientific_notation(entity.list[param_name])
            self.param_textbox[param_index][0].insert(tk.END, param_string)

    def get_current_neuron_entity(self):
        """
        Returns the currently active neuron type entity.
        :return:    The currently active neuron type entity.
        """
        curr_neuron_entity = None
        for idx, neuron in enumerate(self.neuron_list):
            if self.curr_neuron == neuron[0]:
                curr_neuron_entity = neuron[1]

        return curr_neuron_entity

    def store_option_parameter(self, option, name):
        """
        Stores a parameter in the neuron type.
        :param option:  The new value of the parameter.
        :param name:    The name of the addressed parameter.
        :return:        None
        """
        curr_neuron_entity = self.get_current_neuron_entity()
        curr_neuron_entity.list[name] = option

    def store_parameter(self):
        """
        Saves all parameters of the currently active neuron type.
        :return:    None
        """
        curr_neuron_entity = self.get_current_neuron_entity()

        for idx, container in enumerate(self.param_textbox):
            if not ParameterHandler.is_menu(container[1]):
                temp_param = container[0].get()
                try:
                    curr_neuron_entity.list[container[1]] = float(temp_param)
                except ValueError:
                    curr_neuron_entity.list[container[1]] = None

    def render_parameter(self, event=None, store=True):
        """
        Renders all parameters and their widgets.
        :param event:   tkinter parameter for event callback.
        :param store:   A boolean indicating if the parameters should be stored before rendering.
        :return:        None
        """
        if store:
            self.store_parameter()

        curr_neuron_entity = self.get_current_neuron_entity()

        for i in range(0, len(self.param_info)):
            self.param_info[i].destroy()
        self.param_info.clear()
        for i in range(0, len(self.param_textbox)):
            self.param_textbox[i][0].destroy()
        self.param_textbox.clear()

        self.param_list = ParameterHandler.get_paramter_list(self.param_selection, "NeuronType")

        for i, name in enumerate(self.param_list):
            if ParameterHandler.is_menu(name):
                var = tk.StringVar()
                var.set(curr_neuron_entity.list[name])
                menu = ParameterHandler.get_option_menu_list(name, self.network_manager)

                self.param_textbox.append([tk.OptionMenu(self.param_frames[i + 1],
                                                         var,
                                                         *menu,
                                                         command=lambda option, n=name: self.store_option_parameter(option=option,
                                                                                                                    name=n)),
                                           name])

                self.param_textbox[i][0].config(bg=design.grey_7[design.theme], width=15,
                                                fg=design.black[design.theme],
                                                borderwidth=0, highlightthickness=3,
                                                highlightbackground=design.grey_2[design.theme],
                                                activebackground=design.grey_7[design.theme])
            else:
                self.param_textbox.append([tk.Entry(master=self.param_frames[i + 1], width=20,
                                                    fg=design.black[design.theme],
                                                    bg=design.grey_7[design.theme], borderwidth=0,
                                                    highlightthickness=2,
                                                    highlightbackground=design.grey_2[design.theme]),
                                           name])

                self.print_parameter(curr_neuron_entity, i, name)
            self.param_textbox[i][0].pack(side=tk.LEFT, padx=20, pady=10)

            self.param_info.append(tk.Label(master=self.param_frames[i+1], text=name,
                                            bg=design.grey_4[design.theme], fg=design.grey_c[design.theme]))
            self.param_info[i].pack(side=tk.LEFT, padx=20, pady=10)

    def switch_neuron(self, n):
        """
        Switches the currently active neuron and calls all functions for that.
        :param n:   The name of the neuron which should be activated.
        :return:    None
        """
        self.store_parameter()
        self.curr_neuron = n[0]
        self.render_buttons()
        self.render_parameter(store=False)

    def del_neuron(self, n):
        """
        Deletes a neuron type based on its name.
        :param n:   The name of the neuron which should be activated.
        :return:    None
        """
        for idx, neuron in enumerate(self.neuron_list):
            if n == neuron:
                self.deleted_neurons.append(neuron[0])
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
        """
        Activates another dialog box for naming a new neuron.
        :return:    None
        """
        def add_neuron():
            self.store_parameter()
            name = add_entry.get()
            if name:
                can_add = True
                for check_name in self.neuron_list:
                    if name == check_name[0]:
                        can_add = False
                if can_add:
                    self.neuron_list.append([name, copy.deepcopy(self.neuron_list[0][1])])
                    self.curr_neuron = name

            add_frame.grab_release()
            add_frame.destroy()
            self.render_buttons()
            self.top_frame.grab_set()
            self.top_frame.update_idletasks()
            self.render_parameter(store=False)

        self.top_frame.grab_release()
        add_width = int(self.top_frame.winfo_width() / 3)
        add_height = int(self.top_frame.winfo_height() / 8)
        add_pos_x = self.root_frame.winfo_screenwidth() // 2 - add_width // 2
        add_pos_y = self.root_frame.winfo_screenheight() // 2 - add_height // 2
        add_frame = tk.Toplevel()
        add_frame.geometry(f"{add_width}x{add_height}+{add_pos_x}+{add_pos_y}")
        add_frame.overrideredirect(True)
        add_frame.update_idletasks()
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

    def close_window(self, save):
        """
        Closes the dialog box and saves the neuron types.
        :param save:    A boolean indicating if the neuron types should be saved.
        :return:        None
        """
        if save:
            self.store_parameter()
            error_code = self.network_manager.save_storing(["neuron_type"], self.deleted_neurons, [self.neuron_list[0][0]])
            if error_code == Globals.SUCCESS:
                self.network_manager.neuron_types = copy.deepcopy(self.neuron_list)
                self.network_manager.save_neuron_types()
        self.top_frame.grab_release()
        self.top_frame.destroy()
        self.mainframe.show_editmenu(store=False)
