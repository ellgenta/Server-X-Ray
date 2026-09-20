import tkinter as tk
from tkinter import ttk


class RamSwapTable(tk.Frame):
    ROWS = (
        ("total", "Total"),
        ("used", "Used"),
        ("free", "Free"),
        ("shared", "Shared"),
        ("cache", "Cache"),
        ("available", "Available"),
        ("usage_percent", "Usage %"),
    )

    SWAP_ONLY_FIELDS = ("total", "used", "free", "usage_percent")

    EVEN_ROW_COLOR = "#1f2226"
    ODD_ROW_COLOR = "#292d30"

    def __init__(self, parent):
        super().__init__(parent, bg="#292d30")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self.style.configure(
            "RamSwap.Treeview",
            background="#292d30",
            fieldbackground="#292d30",
            foreground="#ffffff",
            font=("Roboto", 11),
            rowheight=24,
            borderwidth=0
        )

        self.style.configure(
            "RamSwap.Treeview.Heading",
            background="#202020",
            foreground="#7ac2a2",
            font=("Roboto", 11, "bold"),
            borderwidth=0
        )

        self.style.map(
            "RamSwap.Treeview",
            background=[("selected", "#333637")],
            foreground=[("selected", "#ffffff")]
        )

        self.style.map(
            "RamSwap.Treeview.Heading",
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
            columns=("metric", "ram", "swap"),
            show="headings",
            style="RamSwap.Treeview",
            height=len(self.ROWS)
        )

        self.tree.heading("metric", text="")
        self.tree.heading("ram", text="RAM")
        self.tree.heading("swap", text="Swap")

        self.tree.column("metric", anchor="w", width=80, minwidth=60, stretch=True)
        self.tree.column("ram", anchor="center", width=60, minwidth=45, stretch=True)
        self.tree.column("swap", anchor="center", width=60, minwidth=45, stretch=True)

        self.tree.grid(row=0, column=0, sticky="nsew")

        self.tree.tag_configure("evenrow", background=self.EVEN_ROW_COLOR)
        self.tree.tag_configure("oddrow", background=self.ODD_ROW_COLOR)

        self.caption = tk.Label(
            self,
            text="RAM / Swap Load",
            bg="#292d30",
            fg="#ffffff",
            font=("Roboto", 12)
        )

        self.caption.grid(row=1, column=0, pady=(10, 0))

    def _format_value(self, entry, key, units):
        if entry is None:
            return "-"

        value = getattr(entry, key, None)

        if value is None:
            return "-"

        if key == "usage_percent":
            return f"{value}%"

        return f"{value} {units}"

    def update_stats(self, ram_stats_history, swap_stats):
        self.tree.delete(*self.tree.get_children())

        latest_ram = ram_stats_history[-1] if ram_stats_history else None

        for index, (key, label) in enumerate(self.ROWS):
            tag = "evenrow" if index % 2 == 0 else "oddrow"

            ram_units = latest_ram.units if latest_ram else ""
            ram_display = self._format_value(latest_ram, key, ram_units)

            if key in self.SWAP_ONLY_FIELDS:
                swap_units = swap_stats.units if swap_stats else ""
                swap_display = self._format_value(swap_stats, key, swap_units)
            else:
                swap_display = "-"

            self.tree.insert(
                "",
                "end",
                values=(label, ram_display, swap_display),
                tags=(tag,)
            )