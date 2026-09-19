import tkinter as tk
from tkinter import ttk


class DiskTable(tk.Frame):
    COLUMNS = (
        ("fs_name", "FS"),
        ("size", "Size"),
        ("used", "Used"),
        ("available", "Avail"),
        ("mount", "Mount"),
        ("usage_percent", "Use %"),
    )

    COLUMN_WIDTHS = {
        "fs_name": 55,
        "size": 50,
        "used": 50,
        "available": 50,
        "mount": 60,
        "usage_percent": 45,
    }

    MIN_VISIBLE_ROWS = 1
    MAX_VISIBLE_ROWS = 8

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
            columns=[key for key, _ in self.COLUMNS],
            show="headings",
            style="DiskStats.Treeview",
            height=self.MIN_VISIBLE_ROWS
        )

        for key, label in self.COLUMNS:
            self.tree.heading(key, text=label)

            self.tree.column(
                key,
                anchor="center",
                width=self.COLUMN_WIDTHS[key],
                minwidth=self.COLUMN_WIDTHS[key],
                stretch=False
            )

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree.tag_configure("evenrow", background=self.EVEN_ROW_COLOR)
        self.tree.tag_configure("oddrow", background=self.ODD_ROW_COLOR)

        self.v_scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )

        self.h_scrollbar = ttk.Scrollbar(
            self,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set
        )

        self.v_scrollbar.grid(row=0, column=1, sticky="ns")
        self.h_scrollbar.grid(row=1, column=0, sticky="ew")

    def update_disks(self, disk_stats):
        self.tree.delete(*self.tree.get_children())

        if not disk_stats:
            self.tree.configure(height=self.MIN_VISIBLE_ROWS)
            return

        visible_rows = max(
            self.MIN_VISIBLE_ROWS,
            min(len(disk_stats), self.MAX_VISIBLE_ROWS)
        )

        self.tree.configure(height=visible_rows)

        for index, entry in enumerate(disk_stats):
            tag = "evenrow" if index % 2 == 0 else "oddrow"

            self.tree.insert(
                "",
                "end",
                values=(
                    entry.fs_name,
                    f"{entry.size} {entry.units}",
                    f"{entry.used} {entry.units}",
                    f"{entry.available} {entry.units}",
                    entry.mount,
                    f"{entry.usage_percent}%"
                ),
                tags=(tag,)
            )