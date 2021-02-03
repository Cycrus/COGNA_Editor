from params import *

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

        self.root_frame = root
        self.network_manager = network_manager

        self.img_default_neuron = ImageTk.PhotoImage(Image.open("default_neuron.png"))

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
                                  width=editframe_width,
                                  relief=tk.FLAT)
        self.editframe.grid_columnconfigure(0, weight=1)

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

        self.mainframe.pack(side=tk.TOP, fill=tk.BOTH, padx=0, pady=0, expand=True)
        self.editframe.pack(side=tk.LEFT, fill=tk.BOTH, padx=0, pady=0, expand=False)
        self.viewframe.pack(side=tk.LEFT, fill=tk.BOTH, padx=0, pady=0, expand=True)
        self.editorcanvas.pack(side=tk.RIGHT, fill=tk.BOTH, padx=0, pady=0, expand=True)

        self.root_frame.update()
        self.render_scene()

        self.do_connection = False
        self.connecting_neuron = None

        self.editorcanvas.bind("<Motion>", self.get_cursor_position)

        self.editorcanvas.bind("<Button-2>", self.init_camera)
        self.editorcanvas.bind("<B2-Motion>", self.move_camera)
        self.editorcanvas.bind("<Button-1>", self.left_click)
        self.editorcanvas.bind("<B1-Motion>", self.draw_connection)
        self.editorcanvas.bind("<ButtonRelease-1>", self.create_connection)
        self.editorcanvas.bind("<Button-3>", self.delete_neuron)
        # Windows Mouse Wheel
        self.editorcanvas.bind("<MouseWheel>", self.zoom_scene)
        # Linux Mouse Wheel
        self.editorcanvas.bind("<Button-4>", self.zoom_scene)
        self.editorcanvas.bind("<Button-5>", self.zoom_scene)

    def render_scene(self):
        self.editorcanvas.delete("all")
        for neuron in self.network_manager.networks[0].neurons:
            self.editorcanvas.create_image((neuron.posx + self.camera_x)*self.zoom_factor,
                                           (neuron.posy + self.camera_y)*self.zoom_factor,
                                           image=neuron.image)

            self.img_default_neuron = ImageTk.PhotoImage(Image.open("default_neuron.png"))

        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 45, anchor="w",
                                      text=f"X:{self.camera_x}", fill=viewframe_textcolor)
        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 15, anchor="w",
                                      text=f"Y:{self.camera_y}", fill=viewframe_textcolor)

        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 130, anchor="w",
                                      text=f"X:{self.cursor_x}", fill=viewframe_textcolor)
        self.editorcanvas.create_text(5, self.editorcanvas.winfo_height() - 100, anchor="w",
                                      text=f"Y:{self.cursor_y}", fill=viewframe_textcolor)

        self.editorcanvas.create_text(self.editorcanvas.winfo_width()-5, self.editorcanvas.winfo_height()-15, anchor="e",
                                      text=f"Zoom:{round(self.zoom_factor*100, 0)}%", fill=viewframe_textcolor)

    def calc_cursor_collision(self, cursor, object):
        if self.correct_zoom(cursor.x) - self.camera_x <= object.posx + object.img_width / 2 and \
                self.correct_zoom(cursor.x) - self.camera_x >= object.posx - object.img_width / 2:
            if self.correct_zoom(cursor.y) - self.camera_y <= object.posy + object.img_height / 2 and \
                    self.correct_zoom(cursor.y) - self.camera_y >= object.posy - object.img_height / 2:
                return True
        return False

    def correct_zoom(self, coord):
        return coord * 1/self.zoom_factor

    def get_cursor_position(self, event):
        self.cursor_x = int(self.correct_zoom(event.x))
        self.cursor_y = int(self.correct_zoom(event.y))
        self.render_scene()

    def add_neuron(self, event):
            self.network_manager.add_neuron(self.correct_zoom(event.x) - self.camera_x,
                                            self.correct_zoom(event.y) - self.camera_y, self.img_default_neuron)
            self.render_scene()
        
    def init_connection(self, event, neuron):
        self.connecting_neuron = neuron
        self.do_connection = True

    def draw_connection(self, event):
        if self.do_connection:
            self.render_scene()
            self.editorcanvas.create_line(self.connecting_neuron.posx*self.zoom_factor-self.camera_x,
                                          self.connecting_neuron.posy*self.zoom_factor-self.camera_y,
                                          event.x, event.y, fill=connection_color,
                                          width=connection_width)

    def create_connection(self, event):
        if self.do_connection:
            for neuron in self.network_manager.networks[0].neurons:
                if self.calc_cursor_collision(event, neuron):
                    print("creating connection")
        self.do_connection = False
        self.connecting_neuron = None
        self.render_scene()

    def left_click(self, event):
        can_place = True
        for neuron in self.network_manager.networks[0].neurons:
            if self.calc_cursor_collision(event, neuron):
                self.init_connection(event, neuron)
                can_place = False

        if can_place:
            self.add_neuron(event)

    def delete_neuron(self, event):
        for neuron in self.network_manager.networks[0].neurons:
            if self.calc_cursor_collision(event, neuron):
                self.network_manager.delete_neuron(neuron.id)
        self.render_scene()

    def init_camera(self, event):
        self.prev_wheel_pos_x = event.x
        self.prev_wheel_pos_y = event.y
        self.next_wheel_pos_x = event.x
        self.next_wheel_pos_y = event.y

    def move_camera(self, event):
        self.prev_wheel_pos_x = event.x
        self.prev_wheel_pos_y = event.y

        self.camera_x = self.camera_x + (self.next_wheel_pos_x - self.prev_wheel_pos_x)
        self.camera_y = self.camera_y + (self.next_wheel_pos_y - self.prev_wheel_pos_y)

        self.render_scene()

        self.next_wheel_pos_x = event.x
        self.next_wheel_pos_y = event.y

    def zoom_scene(self, event):
        if event.num == 4 or event.delta == 120:
            if self.zoom_factor < 2.0:
                self.zoom_factor = self.zoom_factor + 0.01
        if event.num == 5 or event.delta == -120:
            if self.zoom_factor > 0.1:
                self.zoom_factor = self.zoom_factor - 0.01

        self.render_scene()
