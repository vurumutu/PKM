# -*- coding: utf-8 -*-

from xpressnet import Client
from xpressnet import Train

import zbar
from PIL import Image
import cv2
import urllib 
import requests
import numpy as np


TCP_IP = '192.168.210.200'
TCP_PORT = 5550

to_find_trains = ["train_one", "train_two", "train_six"]
found_train = None
# Pawła kod

def find_train():

    url = 'http://192.168.2.1/?action=stream'
    stream = requests.get(url, stream=True)
    bytes = b''


    while True:
        bytes+=stream.raw.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) ==27:
                exit(0)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image = Image.fromarray(gray)
            width, height = image.size
            zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())
            scanner = zbar.ImageScanner()
            scanner.scan(zbar_image)

        # Prints data from image.
            for decoded in zbar_image:
                return decoded.data


def main():
    client = Client()
    client.connect(TCP_IP, TCP_PORT)
    train = Train(5)  # lokomotywa z kamerą
    while True:
        client.send(train.move(127, 1))
        # find_train()
        if found_train == "train_one":
            print("Znalazlem pociag 1")
            to_find_trains.remove("train_one")
            found_train = None
            client.send(train.move(127, 0))
        elif found_train == "train_two":
            print("Znalazlem pociag 2")
            to_find_trains.remove("train_two")
            found_train = None
            client.send(train.move(127, 0))
        elif found_train == "train_six":
            print("Znalazlem pociag 6")
            to_find_trains.remove("train_six")
            found_train = None
            client.send(train.move(127, 0))
        if not to_find_trains:
            break
    client.disconnect()

if __name__ == "__main__":
    main()
