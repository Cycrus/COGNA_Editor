from src.GlobalLibraries import *
from src.NetworkManager import NetworkManager


class GlobalConfig:
    def __init__(self, root, network_manager):
       self.root_frame = root
       self.network_manager = network_manager
       self.frame_number = 30

