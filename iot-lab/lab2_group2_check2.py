from machine import Pin, PWM, ADC
from time import sleep
led = Pin(13, Pin.OUT)
button = Pin(12, Pin.IN, Pin.PULL_UP) 
led.value(0)
value=1
counter=0

def start(v):
    global value,counter
    sleep(0.1)
    counter+=1
    led.value(value)
    if (value == 1):
        value = 0
    else:
        value = 1
    print("IRQ ",counter," ", value)

button.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=start)

# rising is when you release