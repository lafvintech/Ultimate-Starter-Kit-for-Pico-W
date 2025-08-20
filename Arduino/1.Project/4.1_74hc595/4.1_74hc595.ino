/*
 * 74HC595 Smooth Flowing LED Project
 * 
 * Creates a smooth flowing LED effect using a 74HC595 shift register.
 * LEDs progressively light up and then smoothly flow back, creating
 * a continuous mesmerizing water-like animation.
 * 
 * Hardware: 74HC595 shift register + 8 LEDs with current limiting resistors
 */

// 74HC595 Pin Configuration Constants
#define LATCH_PIN             1     // ST_CP (Storage Register Clock) - pin 12 of 74HC595
#define CLOCK_PIN             2     // SH_CP (Shift Register Clock) - pin 11 of 74HC595  
#define DATA_PIN              0     // DS (Serial Data Input) - pin 14 of 74HC595

// Animation Timing Constants
#define FLOW_DELAY_MS         150   // Delay between flow steps for smooth animation

// Smooth Flowing LED Patterns
byte flowPatterns[] = {
  0b00000000,  // All off (start)
  0b00000001,  // 1 LED
  0b00000011,  // 2 LEDs
  0b00000111,  // 3 LEDs
  0b00001111,  // 4 LEDs
  0b00011111,  // 5 LEDs
  0b00111111,  // 6 LEDs
  0b01111111,  // 7 LEDs
  0b11111111,  // All on (peak)
  0b11111110,  // Flow back: 7 LEDs
  0b11111100,  // 6 LEDs
  0b11111000,  // 5 LEDs
  0b11110000,  // 4 LEDs
  0b11100000,  // 3 LEDs
  0b11000000,  // 2 LEDs
  0b10000000,  // 1 LED
  0b00000000   // All off (end cycle)
};

/**
 * Arduino Setup Function
 * Initializes the 74HC595 control pins as outputs.
 */
void setup() {
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);
  
  // Clear all LEDs initially
  updateShiftRegister(0b00000000);
}

/**
 * Arduino Main Loop Function
 * Continuously runs the smooth flowing LED animation.
 */
void loop() {
  runSmoothFlowingAnimation();
}

/**
 * Update Shift Register
 * Sends data to 74HC595 and latches the output.
 */
void updateShiftRegister(byte pattern) {
  digitalWrite(LATCH_PIN, LOW);                    // Prepare for data
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, pattern); // Send 8 bits
  digitalWrite(LATCH_PIN, HIGH);                   // Latch data to outputs
}

/**
 * Run Smooth Flowing Animation
 * Creates a mesmerizing water-like flow effect that builds up
 * all LEDs then smoothly flows back to create continuous motion.
 */
void runSmoothFlowingAnimation() {
  for (int i = 0; i < sizeof(flowPatterns); i++) {
    updateShiftRegister(flowPatterns[i]);
    delay(FLOW_DELAY_MS);
  }
}
