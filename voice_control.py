import speech_recognition as sr
import pyttsx3
import websockets
import time
import json
from openai import OpenAI 

WS_URL = "ws://192.168.4.1:81/"  #This is the WebSocket URL for the ESP32 device

openai_client = OpenAI(api_key="YOUR_OPENAI_API_KEY") #Here u have to paste the API Key of Gemini or any openai api key 

#this will speak the output text
engine = pyttsx3.init()
engine.setProperty('rate',160)
engine.setProperty('volume',1.0)

# ------------------ this is for female voice-------------
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)  # index 1 is usually the built-in female voice

def robot_talk(text):
    """Now What cmd u give it will speak"""
    print(f"{text}")
    engine.say(text)
    engine.runAndWait()

def capture_voice():
    """This will take(capture) the voice cmd from user"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("I a Listing Sir..." \
        "whats ur command sir??")
        engine.say("I a Listing Sir..." \
        "whats ur command sir??")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        audio = recognizer.listen(source)



if __name__ == "__main__":
    # Say hello at startup
    robot_talk("Your Robot is online. Awaiting command")
