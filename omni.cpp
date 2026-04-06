// LIBRARIES REQUIRED FOR THIS PROJECT 
#include <WiFi.h>
#include <WebServer.h>
#include <WebSocketsServer.h>

// DEFINE THE WIFI CREDENTIALS
const char* ssid = "OMNI_WIFI";
const char* password = "Omni@1234";

// CREATE A WEBSERVER OBJECT ON PORT 80
WebServer server(80);
// CREATE A WEBSOCKET SERVER OBJECT ON PORT 81
WebSocketsServer webSocket = WebSocketsServer(81);

// Pin definitions
const int M1_RPWM = 25; // Motor 1 PWM pin
const int M1_LPWM = 26; // Motor 1 direction pin
const int M1_REN = 33;  // Motor 1 enable pin
const int M1_LEN = 32; // Motor 1 direction pin

const int M2_RPWM = 27; // Motor 2 PWM pin
const int M2_LPWM = 14; // Motor 2 direction pin
const int M2_REN = 12;  // Motor 2 enable pin
const int M2_LEN = 13; // Motor 2 direction pin


const int M3_RPWM = 18; // Motor 3 PWM pin
const int M3_LPWM = 19; // Motor 3 direction pin
const int M3_REN = 5;  // Motor 3 enable pin
const int M3_LEN = 17; // Motor 3 direction pin


// Kinematics & Motor control function
void setMotor(int rpwmPin, int lpwmPin, int renPin, int lenPin, int speed) {

    int s = constrain(speed, -255, 255); // Constrain speed to -255 to 255
    if (s > 0) {
        analogWrite(rpwmPin, s);   // Set speed
        analogWrite(lpwmPin, 0);
    } 
    else if (s < 0) {
        analogWrite(rpwmPin, 0);
        analogWrite(lpwmPin, -s);  // Set speed
    }
    else {
        analogWrite(rpwmPin, 0);
        analogWrite(lpwmPin, 0);
    }
}


// Function to move the robot based on x and y inputs
void moveRobot(int x, int y) {
    // Calculate motor speeds based on desired x and y movement
    int m1Speed = y + x; // Front motor
    int m2Speed = y - x; // Left motor
    int m3Speed = y - x; // Right motor

    // Set motor speeds
    setMotor(M1_RPWM, M1_LPWM, M1_REN, M1_LEN, m1Speed);
    setMotor(M2_RPWM, M2_LPWM, M2_REN, M2_LEN, m2Speed);
    setMotor(M3_RPWM, M3_LPWM, M3_REN, M3_LEN, m3Speed);
}

// WEBSOCKET EVENT HANDLER
void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {     
    if (type == WStype_TEXT) {
        
        int x,y,t;
        if (sscanf((char*)payload, "%d,%d,%d", &x, &y, &t) == 3) {
            moveRobot(x, y,t); // Move the robot based on received x , y and t values
        }
    }
}

// web Interface handler
void handleRoot() {
  String html = "<html><head><meta name='viewport' content='width=device-width, initial-scale=1.0, user-scalable=no'>";
  html += "<style>body{background:#222; color:white; text-align:center; font-family:sans-serif; touch-action:none;}";
  html += ".btn{width:70px; height:70px; margin:5px; font-size:20px; border-radius:10px; border:none; background:#444; color:white;}";
  html += ".btn:active{background:#00ff00; color:black;} .rot{background:#55acee;} .stop{background:#ff4b2b; width:100%}</style></head><body>";
  
  html += "<h1>Omni WS Control</h1>";
  html += "<table>";
  html += "<tr><td></td><td><button class='btn' onmousedown='send(0,200,0)' onmouseup='send(0,0,0)' ontouchstart='send(0,200,0)' ontouchend='send(0,0,0)'>&uarr;</button></td><td></td></tr>";
  html += "<tr><td><button class='btn' onmousedown='send(-200,0,0)' onmouseup='send(0,0,0)' ontouchstart='send(-200,0,0)' ontouchend='send(0,0,0)'>&larr;</button></td>";
  html += "<td><button class='btn rot' onmousedown='send(0,0,-150)' onmouseup='send(0,0,0)' ontouchstart='send(0,0,-150)' ontouchend='send(0,0,0)'>&#8634;</button></td>";
  html += "<td><button class='btn' onmousedown='send(200,0,0)' onmouseup='send(0,0,0)' ontouchstart='send(200,0,0)' ontouchend='send(0,0,0)'>&rarr;</button></td></tr>";
  html += "<tr><td><button class='btn rot' onmousedown='send(0,0,150)' onmouseup='send(0,0,0)' ontouchstart='send(0,0,150)' ontouchend='send(0,0,0)'>&#8635;</button></td>";
  html += "<td><button class='btn' onmousedown='send(0,-200,0)' onmouseup='send(0,0,0)' ontouchstart='send(0,-200,0)' ontouchend='send(0,0,0)'>&darr;</button></td><td></td></tr>";
  html += "</table><br><button class='btn stop' onclick='send(0,0,0)'>STOP</button>";

  html += "<script>var ws = new WebSocket('ws://' + window.location.hostname + ':81/');";
  html += "function send(x,y,t){ if(ws.readyState===1) ws.send(x+','+y+','+t); }</script></body></html>";
  
  server.send(200, "text/html", html);
}

void setup() {

    int pins[] = {25,26,33,32,27,14,12,13,18,19,5,17};
    for (int p : pins) {
         digitalWrite(33, 1); digitalWrite(32, 1);
  digitalWrite(12, 1); digitalWrite(13, 1);
  digitalWrite(5, 1);  digitalWrite(17, 1);}

  WiFi.softAP(ssid, password); // Start WiFi in AP mode
  server.on("/", handleRoot); // Define route for root URL
  server.begin(); // Start the web server

  webSocket.begin(); // Start the WebSocket server
  webSocket.onEvent(webSocketEvent); // Set the WebSocket event handler  
}

