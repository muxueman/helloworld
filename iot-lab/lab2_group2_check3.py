from machine import Pin, PWM, ADC
from time import sleep
led = Pin(13, Pin.OUT)
pwm_l = PWM(Pin(13))
motor = Pin(15, Pin.OUT)
pwm_m = PWM(Pin(15))
sensor = Pin(14, Pin.OUT)
sensor.value(1)
adc = ADC(0)
button = Pin(12, Pin.IN, Pin.PULL_UP) 

led.value(0)
value=1
counter=0

def start(v):
    global value,counter
    sleep(0.1)
    counter+=1
    print("IRQ ",counter," ", value)
    if (value == 1):
        value = 0
        while (button.value()==0):
            pwm_l.duty(2*adc.read())
            pwm_m.duty(2*adc.read())
            sleep(0.2)
    else:
        value = 1
        pwm_l.duty(0)
        pwm_m.duty(0)
    
button.irq(trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING, handler=start)
