# -*- coding: utf-8 -*-

import kalman
from time import sleep
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


def find_train():
    url = 'http://192.168.2.1/?action=stream'
    stream = requests.get(url, stream=True)
    bytes = b''

    while True:
        bytes += stream.raw.read(1024)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) == 27:
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


def find_train_simulator():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == 27:
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
    # Nawiązanie połączenia
    client = Client()
    client.connect(TCP_IP, TCP_PORT)

    # Ustawienia startowe
    train = Train(6)  # lokomotywa z kamerą
    spotter = kalman.Model(0)
    camera_distance = 14
    start_position = True
    on_the_route = False

    to_find_trains = ["train_one", "train_two", "train_five"]
    tracks = ["track_one", "track_two", "track_three", "track_four"]
    found_qr_code = None
    actual_track = None

    while True:
        # Ruszanie ze stacji jeżeli zwiadowca znajduje się na niej, istnieją pociągi do znalezienia oraz istnieją
        # trasy do przejechania
        if start_position is True and to_find_trains is True and tracks is True:
            actual_track = tracks[0]
            start_position = False
            on_the_route = True
            client.send(train.move(50, 0))
            spotter.set_power(50)

        found_qr_code = find_train()
        # Zatrzymanie zwiadowcy na stacji i przygotowanie do ponownego wyjazdu
        if found_qr_code == "train_station" and start_position is False and on_the_route is False:
            start_position = True
            spotter.set_power(0)
            client.send(train.move(0))
            sleep(5)
            spotter = kalman.Model(0)

        if found_qr_code == "train_one" and "train_one" in to_find_trains and on_the_route is True:
            print("Znalazłem pociąg 1 na trasie: %s" (actual_track))
            print(spotter.get_position() + spotter.get_stop_distance() + camera_distance)

            to_find_trains.remove("train_one")
            tracks.remove(actual_track)
            found_qr_code = None
            # Zatrzymanie zwiadowcy
            on_the_route = False
            spotter.set_power(0)
            client.send(train.move(0))
            sleep(5)
            # Powrót na pozycje startową
            spotter = kalman.Model(0)
            client.send(train.move(50, 1))
            spotter.set_power(50)
        elif found_qr_code == "train_two" and "train_two" in to_find_trains and on_the_route is True:
            print("Znalazłem pociąg 2 na trasie: %s" (actual_track))
            print(spotter.get_position() + spotter.get_stop_distance() + camera_distance)

            to_find_trains.remove("train_two")
            tracks.remove(actual_track)
            found_qr_code = None
            # Zatrzymanie zwiadowcy
            on_the_route = False
            spotter.set_power(0)
            client.send(train.move(0))
            sleep(5)
            # Powrót na pozycje startową
            spotter = kalman.Model(0)
            client.send(train.move(50, 1))
            spotter.set_power(50)
        elif found_qr_code == "train_six" and "train_five" in to_find_trains and on_the_route is True:
            print("Znalazłem pociąg 5 na trasie: %s" (actual_track))
            print(spotter.get_position() + spotter.get_stop_distance() + camera_distance)

            to_find_trains.remove("train_five")
            tracks.remove(actual_track)
            found_qr_code = None
            # Zatrzymanie zwiadowcy
            on_the_route = False
            spotter.set_power(0)
            client.send(train.move(0))
            sleep(5)
            # Powrót na pozycje startową
            spotter = kalman.Model(0)
            client.send(train.move(50, 1))
            spotter.set_power(50)

        if not to_find_trains or not tracks:
            break
    client.disconnect()


if __name__ == "__main__":
    main()
