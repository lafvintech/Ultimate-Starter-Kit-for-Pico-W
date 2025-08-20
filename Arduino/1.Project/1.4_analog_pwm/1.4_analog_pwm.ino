// Define pin array
const int pinNums[] = {6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
const int PIN_COUNT = 10;  // Number of pins

// Breathing light parameters
const int STEPS = 32;
const int MAX_DUTY = 255;  // Arduino's PWM range is 0-255
int breathPattern[STEPS];

void setup() {
  // Initialize all pins as output mode
  for (int i = 0; i < PIN_COUNT; i++) {
    pinMode(pinNums[i], OUTPUT);
  }
  
  // Generate the breathing pattern array
  for (int i = 0; i < STEPS; i++) {
    float ratio = 1.0 - abs((i - STEPS/2.0)/(STEPS/2.0));
    breathPattern[i] = int(MAX_DUTY * ratio);
  }
}

void loop() {
  // Main loop
  for (int step = 0; step < STEPS; step++) {
    for (int i = 0; i < PIN_COUNT; i++) {
      int phase = (step - i * 2) % STEPS;
      // Handle negative modulus
      if (phase < 0) {
        phase += STEPS;
      }
      analogWrite(pinNums[i], breathPattern[phase]);
    }
    delay(50);
  }
}