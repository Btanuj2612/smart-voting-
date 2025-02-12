#include <ESP8266WiFi.h>
#include <ESPAsyncWebServer.h>

// Wi-Fi credentials
const char* ssid = "TanuPriya";
const char* password = "PritaN@06";

// Web server on port 80
AsyncWebServer server(80);

// Pin definitions
int LED1 = D0, LED2 = D4, LED3 = D2, LED4 = D3;
int touch1 = D5, touch2 = D6, touch3 = D7, touch4 = D8;
int buzzer = D1;

// Vote counters for each candidate
int count1 = 0, count2 = 0, count3 = 0, count4 = 0;

void setup() {
  Serial.begin(115200);

  // Initialize Wi-Fi connection
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
  Serial.println("IP Address: " + WiFi.localIP().toString());

  // Set pin modes
  pinMode(touch1, INPUT);
  pinMode(LED1, OUTPUT);
  pinMode(touch2, INPUT);
  pinMode(LED2, OUTPUT);
  pinMode(touch3, INPUT);
  pinMode(LED3, OUTPUT);
  pinMode(touch4, INPUT);
  pinMode(LED4, OUTPUT);
  pinMode(buzzer, OUTPUT);

  // Serve the web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    String html = R"rawliteral(
      <!DOCTYPE html>
      <html>
      <head>
        <title>Vote Counter</title>
        <script>
          function fetchVotes() {
            fetch('/getVotes')
              .then(response => response.json())
              .then(data => {
                document.getElementById('candidate1').textContent = data.count1;
                document.getElementById('candidate2').textContent = data.count2;
                document.getElementById('candidate3').textContent = data.count3;
                document.getElementById('candidate4').textContent = data.count4;
              });
          }
          setInterval(fetchVotes, 1000);  // Fetch votes every 1 second
        </script>
      </head>
      <body onload="fetchVotes()">
        <h1>Vote Counts:</h1>
        <p>Candidate 1: <span id="candidate1">0</span></p>
        <p>Candidate 2: <span id="candidate2">0</span></p>
        <p>Candidate 3: <span id="candidate3">0</span></p>
        <p>Candidate 4: <span id="candidate4">0</span></p>
      </body>
      </html>
    )rawliteral";
    request->send(200, "text/html", html);
  });

  // Endpoint to send vote counts as JSON
  server.on("/getVotes", HTTP_GET, [](AsyncWebServerRequest *request) {
    String json = "{";
    json += "\"count1\":" + String(count1) + ",";
    json += "\"count2\":" + String(count2) + ",";
    json += "\"count3\":" + String(count3) + ",";
    json += "\"count4\":" + String(count4);
    json += "}";
    request->send(200, "application/json", json);
  });

  server.begin();
}

void loop() {
  // Check touch sensors and increment votes
  if (digitalRead(touch1) == HIGH) {
    handleVote(1);
    delay(1000);  // Debounce delay
  } else if (digitalRead(touch2) == HIGH) {
    handleVote(2);
    delay(1000);
  } else if (digitalRead(touch3) == HIGH) {
    handleVote(3);
    delay(1000);
  } else if (digitalRead(touch4) == HIGH) {
    handleVote(4);
    delay(1000);
  }
}

// Handle vote and provide feedback
void handleVote(int candidate) {
  switch (candidate) {
    case 1:
      count1++;
      digitalWrite(LED1, HIGH);
      break;
    case 2:
      count2++;
      digitalWrite(LED2, HIGH);
      break;
    case 3:
      count3++;
      digitalWrite(LED3, HIGH);
      break;
    case 4:
      count4++;
      digitalWrite(LED4, HIGH);
      break;
  }

  // Buzzer feedback
  digitalWrite(buzzer, HIGH);
  delay(500);
  digitalWrite(buzzer, LOW);

  resetLEDs();
  Serial.println("Vote Registered: Candidate " + String(candidate));
}

// Reset LEDs after feedback
void resetLEDs() {
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
  digitalWrite(LED4, LOW);
}
