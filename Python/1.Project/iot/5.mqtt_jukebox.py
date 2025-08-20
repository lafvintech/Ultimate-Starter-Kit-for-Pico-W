"""
MQTT Music Player with Keyboard Control

This program connects to an MQTT broker and plays predefined melodies
based on received messages. It includes graceful exit functionality
using keyboard interrupt (Ctrl+C).

Hardware Requirements:
- ESP32/ESP8266 with MicroPython
- Buzzer connected to GPIO 15

Supported Songs:
- "nokia" - Nokia ringtone
- "starwars" - Star Wars theme
- "nevergonnagiveyouup" - Rick Astley
- "imperialmarch" - Imperial March (Darth Vader theme)

Usage:
- Send song name to MQTT topic 'LAFVIN MQTT'
- Use Ctrl+C to exit gracefully
"""

import time
import sys
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# Buzzer setup
from play_music import *
buzzer = PWM(Pin(15))
play_flag = False

# Wi-Fi connection
from secrets import *
from do_connect import *
do_connect()

# MQTT configuration
mqtt_server = 'broker.hivemq.com'
client_id = 'Jimmy'

# MQTT topic to subscribe for music commands
topic = b'LAFVIN MQTT'

# Global variables for resource management
client = None
running = True
melody = None

def cleanup_resources():
    """
    Clean up all resources including MQTT connection and buzzer
    """
    global client, buzzer
    print("\nCleaning up resources...")
    
    try:
        # Stop buzzer
        if buzzer:
            buzzer.duty_u16(0)  # Stop PWM output
            print("✓ Buzzer stopped")
    except Exception as e:
        print(f"Error cleaning buzzer: {e}")
    
    try:
        # Disconnect MQTT
        if client:
            client.disconnect()
            print("✓ MQTT connection closed")
    except Exception as e:
        print(f"Error disconnecting MQTT: {e}")
    
    print("✓ Resource cleanup completed")


def callback(topic, message):
    print("New message on topic {}".format(topic.decode('utf-8')))
    message = message.decode('utf-8')
    print(message)
    if message in song.keys():
        global melody,play_flag
        melody = song[message]
        play_flag = True


# Main program
def main():
    """
    Main program entry point with graceful exit handling
    """
    global client, running, play_flag, melody
    
    try:
        # Initialize MQTT client
        client = MQTTClient(client_id, mqtt_server, keepalive=60)
        client.set_callback(callback)
        client.connect()
        print(f'✓ Successfully connected to MQTT server: {mqtt_server}')
        print(f'✓ Client ID: {client_id}')
        print(f'✓ Subscribed topic: {topic.decode("utf-8")}')
        print("✓ Music player started - Press Ctrl+C to exit")
        print("-" * 50)
        
        # Main loop
        while running:
            try:
                client.subscribe(topic)
                client.check_msg()  # Check for new messages
                
                # Play music if requested
                if play_flag:
                    print(f"🎵 Starting music playback...")
                    play(buzzer, melody)
                    play_flag = False
                    print("🎵 Music playback completed")
                
                time.sleep(0.1)  # Reduce CPU usage
                
            except KeyboardInterrupt:
                # Catch Ctrl+C
                print("\nUser interrupt detected, shutting down...")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)  # Brief delay after error
                
    except OSError as e:
        print(f'❌ Failed to connect to MQTT server: {e}')
        print('Try restarting device or check network connection...')
        cleanup_resources()
        return
    except Exception as e:
        print(f'❌ Program initialization failed: {e}')
        cleanup_resources()
        return
    finally:
        # Ensure resources are cleaned up
        running = False
        cleanup_resources()

# Run main program
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Program terminated with exception: {e}")
        cleanup_resources()

