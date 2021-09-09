"""
GlobalLibraries.py

Import of general libraries and redefinition/enhancement of certain elements in some libraries.

Author: Cyril Marx
Date: 09.09.2021
"""

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

os.sep = "/"


def _create_circle(self, x, y, r, **kwargs):
    """
    An addon of tkinter canvas drawing. Draws a circle on the canvas.
    :return:    Returns the pixels of the circle on the canvas.
    """
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


tk.Canvas.create_circle = _create_circle


def _create_triange(self, x, y, r, **kwargs):
    """
    An addon of tkinter canvas drawing. Draws a uniform triangle on the canvas.
    :return:    Returns the pixels of the triangle on the canvas.
    """
    return self.create_polygon(x, y-r, x+r, y+r, x-r, y+r, **kwargs)


tk.Canvas.create_triangle = _create_triange


def _create_rectangle_by_size(self, x, y, r, **kwargs):
    """
    An addon of tkinter canvas drawing. Draws a rectangle on the canvas based on size instead of corner points.
    :return:    Returns the pixels of the rectangle on the canvas.
    """
    return self.create_polygon(x-r, y-r, x+r, y-r, x+r, y+r, x-r, y+r, **kwargs)


tk.Canvas.create_rectangle_by_size = _create_rectangle_by_size
