from src.GlobalLibraries import *
from src.NetworkManager import NetworkManager


class TransmitterConfigurator:
    def __init__(self, root, network_manager, mainframe):
        self.root_frame = root
        self.transmitter_list = copy.deepcopy(network_manager.transmitters)
        self.deleted_transmitters = []
        self.renamed_transmitters = []
        self.renamed_transmitters.append([])
        self.renamed_transmitters.append([])
        for t in self.transmitter_list:
            self.renamed_transmitters[0].append(t)
            self.renamed_transmitters[1].append(None)
        self.network_manager = network_manager
        self.mainframe = mainframe
        self.frame_number = 30

        self.width = self.root_frame.winfo_screenwidth() // 5
        self.height = self.root_frame.winfo_screenheight() // 2
        self.pos_x = self.root_frame.winfo_screenwidth() // 2 - self.width // 2
        self.pos_y = self.root_frame.winfo_screenheight() // 2 - self.height // 2
        self.transmitter_frame = tk.Toplevel()
        self.transmitter_frame.grab_set()
        self.transmitter_frame.geometry(f"{self.width}x{self.height}+{self.pos_x}+{self.pos_y}")
        self.transmitter_frame.overrideredirect(True)
        self.transmitter_frame.configure(background=design.grey_4[design.theme], highlightthickness=4,
                                         highlightbackground=design.grey_2[design.theme])
        self.transmitter_frame.update()

        self.label_frame = tk.Frame(master=self.transmitter_frame, background=design.dark_blue[design.theme],
                                    borderwidth=0,
                                    highlightthickness=2,
                                    highlightbackground=design.grey_2[design.theme],
                                    height=self.transmitter_frame.winfo_height() // 7,
                                    width=self.transmitter_frame.winfo_width())
        self.label_frame.pack(side=tk.TOP, fill=tk.X)
        self.label = tk.Label(master=self.label_frame, background=design.dark_blue[design.theme],
                              text="Neurotransmitter Configuration",
                              fg=design.grey_c[design.theme])
        self.label.pack(pady=5)
        self.transmitter_frame.update()

        self.editor = tk.Frame(master=self.transmitter_frame, background=design.grey_4[design.theme],
                               borderwidth=0,
                               highlightthickness=0,
                               height=self.transmitter_frame.winfo_height() - (self.label_frame.winfo_height() * 2),
                               width=self.transmitter_frame.winfo_width())
        self.editor.pack(side=tk.TOP, fill=tk.BOTH)

        self.edit_frames = []
        for idx in range(0, self.frame_number):
            self.edit_frames.append(tk.Frame(master=self.editor, background=design.grey_4[design.theme], borderwidth=0,
                                    highlightthickness=0))
            self.edit_frames[idx].pack(side=tk.TOP, anchor="w")
        self.edit_widgets = []

        self.render_editor()

        self.button_space = tk.Frame(master=self.transmitter_frame, background=design.grey_4[design.theme],
                                     borderwidth=0,
                                     highlightthickness=0,
                                     height=self.transmitter_frame.winfo_height() // 8,
                                     width=self.transmitter_frame.winfo_width())
        self.button_space.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        self.close_button = tk.Button(master=self.button_space, text="Discard", background=design.grey_3[design.theme],
                                      fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                      command=lambda: self.close_window(save=False))

        self.save_button = tk.Button(master=self.button_space, text="Save & Close", background=design.grey_3[design.theme],
                                     fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                     command=lambda: self.close_window(save=True))

        self.close_button.pack(side=tk.LEFT, padx=20, pady=5)
        self.save_button.pack(side=tk.RIGHT, padx=20, pady=5)

    def render_editor(self):
        for widget in self.edit_widgets:
            if widget[0] is not None:
                widget[0].forget()
            if widget[1] is not None:
                widget[1].forget()
        self.edit_widgets.clear()

        for idx, tran in enumerate(self.transmitter_list):
            if idx > 0:
                textcol = design.black[design.theme]
            else:
                textcol = design.grey_4[design.theme]
            temp_textbox = tk.Entry(master=self.edit_frames[idx], width=15,
                                    bg=design.grey_7[design.theme], borderwidth=0, fg=textcol,
                                    highlightthickness=2, highlightbackground=design.grey_2[design.theme])
            temp_textbox.insert(tk.END, tran)
            temp_button = tk.Button(master=self.edit_frames[idx], text="Delete", background=design.grey_3[design.theme],
                                    fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                    command=lambda i=idx: self.delete_transmitter(trans_index=i))
            self.edit_widgets.append([temp_textbox, temp_button])

        self.edit_widgets.append([tk.Button(master=self.edit_frames[len(self.transmitter_list)],
                                 text="Add Transmitter", background=design.grey_3[design.theme],
                                 fg=design.grey_c[design.theme], activebackground=design.grey_7[design.theme],
                                 command=self.add_transmitter), None])

        for idx, widget in enumerate(self.edit_widgets):
            if widget[0] is not None:
                widget[0].pack(side=tk.LEFT, padx=20, pady=10)
            if widget[1] is not None:
                if idx != 0:
                    widget[1].pack(side=tk.LEFT, padx=0, pady=10)

    def store_transmitter(self):
        for idx, tran in enumerate(self.transmitter_list):
            if idx > 0:
                temp_tran = self.edit_widgets[idx][0].get().replace("\n", "").replace(" ", "")
                for j, check_trans in enumerate(self.renamed_transmitters[0]):
                    if check_trans == tran:
                        self.renamed_transmitters[1][j] = temp_tran
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
        self.deleted_transmitters.append(self.transmitter_list[trans_index])
        self.transmitter_list.pop(trans_index)
        self.renamed_transmitters[0].pop(trans_index)
        self.renamed_transmitters[1].pop(trans_index)
        self.render_editor()

    def close_window(self, save):
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
                    try:
                        if not can_save and self.renamed_transmitters[0][idx] is not None:
                            temp_list.append(self.renamed_transmitters[0][idx])
                    except:
                        pass

            error_code_1 = self.network_manager.save_storing(["influenced_transmitter", "used_transmitter"],
                                                             self.deleted_transmitters, [self.transmitter_list[0]])
            error_code_2 = self.network_manager.save_storing(["influenced_transmitter", "used_transmitter"],
                                                             self.renamed_transmitters[0], self.renamed_transmitters[1])
            if error_code_1 == Globals.SUCCESS and error_code_2 == Globals.SUCCESS:
                self.network_manager.transmitters = temp_list

        for idx, frame in enumerate(self.edit_frames):
            frame.destroy()

        self.edit_widgets.clear()
        self.transmitter_frame.grab_release()
        self.network_manager.save_transmitters()
        self.transmitter_frame.destroy()
        self.mainframe.show_editmenu(store=False)
