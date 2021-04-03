from src.GlobalLibraries import *
from src.NetworkManager import NetworkManager

class TransmitterConfigurator:
    def __init__(self, root, transmitter_list, network_manager):
        self.root_frame = root
        self.transmitter_list = transmitter_list
        self.network_manager = network_manager
        self.frame_number = 30

        self.width = self.root_frame.winfo_width() // 3
        self.height = self.root_frame.winfo_height() // 2
        self.pos_x = self.root_frame.winfo_width() // 2 - self.width // 2 + self.root_frame.winfo_x()
        self.pos_y = self.root_frame.winfo_height() // 2 - self.height // 2 + self.root_frame.winfo_y()
        self.transmitter_frame = tk.Toplevel()
        self.transmitter_frame.grab_set()
        self.transmitter_frame.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")
        self.transmitter_frame.overrideredirect(True)
        self.transmitter_frame.configure(background=grey_4, highlightthickness=4,
                                         highlightbackground=grey_2)
        self.transmitter_frame.update()

        self.label_frame = tk.Frame(master=self.transmitter_frame, background=dark_blue,
                                    borderwidth=0,
                                    highlightthickness=2,
                                    highlightbackground=grey_2,
                                    height=self.transmitter_frame.winfo_height() // 7,
                                    width=self.transmitter_frame.winfo_width())
        self.label_frame.pack(side=tk.TOP, fill=tk.X)
        self.label = tk.Label(master=self.label_frame, background=dark_blue, text="Neurotransmitter Configuration",
                              fg=grey_c)
        self.label.pack()
        self.transmitter_frame.update()

        self.editor = tk.Frame(master=self.transmitter_frame, background=grey_4,
                               borderwidth=0,
                               highlightthickness=0,
                               height=self.transmitter_frame.winfo_height() - (self.label_frame.winfo_height() * 2),
                               width=self.transmitter_frame.winfo_width())
        self.editor.pack(side=tk.TOP, fill=tk.BOTH)

        self.edit_frames = []
        for idx in range(0, self.frame_number):
            self.edit_frames.append(tk.Frame(master=self.editor, background=grey_4, borderwidth=0,
                                    highlightthickness=0))
            self.edit_frames[idx].pack(side=tk.TOP)
        self.edit_widgets = []

        self.render_editor()

        self.button_space = tk.Frame(master=self.transmitter_frame, background=grey_4,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     height=self.transmitter_frame.winfo_height() // 8,
                                     width=self.transmitter_frame.winfo_width())
        self.button_space.pack(side=tk.TOP, fill=tk.X)

        self.save_button = tk.Button(master=self.button_space, text="Save", background=grey_3,
                                     fg=grey_c, activebackground=grey_7,
                                     command=lambda: self.close_window(save=True))
        self.save_button.pack(side=tk.LEFT, padx=self.transmitter_frame.winfo_width()/7)

        self.close_button = tk.Button(master=self.button_space, text="Close", background=grey_3,
                                      fg=grey_c, activebackground=grey_7,
                                      command=lambda: self.close_window(save=False))
        self.close_button.pack(side=tk.RIGHT, padx=self.transmitter_frame.winfo_width()/7)

    def __del__(self):
        self.close_window()

    def render_editor(self):
        for widget in self.edit_widgets:
            if widget[0] is not None:
                widget[0].forget()
            if widget[1] is not None:
                widget[1].forget()
        self.edit_widgets.clear()

        for idx, tran in enumerate(self.transmitter_list):
            if idx > 0:
                textcol = black
            else:
                textcol = grey_4
            temp_textbox = tk.Text(master=self.edit_frames[idx], height=1, width=15,
                                   bg=grey_7, borderwidth=0, fg=textcol,
                                   highlightthickness=2, highlightbackground=grey_2)
            temp_textbox.insert("1.0", tran)
            temp_button = tk.Button(master=self.edit_frames[idx], text="Delete", background=grey_3,
                                    fg=grey_c, activebackground=grey_7,
                                    command=lambda i=idx: self.delete_transmitter(trans_index=i))
            self.edit_widgets.append([temp_textbox, temp_button])

        self.edit_widgets.append([tk.Button(master=self.edit_frames[len(self.transmitter_list)],
                                 text="Add Transmitter", background=grey_3,
                                 fg=grey_c, activebackground=grey_7,
                                 command=self.add_transmitter), None])

        for widget in self.edit_widgets:
            if widget[0] is not None:
                widget[0].pack(side=tk.LEFT, padx=20, pady=10)
            if widget[1] is not None:
                widget[1].pack(side=tk.LEFT, padx=0, pady=10)

    def store_transmitter(self):
        for idx, tran in enumerate(self.transmitter_list):
            if idx > 0:
                temp_tran = self.edit_widgets[idx][0].get("1.0", "end").replace("\n", "").replace(" ", "")
            else:
                temp_tran = "Default"
            self.transmitter_list[idx] = temp_tran
        self.render_editor()

    def add_transmitter(self):
        self.store_transmitter()
        self.transmitter_list.append("")
        self.render_editor()

    def delete_transmitter(self, trans_index):
        self.store_transmitter()
        self.transmitter_list.pop(trans_index)
        self.render_editor()

    def close_window(self, save=False):
        if save:
            self.store_transmitter()
            temp_list = []
            for idx, trans in enumerate(self.transmitter_list):
                if trans:
                    can_save = True
                    for test_tran in range(0, idx):
                        if trans == self.transmitter_list[test_tran]:
                            can_save = False
                    if can_save:
                        temp_list.append(trans)
            self.network_manager.transmitters = temp_list

        for idx, frame in enumerate(self.edit_frames):
            frame.destroy()

        self.edit_widgets.clear()
        self.transmitter_frame.grab_release()
        self.transmitter_frame.destroy()