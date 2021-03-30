from src.GlobalLibraries import *

# Good Tutorial: https://pythonguides.com/python-tkinter-menu-bar/


class Topmenu:
    def __init__(self, root, network_manager):
        self.root_frame = root
        self.network_manager = network_manager

        self.topmenu = tk.Frame(master=root, background=topmenu_backcolor,
                                borderwidth=0,
                                highlightthickness=1,
                                width=root.winfo_width(),
                                height=topmenu_height,
                                highlightbackground=highlight_color)
        self.topmenu.grid_columnconfigure(0, weight=1)

        self.menubar = tk.Menu(master=self.topmenu, background=topmenu_backcolor, foreground=top_button_textcolor,
                               activebackground=active_button_color, activeforeground=textcolor, borderwidth=0,
                               relief=tk.RIDGE)
        self.file = tk.Menu(master=self.menubar, tearoff=0, background=topmenu_backcolor,
                            foreground=top_button_textcolor, activebackground=active_button_color,
                            activeforeground=textcolor, borderwidth=1, relief=tk.RIDGE)
        self.file.add_command(label="New        <ctr-w>", command=self.new_command)
        self.file.add_separator()
        self.file.add_command(label="Open       <ctr-o>", command=self.open_command)
        self.file.add_command(label="Import     <ctr-i>", command=self.import_command)
        self.file.add_separator()
        self.file.add_command(label="Save        <ctr-s>", command=self.save_command)
        self.file.add_command(label="Save as   <ctr-alt-s>", command=self.save_as_command)
        self.file.add_separator()
        self.file.add_command(label="Exit", command=self.root_frame.quit)
        self.menubar.add_cascade(label="File", menu=self.file)

        self.edit = tk.Menu(master=self.menubar, tearoff=0, background=topmenu_backcolor,
                            foreground=top_button_textcolor, activebackground=active_button_color,
                            activeforeground=textcolor, borderwidth=1, relief=tk.RIDGE)
        self.edit.add_command(label="Undo     <ctr-z>")
        self.edit.add_command(label="Redo     <ctr-y>")
        self.edit.add_separator()
        self.edit.add_command(label="Cut        <ctr-x>")
        self.edit.add_command(label="Copy      <ctr-c>")
        self.edit.add_command(label="Paste     <ctr-v>")
        self.edit.add_separator()
        self.edit.add_command(label="Neuron Type Config")
        self.edit.add_command(label="Transmitter Config")
        self.menubar.add_cascade(label="Edit", menu=self.edit)

        self.view = tk.Menu(master=self.menubar, tearoff=0, background=topmenu_backcolor,
                            foreground=top_button_textcolor, activebackground=active_button_color,
                            activeforeground=textcolor, borderwidth=1, relief=tk.RIDGE)
        self.view.add_command(label="Snap to Grid    <g>")
        self.view.add_command(label="Reset View      <space>")
        self.menubar.add_cascade(label="View", menu=self.view)

        self.help = tk.Menu(master=self.menubar, tearoff=0, background=topmenu_backcolor,
                            foreground=top_button_textcolor, activebackground=active_button_color,
                            activeforeground=textcolor, borderwidth=1, relief=tk.RIDGE)
        self.help.add_command(label="About COGNA Editor", command=self.show_about)
        self.help.add_command(label="Help", command=self.show_help)
        self.help.add_command(label="Controls", command=self.show_controls)
        self.menubar.add_cascade(label="Help", menu=self.help)

        self.root_frame.config(menu=self.menubar)

        self.topmenu.pack(side=tk.TOP, fill=tk.BOTH, padx=0, pady=0, expand=False)

    def new_command(self):
        print("New file")

    def open_command(self):
        print("Open file")

    def import_command(self):
        print("Import network")

    def save_command(self):
        print("Save file")

    def save_as_command(self):
        print("Save file as")

    def show_about(self):
        messagebox.showinfo('About COGNA Editor',
                            'Editor for constructing COGNA network architectures.\n'
                            'Author: Cyril Marx\n'
                            'Copyright (c) by Cyril Marx 2021')

    def show_help(self):
        messagebox.showinfo("Help for COGNA Editor",
                            "Help for COGNA Editor")

    def show_controls(self):
        messagebox.showinfo("Controls of COGNA Editor",
                            "Select tool with top left buttons [S][N][C]:\n"
                            "   [S] Select and control parameters\n"
                            "   [N] Add and manipulate neurons\n"
                            "   [C] Add and manipulate connections")
