#include <ESP8266WiFi.h>
#include <ESPAsyncWebServer.h>

// Wi-Fi credentials
const char* ssid = "PCU_Guest";
const char* password = "P@$$w0rd@1234";

// Create an AsyncWebServer object on port 80
AsyncWebServer server(80);

// Voting counters
int voteCount = 0;

// Debounce logic
unsigned long lastTouchTime = 0;
const unsigned long debounceDelay = 500;

// Web Page HTML (Embedded in Code)
const char* index_html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <title>Vote Counter</title>
</head>
<body>
  <h1>Vote Count: <span id="voteCount">0</span></h1>
  <button onclick="vote()">Vote</button>

  <script>
    function vote() {
      fetch('/vote')
        .then(response => response.text())
        .then(data => {
          document.getElementById('voteCount').textContent = data;
        });
    }
  </script>
</body>
</html>
)rawliteral";

void setup() {
  // Initialize serial communication
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.println("IP Address: " + WiFi.localIP().toString());

  // Serve the HTML page on the root "/"
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send_P(200, "text/html", index_html);
  });

  // Handle the "/vote" route
  server.on("/vote", HTTP_GET, [](AsyncWebServerRequest *request) {
    // Simple debounce logic
    if (millis() - lastTouchTime > debounceDelay) {
      voteCount++;
      lastTouchTime = millis();
      Serial.println("Vote counted! Total votes: " + String(voteCount));
    }
    request->send(200, "text/plain", String(voteCount));
  });

  // Start the server
  server.begin();
}

void loop() {
  // Nothing needed in loop; server handles everything
}
