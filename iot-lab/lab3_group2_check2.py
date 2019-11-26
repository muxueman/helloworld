from machine import RTC, Pin, I2C, SPI, ADC
from time import sleep
import ssd1306
rtc = RTC()
rtc.datetime((2019, 9, 25, 4, 16, 5, 0, 0))
rtc.datetime()
# init button
button_A = Pin(12, Pin.IN, Pin.PULL_UP)
button_B = Pin(13, Pin.IN)
button_C = Pin(14, Pin.IN, Pin.PULL_UP)
sensor = Pin(15, Pin.OUT)
sensor.value(1)
adc = ADC(0)
# counter indicates the current operate element in datetime
counter=0
# construct an I2C bus in LED
i2c = I2C(-1, Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
# write and show real time
def week(n_week):
    if(n_week==1): return 'Monday'
    elif(n_week==2): return 'Tuesday'
    elif(n_week==3): return 'Wednesday'
    elif(n_week==4): return 'Thursday'
    elif(n_week==5): return 'Friday'
    elif(n_week==6): return 'Saturday'
    elif(n_week==7): return 'Sunday'
    return 'Monday'
def show():
    oled.contrast(255-int(adc.read()/2))
    oled.fill(0)
    oled.text(str(rtc.datetime()[0]), 0, 0, 1)
    oled.text('/', 40, 0, 1)
    oled.text(str(rtc.datetime()[1]), 50, 0, 1)
    oled.text('/', 70, 0, 1)
    oled.text(str(rtc.datetime()[2]), 80, 0, 1)
    oled.text(week(rtc.datetime()[3]), 0, 10, 1)
    oled.text(str(rtc.datetime()[4]), 0, 20, 1)
    oled.text(':', 20, 20, 1)
    oled.text(str(rtc.datetime()[5]), 30, 20, 1)
    oled.text(':', 50, 20, 1)
    oled.text(str(rtc.datetime()[6]), 60, 20, 1)
    oled.show()
# check if there is an interrupt. if there is no interrupt, pause() == True, to be modified
def pause():
    return button_A.value() and button_B.value() and button_C.value()
def show_time():
    while (pause()):
        show()

show_time()
	