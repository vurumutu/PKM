#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import timeit
import threading
import io

# typy urzadzen
TYP_NONE = 0x00
TYP_Zwrotnica = 0x01
TYP_Semafor = 0x02
TYP_Balisa = 0x03

# strefy
STR_NONE = 0x00
STR_Strzyza = 0x01
STR_Kielpinek = 0x02
STR_Rebiechowo = 0x03
STR_Banino = 0x04
STR_Wrzeszcz = 0x05

#semafory
LED_GREEN = 0x31
LED_YELLOW1 = 0x32
LED_RED = 0x33
LED_YELLOW2 = 0x34
LED_WHITE = 0x35
LED_OFF = 0x30
LED_GET = 0x39

# ramka:
# 1: '>'
# 4: addr hex in ascii
# 1: space
# 1: command
# n: parameters
# 1: '\r'

semafor = []
zwrotnica = []
balisa = []


class Agent:
    def __init__(self, addr='1F000000', strefa='', l_addr=None):
        self.address = addr
        self.strefa = strefa
        self.l_address = l_addr

    def send(self, data):
        msg = '>'+self.address+' ' + data + '\r'
        ser.write(msg.decode('unicode-escape'))

    @staticmethod
    def skanuj():
        ser.write(u'>1F000000 39\r')

    def zmien_adres(self, strefa, adres):
        ser.write("61 "+format(strefa, 'x')+format(adres, 'x'))
        self.address = strefa << 16 + adres


class Semafor:
    def __init__(self, addr, strefa, l_addr):
        self.agent = Agent(addr, strefa, l_addr)

    def wlacz(self, led):
        self.agent.send(format(led, "x") + " 00")

    def mrugaj(self, led):
        self.agent.send("00 " + format(led, "x"))

    def wylacz(self):
        self.agent.send(format(0x30, "x") + ' ' + format(0x30, "x"))


class Zwrotnica:
    def __init__(self, addr, strefa, l_addr, stat, limit):
        self.agent = Agent(addr, strefa, l_addr)
        self.state = stat
        self.limiter = limit
        #self.addr = addr

    def lewo(self):
        #self.agent.send(format("31", "x"))
        self.agent.send("31")

    def prawo(self):
        #self.agent.send(format("32", "x"))
        self.agent.send("32")

    def wylacz(self):
        self.agent.send(format("30", "x"))


class Balisa:
    def __init__(self, addr, strefa, l_addr, stat, hist):
        self.agent = Agent(addr, strefa, l_addr)
        self.state = stat
        self.histereza = hist

    def wlacz(self, hist):
        self.histereza = hist
        self.agent.send("33 " + format(self.histereza, "x"))

    def wylacz(self):
        self.agent.send("30")


### KONIEC KLAS ###
def _readline():
    ms = []
    while True:
        c = ser.read(1)
        if c == '\r':
            return ms
        else:
            ms.append(c)

def can_odb():
    while ser_raw.isOpen():
        reading = ser.readline()
        print('odebralem: '+reading)
        handle_data(reading)
    print('can_odb koniec')


time1 = 0
last_time1 = 0

# funkcja parsujaca pojedyncza komende/odpowiedz
def handle_scan(data):
    global time1
    global last_time1

    typ = data[1:3]
    strefa = data[3:5]
    l_adres = data[5:9]
    attr1 = data[10:12]
    attr2 = data[13:15]

    if typ == '01' and len(zwrotnica) < 49:
    # do mierzenia czasu
        # for x in zwrotnica:
        #     if x.l_addr == l_adres:
        #         return None
        zwrotnica.append(Zwrotnica(data[1:9], strefa, l_adres, attr1, attr2))

    elif typ == '02' and len(semafor) < 49: #Semafor
        semafor.append(Semafor(data[1:9], strefa, l_adres))
    elif typ == '03' and len(balisa) < 49: # Balisa
        # for x in balisa:
        #     if x.l_addr == l_adres:
        #         print 'balisa ' + l_adres + '\t' #+ end - start
        #         return None
        #         last_time = time
        #         time = timeit.timeit()
        #         print time-last_time
        balisa.append(Balisa(data[1:9], strefa, l_adres, attr1, attr2))
    if typ == '03' and data[16:18] <'70': # wieksze tyl mniejsze przod
        #print data[16:18]
        # print u'time1 ' + str(time1)
        # print u'last_time ' + str(last_time1)
        last_time1 = time1
        time1 = time.clock() # aktualny czas
        print u'balisa ' + l_adres + u'\t' + str(time1 - last_time1)
        #print (time1 - last_time1)


# obsluga ciagu wejsciowego z CAN
def handle_data(data):
    dat = data.split('\r')
    for d in dat:
        handle_scan(d)

#configure the serial connections (the parameters differs on the device you are connecting to)
ser_raw = serial.Serial(
    port='COM6',
    # port='COM21',
    baudrate=500000,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

if ser_raw.isOpen():
    print("Serial is open: ")
else:
    print("Serial is closed!!")
print(ser_raw.portstr)

# aby obejsc domyslne konczenie ramki znakiem '\n' i konczyc ja '\r'
ser = io.TextIOWrapper(io.BufferedRWPair(ser_raw, ser_raw, 1),
                       newline='\r',
                       line_buffering=True)
ser._CHUNK_SIZE = 1 # pojedyncza wielkosc bufora odbiorczego, aby nie wprowadzac opoznien

# listy agentow
zwrotnica = []
balisa = []
semafor = []

# watek odbioru
watek_odb = threading.Thread(target=can_odb)
watek_odb.start()

'''
if __name__ == '__main__':
    a1 = Agent()
    z1 = Zwrotnica(a1)
    print(a1.skanuj())
    for i in range(5):
        z1.lewo()
        time.sleep(5)
        z1.prawo()
        time.sleep(5)
    ser.close()
    '''

ser.write(u'master\r')
Agent.skanuj()


time.sleep(1)
for balisas in balisa: # ustawiamy automatyczne zglaszanie i histereze
    balisas.wlacz(0x70)
    time.sleep(0.1) # bez sleepa zapycha sie

print "test balis"
print len(zwrotnica)
print len(zwrotnica)
print len(balisa)
lista3 = [32]
lista = [0, 1, 3, 4, 6, 7, 11, 12, 13, 15, 17, 18, 20, 21, 22, 23, 24, 30, 31, 38]
lista2 = [2, 5, 9, 10, 14, 16, 17, 32, 33, 34, 35, 36, 37, 39, 40, 41, 42]

"""while True:
    for y in zwrotnica:
        if y.agent.address == '010003DC': # 0102000B 0102000C 01020001
            y.lewo() # 010003DC 0100047B 010003DF
            time.sleep(1)
            y.prawo()
            time.sleep(1)"""
        # if y.agent.address == '01020001': # 0102000B 0102000C 01020001
        #     y.lewo()
        #     time.sleep(1)
        #     y.prawo()
        #     time.sleep(1)
        # if y.agent.address == '0102000B': # 0102000B 0102000C 01020001
        #     y.lewo()
        #     time.sleep(1)
        #     y.prawo()
        #     time.sleep(1)
        # if y.agent.address == '0102000C': # 0102000B 0102000C 01020001
        #     y.lewo()
        #     time.sleep(1)
        #     y.prawo()
        #     time.sleep(1)
        # x = lista3[y]
        # for i in range(1):
        #     print("Test zwrotnicy: " + str(x))
        #     print("Adres: " + str(zwrotnica[x].addr))
        #     time.sleep(1)
        #     zwrotnica[x].prawo()
        #     time.sleep(1)
        #     zwrotnica[x].lewo()


# szukanie zwrotnic po adresach oraz
# tworzenie listy znalezionych zwrotnic
addr_zwrotnic = ['0102000B', '0102000C', '010003DF', '01020001']
zwrotnice_ = []
for zwrot in zwrotnica:
    for address in addr_zwrotnic:
        if zwrot.agent.address == address:
            zwrotnice_.append(zwrot)


# time.sleep(1)
# Agent.skanuj()

# f = open('pkm_scan.txt', 'r')
# data = f.read()
# print data

#while True:
    #time.sleep(5)
    # print('suma: ' + str(len(balisa)+len(zwrotnica)+len(semafor)))
    #break
