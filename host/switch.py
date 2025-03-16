from typing import Callable
import debug

class switch:
    state = False
    name = ''
    
    def __init__(self, name: str):
        self.state = False
        self.name = name
    
    def toggle(self):
        self.state = not self.state
        debug.debugPrint(f'{self.name}: {self.state}')
    
    def runIfSwitchStatus(self, target_status: bool, log_message: str, func: Callable):
        if self.state == target_status:
            debug.debugPrint(log_message)
            func()
        else:
            debug.debugPrint(f'{log_message}: IGNORED')
