# -*- coding: utf-8 -*-

from xpressnet import Client
from xpressnet import Train
from time import sleep

TCP_IP = '192.168.210.200'
TCP_PORT = 5550


def menu():
    print("1. Do przodu - max prędkość")
    print("2. Do tylu - max prędkość")
    print("3. Do przodu - ustal prędkość")
    print("4. Do tylu - ustal prędkość")
    print("5. Stop - zerowa prędkość")
    print("6. Wyłącz zasilanie pociągów")  # klawisz off na pilocie
    print("0. Zakończ")
    print("Aby zakończyć program naciśnij klawisz q.")


def main():
    direction = {"Forward": 1, "Backward": 0}
    client = Client()
    client.connect(TCP_IP, TCP_PORT)
    while True:
        numer = input("Podaj numer pociągu[1-7]: ")
        if numer not in range(1, 8):
            print("Nieprawidłowy numer pociągu.\n")
            continue
        train = Train(numer)
        while True:
            key = input(menu())
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
                msg = train.move(0)  # Stop - zadanie zerowej prędkości
            elif key == 6:
                msg = client.stop_all_locomotives()  # Zatrzymanie wszystkich lokomotyw awaryjnie
            elif key == 7:
                msg = train.stop_locomotive()  # Zatrzymanie aktualnej lokomotywy awaryjnie
            elif key == 0:
                msg = train.move(0)  # Zakończ
                client.send(msg)
                sleep(1)
                break
            else:
                print("Podano nieprawidłowy klawisz!")
                continue
            client.send(msg)
            sleep(1)  # Czekaj 1s
        key1 = raw_input(menu())
        if key1 == 'q' or key1 == 'Q':
            break
        else:
            continue
    client.disconnect()

if __name__ == "__main__":
    main()