/*
  Digital Thermometer

  Reads temperature from a thermistor and displays 
  the temperature in both Celsius and Fahrenheit.
*/

// Pin and sensor constants
const int THERMISTOR_PIN = A2;      // thermistor connected to analog pin A2
const int BETA_VALUE = 3950;        // beta coefficient of the thermistor
const int PULLUP_RESISTANCE = 10;   // pull-up resistor value in kOhms
const int UPDATE_INTERVAL = 1000;   // reading interval in milliseconds

// Temperature calculation constants
const float ROOM_TEMP_KELVIN = 298.0;  // room temperature in Kelvin (25°C)
const float KELVIN_OFFSET = 273.0;     // conversion offset from Celsius to Kelvin

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  Serial.println("=== Digital Thermometer ===");
  Serial.println("Reading temperature from thermistor...");
  Serial.println();
}

void loop() {
  // Read temperature and display results
  readAndDisplayTemperature();
  
  // Wait before next reading
  delay(UPDATE_INTERVAL);
}

// Function to read thermistor and calculate temperature
void readAndDisplayTemperature() {
  // Read raw analog value from thermistor
  int analogValue = analogRead(THERMISTOR_PIN);
  
  // Calculate temperature using the same logic as reference code
  // Convert ADC reading to voltage (Arduino: 0-1023 maps to 0-3.3V)
  float voltage = (float)analogValue / 1023.0 * 3.3;
  
  // Calculate thermistor resistance using voltage divider formula
  float thermistorResistance = PULLUP_RESISTANCE * voltage / (3.3 - voltage);
  
  // Calculate temperature using Beta equation (same as reference)
  float tempKelvin = 1.0 / (1.0 / (273.15 + 25) + log(thermistorResistance / PULLUP_RESISTANCE) / BETA_VALUE);
  float tempCelsius = tempKelvin - 273.15;
  
  // Convert to Fahrenheit
  float tempFahrenheit = (tempCelsius * 1.8) + 32.0;
  
  // Display temperature readings
  Serial.print("Temperature: ");
  Serial.print(tempCelsius, 1);  // 1 decimal place
  Serial.print("°C (");
  Serial.print(tempFahrenheit, 1);
  Serial.print("°F)");
  
  // Show temperature category
  if (tempCelsius < 15) {
    Serial.println(" - Cold");
  } else if (tempCelsius < 25) {
    Serial.println(" - Cool");
  } else if (tempCelsius < 30) {
    Serial.println(" - Comfortable");
  } else {
    Serial.println(" - Warm");
  }
}