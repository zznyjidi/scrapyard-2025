from machine import TOUCH
import time

# Instantiate the TOUCH device (device 0)
tp = TOUCH(0)

while True:
    p = tp.read()
    if p != ():  # Touch event occurred
        # For each touch point (for debugging, print coordinates)
        for i in range(len(p)):
            print('x{}={}'.format(i, p[i].x), 'y{}={}'.format(i, p[i].y))
        # Send a simple token to indicate a click event.
        print("CLICK")
    time.sleep_ms(50)
