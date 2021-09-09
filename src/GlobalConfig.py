"""
GlobalConfig.py

The settings of the dialog window for global settings of a projects.

Author: Cyril Marx
Date: 09.09.2021
"""

from src.GlobalLibraries import *
from src.NetworkManager import NetworkManager


class GlobalConfig:
    def __init__(self, root, network_manager):
        """
        Constructor. Builds the tkinter window for global settings.
        :param root:            The root window of tkinter, where every other window is placed on.
        :param network_manager: The network manager, which handles all networks and projects.
        :return:                None
        """
        self.root_frame = root
        self.network_manager = network_manager
        self.frame_number = 30

        self.width = self.root_frame.winfo_screenwidth() // 3
        self.height = self.root_frame.winfo_screenheight() // 4
        self.pos_x = self.root_frame.winfo_screenwidth() // 2 - self.width // 2
        self.pos_y = self.root_frame.winfo_screenheight() // 2 - self.height // 2
        self.top_frame = tk.Toplevel()
        self.top_frame.grab_set()
        self.top_frame.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")
        self.top_frame.overrideredirect(True)
        self.top_frame.configure(background=design.grey_4[design.theme], highlightthickness=4,
                                         highlightbackground=design.grey_2[design.theme])
        self.top_frame.update()

        self.label_frame = tk.Frame(master=self.top_frame, background=design.dark_blue[design.theme],
                                    borderwidth=0,
                                    highlightthickness=2,
                                    highlightbackground=design.grey_2[design.theme],
                                    height=self.top_frame.winfo_height() // 7,
                                    width=self.top_frame.winfo_width())
        self.label_frame.pack(side=tk.TOP, fill=tk.X)
        self.label = tk.Label(master=self.label_frame, background=design.dark_blue[design.theme],
                              text="Global Configurations",
                              fg=design.grey_c[design.theme])
        self.label.pack(pady=5)

        self.editor = tk.Frame(master=self.top_frame, background=design.grey_4[design.theme],
                               borderwidth=0,
                               highlightthickness=0,
                               height=self.top_frame.winfo_height() - (self.label_frame.winfo_height() * 2),
                               width=self.top_frame.winfo_width())
        self.editor.pack(side=tk.TOP, fill=tk.BOTH)

        self.edit_frames = []
        for idx in range(0, self.frame_number):
            self.edit_frames.append(tk.Frame(master=self.editor, background=design.grey_4[design.theme], borderwidth=0,
                                             highlightthickness=0))
            self.edit_frames[idx].pack(side=tk.TOP, anchor="w")
        self.edit_labels = []
        self.edit_widgets = []

        self.button_space = tk.Frame(master=self.top_frame, background=design.grey_4[design.theme],
                                     borderwidth=0,
                                     highlightthickness=0,
                                     height=self.top_frame.winfo_height() // 8,
                                     width=self.top_frame.winfo_width())
        self.button_space.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        self.close_button = tk.Button(master=self.button_space, text="Discard",
                                      background=design.grey_3[design.theme],
                                      fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                      command=lambda x=False: self.close_window(x))
        self.save_button = tk.Button(master=self.button_space, text="Save & Close",
                                     background=design.grey_3[design.theme],
                                     fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                     command=lambda x=True: self.close_window(x))
        self.close_button.pack(side=tk.LEFT, padx=20, pady=5)
        self.save_button.pack(side=tk.RIGHT, padx=20, pady=5)

        self.main_network_menu = None
        self.main_network_label = None
        self.fps_entry = None
        self.fps_label = None

        self.network_list = self.network_manager.get_network_list()
        self.main_network_option = tk.StringVar()
        self.main_network_option.set(self.network_manager.main_network)
        if self.main_network_option.get() not in self.network_list:
            self.main_network_option.set(self.network_list[0])

        self.render_editor()

    def render_editor(self):
        """
        Renders the contents of the widgets in the window.
        :return:    None
        """
        self.main_network_menu = tk.OptionMenu(self.edit_frames[0], self.main_network_option,
                                               *self.network_list)
        self.main_network_menu.config(bg=design.grey_4[design.theme], width=20,
                                      fg=design.grey_c[design.theme],
                                      borderwidth=0, highlightthickness=3,
                                      highlightbackground=design.grey_2[design.theme],
                                      activebackground=design.grey_7[design.theme])
        self.main_network_label = tk.Label(master=self.edit_frames[0], text="Main Network",
                                           bg=design.grey_4[design.theme], fg=design.grey_c[design.theme])

        self.main_network_menu.pack(side=tk.LEFT, padx=20, pady=10)
        self.main_network_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.fps_entry = tk.Entry(master=self.edit_frames[1], width=15,
                                  bg=design.grey_7[design.theme], borderwidth=0, fg=design.black[design.theme],
                                  highlightthickness=2, highlightbackground=design.grey_2[design.theme])
        self.fps_entry.insert(tk.END, str(self.network_manager.frequency))
        self.fps_label = tk.Label(master=self.edit_frames[1], text="Frequency of Network",
                                  bg=design.grey_4[design.theme], fg=design.grey_c[design.theme])

        self.fps_entry.pack(side=tk.LEFT, padx=20, pady=10)
        self.fps_label.pack(side=tk.LEFT, padx=20, pady=10)

    def close_window(self, save):
        """
        Closes the window down and saves the contents of widgets/settings if save button is pressed.
        :param save:    A boolean. If true, the content of the widgets is saved.
        :return:        None
        """
        if save:
            self.network_manager.main_network = self.main_network_option.get()
            self.network_manager.frequency = self.fps_entry.get()

        for idx, frame in enumerate(self.edit_frames):
            frame.destroy()

        self.edit_widgets.clear()
        self.top_frame.grab_release()
        self.network_manager.save_global_info()
        self.top_frame.destroy()

