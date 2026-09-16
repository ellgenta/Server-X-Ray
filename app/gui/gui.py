import tkinter as tk
import ctypes
from .login_page import LoginPage
from .performace_page import PerformancePage

class App:
    def __init__(self, controller):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        self.controller = controller
        self.root = tk.Tk()

        self.root.title("Server X-Ray")
        self.root.geometry("1000x700")

        self.show_login_page()
        self.run()

    def run(self):
        self.root.mainloop()

    def show_login_page(self):
        self.login_page = LoginPage(
            self.root, 
            self.controller, 
            self.show_performance_page
        )
        
        self.login_page.pack(fill="both", expand=True)

    def show_performance_page(self):
        self.login_page.destroy()

        self.performance_page = PerformancePage(
            self.root,
            self.controller
        )

        self.performance_page.pack(
            fill="both",
            expand=True
        )