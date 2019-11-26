import machine
import time
import ustruct
import ssd1306

REG_DATAX0 =(0x32)
REG_DATAY0 = (0x34)
REG_POWER_CTL = (0x2D)
MULTIPLIER = (0.004)  
GRAVITY = (9.80665) 
X_LIMIT = 128
Y_LIMIT = 32

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

cs = machine.Pin(15, machine.Pin.OUT)
cs.on()
spi = machine.SPI(1, baudrate=400000, polarity=1, phase=1)

x_now = 0
y_now = 0
    
def read(reg_add):
    reg_add = reg_add | 0xC0
    reg_add = ustruct.pack('b',reg_add)
    cs.off()
    spi.write(reg_add)
    read_data = spi.read(2)
    cs.on()
    return read_data

def write(reg_add,value):
    reg_add = reg_add & 0x7f
    reg_add = ustruct.pack('b',reg_add)
    value = ustruct.pack('b',value)
    cs.off()
    spi.write(reg_add)
    spi.write(value)
    cs.on()
    
def init():
    write(REG_POWER_CTL,0x08)

def X_get():
    read_x = read(REG_DATAX0)
    read_x =  ustruct.unpack('h',read_x)
    return read_x[0]*MULTIPLIER*GRAVITY

def Y_get():
    read_y = read(REG_DATAY0)
    read_y =  ustruct.unpack('h',read_y)
    return read_y[0]*MULTIPLIER*GRAVITY

def X_change():
    global x_now
    x_dif = X_get()

    if x_dif > 1:
        x_now = x_now - 5
    elif x_dif < -1:
        x_now = x_now + 5

    if x_now < 0:
        x_now = X_LIMIT
    if x_now > X_LIMIT:
        x_now = 0

def Y_change():
    global y_now
    y_dif = Y_get()

    if y_dif > 1:
        y_now = y_now + 2
    elif y_dif < -1:
        y_now = y_now - 2

    if y_now < 0:
        y_now = Y_LIMIT
    if y_now > Y_LIMIT:
        y_now = 0

def showtext(x,y):
    oled.text("Group2", x, y)
    oled.show()

init()

while(1):
    oled.fill(0)
    X_change()
    Y_change()
    showtext(x_now, y_now)
