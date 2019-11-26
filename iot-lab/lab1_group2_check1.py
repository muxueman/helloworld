# Problem 1
from machine import Pin
from time import sleep

led = Pin(15,Pin.OUT)
while True:
     for i in range(0,3):
         led.on()
         sleep(1)
         led.off()
         sleep(0.3)
     for i in range(0,3):
         led.on()
         sleep(2)
         led.off()
         sleep(0.3)
     for i in range(0,3):
         led.on()
         sleep(1)
         led.off()
         sleep(0.3)
