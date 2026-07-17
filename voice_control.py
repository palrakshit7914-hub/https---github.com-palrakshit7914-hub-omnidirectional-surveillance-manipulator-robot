import speech_recognition as sr
import pyttsx3
import websocket
import time
import json
from google import genai
from pydantic import BaseModel

class RobotActionSchema(BaseModel):
    reasoning: str
    sequence: list[str]

WS_URL = "ws://192.168.4.1:81/"  #This is the WebSocket URL for the ESP32 device

client = genai.Client()

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
    Always conclude standard movement lists with a halt ("0,0,0") command.
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_command,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            response_schema=RobotActionSchema,
            temperature=0.1
        ),
    )
    
    return json.loads(response.text)

def execute_robot(command_sequence):
    try:
        print(f"Connecting to the WebSocket at {WS_URL}")
        ws = websocket.create_connection(WS_URL, timeout = 3)
        print("websocket pipeline establish") #means py script and robot has connected

        if ',' in command and not command.startswith("S") and not command.startswith("N") and command != "0,0,0":
            time.sleep(1.5)
        else:
            time.sleep(0.5)
    
    except Exception as e:
        robot_talk("You are offline, Connect to the wifi")
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    robot_talk("I am ready for the work. Gimme command sir")

# without while loop it will run once and stop but if we use while loop it will run until we say stop or we manually stop

    while True:
        voice_input = capture_voice()
        if voice_input:
            cleaned_input= voice_input.lower().strip()
            if cleaned_input in ["Stop","terminate", "exit", "stop loop","Dont move","shut down","power off"]:
                robot_talk("Shutting down the omnidirectional surveillance and manipulator robot")

            break

        print("Processing Agentic logic map")
        try:
            agent_decision = ai_agent_reasoning(voice_input)
            print(f"Reasoning Matrix: {agent_decision['reasoning']}")
            
            robot_talk(f"Planning complete. Reason: {agent_decision['reasoning']}")
            execute_robot(agent_decision['sequence'])
            robot_talk("Task completed successfully.")

        except Exception as parse_error:
            robot_talk("Parsing error in cognitive core.")
            print(f"Error compiling JSON: {parse_error}")