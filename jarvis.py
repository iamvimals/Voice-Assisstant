import os
import pyttsx3
import requests
from decouple import config
from datetime import datetime
import sys
import speech_recognition as sr
import subprocess as sp
from playsound import playsound

CREATOR = config('CREATOR')
BOTNAME = config('BOTNAME')

application_paths = {
    'calculator': 'C:\\Windows\\System32\\calc.exe',
    'chrome': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
}

# greetings
greetings_commands = ['hello', 'hi', 'whats\'s up', 'hey', 'heya']
greetings_reponse = 'Sure, ask me anything. I can do quite a few things.'

# exit
exit_commands = ['goodbye', 'bye', 'see ya', 'terminate', 'see you later alligator', 'quit']
exit_response = f'Have a good day {CREATOR}'

engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 195)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
if BOTNAME == 'NATASHA':
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)


# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""
    engine.say(text)
    engine.runAndWait()


def greet_user_startup():
    """Greets the user according to the time"""
    hour = datetime.now().hour
    if (hour >= 0) and (hour < 12):
        speak(f"Good Morning {CREATOR}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {CREATOR}")
    elif (hour >= 16) and (hour <= 23):
        speak(f"Good Evening {CREATOR}")
    speak(f"I am {BOTNAME}. How may I assist you today?")


def get_current_time():
    time = datetime.today().strftime("%H:%M %p")
    speak(f'It\'s currently {time}')


def fetch_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        # if not 'exit' in query or 'stop' in query:
        #     # speak(choice(opening_text))
        # else:
        #     hour = datetime.now().hour
        #     if hour >= 21 and hour < 6:
        #         speak("Good night sir, take care!")
        #     else:
        #         speak('Have a good day sir!')
        #     exit()
    except Exception:
        # speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query


def missing_feature():
    text = 'Sorry, I could not understand that. Could you please say that again?'
    speak(text)


def get_random_advice():
    speak('Okay, so now you want my advice is it, sure here it is')
    res = requests.get("https://api.adviceslip.com/advice").json()
    for i in range(2):
        speak(res['slip']['advice'])
        if i == 1:
            break
        speak('I repeat')


def open_calculator():
    speak('Opening calculator')
    sp.Popen(application_paths['calculator'])

def open_chrome():
    speak('Opening Chrome')
    sp.Popen(application_paths['chrome'])

def open_cmd():
    speak('Opening Command Prompt')
    os.system('start cmd')

if __name__ == '__main__':
    playsound('sound.mp3')
    greet_user_startup()
    while True:
        query = fetch_user_input().lower()
        print(f'Query: {query}')
        if BOTNAME.lower() in query or 'are you here' in query:
            speak(f'Yes {CREATOR}, I\'m here')
        if 'greet me now' in query:
            greet_user_startup()
        elif 'what do you do' in query:
            speak('I can do a lot of things, why dont you give a try')
        elif query in greetings_commands:
            speak(greetings_reponse)
        elif 'what\'s the time' in query:
            get_current_time()
        elif 'give me an advice' in query:
            get_random_advice()
        elif 'open calculator' in query:
            open_calculator()
        elif 'open chrome' in query:
            open_chrome()
        elif 'how are you' in query:
            speak('I\'m doing great, thank you')
        elif 'open command prompt' in query:
            open_cmd()
        elif 'great' in query or 'thanks' in query:
            speak('Anytime')
        elif 'who are you' in query or 'who created you' in query:
            speak(f'I\'m {BOTNAME}, and I was created by Mr.{CREATOR}')
        elif 'what do i call you' in query:
            speak(f'I was called {BOTNAME} by my creator and that is what everyone calls me. So you can call me that.')
        elif query in exit_commands:
            speak(exit_response)
            playsound('sound.mp3')
            sys.exit()
        # else:
        #     missing_feature()
