import tkinter as tk

class TopBar(tk.Frame):
    BASE_FONT_SIZE = 25
    MIN_FONT_SIZE = 10

    def __init__(self, parent, host, on_tab_change, on_disconnect):
        super().__init__(parent, bg="#292d30")

        self.host = host
        self.on_tab_change = on_tab_change
        self.on_disconnect = on_disconnect

        self._font_widgets = []
        self._base_min_width = None
        self._resize_job = None

        self.create_widgets()

        self.bind("<Configure>", self._on_resize)

    def create_widgets(self):
        for col, weight in enumerate([2, 1, 1, 1, 1, 1]):
            self.grid_columnconfigure(col, weight=weight)
        self.grid_rowconfigure(0, weight=1)

        self.connection_label = tk.Label(
            self,
            text=f"Connected to {self.host}",
            bg="#292d30",
            fg="#7ac2a2",
            font=("Roboto", 25, "bold")
        )

        self.connection_label.grid(row=0, column=0, sticky="nsew")

        self.performance_button = tk.Button(
            self,
            text="Performance",
            bg="#292d30",
            fg="#7ac2a2",
            font=("Roboto", 25, "bold"),
            activebackground="#333637",
            activeforeground="#7ac2a2",
            borderwidth=0,
            highlightthickness=0,
            takefocus=0,
            command=lambda: self.on_tab_change("performance")
        )

        self.performance_button.grid(row=0, column=1, sticky="nsew")

        self.log1_button = tk.Button(
            self,
            bg="#292d30",
            fg="#7ac2a2",
            activebackground="#333637",
            activeforeground="#7ac2a2",
            font=("Roboto", 25, "bold"),
            text="Authlogs",
            borderwidth=0,
            highlightthickness=0,
            takefocus=0,
            command=lambda: self.on_tab_change("log1")
        )

        self.log1_button.grid(row=0, column=2, sticky="nsew")

        self.log2_button = tk.Button(
            self,
            text="Syslogs",
            bg="#292d30",
            fg="#7ac2a2",
            activebackground="#333637",
            activeforeground="#7ac2a2",
            font=("Roboto", 25, "bold"),
            borderwidth=0,
            highlightthickness=0,
            takefocus=0,
            command=lambda: self.on_tab_change("log2")
        )

        self.log2_button.grid(row=0, column=3, sticky="nsew")

        self.log3_button = tk.Button(
            self,
            text="Kernlogs",
            bg="#292d30",
            fg="#7ac2a2",
            activebackground="#333637",
            activeforeground="#7ac2a2",
            font=("Roboto", 25, "bold"),
            borderwidth=0,
            highlightthickness=0,
            takefocus=0,
            command=lambda: self.on_tab_change("log3")
        )

        self.log3_button.grid(row=0, column=4, sticky="nsew")

        self.disconnect_button = tk.Button(
            self,
            text="Disconnect",
            bg="#292d30",
            fg="#e23535",
            activebackground="#f66d6b",
            activeforeground="#ffffff",
            borderwidth=0,
            highlightthickness=0,
            takefocus=0,
            font=("Roboto", 25, "bold"),

            command=self.on_disconnect
        )

        self.disconnect_button.grid(row=0, column=5, sticky="nsew")

        self.border = tk.Frame(
            self,
            bg="#202020",
            height=8
        )

        self.border.grid(row=1, column=0, columnspan=6, sticky="ew")

        self._font_widgets = [
            self.connection_label,
            self.performance_button,
            self.log1_button,
            self.log2_button,
            self.log3_button,
            self.disconnect_button,
        ]

        self.after_idle(self._measure_base_width)

    def _measure_base_width(self):
        self.update_idletasks()
        self._base_min_width = self.winfo_reqwidth()

    def _on_resize(self, event):
        if self._resize_job:
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(50, self._apply_font_scale)

    def _apply_font_scale(self):
        self._resize_job = None

        if not self._base_min_width:
            return

        current_width = self.winfo_width()
        scale = current_width / self._base_min_width
        scale = max(0.35, min(scale, 1.0))

        new_size = max(self.MIN_FONT_SIZE, round(self.BASE_FONT_SIZE * scale))
        new_font = ("Roboto", new_size, "bold")

        for widget in self._font_widgets:
            if widget.cget("font") != new_font:
                widget.config(font=new_font)