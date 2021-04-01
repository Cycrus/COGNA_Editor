#!/usr/bin/python3

import os
from src.UI import *
from sys import platform

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
    if platform == "linux" or platform == "linux2":
        root.attributes("-zoomed", True)
    elif platform == "win32":
        root.state("zoomed")
    root.unbind_all("<<NextWindow>>")
    root.unbind_all("<<PrevWindow>>")

    network_manager = NetworkManager()

    ui = UI(root, network_manager)

    root.mainloop()
