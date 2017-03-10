# -*- coding: utf-8 -*-

import socket
import threading
import time
from datetime import datetime
from time import sleep

TCP_PORT = 5550
BUFFER_SIZE = 1024


class Client(object):
    # Klasa do obsługi połączenia z sterownikiem
    def __init__(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.address = ''
        pass

    def __keepAlive__(self):
        while self.connected:
            self.connection.send('0xe40x100x000x010x8b\r\n')
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

    def connect(self, address):
        # Nawiązanie połączenia z hostem o podanym adresie
        self.address = address
        if not self.connected:
            try:
                print str(datetime.now().strftime('%H:%M:%S')) + ": Próba połączenia z sterownikiem"
                self.connection.connect((address, TCP_PORT))
                self.connected = True
                self.__start_reader__()
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

    def send(self, message):
        # Wysłanie wiadomości do hosta
        if self.connected:
            self.connection.send(message)
            print str(datetime.now().strftime('%H:%M:%S')) + ": Wysłano wiadomość: " + str(message)
