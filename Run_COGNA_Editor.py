#!/usr/bin/python3

import os
from src.ui import *

if __name__ == "__main__":
    os.path.dirname(os.path.abspath(__file__))

    root = tk.Tk()
    if root.winfo_screenwidth() == 2736:
        root.tk.call('tk', 'scaling', 2.0)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.title("untitled.nn")
    root.geometry(f"{width}x{height}")

    network_manager = NetworkManager()

    ui = UI(root, network_manager)

    root.mainloop()
