#include <WiFi.h>

const char* ssid = ""; // Router SSID
const char* password = ""; // Router Password

const char * host = ""; // Server ip
const uint16_t port = ; // Port

const int potPin = 34;
int potValue = 0;

WiFiClient client;

void setup() {
  WiFi.begin(ssid, password); // Try to connect to the internet.

  Serial.begin(115200);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  } // Keep trying to connect to the internet.

  client.connect(host, port); // Connect to server.
  delay(100);
  client.print("b"); // Send identification id.

  delay(1000);
}

void loop() {
  if (client.connected()) { // If connected to the server.
    potValue = analogRead(potPin);
    delay(100);
    Serial.println(potValue);
    client.print(potValue);
  } else { // If not connected to the server.
    client.connect(host, port); // Connect to the server on the given host and port.
    delay(100);
    client.print("b"); // Send the proper id.
  }
  delay(1000);
}
