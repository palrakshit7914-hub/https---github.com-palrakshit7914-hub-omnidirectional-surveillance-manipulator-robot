import speech_recognition as sr
import pyttsx3
import websockets
import time
import json
from google import genai

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
    try:
        text= recognizer.recognize_google(audio)
        print(f"Command is: '{text}'")
        engine.say(f"Command is: '{text}")
        return text
    
    except Exception:
        robot_talk("I did't catch the command. Please say it again")
        return None


def ai_agent_reasoning(user_command):
    """The AI Agent Brain. Translates conversational text into your exact
    ESP32 WebSocket string packets dynamically."""

    system_prompt = """
    You are the Agentic AI brain managing an omnidirectional mobile manipulator robot.
    Your physical host platform accepts exact command strings over a raw websocket network:
    
    1. Omni Base Movement string template: "x,y,turn"
       - Forward: "0,200,0"  | Backward: "0,-200,0"
       - Strafe Left: "-200,0,0" | Strafe Right: "200,0,0"
       - Rotate Counter-Clockwise: "0,0,-150" | Rotate Clockwise: "0,0,150"
       - Complete Halt: "0,0,0"
       
    2. Manipulator / Eye Servos template: "S,channel,angle"
       - Channels available: 0, 1, 2, 3 (Angles range from 0 to 180)
       
    3. Accessory N20 Motor template: "N,speed"
       - Forward: "N,255" | Reverse: "N,-255" | Halt: "N,0"

    Analyze the user's natural language instruction. Reason out the necessary logical movements. 
    Output a clean, valid JSON dictionary containing your structural reasoning and a simple array 
    list of sequential command strings to execute. Always conclude standard movement lists with a halt ("0,0,0") command.

    Example Input: "Slide left to avoid the wall, step forward, and rotate the first servo to ninety degrees."
    Example Output: {"reasoning": "Bypassing obstacle by strafing left, moving forward, adjusting arm servo 0, and halting.", "sequence": ["-200,0,0", "0,200,0", "S,0,90", "0,0,0"]}
    
    Output valid raw JSON only. Do not include markdown design tick marks or code blocks.
    """
    response = client.chat.completion.create(
        model = "gemini-2.5-flash",
        contents = user_command,
        config = genai.types.GenerateContentConfig(system_instruction=system_prompt,response_mime_type="application/json", response_schema=RobotActionSchema, temprature = 0.1),
    )

    return json.loads(response.text)

def execute_robot(command_sequence):
    try:
        print(f"Connecting to the WebSocket at {WS_URL}")
        ws = websocket.create_connection(WS_URL, timeout = 3)
        print("websocket pipeline establish") #means py script and robot has connected



if __name__ == "__main__":
    robot_talk("I am ready for the work. Gimme command sir")
