# -*- coding: utf-8 -*-

import socket
import threading
import time

TCP_PORT = 5550
BUFFER_SIZE = 1024


class Client(object):
    # Klasa do obsługi połączenia z sterownikiem
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.address = ''
        pass


    def connect(self, address):
        # Nawiązanie połączenia z hostem o podanym adresie
        self.address = address
        if not self.connected:
            try:
                print "%s : Próba połączenia z sterownikiem" % time.ctime()
                self.connection.connect((address, TCP_PORT))
                self.connected = True
                print "%s : Połączono z sterownikiem" % time.ctime()

            except socket.error as message:
                print "%s : Nie udało sie połączyć z sterownikiem" % time.ctime()
                print message
                self.connected = False


    def disconnect(self):
        # Zamknięcie połączenia z hostem
        if self.connected:
            self.connection.close()
            self.connected = False