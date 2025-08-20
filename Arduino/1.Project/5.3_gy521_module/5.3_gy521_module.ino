/*
 * MPU6050 Gyroscope and Accelerometer Reading (Arduino)
 */

#include <Adafruit_MPU6050.h>
#include <Wire.h>
#include <math.h>

// Constants
#define SERIAL_BAUD_RATE      115200 // Serial communication speed
#define READING_INTERVAL_MS   500    // Interval between sensor readings
#define ACCEL_RANGE_G         8      // Accelerometer range (±8g)
#define GYRO_RANGE_DEG        500    // Gyroscope range (±500°/s)
#define FILTER_BANDWIDTH_HZ   21     // Digital filter bandwidth

// Create MPU6050 sensor object
Adafruit_MPU6050 mpu;

void setup() {
  // Initialize serial communication
  Serial.begin(SERIAL_BAUD_RATE);
  while (!Serial) delay(10);
  
  Serial.println("MPU6050 sensor reading started.");
  
  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) delay(10);
  }
  
  // Configure sensor settings
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  
  Serial.println("MPU6050 sensor is ready.");
  Serial.println();
}

void loop() {
  // Get new sensor readings
  sensors_event_t accel, gyro, temp;
  mpu.getEvent(&accel, &gyro, &temp);
  
  // Calculate rotation angles from accelerometer data
  double xRotation = calculateXRotation(accel.acceleration.x, accel.acceleration.y, accel.acceleration.z);
  double yRotation = calculateYRotation(accel.acceleration.x, accel.acceleration.y, accel.acceleration.z);
  
  // Display formatted sensor data (similar to C code output)
  displaySensorData(gyro, accel, xRotation, yRotation);
  
  delay(READING_INTERVAL_MS);
}

// Calculate X-axis rotation from accelerometer data
double calculateXRotation(double x, double y, double z) {
  return atan2(y, sqrt(x*x + z*z)) * 180.0 / PI;
}

// Calculate Y-axis rotation from accelerometer data  
double calculateYRotation(double x, double y, double z) {
  return -atan2(x, sqrt(y*y + z*z)) * 180.0 / PI;
}

// Display sensor data in organized format (matching C code style)
void displaySensorData(sensors_event_t gyro, sensors_event_t accel, double xRot, double yRot) {
  Serial.println("--- Gyroscope (°/s) ---");
  Serial.print("X: "); Serial.print(gyro.gyro.x * 180.0/PI, 2);
  Serial.print(" | Y: "); Serial.print(gyro.gyro.y * 180.0/PI, 2);
  Serial.print(" | Z: "); Serial.print(gyro.gyro.z * 180.0/PI, 2);
  Serial.println();
  
  Serial.println("--- Accelerometer (g) ---");
  Serial.print("X: "); Serial.print(accel.acceleration.x / 9.81, 2);
  Serial.print(" | Y: "); Serial.print(accel.acceleration.y / 9.81, 2);
  Serial.print(" | Z: "); Serial.print(accel.acceleration.z / 9.81, 2);
  Serial.println();
  
  Serial.println("--- Calculated Rotation (°) ---");
  Serial.print("X-Rotation: "); Serial.print(xRot, 1);
  Serial.print(" | Y-Rotation: "); Serial.print(yRot, 1);
  Serial.println();
  
  Serial.println();
  Serial.println("----------------------------------");
  Serial.println();
}
