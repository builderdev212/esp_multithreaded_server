#include <WiFi.h>

/*
This is the code for espa, with 2 LED's connected on pin 22 and 21.
*/

const char* ssid = ""; // Router SSID
const char* password = ""; // Router Password

const char * host = ""; // Server ip
const uint16_t port = ; // Port

WiFiClient client;

void setup() {
  pinMode(22, OUTPUT); // Red LED
  pinMode(21, OUTPUT); // Blue LED

  WiFi.begin(ssid, password); // Try to connect to the internet.

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  } // Keep trying to connect to the internet.

  client.connect(host, port); // Connect to server.
  delay(100);
  client.print("a"); // Send identification id.
}

void loop() {
  if (client.connected()) { // If connected to the server.
    if (client.available()) { // If data is sent.
      char info = client.read(); // Read the data sent.
      delay(100);
      char one = '1';
      char two = '2';
      char three = '3';
      char four = '4';

      if (info == one) { // If command is 1.
        digitalWrite(22, HIGH); // Turn the red LED on.
        client.print("ack"); // Send ack back to the server.
      } else if (info == two) { // If the command is 2.
        digitalWrite(22, LOW); // Turn the red LED off.
        client.print("ack"); // Send ack back to the server.
      } else if (info == three) { // If the command is 3.
        digitalWrite(21, HIGH); // Turn the blue LED on.
        client.print("ack"); // Send ack back to the server.
      } else if (info == four) { // If the command is 4.
        digitalWrite(21, LOW); // Turn off the blue LED.
        client.print("ack"); // Send ack back to the server.
      } else { // If the command is something else.
        client.print("fail"); // Send fail back to the server.
      }
      delay(100);
    }
  } else { // If not connected to the server.
    client.connect(host, port); // Connect to the server on the given host and port.
    delay(100);
    client.print("a"); // Send the proper id.
  }
  delay(100);
}
