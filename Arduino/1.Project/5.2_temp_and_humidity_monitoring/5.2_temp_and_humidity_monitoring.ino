/*
 * Simple DHT11 Temperature and Humidity Monitoring (Arduino)
 */

#include <DHT.h>

// Constants
#define SENSOR_PIN            16    // Pin connected to DHT11 sensor
#define SENSOR_TYPE           DHT11 // DHT sensor type
#define SERIAL_BAUD_RATE      115200 // Serial communication speed
#define INITIAL_DELAY_S       5     // Initial sensor warm-up time (seconds)
#define READ_INTERVAL_S       2     // Interval between reads (seconds)
#define ERROR_RETRY_DELAY_MS  200   // Delay before retry on error (milliseconds)

// Create DHT sensor object
DHT sensor(SENSOR_PIN, SENSOR_TYPE);

void setup() {
  // Initialize serial communication
  Serial.begin(SERIAL_BAUD_RATE);
  
  // Initialize DHT sensor
  sensor.begin();
  
  // Allow sensor to stabilize
  Serial.println("Warming up DHT11 sensor...");
  delay(INITIAL_DELAY_S * 1000);
  Serial.println("DHT11 sensor is ready.");
}

void loop() {
  // Read humidity and temperature
  float humidity = sensor.readHumidity();
  float temperature = sensor.readTemperature();
  
  // Check if reading failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Bad reading - retrying...");
    delay(ERROR_RETRY_DELAY_MS);
  } else {
    // Print temperature and humidity in clean format
    Serial.print("Temperature: ");
    Serial.print(temperature, 1);
    Serial.print(" C, Humidity: ");
    Serial.print(humidity, 1);
    Serial.println(" %");
    
    delay(READ_INTERVAL_S * 1000);
  }
}
