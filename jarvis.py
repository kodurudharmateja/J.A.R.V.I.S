import pyttsx3
import pywhatkit
import wikipedia
import pyautogui
import time
import speech_recognition as sr

import webbrowser
import datetime
from openai import OpenAI
import os
import sys
import smtplib
# from huggingface_hub import InferenceClient
from gtts import gTTS
from playsound import playsound
import requests
import os
from helpers import *
from youtube import youtube
# import google.generativeai as genai
from sys import platform

# ------------------ ENGINE SETUP ------------------
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # 0 = male, 1 = female
engine.setProperty('rate', 150)           # speaking speed




# genai.configure(api_key="AIzaSyCl_amqoAWgHB51P9SC6GVqAYRp_NNlcNQ")

# model = genai.GenerativeModel("gemini-pro")


# def ask_brain(question):
#     try:
#         response = model.generate_content(question)
#         return response.text
#     except Exception as e:
#         print("Gemini Error:", e)
#         return "Sorry sir, my brain is not working right now."
    
# client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2")

# def ask_brain(query):
#     response = client.text_generation(query, max_new_tokens=100)
#     return response



def ask_brain(query):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:8b",
            "prompt": query,
            "stream": False
        }
    )
    return response.json()["response"]




# def speak(text):
#     print("JARVIS:", text)
#     tts = gTTS(text=text, lang='en')
#     filename = "voice.mp3"
#     tts.save(filename)
#     playsound(filename)
#     os.remove(filename)

def speak(text):
    print("JARVIS:", text)
    engine.say(text)
    engine.runAndWait()



# ------------------ WISH ------------------
def wishMe():
    hour = int(datetime.datetime.now().hour)

    if hour < 12:
        speak("Good morning sir  I am Jarvis, your personal assistant What is the plan?")
    elif hour < 18:
        speak("Good afternoon sir  I am Jarvis, your personal assistant What is the plan?")
    else:
        speak("Good evening sir I am Jarvis, your personal assistant What is the plan?")
# ------------------ JARVIS CLASS ------------------
class Jarvis:
    def __init__(self):
        if platform == "win32":
            self.chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        elif platform == "darwin":
            self.chrome_path = r"open -a /Applications/Google Chrome.app"
        else:
            self.chrome_path = "/usr/bin/google-chrome"

        webbrowser.register(
            'chrome', None, webbrowser.BackgroundBrowser(self.chrome_path)
        )




    

    def execute_query(self, query):
        query = query.lower()

        # Wikipedia search
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
            speak("Do you want me to search something else?")
            return True

        # Open YouTube
        elif 'open youtube' in query:
            speak("Opening YouTube, sir.")
            webbrowser.open_new_tab("https://youtube.com")
            speak("YouTube is ready for you.")
            speak("Anything else, sir?")
            return True

        # Open Google
        elif 'open google' in query:
            speak("Opening Google, sir.")
            webbrowser.get('chrome').open_new_tab("https://google.com")
            speak("Google is ready. What do you want to search?")
            return True

        # Google search
        elif 'search' in query:
            speak("What should I search for you, sir?")
            search = takeCommand()
            
            if search != "none":
                url = "https://google.com/search?q=" + search
                webbrowser.get('chrome').open_new_tab(url)
                speak(f"Here is what I found for {search}.")
            else:
                speak("I didn't catch that. Can you repeat?")
            return True
                

        # Play music
        elif 'play music' in query:
            music_dir = "D:\\Music"  # change this path
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Playing your music now.")
            else:
                speak("No music found in the folder.")
            return True

        # Tell the time
        elif 'time' in query:
            time_str = datetime.datetime.now().strftime("%H:%M")
            speak(f"The current time is {time_str}.")
            speak("Do you want me to remind you of anything?")
            return True
            
        elif 'send whatsapp message' in query:
            speak("Opening WhatsApp")
            os.system("start whatsapp:")
            time.sleep(5)

            speak("Whom should I send?")
            name = takeCommand()

            speak("What is the message?")
            msg = takeCommand()

            # Type name in search bar
            pyautogui.write(name)
            time.sleep(2)
            pyautogui.press("enter")

            time.sleep(2)

            pyautogui.write(msg)
            pyautogui.press("enter")

            speak("Message sent")
            return True


        elif 'open whatsapp' in query:
            speak("Opening WhatsApp")
            os.system("start whatsapp:")
            return True

        # Tell joke
        elif 'joke' in query:
            joke()
            speak("Hope that made you smile, sir.")
            return True

        # Show CPU info
        elif 'cpu' in query:
            cpu()
            speak("This is your system CPU info, sir.")
            speak("Anything else, sir?")
            return True

        # Shutdown
        elif 'shutdown' in query:
            speak("Shutting down the system now. Goodbye, sir!")
            os.system("shutdown /s /t 1")
            return True

        # Force exit
        elif 'exit' in query or 'stop' in query:
            speak("Shutting down JARVIS. See you later, sir!")
            os._exit(0)
            return True
        
        elif "go to sleep" in query:
            speak("Going to sleep, sir.")
            return True

        # Conversational responses
        elif "hello" in query or "hi" in query:
            speak("Hello, sir! How can I assist you today?")
            return True

        elif "how are you" in query:
            speak("I am functioning perfectly, sir. What about you?")
            return True

        elif "thank you" in query:
            speak("You're welcome, sir.")
            return True
            
            # Keep the conversation going
        return False 
            
 

# ------------------ MAIN ------------------
def wakeUpJARVIS():
    bot = Jarvis()
    wishMe()

    while True:
        query = takeCommand()

        if query == "none":
            continue

        print("Command:", query)

        speak("Yes sir")

        handled = bot.execute_query(query)

        if not handled:
            speak("Let me think...")
            answer = ask_brain(query)
            print("JARVIS:", answer)
            speak(answer)

        speak("Anything else, sir?")


# ------------------ START ------------------
if __name__ == "__main__":
    print("JARVIS STARTED")

    try:
        wakeUpJARVIS()
    except KeyboardInterrupt:
        print("\nStopped")
        os._exit(0)