/*
  Chaser Light

  Controls 10 LEDs in sequence with different animation patterns:
  - Odd positioned LEDs (0, 2, 4, 6, 8)
  - Even positioned LEDs (1, 3, 5, 7, 9)
  - All LEDs in sequence (0 to 9)

*/

// LED pins array - using pins 6 through 15
const int ledPins[] = {6, 7, 8, 9, 10, 11, 12, 13, 14, 15};
const int numLeds = 10;
const int delayTime = 300;  // delay between LED changes

void setup() {
  // initialize all LED pins as outputs
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);  // turn off all LEDs initially
  }
}

void loop() {
  // Pattern 1: Light odd positioned LEDs (0, 2, 4, 6, 8)
  lightOddLeds();
  delay(delayTime);
  
  // Pattern 2: Light even positioned LEDs (1, 3, 5, 7, 9)
  lightEvenLeds();
  delay(delayTime);
  
  // Pattern 3: Light all LEDs in sequence
  lightAllLeds();
  delay(delayTime);
}

void lightOddLeds() {
  for (int i = 0; i < numLeds; i += 2) {  // 0, 2, 4, 6, 8
    digitalWrite(ledPins[i], HIGH);   // turn LED on
    delay(delayTime);
    digitalWrite(ledPins[i], LOW);    // turn LED off
  }
}

void lightEvenLeds() {
  for (int i = 1; i < numLeds; i += 2) {  // 1, 3, 5, 7, 9
    digitalWrite(ledPins[i], HIGH);   // turn LED on
    delay(delayTime);
    digitalWrite(ledPins[i], LOW);    // turn LED off
  }
}

void lightAllLeds() {
  for (int i = 0; i < numLeds; i++) {  // 0 to 9
    digitalWrite(ledPins[i], HIGH);   // turn LED on
    delay(delayTime);
    digitalWrite(ledPins[i], LOW);    // turn LED off
  }
}
