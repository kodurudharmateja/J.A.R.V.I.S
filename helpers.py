import pyttsx3
import pyautogui
import psutil
import pyjokes
import speech_recognition as sr
import json
import requests
import geocoder
from difflib import get_close_matches


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
g = geocoder.ip('me')
data = json.load(open('data.json'))

def speak(audio) -> None:
        engine.say(audio)
        engine.runAndWait()

def screenshot() -> None:
    img = pyautogui.screenshot()
    img.save('path of folder you want to save/screenshot.png')

def cpu() -> None:
    usage = str(psutil.cpu_percent())
    speak("CPU is at"+usage)

    battery = psutil.sensors_battery()
    speak("battery is at")
    speak(battery.percent)

def joke() -> None:
    for i in range(5):
        speak(pyjokes.get_jokes()[i])

import speech_recognition as sr

MIC_INDEX = 1 # <-- set this to the working mic index from the test (2 in your case)
def takeCommand():
    r = sr.Recognizer()

    r.pause_threshold = 0.8
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True

    try:
        with sr.Microphone() as source:
            print("Listening...")

            # Quickly adjust to background noise
            r.adjust_for_ambient_noise(source, duration=0.5)

            audio = r.listen(
                source,
                timeout=8,
                phrase_time_limit=6
            )

        print("Recognizing...")

        query = r.recognize_google(
            audio,
            language='en-IN'
        )

        print("You said:", query)
        return query.lower()

    except sr.WaitTimeoutError:
        print("No speech detected.")
        return "none"

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return "none"

    except sr.RequestError as e:
        print("Speech recognition service error:", e)
        return "none"

    except Exception as e:
        print("Recognition Error:", e)
        return "none"

def weather():
    api_key = "53e5477bb4ab6960c0de6d896b1b3a2e"
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={g.latlng[0]}&lon={g.latlng[1]}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    print(response.text)  # DEBUG
    
    data = response.json()

    if data["cod"] == 200:
        main = data["main"]
        wind = data["wind"]
        weather_desc = data["weather"][0]

        speak(f"Location {data['name']}")
        speak(f"Weather {weather_desc['main']}")
        speak(f"Temperature {main['temp']} degree celsius")
        speak(f"Humidity {main['humidity']} percent")
        speak(f"Wind speed {wind['speed']} meter per second")
    else:
        speak("Weather data not available")

def translate(word):
    word = word.lower()
    if word in data:
        speak(data[word])
    elif len(get_close_matches(word, data.keys())) > 0:
        x = get_close_matches(word, data.keys())[0]
        speak('Did you mean ' + x +
              ' instead,  respond with Yes or No.')
        ans = takeCommand().lower()
        if 'yes' in ans:
            speak(data[x])
        elif 'no' in ans:
            speak("Word doesn't exist. Please make sure you spelled it correctly.")
        else:
            speak("We didn't understand your entry.")

    else:
        speak("Word doesn't exist. Please double check it.")
