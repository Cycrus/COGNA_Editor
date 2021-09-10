"""
Topmenu.py

Controls the menu at the top of the window and a lot of project operations.

Author: Cyril Marx
Date: 09.09.2021
"""

from src.GlobalLibraries import *
from src.Mainframe import *
from src.TransmitterConfigurator import TransmitterConfigurator
from src.NeuronConfigurator import NeuronConfigurator
from src.SpashScreen import SplashScreen
from src.NewProject import NewProject
from src.GlobalConfig import GlobalConfig

# Good Tutorial: https://pythonguides.com/python-tkinter-menu-bar/


class Topmenu:
    def __init__(self, root, network_manager, mainframe):
        """
        Constructor. Creates the menu.
        :param root:            The tkinter root frame.
        :param network_manager: The network manager object of the program.
        :param mainframe:       The mainframe of the program.
        :return:                None
        """
        self.root_frame = root
        self.network_manager = network_manager
        self.mainframe = mainframe

        self.tabframe = tk.Frame(master=root, background=design.grey_4[design.theme],
                                 borderwidth=0,
                                 highlightthickness=0,
                                 highlightbackground=design.grey_2[design.theme],
                                 width=root.winfo_width())

        self.tablist = []
        self.tablabel = []
        self.tabframe.pack()
        self.create_tab(0)

        self.menubar = tk.Menu(master=self.root_frame, background=design.grey_4[design.theme], foreground=design.grey_c[design.theme],
                               activebackground=design.dark_blue[design.theme], activeforeground=design.grey_c[design.theme], borderwidth=0,
                               relief=tk.RIDGE)
        self.file = tk.Menu(master=self.menubar, tearoff=0, background=design.grey_4[design.theme],
                            foreground=design.grey_c[design.theme], activebackground=design.dark_blue[design.theme],
                            activeforeground=design.grey_c[design.theme], borderwidth=1, relief=tk.RIDGE)

        self.file.add_command(label="New Project", command=self.new_project_command)
        self.file.add_command(label="Save Project")
        self.file.add_command(label="Open Project", command=self.open_project_command)
        self.file.add_separator()
        self.file.add_command(label="New Network    <ctr-n>", command=self.new_command)
        self.file.add_command(label="Save Network     <ctr-s>", command=self.save_command)
        self.file.add_command(label="Save Network as", command=self.save_as_command)
        self.file.add_command(label="Open Network   <ctr-o>", command=self.open_command)
        self.file.add_command(label="Import Network <ctr-i>", command=self.import_command)
        self.file.add_command(label="Close Network     <ctr-w>", command=self.close_command)
        self.file.add_separator()
        self.file.add_command(label="Exit", command=self.root_frame.quit)
        self.menubar.add_cascade(label="File", menu=self.file)

        self.edit = tk.Menu(master=self.menubar, tearoff=0, background=design.grey_4[design.theme],
                            foreground=design.grey_c[design.theme], activebackground=design.dark_blue[design.theme],
                            activeforeground=design.grey_c[design.theme], borderwidth=1, relief=tk.RIDGE)
        self.edit.add_command(label="Copy      <ctr-c>", command=self.copy_entity)
        self.edit.add_command(label="Paste     <ctr-v>", command=self.paste_entity)
        self.menubar.add_cascade(label="Edit", menu=self.edit)

        self.configuration = tk.Menu(master=self.menubar, tearoff=0, background=design.grey_4[design.theme],
                                     foreground=design.grey_c[design.theme], activebackground=design.dark_blue[design.theme],
                                     activeforeground=design.grey_c[design.theme], borderwidth=1, relief=tk.RIDGE)
        self.configuration.add_command(label="Global Configurations", command=self.global_config_command)
        self.configuration.add_command(label="Neuron Type Config", command=self.neuron_config_command)
        self.configuration.add_command(label="Transmitter Config", command=self.transmitter_config_command)
        self.configuration.add_command(label="Plasticity Rules", command=self.plasticity_rules_command)
        self.menubar.add_cascade(label="Configuration", menu=self.configuration)

        self.view = tk.Menu(master=self.menubar, tearoff=0, background=design.grey_4[design.theme],
                            foreground=design.grey_c[design.theme], activebackground=design.dark_blue[design.theme],
                            activeforeground=design.grey_c[design.theme], borderwidth=1, relief=tk.RIDGE)
        self.view.add_command(label="Snap to Grid    <g>", command=self.grid_command)
        self.view.add_command(label="Reset View      <space>", command=self.reset_view_command)
        self.view.add_separator()
        self.view.add_command(label="Light Mode", command=lambda: self.toggle_mode(mode="Light"))
        self.view.add_command(label="Dark Mode", command=lambda: self.toggle_mode(mode="Dark"))
        self.menubar.add_cascade(label="View", menu=self.view)

        self.help = tk.Menu(master=self.menubar, tearoff=0, background=design.grey_4[design.theme],
                            foreground=design.grey_c[design.theme], activebackground=design.dark_blue[design.theme],
                            activeforeground=design.grey_c[design.theme], borderwidth=1, relief=tk.RIDGE)
        self.help.add_command(label="About COGNA Editor", command=self.show_about)
        self.help.add_command(label="Manual/Help    <F1>", command=self.show_help)
        self.menubar.add_cascade(label="Help", menu=self.help)

        self.root_frame.config(menu=self.menubar)
        self.mark_active_tab()

        self.root_frame.bind("<Control-Left>", self.prev_network)
        self.root_frame.bind("<Control-Right>", self.next_network)
        self.root_frame.bind("<Control-n>", self.new_command)
        self.root_frame.bind("<Control-i>", self.import_command)
        self.root_frame.bind("<Control-o>", self.open_command)
        self.root_frame.bind("<Control-w>", self.close_command)
        self.root_frame.bind("<Control-s>", self.save_command)
        self.root_frame.bind("<Configure>", self.resize_window)
        self.root_frame.bind("<Control-Tab>", self.next_network)
        self.root_frame.bind("<F1>", self.show_help)
        if platform == "linux" or platform == "linux2":
            self.root_frame.bind("<ISO_Left_Tab>", self.prev_network)
        elif platform == "win32":
            self.root_frame.bind("<Shift-Tab>", self.prev_network)

        self.create_spashscreen()

    def copy_entity(self):
        """
        For binding a key to copying an entity.
        :return:    None
        """
        self.mainframe.copy_entity()

    def paste_entity(self):
        """
        For binding a key to pasting an entity.
        :return:    None
        """
        self.mainframe.paste_entity()

    def create_spashscreen(self):
        """
        Creates the slashscreen. Not finished yet.
        """
        #splash_screen = SplashScreen(self.network_manager, self.root_frame)
        pass

    def create_tab_text(self, network_id):
        """
        Returns the name of a network as a String. For putting in the tabs later.
        :param network_id:  The ID of the network.
        :return:            The Filename of the network.
        """
        return self.network_manager.filename[network_id]

    def create_tab(self, network_id):
        """
        Creates a new tab and associates it with a network.
        :param network_id:  The ID of the new tab.
        :return:            None
        """
        temp_frame = tk.Frame(master=self.tabframe, background=design.grey_4[design.theme],
                              borderwidth=0,
                              highlightthickness=1,
                              highlightbackground=design.grey_2[design.theme],
                              height= self.root_frame.winfo_height() / 40,
                              width=1)
        tab_text = self.create_tab_text(network_id)
        self.tablist.append([temp_frame, network_id,
                             tk.Label(master=temp_frame, background=design.grey_4[design.theme],
                                      text=tab_text, fg=design.light_blue[design.theme])])

        for idx, tab in enumerate(self.tablist):
            tab[0].config(width=self.root_frame.winfo_width()/len(self.tablist))
            tab[0].grid(row=0, column=tab[1])
            tab[2].pack()
            tab[0].unbind("<Button-1>")
            tab[0].bind("<Button-1>", self.click_tab)
            tab[2].unbind("<Button-1>")
            tab[2].bind("<Button-1>", self.click_tab)
            tab[2].unbind("<Button-2>")
            tab[2].bind("<Button-2>", self.click_tab)
            tab[0].unbind("<Button-2>")
            tab[0].bind("<Button-2>", self.click_tab)

        self.mark_active_tab()

    def delete_tab(self, network_id):
        """
        Deletes a certain tab.
        :param network_id:  The ID of the network to delete.
        :return:            None
        """
        if len(self.tablist) > 1:
            self.tablist.pop(network_id)
            for idx, tab in enumerate(self.tablist):
                if idx >= network_id:
                    tab[1] = tab[1] - 1
                tab[0].config(width=self.root_frame.winfo_width() / len(self.tablist))
                tab[0].grid(row=0, column=tab[1])
                tab[2].pack()
                tab[0].unbind("<Button-1>")
                tab[0].bind("<Button-1>", self.click_tab)
                tab[2].unbind("<Button-2>")
                tab[2].bind("<Button-2>", self.click_tab)
                tab[0].unbind("<Button-2>")
                tab[0].bind("<Button-2>", self.click_tab)

        self.mark_active_tab()

    def mark_active_tab(self):
        """
        Changes the design of the active tab.
        :return:    None
        """
        for tab in self.tablist:
            if tab[1] == self.network_manager.curr_network:
                tab[0].config(background=design.dark_blue[design.theme])
                tab[2].config(background=design.dark_blue[design.theme], fg=design.grey_c[design.theme])
            else:
                tab[0].config(background=design.grey_4[design.theme])
                tab[2].config(background=design.grey_4[design.theme], fg=design.grey_c[design.theme])
            tab_text = self.create_tab_text(tab[1])
            tab[2].config(text=tab_text)

    def resize_window(self, event):
        """
        Event handler for resizing the window.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        for tab in self.tablist:
            tab[0].config(width=self.root_frame.winfo_width()/len(self.tablist))
        self.mainframe.render_scene()

    def click_tab(self, event=None):
        """
        Event handler for clicking a tab. Changes to the selected tab.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        for tab in self.tablist:
            if event.widget == tab[0] or event.widget == tab[2]:
                if event.num == 1:
                    self.show_specific_network(tab[1])
                    break
                elif event.num == 2:
                    self.delete_network(tab[1])
                    self.mainframe.render_scene()
                    break

    def prev_network(self, event=None):
        """
        Selects the previous network.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.mainframe.store_parameters(entity=self.mainframe.selected_entity,
                                        parameter_names=self.mainframe.param_list)
        self.network_manager.curr_network = self.network_manager.curr_network - 1
        if self.network_manager.curr_network < 0:
            self.network_manager.curr_network = len(self.network_manager.networks)-1
        self.mainframe.render_scene()
        self.mainframe.deselect_all()
        self.mainframe.show_editmenu(store=False)
        self.mark_active_tab()

    def next_network(self, event=None):
        """
        Selects the next network.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.mainframe.store_parameters(entity=self.mainframe.selected_entity,
                                        parameter_names=self.mainframe.param_list)
        self.network_manager.curr_network = self.network_manager.curr_network + 1
        if self.network_manager.curr_network > len(self.network_manager.networks)-1:
            self.network_manager.curr_network = 0
        self.mainframe.render_scene()
        self.mainframe.deselect_all()
        self.mainframe.show_editmenu(store=False)
        self.mark_active_tab()

    def show_specific_network(self, network_id):
        """
        Selects a specific network based on ID.
        :param network_id:   The ID of the network to select.
        :return:            None
        """
        self.mainframe.store_parameters(entity=self.mainframe.selected_entity,
                                        parameter_names=self.mainframe.param_list)
        self.network_manager.curr_network = network_id
        self.mainframe.render_scene()
        self.mainframe.deselect_all()
        self.mainframe.show_editmenu(store=False)
        self.mark_active_tab()

    def new_project_command(self, event=None):
        """
        Opens the dialog box for creating a new project.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        new_project_frame = NewProject(self.root_frame, self.network_manager, self.mainframe)
        self.close_all_command()

    def open_project_command(self, event=None):
        """
        Opens the dialog box for opening a network.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.mainframe.deselect_all()
        file = filedialog.askopenfile(initialdir=self.network_manager.root_path + os.sep + self.network_manager.projects_folder,
                                      title="Open Project", filetypes=(("project files", "*.project"),))
        if not file:
            return
        if not "Valid COGNA Project" in file.read():
            messagebox.showerror("Project Error", f"{file.name.split(os.sep)[-1]} Not a valid COGNA project.")
            file.close()
            return

        splitfile = file.name.split(os.sep)
        path = ""
        for idx, token in enumerate(splitfile):
            if idx < len(splitfile) - 1:
                path = path + token + os.sep

        project_files = os.listdir(path)
        necessary_files = ["transmitters.config", "networks", "neuron_type.config", "global.config"]
        for file_idx in necessary_files:
            if file_idx not in project_files:
                messagebox.showerror("Project Error", f"Invalid COGNA project. {file_idx} missing in project structure.")
                file.close()
                return

        self.network_manager.open_project(path)
        self.close_all_command()
        try:
            self.open_command(filename=self.network_manager.project_path + os.sep + "networks" + os.sep + self.network_manager.main_network)
        except:
            self.new_command(self.network_manager.main_network)
        self.close_command(del_network=0)
        file.close()

    def new_command(self, event=None, filename=None):
        """
        Creates a new network and adds a tab for it.
        :param event:       tkinter parameter for event callback.
        :param filename:    The filename of the new network.
        :return:            None
        """
        self.mainframe.store_parameters(entity=self.mainframe.selected_entity,
                                        parameter_names=self.mainframe.param_list)
        self.mainframe.deselect_all()
        self.network_manager.add_network(name=filename)
        self.mainframe.reset_camera()
        self.mainframe.render_scene()
        self.mainframe.show_editmenu(store=False)
        self.create_tab(self.network_manager.curr_network)

    def open_command(self, event=None, filename=None):
        """
        Opens an existing network of the project.
        :param event:       tkinter parameter for event callback.
        :param filename:    The name of the network to open.
        :return:            None
        """
        self.mainframe.show_editmenu(store=True)
        error_code = self.network_manager.load_network(filename=filename)
        if error_code == Globals.SUCCESS:
            self.mainframe.reset_camera()
            self.mainframe.render_scene()
            self.mainframe.deselect_all()
            self.mainframe.show_editmenu(store=False)
            self.create_tab(self.network_manager.curr_network)
        else:
            self.mark_active_tab()

    def import_command(self, event=None):
        """
        Opens the dialogbox for importing a foreign network.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.mainframe.show_editmenu(store=True)
        self.mainframe.deselect_all()
        error_code = self.network_manager.import_network()
        if error_code == Globals.SUCCESS:
            self.mainframe.reset_camera()
            self.mainframe.render_scene()
            self.mainframe.show_editmenu(store=False)
            self.create_tab(self.network_manager.curr_network)
        else:
            self.mark_active_tab()

    def save_command(self, event=None):
        """
        Saves the currently active network.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.mainframe.show_editmenu(store=True)
        self.network_manager.save_network(save_as=False)
        self.mark_active_tab()

    def save_as_command(self, event=None):
        """
        Saves the currently active network with a "save as" dialogbox.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        self.mainframe.show_editmenu(store=True)
        self.network_manager.save_network(save_as=True)
        self.mark_active_tab()

    def delete_network(self, network_id):
        """
        Deletes a network based on its ID.
        :param network_id:  The ID of the network to delete.
        :return:            None
        """
        if len(self.network_manager.networks) > 0:
            reset_view = self.network_manager.clear_single_network(network_id)
            self.delete_tab(network_id)
            if reset_view:
                self.mainframe.reset_camera()
        self.mainframe.show_editmenu(store=False)

    def close_command(self, event=None, del_network=None):
        """
        Eventhandler for closing down a network.
        :param event:       tkinter parameter for event callback.
        :param del_network: The ID of the network to delete. If None the current network will be deleted.
        :return:            None
        """
        if del_network is None:
            deleted_network = self.network_manager.curr_network
        else:
            deleted_network = del_network
        self.mainframe.deselect_all()
        self.delete_network(deleted_network)

        self.mainframe.reset_camera()
        self.mainframe.render_scene()
        self.mark_active_tab()

    def close_all_command(self, event=None):
        """
        Closes all networks down.
        :param event:   tkinter parameter for event callback.
        :return:        None
        """
        for tab in reversed(self.tablist):
            self.delete_network(self.network_manager.curr_network)
        self.mainframe.render_scene()
        self.mark_active_tab()

    def neuron_config_command(self):
        """
        Opens dialogbox for neuron type configuration.
        :return:    None
        """
        neuron_configurator = NeuronConfigurator(self.root_frame, self.mainframe, self.network_manager)

    def transmitter_config_command(self):
        """
        Opens dialogbox for neurotransmitter configuration.
        :return:    None
        """
        transmitter_configurator = TransmitterConfigurator(self.root_frame, self.network_manager, self.mainframe)

    def plasticity_rules_command(self):
        """
        No finished yet. Opens dialogbox for plasticity configuration.
        :return:    None
        """
        pass

    def global_config_command(self):
        """
        Opens dialogbox for global configuration.
        :return:    None
        """
        global_configurator = GlobalConfig(self.root_frame, self.network_manager)

    def grid_command(self):
        """
        Toggles grid snap of cursor on the canvas.
        :return:    None
        """
        self.mainframe.toggle_grid_snap(None)

    def reset_view_command(self):
        """
        Resets the camera view on the canvas to the center.
        :return:    None
        """
        self.mainframe.reset_camera(None)

    def toggle_mode(self, mode):
        """
        Toggles between dark mode and light mode.
        :param mode:    The mode to select.
        :return:        None
        """
        if mode == "Light":
            design.theme = 1
        elif mode == "Dark":
            design.theme = 0

        self.root_frame.update()
        self.tabframe.config(background=design.grey_4[design.theme], highlightbackground=design.grey_2[design.theme])
        self.menubar.config(background=design.grey_4[design.theme], foreground=design.grey_c[design.theme],
                            activebackground=design.dark_blue[design.theme], activeforeground=design.grey_c[design.theme])
        self.file.config(background=design.grey_4[design.theme], foreground=design.grey_c[design.theme],
                         activebackground=design.dark_blue[design.theme], activeforeground=design.grey_c[design.theme])
        self.edit.config(background=design.grey_4[design.theme], foreground=design.grey_c[design.theme],
                         activebackground=design.dark_blue[design.theme], activeforeground=design.grey_c[design.theme])
        self.view.config(background=design.grey_4[design.theme], foreground=design.grey_c[design.theme],
                         activebackground=design.dark_blue[design.theme], activeforeground=design.grey_c[design.theme])
        self.help.config(background=design.grey_4[design.theme], foreground=design.grey_c[design.theme],
                         activebackground=design.dark_blue[design.theme], activeforeground=design.grey_c[design.theme])
        self.configuration.config(background=design.grey_4[design.theme], foreground=design.grey_c[design.theme],
                                  activebackground=design.dark_blue[design.theme], activeforeground=design.grey_c[design.theme])
        for tab in self.tablist:
            tab[0].config(background=design.grey_4[design.theme],
                          highlightbackground=design.grey_2[design.theme])
            tab[2].config(background=design.grey_4[design.theme],
                          fg=design.light_blue[design.theme])

        self.mainframe.editorcanvas.config(background=design.grey_3[design.theme])
        self.mainframe.mainframe.config(background=design.grey_7[design.theme])
        self.mainframe.editframe.config(background=design.grey_4[design.theme])
        self.mainframe.editresize.config(background=design.grey_2[design.theme])
        self.mainframe.edit_top.config(background=design.grey_4[design.theme])
        self.mainframe.project_name_label.config(background=design.grey_4[design.theme],
                                                 fg=design.light_blue[design.theme])
        self.mainframe.select_button.config(background=design.grey_3[design.theme], fg=design.grey_c[design.theme],
                                            activebackground=design.grey_7[design.theme])
        self.mainframe.neuron_button.config(background=design.grey_3[design.theme], fg=design.grey_c[design.theme],
                                            activebackground=design.grey_7[design.theme])
        self.mainframe.connection_button.config(background=design.grey_3[design.theme], fg=design.grey_c[design.theme],
                                                activebackground=design.grey_7[design.theme])
        self.mainframe.import_button.config(background=design.grey_3[design.theme], fg=design.grey_c[design.theme],
                                            activebackground=design.grey_7[design.theme])
        self.mainframe.exchange_button.config(background=design.grey_3[design.theme], fg=design.grey_c[design.theme],
                                              activebackground=design.grey_7[design.theme])
        self.mainframe.viewframe.config(background=design.grey_3[design.theme])
        self.mainframe.edit_1.config(background=design.grey_4[design.theme])
        for frame in self.mainframe.parameter_frame:
            frame.config(background=design.grey_4[design.theme])
        self.mainframe.general_info.config(bg=design.grey_4[design.theme], fg=design.light_blue[design.theme])
        self.mainframe.id_info.config(bg=design.grey_4[design.theme], fg=design.grey_c[design.theme])
        self.mainframe.show_editmenu(store=False)
        self.root_frame.update()
        self.mainframe.render_scene()
        self.mark_active_tab()
        self.root_frame.update()

    def show_about(self):
        """
        Shows information about the program.
        :return:    None
        """
        messagebox.showinfo('About COGNA Editor',
                            'Editor for constructing COGNA network architectures.\n'
                            'Author: Cyril Marx\n'
                            'Copyright (c) by Cyril Marx 2021')

    def show_help(self, event=None):
        """
        Shows helf for the program in the web browser.
        :param event:       tkinter parameter for event callback.
        :return:            None
        """
        if platform == "linux" or platform == "linux2":
            error_code = os.system("google-chrome html" + os.sep + "help.html")
            if error_code != Globals.SUCCESS:
                error_code = os.system("firefox html" + os.sep + "help.html")
            if error_code != Globals.SUCCESS:
                messagebox.showerror("Browser Error",
                                     "Cannot open help file probably due to unexpected browser. Try opening html/help manually.")
        elif platform == "win32":
            os.system("start html" + os.sep + "help.html")
