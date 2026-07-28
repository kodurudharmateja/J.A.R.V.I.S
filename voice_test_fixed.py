import speech_recognition as sr
import pyttsx3

# Initialize text-to-speech
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# List available microphones
print("Available microphones:")
for i, mic_name in enumerate(sr.Microphone.list_microphone_names()):
    print(i, mic_name)

# Choose your microphone index here (replace 1 with the correct number)
mic_index = int(input("Enter the microphone index you want to use: "))

r = sr.Recognizer()

with sr.Microphone(device_index=mic_index) as source:
    print("Adjusting for ambient noise, please wait...")
    r.adjust_for_ambient_noise(source, duration=2)  # this now works
    print("Listening...")
    try:
        audio = r.listen(source, timeout=5, phrase_time_limit=5)
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("You said:", query)
        speak("You said: " + query)
    except sr.UnknownValueError:
        print("Could not understand audio")
        speak("I could not understand you")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        speak("There was an error with the recognition service")