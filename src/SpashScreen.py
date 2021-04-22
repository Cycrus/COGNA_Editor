from src.GlobalLibraries import *

class SplashScreen:
    def __init__(self, network_manager, root):
        self.network_manager = network_manager
        self.root_frame = root
        splash_x = self.root_frame.winfo_width() // 2 - design.splash_width // 2
        splash_y = self.root_frame.winfo_height() // 2 - design.splash_height // 2
        self.splash = tk.Toplevel()
        self.splash.configure(background=design.grey_7[design.theme], highlightthickness=4,
                              highlightbackground=design.grey_2[design.theme])
        self.splash.geometry(f"{design.splash_width}x{design.splash_height}+{splash_x}+{splash_y}")
        self.splash.overrideredirect(True)
        self.splash.grab_set()

    def close_splash_screen(self):
        self.splash.grab_release()
        self.splash.destroy()
