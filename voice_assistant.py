import pyttsx3
import speech_recognition as sr
import requests

# Initialize voice engine
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)   # TEXT OUTPUT
    engine.say(text)            # VOICE OUTPUT
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
        return ""   # ❌ removed extra error print to avoid confusion

# 🌦️ Weather function
def get_weather(city):
    try:
        api_key = "263964c17ef66abc6e66274eb54dcfcb"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]

            # TEXT OUTPUT
            result = f"Temperature in {city}: {temp}°C | Condition: {desc}"
            print("\n🌤️ Weather Result:")
            print(result)

            # ✅ SINGLE SPEAK (FIXED)
            speak(f"The temperature in {city} is {temp} degree Celsius and the weather condition is {desc}")

        else:
            print("❌ City not found")
            speak("City not found")

    except Exception as e:
        print("Error:", e)
        speak("Error fetching weather")

# 🎯 MAIN PROGRAM
while True:
    input("\n👉 Press ENTER and speak...")

    command = take_command()

    # ✅ FIX: no wrong voice message
    if command == "":
        print("⚠️ No clear voice detected")
        continue

    print(f"👉 Processing command: {command}")

    if "weather" in command:
        # Extract city
        city = command.replace("weather", "").replace("in", "").strip()

        if city == "":
            speak("Please say the city name")
            city = take_command()

        if city != "":
            print(f"📍 Fetching weather for: {city}")
            get_weather(city)
        else:
            print("❌ City not recognized")
            speak("City not recognized")

    elif "exit" in command:
        print("👋 Exiting program")
        speak("Goodbye")
        break

    else:
        print("❌ Invalid command")
        speak("Please say weather command")