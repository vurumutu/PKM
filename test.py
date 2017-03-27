# -*- coding: utf-8 -*-

from TCP_connection import Client
from command import Train
from time import sleep
import os

TCP_IP = '192.168.210.200'
TCP_PORT = 5550


def cls():
    # TODO Sprawdzić działanie w konsoli - czyszczenie ekranu w obsłudze menu
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    direction = {"Forward": 1, "Backward": 0}
    client = Client()
    client.connect(TCP_IP, TCP_PORT)
    # TODO Rozbudowa menu do testów
    while True:
        numer = input("Podaj numer pociągu[1-7]: ")
        if not numer in range(1, 8):
            # cls()
            print("Nieprawidlowy numer pociagu.\n")
            continue
        train = Train(numer)
        while True:
            key = input(train.menu())
            if key == 1:
                msg = train.move(127, direction["Forward"])  # do przodu z prędkością max
            elif key == 2:
                msg = train.move(127, direction["Backward"])  # do tylu z prędkością max
            elif key == 3:
                vel = input("Zakres[0-127]: ")
                msg = train.move(vel, direction["Forward"])  # do przodu z określoną prędkością
            elif key == 4:
                vel = input("Zakres[0-127]: ")
                msg = train.move(vel, direction["Backward"])  # do tylu z określoną prędkością
            elif key == 5:
                msg = train.move(0)  # Stop
            elif key == 6:
                msg = train.off_energy()
            elif key == 0:
                msg = train.move(0)  # Zakończ
                client.send(msg)
                sleep(1)
                break
            else:
                # cls()
                print("Podano nieprawidłowy klawisz. Cofam na poczatek.")
                continue
            client.send(msg)
            sleep(1)  # Czekaj 1s
        key1 = input(menu())
        if key1 == 'q' or key1 == 'Q':
            break
        else:
            pass
    client.disconnect()


def menu():
    print("Aby zakończyć program naciśnij klawisz q.")


if __name__ == "__main__":
    main()
