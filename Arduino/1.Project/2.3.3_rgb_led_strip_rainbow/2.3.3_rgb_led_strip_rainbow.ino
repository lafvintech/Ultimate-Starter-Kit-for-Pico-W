/*
 * Rainbow LED Strip Project
 * 
 * This project creates a beautiful rainbow effect on an RGB LED strip
 * using the Adafruit NeoPixel library. The rainbow continuously cycles
 * through all colors creating a mesmerizing visual effect.
 * 
 * Hardware Requirements:
 * - Arduino-compatible board
 * - WS2812B RGB LED strip (8 pixels)
 * - Appropriate power supply for LED strip
 */

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif

// Hardware Configuration Constants
#define LED_STRIP_PIN         0     // Digital pin connected to LED strip data line
#define LED_PIXEL_COUNT       8     // Number of pixels in the LED strip
#define LED_STRIP_TYPE        (NEO_GRB + NEO_KHZ800)  // LED strip specifications

// Animation Constants
#define RAINBOW_DELAY_MS      10    // Delay between rainbow animation frames (milliseconds)
#define COLOR_WHEEL_MAX       65536 // Maximum value for HSV color wheel
#define HUE_INCREMENT_STEP    256   // Step size for hue progression
#define BRIGHTNESS_MAX        255   // Maximum brightness value
#define SATURATION_MAX        255   // Maximum saturation value

// Create NeoPixel strip object with specified configuration
Adafruit_NeoPixel ledStrip(LED_PIXEL_COUNT, LED_STRIP_PIN, LED_STRIP_TYPE);


/**
 * Arduino Setup Function
 * 
 * Initializes the LED strip and prepares it for operation.
 * This function runs once when the Arduino starts up.
 */
void setup() {
  // Initialize the LED strip hardware
  ledStrip.begin();
  
  // Turn off all pixels initially
  clearAllPixels();
  
  // Display the initial state
  ledStrip.show();
}

/**
 * Arduino Main Loop Function
 * 
 * Continuously runs the rainbow animation effect.
 * This function repeats indefinitely while the Arduino is powered.
 */
void loop() {
  displayRainbowEffect();
}



/**
 * Clear All Pixels
 * 
 * Turns off all pixels in the LED strip by setting them to black (0,0,0).
 * This provides a clean starting state for animations.
 */
void clearAllPixels() {
  for (int i = 0; i < LED_PIXEL_COUNT; i++) {
    ledStrip.setPixelColor(i, 0, 0, 0);  // Set pixel to black (off)
  }
}

/**
 * Display Rainbow Effect
 * 
 * Creates a continuous rainbow animation that cycles through all colors
 * of the spectrum. The rainbow moves smoothly across the entire LED strip.
 * 
 * The effect works by:
 * 1. Cycling through all possible hue values (0-65535)
 * 2. Distributing colors evenly across all pixels
 * 3. Creating a smooth color transition between adjacent pixels
 */
void displayRainbowEffect() {
  // Cycle through the complete color wheel
  for (long startingHue = 0; startingHue < COLOR_WHEEL_MAX; startingHue += HUE_INCREMENT_STEP) {
    
    // Set color for each pixel in the strip
    for (int pixelIndex = 0; pixelIndex < LED_PIXEL_COUNT; pixelIndex++) {
      
      // Calculate the hue for this specific pixel
      // This creates an even distribution of colors across the strip
      int currentPixelHue = startingHue + (pixelIndex * COLOR_WHEEL_MAX / LED_PIXEL_COUNT);
      
      // Convert HSV color to RGB and apply gamma correction for better color accuracy
      uint32_t pixelColor = ledStrip.gamma32(
        ledStrip.ColorHSV(currentPixelHue, SATURATION_MAX, BRIGHTNESS_MAX)
      );
      
      // Set the calculated color to the current pixel
      ledStrip.setPixelColor(pixelIndex, pixelColor);
    }
    
    // Update the LED strip to display the new colors
    ledStrip.show();
    
    // Wait before the next animation frame
    delay(RAINBOW_DELAY_MS);
  }
}
