# aws label detection with boto3
import csv
import time
import boto3
from picamera import PiCamera

directory = '/home/pi/Desktop'  # folder name on your raspberry pi

P = PiCamera()
P.resolution = (800, 600)
P.start_preview()
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

time.sleep(2)
image = '{}/image_a.jpg'.format(directory)
P.capture(image)  # capture an image
print('captured ' + image)

#photo = 'apple.jpg'

with open(image, 'rb') as image:
    try:
        response = client.detect_labels(Image = {'Bytes':image.read()},
                                MaxLabels=3,
                                MinConfidence=90)
        print(response)
    except:
        print('no food')
        

#    source_bytes = source_image.read()