# Part 1 without button
from machine import Pin, PWM, ADC
from time import sleep
led = Pin(13, Pin.OUT)
pwm_l = PWM(Pin(13))
motor = Pin(15, Pin.OUT)
pwm_m = PWM(Pin(15))
sensor = Pin(14, Pin.OUT)
adc = ADC(0)
sensor.value(1)

while True:
    adc.read()
    pwm_l.duty(2*adc.read())
    pwm_m.duty(2*adc.read())
    sleep(0.2)


# pwm_l.deinit()
# pwm_m.deinit()
# sensor.value(0)

