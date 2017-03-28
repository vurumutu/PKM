#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Train:

    def __init__(self):                             #i - numer pociagu
        self.t_x = [0, 50, 100, 150, 200, 250]      #t_x - pozycja pociagu
        self.t_l = [73, 73, 34, 34, 16, 16]         #t_l - dlugosc pociagu
        self.t_v = [0, 0, 0, 0, 0, 0]               #t_v - predkosc pociagu

    def setValue(self, x, i):
        self.t_x[i-1] = x

    def getValue(self, i):
        return self.t_x[i-1]

    def getLength(self, i):
        return self.t_l[i-1]

    def setSpeed(self, v, i):
        self.t_v[i-1] = v

    def getSpeed(self,i):
        return self.t_v[i-1]