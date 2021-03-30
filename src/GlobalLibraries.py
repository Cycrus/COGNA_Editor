try:
    import tkinter as tk
    from tkinter import messagebox
except:
    print("[ERROR] Missing package. Install package <tkinter> first.")
try:
    from PIL import ImageTk, Image
except:
    print("[ERROR] Missing package. Install package <pillow> first.")
import math
from src.NetworkManager import *
from src.Design import *


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle


def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc
