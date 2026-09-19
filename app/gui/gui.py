import tkinter as tk
import ctypes
import threading
from .login.login_page import LoginPage
from .performance.performace_page import PerformancePage


class App:
    def __init__(self, controller):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        self.controller = controller
        self.root = tk.Tk()

        self.root.title("Server X-Ray")
        self.root.geometry("1000x700")

        self.updating = False

        self.show_login_page()
        self.root.after(10000, self.update_data)

        self.run()

    def run(self):
        self.root.mainloop()

    def show_login_page(self):
        self.login_page = LoginPage(
            self.root,
            self.controller,
            self.show_performance_page
        )

        self.login_page.pack(
            fill="both",
            expand=True
        )

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

        self.start_update()

    def start_update(self):
        if self.controller.is_connected and not self.updating:
            self.updating = True

            thread = threading.Thread(
                target=self.update_worker,
                daemon=True
            )

            thread.start()

    def update_data(self):
        self.start_update()
        self.root.after(10000, self.update_data)

    def update_worker(self):
        try:
            self.controller.update()
            self.root.after(0, self.refresh_gui)
        finally:
            self.updating = False

    def refresh_gui(self):
        if not hasattr(self, "performance_page"):
            return

        self.performance_page.refresh_processes()
        self.performance_page.refresh_cpu_stats()
        self.performance_page.refresh_disks()