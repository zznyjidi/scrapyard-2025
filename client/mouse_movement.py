#!/usr/bin/env python3
import serial
import uinput
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 115200

# Create a virtual mouse device supporting relative X and Y movement.
device = uinput.Device([
    uinput.REL_X,
    uinput.REL_Y,
])

# Open the serial port with a shorter timeout.
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.5)

print("Listening for touch events on", SERIAL_PORT)

prev_x = None
prev_y = None

# Scaling factor to amplify the movement.
SCALE = 2  # Increase this number to amplify movement if needed.

def parse_coordinates(line):
    """
    Parse a line containing coordinates in the format "x0=405 y0=212".
    Returns (cur_x, cur_y) as integers, or (None, None) on failure.
    """
    cur_x = None
    cur_y = None
    parts = line.split()
    for part in parts:
        if part.startswith("x0="):
            try:
                cur_x = int(part[3:])
            except ValueError:
                pass
        elif part.startswith("y0="):
            try:
                cur_y = int(part[3:])
            except ValueError:
                pass
    return cur_x, cur_y

while True:
    try:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue  # Skip empty lines.
            print("Received:", line)
            # Check if the line contains coordinate info.
            if "x0=" in line and "y0=" in line:
                cur_x, cur_y = parse_coordinates(line)
                if cur_x is None or cur_y is None:
                    continue
                if prev_x is not None and prev_y is not None:
                    dx = (cur_x - prev_x) * SCALE
                    dy = (cur_y - prev_y) * SCALE
                    # Debug print the computed movement.
                    print("Moving: dx =", dx, "dy =", dy)
                    # Emit relative movement events:
                    # Use syn=False on the first emit and syn=True on the second to combine them.
                    device.emit(uinput.REL_X, dx, syn=False)
                    device.emit(uinput.REL_Y, -dy, syn=True)
                prev_x = cur_x
                prev_y = cur_y
    except Exception as e:
        print("Error:", e)
        time.sleep(0.5)
