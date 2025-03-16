#from typing import Callable, List
from machine import Pin, FPIOA, TOUCH # type: ignore
import time
import _thread

# Init Touch
touch = TOUCH(0)

# Init Button
fpioa = FPIOA()
fpioa.set_function(21, FPIOA.GPIO21)
KEY = Pin(21, Pin.IN, Pin.PULL_UP)

threadLockPool = []

def waitForAllLocks():
    global threadLockPool
    while any(map(lambda lock: not lock.locked(), threadLockPool)):
        pass
    for lock in threadLockPool:
        lock.acquire()
        lock.release()

def withLock(func):
    global threadLockPool
    lock: _thread.LockType = _thread.allocate_lock()
    threadLockPool.append(lock)
    
    def wrapper(*args, **kwargs):
        lock.acquire()
        try:
            func(*args, **kwargs)
        finally:
            lock.release()
    return wrapper

@withLock
def touchThread():
    firstTouch = False
    upSent = False
    emptyTouchCount = 0
    buttonTriggered = False
    
    while True:
        touchEvents = touch.read()
        if touchEvents:
            emptyTouchCount = 0
            upSent = False
            pos = (touchEvents[0].x, touchEvents[0].y)
            print(f'x0={pos[0]} y0={pos[1]}')
            if (not firstTouch):
                print('DOWN')
                firstTouch = True
        else:
            emptyTouchCount += 1
            if emptyTouchCount > 10:
                if not upSent:
                    print('UP')
                    upSent = True
                firstTouch = False
                emptyTouchCount = 0
        if (KEY.value() == 0):
            if (not buttonTriggered):
                print('SWITCH')
                buttonTriggered = True
        else:
            buttonTriggered = False

_thread.start_new_thread(touchThread, ())

waitForAllLocks()
