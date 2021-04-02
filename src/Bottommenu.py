from src.GlobalLibraries import *


class Bottommenu:
    def __init__(self, root):
        self.root_frame = root
    
        barmenu_height = self.root_frame.winfo_height() / 40
        
        self.bottommenu = tk.Frame(master=root, background=grey_4,
                                   borderwidth=0,
                                   highlightthickness=1,
                                   width=root.winfo_width(),
                                   height=barmenu_height,
                                   highlightbackground=grey_2)
        self.bottommenu.grid_columnconfigure(0, weight=1)
        self.bottommenu.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=0, pady=0, expand=False)