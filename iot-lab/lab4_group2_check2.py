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

def get_location():
    url = 'https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyCNYYI5dEVar6OPOgKM-ivPcOhX1w54vVI'
    response = urequests.post(url, data = "some dummy content")
    parsed = response.json()
    lat = parsed.get('location').get('lat')
    lng = parsed.get('location').get('lng')
    return lat, lng

def show_weather():
    lat, lng = get_location()
    api = "1d2ed39530531bc8f4789e9613dd89ca"
    url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}".format(lat,lng)
    url +="&APPID="+api
    response = urequests.get(url, data = "some dummy content")
    parsed = response.json()
    des = parsed.get('weather')[0].get('description')
    tem = parsed.get('main').get('temp')
    oled.fill(0)
    oled.text("weather:", 0, 0)
    oled.text(des,0,10)
    oled.text("temp:%d" % (tem), 0, 20)
    oled.show()

do_connect()
show_weather()