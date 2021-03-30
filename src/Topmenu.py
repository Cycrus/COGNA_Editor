from src.GlobalLibraries import *

# Good Tutorial: https://pythonguides.com/python-tkinter-menu-bar/


class Topmenu:
    def __init__(self, root, network_manager):
        self.root_frame = root
        self.network_manager = network_manager

        file_menu = ["New", "Save", "Open", "Import"]
        edit_menu = ["Work", "In", "Progress"]
        view_menu = ["View Grid", "Snap to Grid"]
        help_menu = ["About COGNA Editor", "Controls"]

        self.topmenu = tk.Frame(master=root, background=topmenu_backcolor,
                                borderwidth=0,
                                highlightthickness=1,
                                width=root.winfo_width(),
                                height=topmenu_height,
                                highlightbackground=highlight_color)
        self.topmenu.grid_columnconfigure(0, weight=1)

        self.button_file = tk.Button(master=self.topmenu, text="File",
                                     background=topmenu_backcolor,
                                     fg=top_button_textcolor,
                                     width=top_button_width,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     activebackground=mainframe_backcolor)

        self.button_edit = tk.Button(master=self.topmenu, text="Edit",
                                     background=topmenu_backcolor,
                                     fg=top_button_textcolor,
                                     width=top_button_width,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     activebackground=mainframe_backcolor)

        self.button_view = tk.Button(master=self.topmenu, text="View",
                                     background=topmenu_backcolor,
                                     fg=top_button_textcolor,
                                     width=top_button_width,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     activebackground=mainframe_backcolor)

        self.button_help = tk.Button(master=self.topmenu, text="Help",
                                     background=topmenu_backcolor,
                                     fg=top_button_textcolor,
                                     width=top_button_width,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     activebackground=mainframe_backcolor)

        self.topmenu.pack(side=tk.TOP, fill=tk.BOTH, padx=0, pady=0, expand=False)
