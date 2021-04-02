#!/usr/bin/python3

from src.Topmenu import *
from src.Bottommenu import *
from src.Mainframe import *

class UI:
    def __init__(self, root, network_manager):
        self.mainframe = Mainframe(root, network_manager)
        self.topmenu = Topmenu(root, network_manager, self.mainframe)
        self.mainframe.pack_widgets()
        self.bottommenu = Bottommenu(root)

