// Define analog pins for joystick X and Y axes
const int X_PIN = A1;  // X-axis connected to analog pin A1
const int Y_PIN = A0;  // Y-axis connected to analog pin A0

void setup() {
  Serial.begin(9600);  // Initialize serial communication at 9600 baud rate
}

void loop() {
  // Read analog values from joystick X and Y axes
  int xValue = analogRead(X_PIN);  // Read X-axis analog value (range: 0-1023)
  int yValue = analogRead(Y_PIN);  // Read Y-axis analog value (range: 0-1023)

  // Output the read X and Y values through serial communication
  Serial.print("X: ");
  Serial.print(xValue);  // Output X-axis value
  Serial.print("  Y: ");
  Serial.println(yValue);  // Output Y-axis value and move to next line

  delay(200);  // Delay for 200 milliseconds to control reading and output frequency
}
