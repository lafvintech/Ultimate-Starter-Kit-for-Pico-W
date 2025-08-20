/*
 * MPR121 Capacitive Touch Sensor Project
 * 
 * Reads 12-channel touch input and displays touch patterns.
 * Hardware: MPR121 breakout board connected via I2C
 */

#include <Wire.h>
#include "Adafruit_MPR121.h"

// Configuration Constants
#define TOUCH_CHANNELS        12      // Number of touch channels
#define MPR121_ADDRESS        0x5A    // Default I2C address
#define SERIAL_BAUD           115200  // Serial communication speed

// Create touch sensor object and state variables
Adafruit_MPR121 touchSensor = Adafruit_MPR121();
uint16_t lastTouched = 0;
uint16_t currentTouched = 0;
boolean touchState[TOUCH_CHANNELS];


/**
 * Arduino Setup Function
 * Initializes serial communication and MPR121 touch sensor.
 */
void setup() {
  Serial.begin(SERIAL_BAUD);
  while (!Serial) delay(10);  // Wait for serial connection
  
  Serial.println("MPR121 Touch Sensor Initializing...");
  
  if (!touchSensor.begin(MPR121_ADDRESS)) {
    Serial.println("MPR121 not found! Check wiring.");
    while (1);  // Halt if sensor not found
  }
}

/**
 * Arduino Main Loop Function
 * Monitors touch states and displays changes.
 */
void loop() {
  currentTouched = touchSensor.touched();
  
  // Only display when touch state changes
  if (currentTouched != lastTouched) {
    updateTouchStates();
    displayTouchPattern();
    lastTouched = currentTouched;
  }
}

/**
 * Update Individual Touch States
 * Extracts each channel state using bit manipulation.
 */
void updateTouchStates() {
  for (int i = 0; i < TOUCH_CHANNELS; i++) {
    touchState[i] = (currentTouched & (1 << i)) ? true : false;
  }
}

/**
 * Display Touch Pattern
 * Shows current touch state as binary pattern.
 */
void displayTouchPattern() {
  Serial.print("Touch: ");
  for (int i = 0; i < TOUCH_CHANNELS; i++) {
    Serial.print(touchState[i] ? "1" : "0");
  }
  Serial.println();
}