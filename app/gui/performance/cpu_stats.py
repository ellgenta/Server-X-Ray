import logging
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

logging.getLogger("matplotlib").setLevel(logging.WARNING)


class CPUStats(tk.Frame):
    BAR_LABELS = ("Last minute", "Last 5 minutes", "Last 15 minutes")

    GREEN = "#7ac2a2"
    YELLOW = "#e2c53c"
    RED = "#e23535"

    def __init__(self, parent):
        super().__init__(parent, bg="#292d30")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.figure = Figure(facecolor="#292d30")
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().configure(bg="#292d30", highlightthickness=0)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.canvas.get_tk_widget().bind("<Configure>", lambda event: self.canvas.draw_idle())

        self.values = (0.0, 0.0, 0.0)
        self._draw()

    def update_stats(self, load_average_stats):
        if load_average_stats is None:
            self.values = (0.0, 0.0, 0.0)
        else:
            self.values = (
                load_average_stats.last_1,
                load_average_stats.last_5,
                load_average_stats.last_15
            )

        self._draw()

    def _color_for(self, value):
        if value < 0.5:
            return self.GREEN
        if value <= 1:
            return self.YELLOW
        return self.RED

    def _draw(self):
        self.ax.clear()
        self.ax.set_facecolor("#292d30")

        colors = [self._color_for(value) for value in self.values]

        bars = self.ax.bar(self.BAR_LABELS, self.values, color=colors)
        self.ax.bar_label(bars, fmt="%.2f", color="#ffffff", padding=4)

        self.ax.tick_params(colors="#ffffff", labelsize=10)

        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.ax.set_yticks([])
        self.ax.set_ylim(0, max(max(self.values), 1.0) * 1.2)

        self.canvas.draw()