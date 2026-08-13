import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests
from PIL import Image, ImageTk

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("760x650")
        self.root.resizable(False, False)
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.unit = "metric"
        self.icon_image = None
        self.build_ui()

    def build_ui(self):
        title = ttk.Label(
            self.root,
            text="Weather App",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(pady=(20, 10))
        search_frame = ttk.Frame(self.root)
        search_frame.pack(pady=10)
        self.city_entry = ttk.Entry(search_frame, width=32, font=("Segoe UI", 12))
        self.city_entry.grid(row=0, column=0, padx=6)
        self.city_entry.bind("<Return>", lambda event: self.search_weather())
        ttk.Button(search_frame, text="Search", command=self.search_weather
        ).grid(row=0, column=1, padx=6)
        self.unit_button = ttk.Button(
            search_frame, text="Switch to °F", command=self.toggle_unit
        )
        self.unit_button.grid(row=0, column=2, padx=6)
        self.status = ttk.Label(self.root, text="Enter a city to get the weather.")
        self.status.pack(pady=5)
        self.location_label = ttk.Label(
            self.root, text="—", font=("Segoe UI", 18, "bold")
        )
        self.location_label.pack(pady=(15, 5))
        self.icon_label = ttk.Label(self.root)
        self.icon_label.pack()
        self.temperature_label = ttk.Label(
            self.root, text="—", font=("Segoe UI", 32, "bold")
        )
        self.temperature_label.pack(pady=5)
        self.condition_label = ttk.Label(self.root, text="—", font=("Segoe UI", 14))
        self.condition_label.pack(pady=5)
        info = ttk.Frame(self.root)
        info.pack(pady=20)
        self.feels_label = ttk.Label(info, text="Feels like: —")
        self.feels_label.grid(row=0, column=0, padx=20, pady=8)
        self.humidity_label = ttk.Label(info, text="Humidity: —")
        self.humidity_label.grid(row=0, column=1, padx=20, pady=8)
        self.wind_label = ttk.Label(info, text="Wind: —")
        self.wind_label.grid(row=1, column=0, padx=20, pady=8)
        self.pressure_label = ttk.Label(info, text="Pressure: —")
        self.pressure_label.grid(row=1, column=1, padx=20, pady=8)
        self.updated_label = ttk.Label(self.root, text="")
        self.updated_label.pack(pady=10)
        note = ttk.Label(self.root,
            text="Weather data provided by OpenWeatherMap",
            font=("Segoe UI", 9)
        )
        note.pack(side="bottom", pady=12)

    def toggle_unit(self):
        if self.unit == "metric":
            self.unit = "imperial"
            self.unit_button.config(text="Switch to °C")
        else:
            self.unit = "metric"
            self.unit_button.config(text="Switch to °F")
        if self.city_entry.get().strip():
            self.search_weather()

    def search_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Missing City", "Please enter a city name.")
            return
        if not self.api_key:
            messagebox.showerror(
                "API Key Missing",
                "Set the OPENWEATHER_API_KEY environment variable before running the app."
            )
            return
        self.status.config(text="Loading weather...")
        self.root.update_idletasks()
        try:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "q": city,
                    "appid": self.api_key,
                    "units": self.unit
                },
                timeout=10
            )
            if response.status_code == 404:
                messagebox.showerror(
                    "City Not Found",
                    f"Could not find weather data for '{city}'."
                )
                self.status.config(text="City not found.")
                return
            if response.status_code == 401:
                messagebox.showerror(
                    "Invalid API Key",
                    "The OpenWeatherMap API key is invalid."
                )
                self.status.config(text="Invalid API key.")
                return
            if response.status_code == 429:
                messagebox.showerror(
                    "API Limit",
                    "The weather API request limit has been reached."
                )
                self.status.config(text="API limit reached.")
                return
            response.raise_for_status()
            data = response.json()
            self.display_weather(data)
        except requests.exceptions.Timeout:
            messagebox.showerror(
                "Timeout",
                "The weather service took too long to respond."
            )
            self.status.config(text="Request timed out.")
        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Connection Error",
                "Could not connect to the weather service. Check your internet connection."
            )
            self.status.config(text="Connection error.")
        except requests.exceptions.RequestException as error:
            messagebox.showerror(
                "Request Error",
                f"Could not retrieve weather data.\n\n{error}"
            )
            self.status.config(text="Request failed.")
        except (KeyError, ValueError):
            messagebox.showerror(
                "Data Error",
                "The weather service returned an unexpected response."
            )
            self.status.config(text="Invalid weather data.")
    def display_weather(self, data):
        city = data["name"]
        country = data["sys"].get("country", "")
        weather = data["weather"][0]
        main = data["main"]
        wind = data.get("wind", {})
        symbol = "°C" if self.unit == "metric" else "°F"
        wind_unit = "m/s" if self.unit == "metric" else "mph"
        self.location_label.config(text=f"{city}, {country}")
        self.temperature_label.config(
            text=f"{main['temp']:.1f}{symbol}"
        )
        self.condition_label.config(
            text=weather["description"].title()
        )
        self.feels_label.config(
            text=f"Feels like: {main['feels_like']:.1f}{symbol}"
        )
        self.humidity_label.config(
            text=f"Humidity: {main['humidity']}%"
        )
        self.wind_label.config(
            text=f"Wind: {wind.get('speed', 0):.1f} {wind_unit}"
        )
        self.pressure_label.config(
            text=f"Pressure: {main['pressure']} hPa"
        )
        timestamp = data.get("dt")
        if timestamp:
            local_time = datetime.fromtimestamp(timestamp).strftime(
                "%d %B %Y, %I:%M %p"
            )
            self.updated_label.config(text=f"Updated: {local_time}")
        self.load_icon(weather.get("icon"))
        self.status.config(text="Weather updated successfully.")

    def load_icon(self, icon_code):
        if not icon_code:
            self.icon_label.config(image="")
            return
        try:
            url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
            image_data = requests.get(url, timeout=10).content
            temp_file = Path("weather_icon.png")
            temp_file.write_bytes(image_data)
            image = Image.open(temp_file).convert("RGBA")
            image = image.resize((100, 100))
            self.icon_image = ImageTk.PhotoImage(image)
            self.icon_label.config(image=self.icon_image)
            # Local temporary file is only used for displaying the icon.
            try:
                temp_file.unlink()
            except OSError:
                pass
        except (requests.RequestException, OSError):
            self.icon_label.config(image="")

if __name__ == "__main__":
    from pathlib import Path

    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
