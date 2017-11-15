#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from train_map import Railline

class Train:

    def __init__(self, x, x_init, number, kalman_train, lines, length = 30, dual = -1, target = 1, priority = 1, track = 1):                             #i - numer pociagu
        self.x = x  #pozycja pociągu
        self.x_init = x_init    #pozycja pociągu początkowa
        self.number = number
        self.kalman_train = kalman_train
        self.lines = lines      #linie na których jest rysowany pociag
        self.length = length    #dlugosc pociagu
        self.color = Qt.darkGreen
        self.target = target    #cel podrozy, mozna by oznaczac, jako x na kokretnym torze, przy jakim pociag ma sie zatrzymac
        self.priority = priority    #jak by mialy watpliwosci, ktory ustepuje, moze po prostu na poczatku taki prior, jaki nr pociagu
        self.track = track      #musimy teraz juz wiedziec, ktory pociag jest na ktorym torze, zeby mogly sie mijac
        self.dual = dual    #wartość mówiąca w jaki sposób ma być rysowany pociąg
                            # -1 podwojnie po lewej
                            # -2 podwojnie po prawej
                            # 1 gorna lina
                            # 2 dolna linia
        self.flag_up = False # zmienna informuje czy pociąg ostatnio był umieszczony
                        # False - dol (down)
                        # True - góra (up)

        self.reverse = False # zmienna informuje czy pociąg jedzie do tyłu

        self.actual_track_section_l0 = -1 # numer obiektu na którym znajduje się pociag dla lini0
        self.actual_track_section_l1 = -1 # numer obiektu na którym znajduje się pociag dla lini1
        # (-1 oznacza że nie znajduje się na tej lini)

        self.is_track_section_changed = False

        self.number_obj_in_line0 = len(self.lines[0].map_object)
        self.num_switch1_in_line0 = self.lines[0].get_numobj_switch(0)
        self.num_switch2_in_line0 = self.lines[0].get_numobj_switch(1)

        self.number_obj_in_line1 = len(self.lines[1].map_object)
        self.num_switch1_in_line1 = self.lines[1].get_numobj_switch(0)
        self.num_switch2_in_line1 = self.lines[1].get_numobj_switch(1)

        lenToSwitch2line0 = self.lines[0].get_x_fromobj(self.num_switch2_in_line0)
        lenToSwitch2line1 = self.lines[1].get_x_fromobj(self.num_switch2_in_line1)
        self.diff = lenToSwitch2line0 - lenToSwitch2line1

    def setTarget(self, target):
        self.target = target

    def getTarget(self):
        return self.target

    def getPriority(self):
        return self.priority

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
        kalman_position = self.kalman_train#self.kalman_train.get_position()
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

        self.prev_track_section_l0 = self.actual_track_section_l0
        self.prev_track_section_l1 = self.actual_track_section_l1

        self.check_track_section()

        changetrack0 = not self.prev_track_section_l0 == self.actual_track_section_l0
        changetrack1 = not self.prev_track_section_l1 == self.actual_track_section_l1

        if (changetrack0 or changetrack1):
            if not self.is_track_section_changed:
                self.is_track_section_changed = True



    def messageChangeTrack(self, q_window):
        if self.is_track_section_changed:
            title = 'Zmiana odcinka dla pociagu ' + str(self.number)
            message1 = "Dlugosc poprzedniego odcinka trasy 0: " + str(
                self.lines[0].get_length_fromobj(self.prev_track_section_l0)) + "                                +\n"
            message2 = "Dlugosc akualnego odcinka trasy 0: " + str(
                self.lines[0].get_length_fromobj(self.actual_track_section_l0)) + "\n"
            message3 = "Dlugosc poprzedniego odcinka trasy 1: " + str(
                self.lines[1].get_length_fromobj(self.prev_track_section_l1)) + "\n"
            message4 = "Dlugosc akualnego odcinka trasy 1: " + str(
                self.lines[1].get_length_fromobj(self.actual_track_section_l1))
            QMessageBox.information(q_window, title, message1 + message2 + message3 + message4, QMessageBox.Ok)
            self.is_track_section_changed = False


    def draw(self, q_window):
        self.draw_section(q_window)

        if self.dual == -1:
            # konwersja poleozenia x na polozenia na mapie
            x1 = self.lines[0].x + self.x*q_window.scale
            x2 = self.lines[1].x + self.x*q_window.scale
            # rysowanie 2 pociagów
            self.draw_one_train(q_window, x1, self.lines[0].y)
            self.draw_one_train(q_window, x2, self.lines[1].y)

        elif self.dual == -2:
            # konwersja poleozenia x na polozenia na mapie
            if self.flag_up:
                x1 = self.lines[0].x + self.x*q_window.scale
                x2 = self.lines[1].x + (self.x - self.diff)*q_window.scale
            else:
                x1 = self.lines[0].x + (self.x + self.diff)*q_window.scale
                x2 = self.lines[1].x + self.x*q_window.scale
            # rysowanie 2 pociagów
            self.draw_one_train(q_window, x1, self.lines[0].y)
            self.draw_one_train(q_window, x2, self.lines[1].y)

        elif self.dual == 1:
            # konwersja poleozenia x na polozenia na mapie
            x = self.lines[0].x + self.x*q_window.scale
            # rysowanie pociagu
            self.draw_one_train(q_window, x, self.lines[0].y)

        elif self.dual == 2:
            # konwersja poleozenia x na polozenia na mapie
            x = self.lines[1].x + self.x*q_window.scale
            # rysowanie pociagu
            self.draw_one_train(q_window, x, self.lines[1].y)


    def check_track_section(self):
        if self.dual == -1:
            self.actual_track_section_l0 = self.get_number_section(self.lines[0], self.x)
            self.actual_track_section_l1 = self.get_number_section(self.lines[1], self.x)

        elif self.dual == -2:
            if self.flag_up:
                x1 = self.x
                x2 = self.x - self.diff
            else:
                x1 = self.x + self.diff
                x2 = self.x

            self.actual_track_section_l0 = self.get_number_section(self.lines[0], x1)
            self.actual_track_section_l1 = self.get_number_section(self.lines[1], x2)

        elif self.dual == 1:
            self.actual_track_section_l0 = self.get_number_section(self.lines[0], self.x)
            self.actual_track_section_l1 = -1

        elif self.dual == 2:
            self.actual_track_section_l0 = -1
            self.actual_track_section_l1 = self.get_number_section(self.lines[1], self.x)


    def get_number_section(self, line, pos):
        for i in range(len(line.map_object)):
            if pos <= line.get_x_fromobj(i+1):
                return i
        return len(line.map_object) - 1


    def draw_section(self, q_window):
        paint = QPainter()
        paint.begin(q_window)
        paint.setRenderHint(QPainter.Antialiasing)

        if self.actual_track_section_l0 >= 0:
            x1 = self.lines[0].get_x_fromobj(self.actual_track_section_l0)
            x2 = x1 + self.lines[0].get_length_fromobj(self.actual_track_section_l0)
            pencil = QPen()
            pencil.setColor(self.color)
            pencil.setWidth(5)

            paint.setPen(pencil)
            paint.drawLine(x1 * q_window.scale + self.lines[0].x, self.lines[0].y,
                           x2 * q_window.scale + self.lines[0].x, self.lines[0].y)

        if self.actual_track_section_l1 >= 0:
            x1 = self.lines[1].get_x_fromobj(self.actual_track_section_l1)
            x2 = x1 + self.lines[1].get_length_fromobj(self.actual_track_section_l1)
            pencil = QPen()
            pencil.setColor(self.color)
            pencil.setWidth(5)

            paint.setPen(pencil)
            paint.drawLine(x1 * q_window.scale + self.lines[1].x, self.lines[1].y,
                           x2 * q_window.scale + self.lines[1].x, self.lines[1].y)

        paint.end()

    def draw_one_train(self, q_window, x0 ,y0):
        paint = QPainter()
        paint.begin(q_window)
        paint.setRenderHint(QPainter.Antialiasing)

        width_sc = round(self.length * q_window.scale)
        height_sc = round(10 * q_window.scale)

        st_dim = QRect((x0 - width_sc/2), y0 - height_sc/2, width_sc, height_sc)

        paint.setPen(Qt.black)
        paint.setBrush(self.color)
        paint.drawRect(st_dim)
        paint.setPen(Qt.white)
        paint.setFont(QFont('Arial', round(7 * q_window.scale)))
        paint.drawText(st_dim, Qt.AlignCenter, str(self.number))
        paint.end()