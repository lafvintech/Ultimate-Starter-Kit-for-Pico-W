/*
  Automatic Relay Controller

  Controls a relay to automatically switch external circuits
  on and off with timing control and status monitoring.
*/

// Pin and timing constants
const int RELAY_PIN = 15;           // relay control pin
const int ON_TIME = 3000;           // relay on duration (milliseconds)
const int OFF_TIME = 2000;          // relay off duration (milliseconds)

// Variables for timing and status
unsigned long lastSwitchTime = 0;
bool relayState = false;
int cycleCount = 0;

void setup() {
  // Set up relay pin
  pinMode(RELAY_PIN, OUTPUT);
  
  // Initialize serial communication
  Serial.begin(115200);
  Serial.println("=== Automatic Relay Controller ===");
  Serial.println("Relay switches external circuit ON/OFF automatically");
  Serial.println("Can control lights, motors, or other AC/DC devices");
  Serial.println();
  
  // Start with relay OFF
  digitalWrite(RELAY_PIN, LOW);
  lastSwitchTime = millis();
  Serial.println("Starting cycle... Relay: OFF");
}

void loop() {
  // Check if it's time to switch relay state
  checkRelayTiming();
  
  // Show continuous status every 5 seconds
  showPeriodicStatus();
}

// Function to handle relay timing and switching
void checkRelayTiming() {
  unsigned long currentTime = millis();
  unsigned long elapsedTime = currentTime - lastSwitchTime;
  
  // Check if it's time to switch state
  bool shouldSwitch = false;
  
  if (relayState && elapsedTime >= ON_TIME) {
    // Relay is ON and ON_TIME has passed - turn OFF
    shouldSwitch = true;
  } else if (!relayState && elapsedTime >= OFF_TIME) {
    // Relay is OFF and OFF_TIME has passed - turn ON
    shouldSwitch = true;
  }
  
  // Switch relay if needed
  if (shouldSwitch) {
    relayState = !relayState;
    digitalWrite(RELAY_PIN, relayState ? HIGH : LOW);
    lastSwitchTime = currentTime;
    
    if (relayState) {
      cycleCount++;
    }
    
    // Display switch event
    Serial.print("Cycle #");
    Serial.print(cycleCount);
    Serial.print(" - Relay switched: ");
    Serial.println(relayState ? "ON" : "OFF");
    
    if (relayState) {
      Serial.println("External circuit powered - Device running");
    } else {
      Serial.println("External circuit off - Device stopped");
    }
    Serial.println();
  }
}

// Function to show periodic status updates
void showPeriodicStatus() {
  static unsigned long lastStatusTime = 0;
  unsigned long currentTime = millis();
  
  // Show status every 5 seconds
  if (currentTime - lastStatusTime >= 5000) {
    unsigned long timeInState = currentTime - lastSwitchTime;
    unsigned long remainingTime;
    
    if (relayState) {
      remainingTime = ON_TIME - timeInState;
      Serial.print("Status: Relay ON for ");
      Serial.print(timeInState / 1000);
      Serial.print("s, turning OFF in ");
      Serial.print(remainingTime / 1000);
      Serial.println("s");
    } else {
      remainingTime = OFF_TIME - timeInState;
      Serial.print("Status: Relay OFF for ");
      Serial.print(timeInState / 1000);
      Serial.print("s, turning ON in ");
      Serial.print(remainingTime / 1000);
      Serial.println("s");
    }
    
    lastStatusTime = currentTime;
  }
}