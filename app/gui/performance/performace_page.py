import tkinter as tk
from .top_bar import TopBar

class PerformancePage(tk.Frame):  
    def __init__(self, parent, controller, host, on_disconnect):
        super().__init__(parent)

        self.controller = controller
        self.host = host
        self.on_disconnect = on_disconnect

        self.create_widgets()

    def create_widgets(self):
        self.top_bar = TopBar(
            self,
            self.host,
            None,
            self.disconnect
        )

        self.top_bar.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.grid_columnconfigure(0, weight=1)

    def disconnect(self):
        self.controller.disconnect()
        #self.top_bar.destroy()
        self.destroy()
        self.on_disconnect()