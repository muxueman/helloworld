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

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    print('content = %s' % request)

    if 'msg' in request:
        msg = request.split('/?msg=')[1].split('HTTP')[0]
        msg = msg.replace('%20', ' ')

        oled.fill(0)
        oled.text(msg, 0, 0)
        oled.show()

        suc_response = "HTTP/1.1 200 OK\r\n\r\n%s"
        cl.send(str.encode(suc_response))

    else:
        fail_response = "HTTP/1.1 501 Implemented\r\n\r\nPlease attach msg!"
        cl.send(str.encode(fail_response))

    time.sleep(1)
    cl.close()


