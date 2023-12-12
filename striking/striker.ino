#include <ESP8266WiFi.h>

const char *ssid = "airobotlab";
const char *password = "robot120";
const uint16_t port = 8087;
WiFiServer server(port);

// https://blog.csdn.net/title71/article/details/118764716
// 
void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.println("\nconnecting to WiFi...");

  while(WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }

  Serial.println();
  Serial.print("WiFi connected, local IP address:");
  Serial.println(WiFi.localIP());

  delay(500);
  server.begin();
  Serial.println("server started");

  pinMode(D7, OUTPUT);
}

void loop() {
  WiFiClient client = server.available();
  if(client){
    Serial.println("New client connected");
    while(client.connected()){
      if(client.available()){
        String message = client.readStringUntil('\r');
        digitalWrite(D7, HIGH);
        delay(atoi(message.c_str()));
        digitalWrite(D7, LOW);
        delay(1000);
        Serial.println(message);
      }
    }
    client.stop();
    Serial.println("client disconnected");
  }
}
