# -*- coding: utf-8 -*-

from TCP_connection import Client
from command import Train
from time import sleep

TCP_IP = '192.168.210.200'


def main():
    direction = {"Forward": 1, "Backward": 0}
    client = Client()
    client.connect(TCP_IP)
    while True:
        numer = input("Podaj numer pociagu[1-7]: ")
        train = Train(numer)
        while True:
            key = input(train.menu())
            if key == 1:
                msg = train.move(13, direction["Forward"])  # do przodu z predkoscią max
            elif key == 2:
                msg = train.move(13, direction["Backward"])  # do tylu z predkoscią max
            elif key == 3:
                vel = input("Zakres[0-13]: ")
                msg = train.move(vel, direction["Forward"])  # do przodu z okreslona predkoscią
            elif key == 4:
                vel = input("Zakres[0-13]: ")
                msg = train.move(vel, direction["Backward"])  # do tylu z okreslona predkoscią
            elif key == 5:
                msg = train.move(0)  # stop
            elif key == 0:
                msg = train.move(0)  # zakoncz
                client.send(msg)
                sleep(1)
                break
            else:
                print("Podano bledny klawisz. Cofam na poczatek.")
                continue
            client.send(msg)
            sleep(1) #czekaj 1s
        key1 = input(menu())
        if key1 == 'q' or key1 == 'Q':
            break
        else:
            pass
    client.disconnect()

def menu():
    print("Aby zakonczyc program wcisnij klawisz q.")


if __name__ == "__main__":
    main()