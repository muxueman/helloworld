# Problem 2
from machine import Pin
from time import sleep

led0 = Pin(0, Pin.OUT) # RED_LED
led1 = Pin(2, Pin.OUT) # BLUE_LED

while True:
    led0.off()  
    led1.off()
    sleep(0.1)
    led1.on()
    sleep(0.1)
    led1.off()
    sleep(0.1)
    led1.on()
    sleep(0.1)
    led0.on()
    sleep(0.1)
    led1.off()
    sleep(0.1)
    led1.on()
    sleep(0.1)
    led1.off()
    sleep(0.1)
    led1.on()
    sleep(0.1)
    led1.off()
    sleep(0.1)
    led1.on()
    sleep(0.1)
