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

