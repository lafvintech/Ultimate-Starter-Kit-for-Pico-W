const int slidePin = 14;  // Define the pin connected to the slide switch
int state = 0;            // Variable to store the state of the switch

void setup() {
  pinMode(slidePin, INPUT);  // Set the slide switch pin as an input
  Serial.begin(115200);      // Initialize serial communication at 115200 baud rate
}

void loop() {
  state = digitalRead(slidePin);  // Read the state of the slide switch
  if (state == HIGH) {            // Check if the switch is in the HIGH position
    Serial.println("ON");         // Print "ON" to the serial monitor
  }
  else {                          // If the switch is not HIGH (i.e., LOW)
    Serial.println("OFF");        // Print "OFF" to the serial monitor
  }
}