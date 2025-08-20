/*
  Press Duration Counter

  Measures how long a button is pressed and provides
  different responses based on press duration.
  Shows statistics about button usage.
*/

// Pin definition for the button
const int BUTTON_PIN = 14;          // button connected to pin 14

// Variables to track button state
bool isPressed = false;             // current button state (true = pressed)
bool wasPressed = false;            // previous button state for comparison
unsigned long pressStartTime = 0;   // when the button was first pressed
unsigned long pressDuration = 0;    // how long the button was held
int totalPresses = 0;               // count of total button presses

void setup() {
  // Set up the button pin as input
  pinMode(BUTTON_PIN, INPUT);
  
  // Start serial communication
  Serial.begin(115200);
  
  // Show instructions to user
  showInstructions();
}

void loop() {
  // Check button state and handle press events
  handleButtonPress();
  
  // Small delay for stability
  delay(10);
}

// Function to display instructions at startup
void showInstructions() {
  Serial.println("*** Press Duration Counter ***");
  Serial.println("Press and hold the button for different durations:");
  Serial.println("- Quick press (< 500ms): Short beep");
  Serial.println("- Medium press (500-2000ms): Medium beep");
  Serial.println("- Long press (> 2000ms): Long beep");
  Serial.println("===============================");
}

// Function to monitor button state and detect press/release events
void handleButtonPress() {
  // Read current button state
  isPressed = digitalRead(BUTTON_PIN);
  
  // Check if button was just pressed (transition from not pressed to pressed)
  if (isPressed && !wasPressed) {
    // Record the time when button was pressed
    pressStartTime = millis();
    Serial.print("Button pressed... ");
  }
  
  // Check if button was just released (transition from pressed to not pressed)
  if (!isPressed && wasPressed) {
    // Calculate how long the button was held
    pressDuration = millis() - pressStartTime;
    totalPresses++;  // increment total press counter
    
    // Show the duration
    Serial.print("Released! Duration: ");
    Serial.print(pressDuration);
    Serial.println("ms");
    
    // Analyze the press type based on duration
    categorizePressType();
    
    // Show current statistics
    showStatistics();
  }
  
  // Remember current state for next loop comparison
  wasPressed = isPressed;
}

// Function to categorize press type based on duration
void categorizePressType() {
  Serial.print("Press type: ");
  
  // Check duration and provide appropriate feedback
  if (pressDuration < 500) {
    Serial.println("QUICK TAP");
    Serial.println("♪ Beep!");           // short sound effect
  } else if (pressDuration < 2000) {
    Serial.println("MEDIUM PRESS");
    Serial.println("♪♪ Beep-Beep!");     // medium sound effect
  } else {
    Serial.println("LONG HOLD");
    Serial.println("♪♪♪ Beep-Beep-Beep!"); // long sound effect
  }
}

// Function to display usage statistics
void showStatistics() {
  Serial.print("Total presses: ");
  Serial.println(totalPresses);
  Serial.println("---");  // separator line for readability
}