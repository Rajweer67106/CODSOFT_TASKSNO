# Task 1 – Voice Assistant

This project is part of my OASIS INFOBYTE Python Programming Internship.

I built this voice assistant to practice speech recognition, text-to-speech, API integration, web browsing, reminders, and basic automation using Python.

## Features

- Voice input through a microphone
- Text-to-speech responses
- Greeting and help commands
- Current date and time
- Google web search
- Open Google and YouTube
- Weather information using OpenWeatherMap
- Voice-based reminders
- Email functionality using SMTP
- Basic error handling

## Technologies Used

- Python
- SpeechRecognition
- pyttsx3
- Requests
- PyAudio
- OpenWeatherMap API
- SMTP

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

A working microphone is required.

## API and Security

The weather feature uses `OPENWEATHER_API_KEY`.

The email feature uses `VOICE_EMAIL`, `VOICE_EMAIL_PASSWORD`, and `VOICE_EMAIL_RECEIVER`.

Keep API keys and passwords private. Do not upload them to GitHub.

## Project Structure

```text
Python-L2-Task1-VoiceAssistant/
├── app.py
├── requirements.txt
└── README.md
```

## What I Learned

This project helped me understand voice input, text-to-speech, APIs, web automation, background reminders, SMTP, and error handling in Python.
