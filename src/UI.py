"""
UI.py

Initializes the graphical user interface.

Author: Cyril Marx
Date: 09.09.2021
"""

from src.Topmenu import *
from src.Mainframe import *

class UI:
    def __init__(self, root, network_manager):
        """
        Constructor.
        :return:    None
        """
        self.mainframe = Mainframe(root, network_manager)
        self.topmenu = Topmenu(root, network_manager, self.mainframe)
        self.mainframe.pack_widgets()

