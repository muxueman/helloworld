# 160.39.190.131
import network
import machine
import ssd1306
import socket
import time
from machine import Pin

i2c = machine.I2C(-1, Pin(5), Pin(4))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Columbia University', '')
ip_addr = sta_if.ifconfig()
socket_addr = socket.getaddrinfo(ip_addr[0], 80)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(socket_addr)
s.listen(1)
print('listening on', socket_addr)
rtc = machine.RTC()
rtc.datetime((2019, 9, 25, 4, 16, 5, 0, 0))

oled_on = False
show_time_now = False

def show_time():
    oled.fill(0)
    time = str(rtc.datetime()[4]) + ':' + str(rtc.datetime()[5]) + ':' + str(rtc.datetime()[6])
    oled.text(time, 0, 0)
    oled.show()
def show_start():
    oled.fill(0)
    oled.text("Welcome to IOT!", 0, 0)
    oled.show()
    time.sleep(3)
def show_stop():
    oled.fill(0)
    oled.text("Bye~", 0, 0)
    oled.show()
    time.sleep(5)
    oled.fill(0)
    oled.show()

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        request = str(request)
        print('content = %s' % request)

        if 'msg' in request:
            msg = request.split('/?msg=')[1].split('HTTP')[0]
            msg = msg.replace('%20', ' ')
            resp_msg = msg
            if 'start' in msg:
                show_start()
                oled_on = True
                resp_msg = "start now"
                show_time_now = False
            elif 'stop' in msg:
                show_stop()
                oled_on = False
                resp_msg = "stop now"
                show_time_now = False
            elif 'time' in msg:
                time_digits = msg.split("=")[1].split("-")
                msg = "show time"
                resp_msg = "showing time now"
                rtc.datetime((int(time_digits[0]), int(time_digits[1]), int(time_digits[2]), 0, int(time_digits[3]),
                                int(time_digits[4]), int(time_digits[5]), 0))
                show_time()
                show_time_now = True

            if oled_on and not show_time_now:
                oled.fill(0)
                oled.text(msg, 0, 0)
                oled.show()
            if oled_on and show_time_now:
                show_time()

            suc_response = "HTTP/1.1 200 OK\r\n\r\n%s" % resp_msg
            cl.send(str.encode(suc_response))

        else:
            fail_response = "HTTP/1.1 501 Implemented\r\n\r\nPlease attach msg!"
            cl.send(str.encode(fail_response))

    except:
        if oled_on and show_time_now:
            show_time()

    finally:
        cl.close()