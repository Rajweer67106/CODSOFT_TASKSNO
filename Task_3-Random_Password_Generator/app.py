import secrets
import string
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip

AMBIGUOUS = set("O0oIl1|")


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Random Password Generator")
        self.root.geometry("760x650")
        self.root.minsize(700, 600)

        self.history = []
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=False)
        self.length_var = tk.IntVar(value=16)
        self.password_var = tk.StringVar()
        self.strength_var = tk.StringVar(value="Strength: —")
        self.status_var = tk.StringVar(value="Ready")

        self.build_ui()

    def build_ui(self):
        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Secure Password Generator",
                  font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(
            main,
            text="Generate strong passwords using Python's cryptographically secure secrets module."
        ).pack(anchor="w", pady=(0, 14))

        settings = ttk.LabelFrame(main, text="Password Settings", padding=14)
        settings.pack(fill="x")
        settings.columnconfigure(1, weight=1)

        ttk.Label(settings, text="Password length:").grid(
            row=0, column=0, sticky="w", padx=5, pady=7)

        self.length_scale = ttk.Scale(
            settings, from_=8, to=64, orient="horizontal",
            command=self.update_length_label)
        self.length_scale.set(16)
        self.length_scale.grid(row=0, column=1, sticky="ew", padx=10)

        self.length_label = ttk.Label(settings, text="16 characters")
        self.length_label.grid(row=0, column=2, sticky="w", padx=5)

        ttk.Label(settings, text="Character types:").grid(
            row=1, column=0, sticky="nw", padx=5, pady=10)

        checks = ttk.Frame(settings)
        checks.grid(row=1, column=1, columnspan=2, sticky="w")

        ttk.Checkbutton(checks, text="Uppercase (A-Z)",
                        variable=self.upper_var).grid(row=0, column=0, sticky="w", padx=(0, 20))
        ttk.Checkbutton(checks, text="Lowercase (a-z)",
                        variable=self.lower_var).grid(row=0, column=1, sticky="w")
        ttk.Checkbutton(checks, text="Numbers (0-9)",
                        variable=self.number_var).grid(row=1, column=0, sticky="w", padx=(0, 20))
        ttk.Checkbutton(checks, text="Symbols (!@#$...)",
                        variable=self.symbol_var).grid(row=1, column=1, sticky="w")

        ttk.Checkbutton(
            settings,
            text="Exclude ambiguous characters (O, 0, I, l, 1, |)",
            variable=self.ambiguous_var
        ).grid(row=2, column=1, columnspan=2, sticky="w", pady=10)

        result = ttk.LabelFrame(main, text="Generated Password", padding=14)
        result.pack(fill="x", pady=14)

        ttk.Entry(
            result, textvariable=self.password_var,
            font=("Consolas", 16), state="readonly"
        ).pack(fill="x", pady=(0, 10))

        info = ttk.Frame(result)
        info.pack(fill="x")
        ttk.Label(info, textvariable=self.strength_var,
                  font=("Segoe UI", 11, "bold")).pack(side="left")
        ttk.Button(info, text="Copy to Clipboard",
                   command=self.copy_password).pack(side="right")

        buttons = ttk.Frame(main)
        buttons.pack(fill="x")

        ttk.Button(buttons, text="Generate Password",
                   command=self.generate_password).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Generate Another",
                   command=self.generate_password).pack(side="left", padx=8)
        ttk.Button(buttons, text="Clear",
                   command=self.clear_password).pack(side="left", padx=8)

        history_frame = ttk.LabelFrame(
            main, text="Session History — Last 5 Passwords", padding=10)
        history_frame.pack(fill="both", expand=True, pady=(14, 0))

        self.history_list = tk.Listbox(
            history_frame, height=7, font=("Consolas", 11))
        self.history_list.pack(fill="both", expand=True)

        ttk.Label(main, textvariable=self.status_var,
                  foreground="gray").pack(anchor="w", pady=(7, 0))

    def update_length_label(self, value):
        length = int(round(float(value)))
        self.length_var.set(length)
        self.length_label.config(text=f"{length} characters")

    def selected_sets(self):
        sets = []
        if self.upper_var.get():
            sets.append(string.ascii_uppercase)
        if self.lower_var.get():
            sets.append(string.ascii_lowercase)
        if self.number_var.get():
            sets.append(string.digits)
        if self.symbol_var.get():
            sets.append(string.punctuation)
        return sets

    def clean_charset(self, charset):
        if not self.ambiguous_var.get():
            return charset
        return "".join(c for c in charset if c not in AMBIGUOUS)

    def generate_password(self):
        length = self.length_var.get()
        selected = self.selected_sets()

        if length < 8:
            messagebox.showwarning("Invalid Length",
                                   "Password length must be at least 8 characters.")
            return

        if len(selected) < 2:
            messagebox.showwarning(
                "Character Types Required",
                "Please select at least 2 character types.")
            return

        selected = [self.clean_charset(s) for s in selected]
        if any(not s for s in selected):
            messagebox.showwarning(
                "Invalid Selection",
                "A selected character type has no usable characters.")
            return

        # Guarantee at least one character from every selected type.
        chars = [secrets.choice(s) for s in selected]
        combined = "".join(selected)

        for _ in range(length - len(chars)):
            chars.append(secrets.choice(combined))

        # Secure Fisher-Yates shuffle.
        for i in range(len(chars) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            chars[i], chars[j] = chars[j], chars[i]

        password = "".join(chars)
        self.password_var.set(password)
        self.update_strength(password, len(selected))
        self.history.insert(0, password)
        self.history = self.history[:5]

        self.history_list.delete(0, tk.END)
        for item in self.history:
            self.history_list.insert(tk.END, item)

        self.status_var.set("New secure password generated.")

    def update_strength(self, password, type_count):
        length = len(password)
        if length >= 20 and type_count >= 4:
            strength = "Very Strong"
        elif length >= 16 and type_count >= 3:
            strength = "Strong"
        elif length >= 12 and type_count >= 2:
            strength = "Medium"
        else:
            strength = "Weak"
        self.strength_var.set(f"Strength: {strength}")

    def copy_password(self):
        password = self.password_var.get()
        if not password:
            messagebox.showinfo("Nothing to Copy",
                                "Generate a password first.")
            return
        try:
            pyperclip.copy(password)
            self.status_var.set("Password copied to clipboard.")
        except pyperclip.PyperclipException as exc:
            messagebox.showerror("Clipboard Error", str(exc))

    def clear_password(self):
        self.password_var.set("")
        self.strength_var.set("Strength: —")
        self.status_var.set("Password cleared.")


def main():
    root = tk.Tk()
    PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
