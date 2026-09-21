import tkinter as tk
from ..performance.top_bar import TopBar
from ..performance.panel import Panel
from .log_table import LogTable
from .log_dashboard import LogDashboard


class LogPage(tk.Frame):
    def __init__(self, parent, controller, host, title, log_attr, on_tab_change, on_disconnect):
        super().__init__(parent, bg="#202020")

        self.controller = controller
        self.host = host
        self.title = title
        self.log_attr = log_attr
        self.on_tab_change = on_tab_change
        self.on_disconnect = on_disconnect

        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        self.top_bar = TopBar(
            self,
            self.host,
            self.on_tab_change,
            self.disconnect
        )

        self.top_bar.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.content = tk.Frame(
            self,
            bg="#202020"
        )

        self.content.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.content.grid_columnconfigure(0, weight=4)
        self.content.grid_columnconfigure(1, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.table_panel = Panel(self.content)

        self.table_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        self.table_panel.grid_columnconfigure(0, weight=1)
        self.table_panel.grid_rowconfigure(1, weight=1)

        self.table_title = tk.Label(
            self.table_panel,
            text=self.title,
            bg="#292d30",
            fg="#ffffff",
            font=("Roboto", 22)
        )

        self.table_title.grid(
            row=0,
            column=0,
            sticky="nw",
            padx=10,
            pady=10
        )

        self.log_table = LogTable(
            self.table_panel
        )

        self.log_table.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(10, 10),
            pady=(0, 10)
        )

        self.dashboard_panel = Panel(self.content)

        self.dashboard_panel.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.dashboard_panel.grid_columnconfigure(0, weight=1)
        self.dashboard_panel.grid_rowconfigure(1, weight=1)

        self.dashboard_title = tk.Label(
            self.dashboard_panel,
            text="Dashboard",
            bg="#292d30",
            fg="#ffffff",
            font=("Roboto", 22)
        )

        self.dashboard_title.grid(
            row=0,
            column=0,
            sticky="nw",
            padx=10,
            pady=10
        )

        self.log_dashboard = LogDashboard(
            self.dashboard_panel
        )

        self.log_dashboard.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

    def refresh(self):
        logs = getattr(self.controller, self.log_attr, [])

        self.log_table.update_logs(logs)
        self.log_dashboard.update_logs(logs)

    def disconnect(self):
        self.controller.disconnect()
        self.destroy()
        self.on_disconnect()