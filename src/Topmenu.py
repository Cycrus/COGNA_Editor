from src.GlobalLibraries import *
from src.Mainframe import *

# Good Tutorial: https://pythonguides.com/python-tkinter-menu-bar/


class Topmenu:
    def __init__(self, root, network_manager, mainframe):
        self.root_frame = root
        self.network_manager = network_manager
        self.mainframe = mainframe

        self.tabframe = tk.Frame(master=root, background=editframe_backcolor,
                                 borderwidth=0,
                                 highlightthickness=0,
                                 highlightbackground=highlight_color,
                                 height=tabframe_height,
                                 width=root.winfo_width())

        self.tablist = []
        self.tabframe.pack()
        self.create_tab(0)

        self.menubar = tk.Menu(master=self.root_frame, background=topmenu_backcolor, foreground=top_button_textcolor,
                               activebackground=active_button_color, activeforeground=textcolor, borderwidth=0,
                               relief=tk.RIDGE)
        self.file = tk.Menu(master=self.menubar, tearoff=0, background=topmenu_backcolor,
                            foreground=top_button_textcolor, activebackground=active_button_color,
                            activeforeground=textcolor, borderwidth=1, relief=tk.RIDGE)
        self.file.add_command(label="New        <ctr-n>", command=self.new_command)
        self.file.add_separator()
        self.file.add_command(label="Open       <ctr-o>", command=self.open_command)
        self.file.add_command(label="Import     <ctr-i>", command=self.import_command)
        self.file.add_separator()
        self.file.add_command(label="Save        <ctr-s>", command=self.save_command)
        self.file.add_command(label="Save as", command=self.save_as_command)
        self.file.add_separator()
        self.file.add_command(label="Close File  <ctr-w>", command=self.close_command)
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
        self.view.add_command(label="Snap to Grid    <g>", command=self.grid_command)
        self.view.add_command(label="Reset View      <space>", command=self.reset_view_command)
        self.menubar.add_cascade(label="View", menu=self.view)

        self.help = tk.Menu(master=self.menubar, tearoff=0, background=topmenu_backcolor,
                            foreground=top_button_textcolor, activebackground=active_button_color,
                            activeforeground=textcolor, borderwidth=1, relief=tk.RIDGE)
        self.help.add_command(label="About COGNA Editor", command=self.show_about)
        self.help.add_command(label="Help", command=self.show_help)
        self.help.add_command(label="Controls", command=self.show_controls)
        self.menubar.add_cascade(label="Help", menu=self.help)

        self.root_frame.config(menu=self.menubar)

        self.root_frame.bind("<Control-Left>", self.prev_network)
        self.root_frame.bind("<Control-Right>", self.next_network)
        self.root_frame.bind("<Control-n>", self.new_command)
        self.root_frame.bind("<Control-w>", self.close_command)
        self.root_frame.bind("<Control-s>", self.save_command)

    def create_tab(self, network_id):
        self.tablist.append([tk.Frame(master=self.tabframe, background=editframe_backcolor,
                                      borderwidth=0,
                                      highlightthickness=1,
                                      highlightbackground=highlight_color,
                                      height=tabframe_height,
                                      width=1),
                            network_id])
        tabcount = len(self.tablist)
        for tab in self.tablist:
            tab[0].config(width=self.root_frame.winfo_width()/tabcount)
            tab[0].grid(row=0, column=tab[1])
            tab[0].unbind("<Button-1>")
            tab[0].bind("<Button-1>", self.click_tab)

    def click_tab(self, event=None):
        for tab in self.tablist:
            if event.widget == tab[0]:
                print(tab[1])
                self.show_specific_network(tab[1])
                break

    def prev_network(self, event=None):
        self.network_manager.curr_network = self.network_manager.curr_network - 1
        if self.network_manager.curr_network < 0:
            self.network_manager.curr_network = len(self.network_manager.networks)-1
        self.mainframe.render_scene()
        self.mainframe.show_parameters(store=True)

    def next_network(self, event=None):
        self.network_manager.curr_network = self.network_manager.curr_network + 1
        if self.network_manager.curr_network > len(self.network_manager.networks)-1:
            self.network_manager.curr_network = 0
        self.mainframe.render_scene()
        self.mainframe.show_parameters(store=True)

    def show_specific_network(self, network_id):
        print(network_id)
        self.network_manager.curr_network = network_id
        self.mainframe.render_scene()
        self.mainframe.show_parameters(store=True)

    def new_command(self, event=None):
        self.network_manager.add_network()
        self.mainframe.reset_camera()
        self.mainframe.render_scene()
        self.mainframe.show_parameters(store=True)
        self.create_tab(self.network_manager.curr_network)

    def open_command(self):
        print("Open file")

    def import_command(self):
        print("Import network")

    def save_command(self, event=None):
        self.network_manager.save_network(save_as=False)

    def save_as_command(self, event=None):
        self.network_manager.save_network(save_as=True)

    def close_command(self, event=None):
        if len(self.network_manager.networks) > 0:
            self.network_manager.clear_single_network(self.network_manager.curr_network)
        self.mainframe.reset_camera()
        self.mainframe.render_scene()

    def grid_command(self):
        self.mainframe.toggle_grid_snap(None)

    def reset_view_command(self):
        self.mainframe.reset_camera(None)

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
