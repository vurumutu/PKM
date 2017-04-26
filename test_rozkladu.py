# -*- coding: utf-8 -*-

from xpressnet import Client
from xpressnet import Train
from time import sleep
import sys

import numpy as np
from PyQt4 import QtGui, QtCore

TCP_IP = '192.168.210.200'
TCP_PORT = 5550

class Test(QtGui.QMainWindow):
    def __init__(self):
        super(Test, self).__init__()
        self.setGeometry(50, 50, 100, 100)
        self.setWindowTitle("TEST ROZKLADU")
        self.show()

        self.lista_pociagow = [6,5,1,2]

        self.per = 3000  # postoj na peronie
        self.w_s = 3000  # odcinek wrzeszcz - strzyza
        self.s_k = 2500  # odcinek strzyza - kielpinek
        self.w_o = 28000   # odcinek wrzeszcz - osowa
        self.o_w = 24820
        self.o_o1 = 3000  # zmiana toru na stacji osowa
        self.o_o2 = 2000
        self.o_o3 = 3200

        self.timeTable = np.array([
            [self.per, self.w_o, self.o_o2, self.o_o3, self.per, self.o_w],  # wrzeszcz -> osowa -> wrzeszcz
            [self.per, self.w_o, self.per, self.w_o, self.per, self.o_o1],  # osowa -> wrzeszcz -> osowa
            [self.per, self.w_s, self.per, self.s_k, self.per, self.s_k, self.per, self.w_s],  # wrzeszcz -> kielpinek -> wrzeszcz
            [self.per, self.s_k, self.per, self.w_s, self.per, self.w_s, self.per, self.s_k]  # kielpinek -> wrzeszcz -> kielpinek
        ])  # jadac z osowy do wrzeszcza przedluzamy postoj, zeby sie wyminac zdazyly

        self.jedz_table = np.array([
            [0, 1, 0, -1, 0, -1],  # 0 - stoj
            [0, -1, 0, 1, 0, 2],  # 1 - jedz do przodu
            [0, 1, 0, 1, 0, -1, 0, -1],  # -1 - jedz do tylu
            [0, -1, 0, -1, 0, 1, 0, 1]  # 2 - zawracanka na osowej
        ])

        self.licznik = [0, 0, 0, 0]
        self.timers = []
        self.jazda = []
        for i in range(4):
            new_timer = QtCore.QBasicTimer()
            new_timer.start(self.timeTable[i][self.licznik[i]], self)
            self.timers.append(new_timer)
            self.jazda.append(self.jedz_table[i][self.licznik[i]])

        self.connect_test()

    #def __del__(self):
    #    self.client.disconnect()

    def updateTimers(self, i):
        if self.licznik[i] < len(self.timeTable[i])-1:
            self.licznik[i] = self.licznik[i] + 1
        else:
            self.licznik[i] = 0
        new_timer = QtCore.QBasicTimer()
        new_timer.start(self.timeTable[i][self.licznik[i]], self)
        self.timers[i] = new_timer
        self.jazda[i] = self.jedz_table[i][self.licznik[i]]


    def timerEvent(self, event):
        for i in range(4):
            if i == 0:
                if event.timerId() == self.timers[i].timerId():
                    self.updateTimers(i)
                    train = Train(self.lista_pociagow[i])
                    if self.jazda[i] == 1:
                        msg = train.move(100, self.direction["Backward"])
                    elif self.jazda[i] == 0:
                        msg = train.move(0)
                    elif self.jazda[i] == -1:
                        msg = train.move(100, self.direction["Forward"])
                    elif self.jazda[i] == 2:
                        msg = train.move(0)
                    self.client.send(msg)

    def connect_test(self):

        self.direction = {"Forward": 1, "Backward": 0}
        self.client = Client()
        self.client.connect(TCP_IP, TCP_PORT)

def main():

    app = QtGui.QApplication(sys.argv)
    test = Test()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
