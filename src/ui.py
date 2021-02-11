#!/usr/bin/python3

from topmenu_class import *
from bottommenu_class import *
from mainframe_class import *

class UI:
    def __init__(self, root, network_manager):
        self.topmenu = Topmenu(root, network_manager)
        self.bottommenu = Bottommenu(root)
        self.mainframe = Mainframe(root, network_manager)


