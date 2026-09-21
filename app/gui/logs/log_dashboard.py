import logging
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

logging.getLogger("matplotlib").setLevel(logging.WARNING)


class LogLevelGauge(tk.Frame):
    BG_COLOR = "#3a3f42"

    def __init__(self, parent, level, color):
        super().__init__(parent, bg="#292d30")

        self.level = level
        self.color = color

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.figure = Figure(figsize=(1.3, 1.3), facecolor="#292d30")
        self.figure.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().configure(bg="#292d30", highlightthickness=0)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.caption = tk.Label(
            self,
            text=level,
            bg="#292d30",
            fg=color,
            font=("Roboto", 11, "bold")
        )

        self.caption.grid(row=1, column=0, pady=(2, 8))

        self.update_value(0, 0)

    def update_value(self, count, total):
        self.ax.clear()

        remainder = max(total - count, 0)

        if total <= 0:
            values = [1]
            colors = [self.BG_COLOR]
        else:
            values = [count, remainder]
            colors = [self.color, self.BG_COLOR]

        self.ax.pie(
            values,
            colors=colors,
            startangle=90,
            counterclock=False,
            wedgeprops=dict(width=0.32, edgecolor="#292d30", linewidth=1)
        )

        self.ax.text(
            0, 0,
            str(count),
            ha="center",
            va="center",
            color="#ffffff",
            fontsize=13,
            fontweight="bold"
        )

        self.ax.set_aspect("equal")
        self.canvas.draw()


class LogDashboard(tk.Frame):
    LEVELS = (
        ("INFO", "#3dd840"),
        ("WARNING", "#e2c53c"),
        ("ERROR", "#e23535"),
        ("CRITICAL", "#ff2d55"),
    )

    def __init__(self, parent):
        super().__init__(parent, bg="#292d30")

        self.grid_columnconfigure(0, weight=1)

        for i in range(len(self.LEVELS)):
            self.grid_rowconfigure(i, weight=1)

        self.gauges = {}

        for index, (level, color) in enumerate(self.LEVELS):
            gauge = LogLevelGauge(self, level, color)

            gauge.grid(
                row=index,
                column=0,
                sticky="nsew",
                padx=10,
                pady=10
            )

            self.gauges[level] = gauge

    def update_logs(self, logs):
        total = len(logs) if logs else 0
        counts = {level: 0 for level, _ in self.LEVELS}

        if logs:
            for entry in logs:
                if entry.level in counts:
                    counts[entry.level] += 1

        for level, gauge in self.gauges.items():
            gauge.update_value(counts[level], total)