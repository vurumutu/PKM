# -*- coding: utf-8 -*-

from xpressnet import Client
from xpressnet import Train
from time import sleep

TCP_IP = '192.168.210.200'
TCP_PORT = 5550


# Konfiguracja karty sieciowej
# IP address: 192.168.210.201
# Subnet mask: 255.255.255.0
# Default gateway: 192.168.210.1
# Preferred DNS server: 192.168.210.1


def menu():
    print("1. Do przodu - max prędkość")
    print("2. Do tylu - max prędkość")
    print("3. Do przodu - ustal prędkość")
    print("4. Do tylu - ustal prędkość")
    print("5. Stop - zerowa prędkość")
    print("6. Wyłącz zasilanie pociągów")  # klawisz off na pilocie
    print("7. Wyłącz zasilanie aktualnego pociągu")  # klawisz off na pilocie
    print("8. Żądanie następnego adresu")  # klawisz off na pilocie
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
            elif key == 8:
                msg = client.get_next_address_in_stack(12)  # Żądanie następnego adresu
            elif key == 0:
                msg = train.move(9)  # Zakończ
                client.send(msg)
                sleep(1)
                break
            else:
                print("Podano nieprawidłowy klawisz!")
                continue
            print(client.send(msg))
            sleep(1)  # Czekaj 1s
        key1 = raw_input(menu())
        if key1 == 'q' or key1 == 'Q':
            break
        else:
            continue
    client.disconnect()


if __name__ == "__main__":
    # main()
    client = Client()
    client.connect(TCP_IP, TCP_PORT)
    address = 0
    while True:
        msg = client.get_next_address_in_stack(address)
        rec = client.send(msg)
        print(rec)
        if rec[3] is '0':
            print("Znaleziony adres lokomotywy: " + rec[4:8])
            address = int(rec[4:8], 16)
            msg = client.get_locomotive_status(address)
            rec2 = client.send(msg)
            rec2 = bin(int(rec, 16))[2:]
            if rec2[12] is '0':
                print("Lokomotywa o adresie" + str(address) + "jest dostępna.")
            else:
                print("Lokomotywa o adresie" + str(address) + "jest zajęta przez inne urządzenie.")

            if rec2[13:16] is '000':
                print("Lokomotywa o adresie" + str(address) + "używa 14 stopniowego trybu prędkości.")
            elif rec2[13:16] is '001':
                print("Lokomotywa o adresie" + str(address) + "używa 27 stopniowego trybu prędkości.")
            elif rec2[13:16] is '010':
                print("Lokomotywa o adresie" + str(address) + "używa 28 stopniowego trybu prędkości.")
            else:
                print("Lokomotywa o adresie" + str(address) + "używa 128 stopniowego trybu prędkości.")

            if rec2[16] is '0':
                print("Lokomotywa o adresie" + str(address) + "ma ustawiony kierunek jazdy do tylu.")
            else:
                print("Lokomotywa o adresie" + str(address) + "ma ustawiony kierunek jazdy do przodu.")

            if rec2[17:24] is '0000000':
                print("Lokomotywa o adresie" + str(address) + "ma prędkość zerowa.")
            elif rec2[17:24] is '0000001':
                print("Lokomotywa o adresie" + str(address) + "ma ustawione awaryjne zatrzymanie.")
            else:
                print("Lokomotywa o adresie" + str(address) + "ma ustawiona prędkość: " + str(int(rec2, 2) - 1))
        else:
            break
        sleep(1)
