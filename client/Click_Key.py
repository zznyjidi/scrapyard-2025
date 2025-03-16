from maix import GPIO
from fpioa_manager import fm

fm.register(16, fm.fpioa.GPIO1)

KEY = GPIO(GPIO.GPIO1, GPIO.IN)

while True:

    if KEY.value()==0: #按键被按下接地
        print("Click")
    else:
        print("No_Click")
