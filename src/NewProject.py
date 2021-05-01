from src.GlobalLibraries import *
from src.NetworkManager import NetworkManager


class NewProject:
    def __init__(self, root, network_manager, mainframe):
        self.root_frame = root
        self.network_manager = network_manager
        self.mainframe = mainframe

        self.width = self.root_frame.winfo_screenwidth() // 4
        self.height = self.root_frame.winfo_screenheight() // 8
        self.pos_x = self.root_frame.winfo_screenwidth() // 2 - self.width // 2
        self.pos_y = self.root_frame.winfo_screenheight() // 2 - self.height // 2

        self.topframe = tk.Toplevel()
        self.topframe.grab_set()
        self.topframe.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")
        self.topframe.overrideredirect(True)
        self.topframe.configure(background=design.grey_4[design.theme], highlightthickness=4,
                                highlightbackground=design.grey_2[design.theme])
        self.topframe.update()

        self.entry_frame = tk.Frame(master=self.topframe, background=design.grey_4[design.theme],
                                    borderwidth=0,
                                    highlightthickness=0,
                                    height=self.topframe.winfo_height() // 2,
                                    width=self.topframe.winfo_width())
        self.entry_frame.pack(side=tk.TOP, fill=tk.X)

        self.name_label = tk.Label(master=self.entry_frame, background=design.grey_4[design.theme],
                                   borderwidth=0, text="Project Name")
        self.name_label.pack(side=tk.TOP, pady=20)

        self.name_entry = tk.Entry(master=self.entry_frame, width=30,
                                   bg=design.grey_7[design.theme], borderwidth=0,
                                   highlightthickness=2, highlightbackground=design.grey_2[design.theme])
        self.name_entry.pack(side=tk.TOP)
        self.topframe.update()

        self.button_frame = tk.Frame(master=self.topframe, background=design.grey_4[design.theme],
                                     borderwidth=0,
                                     highlightthickness=0,
                                     height=self.topframe.winfo_height() // 2,
                                     width=self.topframe.winfo_width())
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.cancel_button = tk.Button(master=self.button_frame, text="Close", background=design.grey_3[design.theme],
                                       fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                       command=lambda: self.close_window(save=False))
        self.cancel_button.pack(side=tk.LEFT, pady=20, padx=20)

        self.create_button = tk.Button(master=self.button_frame, text="Create", background=design.grey_3[design.theme],
                                       fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                       command=lambda: self.close_window(save=True))
        self.create_button.pack(side=tk.RIGHT, pady=20, padx=20)

    def project_is_unique(self, project_name):
        existing_projects = os.listdir(os.getcwd() + os.sep + "Projects")
        return not project_name in existing_projects

    def close_window(self, save=False):
        can_close = True
        if save:
            project_name = self.name_entry.get()
            if not project_name:
                can_close = False
            elif not self.project_is_unique(project_name):
                can_close = False
            else:
                self.network_manager.new_project(project_name)
                self.network_manager.clear_all_networks()

        if can_close:
            self.topframe.grab_release()
            self.network_manager.save_transmitters()
            self.mainframe.show_editmenu(store=False)
            self.topframe.destroy()
