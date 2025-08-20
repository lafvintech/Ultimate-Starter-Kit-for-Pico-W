/*
 * Ultrasonic Distance Sensor Project
 * 
 * Measures distance using HC-SR04 ultrasonic sensor with professional
 * error handling and timeout protection. Based on sound wave travel time
 * calculation with accurate physics constants.
 * 
 * Hardware: HC-SR04 ultrasonic sensor (Trigger + Echo pins)
 */

// Pin Configuration Constants
#define TRIGGER_PIN           17    // Ultrasonic sensor trigger pin
#define ECHO_PIN              16    // Ultrasonic sensor echo pin

// Physics Constants
#define SOUND_SPEED_CM_PER_US 0.0343 // Speed of sound: 343 m/s = 0.0343 cm/µs
#define PULSE_TRIGGER_US      10     // Trigger pulse duration (microseconds)
#define PULSE_DELAY_US        2      // Pre-trigger delay (microseconds)

// Measurement Constants
#define ECHO_TIMEOUT_US       25000  // Maximum wait time for echo (µs) ≈ 4.3m max range
#define MEASUREMENT_DELAY_MS  500    // Delay between measurements (milliseconds)
#define SERIAL_BAUD_RATE      115200 // Serial communication speed

// Measurement Range Constants
#define MIN_DISTANCE_CM       2.0    // Minimum measurable distance
#define MAX_DISTANCE_CM       400.0  // Maximum measurable distance

void setup() {
  // Initialize serial communication
  Serial.begin(SERIAL_BAUD_RATE);
  
  // Configure ultrasonic sensor pins
  setupUltrasonicSensor();
  
  // Display startup information
  Serial.println("=== Ultrasonic Distance Sensor ===");
  Serial.println("Range: 2cm - 400cm");
  Serial.println("Accuracy: ±1cm");
  Serial.println("==================================");
}

void loop() {
  float distance = measureDistance();
  displayMeasurement(distance);
  delay(MEASUREMENT_DELAY_MS);
}

/**
 * Setup Ultrasonic Sensor
 * Initializes the trigger and echo pins for the HC-SR04 sensor.
 */
void setupUltrasonicSensor() {
  pinMode(ECHO_PIN, INPUT);
  pinMode(TRIGGER_PIN, OUTPUT);
  digitalWrite(TRIGGER_PIN, LOW);  // Ensure trigger starts LOW
}

/**
 * Measure Distance
 * Performs ultrasonic distance measurement with timeout protection.
 * Returns -1.0 on timeout or invalid measurement.
 */
float measureDistance() {
  // Send trigger pulse
  sendTriggerPulse();
  
  // Measure echo pulse duration with timeout protection
  unsigned long pulseDuration = measureEchoPulse();
  
  // Check for timeout
  if (pulseDuration == 0) {
    return -1.0;  // Measurement failed
  }
  
  // Calculate distance using physics formula
  float distance = calculateDistanceFromPulse(pulseDuration);
  
  // Validate measurement range
  if (distance < MIN_DISTANCE_CM || distance > MAX_DISTANCE_CM) {
    return -1.0;  // Out of valid range
  }
  
  return distance;
}

/**
 * Send Trigger Pulse
 * Sends a 10µs pulse to trigger the ultrasonic measurement.
 */
void sendTriggerPulse() {
  digitalWrite(TRIGGER_PIN, LOW);
  delayMicroseconds(PULSE_DELAY_US);
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(PULSE_TRIGGER_US);
  digitalWrite(TRIGGER_PIN, LOW);
}

/**
 * Measure Echo Pulse
 * Measures the duration of the echo pulse with timeout protection.
 * Returns 0 on timeout, pulse duration in microseconds on success.
 */
unsigned long measureEchoPulse() {
  // Use pulseIn with timeout for reliable measurement
  unsigned long duration = pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT_US);
  return duration;  // Returns 0 if timeout occurred
}

/**
 * Calculate Distance From Pulse
 * Converts pulse duration to distance using sound speed.
 * Distance = (Pulse_Duration * Sound_Speed) / 2
 */
float calculateDistanceFromPulse(unsigned long pulseDuration) {
  // Convert microseconds to distance in centimeters
  // Divide by 2 because sound travels to object and back
  return (pulseDuration * SOUND_SPEED_CM_PER_US) / 2.0;
}

/**
 * Display Measurement
 * Shows measurement result with appropriate error handling.
 */
void displayMeasurement(float distance) {
  if (distance > 0) {
    Serial.print("Distance: ");
    Serial.print(distance, 1);  // Show 1 decimal place
    Serial.println(" cm");
  } else {
    Serial.println("Measurement failed (Timeout or Out of Range)");
  }
}
