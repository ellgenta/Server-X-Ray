import tkinter as tk
import ctypes
import threading
from .login.login_page import LoginPage
from .performance.performace_page import PerformancePage
from .logs.log_page import LogPage


class App:
    LOG_TABS = {
        "log1": ("auth_logs", "Authlogs"),
        "log2": ("sys_logs", "Syslogs"),
        "log3": ("kern_logs", "Kernlogs"),
    }

    def __init__(self, controller):
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        self.controller = controller
        self.root = tk.Tk()

        self.root.title("Server X-Ray")
        self.root.geometry("1000x700")

        self.update_in_progress = False
        self.current_page = None

        self.show_login_page()
        self.run()

    def run(self):
        self.root.mainloop()

    def show_login_page(self):
        self.current_page = None

        self.login_page = LoginPage(
            self.root,
            self.controller,
            self.show_performance_page
        )

        self.login_page.pack(fill="both", expand=True)

        self.update_data()

    def show_performance_page(self):
        if hasattr(self, "login_page") and self.login_page.winfo_exists():
            self.login_page.destroy()

        page = PerformancePage(
            self.root,
            self.controller,
            "meow",
            self.on_tab_change,
            self.show_login_page
        )

        self._switch_page(page)

    def show_log_page(self, tab_name):
        log_attr, title = self.LOG_TABS[tab_name]

        page = LogPage(
            self.root,
            self.controller,
            "meow",
            title,
            log_attr,
            self.on_tab_change,
            self.show_login_page
        )

        self._switch_page(page)

    def _switch_page(self, page):
        if self.current_page is not None and self.current_page.winfo_exists():
            self.current_page.destroy()

        self.current_page = page

        self.current_page.pack(
            fill="both",
            expand=True
        )

        self._trigger_update()

    def on_tab_change(self, tab_name):
        if tab_name == "performance":
            self.show_performance_page()
        elif tab_name in self.LOG_TABS:
            self.show_log_page(tab_name)

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

        if self.current_page is not None and self.current_page.winfo_exists():
            self.current_page.refresh()