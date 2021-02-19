from src.GlobalLibraries import *

TOOL_NEURONS = 0
TOOL_CONNECTIONS = 1
TOOL_SELECT = 2


class Mainframe:
    def __init__(self, root, network_manager):
        self.cursor_x = 0.0
        self.cursor_y = 0.0
        self.camera_x = 0.0
        self.camera_y = 0.0
        self.zoom_factor = 1.0

        self.prev_wheel_pos_x = 0.0
        self.prev_wheel_pos_y = 0.0
        self.next_wheel_pos_x = 0.0
        self.next_wheel_pos_y = 0.0

        self.tool = TOOL_NEURONS
        self.selected_neuron = -1
        self.selected_connection = -1

        self.connecting_neuron = None

        self.root_frame = root
        self.network_manager = network_manager

        self.img_default_neuron = ImageTk.PhotoImage(Image.open(default_neuron_filename))
        self.img_neuron_selected = ImageTk.PhotoImage(Image.open(neuron_selected_filename))

        root.update()

        self.editframe_width = int(root.winfo_width()/4)

        self.mainframe = tk.Frame(master=root, background=mainframe_backcolor,
                                  borderwidth=0,
                                  highlightthickness=1,
                                  highlightbackground=highlight_color,
                                  height=root.winfo_height() - topmenu_height - bottommenu_height,
                                  width=root.winfo_width())
        self.mainframe.grid_columnconfigure(0, weight=1)

        self.editframe = tk.Frame(master=self.mainframe, background=editframe_backcolor,
                                  borderwidth=2,
                                  highlightthickness=0,
                                  height=self.mainframe.winfo_height(),
                                  width=self.editframe_width,
                                  relief=tk.FLAT)
        self.editframe.pack_propagate(0)

        self.edit_top = tk.Frame(master=self.editframe, background=editframe_backcolor,
                                 borderwidth=0,
                                 highlightthickness=0,
                                 width=self.editframe_width)

        self.neuron_button = tk.Button(master=self.edit_top, text="N", background=active_button_color,
                                       fg=textcolor, command=self.switch_tool_neurons,
                                       activebackground=mainframe_backcolor)
        self.connection_button = tk.Button(master=self.edit_top, text="C", background=inactive_button_color,
                                           fg=textcolor, command=self.switch_tool_connections,
                                       activebackground=mainframe_backcolor)
        self.select_button = tk.Button(master=self.edit_top, text="S", background=inactive_button_color,
                                       fg=textcolor, command=self.switch_tool_select,
                                       activebackground=mainframe_backcolor)

        self.viewframe = tk.Frame(master=self.mainframe, background=viewframe_backcolor,
                                  highlightthickness=0,
                                  borderwidth=2,
                                  height=self.editframe.winfo_height(),
                                  width=self.mainframe.winfo_width() - self.editframe.winfo_width())
        self.viewframe.grid_columnconfigure(0, weight=1)

        self.editorcanvas = tk.Canvas(master=self.viewframe, background=viewframe_backcolor,
                                      highlightthickness=0,
                                      borderwidth=0,
                                      height=self.viewframe.winfo_height(),
                                      width=self.viewframe.winfo_width())

        self.edit_1 = tk.Frame(master=self.editframe, background=editframe_backcolor,
                               borderwidth=0,
                               highlightthickness=0,
                               width=self.editframe_width)
        self.parameter_count = 50
        self.parameter_frame = []
        for i in range(0, self.parameter_count):
            self.parameter_frame.append(tk.Frame(master=self.editframe, background=editframe_backcolor,
                                        borderwidth=0,
                                        highlightthickness=0,
                                        width=self.editframe_width))

        self.general_info = tk.Label(master=self.parameter_frame[0], text="No Entity Selected", bg=editframe_backcolor,
                                     fg=mode_text_color)
        self.id_info = tk.Label(master=self.parameter_frame[1], text="", bg=editframe_backcolor,
                                fg=textcolor)

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
        self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[2], self.edit_selection, *self.edit_drop_options,
                                            command=self.show_parameters)
        self.edit_drop_menu.config(bg=editframe_backcolor, width=self.editframe_width, fg=textcolor,
                                   borderwidth=0, highlightthickness=3, highlightbackground=highlight_color,
                                   activebackground=mainframe_backcolor)

        self.parameter_info = []
        self.parameter_textbox = []

        self.mainframe.pack(side=tk.TOP, fill=tk.BOTH, padx=0, pady=0, expand=True)
        self.editframe.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0, expand=False)
        self.edit_top.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=15, expand=False)
        self.neuron_button.pack(side=tk.LEFT, padx=button_padding_x, pady=button_padding_y)
        self.connection_button.pack(side=tk.LEFT, padx=button_padding_x, pady=button_padding_y)
        self.select_button.pack(side=tk.LEFT, padx=button_padding_x, pady=button_padding_y)

        for i in range(0, self.parameter_count):
            padding_y = 10
            if i == 2:
                padding_y = 40
            self.parameter_frame[i].pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=padding_y, expand=False)

        self.edit_1.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=20, expand=False)

        self.viewframe.pack(side=tk.LEFT, fill=tk.BOTH, padx=0, pady=0, expand=True)
        self.editorcanvas.pack(side=tk.RIGHT, fill=tk.BOTH, padx=0, pady=0, expand=True)

        self.do_connection = False

        self.grid_size = 50
        self.grid_snap = True

        self.root_frame.update()
        self.camera_x = self.editorcanvas.winfo_width() / 2
        self.camera_y = self.editorcanvas.winfo_height() / 2
        self.render_scene()

        self.show_parameters()

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
        self.root_frame.bind("<BackSpace>", self.delete_event)
        self.root_frame.bind("<Tab>", self.tab_event)
        self.root_frame.bind("<g>", self.toggle_grid_snap)
        self.root_frame.bind("<space>", self.reset_camera)

    def show_network_information(self):
        self.edit_drop_options = ["Connection Specific",
                                  "Connection Habituation",
                                  "Connection Sensitization",
                                  "Connection Presynaptic",
                                  "Neuron Activation",
                                  "Neuron Transmitter",
                                  "Neuron Random",
                                  "Network"]

        self.edit_drop_menu.destroy()
        self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[2], self.edit_selection, *self.edit_drop_options,
                                            command=self.show_parameters)
        self.edit_drop_menu.config(bg=editframe_backcolor, width=self.editframe_width, fg=textcolor,
                                   borderwidth=0, highlightthickness=3, highlightbackground=highlight_color,
                                   activebackground=mainframe_backcolor)

        self.general_info.config(text="Neural Network Selected")
        self.id_info.pack_forget()
        self.general_info.pack(side=tk.LEFT)

        self.edit_drop_menu.pack(side=tk.LEFT)

        for i in range(0, len(self.parameter_info)):
            self.parameter_info[i].destroy()
        self.parameter_info.clear()
        for i in range(0, len(self.parameter_textbox)):
            self.parameter_textbox[i].destroy()
        self.parameter_textbox.clear()

        temp_param_list = network_parameter

        if self.edit_selection.get() == self.edit_drop_options[0]:
            temp_param_list = connection_special_parameter
        elif self.edit_selection.get() == self.edit_drop_options[1]:
            temp_param_list = connection_habituation_parameter
        elif self.edit_selection.get() == self.edit_drop_options[2]:
            temp_param_list = connection_sensitization_parameter
        elif self.edit_selection.get() == self.edit_drop_options[3]:
            temp_param_list = connection_presynaptic_parameter
        elif self.edit_selection.get() == self.edit_drop_options[4]:
            temp_param_list = neuron_activation_parameter
        elif self.edit_selection.get() == self.edit_drop_options[5]:
            temp_param_list = neuron_transmitter_parameter
        elif self.edit_selection.get() == self.edit_drop_options[6]:
            temp_param_list = neuron_random_parameter
        elif self.edit_selection.get() == self.edit_drop_options[7]:
            temp_param_list = network_parameter

        for i, name in enumerate(temp_param_list):
            self.parameter_textbox.append(tk.Text(master=self.parameter_frame[i+3], height=1, width=5,
                                                  bg=mainframe_backcolor, borderwidth=0,
                                                  highlightthickness=2, highlightbackground=highlight_color))

            self.parameter_textbox[i].insert("1.0", self.network_manager.networks[0].param.list[name])
            self.parameter_textbox[i].pack(side=tk.LEFT, padx=20)

            self.parameter_info.append(tk.Label(master=self.parameter_frame[i+3], text=name,
                                                bg=editframe_backcolor, fg=textcolor))
            self.parameter_info[i].pack(side=tk.LEFT)

    def show_neuron_information(self):
        self.edit_drop_options = ["Connection Specific",
                                  "Connection Habituation",
                                  "Connection Sensitization",
                                  "Connection Presynaptic",
                                  "Neuron Activation",
                                  "Neuron Transmitter",
                                  "Neuron Random"]

        self.edit_drop_menu.destroy()
        self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[2], self.edit_selection, *self.edit_drop_options,
                                            command=self.show_parameters)
        self.edit_drop_menu.config(bg=editframe_backcolor, width=self.editframe_width, fg=textcolor,
                                   borderwidth=0, highlightthickness=3, highlightbackground=highlight_color,
                                   activebackground=mainframe_backcolor)

        self.general_info.config(text="Neuron Selected")
        self.id_info.config(text=f"ID: {self.selected_neuron}")
        self.general_info.pack(side=tk.LEFT)
        self.id_info.pack(side=tk.LEFT)

        self.edit_drop_menu.pack(side=tk.LEFT)

        for i in range(0, len(self.parameter_info)):
            self.parameter_info[i].destroy()
        self.parameter_info.clear()
        for i in range(0, len(self.parameter_textbox)):
            self.parameter_textbox[i].destroy()
        self.parameter_textbox.clear()

        temp_param_list = neuron_activation_parameter

        if self.edit_selection.get() == self.edit_drop_options[0]:
            temp_param_list = connection_special_parameter
        elif self.edit_selection.get() == self.edit_drop_options[1]:
            temp_param_list = connection_habituation_parameter
        elif self.edit_selection.get() == self.edit_drop_options[2]:
            temp_param_list = connection_sensitization_parameter
        elif self.edit_selection.get() == self.edit_drop_options[3]:
            temp_param_list = connection_presynaptic_parameter
        elif self.edit_selection.get() == self.edit_drop_options[4]:
            temp_param_list = neuron_activation_parameter
        elif self.edit_selection.get() == self.edit_drop_options[5]:
            temp_param_list = neuron_transmitter_parameter
        elif self.edit_selection.get() == self.edit_drop_options[6]:
            temp_param_list = neuron_random_parameter

        for i, name in enumerate(temp_param_list):
            self.parameter_textbox.append(tk.Text(master=self.parameter_frame[i + 3], height=1, width=5,
                                                  bg=mainframe_backcolor, borderwidth=0,
                                                  highlightthickness=2, highlightbackground=highlight_color))

            self.parameter_textbox[i].insert("1.0", self.network_manager.networks[0].
                                             neurons[self.selected_neuron-1].param.list[name])
            self.parameter_textbox[i].pack(side=tk.LEFT, padx=20)

            self.parameter_info.append(tk.Label(master=self.parameter_frame[i+3], text=name,
                                                bg=editframe_backcolor, fg=textcolor))
            self.parameter_info[i].pack(side=tk.LEFT)

    def show_connection_information(self):
        self.edit_drop_options = ["Connection Specific",
                                  "Connection Habituation",
                                  "Connection Sensitization",
                                  "Connection Presynaptic"]

        self.edit_drop_menu.destroy()
        self.edit_drop_menu = tk.OptionMenu(self.parameter_frame[2], self.edit_selection, *self.edit_drop_options,
                                            command=self.show_parameters)
        self.edit_drop_menu.config(bg=editframe_backcolor, width=self.editframe_width, fg=textcolor,
                                   borderwidth=0, highlightthickness=3, highlightbackground=highlight_color,
                                   activebackground=mainframe_backcolor)

        self.general_info.config(text="Connection Selected")
        self.id_info.config(text=f"ID: {self.selected_connection}")
        self.general_info.pack(side=tk.LEFT)
        self.id_info.pack(side=tk.LEFT)

        self.edit_drop_menu.pack(side=tk.LEFT)

        for i in range(0, len(self.parameter_info)):
            self.parameter_info[i].destroy()
        self.parameter_info.clear()
        for i in range(0, len(self.parameter_textbox)):
            self.parameter_textbox[i].destroy()
        self.parameter_textbox.clear()

        temp_param_list = connection_special_parameter

        if self.edit_selection.get() == self.edit_drop_options[0]:
            temp_param_list = connection_special_parameter
        elif self.edit_selection.get() == self.edit_drop_options[1]:
            temp_param_list = connection_habituation_parameter
        elif self.edit_selection.get() == self.edit_drop_options[2]:
            temp_param_list = connection_sensitization_parameter
        elif self.edit_selection.get() == self.edit_drop_options[3]:
            temp_param_list = connection_presynaptic_parameter

        for i, name in enumerate(temp_param_list):
            self.parameter_textbox.append(tk.Text(master=self.parameter_frame[i + 3], height=1, width=5,
                                                  bg=mainframe_backcolor, borderwidth=0,
                                                  highlightthickness=2, highlightbackground=highlight_color))

            self.parameter_textbox[i].insert("1.0", self.network_manager.networks[0].
                                             connections[self.selected_connection].param.list[name])
            self.parameter_textbox[i].pack(side=tk.LEFT, padx=20)

            self.parameter_info.append(tk.Label(master=self.parameter_frame[i+3], text=name,
                                                bg=editframe_backcolor, fg=textcolor))
            self.parameter_info[i].pack(side=tk.LEFT)

    def show_parameters(self, event=None):
        if not event:
            self.edit_selection.set(self.edit_drop_options[0])

        if self.selected_neuron > -1:
            self.show_neuron_information()
        elif self.selected_connection > -1:
            self.show_connection_information()
        else:
            self.show_network_information()

    def switch_tool_neurons(self):
        self.tool = TOOL_NEURONS
        self.neuron_button.configure(background=active_button_color)
        self.connection_button.configure(background=inactive_button_color)
        self.select_button.configure(background=inactive_button_color)
        self.discard_connection()
        self.deselect_neurons()
        self.deselect_connections()
        self.show_parameters()
        self.render_scene()

    def switch_tool_connections(self):
        self.tool = TOOL_CONNECTIONS
        self.neuron_button.configure(background=inactive_button_color)
        self.connection_button.configure(background=active_button_color)
        self.select_button.configure(background=inactive_button_color)
        self.deselect_neurons()
        self.deselect_connections()
        self.show_parameters()
        self.render_scene()

    def switch_tool_select(self):
        self.tool = TOOL_SELECT
        self.neuron_button.configure(background=inactive_button_color)
        self.connection_button.configure(background=inactive_button_color)
        self.select_button.configure(background=active_button_color)
        self.discard_connection()
        self.render_scene()

    def project_coordinate(self, coordinate, camera_axis):
        return (coordinate + camera_axis) * self.zoom_factor

    def reset_camera(self, event):
        self.camera_x = self.editorcanvas.winfo_width() / 2
        self.camera_y = self.editorcanvas.winfo_height() / 2
        self.zoom_factor = 1.0
        self.render_scene()

    def render_grid(self):
        temp_x = self.camera_x % self.grid_size
        temp_y = self.camera_y % self.grid_size

        if self.zoom_factor < 1:
            corrected_y = self.correct_zoom(self.editorcanvas.winfo_height())
            corrected_x = self.correct_zoom(self.editorcanvas.winfo_width())
        else:
            corrected_y = self.editorcanvas.winfo_height()*self.zoom_factor
            corrected_x = self.editorcanvas.winfo_width()*self.zoom_factor

        if self.camera_x > 0:
            temp_camera_x = self.camera_x
        else:
            temp_camera_x = -self.camera_x
        if self.camera_y > 0:
            temp_camera_y = self.camera_y
        else:
            temp_camera_y = -self.camera_y

        while temp_x < self.correct_zoom(self.editorcanvas.winfo_width()+temp_camera_x):
            self.editorcanvas.create_line(temp_x*self.zoom_factor, 0,
                                          temp_x*self.zoom_factor, corrected_y,
                                          fill=grid_color, width=2)
            temp_x = temp_x + self.grid_size

        while temp_y < self.correct_zoom(self.editorcanvas.winfo_height()+temp_camera_y):
            self.editorcanvas.create_line(0, temp_y*self.zoom_factor,
                                          corrected_x, temp_y*self.zoom_factor,
                                          fill=grid_color, width=2)
            temp_y = temp_y + self.grid_size

    def render_scene(self):
        self.editorcanvas.delete("all")

        if self.grid_snap:
            self.render_grid()

        for connection in self.network_manager.networks[0].connections:
            for vert in range(0, len(connection.vertices) - 1):
                if connection.id == self.selected_connection:
                    self.editorcanvas.create_line(self.project_coordinate(connection.vertices[vert][0], self.camera_x),
                                                  self.project_coordinate(connection.vertices[vert][1], self.camera_y),
                                                  self.project_coordinate(connection.vertices[vert + 1][0],
                                                                          self.camera_x),
                                                  self.project_coordinate(connection.vertices[vert + 1][1],
                                                                          self.camera_y),
                                                  fill=selected_connection_color, width=selected_connection_width)
                else:
                    self.editorcanvas.create_line(self.project_coordinate(connection.vertices[vert][0], self.camera_x),
                                                  self.project_coordinate(connection.vertices[vert][1], self.camera_y),
                                                  self.project_coordinate(connection.vertices[vert + 1][0], self.camera_x),
                                                  self.project_coordinate(connection.vertices[vert + 1][1], self.camera_y),
                                                  fill=connection_color, width=connection_width)

        for neuron in self.network_manager.networks[0].neurons:
            if self.selected_neuron == neuron.id:
                self.editorcanvas.create_image(self.project_coordinate(neuron.posx, self.camera_x),
                                               self.project_coordinate(neuron.posy, self.camera_y),
                                               image=self.img_neuron_selected)
            else:
                self.editorcanvas.create_image(self.project_coordinate(neuron.posx, self.camera_x),
                                               self.project_coordinate(neuron.posy, self.camera_y),
                                               image=self.img_default_neuron)
            self.editorcanvas.create_text(self.project_coordinate(neuron.posx, self.camera_x),
                                          self.project_coordinate(neuron.posy, self.camera_y),
                                          text=f"{neuron.id}", fill=viewframe_neurontext)

        self.editorcanvas.create_text(self.project_coordinate(0, self.camera_x),
                                      self.project_coordinate(0, self.camera_y),
                                      text="X", fill=mode_text_color, font="arial 15")

        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 15, anchor="w",
                                      text="Mode:", fill=viewframe_textcolor)
        if self.tool == TOOL_SELECT:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="SELECTING", fill=mode_text_color)
        elif self.tool == TOOL_NEURONS:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="NEURON EDITING", fill=mode_text_color)
        elif self.tool == TOOL_CONNECTIONS:
            self.editorcanvas.create_text(85, self.editorcanvas.winfo_height() - 15, anchor="w",
                                          text="CONNECTION EDITING", fill=mode_text_color)

        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 90, anchor="w",
                                      text=f"Camera X: {int(self.camera_x)}", fill=viewframe_textcolor)
        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 60, anchor="w",
                                      text=f"Camera Y: {int(self.camera_y)}", fill=viewframe_textcolor)

        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 175, anchor="w",
                                      text=f"Cursor X: {int(self.cursor_x)}", fill=viewframe_textcolor)
        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 145, anchor="w",
                                      text=f"Cursor Y: {int(self.cursor_y)}", fill=viewframe_textcolor)

        self.editorcanvas.create_text(self.editorcanvas.winfo_width() - 5, self.editorcanvas.winfo_height() - 15,
                                      anchor="e",
                                      text=f"Zoom: {round(self.zoom_factor * 100, 0)}%", fill=viewframe_textcolor)

        if self.grid_snap:
            self.editorcanvas.create_text(self.editorcanvas.winfo_width() - 5, self.editorcanvas.winfo_height() - 60,
                                          anchor="e", fill=mode_text_color,
                                          text="Grid Snap Active")

    def calc_cursor_collision(self, x, y, object):
        if x <= object.posx + self.correct_zoom(object.img_width / 2) and \
                x >= object.posx - self.correct_zoom(object.img_width / 2):
            if y <= object.posy + self.correct_zoom(object.img_height / 2) and \
                    y >= object.posy - self.correct_zoom(object.img_height / 2):
                return True
        return False

    def calc_rect_collision(self, cursor, bottom_left, top_right):
        if cursor[0] > bottom_left[0] and cursor[0] < top_right[0] and \
                cursor[1] < bottom_left[1] and cursor[1] > top_right[1]:
            return True
        return False

    def calc_vector(self, point_1, point_2):
        return np.array([point_2[0]-point_1[0], point_2[1]-point_1[1]])

    def unit_vector(self, vector):
        length = math.sqrt(math.pow(vector[0], 2) + math.pow(vector[1], 2))
        return np.array([vector[0]/length, vector[1]/length])

    def normal_vector(self, vector):
        return np.array([-vector[1], vector[0]])

    def uninormal_vector(self, vector):
        return self.unit_vector(self.normal_vector(vector))

    def get_rect_center(self, c1, c2, c3, c4):
        v1 = self.calc_vector(c1, c2) * 0.5
        v2 = self.calc_vector(c3, c1) * 0.5
        return c1 - v2 + v1

    def rotate_point(self, point, angle, origin):
        translated_point = point - origin
        temp = np.array([translated_point[0] * math.cos(angle) - translated_point[1] * math.sin(angle),
                         translated_point[0] * math.sin(angle) + translated_point[1] * math.cos(angle)])
        return temp + origin

    def get_vector_rotation(self, vector):
        coord_vector = np.array([1, 0])
        scalarproduct = (vector[0]*coord_vector[0]+vector[1]*coord_vector[1])
        absolute_vector = math.sqrt(vector[0]**2 + vector[1]**2)
        absolute_coord_vector = math.sqrt(coord_vector[0]**2 + coord_vector[1]**2)
        return math.acos(scalarproduct / (absolute_vector * absolute_coord_vector))

    def connection_cursor_collision(self, connection):
        for vert in range(0, len(connection.vertices) - 1):
            connection_bounding_box_width = 15
            uninormal_vector = np.array(self.calc_vector(connection.vertices[vert],
                                                         connection.vertices[vert + 1]))
            uninormal_vector = self.uninormal_vector(uninormal_vector)
            uninormal_vector = uninormal_vector * connection_bounding_box_width

            c = [connection.vertices[vert] + uninormal_vector,
                 connection.vertices[vert] - uninormal_vector,
                 connection.vertices[vert + 1] + uninormal_vector,
                 connection.vertices[vert + 1] - uninormal_vector]
            for i in range(0, len(c)):
                c[i][0] = self.project_coordinate(c[i][0], self.camera_x)
                c[i][1] = self.project_coordinate(c[i][1], self.camera_y)

            temp_angle = self.get_vector_rotation(np.array(self.calc_vector(c[0], c[2])))
            temp_origin = self.get_rect_center(c[0], c[1], c[2], c[3])
            temp_cursor = np.array([self.cursor_x + self.camera_x, self.cursor_y + self.camera_y])
            temp_cursor = temp_cursor * self.zoom_factor
            if connection.vertices[vert][1] < connection.vertices[vert + 1][1]:
                temp_angle = -temp_angle
            temp_cursor = self.rotate_point(temp_cursor, temp_angle, temp_origin)

            bottom_left = c[0]
            top_right = c[3]

            if self.calc_rect_collision(temp_cursor, self.rotate_point(bottom_left, temp_angle, temp_origin),
                                        self.rotate_point(top_right, temp_angle, temp_origin)):
                return True
        return False

    def correct_zoom(self, coord):
        return coord * 1 / self.zoom_factor

    def snap_cursor_to_grid(self):
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
        self.cursor_x = self.correct_zoom(event.x) - self.camera_x
        self.cursor_y = self.correct_zoom(event.y) - self.camera_y

    def get_cursor_position(self, event):
        self.get_free_cursor(event)
        self.render_scene()

        self.snap_cursor_to_grid()

    def add_neuron(self):
        neuron_x = self.cursor_x
        neuron_y = self.cursor_y

        self.network_manager.add_neuron(neuron_x, neuron_y, self.img_default_neuron)

    def init_connection(self, neuron):
        self.connecting_neuron = neuron
        self.do_connection = True

        self.network_manager.add_connection(neuron)
        connection_position = len(self.network_manager.networks[0].connections) - 1
        self.network_manager.networks[0].connections[connection_position].vertices.append(
            np.array([self.cursor_x,
                      self.cursor_y]))

    def draw_connection(self):
        if self.do_connection:
            self.render_scene()
            connection_position = len(self.network_manager.networks[0].connections) - 1
            vertex_position = len(self.network_manager.networks[0].connections[connection_position].vertices) - 1
            self.network_manager.networks[0].connections[connection_position].vertices[vertex_position] = [self.cursor_x,
                                                                                                           self.cursor_y]

    def discard_connection(self):
        if self.do_connection:
            connection_position = len(self.network_manager.networks[0].connections) - 1
            self.network_manager.delete_connection(connection_position)
            self.do_connection = False

    def deselect_neurons(self):
        self.selected_neuron = -1

    def deselect_connections(self):
        self.selected_connection = -1

    def escape_event(self, event):
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
            connection_position = len(self.network_manager.networks[0].connections) - 1
            for check_con in self.network_manager.networks[0].connections:
                if check_con.prev_neuron == self.network_manager.networks[0].connections[connection_position].prev_neuron \
                        and check_con.next_neuron == neuron.id:
                    can_connect = False
            if can_connect:
                vertex_position = len(self.network_manager.networks[0].connections[connection_position].vertices) - 1
                self.network_manager.networks[0].connections[connection_position].next_neuron = neuron.id
                self.network_manager.networks[0].connections[connection_position].vertices[vertex_position] = [
                    neuron.posx, neuron.posy]
            else:
                self.discard_connection()
            self.do_connection = False
        else:
            self.init_connection(neuron)

    def create_synaptic_connection(self, connection):
        if self.do_connection:
            if connection.id < len(self.network_manager.networks[0].connections) - 1:
                can_connect = True
                connection_position = len(self.network_manager.networks[0].connections) - 1
                for check_con in self.network_manager.networks[0].connections:
                    if check_con.prev_neuron == self.network_manager.networks[0].connections[connection_position].prev_neuron \
                            and check_con.next_connection == connection.id:
                        can_connect = False
                if can_connect:
                    vertex_position = len(self.network_manager.networks[0].connections[connection_position].vertices) - 1
                    self.network_manager.networks[0].connections[connection_position].next_connection = connection.id
                    self.network_manager.networks[0].connections[connection_position].vertices[vertex_position] = [
                        self.cursor_x, self.cursor_y]
                    print(self.network_manager.networks[0].connections[connection_position].next_connection)
                else:
                    self.discard_connection()
                self.do_connection = False

    def left_click(self, event):
        neuron_collision = False
        connection_collision = False
        for neuron in self.network_manager.networks[0].neurons:
            if self.calc_cursor_collision(self.cursor_x, self.cursor_y, neuron):
                if self.tool == TOOL_CONNECTIONS:
                    self.create_neuron_connection(neuron)
                elif self.tool == TOOL_SELECT:
                    self.deselect_connections()
                    self.selected_neuron = neuron.id
                    self.show_parameters()

                neuron_collision = True

        if not neuron_collision:
            for connection in self.network_manager.networks[0].connections:
                if self.connection_cursor_collision(connection):
                    if self.tool == TOOL_CONNECTIONS:
                        self.create_synaptic_connection(connection)

            if not self.do_connection:
                if self.tool == TOOL_NEURONS:
                    self.add_neuron()
            else:
                connection_position = len(self.network_manager.networks[0].connections) - 1
                self.network_manager.networks[0].connections[connection_position].vertices.append(
                    np.array([self.cursor_x, self.cursor_y]))
            if self.tool == TOOL_SELECT:
                self.deselect_neurons()
                self.show_parameters()

            if self.tool == TOOL_SELECT:
                for connection in self.network_manager.networks[0].connections:
                    self.deselect_neurons()
                    if self.connection_cursor_collision(connection):
                        self.selected_connection = connection.id
                        connection_collision = True
                if not connection_collision:
                    self.deselect_connections()
                self.show_parameters()

        self.render_scene()

    def motion_event(self, event):
        self.get_cursor_position(event)
        self.draw_connection()

    def delete_neuron(self):
        if self.tool == TOOL_NEURONS:
            for neuron in self.network_manager.networks[0].neurons:
                if self.calc_cursor_collision(self.cursor_x, self.cursor_y, neuron):
                    self.network_manager.delete_neuron(neuron.id)
            self.render_scene()

    def delete_connection(self):
        if self.tool == TOOL_CONNECTIONS and not self.do_connection:
            for connection in self.network_manager.networks[0].connections:
                if self.connection_cursor_collision(connection):
                    self.network_manager.delete_connection(connection.id)
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

        self.camera_x = self.camera_x - self.correct_zoom(self.next_wheel_pos_x - self.prev_wheel_pos_x)
        self.camera_y = self.camera_y - self.correct_zoom(self.next_wheel_pos_y - self.prev_wheel_pos_y)

        self.next_wheel_pos_x = event.x
        self.next_wheel_pos_y = event.y

        self.render_scene()

    def zoom_scene(self, event):
        self.get_free_cursor(event)
        old_cursor_x = self.cursor_x
        old_cursor_y = self.cursor_y

        if event.num == 4 or event.delta == 120:
            if self.zoom_factor < 4.0:
                self.zoom_factor = self.zoom_factor + 0.1
        if event.num == 5 or event.delta == -120:
            if self.zoom_factor > 0.2:
                self.zoom_factor = self.zoom_factor - 0.1

        self.get_free_cursor(event)
        self.camera_x = self.camera_x - (old_cursor_x - self.cursor_x)
        self.camera_y = self.camera_y - (old_cursor_y - self.cursor_y)

        self.get_cursor_position(event)

        self.render_scene()
