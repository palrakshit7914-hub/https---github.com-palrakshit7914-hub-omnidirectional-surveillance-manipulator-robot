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
        "whats ur command")
