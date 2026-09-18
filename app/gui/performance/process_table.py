import tkinter as tk
from tkinter import ttk

class ProcessTable(tk.Frame):
    COLUMNS = (
        ("user", "User"),
        ("pid", "Process ID"),
        ("cpu_load", "CPU Load"),
        ("mem_load", "Memory Load"),
        ("status", "Status"),
        ("time", "Time"),
        ("command", "Command"),
    )

    COLUMN_WIDTHS = {
        "user": 70,
        "pid": 85,
        "cpu_load": 120,
        "mem_load": 150,
        "status": 75,
        "time": 70,
        "command": 120,
    }

    EVEN_ROW_COLOR = "#1f2226"
    ODD_ROW_COLOR = "#292d30"

    def __init__(self, parent):
        super().__init__(parent, bg="#292d30")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure(
            "Processes.Treeview",
            background="#292d30",
            fieldbackground="#292d30",
            foreground="#ffffff",
            font=("Roboto", 12),
            rowheight=28,
            borderwidth=0
        )

        self.style.configure(
            "Processes.Treeview.Heading",
            background="#202020",
            foreground="#7ac2a2",
            font=("Roboto", 12, "bold"),
            borderwidth=0
        )

        self.style.map(
            "Processes.Treeview",
            background=[("selected", "#333637")],
            foreground=[("selected", "#ffffff")]
        )

        self.style.map(
            "Processes.Treeview.Heading",
            background=[
                ("active", "#202020"),
                ("pressed", "#202020")
            ],
            foreground=[
                ("active", "#7ac2a2"),
                ("pressed", "#7ac2a2")
            ]
        )

        self.tree = ttk.Treeview(
            self,
            columns=[key for key, _ in self.COLUMNS],
            show="headings",
            style="Processes.Treeview"
        )

        for key, label in self.COLUMNS:
            self.tree.heading(
                key,
                text=label
            )

            self.tree.column(
                key,
                anchor="center",
                width=self.COLUMN_WIDTHS[key],
                minwidth=self.COLUMN_WIDTHS[key],
                stretch=(key == "command")
            )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.tree.tag_configure("evenrow", background=self.EVEN_ROW_COLOR)
        self.tree.tag_configure("oddrow", background=self.ODD_ROW_COLOR)

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

    def update_processes(self, proc_list):
        self.tree.delete(*self.tree.get_children())

        if not proc_list:
            return

        for index, entry in enumerate(proc_list):
            tag = "evenrow" if index % 2 == 0 else "oddrow"

            self.tree.insert(
                "",
                "end",
                values=(
                    entry.user,
                    entry.pid,
                    f"{entry.cpu_load:.1f}%",
                    f"{entry.mem_load:.1f}%",
                    entry.status,
                    entry.time.strftime("%H:%M"),
                    entry.command
                ),
                tags=(tag,)
            )