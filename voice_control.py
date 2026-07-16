import speech_recognition as sr
import websockets
import time
import json
from openai import OpenAI 

WS_URL = "ws://192.168.4.1:81/"  #This is the WebSocket URL for the ESP32 device
    
