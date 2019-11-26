#1. 测试button 和 pause() 2.是否可以正确跳出循环
from machine import RTC, Pin, I2C, SPI
from time import sleep
import ssd1306
rtc = RTC()
rtc.datetime((2019, 9, 25, 4, 16, 5, 0, 0))
rtc.datetime()
# init button
button_A = Pin(12, Pin.IN, Pin.PULL_UP)
button_B = Pin(13, Pin.IN)
button_C = Pin(14, Pin.IN, Pin.PULL_UP)
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
# curent operate element blink within 5 seconds
def blink():
    global counter
    # set time for customer
    def t_blink():
        return time_blink<4
    time_blink = 0
    if(counter==0):
        while (pause() and t_blink()):
            oled.fill(0)
            oled.text(str(rtc.datetime()[0]), 0, 0, 0)
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
            sleep(0.5)
            show()
            sleep(0.5)
            time_blink += 1
    elif(counter==1):
        while (pause() and t_blink()):
            oled.fill(0)
            oled.text(str(rtc.datetime()[0]), 0, 0, 1)
            oled.text('/', 40, 0, 1)
            oled.text(str(rtc.datetime()[1]), 50, 0, 0)
            oled.text('/', 70, 0, 1)
            oled.text(str(rtc.datetime()[2]), 80, 0, 1)
            oled.text(week(rtc.datetime()[3]), 0, 10, 1)
            oled.text(str(rtc.datetime()[4]), 0, 20, 1)
            oled.text(':', 20, 20, 1)
            oled.text(str(rtc.datetime()[5]), 30, 20, 1)
            oled.text(':', 50, 20, 1)
            oled.text(str(rtc.datetime()[6]), 60, 20, 1)
            oled.show()
            sleep(0.5)
            show()
            sleep(0.5)
            time_blink += 1
    elif(counter==2):
        while (pause() and t_blink()):
            oled.fill(0)
            oled.text(str(rtc.datetime()[0]), 0, 0, 1)
            oled.text('/', 40, 0, 1)
            oled.text(str(rtc.datetime()[1]), 50, 0, 1)
            oled.text('/', 70, 0, 1)
            oled.text(str(rtc.datetime()[2]), 80, 0, 0)
            oled.text(week(rtc.datetime()[3]), 0, 10, 1)
            oled.text(str(rtc.datetime()[4]), 0, 20, 1)
            oled.text(':', 20, 20, 1)
            oled.text(str(rtc.datetime()[5]), 30, 20, 1)
            oled.text(':', 50, 20, 1)
            oled.text(str(rtc.datetime()[6]), 60, 20, 1)
            oled.show()
            sleep(0.5)
            show()
            sleep(0.5)
            time_blink += 1
    elif(counter==3):
        while (pause() and t_blink()):
            oled.fill(0)
            oled.text(str(rtc.datetime()[0]), 0, 0, 1)
            oled.text('/', 40, 0, 1)
            oled.text(str(rtc.datetime()[1]), 50, 0, 1)
            oled.text('/', 70, 0, 1)
            oled.text(str(rtc.datetime()[2]), 80, 0, 1)
            oled.text(week(rtc.datetime()[3]), 0, 10, 0)
            oled.text(str(rtc.datetime()[4]), 0, 20, 1)
            oled.text(':', 20, 20, 1)
            oled.text(str(rtc.datetime()[5]), 30, 20, 1)
            oled.text(':', 50, 20, 1)
            oled.text(str(rtc.datetime()[6]), 60, 20, 1)
            oled.show()
            sleep(0.5)
            show()
            sleep(0.5)
            time_blink += 1
    elif(counter==4):
        while (pause() and t_blink()):
            oled.fill(0)
            oled.text(str(rtc.datetime()[0]), 0, 0, 1)
            oled.text('/', 40, 0, 1)
            oled.text(str(rtc.datetime()[1]), 50, 0, 1)
            oled.text('/', 70, 0, 1)
            oled.text(str(rtc.datetime()[2]), 80, 0, 1)
            oled.text(week(rtc.datetime()[3]), 0, 10, 1)
            oled.text(str(rtc.datetime()[4]), 0, 20, 0)
            oled.text(':', 20, 20, 1)
            oled.text(str(rtc.datetime()[5]), 30, 20, 1)
            oled.text(':', 50, 20, 1)
            oled.text(str(rtc.datetime()[6]), 60, 20, 1)
            oled.show()
            sleep(0.5)
            show()
            sleep(0.5)
            time_blink += 1
    elif(counter==5):
        while (pause() and t_blink()):
            oled.fill(0)
            oled.text(str(rtc.datetime()[0]), 0, 0, 1)
            oled.text('/', 40, 0, 1)
            oled.text(str(rtc.datetime()[1]), 50, 0, 1)
            oled.text('/', 70, 0, 1)
            oled.text(str(rtc.datetime()[2]), 80, 0, 1)
            oled.text(week(rtc.datetime()[3]), 0, 10, 1)
            oled.text(str(rtc.datetime()[4]), 0, 20, 1)
            oled.text(':', 20, 20, 1)
            oled.text(str(rtc.datetime()[5]), 30, 20, 0)
            oled.text(':', 50, 20, 1)
            oled.text(str(rtc.datetime()[6]), 60, 20, 1)
            oled.show()
            sleep(0.5)
            show()
            sleep(0.5)
            time_blink += 1
    elif(counter==6):
        while (pause() and t_blink()):
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
            oled.text(str(rtc.datetime()[6]), 60, 20, 0)
            oled.show()
            sleep(0.5)
            show()
            sleep(0.5)
            time_blink += 1
    show_time()
# set time
def set_time(adjust):
    global counter
    year, month, date, week, hour, minute, second, mills = rtc.datetime()
    if (adjust == 1):
        if (counter == 0):
            rtc.datetime((year + adjust, month, date, week, hour, minute, second, mills))
        elif (counter == 1):
            rtc.datetime((year, month + adjust, date, week, hour, minute, second, mills))
        elif (counter == 2):
            rtc.datetime((year, month, date + adjust, week, hour, minute, second, mills))
        elif (counter == 3):
            rtc.datetime((year, month, date, week + adjust, hour, minute, second, mills))
        elif (counter == 4):
            rtc.datetime((year, month, date, week, hour + adjust, minute, second, mills))
        elif (counter == 5):
            rtc.datetime((year, month, date, week, hour, minute + adjust, second, mills))
        elif (counter == 6):
            rtc.datetime((year, month, date, week, hour, minute, second + adjust, mills))
    else:
        if (counter == 0):
            if (hour > 0):
                rtc.datetime((year + adjust, month, date, week, hour, minute, second, mills))
        elif (counter == 1):
            if (month == 1):
                rtc.datetime((year, 12, date, week, hour, minute, second, mills))
            else:
                rtc.datetime((year, month + adjust, date, week, hour, minute, second, mills))
        elif (counter == 2):
            if (date == 1):
                rtc.datetime((year, month, 31, week, hour, minute, second, mills))
            else:
                rtc.datetime((year, month, date + adjust, week, hour, minute, second, mills))
        elif (counter == 3):
            if (week == 1):
                rtc.datetime((year, month, date, 7, hour, minute, second, mills))
            else:
                rtc.datetime((year, month, date, week + adjust, hour, minute, second, mills))
        elif (counter == 4):
            if (hour == 0):
                rtc.datetime((year, month, date, week, 23, minute, second, mills))
            else:
                rtc.datetime((year, month, date, week, hour + adjust, minute, second, mills))
        elif (counter == 5):
            if (minute == 0):
                rtc.datetime((year, month, date, week, hour, 59, second, mills))
            else:
                rtc.datetime((year, month, date, week, hour, minute + adjust, second, mills))
        elif (counter == 6):
            if (second == 0):
                rtc.datetime((year, month, date, week, hour, minute, 59, mills))
            else:
                rtc.datetime((year, month, date, week, hour, minute, second + adjust, mills))

# button-control change current operate element
def select(v):
    global counter
    if(counter!=6): counter += 1
    else: counter=0
    blink()
def set_up(v1):
    set_time(1)
    blink()
def set_down(v2):
    set_time(-1)
    blink()

show_time()
button_A.irq(trigger=Pin.IRQ_RISING, handler=select)
button_B.irq(trigger=Pin.IRQ_RISING, handler=set_up)
button_C.irq(trigger=Pin.IRQ_RISING, handler=set_down)
