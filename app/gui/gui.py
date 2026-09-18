import tkinter as tk
import ctypes
from .login.login_page import LoginPage
from .performance.performace_page import PerformancePage

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

        self.update_data()

    def show_performance_page(self):
        self.login_page.destroy()

        self.performance_page = PerformancePage(
            self.root,
            self.controller,
            "meow",
            self.show_login_page
        )

        self.performance_page.pack(
            fill="both",
            expand=True
        )

    def update_data(self):
        if self.controller.is_connected:
            self.controller.update()

            if hasattr(self, "performance_page"):
                self.performance_page.refresh_processes()
                self.performance_page.refresh_cpu_stats()

        self.root.after(10000, self.update_data)