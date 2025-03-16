from machine import Pin
from machine import FPIOA
import time


#Configure GPIO52、GPIO21 as a normal GPIO
fpioa = FPIOA()
fpioa.set_function(21,FPIOA.GPIO21)
KEY=Pin(21,Pin.IN,Pin.PULL_UP) #Construct KEY object
while True:

    if KEY.value()==0:   #Key pressed
        time.sleep_ms(10) #Eliminate jitter
        if KEY.value()==0: #Confirm key is pressed
            print('KEY')
            while not KEY.value(): #Detect whether the button is released
                pass
