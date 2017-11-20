# -*- coding: utf-8 -*-

import socket
import threading
from datetime import datetime
from time import sleep
import binascii


class Client(object):
    """Klasa do obsługi połączenia z sterownikiem

        *Pozwala na wysyłanie i odbieranie komunikatów z sterownika.
        *Zapewnia poprawną inicjalizacje połączenia z sterownikiem.
        *Zapewnia prawidłowe kodowanie wysyłanych komunikatów.
        *Zapewnia poprawne odkodowanie otrzymanych komunikatów
        *Pozwala na wysłanie podstawowych komunikatów operujących sterownikiem
    """
    def __init__(self):
        """Domyślne ustawienia klasy"""
        self.connection = None
        self.connected = False
        self.address = ''
        self.port = ''
        self.lock = threading.Lock()
        pass

    def keep_alive(self, once=False):
        """Zapewnienia poprawne połączenie"""
        while True:
            self.lock.acquire()
            self.connection.setblocking(False)
            try:
                self.receive()
            except:
                pass
            self.connection.setblocking(True)
            self.lock.release()
            if once:
                break
            sleep(0.2)

    @staticmethod
    def calculate_xor(message):
        """Obliczenie X-OR dla komunikatu

            Args:
                message (string): Komunikat  dla którego będzie obliczony X-OR

            Returns:
                xor (string): Zwraca obliczony X-OR komunikatu

        """
        data = []
        xor = ""
        while message:
            data.append(int(message[:2], 16))
            message = message[2:]
        for i in range(1, len(data)):
            if i == 1:
                xor = data[i - 1] ^ data[i]
            else:
                xor ^= data[i]
        if len(data) == 1:
            xor = data[0]
        if xor < 16:
            xor = hex(xor)[2:]
            xor = '0' + str(xor)
        else:
            xor = hex(xor)[2:]
        return xor

    def connect(self, address, port):
        """Nawiązanie połączenia z sterownikiem.

            Args:
                address (string): Adres IP sterownika
                port (int): Numer portu sterownika

        """
        self.address = address
        self.port = port
        if not self.connected:
            try:
                print str(datetime.now().strftime('%H:%M:%S')) + ": Próba połączenia z sterownikiem"
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((self.address, self.port))
                self.connected = True
                threading._start_new_thread(self.keep_alive, (False,))
                print str(datetime.now().strftime('%H:%M:%S')) + ": Połączono z sterownikiem"

            except socket.error as message:
                print str(datetime.now().strftime('%H:%M:%S')) + ": Nie udało sie połączyć z sterownikiem"
                print message
                self.connected = False

    def disconnect(self):
        """Zamknięcie połączenia z sterownikiem"""
        if self.connected:
            self.connection.close()
            self.connected = False

    def send(self, message):
        """Wysłanie rozkazu do sterownika

            Args:
                message (string): Rozkaz wysyłany do sterownika - format szesnastkowy

            Returns:
                response (string): Zwraca odpowiedź sterownika na dany rozkaz

        """
        self.keep_alive(True)
        if self.connected:
            xor = self.calculate_xor(message)
            message += xor
            message = 'fffe' + message
            msg = binascii.unhexlify(message)
            self.lock.acquire()
            self.connection.send(msg)
            self.lock.release()
            print str(datetime.now().strftime('%H:%M:%S')) + ": Wysłano wiadomość: " + str(message)
            response = self.receive()
            return response

    def receive(self):
        """Metoda zwracająca odpowiedź sterownika

            Returns:
            message (string): Zwraca otrzymaną odpowiedź sterownika

        """
        message = self.connection.recv(64)
        message = binascii.hexlify(message)
        message = message[4:]  # wycinanie nagłówka fffe
        return message

    @staticmethod
    def stop_all_locomotives():
        """Zatrzymanie wszystkich pociągów

            Returns:
                command (string): Zwraca komendę

        """
        command = '80'
        return command

    @staticmethod
    def off_energy():
        """Wyłączenie zasilania

            Returns:
                command (string): Zwraca komendę

        """
        command = '2180'
        return command

    @staticmethod
    def get_soft_version():
        """Żądanie wersji oprogramowania sterownika

            Returns:
                command (string): Zwraca komendę

        """
        command = '2121'
        return command

    @staticmethod
    def get_status():
        """Żądanie stanu sterownika

            Returns:
                command (string): Zwraca komendę

        """
        command = '2124'
        return command


class Train(object):
    """Klasa do obsługi sterownia poszczególnych pociągów

        *Przy tworzeniu przypisuje adres pociągu
        *Pozwala zadać prędkość i kierunek
        """
    def __init__(self, number):
        """Domyślne ustawienia klasy

            Args:
                number (int): Numer  pociągu

        """
        self.order = None
        self.locomotive = number
        self.velocity = 0
        self.course = True
        pass

    @staticmethod
    def header(order):
        """Wybór nagłówka rozkazu określającego precyzje zadawanej prędkości

            Args:
                order (int): Numer rozkazu

            Returns:
                header (string): Zwraca nagłówek rozkazu

        """
        if order == 1:
            header = 'E410'  # 14
            return header
        elif order == 2:
            header = 'E411'  # 27
            return header
        elif order == 3:
            header = 'E412'  # 28
            return header
        elif order == 4:
            header = 'E413'  # 127
            return header
        else:
            return 0

    @staticmethod
    def address(locomotive):
        """Wybór lokomotywy

            Args:
                locomotive (int): Numer lokomotywy

            Returns:
                address (string): Zwraca adres lokomotywy

        """
        address = '000' + str(hex(locomotive)[2])
        return address

    @staticmethod
    def speed(velocity, course):
        """Określenie prędkości i kierunku

            Args:
                velocity (int): Prędkość lokomotywy
                course (int): Kierunek lokomotywy

            Returns:
                msg (string): Rozkaz dla lokomotywy

        """
        msg = hex(course * 128 + velocity)[2:]
        if len(msg) == 1:
            msg = '0' + str(msg)
        return msg

    # Tworzenie komendy do sterowania pociągiem
    def move(self, velocity, course=0):
        """Określenie prędkości i kierunku

            Args:
                velocity (int): Prędkość lokomotywy
                course (int): Kierunek lokomotywy

            Returns:
                msg (string): Rozkaz dla lokomotywy

        """
        command = self.header(4) + self.address(self.locomotive) + self.speed(velocity, course)
        return command

    def stop_locomotive(self):
        """Zatrzymanie wybranej lokomotywy

            Returns:
                command (string): Zwraca rozkaz

        """
        command = '92000' + self.address(self.locomotive)
        return command
