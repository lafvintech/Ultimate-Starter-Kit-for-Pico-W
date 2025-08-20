/*
  Tilt Switch Monitor

  Reads a tilt switch and reports when the orientation changes.
  Shows different messages for tilt and level positions.
*/

// Pin definition - connect tilt switch to this pin
const int tiltPin = 14;     // tilt switch connected to pin 14

// Variables to track switch state
int currentState = 0;       // current reading from tilt switch
int lastState = 0;          // previous reading to detect changes
bool showWelcome = true;    // flag to show welcome message once

void setup() {
  // Set up the tilt switch pin as input
  pinMode(tiltPin, INPUT);
  
  // Start serial communication
  Serial.begin(115200);
  
  // Read initial state
  lastState = digitalRead(tiltPin);
}

void loop() {
  // Show welcome message once at start
  if (showWelcome) {
    Serial.println("=== Tilt Switch Monitor ===");
    Serial.println("Current position: " + String(lastState == LOW ? "TILTED" : "LEVEL"));
    Serial.println("Move the sensor to see changes...");
    showWelcome = false;
  }
  
  // Read current tilt switch state
  currentState = digitalRead(tiltPin);
  
  // Check if state changed (only act on changes, not continuous reading)
  if (currentState != lastState) {
    // Print timestamp for the change
    Serial.print("[");
    Serial.print(millis());
    Serial.print("ms] ");
    
    // Check new position and print appropriate message
    if (currentState == LOW) {
      Serial.println(">>> SENSOR TILTED <<<");
      Serial.println("Position changed to: TILTED");
    } else {
      Serial.println("--- Sensor Level ---");
      Serial.println("Position changed to: LEVEL");
    }
    
    Serial.println(); // blank line for readability
    
    // Remember this state for next comparison
    lastState = currentState;
  }
  
  // Small delay for stability
  delay(100);
}