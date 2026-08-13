import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import matplotlib.pyplot as plt


DB_NAME = "bmi_history.db"


class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator - Advanced")
        self.root.geometry("900x650")
        self.root.minsize(820, 600)

        self.conn = sqlite3.connect(DB_NAME)
        self.create_database()

        self.current_bmi = None
        self.current_category = None

        self.setup_style()
        self.build_ui()
        self.load_users()
        self.update_history()

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def create_database(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bmi_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    category TEXT NOT NULL,
                    recorded_at TEXT NOT NULL
                )
            """)
            self.conn.commit()
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Could not create the database:\n{exc}")

    def setup_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("Heading.TLabel", font=("Segoe UI", 13, "bold"))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Treeview", rowheight=28, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def build_ui(self):
        main = ttk.Frame(self.root, padding=18)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="BMI Calculator", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            main,
            text="Calculate BMI, save records for multiple users, and visualize BMI trends.",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(0, 14))

        input_frame = ttk.LabelFrame(main, text="BMI Calculation", padding=14)
        input_frame.pack(fill="x")

        # User
        ttk.Label(input_frame, text="User name:").grid(row=0, column=0, sticky="w", padx=5, pady=7)
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(
            input_frame, textvariable=self.user_var, width=25, state="normal"
        )
        self.user_combo.grid(row=0, column=1, sticky="w", padx=5, pady=7)

        # Weight
        ttk.Label(input_frame, text="Weight (kg):").grid(row=1, column=0, sticky="w", padx=5, pady=7)
        self.weight_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.weight_var, width=28).grid(
            row=1, column=1, sticky="w", padx=5, pady=7
        )

        # Height
        ttk.Label(input_frame, text="Height (m):").grid(row=2, column=0, sticky="w", padx=5, pady=7)
        self.height_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.height_var, width=28).grid(
            row=2, column=1, sticky="w", padx=5, pady=7
        )

        ttk.Label(
            input_frame,
            text="Example: 70 kg and 1.75 m",
            foreground="gray"
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=5)

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=0, column=2, rowspan=4, padx=(35, 5), sticky="ns")

        ttk.Button(
            button_frame, text="Calculate & Save",
            command=self.calculate_and_save,
            style="Action.TButton"
        ).pack(fill="x", pady=4)

        ttk.Button(
            button_frame, text="Clear",
            command=self.clear_inputs
        ).pack(fill="x", pady=4)

        ttk.Button(
            button_frame, text="Show BMI Trend",
            command=self.show_trend
        ).pack(fill="x", pady=4)

        result_frame = ttk.LabelFrame(main, text="Result", padding=14)
        result_frame.pack(fill="x", pady=14)

        self.result_label = tk.Label(
            result_frame,
            text="Enter your details and click Calculate & Save.",
            font=("Segoe UI", 14, "bold"),
            padx=10, pady=10
        )
        self.result_label.pack(fill="x")

        ttk.Label(
            result_frame,
            text="BMI categories: Underweight < 18.5   |   Normal 18.5–24.9   |   Overweight 25–29.9   |   Obese ≥ 30",
            font=("Segoe UI", 9)
        ).pack()

        history_frame = ttk.LabelFrame(main, text="Saved BMI History", padding=10)
        history_frame.pack(fill="both", expand=True)

        columns = ("date", "user", "weight", "height", "bmi", "category")
        self.tree = ttk.Treeview(history_frame, columns=columns, show="headings")

        headings = {
            "date": "Date & Time",
            "user": "User",
            "weight": "Weight (kg)",
            "height": "Height (m)",
            "bmi": "BMI",
            "category": "Category"
        }
        widths = {
            "date": 150, "user": 120, "weight": 100,
            "height": 100, "bmi": 80, "category": 120
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor="center")

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.select_history_user)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main, textvariable=self.status_var, foreground="gray").pack(anchor="w", pady=(7, 0))

    @staticmethod
    def get_category(bmi):
        if bmi < 18.5:
            return "Underweight"
        if bmi < 25:
            return "Normal"
        if bmi < 30:
            return "Overweight"
        return "Obese"

    @staticmethod
    def get_category_color(category):
        return {
            "Underweight": "#d97706",
            "Normal": "#15803d",
            "Overweight": "#ca8a04",
            "Obese": "#dc2626"
        }.get(category, "#111827")

    def validate_inputs(self):
        username = self.user_var.get().strip()

        if not username:
            raise ValueError("Please enter a user name.")

        if len(username) > 50:
            raise ValueError("User name must be 50 characters or fewer.")

        try:
            weight = float(self.weight_var.get().strip())
            height = float(self.height_var.get().strip())
        except ValueError:
            raise ValueError("Weight and height must be numeric values.")

        if weight <= 0:
            raise ValueError("Weight must be greater than 0 kg.")

        if height <= 0:
            raise ValueError("Height must be greater than 0 m.")

        # Practical input limits to catch obvious mistakes.
        if weight > 500:
            raise ValueError("Please enter a realistic weight (500 kg or less).")

        if height > 3:
            raise ValueError("Please enter height in metres, e.g. 1.75.")

        return username, weight, height

    def calculate_and_save(self):
        try:
            username, weight, height = self.validate_inputs()

            bmi = weight / (height ** 2)
            bmi = round(bmi, 2)
            category = self.get_category(bmi)

            recorded_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO bmi_records
                (username, weight, height, bmi, category, recorded_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, weight, height, bmi, category, recorded_at))
            self.conn.commit()

            self.current_bmi = bmi
            self.current_category = category

            self.result_label.config(
                text=f"{username}'s BMI: {bmi:.2f}  —  {category}",
                fg=self.get_category_color(category)
            )

            self.status_var.set(f"Record saved for {username}.")
            self.load_users()
            self.update_history()

        except ValueError as exc:
            messagebox.showwarning("Invalid Input", str(exc))
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Could not save the BMI record:\n{exc}")

    def update_history(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT recorded_at, username, weight, height, bmi, category
                FROM bmi_records
                ORDER BY id DESC
                LIMIT 100
            """)
            rows = cursor.fetchall()

            for row in rows:
                self.tree.insert(
                    "", "end",
                    values=(
                        row[0], row[1],
                        f"{row[2]:.2f}",
                        f"{row[3]:.2f}",
                        f"{row[4]:.2f}",
                        row[5]
                    )
                )
        except sqlite3.Error as exc:
            messagebox.showerror("Database Error", f"Could not read history:\n{exc}")

    def load_users(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT username FROM bmi_records ORDER BY username")
            users = [row[0] for row in cursor.fetchall()]
            self.user_combo["values"] = users
        except sqlite3.Error:
            self.user_combo["values"] = []

    def select_history_user(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        if values:
            self.user_var.set(values[1])
            self.status_var.set(f"Selected history for {values[1]}.")

    def show_trend(self):
        username = self.user_var.get().strip()

        if not username:
            messagebox.showwarning("User Required", "Enter or select a user name first.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT recorded_at, bmi
                FROM bmi_records
                WHERE username = ?
                ORDER BY id ASC
            """, (username,))
            rows = cursor.fetchall()

            if not rows:
                messagebox.showinfo(
                    "No Data",
                    f"No BMI records found for '{username}'. Calculate and save a BMI first."
                )
                return

            dates = [datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S") for row in rows]
            bmis = [row[1] for row in rows]

            plt.figure(figsize=(9, 5))
            plt.plot(dates, bmis, marker="o", linewidth=2)
            plt.axhline(18.5, linestyle="--", linewidth=1, label="18.5")
            plt.axhline(25, linestyle="--", linewidth=1, label="25")
            plt.axhline(30, linestyle="--", linewidth=1, label="30")

            plt.title(f"BMI Trend — {username}")
            plt.xlabel("Date / Time")
            plt.ylabel("BMI")
            plt.grid(True, alpha=0.3)
            plt.legend()
            plt.gcf().autofmt_xdate()
            plt.tight_layout()
            plt.show()

        except (sqlite3.Error, ValueError) as exc:
            messagebox.showerror("Trend Error", f"Could not display BMI trend:\n{exc}")

    def clear_inputs(self):
        self.user_var.set("")
        self.weight_var.set("")
        self.height_var.set("")
        self.current_bmi = None
        self.current_category = None
        self.result_label.config(
            text="Enter your details and click Calculate & Save.",
            fg="black"
        )
        self.status_var.set("Inputs cleared.")

    def close_app(self):
        try:
            self.conn.close()
        finally:
            self.root.destroy()


def main():
    root = tk.Tk()
    BMICalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
