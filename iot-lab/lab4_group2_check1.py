import network
import urequests
from machine import I2C,Pin
import ssd1306

# construct an I2C bus in LED
i2c = I2C(-1, Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)


# ('160.39.170.89', '255.255.254.0', '160.39.170.1', '128.59.1.3')
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Columbia University', '')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def show_location():
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCNYYI5dEVar6OPOgKM-ivPcOhX1w54vVI'
    response = urequests.post(url, data = "some dummy content")
    parsed = response.json()
    lat = parsed.get('location').get('lat')
    lng = parsed.get('location').get('lng')
    oled.fill(0)
    oled.text("location:%d,%d" % (lat,lng), 0, 0)
    oled.show()

do_connect()
show_location()
