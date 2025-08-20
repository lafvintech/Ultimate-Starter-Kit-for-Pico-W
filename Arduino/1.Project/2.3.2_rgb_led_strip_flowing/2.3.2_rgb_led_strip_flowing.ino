/*
  Interactive Flowing LED Strip

  Control RGB LED strip with different color modes through serial commands.
  Type commands in serial monitor to change flowing light colors.
*/

#include <Adafruit_NeoPixel.h>

// Hardware configuration
const int PIXEL_PIN = 0;            // NeoPixel strip pin
const int PIXEL_COUNT = 8;          // Number of LEDs in strip
const int FLOW_SPEED = 100;         // Default flowing speed (milliseconds)

// Color mode constants
const int MODE_RED = 1;
const int MODE_GREEN = 2;
const int MODE_BLUE = 3;
const int MODE_YELLOW = 4;
const int MODE_PURPLE = 5;
const int MODE_RAINBOW = 6;

// Current settings
int currentMode = MODE_RAINBOW;     // Start with rainbow mode
bool isRunning = true;              // Control if effect is running

// Initialize NeoPixel strip
Adafruit_NeoPixel strip(PIXEL_COUNT, PIXEL_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  // Initialize LED strip
  strip.begin();
  strip.show();
  strip.setBrightness(100);  // Set to moderate brightness
  
  // Initialize serial communication
  Serial.begin(115200);
  showWelcomeMessage();
}

void loop() {
  // Check for serial commands
  handleSerialInput();
  
  // Run flowing effect if enabled
  if (isRunning) {
    runFlowingEffect();
  }
  
  delay(FLOW_SPEED);
}

// Function to display welcome message and menu
void showWelcomeMessage() {
  Serial.println("=== Interactive Flowing LED Strip ===");
  Serial.println("Control your LED strip with these commands:");
  Serial.println("1 - Red flowing lights");
  Serial.println("2 - Green flowing lights");
  Serial.println("3 - Blue flowing lights");
  Serial.println("4 - Yellow flowing lights");
  Serial.println("5 - Purple flowing lights");
  Serial.println("6 - Rainbow flowing lights");
  Serial.println("s - Start/Stop effect");
  Serial.println("h - Show this help menu");
  Serial.println();
  Serial.println("Current mode: Rainbow flowing");
  Serial.println("Status: Running");
  Serial.println("Type a command and press Enter:");
}

// Function to handle serial input commands
void handleSerialInput() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // Clear any remaining characters
    while (Serial.available() > 0) {
      Serial.read();
    }
    
    // Process command
    switch (command) {
      case '1':
        currentMode = MODE_RED;
        Serial.println("Mode: Red flowing lights activated");
        break;
        
      case '2':
        currentMode = MODE_GREEN;
        Serial.println("Mode: Green flowing lights activated");
        break;
        
      case '3':
        currentMode = MODE_BLUE;
        Serial.println("Mode: Blue flowing lights activated");
        break;
        
      case '4':
        currentMode = MODE_YELLOW;
        Serial.println("Mode: Yellow flowing lights activated");
        break;
        
      case '5':
        currentMode = MODE_PURPLE;
        Serial.println("Mode: Purple flowing lights activated");
        break;
        
      case '6':
        currentMode = MODE_RAINBOW;
        Serial.println("Mode: Rainbow flowing lights activated");
        break;
        
      case 's':
      case 'S':
        isRunning = !isRunning;
        if (isRunning) {
          Serial.println("Effect started");
        } else {
          Serial.println("Effect stopped");
          clearAllPixels();
        }
        break;
        
      case 'h':
      case 'H':
        showWelcomeMessage();
        break;
        
      default:
        Serial.println("Unknown command. Type 'h' for help.");
        break;
    }
  }
}

// Function to run the flowing effect based on current mode
void runFlowingEffect() {
  // Shift existing colors forward
  for (int i = 0; i < PIXEL_COUNT - 1; i++) {
    strip.setPixelColor(i, strip.getPixelColor(i + 1));
  }
  
  // Add new color at the end based on current mode
  uint32_t newColor = getColorForMode(currentMode);
  strip.setPixelColor(PIXEL_COUNT - 1, newColor);
  
  // Update the strip
  strip.show();
}

// Function to get color based on selected mode
uint32_t getColorForMode(int mode) {
  switch (mode) {
    case MODE_RED:
      return strip.Color(255, 0, 0);
      
    case MODE_GREEN:
      return strip.Color(0, 255, 0);
      
    case MODE_BLUE:
      return strip.Color(0, 0, 255);
      
    case MODE_YELLOW:
      return strip.Color(255, 255, 0);
      
    case MODE_PURPLE:
      return strip.Color(128, 0, 128);
      
    case MODE_RAINBOW:
      {
        // Generate random color for rainbow effect
        int randomHue = random(65536);
        return strip.gamma32(strip.ColorHSV(randomHue));
      }
      
    default:
      return strip.Color(255, 255, 255);  // White as fallback
  }
}

// Function to clear all pixels
void clearAllPixels() {
  for (int i = 0; i < PIXEL_COUNT; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0));
  }
  strip.show();
}