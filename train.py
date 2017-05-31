#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Train:

    def __init__(self, x, x_init, number, kalman_train, lines, length = 30, dual = -1):                             #i - numer pociagu
        self.x = x  #pozycja pociągu
        self.x_init = x_init    #pozycja pociągu początkowa
        self.number = number
        self.kalman_train = kalman_train
        self.lines = lines      #linie na których jest rysowany pociag
        self.length = length    #dlugosc pociagu
        self.color = Qt.darkGreen
        self.dual = dual    #wartość mówiąca w jaki sposób ma być rysowany pociąg
                            # -1 podwojnie po lewej
                            # -2 podwojnie po prawej
                            # 1 gorna lina
                            # 2 dolna linia
        self.flag_up = False # zmienna informuje czy pociąg ostatnio był umieszczony
                        # False - dol (down)
                        # True - góra (up)

        self.reverse = False # zmienna informuje czy pociąg jedzie do tyłu

        self.number_obj_in_line0 = len(self.lines[0].map_object)
        self.num_switch1_in_line0 = self.lines[0].get_numobj_switch(0)
        self.num_switch2_in_line0 = self.lines[0].get_numobj_switch(1)

        self.number_obj_in_line1 = len(self.lines[1].map_object)
        self.num_switch1_in_line1 = self.lines[1].get_numobj_switch(0)
        self.num_switch2_in_line1 = self.lines[1].get_numobj_switch(1)

        lenToSwitch2line0 = self.lines[0].get_x_fromobj(self.num_switch2_in_line0)
        lenToSwitch2line1 = self.lines[1].get_x_fromobj(self.num_switch2_in_line1)
        self.diff = lenToSwitch2line0 - lenToSwitch2line1

    def setPosition(self, x):
        self.x = x

    def setPositionInit(self, x_init):
        self.x_init = x_init

    def setDual(self, dual):
        self.dual = dual

    def setLength(self, length):
        self.length = length

    def setUp(self, flag_up):
        self.flag_up = flag_up

    def setColor(self, color):
        self.color = color

    def setReverse(self, reverse):
        self.reverse = reverse

    def getLength(self):    #z dlugosciami jest tak samo
        return self.length

    def negReverse(self):
        self.reverse = not self.reverse
        #self.setPositionInit(self.x)

    def update_position(self):
        kalman_position = self.kalman_train.get_position()#self.kalman_train
        lenToSwitch2line0 = self.lines[0].get_x_fromobj(self.num_switch2_in_line0)
        lenToSwitch2line1 = self.lines[1].get_x_fromobj(self.num_switch2_in_line1)
        if not self.reverse:
            self.x = self.x_init + kalman_position
        else:
            self.x = self.x_init - kalman_position

        if self.dual == -1:
            if self.x >= self.lines[0].get_x_fromobj(self.num_switch1_in_line0):
                if self.lines[0].railswitch[0].status:
                    self.dual = 1
                else:
                    self.dual = 2

        elif self.dual == -2:
            if self.flag_up:
                test = lenToSwitch2line0
            else:
                test = lenToSwitch2line1
            if self.x <= test + self.lines[0].railswitch[1].length:
                if self.lines[0].railswitch[1].status:
                    self.dual = 1
                else:
                    self.dual = 2

        elif self.dual == 1:
            self.flag_up = True
            if self.x >= (lenToSwitch2line0 + self.lines[0].railswitch[1].length):
                self.dual = -2
            elif self.x <= self.lines[0].get_x_fromobj(self.num_switch1_in_line0):
                self.dual = -1

        elif self.dual == 2:
            self.flag_up = False
            if self.x >= (lenToSwitch2line0 + self.lines[1].railswitch[1].length):
                self.dual = -2
            elif self.x <= self.lines[1].get_x_fromobj(self.num_switch1_in_line1):
                self.dual = -1

    def draw(self, q_window):
        if self.dual == -1:
            # konwersja poleozenia x na polozenia na mapie
            x1 = self.lines[0].x + self.x
            x2 = self.lines[1].x + self.x
            # rysowanie 2 pociagów
            self.draw_one_train(q_window, x1, self.lines[0].y)
            self.draw_one_train(q_window, x2, self.lines[1].y)

        elif self.dual == -2:
            # konwersja poleozenia x na polozenia na mapie
            if self.flag_up:
                x1 = self.lines[0].x + self.x
                x2 = self.lines[1].x + self.x - self.diff
            else:
                x1 = self.lines[0].x + self.x + self.diff
                x2 = self.lines[1].x + self.x
            # rysowanie 2 pociagów
            self.draw_one_train(q_window, x1, self.lines[0].y)
            self.draw_one_train(q_window, x2, self.lines[1].y)

        elif self.dual == 1:
            # konwersja poleozenia x na polozenia na mapie
            x = self.lines[0].x + self.x
            # rysowanie pociagu
            self.draw_one_train(q_window, x, self.lines[0].y)

        elif self.dual == 2:
            # konwersja poleozenia x na polozenia na mapie
            x = self.lines[1].x + self.x
            # rysowanie pociagu
            self.draw_one_train(q_window, x, self.lines[1].y)


    def draw_one_train(self, q_window, x0 ,y0):
        paint = QPainter()
        paint.begin(q_window)
        paint.setRenderHint(QPainter.Antialiasing)

        width_sc = round(self.length * q_window.scale)
        height_sc = round(10 * q_window.scale)

        st_dim = QRect((x0 - width_sc/2)*q_window.scale, y0 - height_sc/2, width_sc, height_sc)


        paint.setPen(Qt.black)
        paint.setBrush(self.color)
        paint.drawRect(st_dim)
        paint.setPen(Qt.white)
        paint.setFont(QFont('Arial', round(7 * q_window.scale)))
        paint.drawText(st_dim, Qt.AlignCenter, str(self.number))
        paint.end()