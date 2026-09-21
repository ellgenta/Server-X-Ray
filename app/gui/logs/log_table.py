import tkinter as tk
from tkinter import ttk


class LogTable(tk.Frame):
    COLUMNS = (
        ("timestamp", "Timestamp", 90),
        ("user", "User", 90),
        ("message", "Message", 260),
        ("level", "Level", 90),
    )

    LEVEL_COLORS = {
        "INFO": "#ffffff",
        "WARNING": "#e2c53c",
        "ERROR": "#e23535",
        "CRITICAL": "#b20a0a",
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
            "LogTable.Treeview",
            background="#292d30",
            fieldbackground="#292d30",
            foreground="#ffffff",
            font=("Roboto", 11),
            rowheight=26,
            borderwidth=0
        )

        self.style.configure(
            "LogTable.Treeview.Heading",
            background="#202020",
            foreground="#7ac2a2",
            font=("Roboto", 11, "bold"),
            borderwidth=0
        )

        self.style.map(
            "LogTable.Treeview",
            background=[("selected", "#333637")],
            foreground=[("selected", "#ffffff")]
        )

        self.style.map(
            "LogTable.Treeview.Heading",
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
            style="LogTable.Treeview"
        )

        for key, label, width in self.COLUMNS:
            self.tree.heading(key, text=label)

            self.tree.column(
                key,
                anchor="center" if key != "message" else "w",
                width=width,
                minwidth=width,
                stretch=(key == "message")
            )

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree.tag_configure("evenrow", background=self.EVEN_ROW_COLOR)
        self.tree.tag_configure("oddrow", background=self.ODD_ROW_COLOR)

        for level, color in self.LEVEL_COLORS.items():
            self.tree.tag_configure(f"level_{level}", foreground=color)

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

    def update_logs(self, logs):
        self.tree.delete(*self.tree.get_children())

        if not logs:
            return

        for index, entry in enumerate(reversed(logs)):
            zebra_tag = "evenrow" if index % 2 == 0 else "oddrow"
            level_tag = f"level_{entry.level}"

            self.tree.insert(
                "",
                "end",
                values=(
                    entry.timestamp.strftime("%H:%M:%S"),
                    entry.user,
                    entry.message,
                    entry.level
                ),
                tags=(zebra_tag, level_tag)
            )