#!/usr/bin/env python3
import serial
import uinput
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUDRATE = 115200

device = uinput.Device([
    uinput.BTN_LEFT,
    uinput.REL_X,
    uinput.REL_Y,
])

ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=2)

print("Listening for touch events on", SERIAL_PORT)

def simulate_click():
    device.emit(uinput.BTN_LEFT, 1)
    time.sleep(0.1)
    device.emit(uinput.BTN_LEFT, 0)
    print("Simulated mouse click.")

while True:
    try:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue 
            print("Received:", line)
            if "CLICK" in line:
                simulate_click()
    except serial.serialutil.SerialException as e:
        print("Serial error:", e)
        time.sleep(1)  
    except Exception as e:
        print("Other error:", e)
        time.sleep(1)
