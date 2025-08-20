/*
  LED Brightness Controller

  Controls LED brightness using a potentiometer input.
  Shows real-time values and provides smooth brightness control.
*/

// Pin definitions and constants
const int POTENTIOMETER_PIN = A2;   // potentiometer connected to analog pin A2
const int LED_PIN = 15;             // LED connected to pin 15
const int READING_DELAY = 100;      // delay between readings in milliseconds
const int MIN_ANALOG_VALUE = 0;     // minimum analog reading
const int MAX_ANALOG_VALUE = 1023;  // maximum analog reading
const int MIN_PWM_VALUE = 0;        // minimum PWM output
const int MAX_PWM_VALUE = 255;      // maximum PWM output

// Variables for brightness control
int currentReading = 0;             // current potentiometer reading
int ledBrightness = 0;              // calculated LED brightness
int lastReading = -1;               // previous reading for change detection

void setup() {
  // Configure LED pin as output
  pinMode(LED_PIN, OUTPUT);
  
  // Initialize serial communication
  Serial.begin(115200);
  
  // Display control information
  showControlInfo();
}

void loop() {
  // Read potentiometer and update LED
  updateBrightnessControl();
  
  // Wait before next reading
  delay(READING_DELAY);
}

// Function to display control information at startup
void showControlInfo() {
  Serial.println("=== LED Brightness Controller ===");
  Serial.println("Turn potentiometer to adjust brightness");
  Serial.println("Range: 0% to 100% brightness");
  Serial.println("================================");
  Serial.println();
}

// Function to read potentiometer and control LED brightness
void updateBrightnessControl() {
  // Read current potentiometer value
  currentReading = analogRead(POTENTIOMETER_PIN);
  
  // Convert analog reading to PWM value for LED brightness
  ledBrightness = map(currentReading, MIN_ANALOG_VALUE, MAX_ANALOG_VALUE, 
                     MIN_PWM_VALUE, MAX_PWM_VALUE);
  
  // Apply brightness to LED
  analogWrite(LED_PIN, ledBrightness);
  
  // Only display info when value changes significantly (reduce serial spam)
  if (abs(currentReading - lastReading) > 10) {
    displayCurrentStatus();
    lastReading = currentReading;
  }
}

// Function to display current brightness status
void displayCurrentStatus() {
  // Calculate percentage for user-friendly display
  int brightnessPercent = map(ledBrightness, MIN_PWM_VALUE, MAX_PWM_VALUE, 0, 100);
  
  Serial.print("Potentiometer: ");
  Serial.print(currentReading);
  Serial.print(" | LED Brightness: ");
  Serial.print(ledBrightness);
  Serial.print("/255 (");
  Serial.print(brightnessPercent);
  Serial.println("%)");
  
  // Show visual brightness indicator
  Serial.print("Brightness: [");
  int barLength = brightnessPercent / 10;  // scale to 0-10 for visual bar
  for (int i = 0; i < 10; i++) {
    if (i < barLength) {
      Serial.print("█");
    } else {
      Serial.print("░");
    }
  }
  Serial.println("]");
  Serial.println();
}