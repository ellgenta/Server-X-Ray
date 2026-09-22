import tkinter as tk
import threading
from tkinter import messagebox
from ssh.credentials import ServerCredentials
from controllers.app_controller import ControllerError

class LoginPage(tk.Frame):
    def __init__(self, parent, controller, on_login_success):
        super().__init__(parent, bg="#282a2d")

        self.controller = controller

        self.on_login_success = on_login_success

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.form_frame = tk.Frame(self, bg="#282a2d")
        self.form_frame.grid(
            row=0,
            column=0,
        )

        self.title_label = tk.Label(
            self.form_frame, 
            text="Server X-Ray", 
            fg="#7ac2a2", 
            bg="#282a2d",
            font=("Roboto", 60, "bold"),
        )

        self.ip_address_label = tk.Label(
            self.form_frame, 
            text="Server IP Address:", 
            fg="#7ac2a2", 
            bg="#282a2d",
            font=("Roboto", 25)
        )
        self.ip_address_entry = tk.Entry(self.form_frame, font=("Roboto", 16))

        self.username_label = tk.Label(
            self.form_frame, 
            text="Username:", 
            fg="#7ac2a2", 
            bg="#282a2d",
            font=("Roboto", 25)
        )
        self.username_entry = tk.Entry(self.form_frame, font=("Roboto", 16))

        self.password_label = tk.Label(
            self.form_frame, 
            text="Password:", 
            fg="#7ac2a2", 
            bg="#282a2d",
            font=("Roboto", 25)
        )
        self.password_entry = tk.Entry(self.form_frame, font=("Roboto", 16), show="*")

        self.connect_button = tk.Button(
            self.form_frame,
            text="Connect",
            font=("Roboto", 18),
            bg="#7ac2a2",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            takefocus=0,
            activebackground="#7a88c2",
            command=self.connect
        )

        self.connect_button.grid(row=7, column=0, pady=40)

        self.title_label.grid(pady=(0, 150), row=0, column=0)

        self.ip_address_label.grid(row=1, column=0)
        self.ip_address_entry.grid(row=2, column=0, pady=10)

        self.username_label.grid(row=3, column=0)
        self.username_entry.grid(row=4, column=0, pady=10)

        self.password_label.grid(row=5, column=0)
        self.password_entry.grid(row=6, column=0, pady=10)

    def connect(self):
        host = self.ip_address_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        credentials = ServerCredentials(
            host=host,
            username=username,
            password=password,
        )

        self.connect_button.configure(state="disabled", text="Connecting...")

        threading.Thread(
            target=self._connect_in_background,
            args=(credentials, host),
            daemon=True
        ).start()

    def _connect_in_background(self, credentials, host):
        try:
            self.controller.connect(credentials)
        except ControllerError as er:
            error_message = str(er)
            self.after(0, lambda: self._on_connect_error(host, error_message))
            return

        self.after(0, self._on_connect_success)

    def _on_connect_success(self):
        self.on_login_success()

    def _on_connect_error(self, host, error_message):
        self.connect_button.configure(state="normal", text="Connect")

        messagebox.showerror(
            title=f"Connection to {host} failed",
            message=error_message
        )