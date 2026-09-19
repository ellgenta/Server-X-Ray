import tkinter as tk
from .top_bar import TopBar
from .panel import Panel
from .process_table import ProcessTable
from .cpu_stats import CPUStats
from .disk_table import DiskTable


class PerformancePage(tk.Frame):
    def __init__(self, parent, controller, host, on_disconnect):
        super().__init__(parent, bg="#202020")

        self.controller = controller
        self.host = host
        self.on_disconnect = on_disconnect

        self.create_widgets()

        self.refresh_processes()
        self.refresh_cpu_stats()
        self.refresh_disks()

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

        self.content.grid_columnconfigure(0, weight=3)
        self.content.grid_columnconfigure(1, weight=5)
        self.content.grid_rowconfigure(0, weight=1)

        self.left_column = tk.Frame(
            self.content,
            bg="#202020"
        )

        self.left_column.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        self.left_column.grid_columnconfigure(
            0,
            weight=1
        )

        for i in range(3):
            self.left_column.grid_rowconfigure(
                i,
                weight=1,
                uniform="left_panels"
            )

        self.panel_1 = Panel(self.left_column)

        self.panel_1.grid(
            row=0,
            column=0,
            sticky="nsew",
            pady=(0, 8)
        )

        self.panel_2 = Panel(self.left_column)

        self.panel_2.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(0, 8)
        )

        self.panel_2.grid_columnconfigure(
            0,
            weight=1
        )

        self.panel_2.grid_rowconfigure(
            1,
            weight=1
        )

        self.panel_2_title = tk.Label(
            self.panel_2,
            text="CPU Stats",
            bg="#292d30",
            fg="#ffffff",
            font=("Roboto", 22)
        )

        self.panel_2_title.grid(
            row=0,
            column=0,
            sticky="nw",
            padx=10,
            pady=10
        )

        self.cpu_stats = CPUStats(
            self.panel_2
        )

        self.cpu_stats.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        self.panel_3 = Panel(self.left_column)

        self.panel_3.grid(
            row=2,
            column=0,
            sticky="nsew"
        )

        self.panel_3.grid_columnconfigure(
            0,
            weight=1
        )

        self.panel_3.grid_rowconfigure(
            1,
            weight=1
        )

        self.panel_3_title = tk.Label(
            self.panel_3,
            text="Disk Usage",
            bg="#292d30",
            fg="#ffffff",
            font=("Roboto", 22)
        )

        self.panel_3_title.grid(
            row=0,
            column=0,
            sticky="nw",
            padx=10,
            pady=10
        )

        self.disk_table = DiskTable(
            self.panel_3
        )

        self.disk_table.grid(
            row=1,
            column=0,
            sticky="new",
            padx=(0, 10),
            pady=(0, 10)
        )

        self.panel_4 = Panel(self.content)

        self.panel_4.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.panel_4.grid_columnconfigure(
            0,
            weight=1
        )

        self.panel_4.grid_rowconfigure(
            1,
            weight=1
        )

        self.panel_4_title = tk.Label(
            self.panel_4,
            text="Current Processes",
            bg="#292d30",
            fg="#ffffff",
            font=("Roboto", 22)
        )

        self.panel_4_title.grid(
            row=0,
            column=0,
            sticky="nw",
            padx=10,
            pady=10
        )

        self.process_table = ProcessTable(
            self.panel_4
        )

        self.process_table.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(0, 10),
            pady=(0, 10)
        )

    def refresh_processes(self):
        self.process_table.update_processes(
            self.controller.proc_list
        )

    def refresh_cpu_stats(self):
        self.cpu_stats.update_stats(
            self.controller.load_average_stats
        )

    def refresh_disks(self):
        self.disk_table.update_disks(
            self.controller.disk_stats
        )

    def disconnect(self):
        self.controller.disconnect()
        self.destroy()
        self.on_disconnect()