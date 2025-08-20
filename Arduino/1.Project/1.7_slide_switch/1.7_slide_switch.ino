/*
  Digital Toggle Monitor

  Monitors a slide switch and counts the number of toggles
  while providing real-time status updates.
*/

// Pin definition for the slide switch
const int TOGGLE_PIN = 14;          // slide switch connected to pin 14

// Variables to track switch state and statistics
bool currentPosition = false;       // current switch position (true = HIGH)
bool previousPosition = false;      // previous position for change detection
int toggleCount = 0;                // total number of switch toggles
unsigned long lastToggleTime = 0;   // timestamp of last toggle event

void setup() {
  // Set up the slide switch pin as input
  pinMode(TOGGLE_PIN, INPUT);
  

  // Start serial communication
  Serial.begin(115200);
  
  // Show welcome message
  displayWelcomeMessage();
  
  // Read initial switch position
  previousPosition = digitalRead(TOGGLE_PIN);
  
  // Show initial status
  reportStatus();
}

void loop() {
  // Monitor the switch for changes
  monitorToggleSwitch();
  
  // Small delay for stability
  delay(100);
}

// Function to display welcome message and instructions
void displayWelcomeMessage() {
  Serial.println("=== Digital Toggle Monitor ===");
  Serial.println("Move the switch to see position changes");
  Serial.println("Toggle counter will track all movements");
  Serial.println("--------------------------------");
}

// Function to check for switch position changes
void monitorToggleSwitch() {
  // Read current switch position
  currentPosition = digitalRead(TOGGLE_PIN);
  
  // Check if position has changed
  if (currentPosition != previousPosition) {
    // Increment toggle counter
    toggleCount++;
    
    // Record the time of this toggle
    lastToggleTime = millis();
    
    // Display updated status
    reportStatus();
    
    // Update previous position for next comparison
    previousPosition = currentPosition;
  }
}

// Function to display current switch status and statistics
void reportStatus() {
  // Show digital value (HIGH/LOW)
  Serial.print("Position: ");
  Serial.print(currentPosition ? "HIGH" : "LOW");
  
  // Show logical state (ON/OFF)
  Serial.print(" | State: ");
  Serial.print(currentPosition ? "ON " : "OFF");
  
  // Show total toggle count
  Serial.print(" | Toggles: ");
  Serial.println(toggleCount);
  
  // Show timestamp of last change (if any toggles occurred)
  if (toggleCount > 0) {
    Serial.print("Last change: ");
    Serial.print(lastToggleTime);
    Serial.println(" ms");
  }
  
  // Add separator line for readability
  Serial.println("---");
}