/*
  RGB Color Mixer

  Creates a smooth color transition effect using an RGB LED.
  Demonstrates color mixing and fading techniques.
*/

// RGB LED connections
int redPin = 13;
int greenPin = 14; 
int bluePin = 15;

// Color values
int redValue = 0;
int greenValue = 0;
int blueValue = 0;

void setup() {
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  // Cycle through color spectrum
  colorSpectrum();
  
  // Flash primary colors
  flashColors();
  
  // Breathing effect with different colors
  breathingEffect();
}

void colorSpectrum() {
  // Red to Yellow (increase green)
  for (int i = 0; i <= 255; i += 5) {
    analogWrite(redPin, 255);
    analogWrite(greenPin, i);
    analogWrite(bluePin, 0);
    delay(20);
  }
  
  // Yellow to Green (decrease red)
  for (int i = 255; i >= 0; i -= 5) {
    analogWrite(redPin, i);
    analogWrite(greenPin, 255);
    analogWrite(bluePin, 0);
    delay(20);
  }
  
  // Green to Cyan (increase blue)
  for (int i = 0; i <= 255; i += 5) {
    analogWrite(redPin, 0);
    analogWrite(greenPin, 255);
    analogWrite(bluePin, i);
    delay(20);
  }
  
  // Turn off
  analogWrite(redPin, 0);
  analogWrite(greenPin, 0);
  analogWrite(bluePin, 0);
  delay(500);
}

void flashColors() {
  // Quick color flashes
  int colors[][3] = {
    {255, 0, 0},    // Red
    {0, 255, 0},    // Green
    {0, 0, 255},    // Blue
    {255, 255, 0},  // Yellow
    {255, 0, 255},  // Magenta
    {0, 255, 255}   // Cyan
  };
  
  for (int i = 0; i < 6; i++) {
    analogWrite(redPin, colors[i][0]);
    analogWrite(greenPin, colors[i][1]);
    analogWrite(bluePin, colors[i][2]);
    delay(300);
    
    // Brief off
    analogWrite(redPin, 0);
    analogWrite(greenPin, 0);
    analogWrite(bluePin, 0);
    delay(100);
  }
}

void breathingEffect() {
  // Purple breathing
  for (int brightness = 0; brightness <= 255; brightness += 3) {
    analogWrite(redPin, brightness);
    analogWrite(greenPin, 0);
    analogWrite(bluePin, brightness);
    delay(10);
  }
  
  for (int brightness = 255; brightness >= 0; brightness -= 3) {
    analogWrite(redPin, brightness);
    analogWrite(greenPin, 0);
    analogWrite(bluePin, brightness);
    delay(10);
  }
  
  delay(300);
}