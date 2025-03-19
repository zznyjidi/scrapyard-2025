from typing import Callable, List, Tuple
import serial
import pyautogui
import re

import random

import config
import switch, mouse, reverse
from mapping import locationMapping

from debug import debugPrint

enableClick = switch.switch('TOUCH')
mouseController = mouse.mouse()
location = ()
pyautogui.PAUSE = 0

# Location Processors
# (Parser Function, Enable/Disable)
locationParserList: List[Tuple[Callable[[Tuple[int, int]], Tuple[int, int]], bool]] = [
    (lambda location: locationMapping(
        location, 
        config.tabletAreaSize, config.screenAreaSize, 
        config.tabletAreaOffset, config.screenAreaOffset, 
        config.serialScreenSize
    ), True), 
    (reverse.reversePos, False)
]

random_total = 0

with serial.Serial(config.serialPath, 115200) as tty:
    while True:
        line = tty.readline().decode().strip()
        
        # Trolling: Random Jump
        if config.randomJump:
            random_total += random.randint(0, 10)
            if random_total > 300:
                random_total = 0
                index = random.randint(0, 1)
                locationParserList[index] = (locationParserList[index][0], not locationParserList[index][1])
                debugPrint(f'REVERSE/MAPPING: {locationParserList[index][1]}')
        
        # Moving Message
        if (location := re.findall(config.serialMoveCommand, line)):
            # Get Raw Pos
            location = (int(location[0][0]), int(location[0][1]))
            
            # Apply Pos Parser
            for process in locationParserList:
                if process[1]:
                    location = process[0](location)
            
            # Move Cursor
            debugPrint(f'MOVE: {location}')
            pyautogui.moveTo(*location)
        
        # Action Messages
        else:
            match (line):
                # Mouse Down
                case config.serialMouseDownCommand:
                    enableClick.runIfSwitchStatus(True, "MOUSE DOWN", mouseController.mouseDown)
                # Mouse Up
                case config.serialMouseUpCommand:
                    enableClick.runIfSwitchStatus(True, "MOUSE UP", mouseController.mouseUp)
                # Toggle Touch
                case config.serialButtonCommand:
                    enableClick.toggle()
                # Unknown Command
                case _:
                    debugPrint(f'UNKNOWN: {line}')
