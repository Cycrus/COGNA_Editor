from src.GlobalLibraries import *


class Bottommenu:
    def __init__(self, root):
        self.bottommenu = tk.Frame(master=root, background=topmenu_backcolor,
                                   borderwidth=0,
                                   highlightthickness=1,
                                   width=root.winfo_width(),
                                   height=bottommenu_height,
                                   highlightbackground=highlight_color)
        self.bottommenu.grid_columnconfigure(0, weight=1)
        self.bottommenu.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=0, pady=0, expand=False)