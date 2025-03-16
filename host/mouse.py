import pyautogui
import switch

class mouse:
    mouse = switch.switch('MOUSE')

    def __init__(self):
        self.mouse = switch.switch('MOUSE')

    def mouseDown(self):
        if not self.mouse.state:
            pyautogui.mouseDown()
            self.mouse.toggle()
            
    def mouseUp(self):
        if self.mouse.state:
            pyautogui.mouseUp()
            self.mouse.toggle()
