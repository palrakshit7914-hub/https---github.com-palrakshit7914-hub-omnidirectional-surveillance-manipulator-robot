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