/*
 * Servo Motor Swinging Project
 * 
 * This project demonstrates smooth servo motor control by creating
 * a continuous swinging motion from 0 to 180 degrees and back.
 * The servo sweeps back and forth in a pendulum-like motion.
 * 
 * Hardware Requirements:
 * - Arduino-compatible board
 * - Standard servo motor (SG90 or similar)
 * - Appropriate power supply for servo
 */

#include <Servo.h>

// Hardware Configuration Constants
#define SERVO_CONTROL_PIN     15    // Digital pin connected to servo signal wire

// Movement Constants
#define SERVO_MIN_ANGLE       0     // Minimum servo angle (degrees)
#define SERVO_MAX_ANGLE       180   // Maximum servo angle (degrees)
#define SERVO_STEP_DELAY_MS   15    // Delay between each degree step (milliseconds)
#define STARTUP_DELAY_MS      1000  // Initial delay after servo attachment (milliseconds)

// Create servo object to control the servo motor
Servo servoMotor;

/**
 * Arduino Setup Function
 * 
 * Initializes the servo motor and sets it to the starting position.
 * This function runs once when the Arduino starts up.
 */
void setup() {
  // Attach servo to the specified control pin
  servoMotor.attach(SERVO_CONTROL_PIN);
  
  // Move servo to starting position (0 degrees)
  servoMotor.write(SERVO_MIN_ANGLE);
  
  // Wait for servo to reach starting position
  delay(STARTUP_DELAY_MS);
}

/**
 * Arduino Main Loop Function
 * 
 * Continuously performs the servo swinging motion.
 * Creates a smooth back-and-forth pendulum effect.
 */
void loop() {
  // Perform complete swinging cycle
  performSwingingMotion();
}

/**
 * Perform Complete Swinging Motion
 * 
 * Executes one full cycle of servo movement:
 * 1. Swing from minimum to maximum angle
 * 2. Swing back from maximum to minimum angle
 */
void performSwingingMotion() {
  // Swing forward: from 0 to 180 degrees
  swingServoForward();
  
  // Swing backward: from 180 to 0 degrees
  swingServoBackward();
}

/**
 * Swing Servo Forward
 * 
 * Moves the servo smoothly from minimum angle to maximum angle.
 * Each step is delayed to create smooth, visible movement.
 */
void swingServoForward() {
  for (int currentAngle = SERVO_MIN_ANGLE; currentAngle <= SERVO_MAX_ANGLE; currentAngle++) {
    // Set servo to current angle position
    servoMotor.write(currentAngle);
    
    // Wait for servo to reach position before next step
    delay(SERVO_STEP_DELAY_MS);
  }
}

/**
 * Swing Servo Backward
 * 
 * Moves the servo smoothly from maximum angle back to minimum angle.
 * Each step is delayed to create smooth, visible movement.
 */
void swingServoBackward() {
  for (int currentAngle = SERVO_MAX_ANGLE; currentAngle >= SERVO_MIN_ANGLE; currentAngle--) {
    // Set servo to current angle position
    servoMotor.write(currentAngle);
    
    // Wait for servo to reach position before next step
    delay(SERVO_STEP_DELAY_MS);
  }
}
