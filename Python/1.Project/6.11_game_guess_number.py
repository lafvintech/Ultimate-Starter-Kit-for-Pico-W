# 6.11_game_guess_number_pro.py
# A professionally refactored version of the Number Guessing Game.
#
# Key Improvements:
# - Uses internal pull-down resistors for the keypad, removing the need for external ones.
# - Implements proper debouncing and state management for reliable key presses.
# - Features a more robust and responsive game loop.
# - Provides a clearer and more interactive user experience on the LCD.

from lcd1602 import LCD
from machine import I2C, Pin
import time
import urandom

# --- Hardware & Game Configuration ---
# LCD Display (I2C bus 0)
LCD_SDA_PIN = 20
LCD_SCL_PIN = 21

# 4x4 Keypad Pins
ROW_PINS = [2, 3, 4, 5]
COL_PINS = [6, 7, 8, 9]

# Keypad Layout
KEYPAD_LAYOUT = [
    ["1", "2", "3", "A"],
    ["4", "5", "6", "B"],
    ["7", "8", "9", "C"],
    ["*", "0", "#", "D"]
]

class GuessTheNumberGame:
    """
    Encapsulates all logic for the number guessing game.
    """
    def __init__(self):
        """Initializes hardware and game state."""
        print("Initializing Guess The Number Game...")
        # Hardware
        self.i2c = I2C(0, sda=Pin(LCD_SDA_PIN), scl=Pin(LCD_SCL_PIN), freq=400000)
        self.lcd = LCD(self.i2c)
        self.row_pins = [Pin(p, Pin.OUT) for p in ROW_PINS]
        # **CRITICAL FIX**: Initialize column pins with internal pull-down resistors.
        self.col_pins = [Pin(p, Pin.IN, Pin.PULL_DOWN) for p in COL_PINS]
        
        # Game State
        self.target_number = 0
        self.upper_bound = 99
        self.lower_bound = 0
        self.current_guess_str = ""
        
        # Keypad State Management
        self.last_key_pressed = None
        self.last_key_time = 0
        self.debounce_delay_ms = 200 # Debounce delay to prevent multiple presses

    def reset_game(self):
        """Resets the game to a new round."""
        self.target_number = urandom.randint(0, 99)
        self.upper_bound = 99
        self.lower_bound = 0
        self.current_guess_str = ""
        print(f"New game started. Secret number is: {self.target_number}") # For debugging
        self.update_lcd_display("Guess the number!", f"{self.lower_bound} < ? < {self.upper_bound}")

    def scan_keypad(self):
        """
        Scans the keypad for a single key press.
        Returns the character of the pressed key or None.
        """
        for r, row_pin in enumerate(self.row_pins):
            row_pin.high()
            for c, col_pin in enumerate(self.col_pins):
                if col_pin.value() == 1:
                    row_pin.low() # Reset the row pin
                    return KEYPAD_LAYOUT[r][c]
            row_pin.low()
        return None

    def get_key_press(self):
        """
        Gets a single, debounced key press from the keypad.
        Returns the key character or None if no new key is pressed.
        """
        key = self.scan_keypad()
        current_time = time.ticks_ms()
        
        if key is not None:
            # Check if this key is different from the last one OR if enough time has passed
            if key != self.last_key_pressed or time.ticks_diff(current_time, self.last_key_time) > self.debounce_delay_ms:
                self.last_key_pressed = key
                self.last_key_time = current_time
                return key
        else:
            # If no key is pressed, reset the last key state
            self.last_key_pressed = None
            
        return None

    def process_guess(self):
        """Processes the player's guess and updates the game state."""
        if not self.current_guess_str:
            return # Do nothing if guess is empty

        guess = int(self.current_guess_str)
        
        if guess == self.target_number:
            self.update_lcd_display("You got it!", f"The number is   {self.target_number}")
            time.sleep(3) # Show success message
            self.reset_game()
        elif guess < self.target_number:
            self.lower_bound = max(self.lower_bound, guess)
            self.update_lcd_display(f"{guess} is too low", f"{self.lower_bound} < ? < {self.upper_bound}")
            self.current_guess_str = "" # Clear guess for next try
        else: # guess > self.target_number
            self.upper_bound = min(self.upper_bound, guess)
            self.update_lcd_display(f"{guess} is too high", f"{self.lower_bound} < ? < {self.upper_bound}")
            self.current_guess_str = "" # Clear guess for next try

    def update_lcd_display(self, line1, line2=""):
        """Clears and updates the LCD with two lines of text."""
        self.lcd.clear()
        self.lcd.message(f"{line1}\n{line2}")

    def handle_input(self, key):
        """Handles user input from the keypad."""
        if key.isdigit():
            # Append number to the guess string, with a limit of 2 digits
            if len(self.current_guess_str) < 2:
                self.current_guess_str += key
                self.update_lcd_display("Your guess:", self.current_guess_str)
        
        elif key == 'D': # 'D' is the confirm/enter key
            self.process_guess()
            
        elif key == 'A': # 'A' is the new game key
            self.reset_game()
        
        elif key == '#': # '#' can be used as a backspace/clear key
            self.current_guess_str = ""
            self.update_lcd_display("Guess cleared", "Enter new number")

    def run(self):
        """The main game loop."""
        self.update_lcd_display("Guess The Number", "Press 'A' to start")
        
        # Wait for 'A' to start the first game
        while self.get_key_press() != 'A':
            time.sleep_ms(50)
            
        self.reset_game()

        while True:
            key = self.get_key_press()
            if key:
                print(f"Key Pressed: {key}") # For debugging
                self.handle_input(key)
            
            # A small delay to keep the loop from running too fast
            time.sleep_ms(20)

def main():
    """Main entry point of the program."""
    try:
        game = GuessTheNumberGame()
        game.run()
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        # Attempt to clear LCD on error
        try:
            lcd = LCD(I2C(0, sda=Pin(20), scl=Pin(21)))
            lcd.clear()
            lcd.message("System Error.\nPlease Reboot.")
        except:
            pass # Ignore if LCD also fails
    finally:
        print("Shutting down.")

if __name__ == "__main__":
    main()