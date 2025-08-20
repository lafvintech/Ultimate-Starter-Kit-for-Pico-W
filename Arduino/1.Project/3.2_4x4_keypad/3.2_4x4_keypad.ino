/*
 * 4x4 Matrix Keypad Input Project
 * 
 * This project demonstrates reading input from a 4x4 matrix keypad
 * using the Adafruit_Keypad library. The keypad provides 16 buttons
 * including numbers (0-9), letters (A-D), and symbols (* #).
 * 
 * Hardware Requirements:
 * - Arduino-compatible board
 * - 4x4 matrix keypad
 * - 8 digital pins for keypad connections
 * - Serial monitor for output display
 */

#include "Adafruit_Keypad.h"

// Keypad Configuration Constants
#define KEYPAD_ROWS           4     // Number of rows in the keypad matrix
#define KEYPAD_COLS           4     // Number of columns in the keypad matrix

// Communication Constants
#define SERIAL_BAUD_RATE      115200  // Serial communication speed
#define KEYPAD_SCAN_DELAY_MS  10      // Delay between keypad scans (milliseconds)

// Hardware Pin Configuration Constants
#define ROW_PIN_1             2     // First row pin connection
#define ROW_PIN_2             3     // Second row pin connection
#define ROW_PIN_3             4     // Third row pin connection
#define ROW_PIN_4             5     // Fourth row pin connection

#define COL_PIN_1             6     // First column pin connection
#define COL_PIN_2             7     // Second column pin connection
#define COL_PIN_3             8     // Third column pin connection
#define COL_PIN_4             9     // Fourth column pin connection

// Keypad layout mapping - defines what character each button represents
char keypadLayout[KEYPAD_ROWS][KEYPAD_COLS] = {
  { '1', '2', '3', 'A' },  // First row: numbers and letter A
  { '4', '5', '6', 'B' },  // Second row: numbers and letter B
  { '7', '8', '9', 'C' },  // Third row: numbers and letter C
  { '*', '0', '#', 'D' }   // Fourth row: symbols and letter D
};

// Pin mapping arrays for keypad connections
byte rowPinConnections[KEYPAD_ROWS] = { ROW_PIN_1, ROW_PIN_2, ROW_PIN_3, ROW_PIN_4 };
byte colPinConnections[KEYPAD_COLS] = { COL_PIN_1, COL_PIN_2, COL_PIN_3, COL_PIN_4 };

// Create keypad object with configuration
Adafruit_Keypad matrixKeypad = Adafruit_Keypad(
  makeKeymap(keypadLayout), 
  rowPinConnections, 
  colPinConnections, 
  KEYPAD_ROWS, 
  KEYPAD_COLS
);

/**
 * Arduino Setup Function
 * 
 * Initializes serial communication and the keypad hardware.
 * This function runs once when the Arduino starts up.
 */
void setup() {
  // Initialize serial communication for output display
  Serial.begin(SERIAL_BAUD_RATE);
  
  // Initialize the matrix keypad
  matrixKeypad.begin();
  
  // Display startup information
  Serial.println("=== 4x4 Matrix Keypad Controller ===");
  Serial.println("Press any key on the keypad...");
  Serial.println("Available keys: 0-9, A-D, *, #");
  Serial.println("===================================");
}

/**
 * Arduino Main Loop Function
 * 
 * Continuously scans the keypad for button presses and releases,
 * then displays the events to the serial monitor.
 */
void loop() {
  // Scan keypad for any state changes
  scanKeypadForEvents();
  
  // Small delay to prevent excessive CPU usage
  delay(KEYPAD_SCAN_DELAY_MS);
}

/**
 * Scan Keypad for Events
 * 
 * Updates the keypad state and processes any key press or release events.
 * Displays formatted output for each detected event.
 */
void scanKeypadForEvents() {
  // Update the internal state of all keys
  matrixKeypad.tick();
  
  // Process all available keypad events
  while (matrixKeypad.available()) {
    // Read the next keypad event
    keypadEvent currentEvent = matrixKeypad.read();
    
    // Process and display the event
    processKeypadEvent(currentEvent);
  }
}

/**
 * Process Keypad Event
 * 
 * Analyzes a keypad event and displays appropriate information
 * about which key was pressed or released.
 * 
 * @param event The keypad event to process
 */
void processKeypadEvent(keypadEvent event) {
  // Extract the key character from the event
  char pressedKey = (char)event.bit.KEY;
  
  // Display the key that was pressed
  Serial.print("Key '");
  Serial.print(pressedKey);
  Serial.print("' ");
  
  // Display the type of event (press or release)
  if (event.bit.EVENT == KEY_JUST_PRESSED) {
    Serial.println("PRESSED");
  } else if (event.bit.EVENT == KEY_JUST_RELEASED) {
    Serial.println("RELEASED");
  }
}
