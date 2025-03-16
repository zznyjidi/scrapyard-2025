from machine import Pin, FPIOA, TOUCH

# Init Touch
touch = TOUCH(0)

# Init Button
fpioa = FPIOA()
fpioa.set_function(21, FPIOA.GPIO21)
KEY = Pin(21, Pin.IN, Pin.PULL_UP)

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
