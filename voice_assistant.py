import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser

# Initialize engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You said:", command)
        return command.lower()
    
    except:
        print("Sorry, try again")
        return ""

def run_assistant():
    command = take_command()

    if "hello" in command:
        speak("Hello! How can I help you?")

    elif "time" in command:
        time = datetime.datetime.now().strftime("%H:%M")
        speak("The time is " + time)

    elif "who is" in command:
        person = command.replace("who is", "")
        info = wikipedia.summary(person, 2)
        speak(info)

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")

    elif "exit" in command:
        speak("Goodbye")
        exit()

# Run assistant
while True:
    run_assistant()