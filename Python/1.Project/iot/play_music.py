"""Music Player Module

This module provides musical note definitions and playback functionality.
Thanks to Robson Couto for open-sourced scores.
GitHub: https://github.com/robsoncouto/arduino-songs
"""

import time
import machine

# Musical note frequency definitions (Hz)
NOTE_B0 =  31
NOTE_C1 =  33
NOTE_CS1 = 35
NOTE_D1 =  37
NOTE_DS1 = 39
NOTE_E1 =  41
NOTE_F1 =  44
NOTE_FS1 = 46
NOTE_G1 =  49
NOTE_GS1 = 52
NOTE_A1 =  55
NOTE_AS1 = 58
NOTE_B1 =  62
NOTE_C2 =  65
NOTE_CS2 = 69
NOTE_D2 =  73
NOTE_DS2 = 78
NOTE_E2 =  82
NOTE_F2 =  87
NOTE_FS2 = 93
NOTE_G2 =  98
NOTE_GS2 = 104
NOTE_A2 =  110
NOTE_AS2 = 117
NOTE_B2 =  123
NOTE_C3 =  131
NOTE_CS3 = 139
NOTE_D3 =  147
NOTE_DS3 = 156
NOTE_E3 =  165
NOTE_F3 =  175
NOTE_FS3 = 185
NOTE_G3 =  196
NOTE_GS3 = 208
NOTE_A3 =  220
NOTE_AS3 = 233
NOTE_B3 =  247
NOTE_C4 =  262
NOTE_CS4 = 277
NOTE_D4 =  294
NOTE_DS4 = 311
NOTE_E4 =  330
NOTE_F4 =  349
NOTE_FS4 = 370
NOTE_G4 =  392
NOTE_GS4 = 415
NOTE_A4 =  440
NOTE_AS4 = 466
NOTE_B4 =  494
NOTE_C5 =  523
NOTE_CS5 = 554
NOTE_D5 =  587
NOTE_DS5 = 622
NOTE_E5 =  659
NOTE_F5 =  698
NOTE_FS5 = 740
NOTE_G5 =  784
NOTE_GS5 = 831
NOTE_A5 =  880
NOTE_AS5 = 932
NOTE_B5 =  988
NOTE_C6 =  1047
NOTE_CS6 = 1109
NOTE_D6 =  1175
NOTE_DS6 = 1245
NOTE_E6 =  1319
NOTE_F6 =  1397
NOTE_FS6 = 1480
NOTE_G6 =  1568
NOTE_GS6 = 1661
NOTE_A6 =  1760
NOTE_AS6 = 1865
NOTE_B6 =  1976
NOTE_C7 =  2093
NOTE_CS7 = 2217
NOTE_D7 =  2349
NOTE_DS7 = 2489
NOTE_E7 =  2637
NOTE_F7 =  2794
NOTE_FS7 = 2960
NOTE_G7 =  3136
NOTE_GS7 = 3322
NOTE_A7 =  3520
NOTE_AS7 = 3729
NOTE_B7 =  3951
NOTE_C8 =  4186
NOTE_CS8 = 4435
NOTE_D8 =  4699
NOTE_DS8 = 4978
REST = 0  # Rest/silence note

# Musical timing constants
DEFAULT_TEMPO = 220              # Default playback tempo (BPM)
NOTE_PLAY_RATIO = 0.9            # Percentage of note duration to play (90%)
PWM_DUTY_CYCLE = 30000           # PWM duty cycle for audio output
SILENCE_DURATION = 100           # Default silence duration in ms

# Note duration guide:
# - Positive numbers: 4=quarter, 8=eighth, 16=sixteenth note
# - Negative numbers: dotted notes (e.g., -4 = dotted quarter note)
song = {
    "nokia":[NOTE_E5, 8, NOTE_D5, 8, NOTE_FS4, 4, NOTE_GS4, 4, NOTE_CS5, 8, NOTE_B4, 8, NOTE_D4, 4, 
                NOTE_E4, 4,NOTE_B4, 8, NOTE_A4, 8, NOTE_CS4, 4, NOTE_E4, 4, NOTE_A4, 2],
    "starwars":[NOTE_AS4,8, NOTE_AS4,8, NOTE_AS4,8,
                    NOTE_F5,2, NOTE_C6,2,
                    NOTE_AS5,8, NOTE_A5,8, NOTE_G5,8, NOTE_F6,2, NOTE_C6,4,  
                    NOTE_AS5,8, NOTE_A5,8, NOTE_G5,8, NOTE_F6,2, NOTE_C6,4,  
                    NOTE_AS5,8, NOTE_A5,8, NOTE_AS5,8, NOTE_G5,2, NOTE_C5,8, 
                    NOTE_C5,8, NOTE_C5,8,NOTE_F5,2, NOTE_C6,2,
                    NOTE_AS5,8, NOTE_A5,8, NOTE_G5,8, NOTE_F6,2, NOTE_C6,4,  
                    
                    NOTE_AS5,8, NOTE_A5,8, NOTE_G5,8, NOTE_F6,2, NOTE_C6,4, 
                    NOTE_AS5,8, NOTE_A5,8, NOTE_AS5,8, NOTE_G5,2, NOTE_C5,-8, NOTE_C5,16, 
                    NOTE_D5,-4, NOTE_D5,8, NOTE_AS5,8, NOTE_A5,8, NOTE_G5,8, NOTE_F5,8,
                    NOTE_F5,8, NOTE_G5,8, NOTE_A5,8, NOTE_G5,4, NOTE_D5,8, NOTE_E5,4,NOTE_C5,-8, NOTE_C5,16,
                    NOTE_D5,-4, NOTE_D5,8, NOTE_AS5,8, NOTE_A5,8, NOTE_G5,8, NOTE_F5,8,
                    
                    NOTE_C6,-8, NOTE_G5,16, NOTE_G5,2, REST,8, NOTE_C5,8,
                    NOTE_D5,-4, NOTE_D5,8, NOTE_AS5,8, NOTE_A5,8, NOTE_G5,8, NOTE_F5,8,
                    NOTE_F5,8, NOTE_G5,8, NOTE_A5,8, NOTE_G5,4, NOTE_D5,8, NOTE_E5,4,NOTE_C6,-8, NOTE_C6,16,
                    NOTE_F6,4, NOTE_DS6,8, NOTE_CS6,4, NOTE_C6,8, NOTE_AS5,4, NOTE_GS5,8, NOTE_G5,4, NOTE_F5,8,
                    NOTE_C6,1],
    "nevergonnagiveyouup":[NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,4, 
                            NOTE_E5,-4, NOTE_FS5,-4, NOTE_A5,16, NOTE_G5,16, NOTE_FS5,8,
                            NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,2,
                            NOTE_A4,16, NOTE_A4,16, NOTE_B4,16, NOTE_D5,8, NOTE_D5,16,
                            NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,4,  
                            NOTE_E5,-4, NOTE_FS5,-4, NOTE_A5,16, NOTE_G5,16, NOTE_FS5,8,
                            NOTE_D5,-4, NOTE_E5,-4, NOTE_A4,2,
                            NOTE_A4,16, NOTE_A4,16, NOTE_B4,16, NOTE_D5,8, NOTE_D5,16,
                            REST,4, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_D5,8, NOTE_E5,8, NOTE_CS5,-8,
                            NOTE_B4,16, NOTE_A4,2, REST,4, 

                            REST,8, NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,4, NOTE_A4,8, 
                            NOTE_A5,8, REST,8, NOTE_A5,8, NOTE_E5,-4, REST,4, 
                            NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, NOTE_D5,8, NOTE_E5,8, REST,8,
                            REST,8, NOTE_CS5,8, NOTE_B4,8, NOTE_A4,-4, REST,4,
                            REST,8, NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, NOTE_A4,4,
                            NOTE_E5,8, NOTE_E5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,4, REST,4,
                            
                            NOTE_D5,2, NOTE_E5,8, NOTE_FS5,8, NOTE_D5,8, 
                            NOTE_E5,8, NOTE_E5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,4, NOTE_A4,4,
                            REST,2, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8,
                            REST,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,-4, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,

                            NOTE_E5,-8, NOTE_E5,-8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,-8, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16, 
                            NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,8, NOTE_A4,8, NOTE_A4,8, 
                            NOTE_E5,4, NOTE_D5,2, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_A5,4, NOTE_CS5,8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,8, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,

                            NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,4, NOTE_A4,8,  
                            NOTE_E5,4, NOTE_D5,2, REST,4,
                            REST,8, NOTE_B4,8, NOTE_D5,8, NOTE_B4,8, NOTE_D5,8, NOTE_E5,4, REST,8,
                            REST,8, NOTE_CS5,8, NOTE_B4,8, NOTE_A4,-4, REST,4,
                            REST,8, NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, NOTE_A4,4,
                            REST,8, NOTE_A5,8, NOTE_A5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,8, NOTE_D5,8,
                            
                            REST,8, NOTE_A4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, 
                            REST,8, NOTE_CS5,8, NOTE_B4,8, NOTE_A4,-4, REST,4,
                            NOTE_B4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, NOTE_A4,4, REST,8,
                            REST,8, NOTE_E5,8, NOTE_E5,8, NOTE_FS5,4, NOTE_E5,-4, 
                            NOTE_D5,2, NOTE_D5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,4, 
                            NOTE_E5,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,8, NOTE_A4,8, NOTE_A4,4,

                            REST,-4, NOTE_A4,8, NOTE_B4,8, NOTE_CS5,8, NOTE_D5,8, NOTE_B4,8, 
                            REST,8, NOTE_E5,8, NOTE_FS5,8, NOTE_E5,-4, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_E5,-8, NOTE_E5,-8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,8, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,4, NOTE_A4,8, 

                            NOTE_E5,4, NOTE_D5,2, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16, 
                            NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_A5,4, NOTE_CS5,8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,8, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,4, NOTE_A4,8,  
                            NOTE_E5,4, NOTE_D5,2, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            
                            NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16, 
                            NOTE_A5,4, NOTE_CS5,8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,8, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,4, NOTE_A4,8,  
                            NOTE_E5,4, NOTE_D5,2, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_FS5,-8, NOTE_FS5,-8, NOTE_E5,-4, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16, 
                            
                            NOTE_A5,4, NOTE_CS5,8, NOTE_D5,-8, NOTE_CS5,16, NOTE_B4,8, NOTE_A4,16, NOTE_B4,16, NOTE_D5,16, NOTE_B4,16,
                            NOTE_D5,4, NOTE_E5,8, NOTE_CS5,-8, NOTE_B4,16, NOTE_A4,4, NOTE_A4,8, 

                            NOTE_E5,4, NOTE_D5,2, REST,4],
    "imperialmarch":[
        # Imperial March - Star Wars (Darth Vader Theme)
        # 原始Arduino代码来源: https://github.com/robsoncouto/arduino-songs
        # Score: https://musescore.com/user/202909/scores/1141521
        NOTE_A4,-4, NOTE_A4,-4, NOTE_A4,16, NOTE_A4,16, NOTE_A4,16, NOTE_A4,16, NOTE_F4,8, REST,8,
        NOTE_A4,-4, NOTE_A4,-4, NOTE_A4,16, NOTE_A4,16, NOTE_A4,16, NOTE_A4,16, NOTE_F4,8, REST,8,
        NOTE_A4,4, NOTE_A4,4, NOTE_A4,4, NOTE_F4,-8, NOTE_C5,16,
        
        NOTE_A4,4, NOTE_F4,-8, NOTE_C5,16, NOTE_A4,2,
        NOTE_E5,4, NOTE_E5,4, NOTE_E5,4, NOTE_F5,-8, NOTE_C5,16,
        NOTE_A4,4, NOTE_F4,-8, NOTE_C5,16, NOTE_A4,2,
        
        NOTE_A5,4, NOTE_A4,-8, NOTE_A4,16, NOTE_A5,4, NOTE_GS5,-8, NOTE_G5,16,
        NOTE_DS5,16, NOTE_D5,16, NOTE_DS5,8, REST,8, NOTE_A4,8, NOTE_DS5,4, NOTE_D5,-8, NOTE_CS5,16,
        
        NOTE_C5,16, NOTE_B4,16, NOTE_C5,16, REST,8, NOTE_F4,8, NOTE_GS4,4, NOTE_F4,-8, NOTE_A4,-16,
        NOTE_C5,4, NOTE_A4,-8, NOTE_C5,16, NOTE_E5,2,
        
        NOTE_A5,4, NOTE_A4,-8, NOTE_A4,16, NOTE_A5,4, NOTE_GS5,-8, NOTE_G5,16,
        NOTE_DS5,16, NOTE_D5,16, NOTE_DS5,8, REST,8, NOTE_A4,8, NOTE_DS5,4, NOTE_D5,-8, NOTE_CS5,16,
        
        NOTE_C5,16, NOTE_B4,16, NOTE_C5,16, REST,8, NOTE_F4,8, NOTE_GS4,4, NOTE_F4,-8, NOTE_A4,-16,
        NOTE_A4,4, NOTE_F4,-8, NOTE_C5,16, NOTE_A4,2
    ],
}


# Global tempo setting - modify to change playback speed
tempo = DEFAULT_TEMPO

# Calculate whole note duration in milliseconds based on tempo
wholenote = (60000 * 4) / tempo

def tone(pin, frequency, duration):
    """
    Generate a tone on the specified pin
    
    Args:
        pin: PWM pin object for audio output
        frequency: Tone frequency in Hz (0 for silence)
        duration: Duration in milliseconds
    """
    if frequency == 0:
        # Silence - no frequency output
        pass
    else:
        # Generate tone with specified frequency
        pin.freq(frequency)
        pin.duty_u16(PWM_DUTY_CYCLE)
    
    time.sleep_ms(duration)
    pin.duty_u16(0)  # Stop audio output

def noTone(pin):
    """
    Stop audio output on the specified pin
    
    Args:
        pin: PWM pin object to silence
    """
    tone(pin, 0, SILENCE_DURATION)

def play(pin, melody):
    """
    Play a melody on the specified PWM pin
    
    Args:
        pin: PWM pin object for audio output
        melody: List containing alternating notes and durations
    """
    print(f"Playing melody with {len(melody)//2} notes")
    
    # Process melody data (notes and durations are alternating)
    for note_index in range(0, len(melody), 2):
        note_frequency = melody[note_index]
        duration_divider = melody[note_index + 1]
        
        # Calculate note duration based on tempo
        if duration_divider > 0:
            # Regular note duration
            note_duration = wholenote / duration_divider
        elif duration_divider < 0:
            # Dotted note duration (1.5x longer)
            note_duration = wholenote / abs(duration_divider)
            note_duration *= 1.5
        else:
            # Invalid duration, skip this note
            continue
            
        # Play note for specified percentage of duration
        play_duration = int(note_duration * NOTE_PLAY_RATIO)
        tone(pin, note_frequency, play_duration)
        
        # Wait for full note duration before next note
        time.sleep_ms(int(note_duration))
        
        # Ensure clean audio output between notes
        noTone(pin)
    
    print("Melody playback completed")
    

# Demo/test code - runs when file is executed directly
if __name__ == '__main__':
    # Initialize PWM pin for audio output
    BUZZER_PIN = 15
    buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
    
    # Select and play a demo song
    demo_song = song["imperialmarch"]
    print(f"Starting Imperial March demo on pin {BUZZER_PIN}")
    play(buzzer, demo_song)
