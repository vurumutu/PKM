# -*- coding: utf-8 -*-

from xpressnet import Client
from xpressnet import Train


TCP_IP = '192.168.210.200'
TCP_PORT = 5550

to_find_trains = ["Train 1", "Train 2", "Train 3"]
found_train = None
# Pawła kod


def main():
    client = Client()
    client.connect(TCP_IP, TCP_PORT)
    train = Train(5)  # lokomotywa z kamerą
    while True:
        client.send(train.move(127, 1))
        # find_train()
        if found_train == "Train 1":
            print("Znalazlem pociag 1")
            to_find_trains.remove("Train 1")
            found_train = None
            client.send(train.move(127, 0))
        elif found_train == "Train 2":
            print("Znalazlem pociag 2")
            to_find_trains.remove("Train 2")
            found_train = None
            client.send(train.move(127, 0))
        elif found_train == "Train 6":
            print("Znalazlem pociag 6")
            to_find_trains.remove("Train 3")
            found_train = None
            client.send(train.move(127, 0))
        if not to_find_trains:
            break
    client.disconnect()

if __name__ == "__main__":
    main()
