#!/usr/bin/env python3
# -*- coding: utf8 -*-

# RFID Card Writer
# This script writes data to an RFID card using the MFRC522 module.
# Features input validation and user-friendly interface.

from mfrc522 import SimpleMFRC522

# --- Configuration Constants ---
# SPI pin configuration for Raspberry Pi Pico W
SPI_ID = 0
SCK_PIN = 18
MISO_PIN = 16
MOSI_PIN = 19
CS_PIN = 17
RST_PIN = 9

# Data constraints
MAX_DATA_LENGTH = 16  # Maximum characters that can be stored

def get_user_input():
    """
    Get and validate user input for the data to write.
    
    Returns:
        str: The validated data to write to the card
    """
    while True:
        user_data = input(f"💬 Enter message to write (max {MAX_DATA_LENGTH} chars): ").strip()
        
        if not user_data:
            print("❌ Empty input. Please enter some text.")
            continue
        
        if len(user_data) > MAX_DATA_LENGTH:
            print(f"⚠️  Input too long. Truncating to {MAX_DATA_LENGTH} characters.")
            user_data = user_data[:MAX_DATA_LENGTH]
        
        return user_data

def display_write_preview(data):
    """
    Display a preview of the data to be written.
    
    Args:
        data (str): The data that will be written
    """
    print("\n📦 Write Preview:")
    print("+" + "-" * 48 + "+")
    padding = ' ' * (40 - len(data))
    print(f"| Data: '{data}'{padding} |")
    print(f"| Length: {len(data)} characters{' ' * (32 - len(str(len(data))))} |")
    print("+" + "-" * 48 + "+")

def main():
    """
    Main function to handle the card writing process.
    """
    # Initialize the MFRC522 reader with pin configuration
    reader = SimpleMFRC522(spi_id=SPI_ID, sck=SCK_PIN, miso=MISO_PIN, 
                          mosi=MOSI_PIN, cs=CS_PIN, rst=RST_PIN)
    
    # Display program header
    print("=" * 50)
    print("    ✍️  RFID CARD WRITER ✍️")
    print("=" * 50)
    print("This program writes data to RFID cards.")
    print("Press Ctrl+C at any time to exit.")
    print("=" * 50)
    
    try:
        # Get user input
        data_to_write = get_user_input()
        
        # Display preview
        display_write_preview(data_to_write)
        
        # Confirm operation
        confirm = input("\n🤔 Proceed with writing? (y/N): ").lower().strip()
        if confirm not in ['y', 'yes']:
            print("❌ Write operation cancelled.")
            return
        
        # Wait for card and write data
        print("\n📡 Waiting for card...")
        print("📝 Please place an RFID card near the sensor.")
        
        # Write data to card
        card_id, written_text = reader.write(data_to_write)
        
        # Display success results
        print("\n✅ CARD DETECTED & WRITTEN!")
        print("+" + "-" * 48 + "+")
        print(f"| 🆔 Card ID:     {card_id:<31} |")
        
        # Display written content
        padding = ' ' * (29 - len(written_text))
        print(f"| 📄 Written:     '{written_text}'{padding} |")
        print("+" + "-" * 48 + "+")
        print("✅ Write operation completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during write operation: {e}")
        print("💡 Tip: Make sure the card is properly positioned.")
    finally:
        print("\n👋 Program terminated. Goodbye!")

if __name__ == '__main__':
    main()