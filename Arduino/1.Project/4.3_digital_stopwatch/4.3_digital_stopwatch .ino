/*
 * 4-Digit Timer Display Project
 * 
 * Shows elapsed time in seconds on 4 seven-segment displays.
 * Counts from 0000 to 9999, then resets automatically.
 * Hardware: 74HC595 shift register + 4 seven-segment displays
 */

// Pin connections
#define LATCH_PIN             19    // 74HC595 latch pin
#define CLOCK_PIN             20    // 74HC595 clock pin
#define DATA_PIN              18    // 74HC595 data pin

// Digit control pins (which digit to show)
const int digitPins[4] = {13, 12, 11, 10};  // Ones, tens, hundreds, thousands

// Patterns for digits 0-9 on seven-segment display
byte digitCode[10] = {
  0x3F,  // 0
  0x06,  // 1
  0x5B,  // 2
  0x4F,  // 3
  0x66,  // 4
  0x6D,  // 5
  0x7D,  // 6
  0x07,  // 7
  0x7F,  // 8
  0x6F   // 9
};

unsigned long startTime = 0;


void setup() {
  // Set up 74HC595 pins
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);
  
  // Set up digit control pins
  for (int i = 0; i < 4; i++) {
    pinMode(digitPins[i], OUTPUT);
    digitalWrite(digitPins[i], HIGH);  // Turn off all digits
  }
  
  startTime = millis();  // Start the timer
}

void loop() {
  // Calculate how many seconds have passed
  unsigned int seconds = (millis() - startTime) / 1000;
  
  // Reset timer after 9999 seconds
  if (seconds > 9999) {
    startTime = millis();
    seconds = 0;
  }
  
  // Show the timer on display
  showNumber(seconds);
}

// Display a 4-digit number
void showNumber(int number) {
  // Break number into individual digits
  int digit1 = number % 10;        // Ones
  int digit2 = (number / 10) % 10; // Tens  
  int digit3 = (number / 100) % 10;// Hundreds
  int digit4 = (number / 1000) % 10;// Thousands
  
  // Show each digit quickly in turn (multiplexing)
  showDigit(0, digit1);
  showDigit(1, digit2); 
  showDigit(2, digit3);
  showDigit(3, digit4);
}

// Show one digit at specified position
void showDigit(int position, int digit) {
  // Turn off all digits first
  for (int i = 0; i < 4; i++) {
    digitalWrite(digitPins[i], HIGH);
  }
  
  // Turn on the digit we want
  digitalWrite(digitPins[position], LOW);
  
  // Send the digit pattern to 74HC595
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, digitCode[digit]);
  digitalWrite(LATCH_PIN, HIGH);
  
  delay(1);  // Small delay for smooth display
}
