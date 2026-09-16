import tkinter as tk


class TopBar(tk.Frame):
    def __init__(self, parent, host, on_tab_change, on_disconnect):
        super().__init__(parent, bg="#292d30")

        self.host = host
        self.on_tab_change = on_tab_change
        self.on_disconnect = on_disconnect

        self.create_widgets()

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
            text="Log 1",
            borderwidth=0,
            highlightthickness=0,
            takefocus=0,
            command=lambda: self.on_tab_change("log1")
        )

        self.log1_button.grid(row=0, column=2, sticky="nsew")

        self.log2_button = tk.Button(
            self, 
            text="Log 2",
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
            text="Log 3",
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