import numpy as np
from PyQt4 import QtGui, QtCore
#from CAN import *

class TimeTable:
    def __init__(self, q_window):
        self.per = 1500    #postoj na peronie
        self.w_s = 3000    #odcinek wrzeszcz - strzyza
        self.s_k = 2500    #odcinek strzyza - kielpinek
        self.w_o = 2500    #odcinek wrzeszcz - osowa
        self.o_o = 1500    #zmiana toru na stacji osowa

        self.timeTable = np.array([
            [self.w_o, self.per, self.o_o, self.per],   #wrzeszcz -> osowa
            [self.w_o, 2*self.per + self.o_o],  #osowa -> wrzeszcz
            [self.w_s, self.per, self.s_k, self.per],  #wrzeszcz -> kielpinek
            [self.s_k, self.per, self.w_s, self.per]   #kielpinek -> wrzeszcz
        ]) #jadac z osowy do wrzeszcza przedluzamy postoj, zeby sie wyminac zdazyly

        self.positionTable = np.array([
            [430, 867, 967, 867],
            [430, 0],
            [150, 325, 700, 1158],
            [700, 325, 150, 0]
        ])
        self.licznik = [0, 0, 0, 0]
        self.q_window = q_window
        self.timers = []
        for i in range(4):
            new_timer = QtCore.QBasicTimer()
            new_timer.start(self.timeTable[i][self.licznik[i]], self.q_window)
            self.timers.append(new_timer)

    def updateTimers(self, i):
        if self.licznik[i] < len(self.timeTable[i])-1:
            self.licznik[i] = self.licznik[i] + 1
        else:
            self.licznik[i] = 0
        new_timer = QtCore.QBasicTimer()
        #print self.licznik
        new_timer.start(self.timeTable[i][self.licznik[i]], self.q_window)
        self.timers[i] = new_timer






