from typing import Tuple
import serial
import pyautogui
import re

serialPath = '/dev/ttyACM0'

areaSize = (1920, 1080)
areaOffset = (0, 0)

ignoreClick = True

serialScreenSize = (320, 240)
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

with serial.Serial(serialPath) as tty:
    while True:
        line = tty.readline().decode().strip()
        if (location := re.findall(serialMoveCommand, line)):
            location = (int(location[0][0]), int(location[0][1]))
            print(f'MOVE: {location}')
            location = locationMapping(location, serialScreenSize, areaSize, areaOffset)
            pyautogui.moveTo(location[0], location[1], 0)
        elif (line == serialClickCommand and not ignoreClick):
            print('CLICK')
            pyautogui.click()
        elif (line == 'SWITCH'):
            print(f'TOUCH: {not ignoreClick}')
            ignoreClick = not ignoreClick
        else:
            print(f'UNKNOWN: {line}')
