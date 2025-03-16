from machine import Pin, FPIOA, TOUCH

# Init Touch
touch = TOUCH(0)

# Init Button
fpioa = FPIOA()
fpioa.set_function(21, FPIOA.GPIO21)
KEY = Pin(21, Pin.IN, Pin.PULL_UP)

firstTouch = False
buttonTriggered = False

while True:
    touchEvents = touch.read()
    if touchEvents:
        pos = (touchEvents[0].x, touchEvents[0].y)
        print(f'x0={pos[0]} y0={pos[1]}')
        if (not firstTouch):
            print('CLICK')
            firstTouch = True
    else:
        firstTouch = False
    if (KEY.value() == 0):
        if (not buttonTriggered):
            print('SWITCH')
            buttonTriggered = True
    else:
        buttonTriggered = False
