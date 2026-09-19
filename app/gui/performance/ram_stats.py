import logging
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

logging.getLogger("matplotlib").setLevel(logging.WARNING)


class RamStats(tk.Frame):
    LINE_COLOR = "#4566da"
    FILL_COLOR = "#4566da"
    GRID_COLOR = "#3a3f42"

    def __init__(self, parent):
        super().__init__(parent, bg="#292d30")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.figure = Figure(figsize=(2, 1.4), facecolor="#292d30")
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().configure(bg="#292d30", highlightthickness=0)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.values = []
        self._draw()

    def update_stats(self, ram_stats_history):
        if ram_stats_history:
            self.values = [entry.usage_percent for entry in ram_stats_history]
        else:
            self.values = []

        self._draw()

    def _draw(self):
        self.ax.clear()
        self.ax.set_facecolor("#292d30")

        values = self.values if self.values else [0]
        x = range(len(values))

        self.ax.plot(x, values, color=self.LINE_COLOR, linewidth=1.5)
        self.ax.fill_between(x, values, color=self.FILL_COLOR, alpha=0.25)

        self.ax.grid(color=self.GRID_COLOR, linewidth=0.6)
        self.ax.set_axisbelow(True)

        self.ax.set_ylim(0, 100)
        self.ax.set_xlim(0, max(len(values) - 1, 1))

        self.ax.set_xticks([])
        self.ax.tick_params(colors="#ffffff", labelsize=8)

        for spine in self.ax.spines.values():
            spine.set_color(self.GRID_COLOR)

        self.canvas.draw()