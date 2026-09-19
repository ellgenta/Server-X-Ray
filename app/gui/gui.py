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

        self.update_in_progress = False

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

        self._trigger_update()

    def update_data(self):
        self._trigger_update()
        self.root.after(5000, self.update_data)

    def _trigger_update(self):
        if self.controller.is_connected and not self.update_in_progress:
            self.update_in_progress = True

            threading.Thread(
                target=self._fetch_update_in_background,
                daemon=True
            ).start()

    def _fetch_update_in_background(self):
        try:
            self.controller.update()
        except Exception:
            self.update_in_progress = False
            return

        self.root.after(0, self._apply_update)

    def _apply_update(self):
        self.update_in_progress = False

        if hasattr(self, "performance_page"):
            self.performance_page.refresh_processes()
            self.performance_page.refresh_cpu_stats()
            self.performance_page.refresh_disks()
            self.performance_page.refresh_ram()