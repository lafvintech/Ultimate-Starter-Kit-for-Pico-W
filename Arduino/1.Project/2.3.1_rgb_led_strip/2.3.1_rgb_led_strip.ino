/*
  Chaotic Random LED Strip

  Each LED changes to random colors at random intervals,
  creating a completely unpredictable light display.
*/

#include <Adafruit_NeoPixel.h>

// Hardware configuration
const int PIXEL_PIN = 0;            // NeoPixel strip pin
const int PIXEL_COUNT = 8;          // Number of LEDs in strip

// Random timing ranges (milliseconds)
const int MIN_CHANGE_TIME = 500;    // Minimum time before LED can change color
const int MAX_CHANGE_TIME = 3000;   // Maximum time before LED can change color

// LED data structure to track each LED independently
struct LEDData {
  unsigned long nextChangeTime;     // When this LED should change color next
  uint32_t currentColor;           // Current color of this LED
};

// Array to store data for each LED
LEDData leds[PIXEL_COUNT];

// Initialize NeoPixel strip
Adafruit_NeoPixel strip(PIXEL_COUNT, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // Initialize LED strip
  strip.begin();
  strip.show();
  strip.setBrightness(120);  // Set moderate brightness
  
  // Initialize serial communication
  Serial.begin(115200);
  Serial.println("=== Chaotic Random LED Strip ===");
  Serial.println("Each LED changes color independently at random intervals");
  Serial.println("Creating completely unpredictable light patterns");
  Serial.println();
  
  // Initialize random seed using analog noise
  randomSeed(analogRead(A0) + analogRead(A1) + analogRead(A2));
  
  // Initialize each LED with random color and random next change time
  for (int i = 0; i < PIXEL_COUNT; i++) {
    leds[i].currentColor = generateRandomColor();
    leds[i].nextChangeTime = millis() + random(MIN_CHANGE_TIME, MAX_CHANGE_TIME);
    strip.setPixelColor(i, leds[i].currentColor);
    
    // Show initial color info
    Serial.print("LED ");
    Serial.print(i);
    Serial.print(" initialized: ");
    printColorInfo(leds[i].currentColor);
    Serial.print(", next change in ");
    Serial.print((leds[i].nextChangeTime - millis()) / 1000.0, 1);
    Serial.println(" seconds");
  }
  
  // Display initial colors
  strip.show();
  Serial.println();
  Serial.println("Starting chaotic color changes...");
  Serial.println();
}

void loop() {
  unsigned long currentTime = millis();
  bool anyLEDChanged = false;
  
  // Check each LED independently
  for (int i = 0; i < PIXEL_COUNT; i++) {
    // Check if this LED should change color now
    if (currentTime >= leds[i].nextChangeTime) {
      // Generate new random color
      leds[i].currentColor = generateRandomColor();
      
      // Set new random time for next change
      leds[i].nextChangeTime = currentTime + random(MIN_CHANGE_TIME, MAX_CHANGE_TIME);
      
      // Update the LED
      strip.setPixelColor(i, leds[i].currentColor);
      
      // Log the change
      Serial.print("LED ");
      Serial.print(i);
      Serial.print(" changed to ");
      printColorInfo(leds[i].currentColor);
      Serial.print(", next change in ");
      Serial.print((leds[i].nextChangeTime - currentTime) / 1000.0, 1);
      Serial.println(" seconds");
      
      anyLEDChanged = true;
    }
  }
  
  // Update strip only if any LED changed (efficiency)
  if (anyLEDChanged) {
    strip.show();
  }
  
  // Small delay to prevent excessive CPU usage
  delay(50);
}

// Function to generate a completely random RGB color
uint32_t generateRandomColor() {
  // Generate random RGB values (0-255 each)
  int red = random(0, 256);
  int green = random(0, 256);
  int blue = random(0, 256);
  
  // Occasionally generate pure colors for variety
  if (random(0, 10) == 0) {  // 10% chance
    switch (random(0, 6)) {
      case 0: return strip.Color(255, 0, 0);     // Pure red
      case 1: return strip.Color(0, 255, 0);     // Pure green
      case 2: return strip.Color(0, 0, 255);     // Pure blue
      case 3: return strip.Color(255, 255, 0);   // Yellow
      case 4: return strip.Color(255, 0, 255);   // Magenta
      case 5: return strip.Color(0, 255, 255);   // Cyan
    }
  }
  
  return strip.Color(red, green, blue);
}

// Function to print color information in readable format
void printColorInfo(uint32_t color) {
  uint8_t r = (color >> 16) & 0xFF;
  uint8_t g = (color >> 8) & 0xFF;
  uint8_t b = color & 0xFF;
  
  Serial.print("RGB(");
  Serial.print(r);
  Serial.print(",");
  Serial.print(g);
  Serial.print(",");
  Serial.print(b);
  Serial.print(")");
}