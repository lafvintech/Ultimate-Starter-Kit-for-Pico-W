const int motor1A = 14;
const int motor2A = 15;
const int switchPin = 16;

bool pumpState = false;
int lastSwitchState = HIGH; // HIGH indicates not pressed

void setup() {
  pinMode(motor1A, OUTPUT);
  pinMode(motor2A, OUTPUT);
  pinMode(switchPin, INPUT_PULLUP);

  pumpOff(); // Initial state: Off
}

void loop() {
  int currentSwitchState = digitalRead(switchPin);

  // Detect the moment when the button changes from not pressed to pressed (falling edge)
  if (currentSwitchState == LOW && lastSwitchState == HIGH) {
    delay(20); // Debounce
    if (digitalRead(switchPin) == LOW) { // Confirm the button state again
      pumpState = !pumpState; // Toggle the state
      if (pumpState) {
        pumpOn();
        Serial.println("Power on");
      } else {
        pumpOff();
        Serial.println("Power off");
      }
    }
  }

  lastSwitchState = currentSwitchState;
  delay(50); // Add a delay to avoid excessive CPU usage
}

void pumpOn() {
  digitalWrite(motor1A, HIGH);
  digitalWrite(motor2A, LOW);
}

void pumpOff() {
  digitalWrite(motor1A, LOW);
  digitalWrite(motor2A, LOW);
}