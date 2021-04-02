import re
from src.GlobalLibraries import *
from src.VectorUtils import VectorUtils

TOOL_NEURONS = 0
TOOL_CONNECTIONS = 1
TOOL_SELECT = 2


class Mainframe:
    def __init__(self, root, network_manager):
        """
        Constructor. Creates frames, widgets, etc.
        :param root: The root frame/window of program.
        :param network_manager: The object handling all currently opened networks.
        """
        self.neuron_size = 25

        self.cursor_x = 0.0
        self.cursor_y = 0.0

        self.prev_wheel_pos_x = 0.0
        self.prev_wheel_pos_y = 0.0
        self.next_wheel_pos_x = 0.0
        self.next_wheel_pos_y = 0.0

        self.tool = TOOL_NEURONS
        self.selected_neuron = -1
        self.selected_connection = -1
        self.selected_entity = None

        self.connecting_neuron = None
        self.connection_source_neuron = None

        self.root_frame = root
        self.network_manager = network_manager
        self.param_list = network_parameter

        self.root_frame.update()

        self.editframe_width = int(self.root_frame.winfo_width()/4)
        barmenu_height = self.root_frame.winfo_height() / 100
        self.pixelVirtual = tk.PhotoImage(width=1, height=1)
        
        self.edit_drop_options = ["Connection Specific",
                                  "Connection Habituation",
                                  "Connection Sensitization",
                                  "Connection Presynaptic",
                                  "Neuron Activation",
                                  "Neuron Transmitter",
                                  "Neuron Random",
                                  "Network"]
        self.edit_selection = tk.StringVar()
        self.edit_selection.set(self.edit_drop_options[0])
        self.parameter_count = 50
        self.parameter_frame = []
        self.parameter_info = []
        self.parameter_textbox = []
        self.do_connection = False
        self.grid_size = 50
        self.grid_snap = True
        
        self.mainframe = None
        self.editframe = None
        self.editresize = None
        self.edit_top = None
        self.select_button = None
        self.neuron_button = None
        self.connection_button = None
        self.viewframe = None
        self.editorcanvas = None
        self.edit_1 = None
        self.general_info = None
        self.id_info = None
        self.edit_drop_menu = None

    def pack_widgets(self):
        """
        Under construction: Will place all GUI widgets onto screen. Will be called in UI.py, to ensure correct
        order of widgets.
        """
        self.mainframe = tk.Frame(master=self.root_frame, background=grey_7,
                                  borderwidth=0,
                                  highlightthickness=1,
                                  highlightbackground=grey_2,
                                  height=self.root_frame.winfo_height(),
                                  width=self.root_frame.winfo_width())
        self.mainframe.grid_columnconfigure(0, weight=1)

        self.editframe = tk.Frame(master=self.mainframe, background=grey_4,
                                  borderwidth=2,
                                  highlightthickness=0,
                                  height=self.mainframe.winfo_height(),
                                  width=self.editframe_width,
                                  relief=tk.FLAT)
        self.editframe.pack_propagate(0)

        self.editresize = tk.Frame(master=self.editframe, background="#222222",
                                   borderwidth=1,
                                   highlightthickness=0,
                                   height=self.mainframe.winfo_height(),
                                   width=7,
                                   relief=tk.FLAT,
                                   cursor="sb_h_double_arrow")
        self.editresize.pack(side=tk.RIGHT, fill=tk.BOTH, padx=0, pady=0, expand=True)

        self.edit_top = tk.Frame(master=self.editframe, background=grey_4,
                                 borderwidth=0,
                                 highlightthickness=0,
                                 width=self.editframe_width)

        self.mainframe.pack(side=tk.TOP, fill=tk.BOTH, padx=0, pady=0, expand=True)
        self.editframe.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0, expand=False)
        self.edit_top.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=15, expand=False)

        self.root_frame.update()

        self.select_button = tk.Button(master=self.edit_top, text="S", background=grey_3,
                                       fg=grey_c, command=self.switch_tool_select, image=self.pixelVirtual,
                                       activebackground=grey_7,
                                       width=50,
                                       compound="c")
        self.neuron_button = tk.Button(master=self.edit_top, text="N", background=dark_blue,
                                       fg=grey_c, command=self.switch_tool_neurons, image=self.pixelVirtual,
                                       activebackground=grey_7,
                                       width=50, compound="c")
        self.connection_button = tk.Button(master=self.edit_top, text="C", background=grey_3,
                                           fg=grey_c, command=self.switch_tool_connections, image=self.pixelVirtual,
                                           activebackground=grey_7,
                                           width=50, compound="c")

        self.viewframe = tk.Frame(master=self.mainframe, background=grey_3,
                                  highlightthickness=0,
                                  borderwidth=2,
                                  height=self.editframe.winfo_height(),
                                  width=self.mainframe.winfo_width() - self.editframe.winfo_width())
        self.viewframe.grid_columnconfigure(0, weight=1)

        self.editorcanvas = tk.Canvas(master=self.viewframe, background=grey_3,
                                      highlightthickness=0,
                                      borderwidth=0,
                                      height=self.viewframe.winfo_height(),
                                      width=self.viewframe.winfo_width(),
                                      cursor="crosshair")

        self.edit_1 = tk.Frame(master=self.editframe, background=grey_4,
                               borderwidth=0,
                               highlightthickness=0,
                               width=self.editframe_width)
        
        for i in range(0, self.parameter_count):
            self.parameter_frame.append(tk.Frame(master=self.editframe, background=grey_4,
                                                 borderwidth=0,
                                                 highlightthickness=0,
                                                 width=self.editframe_width))

        self.general_info = tk.Label(master=self.parameter_frame[0], text="No Entity Selected", bg=grey_4,
                                     fg=light_blue)
        self.id_info = tk.Label(master=self.parameter_frame[1], text="", bg=grey_4,
                                fg=grey_c)

        self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[2], self.edit_selection, *self.edit_drop_options,
                                            command=self.show_parameters)
        self.edit_drop_menu.config(bg=grey_4, width=self.editframe_width, fg=grey_c,
                                   borderwidth=0, highlightthickness=3, highlightbackground=grey_2,
                                   activebackground=grey_7)


        self.select_button.pack(side=tk.LEFT, padx=button_padding_x, pady=button_padding_y)
        self.neuron_button.pack(side=tk.LEFT, padx=button_padding_x, pady=button_padding_y)
        self.connection_button.pack(side=tk.LEFT, padx=button_padding_x, pady=button_padding_y)

        for i in range(0, self.parameter_count):
            padding_y = 10
            if i == 2:
                padding_y = 40
            self.parameter_frame[i].pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=padding_y, expand=False)

        self.edit_1.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=20, expand=False)

        self.viewframe.pack(side=tk.LEFT, fill=tk.BOTH, padx=0, pady=0, expand=True)
        self.editorcanvas.pack(side=tk.RIGHT, fill=tk.BOTH, padx=0, pady=0, expand=True)

        self.root_frame.update()
        self.network_manager.camera_x[self.network_manager.curr_network] = self.editorcanvas.winfo_width() / 2
        self.network_manager.camera_y[self.network_manager.curr_network] = self.editorcanvas.winfo_height() / 2
        self.render_scene()

        self.show_parameters(store=False)

        self.editresize.bind("<Button-1>", self.init_resize)
        self.editresize.bind("<B1-Motion>", self.do_resize)

        self.editorcanvas.bind("<Motion>", self.motion_event)

        self.editorcanvas.bind("<Button-2>", self.init_camera)
        self.editorcanvas.bind("<B2-Motion>", self.move_camera)
        self.editorcanvas.bind("<Button-1>", self.left_click)
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
        self.root_frame.bind("<Return>", self.show_parameters)

        self.switch_tool_select()

    def check_parameter_uniqueness(self, parameter_name):
        """
        Checks if a parameter inside of a textbox is unique, or if any other entity higher in the hierarchy
        has the same value for the parameter
        :param parameter_name: The parameter which should be checked.
        :return: Bool value if parameter is unique or not.
        """
        if self.selected_neuron > -1:
            neuron_param = self.selected_entity.param.list[parameter_name]
            neuron_network = self.selected_entity.network_id
            network_param = self.network_manager.networks[neuron_network].param.list[parameter_name]
            if neuron_param == network_param:
                return False
        elif self.selected_connection > -1:
            connection_param = self.selected_entity.param.list[parameter_name]
            connection_network = self.selected_entity.network_id
            prev_neuron = self.selected_entity.prev_neuron
            neuron_param = self.network_manager.networks[connection_network].neurons[prev_neuron-1].param.list[parameter_name]
            network_param = self.network_manager.networks[connection_network].param.list[parameter_name]
            if connection_param == neuron_param:
                return False
            elif neuron_param is None and connection_param == network_param:
                return False
        else:
            return True

        return True

    def store_parameters(self):
        """
        Stores all parameter, which are currently opened in the GUI.
        """
        if self.tool == TOOL_SELECT:
            for i, name in enumerate(self.param_list):
                for param_container in self.parameter_textbox:
                    if param_container[1] == name:
                        temp_param = param_container[0].get("1.0", "end")
                        try:
                            self.selected_entity.param.list[name] = float(temp_param)
                        except ValueError:
                            self.selected_entity.param.list[name] = None

                        is_unique = self.check_parameter_uniqueness(name)
                        if not is_unique:
                            self.selected_entity.param.list[name] = None

    def print_parameter(self, entity, param_index, name):
        """
        Prints the parameter into its textbox given corresponding index value.
        :param entity: The entity the parameter is assigned to.
        :param param_index: The index of the parameter
        :param name: The name of the parameter. Must be given for other functions and to check for rule exceptions
                     in parameter GUI handling.
        """
        if entity.param.list[name] is None:
            if isinstance(entity, Connection):
                network_id = entity.network_id
                neuron_id = entity.prev_neuron-1
                self.print_parameter(self.network_manager.networks[network_id].neurons[neuron_id], param_index, name)
                self.parameter_textbox[param_index][0].config(fg=grey_4)
            elif isinstance(entity, Neuron):
                network_id = entity.network_id
                self.print_parameter(self.network_manager.networks[network_id], param_index, name)
                self.parameter_textbox[param_index][0].config(fg=grey_4)
            else:
                self.parameter_textbox[param_index][0].insert("1.0", "Missing...")
                self.parameter_textbox[param_index][0].config(fg=dark_red)
        else:
            try:
                regex = re.compile("(-?[0-9]*(\.[0 -9]*[1-9])?)", re.IGNORECASE)
                param_str = regex.findall(format(entity.param.list[name], ".15f"))
                self.parameter_textbox[param_index][0].insert("1.0", param_str[0][0])
            except TypeError:
                self.parameter_textbox[param_index][0].insert("1.0", "Missing...")
                self.parameter_textbox[param_index][0].config(fg=dark_red)

    def show_entity_parameters(self):
        """
        The function which renders the parameters to the left frame of the program.
        """
        if self.selected_connection > -1:
            self.general_info.config(text=f"Connection <{self.selected_connection}> Selected")
        elif self.selected_neuron > -1:
            self.edit_drop_options.append("Neuron Activation")
            self.edit_drop_options.append("Neuron Transmitter")
            self.edit_drop_options.append("Neuron Random")
            self.general_info.config(text=f"Neuron <{self.selected_neuron}> Selected")
        else:
            self.edit_drop_options.append("Neuron Activation")
            self.edit_drop_options.append("Neuron Transmitter")
            self.edit_drop_options.append("Neuron Random")
            self.general_info.config(text="Neuron Selected")
            self.edit_drop_options.append("Network")
            self.general_info.config(text=f"Neural Network <{self.network_manager.curr_network}> Selected")

        self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[2], self.edit_selection, *self.edit_drop_options,
                                            command=self.show_parameters)
        self.edit_drop_menu.config(bg=grey_4, width=self.editframe_width, fg=grey_c,
                                   borderwidth=0, highlightthickness=3, highlightbackground=grey_2,
                                   activebackground=grey_7)
        self.edit_drop_menu["menu"].config(bg=grey_4, fg=grey_c, borderwidth=1,
                                           activebackground=grey_7, relief=tk.RIDGE)

        self.general_info.pack(side=tk.LEFT)
        self.edit_drop_menu.pack(side=tk.LEFT)

        if self.edit_selection.get() == self.edit_drop_options[0]:
            self.param_list = connection_special_parameter
        elif self.edit_selection.get() == self.edit_drop_options[1]:
            self.param_list = connection_habituation_parameter
        elif self.edit_selection.get() == self.edit_drop_options[2]:
            self.param_list = connection_sensitization_parameter
        elif self.edit_selection.get() == self.edit_drop_options[3]:
            self.param_list = connection_presynaptic_parameter
        elif self.edit_selection.get() == self.edit_drop_options[4]:
            self.param_list = neuron_activation_parameter
        elif self.edit_selection.get() == self.edit_drop_options[5]:
            self.param_list = neuron_transmitter_parameter
        elif self.edit_selection.get() == self.edit_drop_options[6]:
            self.param_list = neuron_random_parameter
        elif self.edit_selection.get() == self.edit_drop_options[7]:
            self.param_list = network_parameter

        for i, name in enumerate(self.param_list):
            self.parameter_textbox.append([tk.Text(master=self.parameter_frame[i+3], height=1, width=10,
                                                   bg=grey_7, borderwidth=0,
                                                   highlightthickness=2, highlightbackground=grey_2),
                                           name])

            self.print_parameter(self.selected_entity, i, name)
            self.parameter_textbox[i][0].pack(side=tk.LEFT, padx=20)

            self.parameter_info.append(tk.Label(master=self.parameter_frame[i+3], text=name,
                                                bg=grey_4, fg=grey_c))
            self.parameter_info[i].pack(side=tk.LEFT)

    def show_parameters(self, event=None, store=True):
        """
        Initializes and prepares parameter frame for rendering new parameters.
        :param event: Variable for use as callback function
        :param store: Determines whether parameters should be stored before rendering new parameters.
        """
        if store:
            self.store_parameters()
        if self.selected_connection > -1:
            self.selected_entity = self.network_manager.networks[self.network_manager.curr_network].connections[self.selected_connection]
        elif self.selected_neuron > -1:
            self.selected_entity = self.network_manager.networks[self.network_manager.curr_network].neurons[self.selected_neuron-1]
        else:
            self.selected_entity = self.network_manager.networks[self.network_manager.curr_network]

        self.edit_drop_menu.destroy()
        self.id_info.pack_forget()
        for i in range(0, len(self.parameter_info)):
            self.parameter_info[i].destroy()
        self.parameter_info.clear()
        for i in range(0, len(self.parameter_textbox)):
            self.parameter_textbox[i][0].destroy()
        self.parameter_textbox.clear()
        self.edit_drop_options.clear()
        self.general_info.forget()

        self.edit_drop_options = ["Connection Specific",
                                  "Connection Habituation",
                                  "Connection Sensitization",
                                  "Connection Presynaptic"]

        if not event:
            self.edit_selection.set(self.edit_drop_options[0])

        if self.tool == TOOL_SELECT:
            self.show_entity_parameters()

    def switch_tool_neurons(self):
        """
        Function to switch tool stance to neuron editing.
        """
        self.tool = TOOL_NEURONS
        self.selected_entity = None
        self.neuron_button.configure(background=dark_blue)
        self.connection_button.configure(background=grey_3)
        self.select_button.configure(background=grey_3)
        self.discard_connection()
        self.deselect_all()
        self.show_parameters(store=False)
        self.render_scene()

    def switch_tool_connections(self):
        """
        Function to switch tool stance to connection editing.
        """
        self.tool = TOOL_CONNECTIONS
        self.selected_entity = None
        self.neuron_button.configure(background=grey_3)
        self.connection_button.configure(background=dark_blue)
        self.select_button.configure(background=grey_3)
        self.deselect_all()
        self.show_parameters(store=False)
        self.render_scene()

    def switch_tool_select(self):
        """
        Function to switch tool stance to selecting and parameter editing.
        """
        self.tool = TOOL_SELECT
        self.neuron_button.configure(background=grey_3)
        self.connection_button.configure(background=grey_3)
        self.select_button.configure(background=dark_blue)
        self.discard_connection()
        self.deselect_all()
        self.show_parameters(store=False)
        self.render_scene()

    def reset_camera(self, event=None):
        """
        Resets camera view and zoom.
        :param event: Parameter for use as callback function.
        """
        self.network_manager.camera_x[self.network_manager.curr_network] = self.editorcanvas.winfo_width() / 2
        self.network_manager.camera_y[self.network_manager.curr_network] = self.editorcanvas.winfo_height() / 2
        self.network_manager.zoom_factor[self.network_manager.curr_network] = 1.0
        self.render_scene()

    def render_grid(self):
        """
        Renders the grid onto the edit canvas, if grid snap is activated.
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
                                          fill=grey_4, width=2)
            temp_x = temp_x + self.grid_size

        while temp_y < VectorUtils.correct_zoom(self.editorcanvas.winfo_height()+temp_camera_y, self.network_manager.zoom_factor[self.network_manager.curr_network]):
            self.editorcanvas.create_line(0, temp_y * self.network_manager.zoom_factor[self.network_manager.curr_network],
                                          corrected_x, temp_y * self.network_manager.zoom_factor[self.network_manager.curr_network],
                                          fill=grey_4, width=2)
            temp_y = temp_y + self.grid_size

    def render_connections(self):
        """
        Renders all connections of the currently active network.
        """
        for connection_i, connection in enumerate(self.network_manager.networks[self.network_manager.curr_network].connections):
            distance = 5
            direction_marker_length = 8

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
                                                                             self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(direction_marker_a[1],
                                                                             self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(direction_marker_b[0],
                                                                             self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(direction_marker_b[1],
                                                                             self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              fill=light_blue, width=connection_width)
            except IndexError:
                pass

            for vert in range(0, len(temp_verts)-1):
                if connection.id == self.selected_connection:
                    self.editorcanvas.create_line(VectorUtils.project_coordinate(temp_verts[vert][0],
                                                                                 self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                  VectorUtils.project_coordinate(temp_verts[vert][1],
                                                                                 self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                  VectorUtils.project_coordinate(temp_verts[vert + 1][0],
                                                                                 self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                  VectorUtils.project_coordinate(temp_verts[vert + 1][1],
                                                                                 self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                  fill=grey_c, width=selected_connection_width)
                else:
                    self.editorcanvas.create_line(VectorUtils.project_coordinate(temp_verts[vert][0],
                                                                                 self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                  VectorUtils.project_coordinate(temp_verts[vert][1],
                                                                                 self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                  VectorUtils.project_coordinate(temp_verts[vert + 1][0],
                                                                                 self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                  VectorUtils.project_coordinate(temp_verts[vert + 1][1],
                                                                                 self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                  fill=light_blue, width=connection_width)

    def render_neurons(self):
        """
        Renders all neurons of the currently active network.
        """
        for neuron in self.network_manager.networks[self.network_manager.curr_network].neurons:
            if self.selected_neuron == neuron.id:
                self.editorcanvas.create_circle(VectorUtils.project_coordinate(neuron.posx, self.network_manager.camera_x[self.network_manager.curr_network],
                                                                               self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                VectorUtils.project_coordinate(neuron.posy, self.network_manager.camera_y[self.network_manager.curr_network],
                                                                               self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                self.neuron_size * self.network_manager.zoom_factor[self.network_manager.curr_network], fill=white,
                                                outline=light_blue,
                                                width=5 * self.network_manager.zoom_factor[self.network_manager.curr_network])
            else:
                self.editorcanvas.create_circle(VectorUtils.project_coordinate(neuron.posx, self.network_manager.camera_x[self.network_manager.curr_network],
                                                                               self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                VectorUtils.project_coordinate(neuron.posy, self.network_manager.camera_y[self.network_manager.curr_network],
                                                                               self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                                self.neuron_size * self.network_manager.zoom_factor[self.network_manager.curr_network], fill=white)
            self.editorcanvas.create_text(VectorUtils.project_coordinate(neuron.posx, self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                          VectorUtils.project_coordinate(neuron.posy, self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                          text=f"{neuron.id}", fill=grey_3)

    def render_ui_description(self):
        """
        Renders text elements onto the canvas.
        """
        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 15, anchor="w",
                                      text="Mode:", fill=grey_c)
        if self.tool == TOOL_SELECT:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="SELECTING", fill=light_blue)
        elif self.tool == TOOL_NEURONS:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="NEURON EDITING", fill=light_blue)
        elif self.tool == TOOL_CONNECTIONS:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="CONNECTION EDITING", fill=light_blue)

        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 90, anchor="w",
                                      text=f"Camera X: {int(self.network_manager.camera_x[self.network_manager.curr_network])}", fill=grey_c)
        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 60, anchor="w",
                                      text=f"Camera Y: {int(self.network_manager.camera_y[self.network_manager.curr_network])}", fill=grey_c)

        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 175, anchor="w",
                                      text=f"Cursor X: {int(self.cursor_x)}", fill=grey_c)
        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 145, anchor="w",
                                      text=f"Cursor Y: {int(self.cursor_y)}", fill=grey_c)

        self.editorcanvas.create_text(self.editorcanvas.winfo_width() - 5, self.editorcanvas.winfo_height() - 15,
                                      anchor="e",
                                      text=f"Zoom: {round(self.network_manager.zoom_factor[self.network_manager.curr_network] * 100, 0)}%", fill=grey_c)

        if self.grid_snap:
            self.editorcanvas.create_text(self.editorcanvas.winfo_width() - 5, self.editorcanvas.winfo_height() - 60,
                                          anchor="e", fill=light_blue,
                                          text="Grid Snap Active")

    def render_scene(self):
        """
        Function responsible for calling all other rendering functions and rendering the whole scene in the
        edit canvas.
        """
        if len(self.network_manager.networks) > 0:
            if self.editorcanvas is not None:
                self.editorcanvas.delete("all")

                if self.grid_snap:
                    self.render_grid()

                self.render_connections()
                self.render_neurons()

                self.editorcanvas.create_text(VectorUtils.project_coordinate(0, self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              VectorUtils.project_coordinate(0, self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]),
                                              text="X", fill=light_blue, font="arial 15")

                self.render_ui_description()

                if self.editframe.winfo_width() < 100:
                    self.editframe.config(width=100)

    def snap_cursor_to_grid(self):
        """
        Toggles grid snapping and visibility of grid.
        """
        if self.tool != TOOL_SELECT:
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
        :param event: Parameter for use as callback function.
        """
        self.cursor_x = VectorUtils.correct_zoom(event.x, self.network_manager.zoom_factor[self.network_manager.curr_network]) - self.network_manager.camera_x[self.network_manager.curr_network]
        self.cursor_y = VectorUtils.correct_zoom(event.y, self.network_manager.zoom_factor[self.network_manager.curr_network]) - self.network_manager.camera_y[self.network_manager.curr_network]

    def get_cursor_position(self, event):
        """
        Returns free cursor (not snapped to the grid) to the cursor member variables, even if grid snapping is active.
        Afterwards it renders the scene and snaps cursor back to the grid.
        Useful if a very specific action should be independent from the grid.
        :param event:
        :return:
        """
        self.get_free_cursor(event)
        self.render_scene()

        self.snap_cursor_to_grid()

    def add_neuron(self):
        """
        Adds a neuron to the network.
        """
        neuron_x = self.cursor_x
        neuron_y = self.cursor_y

        self.network_manager.add_neuron(neuron_x, neuron_y, self.neuron_size, self.network_manager.curr_network)

    def init_connection(self, neuron):
        self.connecting_neuron = neuron
        self.do_connection = True

        self.network_manager.add_connection(self.connection_source_neuron, self.network_manager.curr_network)
        connection_position = len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1
        self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices.append(
            np.array([self.cursor_x,
                      self.cursor_y]))

    def draw_connection(self):
        if self.do_connection:
            self.render_scene()
            connection_position = len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1
            vertex_position = len(self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices) - 1
            self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices[vertex_position] = [self.cursor_x,
                                                                                                           self.cursor_y]

    def discard_connection(self):
        if self.do_connection:
            connection_position = len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1
            self.network_manager.delete_connection(connection_position)
            self.do_connection = False

    def deselect_neurons(self):
        self.selected_neuron = -1

    def deselect_connections(self):
        self.selected_connection = -1
       
    def deselect_all(self):
        self.deselect_neurons()
        self.deselect_connections()
        #self.selected_entity = None

    def escape_event(self, event):
        self.store_parameters()
        self.discard_connection()
        self.deselect_neurons()
        self.deselect_connections()
        self.render_scene()

    def delete_event(self, event):
        if self.selected_neuron != -1:
            self.network_manager.delete_neuron(self.selected_neuron)
            self.deselect_neurons()
        if self.selected_connection != -1:
            self.network_manager.delete_connection(self.selected_connection)
            self.deselect_connections()
        self.render_scene()

    def tab_event(self, event):
        self.escape_event(event)
        if self.tool == TOOL_NEURONS:
            self.switch_tool_connections()
        elif self.tool == TOOL_CONNECTIONS:
            self.switch_tool_select()
        elif self.tool == TOOL_SELECT:
            self.switch_tool_neurons()

    def toggle_grid_snap(self, event):
        if self.grid_snap:
            self.grid_snap = False
        else:
            self.grid_snap = True
        self.render_scene()

    def create_neuron_connection(self, neuron):
        if self.do_connection:
            can_connect = True
            connection_position = len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1
            for check_con in self.network_manager.networks[self.network_manager.curr_network].connections:
                if check_con.prev_neuron == self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].prev_neuron \
                        and check_con.next_neuron == neuron.id:
                    can_connect = False
            if can_connect:
                vertex_position = len(self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices) - 1
                self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].next_neuron = neuron.id
                self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices[vertex_position] = [
                    neuron.posx, neuron.posy]
            else:
                self.discard_connection()
            self.do_connection = False
        else:
            self.init_connection(neuron)

    def create_synaptic_connection(self, connection):
        if self.do_connection:
            if connection.id < len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1:
                can_connect = True
                connection_position = len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1
                for check_con in self.network_manager.networks[self.network_manager.curr_network].connections:
                    if check_con.prev_neuron == self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].prev_neuron \
                            and check_con.next_connection == connection.id:
                        can_connect = False

                if can_connect:
                    vertex_position = len(self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices) - 1
                    self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].next_connection = connection.id
                    self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices[vertex_position] = [
                        self.cursor_x, self.cursor_y]
                else:
                    self.discard_connection()
                self.do_connection = False

    def left_click(self, event):
        neuron_collision = False
        connection_collision = False
        for neuron in self.network_manager.networks[self.network_manager.curr_network].neurons:
            if VectorUtils.calc_cursor_collision(self.cursor_x, self.cursor_y, neuron, self.network_manager.zoom_factor[self.network_manager.curr_network]):
                if self.tool == TOOL_CONNECTIONS:
                    if not self.do_connection:
                        self.connection_source_neuron = neuron
                    self.create_neuron_connection(neuron)
                    if not self.do_connection:
                        self.connection_source_neuron = None
                elif self.tool == TOOL_SELECT:
                    self.store_parameters()
                    self.deselect_connections()
                    self.selected_neuron = neuron.id
                    self.show_parameters(store=False)

                neuron_collision = True

        if not neuron_collision:
            for connection in self.network_manager.networks[self.network_manager.curr_network].connections:
                if VectorUtils.connection_cursor_collision(connection, self.cursor_x, self.cursor_y,
                                                           self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]):
                    if self.tool == TOOL_CONNECTIONS:
                        self.create_synaptic_connection(connection)

            if not self.do_connection:
                if self.tool == TOOL_NEURONS:
                    self.add_neuron()
            else:
                connection_position = len(self.network_manager.networks[self.network_manager.curr_network].connections) - 1
                self.network_manager.networks[self.network_manager.curr_network].connections[connection_position].vertices.append(
                    np.array([self.cursor_x, self.cursor_y]))

            if self.tool == TOOL_SELECT:
                self.store_parameters()
                self.deselect_neurons()
                self.show_parameters(store=False)
                for connection in self.network_manager.networks[self.network_manager.curr_network].connections:
                    if VectorUtils.connection_cursor_collision(connection, self.cursor_x, self.cursor_y,
                                                               self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]):
                        self.selected_connection = connection.id
                        connection_collision = True
                if not connection_collision:
                    self.deselect_connections()
                self.show_parameters(store=False)

        self.render_scene()

    def motion_event(self, event):
        self.get_cursor_position(event)
        self.draw_connection()

    def delete_neuron(self):
        if self.tool == TOOL_NEURONS:
            for neuron in self.network_manager.networks[self.network_manager.curr_network].neurons:
                if VectorUtils.calc_cursor_collision(self.cursor_x, self.cursor_y, neuron, self.network_manager.zoom_factor[self.network_manager.curr_network]):
                    self.network_manager.delete_neuron(neuron.id, self.network_manager.curr_network)
            self.render_scene()

    def delete_connection(self):
        if self.tool == TOOL_CONNECTIONS and not self.do_connection:
            for connection in self.network_manager.networks[self.network_manager.curr_network].connections:
                if VectorUtils.connection_cursor_collision(connection, self.cursor_x, self.cursor_y,
                                                           self.network_manager.camera_x[self.network_manager.curr_network], self.network_manager.camera_y[self.network_manager.curr_network], self.network_manager.zoom_factor[self.network_manager.curr_network]):
                    self.network_manager.delete_connection(connection.id, self.network_manager.curr_network)
            self.render_scene()

    def delete_entity(self, event):
        self.get_free_cursor(event)
        self.delete_neuron()
        self.delete_connection()

    def init_camera(self, event):
        self.prev_wheel_pos_x = event.x
        self.prev_wheel_pos_y = event.y
        self.next_wheel_pos_x = event.x
        self.next_wheel_pos_y = event.y

    def move_camera(self, event):
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
        self.prev_wheel_pos_x = event.x
        self.next_wheel_pos_x = event.x

    def do_resize(self, event):
        self.prev_wheel_pos_x = event.x

        offset = self.next_wheel_pos_x - self.prev_wheel_pos_x
        self.editresize.config(width=7)
        self.editframe.config(width=self.editframe.winfo_width() - offset)
        if self.editframe.winfo_width() < 100:
            self.editframe.config(width=100)
        self.edit_top.config(width=self.edit_top.winfo_width() - offset)
        self.editresize.config(width=7)
        self.render_scene()
        self.root_frame.update()
        self.editresize.config(width=7)

        self.next_wheel_pos_x = event.x
