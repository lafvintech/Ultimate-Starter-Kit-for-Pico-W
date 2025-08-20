"""
IR Remote Control Receiver (NEC protocol, MicroPython)

Refactor goals:
- English comments and organized output
- Replace magic numbers with named constants
- Clean, professional data formatting
"""

import time
from machine import Pin
from ir_rx.print_error import print_error
from ir_rx.nec import NEC_8


# =========================
# Constants
# =========================
IR_RECEIVER_PIN = 17

# NEC_8 sends repeat codes as negative "data" in callback
REPEAT_NOTICE = "(repeat)"  # informational note if needed

# Key map (8-bit command codes for typical NEC remote)
KEY_MAP = {
    0x52: "0",
    0x16: "1",
    0x19: "2",
    0x0D: "3",
    0x0C: "4",
    0x18: "5",
    0x5E: "6",
    0x08: "7",
    0x1C: "8",
    0x5A: "9",
    0x42: "*",
    0x4A: "#",
    0x46: "UP",
    0x15: "DOWN",
    0x40: "OK",
    0x44: "LEFT",
    0x43: "RIGHT",
}


def decode_ir_key(data: int) -> str:
    """Return key name or 'UNKNOWN' and print raw code for debugging when unknown."""
    name = KEY_MAP.get(data)
    if name is None:
        print("Unknown IR Code: 0x%X" % data)
        return "UNKNOWN"
    return name


def display_key_press(name: str, data: int) -> None:
    """Print formatted key info (Arduino-like)."""
    print("Key: %s | Code: 0x%X" % (name, data))


def on_ir(data: int, addr: int, ctrl: int) -> None:
    """NEC_8 callback: handle key decode, ignore repeats (negative data)."""
    if data < 0:
        # Repeat code: key held down. Ignore to match Arduino behavior.
        return

    name = decode_ir_key(data)
    if name != "UNKNOWN":
        display_key_press(name, data)


def main() -> None:
    pin_ir = Pin(IR_RECEIVER_PIN, Pin.IN)
    ir = NEC_8(pin_ir, on_ir)
    ir.error_function(print_error)

    print("IR Remote Control Receiver Started")
    print("Press any key on the remote control...")
    print("================================")

    try:
        while True:
            time.sleep(0.1)  # avoid busy-waiting
    except KeyboardInterrupt:
        ir.close()


if __name__ == "__main__":
    main()
