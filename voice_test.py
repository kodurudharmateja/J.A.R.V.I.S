import sounddevice as sd
import numpy as np
import speech_recognition as sr

r = sr.Recognizer()

duration = 5  # seconds
sample_rate = 44100

print("Speak now...")

# Record audio
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
sd.wait()

# Convert to bytes
audio_bytes = audio.tobytes()

# Create AudioData object
audio_data = sr.AudioData(audio_bytes, sample_rate=sample_rate, sample_width=2)

# Recognize
try:
    text = r.recognize_google(audio_data)
    print("You said:", text)
except sr.UnknownValueError:
    print("Could not understand audio")
except sr.RequestError as e:
    print("API error:", e)