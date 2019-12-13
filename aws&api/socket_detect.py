import socket
import time
import sys
import csv
import time
import boto3
from picamera import PiCamera

directory = '/home/pi/Desktop/aws'  # folder name on your raspberry pi

P = PiCamera()
P.resolution = (800, 600)

#collectionId = 'mycollection'  # collection name

with open('credentials.csv', 'r') as input:
    next(input)
    reader = csv.reader(input)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]

client = boto3.client('rekognition',
                      region_name = 'us-east-2',
                      aws_access_key_id = access_key_id,
                      aws_secret_access_key = secret_access_key,
                      )

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("",2021))
s.listen(1)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    request = str(cl.recv(1024))
    print('content = %s' % request)

    if 'msg' in request:
        msg = request.split('/?msg=')[1].split('HTTP')[0]
        msg = msg.replace('%20', ' ')
        resp_msg = msg
        if 'connect' in msg:
            P.start_preview()
            time.sleep(1)
            image = '{}/image_a.jpg'.format(directory)
            P.capture(image)  # capture an image
            print('captured ' + image)
            P.stop_preview()
            with open(image, 'rb') as image:
                try:
                    response = client.detect_labels(Image = {'Bytes':image.read()},
                                MaxLabels=8,
                                MinConfidence=50)
                    result = ""
                    for i in range(0,6): 
                        result = result+response.get('Labels')[i].get('Name')+"/"
                    print(result)
                    result = result.encode('utf-8')
                    resp_msg = result
                except:
                    resp_msg = "no food detected"
        elif 'check' in msg:
            resp_msg = "start check"
        
        suc_response = "HTTP/1.1 200 OK\r\n\r\n%s" % resp_msg
        cl.send(str.encode(suc_response))
        cl.close()
        #cl.send(suc_response.encode('ascii'))

    else:
        fail_response = "HTTP/1.1 501 Implemented\r\n\r\nPlease attach msg!"
        cl.send(str.encode(fail_response))
        cl.close()

#cl.close()