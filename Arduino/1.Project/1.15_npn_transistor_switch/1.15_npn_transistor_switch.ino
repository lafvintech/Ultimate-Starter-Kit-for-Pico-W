/*
  Transistor Switch Control

  Uses a button to control a transistor switch that can
  drive higher current devices like motors or lights.
*/

// Pin definitions
const int BUTTON_PIN = 14;          // button input pin
const int TRANSISTOR_PIN = 15;      // transistor control pin
const int CHECK_DELAY = 50;         // button check interval

// Variables for button state tracking
bool buttonPressed = false;
bool lastButtonState = false;
bool deviceOn = false;
int pressCount = 0;

void setup() {
  // Set up pins
  pinMode(BUTTON_PIN, INPUT);
  pinMode(TRANSISTOR_PIN, OUTPUT);
  
  // Initialize serial communication
  Serial.begin(115200);
  Serial.println("=== Transistor Switch Control ===");
  Serial.println("Press button to toggle device ON/OFF");
  Serial.println("Transistor acts as electronic switch");
  Serial.println();
  
  // Ensure device starts OFF
  digitalWrite(TRANSISTOR_PIN, LOW);
  Serial.println("Device: OFF (Ready)");
}

void loop() {
  // Check button and control transistor
  handleButtonControl();
  
  // Small delay for stable operation
  delay(CHECK_DELAY);
}

// Function to handle button press and transistor control
void handleButtonControl() {
  // Read current button state
  buttonPressed = digitalRead(BUTTON_PIN);
  
  // Detect button press (transition from LOW to HIGH)
  if (buttonPressed && !lastButtonState) {
    // Toggle device state
    deviceOn = !deviceOn;
    pressCount++;
    
    // Control transistor switch
    digitalWrite(TRANSISTOR_PIN, deviceOn ? HIGH : LOW);
    
    // Display status
    Serial.print("Button pressed (#");
    Serial.print(pressCount);
    Serial.print(") - Device: ");
    Serial.println(deviceOn ? "ON" : "OFF");
    
    if (deviceOn) {
      Serial.println("Transistor conducting - High current device active");
    } else {
      Serial.println("Transistor off - High current device inactive");
    }
    Serial.println();
  }
  
  // Update last button state for next comparison
  lastButtonState = buttonPressed;
}