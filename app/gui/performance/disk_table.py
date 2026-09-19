import tkinter as tk
from tkinter import ttk


class DiskTable(tk.Frame):
    UNIT_PX = 8

    COLUMNS = (
        ("fs_name", "File System", 6),
        ("size", "Size (MB)", 3),
        ("used", "Used (MB)", 3),
        ("available", "Available (MB)", 5),
        ("mount", "Mount", 11),
        ("usage_percent", "Usage", 2),
    )

    EVEN_ROW_COLOR = "#1f2226"
    ODD_ROW_COLOR = "#292d30"

    def __init__(self, parent):
        super().__init__(parent, bg="#292d30")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure(
            "DiskStats.Treeview",
            background="#292d30",
            fieldbackground="#292d30",
            foreground="#ffffff",
            font=("Roboto", 11),
            rowheight=26,
            borderwidth=0
        )

        self.style.configure(
            "DiskStats.Treeview.Heading",
            background="#202020",
            foreground="#7ac2a2",
            font=("Roboto", 11, "bold"),
            borderwidth=0
        )

        self.style.map(
            "DiskStats.Treeview",
            background=[("selected", "#333637")],
            foreground=[("selected", "#ffffff")]
        )

        self.style.map(
            "DiskStats.Treeview.Heading",
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
            columns=[key for key, _, _ in self.COLUMNS],
            show="headings",
            style="DiskStats.Treeview"
        )

        for key, label, units in self.COLUMNS:
            self.tree.heading(key, text=label)

            width = units * self.UNIT_PX

            self.tree.column(
                key,
                anchor="center",
                width=width,
                minwidth=width,
                stretch=True
            )

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree.tag_configure("evenrow", background=self.EVEN_ROW_COLOR)
        self.tree.tag_configure("oddrow", background=self.ODD_ROW_COLOR)

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

    def update_disks(self, disk_stats):
        self.tree.delete(*self.tree.get_children())

        if not disk_stats:
            return

        for index, entry in enumerate(disk_stats):
            tag = "evenrow" if index % 2 == 0 else "oddrow"

            self.tree.insert(
                "",
                "end",
                values=(
                    entry.fs_name,
                    entry.size,
                    entry.used,
                    entry.available,
                    entry.mount,
                    f"{entry.usage_percent}%"
                ),
                tags=(tag,)
            )