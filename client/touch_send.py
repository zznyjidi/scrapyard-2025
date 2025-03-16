#from machine import TOUCH
from machine import I2C
import touchscreen as tp
import time
from maix import GPIO
from fpioa_manager import fm

# Instantiate the TOUCH device (device 0)
i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
tp.init(i2c)

# Init Button
fm.register(16, fm.fpioa.GPIO1)

KEY = GPIO(GPIO.GPIO1, GPIO.IN)

lastPos = ()

while True:
    touchEvent = tp.read()
    if touchEvent != lastPos:
        lastPos = touchEvent
        print(f'x0={touchEvent[1]} y0={touchEvent[2]}')
        if (lastPos[0] == tp.STATUS_PRESS):
            print('CLICK')
        if (KEY.value() == 0):
            print('SWITCH')
