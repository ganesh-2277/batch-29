import os
import pyttsx3
import pyautogui
import vosk
import sounddevice as sd
import queue
import json
import subprocess
import webbrowser
import psutil

# ------------------ Initialize TTS ------------------
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# ------------------ Setup Vosk ------------------
q = queue.Queue()
model = vosk.Model(r"C:\Users\PRAVEEN\vosk-model-small-en-us-0.15")
rec = vosk.KaldiRecognizer(model, 16000)

def callback(indata, frames, time, status):
    """Put microphone input into queue"""
    q.put(bytes(indata))

def listen():
    """Listen continuously and return recognized text"""
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Listening...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if result.get("text"):
                    return result["text"].lower()

# ------------------ Command Handling ------------------
def handle_command(cmd):
    if "notepad" in cmd:
        speak("Opening Notepad")
        subprocess.Popen("notepad")
    elif "calculator" in cmd:
        speak("Opening Calculator")
        subprocess.Popen("calc")
    elif "screenshot" in cmd:
        speak("Taking screenshot")
        filename = "screenshot.png"
        pyautogui.screenshot(filename)
        speak(f"Screenshot saved as {filename}")
    elif "battery" in cmd:
        battery = psutil.sensors_battery()
        if battery:
            speak(f"Battery is at {battery.percent} percent")
        else:
            speak("Battery information not available")
    elif "google" in cmd:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "hello" in cmd:
        speak("Hello! How can I assist you today?")
    elif "exit" in cmd or "quit" in cmd:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't understand that command")

# ------------------ Main Loop ------------------
if __name__ == "__main__":
    while True:
        text = listen()
        if text.strip():  # Ignore empty results
            print("You said:", text)
            handle_command(text)
