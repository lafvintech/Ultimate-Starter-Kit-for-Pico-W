/*
  Automatic Night Light

  Uses a photoresistor to control LED brightness automatically.
  Bright environment = dim LED, dark environment = bright LED.
*/

// Pin connections
const int LIGHT_SENSOR_PIN = A2;    // photoresistor on analog pin A2
const int LED_PIN = 15;             // LED on digital pin 15

// Settings
const int UPDATE_DELAY = 200;       // how often to check sensor (milliseconds)

void setup() {
  // Set up pins
  pinMode(LED_PIN, OUTPUT);
  
  // Start serial for monitoring
  Serial.begin(115200);
  Serial.println("Automatic Night Light Started!");
  Serial.println("Cover sensor = LED gets brighter");
  Serial.println("Expose sensor to light = LED gets dimmer");
  Serial.println();
}

void loop() {
  // Read light sensor (0-1023)
  int lightReading = analogRead(LIGHT_SENSOR_PIN);
  
  // Convert to LED brightness (0-255)
  // Note: our sensor gives HIGH values in dark, LOW values in bright light
  int ledBrightness = map(lightReading, 0, 1023, 0, 255);
  
  // Set LED brightness
  analogWrite(LED_PIN, ledBrightness);
  
  // Show current values
  Serial.print("Light sensor: ");
  Serial.print(lightReading);
  Serial.print(" -> LED brightness: ");
  Serial.print(ledBrightness);
  Serial.print("/255");
  
  // Show simple status
  if (lightReading > 700) {
    Serial.println(" (Dark - LED bright)");
  } else if (lightReading > 400) {
    Serial.println(" (Medium - LED medium)");
  } else {
    Serial.println(" (Bright - LED dim)");
  }
  
  delay(UPDATE_DELAY);
}