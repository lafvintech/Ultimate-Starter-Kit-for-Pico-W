#include <DHT.h>

#define DHTPIN 16     // Define the pin connected to the DHT11 sensor
#define DHTTYPE DHT11 // Define the type of sensor used

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
  delay(5000);  // Initial delay of 5 seconds
}

void loop() {
  // Read humidity and temperature
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // Check if reading failed
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
  } else {
    // Print temperature and humidity
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C\nHumidity: ");
    Serial.print(humidity);
    Serial.println(" %");
  }

  delay(4000);  // Wait for 4 seconds
}
