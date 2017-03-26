#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Train:

    def __init__(self, x, i):
        self.x_t = [0, 100, 200, 50, 150, 250]      #x_t - pozycja pociagu
        self.x_t[i] = x                             #i - numer pociagu
        self.t_l = [15, 35, 70, 15, 35, 70]         #t_l - dlugosc pociagu

    def setValue(self, x, i):
        self.x_t[i] = x

    def getValue(self, i):
        return self.x_t[i]

    def getLength(self, i):
        return self.t_l[i]