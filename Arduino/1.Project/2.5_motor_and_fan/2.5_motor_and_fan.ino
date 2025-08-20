/*
 * DC Motor and Fan Control Project
 * 
 * This project demonstrates bidirectional control of a DC motor or fan
 * using digital pins. The motor alternates between clockwise rotation,
 * stop, counterclockwise rotation, and stop in a continuous cycle.
 * 
 * Hardware Requirements:
 * - Arduino-compatible board
 * - DC motor or fan
 * - TA6586 motor driver IC
 * - Appropriate power supply for motor (typically 3V-12V)
 */

// Hardware Configuration Constants
#define MOTOR_PIN_A           14    // TA6586 input pin A (connects to IN1)
#define MOTOR_PIN_B           15    // TA6586 input pin B (connects to IN2)

// Timing Constants
#define ROTATION_DURATION_MS  1000  // How long motor runs in each direction (milliseconds)
#define STOP_DURATION_MS      1000  // How long motor stops between direction changes (milliseconds)

/**
 * Arduino Setup Function
 * 
 * Initializes the motor control pins as outputs.
 * This function runs once when the Arduino starts up.
 */
void setup() {
  // Configure motor control pins as outputs
  pinMode(MOTOR_PIN_A, OUTPUT);
  pinMode(MOTOR_PIN_B, OUTPUT);
  
  // Ensure motor starts in stopped state
  stopMotor();
}

/**
 * Arduino Main Loop Function
 * 
 * Continuously cycles through motor operations:
 * clockwise → stop → counterclockwise → stop → repeat
 */
void loop() {
  // Run motor clockwise
  rotateClockwise();
  delay(ROTATION_DURATION_MS);
  
  // Stop motor
  stopMotor();
  delay(STOP_DURATION_MS);
  
  // Run motor counterclockwise
  rotateCounterclockwise();
  delay(ROTATION_DURATION_MS);
  
  // Stop motor
  stopMotor();
  delay(STOP_DURATION_MS);
}

/**
 * Rotate Motor Clockwise
 * 
 * Sets the motor control pins to rotate the motor in clockwise direction.
 * Pin A is set HIGH and Pin B is set LOW to create the direction signal.
 */
void rotateClockwise() {
  digitalWrite(MOTOR_PIN_A, HIGH);
  digitalWrite(MOTOR_PIN_B, LOW);
}

/**
 * Rotate Motor Counterclockwise
 * 
 * Sets the motor control pins to rotate the motor in counterclockwise direction.
 * Pin A is set LOW and Pin B is set HIGH to reverse the direction signal.
 */
void rotateCounterclockwise() {
  digitalWrite(MOTOR_PIN_A, LOW);
  digitalWrite(MOTOR_PIN_B, HIGH);
}

/**
 * Stop Motor
 * 
 * Stops the motor by setting both control pins to LOW.
 * This removes power from the motor, causing it to stop spinning.
 */
void stopMotor() {
  digitalWrite(MOTOR_PIN_A, LOW);
  digitalWrite(MOTOR_PIN_B, LOW);
}
