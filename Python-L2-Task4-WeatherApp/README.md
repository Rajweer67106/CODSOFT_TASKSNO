# Task 4 – Weather App

This project is part of my **OASIS INFOBYTE Python Programming Internship**.

I built this weather application to practice working with a real-world API and
displaying the returned information in a simple graphical interface.

## Features

- Search weather by city
- Current temperature
- Celsius/Fahrenheit toggle
- Weather condition
- Feels-like temperature
- Humidity
- Wind speed
- Atmospheric pressure
- Weather icon
- User-friendly GUI
- Invalid city handling
- API-key error handling
- Network and timeout handling
- API rate-limit handling

## Technologies Used

- Python
- Tkinter
- Requests
- Pillow
- OpenWeatherMap API

## How to Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Set your OpenWeatherMap API key as an environment variable.

### Windows PowerShell

```powershell
$env:OPENWEATHER_API_KEY="YOUR_API_KEY"
```

### Windows Command Prompt

```cmd
set OPENWEATHER_API_KEY=YOUR_API_KEY
```

Then run:

```bash
python app.py
```

## Security

Do not put your API key directly inside `app.py` and do not upload it to GitHub.

## Project Structure

```text
Python-L2-Task4-WeatherApp/
├── app.py
├── requirements.txt
└── README.md
```

## What I Learned

This project helped me understand API requests, JSON responses, GUI development,
error handling, unit conversion, and displaying data received from an external service.
