from typing import Tuple
import serial
import pyautogui
import re

DEBUG = True

# Connection Settings
serialPath = '/dev/ttyACM0'

# Mapping Settings
areaSize = (1852, 1235)
areaOffset = (0, 0)

# Client Settings
serialScreenSize = (800, 480)
serialMoveCommand = '(?:x0=)([0-9]+)(?: y0=)([0-9]+)'
serialMouseDownCommand = 'DOWN'
serialMouseUpCommand = 'UP'



def locationMapping(
    input: Tuple[int, int], 
    inputSize: Tuple[int, int], 
    outputSize: Tuple[int, int], 
    offset: Tuple[int, int] = (0, 0)
):
    return (
        (int(input[0] / inputSize[0] * outputSize[0]) + offset[0]), 
        (int(input[1] / inputSize[1] * outputSize[1]) + offset[1])
    )

def debugPrint(*values):
    if DEBUG:
        print(*values)

ignoreClick = True
mouse = False
location = ()
pyautogui.PAUSE = 0
with serial.Serial(serialPath, 115200) as tty:
    while True:
        line = tty.readline().decode().strip()
        if (location := re.findall(serialMoveCommand, line)):
            location = (int(location[0][0]), int(location[0][1]))
            location = locationMapping(location, serialScreenSize, areaSize, areaOffset)
            debugPrint(f'MOVE: {location}')
            pyautogui.moveTo(*location)
        elif (line == serialMouseDownCommand):
            if (not ignoreClick):
                debugPrint('MOUSE DOWN')
                if not mouse:
                    pyautogui.mouseDown()
                    mouse = True
            else:
                debugPrint('MOUSE DOWN: IGNORED')
        elif (line == serialMouseUpCommand):
            if (not ignoreClick):
                debugPrint('MOUSE UP')
                if mouse:
                    pyautogui.mouseUp()
                    mouse = False
            else:
                debugPrint('MOUSE UP: IGNORED')
        elif (line == 'SWITCH'):
            debugPrint(f'TOUCH: {ignoreClick}')
            ignoreClick = not ignoreClick
        else:
            debugPrint(f'UNKNOWN: {line}')
