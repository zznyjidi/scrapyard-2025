from typing import Tuple
import serial
import pyautogui
import re

DEBUG = False

# Connection Settings
serialPath = '/dev/ttyACM0'

# Mapping Settings
areaSize = (1920, 1080)
areaOffset = (0, 0)

# Client Settings
serialScreenSize = (800, 480)
serialMoveCommand = '(?:x0=)([0-9]+)(?: y0=)([0-9]+)'
serialClickCommand = 'CLICK'



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
with serial.Serial(serialPath) as tty:
    while True:
        line = tty.readline().decode().strip()
        if (location := re.findall(serialMoveCommand, line)):
            location = (int(location[0][0]), int(location[0][1]))
            debugPrint(f'MOVE: {location}')
            location = locationMapping(location, serialScreenSize, areaSize, areaOffset)
            pyautogui.moveTo(location[0], location[1], 0)
        elif (line == serialClickCommand):
            if (not ignoreClick):
                debugPrint('CLICK')
                pyautogui.click()
            else:
                debugPrint('CLICK: IGNORED')
        elif (line == 'SWITCH'):
            debugPrint(f'TOUCH: {ignoreClick}')
            ignoreClick = not ignoreClick
        else:
            debugPrint(f'UNKNOWN: {line}')
