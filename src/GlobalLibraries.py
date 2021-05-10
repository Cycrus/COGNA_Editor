from sys import platform
import math
import json
import re
import os
import copy
import tkinter as tk
from itertools import chain
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
from src.NetworkManager import *
from src.Design import *
from src.Globals import *


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


tk.Canvas.create_circle = _create_circle


def _create_triange(self, x, y, r, **kwargs):
    return self.create_polygon(x, y-r, x+r, y+r, x-r, y+r, **kwargs)


tk.Canvas.create_triangle = _create_triange


def _create_rectangle_by_size(self, x, y, r, **kwargs):
    return self.create_polygon(x-r, y-r, x+r, y-r, x+r, y+r, x-r, y+r, **kwargs)


tk.Canvas.create_rectangle_by_size = _create_rectangle_by_size
