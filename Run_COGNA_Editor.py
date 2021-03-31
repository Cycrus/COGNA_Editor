#!/usr/bin/python3

import os
from src.UI import *

if __name__ == "__main__":
    os.path.dirname(os.path.abspath(__file__))

    try:
        os.mkdir("networks")
    except:
        pass

    root = tk.Tk()
    root.tk.call('tk', 'scaling', 2.0)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.title("untitled.nn")
    root.geometry(f"{width}x{height}+0+0")
    root.attributes('-zoomed', True)

    network_manager = NetworkManager()

    ui = UI(root, network_manager)

    root.mainloop()
