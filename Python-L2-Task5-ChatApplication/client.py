import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5000

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("OIBSIP Chat Application")
        self.root.geometry("720x560")
        self.root.minsize(600, 450)
        self.sock = None
        self.connected = False
        self.build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def build_ui(self):
        top = tk.Frame(self.root, padx=10, pady=10)
        top.pack(fill="x")
        tk.Label(top, text="Server:").grid(row=0, column=0, sticky="w")
        self.host_entry = tk.Entry(top, width=18)
        self.host_entry.insert(0, DEFAULT_HOST)
        self.host_entry.grid(row=0, column=1, padx=5)
        tk.Label(top, text="Port:").grid(row=0, column=2, sticky="w")
        self.port_entry = tk.Entry(top, width=8)
        self.port_entry.insert(0, str(DEFAULT_PORT))
        self.port_entry.grid(row=0, column=3, padx=5)
        tk.Label(top, text="Username:").grid(row=0, column=4, sticky="w")
        self.username_entry = tk.Entry(top, width=15)
        self.username_entry.grid(row=0, column=5, padx=5)
        self.connect_button = tk.Button(
            top, text="Connect", command=self.connect
        )
        self.connect_button.grid(row=0, column=6, padx=5)
        self.chat_box = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            state="disabled",
            font=("Segoe UI", 11)
        )
        self.chat_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        bottom = tk.Frame(self.root, padx=10, pady=10)
        bottom.pack(fill="x")
        self.message_entry = tk.Entry(bottom, font=("Segoe UI", 11))
        self.message_entry.pack(side="left", fill="x", expand=True)
        self.message_entry.bind("<Return>", lambda event: self.send_message())
        self.send_button = tk.Button(
            bottom, text="Send", command=self.send_message, state="disabled"
        )
        self.send_button.pack(side="left", padx=(8, 0))
        self.status_label = tk.Label(
            self.root, text="Not connected", anchor="w", padx=10
        )
        self.status_label.pack(fill="x")

    def add_message(self, message):
        self.chat_box.config(state="normal")
        self.chat_box.insert("end", message + "\n")
        self.chat_box.see("end")
        self.chat_box.config(state="disabled")

    def connect(self):
        if self.connected:
            return
        host = self.host_entry.get().strip()
        username = self.username_entry.get().strip()
        try:
            port = int(self.port_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Port", "Enter a valid port number.")
            return
        if not host or not username:
            messagebox.showwarning(
                "Missing Information",
                "Enter both server address and username."
            )
            return
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            prompt = self.sock.recv(1024).decode("utf-8")
            if "username" in prompt.lower():
                self.sock.send(username.encode("utf-8"))
            self.connected = True
            self.connect_button.config(state="disabled")
            self.send_button.config(state="normal")
            self.message_entry.focus_set()
            self.status_label.config(text=f"Connected to {host}:{port}")
            threading.Thread(
                target=self.receive_messages,
                daemon=True
            ).start()
        except OSError as error:
            if self.sock:
                self.sock.close()
            self.sock = None
            messagebox.showerror(
                "Connection Error",
                f"Could not connect to the server.\n\n{error}"
            )

    def receive_messages(self):
        while self.connected:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                message = data.decode("utf-8")
                self.root.after(0, self.add_message, message)
            except OSError:
                break
        self.root.after(0, self.connection_lost)

    def connection_lost(self):
        if self.connected:
            self.add_message("[SYSTEM] Connection to server was lost.")
        self.connected = False
        self.send_button.config(state="disabled")
        self.connect_button.config(state="normal")
        self.status_label.config(text="Disconnected")

    def send_message(self):
        if not self.connected:
            return
        message = self.message_entry.get().strip()
        if not message:
            return
        try:
            self.sock.send(message.encode("utf-8"))
            self.message_entry.delete(0, "end")
            if message.lower() == "/quit":
                self.close()
        except OSError:
            self.connection_lost()

    def close(self):
        if self.connected:
            try:
                self.sock.send(b"/quit")
            except OSError:
                pass
        self.connected = False
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
        self.root.destroy()
if __name__ == "__main__":
    root = tk.Tk()
    ChatClient(root)
    root.mainloop()
