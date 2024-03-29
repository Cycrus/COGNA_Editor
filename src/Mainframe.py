"""
Mainframe.py

The class controlling the appearance and function of the whole editor and parameter area.

Author: Cyril Marx
Date: 09.09.2021
"""

from src.GlobalLibraries import *
from src.ParameterHandler import ParameterHandler
from src.VectorUtils import VectorUtils

TOOL_NEURONS = 0
TOOL_CONNECTIONS = 1
TOOL_SELECT = 2
TOOL_IMPORT = 3
TOOL_EXCHANGE = 4


class Mainframe:
    def __init__(self, root, network_manager):
        """
        Constructor. Creates frames, widgets, etc.
        :param root: The root frame/window of program.
        :param network_manager: The object handling all currently opened networks.
        :return:    None
        """
        self.neuron_size = design.neuron_size

        self.cursor_x = 0.0
        self.cursor_y = 0.0

        self.prev_wheel_pos_x = 0.0
        self.prev_wheel_pos_y = 0.0
        self.next_wheel_pos_x = 0.0
        self.next_wheel_pos_y = 0.0

        self.tool = TOOL_NEURONS
        self.selected_neuron = -1
        self.selected_connection = -1
        self.selected_function = ""
        self.selected_entity = network_manager.networks[network_manager.curr_network]
        self.move_entity = False

        self.connecting_neuron = None
        self.connection_source_neuron = None

        self.clipboard = None

        self.root_frame = root
        self.network_manager = network_manager
        self.param_list = network_parameter

        self.root_frame.update()

        self.editframe_width = int(self.root_frame.winfo_width()/3.5)
        self.pixelVirtual = tk.PhotoImage(width=1, height=1)

        self.edit_selection = tk.StringVar()
        self.parameter_count = 50
        self.parameter_frame = []
        self.parameter_info = []
        self.parameter_textbox = []
        self.do_connection = False
        self.grid_size = 50
        self.grid_snap = True

        self.network_option = tk.StringVar()

        self.exchange_option = tk.StringVar()
        self.option_list = ["Interface Input", "Interface Output", "Subnet Input", "Subnet Output"]
        
        self.mainframe = None
        self.editframe = None
        self.editresize = None
        self.edit_top = None
        self.project_name_label = None
        self.select_button = None
        self.neuron_button = None
        self.connection_button = None
        self.import_button = None
        self.exchange_button = None
        self.viewframe = None
        self.editorcanvas = None
        self.edit_1 = None
        self.general_info = None
        self.connection_info = None
        self.id_info = None
        self.edit_drop_menu = None

    def pack_widgets(self):
        """
        Places all GUI widgets onto the screen. Called in UI.py, to ensure correct
        order of widgets.
        :return:    None
        """
        self.mainframe = tk.Frame(master=self.root_frame, background=design.grey_7[design.theme],
                                  borderwidth=0,
                                  highlightthickness=1,
                                  highlightbackground=design.grey_2[design.theme],
                                  height=self.root_frame.winfo_height(),
                                  width=self.root_frame.winfo_width())
        self.mainframe.grid_columnconfigure(0, weight=1)

        self.editframe = tk.Frame(master=self.mainframe, background=design.grey_4[design.theme],
                                  borderwidth=2,
                                  highlightthickness=0,
                                  height=self.mainframe.winfo_height(),
                                  width=self.editframe_width,
                                  relief=tk.FLAT)
        self.editframe.pack_propagate(0)

        self.editresize = tk.Frame(master=self.editframe, background=design.grey_2[design.theme],
                                   borderwidth=1,
                                   highlightthickness=0,
                                   height=self.mainframe.winfo_height(),
                                   width=7,
                                   relief=tk.FLAT,
                                   cursor="sb_h_double_arrow")
        self.editresize.pack(side=tk.RIGHT, fill=tk.BOTH, padx=0, pady=0, expand=True)

        self.edit_top = tk.Frame(master=self.editframe, background=design.grey_4[design.theme],
                                 borderwidth=0,
                                 highlightthickness=0,
                                 width=self.editframe_width)

        self.mainframe.pack(side=tk.TOP, fill=tk.BOTH, padx=0, pady=0, expand=True)
        self.editframe.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0, expand=False)
        self.edit_top.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=15, expand=False)

        self.root_frame.update()

        self.select_button = tk.Button(master=self.edit_top, text="S", background=design.grey_3[design.theme],
                                       fg=design.grey_c[design.theme], command=self.switch_tool_select, image=self.pixelVirtual,
                                       activebackground=design.grey_7[design.theme],
                                       width=50, relief=tk.FLAT, compound="c")
        self.neuron_button = tk.Button(master=self.edit_top, text="N", background=design.dark_blue[design.theme],
                                       fg=design.grey_c[design.theme], command=self.switch_tool_neurons, image=self.pixelVirtual,
                                       activebackground=design.grey_7[design.theme],
                                       width=50, relief=tk.FLAT, compound="c")
        self.connection_button = tk.Button(master=self.edit_top, text="C", background=design.grey_3[design.theme],
                                           fg=design.grey_c[design.theme], command=self.switch_tool_connections, image=self.pixelVirtual,
                                           activebackground=design.grey_7[design.theme],
                                           width=50, relief=tk.FLAT, compound="c")
        self.import_button = tk.Button(master=self.edit_top, text="I", background=design.grey_3[design.theme],
                                       fg=design.grey_c[design.theme], command=self.switch_tool_import, image=self.pixelVirtual,
                                       activebackground=design.grey_7[design.theme],
                                       width=50, relief=tk.FLAT, compound="c")
        self.exchange_button = tk.Button(master=self.edit_top, text="E", background=design.grey_3[design.theme],
                                         fg=design.grey_c[design.theme], command=self.switch_tool_exchange,
                                         image=self.pixelVirtual,
                                         activebackground=design.grey_7[design.theme],
                                         width=50, relief=tk.FLAT, compound="c")

        self.viewframe = tk.Frame(master=self.mainframe, background=design.grey_3[design.theme],
                                  highlightthickness=0,
                                  borderwidth=2,
                                  height=self.editframe.winfo_height(),
                                  width=self.mainframe.winfo_width() - self.editframe.winfo_width())
        self.viewframe.grid_columnconfigure(0, weight=1)

        self.editorcanvas = tk.Canvas(master=self.viewframe, background=design.grey_3[design.theme],
                                      highlightthickness=0,
                                      borderwidth=0,
                                      height=self.viewframe.winfo_height(),
                                      width=self.viewframe.winfo_width(),
                                      cursor="crosshair")

        self.edit_1 = tk.Frame(master=self.editframe, background=design.grey_4[design.theme],
                               borderwidth=0,
                               highlightthickness=0,
                               width=self.editframe_width)
        
        for i in range(0, self.parameter_count):
            self.parameter_frame.append(tk.Frame(master=self.editframe, background=design.grey_4[design.theme],
                                                 borderwidth=0,
                                                 highlightthickness=0,
                                                 width=self.editframe_width))

        self.project_name_label = tk.Label(master=self.parameter_frame[0], text=self.network_manager.project_name,
                                           bg=design.grey_4[design.theme], fg=design.light_blue[design.theme])

        self.general_info = tk.Label(master=self.parameter_frame[1], text="No Entity Selected", bg=design.grey_4[design.theme],
                                     fg=design.light_blue[design.theme])
        self.id_info = tk.Label(master=self.parameter_frame[2], text="", bg=design.grey_4[design.theme],
                                fg=design.grey_c[design.theme])

        self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[3], self.edit_selection,
                                            *ParameterHandler.param_drop_options_all,
                                            command=self.show_editmenu)
        self.edit_drop_menu.config(bg=design.grey_4[design.theme], width=self.editframe_width, fg=design.grey_c[design.theme],
                                   borderwidth=0, highlightthickness=3, highlightbackground=design.grey_2[design.theme],
                                   activebackground=design.grey_7[design.theme])

        self.select_button.pack(side=tk.LEFT, padx=design.button_padding_x, pady=design.button_padding_y)
        self.neuron_button.pack(side=tk.LEFT, padx=design.button_padding_x, pady=design.button_padding_y)
        self.connection_button.pack(side=tk.LEFT, padx=design.button_padding_x, pady=design.button_padding_y)
        self.import_button.pack(side=tk.LEFT, padx=design.button_padding_x, pady=design.button_padding_y)
        self.exchange_button.pack(side=tk.LEFT, padx=design.button_padding_x, pady=design.button_padding_y)

        for i in range(0, self.parameter_count):
            padding_y = 10
            if i == 2:
                padding_y = 40
            self.parameter_frame[i].pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=padding_y, expand=False)

        self.project_name_label.pack(side=tk.LEFT)
        self.edit_1.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=20, expand=False)

        self.viewframe.pack(side=tk.LEFT, fill=tk.BOTH, padx=0, pady=0, expand=True)
        self.editorcanvas.pack(side=tk.RIGHT, fill=tk.BOTH, padx=0, pady=0, expand=True)

        self.root_frame.update()
        self.network_manager.camera_x[self.network_manager.curr_network] = self.editorcanvas.winfo_width() / 2
        self.network_manager.camera_y[self.network_manager.curr_network] = self.editorcanvas.winfo_height() / 2
        self.render_scene()

        self.show_editmenu(store=False)

        self.editresize.bind("<Button-1>", self.init_resize)
        self.editresize.bind("<B1-Motion>", self.do_resize)

        self.editorcanvas.bind("<Motion>", self.motion_event)

        self.editorcanvas.bind("<Button-2>", self.init_camera)
        self.editorcanvas.bind("<B2-Motion>", self.move_camera)
        self.editorcanvas.bind("<Button-1>", self.left_click)
        self.editorcanvas.bind("<ButtonRelease-1>", self.release_left_click)
        self.editorcanvas.bind("<B1-Motion>", self.move_entity_event)
        self.editorcanvas.bind("<Button-3>", self.delete_entity)
        # Windows Mouse Wheel
        self.editorcanvas.bind("<MouseWheel>", self.zoom_scene)
        # Linux Mouse Wheel
        self.editorcanvas.bind("<Button-4>", self.zoom_scene)
        self.editorcanvas.bind("<Button-5>", self.zoom_scene)

        self.root_frame.bind("<Escape>", self.escape_event)
        self.root_frame.bind("<Delete>", self.delete_event)
        self.root_frame.bind("<Tab>", self.tab_event)
        self.root_frame.bind("<g>", self.toggle_grid_snap)
        self.root_frame.bind("<space>", self.reset_camera)
        self.root_frame.bind("<Return>", self.show_editmenu)

        self.root_frame.bind("<Control-c>", self.copy_entity)
        self.root_frame.bind("<Control-v>", self.paste_entity)

        self.switch_tool_select()

    def copy_entity(self, event=None):
        """
        An event handler for copying the parameters of a selected entity.
        Uses the self.selected_entity member variable.
        :parameter event:   tkinter event parameter.
        :return:            None
        """
        if self.tool == TOOL_SELECT:
            if self.selected_entity is not None:
                self.clipboard = copy.deepcopy(self.selected_entity)
            else:
                self.clipboard = None
        if isinstance(self.clipboard, Connection):
            if "input" in self.clipboard.prev_neuron_function:
                self.clipboard = None
        if isinstance(self.clipboard, Subnetwork):
            self.clipboard = None

    def paste_entity(self, event=None):
        """
        An event handler for pasting the copied parameters of a selected entity.
        Uses the self.selected_entity member variable.
        :parameter event:   tkinter event parameter.
        :return:            None
        """
        if self.tool == TOOL_SELECT and self.selected_entity is not None and self.clipboard is not None:
            if isinstance(self.selected_entity, type(self.clipboard)):
                can_copy = True

                if isinstance(self.clipboard, Neuron):
                    if self.clipboard.function != self.selected_entity.function:
                        can_copy = False

                if isinstance(self.clipboard, Connection):
                    if "input" in self.selected_entity.prev_neuron_function:
                        can_copy = False

                if can_copy:
                    self.selected_entity.param = copy.deepcopy(self.clipboard.param)
                    self.show_editmenu(store=False)

    def check_parameter_uniqueness(self, parameter_name):
        """
        Checks if a parameter inside of a textbox is unique, or if any other entity higher in the hierarchy
        has the same value for the parameter
        :param parameter_name: The parameter which should be checked.
        :return: Bool value if parameter is unique or not.
        """
        if isinstance(self.selected_entity, Neuron):
            neuron_param = self.selected_entity.param.list[parameter_name]
            base_param = ParameterHandler.get_base_neuron(self.network_manager.neuron_types, self.selected_entity.param).list[parameter_name]
            if neuron_param == base_param:
                return False
        elif isinstance(self.selected_entity, Connection):
            connection_param = self.selected_entity.param.list[parameter_name]
            connection_network = self.selected_entity.network_id
            prev_neuron = self.selected_entity.prev_neuron
            if "neuron" in self.selected_entity.prev_neuron_function:
                prev_neuron_entity = self.network_manager.networks[connection_network].neurons[prev_neuron-1]
            else:
                prev_neuron_entity = self.network_manager.networks[connection_network].nodes[prev_neuron - 1]
            neuron_param = prev_neuron_entity.param.list[parameter_name]
            base_param = ParameterHandler.get_base_neuron(self.network_manager.neuron_types, prev_neuron_entity.param).list[parameter_name]
            if neuron_param is None and connection_param == base_param:
                return False
            elif connection_param == neuron_param:
                return False
        elif self.selected_entity is None:
            return True

        return True

    def check_and_save_parameters(self, entity, container, parameter_name):
        """
        Checks if parameter is valid and saves a parameter locally in the entity class member parameters.
        :param entity:          The entity which is manipulated right now (eqivalent to self.selected_entity).
        :param container:       The tkinter widget which contains the user-edited parameter value.
        :param parameter_name:  The name of the parameter which is currently addressed (string).
        :return:                None
        """
        if not ParameterHandler.is_menu(parameter_name):
            temp_param = container[0].get()
            try:
                if ParameterHandler.is_menu(parameter_name):
                    entity.param.list[parameter_name] = temp_param
                elif parameter_name == "ip_address" or parameter_name == "port" or parameter_name == "channel":
                    entity.param.list[parameter_name] = temp_param
                else:
                    entity.param.list[parameter_name] = float(temp_param)
            except ValueError:
                entity.param.list[parameter_name] = None

            is_unique = self.check_parameter_uniqueness(parameter_name)
            if not is_unique:
                entity.param.list[parameter_name] = None

    def store_parameters(self, entity, parameter_names):
        """
        Stores all parameter, which are currently opened in the GUI.
        :param entity:          The entity which is manipulated right now (eqivalent to self.selected_entity).
        :param parameter_names: The list of all parameters the currently selected entity can have.
        :return:                None
        """
        if self.tool == TOOL_SELECT:
            for i, name in enumerate(parameter_names):
                for param_container in self.parameter_textbox:
                    if param_container[1] == name and param_container[1] != "neuron_type":
                        self.check_and_save_parameters(entity, param_container, name)

            if isinstance(entity, Neuron):
                for param_container in self.parameter_textbox:
                    if param_container[1] == "neuron_type":
                        self.check_and_save_parameters(entity, param_container, "neuron_type")

    def store_menu_parameters(self, option, name):
        """
        Stores a parameter, if it is chosen from a drop-down list.
        :param option:  The option from the user chosen.
        :param name:    The name of the addressed parameter.
        :return:        None
        """
        self.selected_entity.param.list[name] = option
        if not self.check_parameter_uniqueness(name):
            self.selected_entity.param.list[name] = None
        self.show_editmenu(store=False)

    def print_entry_parameter(self, entity, entity_param, param_index, name):
        """
        Prints the parameter with a textbox into its textbox given corresponding index value.
        :param entity:          The entity the parameter is assigned to.
        :param entity_param:    The current parameter of the currently selected entity.
        :param param_index:     The index of the parameter
        :param name:            The name of the parameter. Must be given for other functions and to check for
                                rule exceptions in parameter GUI handling.
        :return:                None
        """
        if entity_param.list[name] is None:
            if isinstance(entity, Connection):
                network_id = entity.network_id
                neuron_id = entity.prev_neuron-1
                if "neuron" in entity.prev_neuron_function:
                    self.print_entry_parameter(self.network_manager.networks[network_id].neurons[neuron_id],
                                               self.network_manager.networks[network_id].neurons[neuron_id].param,
                                               param_index, name)
                else:
                    self.print_entry_parameter(self.network_manager.networks[network_id].nodes[neuron_id],
                                               self.network_manager.networks[network_id].nodes[neuron_id].param,
                                               param_index, name)
                self.parameter_textbox[param_index][0].config(fg=design.grey_4[design.theme])
            elif isinstance(entity, Neuron):
                neuron_type = ParameterHandler.get_base_neuron(self.network_manager.neuron_types, entity_param)
                self.print_entry_parameter(None, neuron_type, param_index, name)
                self.parameter_textbox[param_index][0].config(fg=design.grey_4[design.theme])
            else:
                self.parameter_textbox[param_index][0].insert(tk.END, "Missing...")
                self.parameter_textbox[param_index][0].config(fg=design.dark_red[design.theme])
        else:
            try:
                param_str = ParameterHandler.deny_scientific_notation(entity_param.list[name])
                self.parameter_textbox[param_index][0].insert(tk.END, param_str)
            except TypeError:
                self.parameter_textbox[param_index][0].insert(tk.END, "Missing...")
                self.parameter_textbox[param_index][0].config(fg=design.dark_red[design.theme])

    def print_menu_parameter(self, entity, entity_param, name):
        """
        Prints a parameter with a drop-down menu.
        :param entity:          The selected entity.
        :param entity_param:    The current parameter value of the current entity.
        :param name:            The name of the parameter.
        :return:                None
        """
        parameter = None
        color = design.black[design.theme]

        if entity_param.list[name] is None:
            if isinstance(entity, Connection):
                network_id = entity.network_id
                neuron_id = entity.prev_neuron - 1
                if "neuron" in entity.prev_neuron_function:
                    temp_neuron = self.network_manager.networks[network_id].neurons[neuron_id]
                else:
                    temp_neuron = self.network_manager.networks[network_id].nodes[neuron_id]
                parameter, color = self.print_menu_parameter(temp_neuron, temp_neuron.param, name)
                color = design.grey_4[design.theme]
            elif isinstance(entity, Neuron):
                neuron_type = ParameterHandler.get_base_neuron(self.network_manager.neuron_types, entity.param)
                parameter, color = self.print_menu_parameter(None, neuron_type, name)
                color = design.grey_4[design.theme]
        else:
            parameter = entity_param.list[name]
            color = design.black[design.theme]

        return parameter, color

    def show_entity_parameters(self):
        """
        The function which renders all parameters to the left frame of the program.
        :return:    None
        """
        show_parameters = True
        if isinstance(self.selected_entity, Connection):
            if "neuron" in self.selected_entity.prev_neuron_function and \
                    "interface_output" not in self.selected_entity.next_neuron_function:
                prev_entity_name = "neuron"
                prev_entity_id = self.selected_entity.prev_neuron
            else:
                prev_entity_name = "node"
                prev_entity_id = self.selected_entity.prev_neuron
                show_parameters = False

            if "connection" in self.selected_entity.next_neuron_function:
                next_entity_name = "connection"
                next_entity_id = self.selected_entity.next_connection
            elif "neuron" in self.selected_entity.next_neuron_function:
                next_entity_name = "neuron"
                next_entity_id = self.selected_entity.next_neuron
            else:
                next_entity_name = "node"
                next_entity_id = self.selected_entity.next_neuron

            connection_text = f"connects {prev_entity_name} {str(prev_entity_id)} to {next_entity_name} {str(next_entity_id)}"
            self.general_info.config(text=f"Connection <{self.selected_connection}> Selected")
            self.connection_info = tk.Label(master=self.parameter_frame[2], text=connection_text,
                                            bg=design.grey_4[design.theme], fg=design.light_blue[design.theme])
            self.param_list = ParameterHandler.get_paramter_list(self.edit_selection, "Connection")
            self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[3], self.edit_selection,
                                                *ParameterHandler.param_drop_options_connection,
                                                command=self.show_editmenu)

        elif isinstance(self.selected_entity, Neuron):
            if "neuron" in self.selected_function:
                self.general_info.config(text=f"Neuron <{self.selected_neuron}> Selected")
            else:
                self.general_info.config(text=f"Node <{self.selected_neuron}> Selected")
            self.param_list = ParameterHandler.get_paramter_list(self.edit_selection, "Neuron",
                                                                 self.selected_entity.function)
            if "neuron" in self.selected_entity.function:
                self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[3], self.edit_selection,
                                                    *ParameterHandler.param_drop_options_neuron,
                                                    command=self.show_editmenu)
            elif "interface" in self.selected_entity.function:
                self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[3], self.edit_selection,
                                                    *ParameterHandler.param_drop_options_interface,
                                                    command=self.show_editmenu)
            elif "subnet" in self.selected_entity.function:
                self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[3], self.edit_selection,
                                                    *ParameterHandler.param_drop_options_subnet,
                                                    command=self.show_editmenu)

        elif isinstance(self.selected_entity, Subnetwork):
            self.general_info.config(text=f"Subnetwork <{self.selected_entity.id}> Selected")
            show_parameters = False

        elif isinstance(self.selected_entity, Network):
            self.general_info.config(text=f"Network <{self.network_manager.filename[self.network_manager.curr_network]}> Selected")
            self.param_list = ParameterHandler.get_paramter_list(self.edit_selection, "Network")
            self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[3], self.edit_selection,
                                                *ParameterHandler.param_drop_options_network,
                                                command=self.show_editmenu)

        self.general_info.pack(side=tk.LEFT)

        if show_parameters:
            if self.connection_info is not None:
                self.connection_info.pack(side=tk.LEFT)

            self.edit_drop_menu.config(bg=design.grey_4[design.theme], width=self.editframe_width, fg=design.grey_c[design.theme],
                                       borderwidth=0, highlightthickness=3, highlightbackground=design.grey_2[design.theme],
                                       activebackground=design.grey_7[design.theme])
            self.edit_drop_menu["menu"].config(bg=design.grey_4[design.theme], fg=design.grey_c[design.theme], borderwidth=1,
                                               activebackground=design.grey_7[design.theme], relief=tk.RIDGE)

            self.edit_drop_menu.pack(side=tk.LEFT)

            if self.selected_neuron < 0 and self.selected_connection < 0:
                try:
                    self.param_list.remove("neuron_type")
                except ValueError:
                    pass

            for i, name in enumerate(self.param_list):
                menu = None

                if ParameterHandler.is_menu(name):
                    var = tk.StringVar()
                    str_value, color = self.print_menu_parameter(self.selected_entity, self.selected_entity.param, name)
                    var.set(str_value)
                    if isinstance(self.selected_entity, Neuron):
                        function = self.selected_entity.function
                    else:
                        function = None
                    menu = ParameterHandler.get_option_menu_list(name, self.network_manager, function,
                                                                 entity=self.selected_entity)
                    if menu:
                        temp_field = tk.OptionMenu(self.parameter_frame[i+5], var, *menu,
                                                   command=lambda option, n=name: self.store_menu_parameters(option=option,
                                                                                                             name=n))
                        temp_field.config(bg=design.grey_7[design.theme], width=15,
                                          fg=color,
                                          borderwidth=0, highlightthickness=3,
                                          highlightbackground=design.grey_2[design.theme],
                                          activebackground=design.grey_7[design.theme])
                        self.parameter_textbox.append([temp_field, name])

                else:
                    temp_field = tk.Entry(master=self.parameter_frame[i+5], width=20,
                                          bg=design.grey_7[design.theme], borderwidth=0,
                                          highlightthickness=2, highlightbackground=design.grey_2[design.theme])
                    self.parameter_textbox.append([temp_field, name])
                    self.print_entry_parameter(self.selected_entity, self.selected_entity.param, i, name)

                if menu or not ParameterHandler.is_menu(name):
                    self.parameter_textbox[i][0].pack(side=tk.LEFT, padx=20)

                    self.parameter_info.append(tk.Label(master=self.parameter_frame[i+5], text=name,
                                                        bg=design.grey_4[design.theme], fg=design.grey_c[design.theme]))
                    self.parameter_info[i].pack(side=tk.LEFT)

    def get_network_list(self):
        """
        Returns the list of all networks in the project.
        :return:    A list of Strings of all networks in the project.
        """
        return os.listdir(self.network_manager.project_path + os.sep + "networks")

    def show_import_menu(self):
        """
        Prints the menu to the left, if the currently selected tool is IMPORT.
        :return:    None
        """
        network_list = self.get_network_list()
        network_list.remove(self.network_manager.filename[self.network_manager.curr_network])
        if len(network_list) > 0:
            self.network_option.set(network_list[0])

            self.parameter_textbox.append([tk.OptionMenu(self.parameter_frame[1], self.network_option, *network_list)])
            self.parameter_textbox[0][0].config(bg=design.grey_7[design.theme], width=15,
                                                fg=design.black[design.theme],
                                                borderwidth=0, highlightthickness=3,
                                                highlightbackground=design.grey_2[design.theme],
                                                activebackground=design.grey_7[design.theme])
            self.parameter_textbox[0][0].pack(side=tk.LEFT, padx=20)
            self.parameter_info.append(tk.Label(master=self.parameter_frame[1], text="Imported Network",
                                                bg=design.grey_4[design.theme], fg=design.grey_c[design.theme]))
            self.parameter_info[0].pack(side=tk.LEFT)

    def show_exchange_menu(self):
        """
        Prints the menu to the left, if the currently selected tool is EXCHANGE.
        :return:    None
        """
        self.exchange_option.set(self.option_list[0])

        self.parameter_textbox.append([tk.OptionMenu(self.parameter_frame[1], self.exchange_option, *self.option_list)])
        self.parameter_textbox[0][0].config(bg=design.grey_7[design.theme], width=15,
                                            fg=design.black[design.theme],
                                            borderwidth=0, highlightthickness=3,
                                            highlightbackground=design.grey_2[design.theme],
                                            activebackground=design.grey_7[design.theme])
        self.parameter_textbox[0][0].pack(side=tk.LEFT, padx=20)
        self.parameter_info.append(tk.Label(master=self.parameter_frame[1], text="Exchange Node Type",
                                            bg=design.grey_4[design.theme], fg=design.grey_c[design.theme]))
        self.parameter_info[0].pack(side=tk.LEFT)

    def show_editmenu(self, event=None, store=True):
        """
        Initializes and prepares parameter frame for rendering new parameters.
        :param event:   tkinter parameter for use as callback function
        :param store:   Determines whether parameters should be stored before rendering new parameters.
        :return:        None
        """
        self.project_name_label.config(text=self.network_manager.project_name)

        if store:
            self.store_parameters(entity=self.selected_entity, parameter_names=self.param_list)

        self.edit_drop_menu.destroy()
        self.id_info.pack_forget()
        for i in range(0, len(self.parameter_info)):
            self.parameter_info[i].destroy()
        self.parameter_info.clear()
        for i in range(0, len(self.parameter_textbox)):
            self.parameter_textbox[i][0].destroy()
        self.parameter_textbox.clear()
        self.general_info.forget()
        if self.connection_info is not None:
            self.connection_info.forget()
        self.connection_info = None

        if self.tool == TOOL_SELECT:
            self.show_entity_parameters()
        elif self.tool == TOOL_IMPORT:
            self.show_import_menu()
        elif self.tool == TOOL_EXCHANGE:
            self.show_exchange_menu()

    def switch_tool_neurons(self):
        """
        Function to switch tool stance to neuron editing.
        :return:    None
        """
        self.tool = TOOL_NEURONS
        self.selected_entity = None
        self.neuron_button.configure(background=design.dark_blue[design.theme])
        self.connection_button.configure(background=design.grey_3[design.theme])
        self.select_button.configure(background=design.grey_3[design.theme])
        self.import_button.configure(background=design.grey_3[design.theme])
        self.exchange_button.configure(background=design.grey_3[design.theme])
        self.discard_connection()
        self.deselect_all()
        self.show_editmenu(store=False)
        self.render_scene()

    def switch_tool_connections(self):
        """
        Function to switch tool stance to connection editing.
        :return:    None
        """
        self.tool = TOOL_CONNECTIONS
        self.selected_entity = None
        self.neuron_button.configure(background=design.grey_3[design.theme])
        self.connection_button.configure(background=design.dark_blue[design.theme])
        self.select_button.configure(background=design.grey_3[design.theme])
        self.import_button.configure(background=design.grey_3[design.theme])
        self.exchange_button.configure(background=design.grey_3[design.theme])
        self.deselect_all()
        self.show_editmenu(store=False)
        self.render_scene()

    def switch_tool_select(self):
        """
        Function to switch tool stance to selecting and parameter editing.
        :return:    None
        """
        self.tool = TOOL_SELECT
        self.neuron_button.configure(background=design.grey_3[design.theme])
        self.connection_button.configure(background=design.grey_3[design.theme])
        self.select_button.configure(background=design.dark_blue[design.theme])
        self.import_button.configure(background=design.grey_3[design.theme])
        self.exchange_button.configure(background=design.grey_3[design.theme])
        self.discard_connection()
        self.deselect_all()
        self.show_editmenu(store=False)
        self.render_scene()

    def switch_tool_import(self):
        """
        Function to switch tool stance to importing other networks.
        :return:    None
        """
        self.tool = TOOL_IMPORT
        self.neuron_button.configure(background=design.grey_3[design.theme])
        self.connection_button.configure(background=design.grey_3[design.theme])
        self.select_button.configure(background=design.grey_3[design.theme])
        self.import_button.configure(background=design.dark_blue[design.theme])
        self.exchange_button.configure(background=design.grey_3[design.theme])
        self.discard_connection()
        self.deselect_all()
        self.show_editmenu(store=False)
        self.render_scene()

    def switch_tool_exchange(self):
        """
        Function to switch tool stance to importing other networks.
        :return:    None
        """
        self.tool = TOOL_EXCHANGE
        self.neuron_button.configure(background=design.grey_3[design.theme])
        self.connection_button.configure(background=design.grey_3[design.theme])
        self.select_button.configure(background=design.grey_3[design.theme])
        self.import_button.configure(background=design.grey_3[design.theme])
        self.exchange_button.configure(background=design.dark_blue[design.theme])
        self.discard_connection()
        self.deselect_all()
        self.show_editmenu(store=False)
        self.render_scene()

    def reset_camera(self, event=None):
        """
        Resets camera view and zoom.
        :param event: Parameter for use as callback function.
        :return:    None
        """
        self.network_manager.camera_x[self.network_manager.curr_network] = self.editorcanvas.winfo_width() / 2
        self.network_manager.camera_y[self.network_manager.curr_network] = self.editorcanvas.winfo_height() / 2
        self.network_manager.zoom_factor[self.network_manager.curr_network] = 1.0
        self.render_scene()

    def render_grid(self):
        """
        Renders the grid onto the edit canvas, if grid snap is activated.
        :return:    None
        """
        temp_x = self.network_manager.camera_x[self.network_manager.curr_network] % self.grid_size
        temp_y = self.network_manager.camera_y[self.network_manager.curr_network] % self.grid_size

        if self.network_manager.zoom_factor[self.network_manager.curr_network] < 1:
            corrected_y = VectorUtils.correct_zoom(self.editorcanvas.winfo_height(), self.network_manager.zoom_factor[self.network_manager.curr_network])
            corrected_x = VectorUtils.correct_zoom(self.editorcanvas.winfo_width(), self.network_manager.zoom_factor[self.network_manager.curr_network])
        else:
            corrected_y = self.editorcanvas.winfo_height()*self.network_manager.zoom_factor[self.network_manager.curr_network]
            corrected_x = self.editorcanvas.winfo_width()*self.network_manager.zoom_factor[self.network_manager.curr_network]

        if self.network_manager.camera_x[self.network_manager.curr_network] > 0:
            temp_camera_x = self.network_manager.camera_x[self.network_manager.curr_network]
        else:
            temp_camera_x = -self.network_manager.camera_x[self.network_manager.curr_network]
        if self.network_manager.camera_y[self.network_manager.curr_network] > 0:
            temp_camera_y = self.network_manager.camera_y[self.network_manager.curr_network]
        else:
            temp_camera_y = -self.network_manager.camera_y[self.network_manager.curr_network]

        while temp_x < VectorUtils.correct_zoom(self.editorcanvas.winfo_width()+temp_camera_x, self.network_manager.zoom_factor[self.network_manager.curr_network]):
            self.editorcanvas.create_line(temp_x * self.network_manager.zoom_factor[self.network_manager.curr_network], 0,
                                          temp_x * self.network_manager.zoom_factor[self.network_manager.curr_network], corrected_y,
                                          fill=design.grey_4[design.theme], width=2)
            temp_x = temp_x + self.grid_size

        while temp_y < VectorUtils.correct_zoom(self.editorcanvas.winfo_height()+temp_camera_y, self.network_manager.zoom_factor[self.network_manager.curr_network]):
            self.editorcanvas.create_line(0, temp_y * self.network_manager.zoom_factor[self.network_manager.curr_network],
                                          corrected_x, temp_y * self.network_manager.zoom_factor[self.network_manager.curr_network],
                                          fill=design.grey_4[design.theme], width=2)
            temp_y = temp_y + self.grid_size

    def get_valid_parameter_value(self, entity, param):
        """
        Determines a valid parameter for a selected entity in a hierarchical way. A connection looks in its source
        neuron and a neuron looks in its neuron type.
        :param entity:  The currently selected entity.
        :param param:   The name of the addressed parameter.
        :return:        The valid parameter
        """
        return_value = None

        if isinstance(entity, Connection):
            if entity.param.list[param] is None:
                if "neuron" in entity.prev_neuron_function:
                    prev_neuron = self.network_manager.networks[self.network_manager.curr_network].neurons[entity.prev_neuron - 1]
                else:
                    prev_neuron = self.network_manager.networks[self.network_manager.curr_network].nodes[entity.prev_neuron - 1]
                return_value = self.get_valid_parameter_value(prev_neuron, param)
            else:
                return_value = entity.param.list[param]
        elif isinstance(entity, Neuron):
            if entity.param.list[param] is None:
                base_neuron = ParameterHandler.get_base_neuron(self.network_manager.neuron_types, entity.param)
                return_value = base_neuron.list[param]
            else:
                return_value = entity.param.list[param]

        return return_value

    def render_connections(self):
        """
        Renders all connections of the currently active network.
        :return:    None
        """
        for connection_i, connection in enumerate(self.network_manager.networks[self.network_manager.curr_network].connections):
            distance = 5
            direction_marker_length = 8

            if "neuron" in connection.prev_neuron_function:
                activation_type = self.get_valid_parameter_value(connection, "activation_type")
                max_weight = self.get_valid_parameter_value(connection, "max_weight")
                base_weight = self.get_valid_parameter_value(connection, "base_weight")
            else:
                activation_type = None
                max_weight = 5
                base_weight = 1

            width_ratio = base_weight / max_weight
            con_width = design.connection_width * width_ratio
            if con_width < 1:
                con_width = 1
            elif con_width > design.connection_width:
                con_width = design.connection_width

            if connection.id == self.selected_connection:
                color = design.white[design.theme]
            elif connection.prev_subnet != -1:
                color = design.grey_c[design.theme]
            elif connection.next_neuron_function == "interface_output":
                color = design.grey_c[design.theme]
            elif activation_type == "Excitatory":
                color = design.light_blue[design.theme]
            elif activation_type == "Inhibitory":
                color = design.light_red[design.theme]
            elif activation_type == "Nondirectional":
                color = design.light_green[design.theme]
            else:
                color = design.grey_c[design.theme]

            if not connection.next_neuron is None:
                distance = self.neuron_size + distance
            if not connection.next_connection is None:
                distance = 5 + distance

            scaled_vert = VectorUtils.calc_vector(connection.vertices[len(connection.vertices)-1],
                                                  connection.vertices[len(connection.vertices)-2])
            scaled_vert = connection.vertices[len(connection.vertices) - 1] + VectorUtils.unit_vector(scaled_vert) *\
                          distance

            temp_verts = connection.vertices[:]
            if not np.isnan(scaled_vert[0]) and not self.do_connection or\
                    connection_i < len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1:
                temp_verts[len(temp_verts)-1] = scaled_vert
            try:
                normal_vector = VectorUtils.uninormal_vector(VectorUtils.calc_vector(temp_verts[len(temp_verts)-1],
                                                                                     temp_verts[len(temp_verts)-2]))
                direction_marker_a = temp_verts[len(temp_verts)-1] + normal_vector * direction_marker_length
                direction_marker_b = temp_verts[len(temp_verts)-1] - normal_vector * direction_marker_length
                self.editorcanvas.create_line(VectorUtils.project_coordinate(direction_marker_a[0],
                                                                             self.network_manager.camera_x[self.network_manager.curr_network],
                                                                             self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(direction_marker_a[1],
                                                                             self.network_manager.camera_y[self.network_manager.curr_network],
                                                                             self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(direction_marker_b[0],
                                                                             self.network_manager.camera_x[self.network_manager.curr_network],
                                                                             self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(direction_marker_b[1],
                                                                             self.network_manager.camera_y[self.network_manager.curr_network],
                                                                             self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              fill=color, width=3)
            except IndexError:
                pass

            for vert in range(0, len(temp_verts)-1):
                self.editorcanvas.create_line(VectorUtils.project_coordinate(temp_verts[vert][0],
                                                                             self.network_manager.camera_x[self.network_manager.curr_network],
                                                                             self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(temp_verts[vert][1],
                                                                             self.network_manager.camera_y[self.network_manager.curr_network],
                                                                             self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(temp_verts[vert + 1][0],
                                                                             self.network_manager.camera_x[self.network_manager.curr_network],
                                                                             self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(temp_verts[vert + 1][1],
                                                                             self.network_manager.camera_y[self.network_manager.curr_network],
                                                                             self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              fill=color, width=con_width)

    def render_neurons(self):
        """
        Renders all neurons of the currently active network.
        :return:    None
        """
        temp_camera_x = self.network_manager.camera_x[self.network_manager.curr_network]
        temp_camera_y = self.network_manager.camera_y[self.network_manager.curr_network]
        temp_zoom = self.network_manager.zoom_factor[self.network_manager.curr_network]

        for neuron in chain(*self.network_manager.networks[self.network_manager.curr_network].all_nodes):
            if self.selected_neuron == neuron.id and self.selected_function == neuron.function:
                temp_outline = design.light_blue[design.theme]
                temp_width = 5 * self.network_manager.zoom_factor[self.network_manager.curr_network]
            else:
                temp_outline = "#000000"
                temp_width = 1

            if "neuron" in neuron.function:
                temp_color = design.white[design.theme]
                temp_text = neuron.id

            elif "interface" in neuron.function:
                temp_text = None
                if "input" in neuron.function:
                    temp_color = design.dark_blue[design.theme]
                    temp_text = "I"
                elif "output" in neuron.function:
                    temp_color = design.dark_red[design.theme]
                    temp_text = "O"

            elif "subnet" in neuron.function:
                temp_text = None
                if "input" in neuron.function:
                    temp_color = design.dark_blue[design.theme]
                    try:
                        temp_text = "I " + str(int(neuron.param.list["node_id"]))
                    except:
                        temp_text = "I"
                elif "output" in neuron.function:
                    temp_color = design.dark_red[design.theme]
                    try:
                        temp_text = "O " + str(int(neuron.param.list["node_id"]))
                    except:
                        temp_text = "O"

            if "neuron" in neuron.function or "subnet" in neuron.function:
                self.editorcanvas.create_circle(VectorUtils.project_coordinate(neuron.posx, temp_camera_x, temp_zoom),
                                                VectorUtils.project_coordinate(neuron.posy, temp_camera_y, temp_zoom),
                                                self.neuron_size * temp_zoom,
                                                fill=temp_color,
                                                outline=temp_outline,
                                                width=temp_width)
                temp_y = neuron.posy
            elif "interface" in neuron.function:
                self.editorcanvas.create_triangle(VectorUtils.project_coordinate(neuron.posx, temp_camera_x, temp_zoom),
                                                  VectorUtils.project_coordinate(neuron.posy, temp_camera_y, temp_zoom),
                                                  self.neuron_size * temp_zoom,
                                                  fill=temp_color,
                                                  outline=temp_outline,
                                                  width=temp_width)
                temp_y = neuron.posy + 10

            if neuron.param.list["influences_transmitter"] is not None:
                if neuron.param.list["influences_transmitter"] == "Yes":
                    self.editorcanvas.create_circle(VectorUtils.project_coordinate(neuron.posx, temp_camera_x, temp_zoom),
                                                    VectorUtils.project_coordinate(neuron.posy, temp_camera_y, temp_zoom),
                                                    (self.neuron_size-5) * temp_zoom,
                                                    fill=temp_color,
                                                    outline=temp_outline,
                                                    width=3)

            if neuron.param.list["random_chance"] is not None:
                if neuron.param.list["random_chance"] > 0:
                    self.editorcanvas.create_text(VectorUtils.project_coordinate(neuron.posx, temp_camera_x, temp_zoom),
                                                  VectorUtils.project_coordinate(neuron.posy+40, temp_camera_y, temp_zoom),
                                                  text=str(neuron.param.list["random_chance"]) + "%",
                                                  fill=design.white[design.theme])

            self.editorcanvas.create_text(VectorUtils.project_coordinate(neuron.posx, temp_camera_x, temp_zoom),
                                          VectorUtils.project_coordinate(neuron.posy, temp_camera_y, temp_zoom),
                                          text=temp_text, fill=design.grey_1[design.theme])

    def render_subnet_nodes(self, subnet):
        """
        Renders all subnet nodes of the current network.
        :return:    None
        """
        temp_camera_x = self.network_manager.camera_x[self.network_manager.curr_network]
        temp_camera_y = self.network_manager.camera_y[self.network_manager.curr_network]
        temp_zoom = self.network_manager.zoom_factor[self.network_manager.curr_network]

        node_size = subnet.node_size * self.network_manager.zoom_factor[self.network_manager.curr_network]

        for node in subnet.input_node_list:
            corr_x = VectorUtils.project_coordinate(node.posx, temp_camera_x, temp_zoom)
            corr_y = VectorUtils.project_coordinate(node.posy, temp_camera_y, temp_zoom)

            self.editorcanvas.create_circle(corr_x, corr_y, node_size, fill=design.white[design.theme])
            self.editorcanvas.create_text(corr_x, corr_y, text=node.id)

        for node in subnet.output_node_list:
            corr_x = VectorUtils.project_coordinate(node.posx, temp_camera_x, temp_zoom)
            corr_y = VectorUtils.project_coordinate(node.posy, temp_camera_y, temp_zoom)

            self.editorcanvas.create_circle(corr_x, corr_y, node_size, fill=design.dark_blue[design.theme])
            self.editorcanvas.create_text(corr_x, corr_y, text=node.id)

    def render_subnets(self):
        """
        Renders all subnetworks of the current network.
        :return:    None
        """
        temp_camera_x = self.network_manager.camera_x[self.network_manager.curr_network]
        temp_camera_y = self.network_manager.camera_y[self.network_manager.curr_network]
        temp_zoom = self.network_manager.zoom_factor[self.network_manager.curr_network]

        for subnet in self.network_manager.networks[self.network_manager.curr_network].subnets:
            if self.selected_entity == subnet:
                temp_outline = design.light_blue[design.theme]
                temp_width = 5 * self.network_manager.zoom_factor[self.network_manager.curr_network]
            else:
                temp_outline = "#000000"
                temp_width = 1
            x0 = VectorUtils.project_coordinate(subnet.posx-subnet.size_x,
                                                temp_camera_x, temp_zoom)
            y0 = VectorUtils.project_coordinate(subnet.posy-subnet.size_y, temp_camera_y, temp_zoom)
            x1 = VectorUtils.project_coordinate(subnet.posx+subnet.size_x, temp_camera_x, temp_zoom)
            y1 = VectorUtils.project_coordinate(subnet.posy+subnet.size_y, temp_camera_y, temp_zoom)

            self.editorcanvas.create_rectangle(x0, y0, x1, y1,
                                               fill=design.grey_7[design.theme],
                                               outline=temp_outline,
                                               width=temp_width)
            self.render_subnet_nodes(subnet)

            label_x = VectorUtils.project_coordinate(subnet.posx, temp_camera_x, temp_zoom)
            label_y = VectorUtils.project_coordinate(subnet.posy - subnet.size_y + 30, temp_camera_y, temp_zoom)
            self.editorcanvas.create_text(label_x, label_y, text=f"{subnet.network_name}", fill=design.grey_1[design.theme])

    def render_ui_description(self):
        """
        Renders text elements onto the canvas.
        :return:    None
        """
        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 15, anchor="w",
                                      text="Mode:", fill=design.grey_c[design.theme])
        if self.tool == TOOL_SELECT:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="SELECTING", fill=design.light_blue[design.theme])
        elif self.tool == TOOL_NEURONS:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="NEURON EDITING", fill=design.light_blue[design.theme])
        elif self.tool == TOOL_CONNECTIONS:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="CONNECTION EDITING", fill=design.light_blue[design.theme])
        elif self.tool == TOOL_IMPORT:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="IMPORTING NETWORK", fill=design.light_blue[design.theme])
        elif self.tool == TOOL_EXCHANGE:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="EXCHANGE NODE EDITING", fill=design.light_blue[design.theme])

        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 90, anchor="w",
                                      text=f"Camera X: {int(self.network_manager.camera_x[self.network_manager.curr_network])}", fill=design.grey_c[design.theme])
        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 60, anchor="w",
                                      text=f"Camera Y: {int(self.network_manager.camera_y[self.network_manager.curr_network])}", fill=design.grey_c[design.theme])

        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 175, anchor="w",
                                      text=f"Cursor X: {int(self.cursor_x)}", fill=design.grey_c[design.theme])
        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 145, anchor="w",
                                      text=f"Cursor Y: {int(self.cursor_y)}", fill=design.grey_c[design.theme])

        self.editorcanvas.create_text(self.editorcanvas.winfo_width() - 5, self.editorcanvas.winfo_height() - 15,
                                      anchor="e",
                                      text=f"Zoom: {round(self.network_manager.zoom_factor[self.network_manager.curr_network] * 100, 0)}%", fill=design.grey_c[design.theme])

        if self.grid_snap:
            self.editorcanvas.create_text(self.editorcanvas.winfo_width() - 5, self.editorcanvas.winfo_height() - 60,
                                          anchor="e", fill=design.light_blue[design.theme],
                                          text="Grid Snap Active")

    def render_scene(self):
        """
        Function responsible for calling all other rendering functions and rendering the whole scene in the
        edit canvas.
        :return:    None
        """
        if len(self.network_manager.networks) > 0:
            if self.editorcanvas is not None:
                self.editorcanvas.delete("all")

                if self.grid_snap:
                    self.render_grid()

                self.render_connections()
                self.render_subnets()
                self.render_neurons()

                self.editorcanvas.create_text(VectorUtils.project_coordinate(0, self.network_manager.camera_x[self.network_manager.curr_network],
                                                                             self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(0, self.network_manager.camera_y[self.network_manager.curr_network],
                                                                             self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              text="X", fill=design.light_blue[design.theme], font="arial 15")

                self.render_ui_description()

                if self.editframe.winfo_width() < 100:
                    self.editframe.config(width=100)

    def snap_cursor_to_grid(self):
        """
        Toggles grid snapping and visibility of grid.
        :return:    None
        """
        if self.tool != TOOL_SELECT or self.move_entity:
            if self.grid_snap:
                posx = self.cursor_x
                posy = self.cursor_y

                x_offset = posx % self.grid_size
                y_offset = posy % self.grid_size

                if x_offset < self.grid_size / 2:
                    self.cursor_x = posx - x_offset
                else:
                    self.cursor_x = posx + (self.grid_size - x_offset)
                if y_offset < self.grid_size / 2:
                    self.cursor_y = posy - y_offset
                else:
                    self.cursor_y = posy + (self.grid_size - y_offset)

    def get_free_cursor(self, event):
        """
        Returns free cursor (not snapped to the grid) to the cursor member variables, even if grid snapping is active.
        :param event:   Parameter for use as callback function.
        :return:        None
        """
        self.cursor_x = VectorUtils.correct_zoom(event.x, self.network_manager.zoom_factor[self.network_manager.curr_network]) - self.network_manager.camera_x[self.network_manager.curr_network]
        self.cursor_y = VectorUtils.correct_zoom(event.y, self.network_manager.zoom_factor[self.network_manager.curr_network]) - self.network_manager.camera_y[self.network_manager.curr_network]

    def get_cursor_position(self, event):
        """
        Returns free cursor (not snapped to the grid) to the cursor member variables, even if grid snapping is active.
        Afterwards it renders the scene and snaps cursor back to the grid.
        Useful if a very specific action should be independent from the grid.
        :param event:   Parameter for use as callback function.
        :return:        None
        """
        self.get_free_cursor(event)
        self.render_scene()
        self.snap_cursor_to_grid()

    def add_neuron(self, function="neuron"):
        """
        Adds a neuron to the network.
        :param function:    The function of the new neuron in its network. Can be neuron, input, output, ...
        :return:            None
        """
        neuron_x = self.cursor_x
        neuron_y = self.cursor_y
        self.network_manager.add_neuron(neuron_x, neuron_y, self.neuron_size, self.network_manager.curr_network, function)

    def add_subnet(self):
        """
        Adds a subnetwork to the network.
        :return:    None
        """
        subnet_x = self.cursor_x
        subnet_y = self.cursor_y
        self.network_manager.add_subnet(self.network_option.get(), subnet_x, subnet_y, self.network_manager.curr_network)

    def init_connection(self, neuron):
        """
        Initializes a new connection.
        :param neuron:  The neuron where the new connection starts.
        :return:    None
        """
        self.connecting_neuron = neuron
        self.do_connection = True

        self.network_manager.add_connection(self.connection_source_neuron, self.network_manager.curr_network)
        connection_position = len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1
        this_connection = self.network_manager.networks[self.network_manager.curr_network].connections[connection_position]
        this_connection.prev_subnet = neuron.subnet_id
        this_connection.vertices.append(np.array([self.cursor_x, self.cursor_y]))
        this_connection.prev_neuron_function = neuron.function


    def draw_connection(self):
        """
        Changes the last vertex of the connection to the position of the cursor if not yet connected with a target
        neuron.
        :return:    None
        """
        if self.do_connection:
            self.render_scene()
            connection_position = len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1
            vertex_position = len(self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices) - 1
            self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices[vertex_position] = [self.cursor_x,
                                                                                                           self.cursor_y]

    def discard_connection(self):
        """
        Discards a connection, if a cancel event happens.
        :return:    None
        """
        if self.do_connection:
            connection_position = len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1
            self.network_manager.delete_connection(connection_position, self.network_manager.curr_network)
            self.do_connection = False

    def deselect_neurons(self):
        """
        Deselects a currently selected neuron.
        :return:    None
        """
        self.selected_neuron = -1
        self.selected_function = ""

    def deselect_connections(self):
        """
        Deselects a currently selected connection.
        :return:    None
        """
        self.selected_connection = -1
        self.selected_function = ""
       
    def deselect_all(self):
        """
        Deselects everything which is currently selected.
        :return:    None
        """
        self.deselect_neurons()
        self.deselect_connections()
        self.selected_entity = self.network_manager.networks[self.network_manager.curr_network]

    def escape_event(self, event):
        """
        Handles the press of the escape button.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.store_parameters(entity=self.selected_entity, parameter_names=self.param_list)
        self.discard_connection()
        self.deselect_neurons()
        self.deselect_connections()
        self.render_scene()

    def delete_event(self, event):
        """
        Handles the deletion of a selected entity.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        if isinstance(self.selected_entity, Neuron):
            self.network_manager.delete_neuron(self.selected_neuron, self.selected_function,
                                               self.network_manager.curr_network)
            self.deselect_neurons()
        elif isinstance(self.selected_entity, Connection):
            self.network_manager.delete_connection(self.selected_connection,
                                                   self.network_manager.curr_network)
            self.deselect_connections()
        elif isinstance(self.selected_entity, Subnetwork):
            self.network_manager.delete_subnet(self.selected_entity.id,
                                               self.network_manager.curr_network)
        self.render_scene()

    def tab_event(self, event):
        """
        Handles the press of the tab button.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.escape_event(event)
        if self.tool == TOOL_SELECT:
            self.switch_tool_neurons()
        elif self.tool == TOOL_NEURONS:
            self.switch_tool_connections()
        elif self.tool == TOOL_CONNECTIONS:
            self.switch_tool_import()
        elif self.tool == TOOL_IMPORT:
            self.switch_tool_exchange()
        elif self.tool == TOOL_EXCHANGE:
            self.switch_tool_select()

    def toggle_grid_snap(self, event):
        """
        Toggles the grid snap function.
        :param event: tkinter parameter for callback function.
        :return:        None
        """
        if self.grid_snap:
            self.grid_snap = False
        else:
            self.grid_snap = True
        self.render_scene()

    def create_neuron_connection(self, neuron):
        """
        Initializes and connects a new neuron connection.
        :param neuron:  The left clicked neuron.
        :return:        None
        """
        if self.do_connection and ("output" in neuron.function or "neuron" in neuron.function):
            can_connect = True
            connection_list = self.network_manager.networks[self.network_manager.curr_network].connections
            connection_position = len(connection_list) - 1
            for check_con in connection_list:
                if check_con.prev_neuron == connection_list[connection_position].prev_neuron \
                        and check_con.next_neuron == neuron.id:
                    if check_con.prev_subnet == connection_list[connection_position].prev_subnet \
                            and check_con.next_subnet == neuron.subnet_id:
                        if check_con.prev_neuron_function == connection_list[connection_position].prev_neuron_function \
                                and check_con.next_neuron_function == neuron.function:
                            can_connect = False
                if connection_list[connection_position].prev_neuron_function == "subnet_input" and neuron.function == "subnet_output":
                    can_connect = False

            if can_connect:
                vertex_position = len(connection_list[connection_position].vertices) - 1
                connection_list[connection_position].next_neuron = neuron.id
                connection_list[connection_position].next_subnet = neuron.subnet_id
                connection_list[connection_position].next_neuron_function = neuron.function
                connection_list[connection_position].vertices[vertex_position] = [neuron.posx, neuron.posy]
            else:
                self.discard_connection()
            self.do_connection = False

        elif not self.do_connection and ("input" in neuron.function or "neuron" in neuron.function):
            self.init_connection(neuron)

        else:
            self.discard_connection()

    def create_synaptic_connection(self, connection):
        """
        Connects a synaptic connection.
        :param connection:  The left clicked connection.
        :return:            None
        """
        if self.do_connection:
            connection_list = self.network_manager.networks[self.network_manager.curr_network].connections
            if connection.id < len(connection_list) - 1:
                can_connect = True
                connection_position = len(connection_list) - 1
                for check_con in connection_list:
                    if check_con.prev_neuron == connection_list[connection_position].prev_neuron \
                            and check_con.next_connection == connection.id \
                            and check_con.prev_neuron_function == connection_list[connection_position].prev_neuron_function:
                        can_connect = False
                        break
                if "neuron" not in connection.prev_neuron_function:
                    can_connect = False

                if can_connect:
                    vertex_position = len(connection_list[connection_position].vertices) - 1
                    connection_list[connection_position].next_connection = connection.id
                    connection_list[connection_position].next_subnet = -1
                    connection_list[connection_position].next_neuron_function = "connection"
                    connection_list[connection_position].vertices[vertex_position] = [self.cursor_x, self.cursor_y]
                else:
                    self.discard_connection()
                self.do_connection = False

    def move_entity_event(self, event):
        """
        Handles the event when an entity is moved.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        if self.move_entity and self.tool == TOOL_SELECT and self.selected_entity is not None:
            self.get_cursor_position(event)

            prev_posx = self.selected_entity.posx
            prev_posy = self.selected_entity.posy

            self.selected_entity.posx = self.cursor_x
            self.selected_entity.posy = self.cursor_y

            if isinstance(self.selected_entity, Subnetwork):
                self.selected_entity.set_node_position(prev_posx, prev_posy, self.cursor_x, self.cursor_y)

            for connection in self.network_manager.networks[self.network_manager.curr_network].connections:
                if isinstance(self.selected_entity, Neuron):
                    if connection.next_neuron == self.selected_entity.id and \
                            connection.next_neuron_function == self.selected_entity.function:
                        connection.vertices[len(connection.vertices)-1][0] = self.cursor_x
                        connection.vertices[len(connection.vertices)-1][1] = self.cursor_y
                    elif connection.prev_neuron == self.selected_entity.id and \
                            connection.prev_neuron_function == self.selected_entity.function:
                        connection.vertices[0][0] = self.cursor_x
                        connection.vertices[0][1] = self.cursor_y
                elif isinstance(self.selected_entity, Subnetwork):
                    for node in chain(self.selected_entity.input_node_list, self.selected_entity.output_node_list):
                        if connection.next_neuron == node.id and connection.next_neuron_function == node.function and \
                                connection.next_subnet == self.selected_entity.id:
                            connection.vertices[len(connection.vertices) - 1][0] = node.posx
                            connection.vertices[len(connection.vertices) - 1][1] = node.posy
                        elif connection.prev_neuron == node.id and connection.prev_neuron_function == node.function and \
                                connection.prev_subnet == self.selected_entity.id:
                            connection.vertices[0][0] = node.posx
                            connection.vertices[0][1] = node.posy

    def release_left_click(self, event):
        """
        Drops a selected entity when moved around and left click if released.
        :return:        None
        """
        self.move_entity = False

    def left_click(self, event):
        """
        Handles the left click eventy.
        :param event: tkinter parameter for event callback.
        :return:        None
        """
        neuron_collision = False
        subnet_collision = False
        connection_collision = False
        for neuron in chain(*self.network_manager.networks[self.network_manager.curr_network].all_nodes):
            if VectorUtils.calc_cursor_collision(self.cursor_x, self.cursor_y, neuron, self.network_manager.zoom_factor[self.network_manager.curr_network]):
                if self.tool == TOOL_CONNECTIONS:
                    if not self.do_connection:
                        self.connection_source_neuron = neuron
                    self.create_neuron_connection(neuron)
                    if not self.do_connection:
                        self.connection_source_neuron = None
                elif self.tool == TOOL_SELECT:
                    self.edit_selection.set(None)
                    self.store_parameters(entity=self.selected_entity, parameter_names=self.param_list)
                    self.deselect_connections()
                    self.selected_neuron = neuron.id
                    self.selected_entity = neuron
                    self.selected_function = neuron.function
                    self.show_editmenu(store=False)
                    self.move_entity = True

                neuron_collision = True

        for subnet in self.network_manager.networks[self.network_manager.curr_network].subnets:
            if self.tool == TOOL_SELECT:
                if VectorUtils.calc_rect_collision_by_size([self.cursor_x, self.cursor_y],
                                                           [subnet.posx, subnet.posy],
                                                           subnet.size_x, subnet.size_y,
                                                           self.network_manager.zoom_factor[self.network_manager.curr_network]):
                    self.selected_entity = subnet
                    subnet_collision = True
                    self.move_entity = True
                    self.show_editmenu(store=False)

            if self.tool == TOOL_CONNECTIONS:
                for node in chain(subnet.output_node_list, subnet.input_node_list):
                    if VectorUtils.calc_cursor_collision(self.cursor_x, self.cursor_y, node,
                                                         self.network_manager.zoom_factor[self.network_manager.curr_network]):
                        if not self.do_connection:
                            self.connection_source_neuron = node
                        self.create_neuron_connection(node)
                        if not self.do_connection:
                            self.connection_source_neuron = node
                        else:
                            neuron_collision = True

        if not neuron_collision and not subnet_collision:
            for connection in self.network_manager.networks[self.network_manager.curr_network].connections:
                if VectorUtils.connection_cursor_collision(connection, self.cursor_x, self.cursor_y,
                                                           self.network_manager.camera_x[self.network_manager.curr_network],
                                                           self.network_manager.camera_y[self.network_manager.curr_network],
                                                           self.network_manager.zoom_factor[self.network_manager.curr_network]):
                    if self.tool == TOOL_CONNECTIONS:
                        self.create_synaptic_connection(connection)

            if not self.do_connection:
                if self.tool == TOOL_NEURONS:
                    self.add_neuron("neuron")
                elif self.tool == TOOL_IMPORT:
                    self.add_subnet()
                elif self.tool == TOOL_EXCHANGE:
                    if self.exchange_option.get() == self.option_list[0]:
                        self.add_neuron("interface_input")
                    elif self.exchange_option.get() == self.option_list[1]:
                        self.add_neuron("interface_output")
                    elif self.exchange_option.get() == self.option_list[2]:
                        self.add_neuron("subnet_input")
                    elif self.exchange_option.get() == self.option_list[3]:
                        self.add_neuron("subnet_output")
            else:
                connection_position = len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1
                self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices.append(
                    np.array([self.cursor_x, self.cursor_y]))

            if self.tool == TOOL_SELECT:
                self.store_parameters(entity=self.selected_entity, parameter_names=self.param_list)
                self.deselect_neurons()
                self.show_editmenu(store=False)
                for connection in self.network_manager.networks[self.network_manager.curr_network].connections:
                    if VectorUtils.connection_cursor_collision(connection, self.cursor_x, self.cursor_y,
                                                               self.network_manager.camera_x[self.network_manager.curr_network],
                                                               self.network_manager.camera_y[self.network_manager.curr_network],
                                                               self.network_manager.zoom_factor[self.network_manager.curr_network]):
                        self.selected_connection = connection.id
                        self.selected_entity = connection
                        connection_collision = True
                if not connection_collision:
                    self.deselect_connections()
                self.show_editmenu(store=False)

        if not neuron_collision and not subnet_collision and not connection_collision:
            self.deselect_all()

        self.render_scene()

    def motion_event(self, event):
        """
        Handles what happens when the cursor is moved.
        :param event:   tkinter parameter for event handling.
        :return:        None
        """
        self.get_cursor_position(event)
        self.draw_connection()

    def delete_neuron(self):
        """
        Deletes a specific neuron based on the position of the cursor.
        :return:        None
        """
        if self.tool == TOOL_NEURONS:
            for neuron in chain(*self.network_manager.networks[self.network_manager.curr_network].all_nodes):
                if neuron.function == "neuron":
                    if VectorUtils.calc_cursor_collision(self.cursor_x, self.cursor_y, neuron, self.network_manager.zoom_factor[self.network_manager.curr_network]):
                        self.network_manager.delete_neuron(neuron.id, neuron.function, self.network_manager.curr_network)
                        break
        elif self.tool == TOOL_EXCHANGE:
            for neuron in chain(*self.network_manager.networks[self.network_manager.curr_network].all_nodes):
                if neuron.function == "interface_input" or neuron.function == "interface_output" or \
                        neuron.function == "subnet_input" or neuron.function == "subnet_output":
                    if VectorUtils.calc_cursor_collision(self.cursor_x, self.cursor_y, neuron, self.network_manager.zoom_factor[self.network_manager.curr_network]):
                        self.network_manager.delete_neuron(neuron.id, neuron.function, self.network_manager.curr_network)
                        break
        self.render_scene()

    def delete_connection(self):
        """
        Deletes a connection based on the cursor position.
        :return:        None
        """
        if self.tool == TOOL_CONNECTIONS and not self.do_connection:
            for connection in reversed(self.network_manager.networks[self.network_manager.curr_network].connections):
                if VectorUtils.connection_cursor_collision(connection, self.cursor_x, self.cursor_y,
                                                           self.network_manager.camera_x[self.network_manager.curr_network],
                                                           self.network_manager.camera_y[self.network_manager.curr_network],
                                                           self.network_manager.zoom_factor[self.network_manager.curr_network]):
                    self.network_manager.delete_connection(connection.id, self.network_manager.curr_network)
                    break
            self.render_scene()

    def delete_subnet(self):
        """
        Deletes a subnetwork based on the cursor position.
        :return:        None
        """
        if self.tool == TOOL_IMPORT:
            for subnet in reversed(self.network_manager.networks[self.network_manager.curr_network].subnets):
                does_collide = VectorUtils.calc_rect_collision_by_size([self.cursor_x, self.cursor_y],
                                                                       [subnet.posx, subnet.posy],
                                                                       subnet.size_x, subnet.size_y,
                                                                       self.network_manager.zoom_factor[self.network_manager.curr_network])
                if does_collide:
                    self.network_manager.delete_subnet(subnet.id, self.network_manager.curr_network)
                    break
            self.render_scene()

    def delete_entity(self, event):
        """
        Deletes an entity based on cursor position.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.get_free_cursor(event)
        self.delete_neuron()
        self.delete_connection()
        self.delete_subnet()

    def init_camera(self, event):
        """
        Initializes the zoom wheel.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.prev_wheel_pos_x = event.x
        self.prev_wheel_pos_y = event.y
        self.next_wheel_pos_x = event.x
        self.next_wheel_pos_y = event.y

    def move_camera(self, event):
        """
        Moves the camera through the network.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.prev_wheel_pos_x = event.x
        self.prev_wheel_pos_y = event.y

        self.network_manager.camera_x[self.network_manager.curr_network] = self.network_manager.camera_x[self.network_manager.curr_network] - VectorUtils.correct_zoom(self.next_wheel_pos_x - self.prev_wheel_pos_x,
                                                                 self.network_manager.zoom_factor[self.network_manager.curr_network])
        self.network_manager.camera_y[self.network_manager.curr_network] = self.network_manager.camera_y[self.network_manager.curr_network] - VectorUtils.correct_zoom(self.next_wheel_pos_y - self.prev_wheel_pos_y,
                                                                 self.network_manager.zoom_factor[self.network_manager.curr_network])

        self.next_wheel_pos_x = event.x
        self.next_wheel_pos_y = event.y

        self.render_scene()

    def zoom_scene(self, event):
        """
        Handles the zoom of the camera.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.get_free_cursor(event)
        old_cursor_x = self.cursor_x
        old_cursor_y = self.cursor_y

        if event.num == 4 or event.delta == 120:
            if self.network_manager.zoom_factor[self.network_manager.curr_network] < 4.0:
                self.network_manager.zoom_factor[self.network_manager.curr_network] = self.network_manager.zoom_factor[self.network_manager.curr_network] + 0.1
        if event.num == 5 or event.delta == -120:
            if self.network_manager.zoom_factor[self.network_manager.curr_network] > 0.2:
                self.network_manager.zoom_factor[self.network_manager.curr_network] = self.network_manager.zoom_factor[self.network_manager.curr_network] - 0.1

        self.get_free_cursor(event)
        self.network_manager.camera_x[self.network_manager.curr_network] = self.network_manager.camera_x[self.network_manager.curr_network] - (old_cursor_x - self.cursor_x)
        self.network_manager.camera_y[self.network_manager.curr_network] = self.network_manager.camera_y[self.network_manager.curr_network] - (old_cursor_y - self.cursor_y)

        self.get_cursor_position(event)

        self.render_scene()

    def init_resize(self, event):
        """
        Sets position of the cursor for resizing.
        :param event:   tkinter parameter for event handling.
        :return:        None
        """
        self.prev_wheel_pos_x = event.x
        self.next_wheel_pos_x = event.x

    def do_resize(self, event):
        """
        Resizes the parameter window when its borders are dragged.
        :param event:   tkinter parameter for event handling.
        :return:        None
        """
        offset = self.editframe.winfo_width() + event.x
        self.editresize.config(width=7)
        self.editframe.config(width=offset)
        if self.editframe.winfo_width() < 100:
            self.editframe.config(width=100)
        self.edit_top.config(width=offset)
        self.editresize.config(width=7)
        self.render_scene()
        self.root_frame.update()
        self.editresize.config(width=7)
