# -*- coding: utf-8 -*-

# TODO Dodać do metod docstring

import socket
import threading
from datetime import datetime
from time import sleep
import binascii

class Client(object):
    # Klasa do obsługi połączenia z sterownikiem
    def __init__(self):
        self.connection = None
        self.connected = False
        self.address = ''
        self.port = ''
        self.lock = threading.Lock()
        pass

    def keep_alive(self, once=False):
        while True:
            self.lock.acquire()
            self.connection.setblocking(False)
            try:
                msg = self.receive()
            except:
                pass
            self.connection.setblocking(True)
            self.lock.release()
            if once:
                break
            sleep(0.2)

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
                threading._start_new_thread(self.keep_alive, False)
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
        self.keep_alive(True)
        if self.connected:
            message = 'fffe' + message
            message = binascii.unhexlify(message)
            self.lock.acquire()
            self.connection.send(message)
            self.lock.release()
            print str(datetime.now().strftime('%H:%M:%S')) + ": Wysłano wiadomość: " + str(message)
            # TODO Metoda ma zwracać odebraną wiadomość na podstawie wysłanej wiadomości

     #TODO Dodanie nowej metody receive)
    def receive(self):
        return "Not added yet."
    # TODO Dodanie metod do obsługi poszczególnych rozkazów do sterownika nie związanych z obsługą pociągów