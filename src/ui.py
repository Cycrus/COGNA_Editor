#!/usr/bin/python3

from src.topmenu_class import *
from src.bottommenu_class import *
from src.mainframe_class import *

class UI:
    def __init__(self, root, network_manager):
        self.topmenu = Topmenu(root, network_manager)
        self.bottommenu = Bottommenu(root)
        self.mainframe = Mainframe(root, network_manager)


