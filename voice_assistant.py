import pyttsx3
import speech_recognition as sr
import requests
import datetime
import webbrowser
import time
import smtplib
import os

# Initialize engine
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("\n🎤 Speak now...")
        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except:
            return ""

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    except:
        return ""

# 🌦️ WEATHER FUNCTION
def get_weather(city):
    try:
        api_key = os.getenv("WEATHER_API_KEY")

        if not api_key:
            speak("API key not found")
            return

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]

            result = f"Temperature in {city}: {temp}°C | Condition: {desc}"
            print("\n🌤️ Weather Result:")
            print(result)

            speak(f"The temperature in {city} is {temp} degree Celsius and the weather condition is {desc}")
        else:
            speak("Unable to fetch weather")

    except Exception as e:
        print(e)
        speak("Error fetching weather")

# 📧 EMAIL FUNCTION
def send_email():
    try:
        sender = os.getenv("EMAIL_ID")
        password = os.getenv("EMAIL_PASS")

        if not sender or not password:
            speak("Email credentials not set")
            return

        receiver = input("Enter receiver email: ")
        message = input("Enter message: ")

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
        server.quit()

        speak("Email sent successfully")

    except Exception as e:
        print(e)
        speak("Failed to send email")

# 🌐 CUSTOM COMMANDS
custom_commands = {
    "open youtube": "https://youtube.com",
    "open google": "https://google.com",
    "open gmail": "https://mail.google.com"
}

# 🎯 MAIN LOOP
while True:
    input("\n👉 Press ENTER and speak...")

    command = take_command()

    if command == "":
        print("⚠️ No clear voice detected")
        continue

    print(f"👉 Processing: {command}")

    # 👋 Interaction
    if "hello" in command:
        speak("Hello! How can I help you?")

    elif "your name" in command:
        speak("I am your advanced voice assistant")

    elif "thank you" in command:
        speak("You're welcome")

    # ⏰ Time
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    # 🌦️ WEATHER (NLP)
    elif any(word in command for word in ["weather", "temperature", "climate"]):
        words = command.split()
        city = words[-1]

        print(f"📍 Fetching weather for: {city}")
        get_weather(city)

    # 📧 EMAIL
    elif "send email" in command:
        send_email()

    # ⏰ REMINDER
    elif "set reminder" in command:
        speak("In how many seconds?")
        sec = take_command()

        try:
            seconds = int(sec)
            speak("Reminder set")
            time.sleep(seconds)
            speak("Time is up")
        except:
            speak("Invalid time")

    # 🌐 CUSTOM COMMANDS
    else:
        found = False
        for key in custom_commands:
            if key in command:
                webbrowser.open(custom_commands[key])
                speak(f"Opening {key}")
                found = True
                break

        if not found:
            speak("I didn't understand that")

    # ❌ EXIT
    if "exit" in command:
        speak("Goodbye")
        break