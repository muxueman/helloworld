from machine import I2C,Pin
import network
import urequests
import ssd1306

i2c = I2C(-1, Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Columbia University', '')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

do_connect()
api_key = 'IGDXL5TUMXYOWFGB'
status = 'hello world'
url = "https://api.thingspeak.com/apps/thingtweet/1/statuses/update?api_key={}&status={}".format(api_key,status)
urequests.post(url, data = "some dummy content")
oled.fill(0)
oled.text("tweet sent!", 0, 0)
oled.show()