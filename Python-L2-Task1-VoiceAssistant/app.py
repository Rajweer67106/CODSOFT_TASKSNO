import datetime
import os
import threading
import time
import webbrowser
import smtplib
import pyttsx3
import requests
import speech_recognition as sr

engine = pyttsx3.init()
engine.setProperty("rate", 170)
recognizer = sr.Recognizer()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            print("You:", command)
            return command.lower()
        except sr.WaitTimeoutError:
            speak("I did not hear anything.")
        except sr.UnknownValueError:
            speak("Sorry, I could not understand that.")
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
    return ""


def tell_date_time():
    now = datetime.datetime.now()
    speak(f"The time is {now.strftime('%I:%M %p')}.")
    speak(f"Today's date is {now.strftime('%d %B %Y')}.")


def search_web(query):
    if not query:
        speak("Please tell me what you want to search for.")
        return
    speak(f"Searching for {query}.")
    webbrowser.open("https://www.google.com/search?q=" + query.replace(" ", "+"))


def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        speak("The weather API key has not been configured.")
        return
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric"},timeout=10)
        if response.status_code == 404:
            speak("I could not find that city.")
            return
        if response.status_code == 401:
            speak("The weather API key is invalid.")
            return
        response.raise_for_status()
        data = response.json()
        speak(f"The weather in {city} is {data['weather'][0]['description']}. "
            f"The temperature is {data['main']['temp']:.1f} degrees Celsius "
            f"with {data['main']['humidity']} percent humidity.")
    except requests.RequestException:
        speak("I could not connect to the weather service.")


def create_reminder(minutes, message):
    def reminder():
        time.sleep(minutes * 60)
        speak(f"Reminder: {message}")
    threading.Thread(target=reminder, daemon=True).start()
    speak(f"I will remind you in {minutes} minutes.")

def send_email():
    sender = os.getenv("VOICE_EMAIL")
    password = os.getenv("VOICE_EMAIL_PASSWORD")
    receiver = os.getenv("VOICE_EMAIL_RECEIVER")
    if not sender or not password or not receiver:
        speak("Email settings have not been configured.")
        return
    speak("What should I write in the email?")
    message = listen()
    if not message:
        return
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, receiver,f"Subject: Voice Assistant Message\n\n{message}")
        speak("The email was sent successfully.")
    except smtplib.SMTPException:
        speak("I could not send the email. Please check the settings.")

def process_command(command):
    if not command:
        return True
    if command in {"hello", "hi", "hey"}:
        speak("Hello! How can I help you?")
    elif "help" in command:
        speak("You can ask for the time, date, weather, a web search, a reminder, or an email.")
    elif "time" in command or "date" in command:
        tell_date_time()
    elif command.startswith("search "):
        search_web(command.replace("search ", "", 1))
    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")
    elif "weather in " in command:
        get_weather(command.split("weather in ", 1)[1].strip())
    elif "send email" in command:
        send_email()
    elif "remind me" in command:
        speak("How many minutes should I wait?")
        try:
            minutes = int(listen())
        except ValueError:
            speak("I could not understand the number.")
            return True
        speak("What should I remind you about?")
        message = listen()
        if message:
            create_reminder(minutes, message)
    elif command in {"exit", "quit", "stop", "goodbye"}:
        speak("Goodbye! Have a nice day.")
        return False
    else:
        speak("I do not know that command. Say help to hear the commands I support.")
    return True


def main():
    speak("Hello! I am your Python voice assistant. Say help to hear what I can do.")
    while process_command(listen()):
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAssistant stopped.")
