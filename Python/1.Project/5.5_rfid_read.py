#!/usr/bin/env python3
# -*- coding: utf8 -*-

# RFID Card Reader
# This script reads data from an RFID card using the MFRC522 module.
# Features a user-friendly interface inspired by professional implementations.

from mfrc522 import SimpleMFRC522

# --- Configuration Constants ---
# SPI pin configuration for Raspberry Pi Pico W
SPI_ID = 0
SCK_PIN = 18
MISO_PIN = 16
MOSI_PIN = 19
CS_PIN = 17
RST_PIN = 9

def main():
    """
    Main function to handle the card reading process.
    """
    # Initialize the MFRC522 reader with pin configuration
    reader = SimpleMFRC522(spi_id=SPI_ID, sck=SCK_PIN, miso=MISO_PIN, 
                          mosi=MOSI_PIN, cs=CS_PIN, rst=RST_PIN)
    
    # Display program header
    print("=" * 50)
    print("    📖 RFID CARD READER 📖")
    print("=" * 50)
    print("This program reads data from RFID cards.")
    print("=" * 50)
    
    try:
        # Wait for card and read data
        print("\n🔍 Reading mode active...")
        print("📡 Please place an RFID card near the sensor.")
        
        # Read card data
        card_id, text_data = reader.read()
        
        # Display results in a formatted table
        print("\n✅ CARD DETECTED!")
        print("+" + "-" * 48 + "+")
        print(f"| 🆔 Card ID:    {card_id:<32} |")
        
        # Process and display the text data
        if text_data and text_data.strip():
            clean_text = text_data.strip()
            padding = ' ' * (30 - len(clean_text))
            print(f"| 📄 Content:   '{clean_text}'{padding} |")
        else:
            print(f"| 📄 Content:   Empty or uninitialized{' ' * 12} |")
        
        print("+" + "-" * 48 + "+")
        print("✅ Read operation completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during read operation: {e}")
    finally:
        print("\n👋 Program terminated. Goodbye!")

if __name__ == '__main__':
    main()