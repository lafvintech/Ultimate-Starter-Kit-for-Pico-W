/*
  Motion Detection Alert System

  Uses a PIR sensor to detect motion and provides 
  alert messages with detection counting.
*/

// Pin definition and constants
const int PIR_SENSOR_PIN = 14;      // PIR sensor connected to pin 14
const int DETECTION_DELAY = 200;    // delay between readings in milliseconds

// Variables for motion tracking
bool motionDetected = false;        // current motion state
bool lastMotionState = false;       // previous state for change detection
int detectionCount = 0;             // total number of detections
unsigned long lastDetectionTime = 0; // timestamp of last detection

void setup() {
  // Configure PIR sensor pin as input
  pinMode(PIR_SENSOR_PIN, INPUT);
  
  // Initialize serial communication
  Serial.begin(115200);
  
  // Display system startup message
  showStartupMessage();
}

void loop() {
  // Check for motion detection
  checkMotionSensor();
  
  // Wait before next reading
  delay(DETECTION_DELAY);
}

// Function to display startup information
void showStartupMessage() {
  Serial.println("=== Motion Detection System ===");
  Serial.println("PIR sensor monitoring active");
  Serial.println("Waiting for motion...");
  Serial.println("==============================");
  Serial.println();
}

// Function to monitor PIR sensor and detect motion changes
void checkMotionSensor() {
  // Read current PIR sensor state
  motionDetected = digitalRead(PIR_SENSOR_PIN);
  
  // Check if motion was just detected (state change from no motion to motion)
  if (motionDetected && !lastMotionState) {
    // Record detection time and increment counter
    lastDetectionTime = millis();
    detectionCount++;
    
    // Trigger motion alert
    triggerMotionAlert();
  }
  
  // Check if motion stopped (state change from motion to no motion)
  if (!motionDetected && lastMotionState) {
    Serial.println("Motion stopped - area clear");
    Serial.println();
  }
  
  // Update last state for next comparison
  lastMotionState = motionDetected;
}

// Function to handle motion detection alert
void triggerMotionAlert() {
  Serial.println(">>> MOTION DETECTED! <<<");
  Serial.println("Alert: Movement in monitored area");
  
  // Show detection statistics
  Serial.print("Detection #");
  Serial.println(detectionCount);
  
  Serial.print("Time: ");
  Serial.print(lastDetectionTime);
  Serial.println(" ms");
  
  Serial.println("Status: ACTIVE");
  Serial.println();
}