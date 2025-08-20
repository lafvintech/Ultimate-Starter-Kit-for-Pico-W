#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Initialize LCD object with I2C address 0x27, 16 columns and 2 rows
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  // Initialize I2C communication
  Wire.begin();
  // Initialize LCD
  lcd.init();
  // Turn on the backlight
  lcd.backlight();
  
  // Display the first line message
  lcd.setCursor(0, 0); // Set cursor position to the first column of the first row
  lcd.print("From Lafvin");
  
  // Wait for 2 seconds
  delay(2000);
  
  // Clear the display
  lcd.clear();
  
  // Display the second line message
  lcd.setCursor(0, 0); // Set cursor position to the first column of the first row
  lcd.print("Hello");
  lcd.setCursor(0, 1); // Set cursor position to the first column of the second row
  lcd.print("       World!");
  
  // Wait for 5 seconds
  delay(5000);
  
  // Clear the display
  lcd.clear();
}

void loop() {
  // Empty loop, no operation
}
