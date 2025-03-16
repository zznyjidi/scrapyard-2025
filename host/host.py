from typing import Tuple
import serial
import pyautogui
import re

import config
import switch, mouse
from mapping import locationMapping

from debug import debugPrint

enableClick = switch.switch('TOUCH')
mouseController = mouse.mouse()
location = ()
pyautogui.PAUSE = 0

with serial.Serial(config.serialPath, 115200) as tty:
    while True:
        line = tty.readline().decode().strip()
        if (location := re.findall(config.serialMoveCommand, line)):
            location = (int(location[0][0]), int(location[0][1]))
            location = locationMapping(location, config.serialScreenSize, config.areaSize, config.areaOffset)
            debugPrint(f'MOVE: {location}')
            pyautogui.moveTo(*location)
        else:
            match (line):
                case config.serialMouseDownCommand:
                    enableClick.runIfSwitchStatus(False, "MOUSE DOWN", mouseController.mouseDown)
                case config.serialMouseUpCommand:
                    enableClick.runIfSwitchStatus(False, "MOUSE UP", mouseController.mouseUp)
                case config.serialButtonCommand:
                    enableClick.toggle()
                case _:
                    debugPrint(f'UNKNOWN: {line}')
