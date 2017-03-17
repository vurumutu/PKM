# -*- coding: utf-8 -*-

# TODO Dodać do metod docstring

import socket
import threading
from datetime import datetime
from time import sleep


class Client(object):
    # Klasa do obsługi połączenia z sterownikiem
    def __init__(self):
        self.connection = None
        self.connected = False
        self.address = ''
        self.port = ''
        pass

    def __keepAlive__(self):
        # TODO Prawdopodobnie po testach z kodowaniem niepotrzebna metoda
        while self.connected:
            self.connection.send('21 21 00')
            sleep(5)
            cc = ''
            for c in self.connection.recv(512):
                if len(hex(int(ord(c)))) == 1:
                    cc += '0'
                cc += hex(int(ord(c)))
            print 'Received: ' + cc.replace('0x', ' ')

    def __start_reader__(self):
        self.receiver_thread = threading.Thread(target=self.__keepAlive__)
        self.receiver_thread.setDaemon(True)
        self.receiver_thread.start()

    def connect(self, address, port):
        self.address = address
        self.port = port
        # Nawiązanie połączenia z hostem o podanym adresie
        if not self.connected:
            try:
                print str(datetime.now().strftime('%H:%M:%S')) + ": Próba połączenia z sterownikiem"
                self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection.connect((self.address, self.port))
                self.connected = True
                self.__start_reader__()
                print str(datetime.now().strftime('%H:%M:%S')) + ": Połączono z sterownikiem"

            except socket.error as message:
                print str(datetime.now().strftime('%H:%M:%S')) + ": Nie udało sie połączyć z sterownikiem"
                print message
                self.connected = False

    def disconnect(self):
        # Zamknięcie połączenia z hostem
        if self.connected:
            self.connection.close()
            self.connected = False

    def send(self, message):
        # Wysłanie wiadomości do hosta
        if self.connected:
            self.connection.send(message)
            print str(datetime.now().strftime('%H:%M:%S')) + ": Wysłano wiadomość: " + str(message)
            # TODO Metoda ma zwracać odebraną wiadomość na podstawie wysłanej wiadomości (Dodanie nowej metody receive)

    # TODO Dodanie metod do obsługi poszczególnych rozkazów do sterownika nie związanych z obsługą pociągów
