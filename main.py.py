import speech_recognition as sr
import requests
import datetime
import webbrowser
import time
import smtplib
import os
from gtts import gTTS
import playsound

# 🗣️ SPEAK FUNCTION (gTTS - STABLE)
def speak(text):
    print("Assistant:", text)

    try:
        filename = "voice.mp3"
        tts = gTTS(text=text, lang='en')
        tts.save(filename)

        playsound.playsound(filename)
        os.remove(filename)

    except Exception as e:
        print("Voice error:", e)

# 🎤 TAKE COMMAND
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
        api_key = "263964c17ef66abc6e66274eb54dcfcb"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]

            print(f"\n🌤️ Weather in {city}: {temp}°C, {desc}")
            speak(f"The temperature in {city} is {temp} degree Celsius and the weather is {desc}")
        else:
            speak("Sorry, I couldn't find the city")

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
    "open gmail": "https://mail.google.com",
    "open my college": "https://yourcollege.com"
}

# 🎯 MAIN LOOP
while True:
    input("\n👉 Press ENTER and speak...")

    command = take_command()

    if command == "":
        print("⚠️ No clear voice detected")
        continue

    print(f"👉 Processing: {command}")

    # ❌ EXIT
    if "exit" in command:
        speak("Goodbye")
        break

    # 👋 Interaction
    elif "hello" in command:
        speak("Hello! How can I help you?")

    elif "your name" in command:
        speak("I am your advanced voice assistant")

    elif "who are you" in command:
        speak("I am an AI voice assistant built using Python")

    elif "thank you" in command:
        speak("You're welcome")

    # ⏰ Time
    elif "time" in command:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "date" in command:
        today = datetime.date.today()
        speak(str(today))

    # 🌦️ WEATHER
    elif any(word in command for word in ["weather", "whether", "wether", "temperature", "climate"]):
        command = command.replace("whether", "weather").replace("wether", "weather")

        words = command.split()
        if "in" in words:
            city = words[words.index("in") + 1]
        else:
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
                speak(key.replace("open ", "Opening "))
                found = True
                break

        if not found:
            speak("I didn't understand that")

    time.sleep(1)