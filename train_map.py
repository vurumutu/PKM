#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from enum import Enum
import train

class Turn(Enum):
    left = 0
    right = 1


class Railmap(QWidget):

    def __init__(self, x, y, height, width, kalman_trains, q_window):
        super(Railmap, self).__init__(q_window)
        #inicjalizacja wielkości mapy
        self.setGeometry(x, y, width, height)
        self.setMinimumSize(1000, 450)

        #dodanie klasy train do mapy
        self.kalman_trains = kalman_trains

        self.d_QWindow = q_window
        self.scale = 1

        img_rail = self.load_image("Pictures/rail.png")
        img_railcomb = self.load_image("Pictures/rail_comb.png")
        img_sation = self.load_image("Pictures/railsation.png")

        self.images = [img_rail, img_railcomb, img_sation]

        self.switch1 = Railswitch(q_window, 0, 0, 10, 6)
        self.switch2 = Railswitch(q_window, 0, 0, 10, 6, 1, Turn.right)
        self.switch3 = Railswitch(q_window, 0, 0, 18.5, 6)
        self.switch4 = Railswitch(q_window, 0, 0, 23, 6, 1, Turn.right)

        # utworzenie lini OSOWA -> WRZESZCZ
        self.line1 = Railline(15, 85)
        self.line1.set_stations([100, "Wrzeszcz", 100, "Osowa"])  # lista rzeczywistych odcinkow torow w cm #miedzy stacjami jest chyba 767
        self.line1.set_leng_rails([25, 5, 90, 50, 20, 20, 20, 20, 20, 300, 197, 10, 5, 40])  # lista stacji (dlugosc peronu, nazwa stacji)
        self.line1.set_map_object([1, 4, 2, 4, 3, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1, 0, 3, 4, 2, 4])  # mapy obiektow - wektor
        self.line1.set_railswitch([self.switch1, self.switch2])

        # utworzenie lini WRZESZCZ -> OSOWA
        self.line2 = Railline(15, 155)
        self.line2.set_stations([100, "Wrzeszcz", 100, "Osowa"])  # lista rzeczywistych odcinkow torow w cm
        self.line2.set_leng_rails([25, 5, 90, 450, 200, 10, 5, 40])  # lista stacji (dlugosc peronu, nazwa stacji)
        self.line2.set_map_object([1, 4, 2, 4, 3, 0, 2, 0, 2, 0, 1, 0, 3, 4, 2, 4])  # mapy obiektow - wektor
        self.line2.set_railswitch([self.switch1, self.switch2])
        self.line2.set_negation(True)

        # utworzenie lini WRZESZCZ -> KIEŁPINEK
        self.line3 = Railline(15, 225)
        self.line3.set_stations([100, "Wrzeszcz", 106, "Strzyza", 101.5, "Kielpinek"])  # lista rzeczywistych odcinkow torow w cm #
        self.line3.set_leng_rails([80, 100, 5, 6.5, 249, 6, 37, 523, 234, 21.5, 10.5, 12.5])  # lista stacji (dlugosc peronu, nazwa stacji)
        self.line3.set_map_object([1, 2, 4, 2, 4, 2, 4, 3, 0, 2, 0, 2, 0, 1, 0, 2, 0, 2, 0, 3, 4, 2, 4, 1, 4])  # mapy obiektow - wektor
        self.line3.set_railswitch([self.switch3, self.switch4])

        # utworzenie lini KIEŁPINEK -> WRZESZCZ
        self.line4 = Railline(15, 295)
        self.line4.set_stations([100, "Wrzeszcz", 106, "Strzyza", 101.5, "Kielpinek"])  # lista rzeczywistych odcinkow torow w cm
        self.line4.set_leng_rails([80, 100, 5, 6.5, 243, 6, 37, 503, 235, 21.5, 10.5, 12.5])  # lista stacji (dlugosc peronu, nazwa stacji)
        self.line4.set_map_object([1, 2, 4, 2, 4, 2, 4, 3, 0, 2, 0, 2, 0, 1, 0, 2, 0, 2, 0, 3, 4, 2, 4, 1, 4])  # mapy obiektow - wektor
        self.line4.set_railswitch([self.switch3, self.switch4])
        self.line4.set_negation(True)
        self.setscale()

        # słownik z przypisanymi pociągami do danych linii
        self.trainsLine = {0 : [self.line3, self.line4], 1 : [self.line3, self.line4],
                           2 : [self.line1, self.line2], 3 : [self.line1, self.line2]}

        # dlugosci pociagow
        self.trains_length = [73, 73, 16, 16]
        self.sym_kalman = 0

        # inicjalizacja pociągów
        x1 = self.line3.get_length_fromobj(0) - self.trains_length[0]/2
        self.train1 = train.Train(0, x1, 1, self.kalman_trains[0], self.trainsLine[0], self.trains_length[0])
        self.train1.setColor(Qt.darkGreen)
        self.train1.setReverse(False)

        x2 = self.line3.get_x_fromobj(len(self.line3.map_object) - 2) + self.trains_length[1]/2
        self.train2 = train.Train(0, x2, 2, self.kalman_trains[1], self.trainsLine[1], self.trains_length[1], -2)
        self.train2.setColor(Qt.darkBlue)
        self.train2.setUp(True)
        self.train2.setReverse(True)

        x3 = self.line1.get_length_fromobj(0) - self.trains_length[2]/2
        self.train3 = train.Train(0, x3, 5, self.kalman_trains[2], self.trainsLine[2], self.trains_length[2])
        self.train3.setColor(Qt.darkRed)
        self.train3.setReverse(False)

        x4 = self.line1.get_x_fromobj(len(self.line1.map_object) - 6) + self.trains_length[3]/2
        self.train4 = train.Train(0, x4, 6, self.kalman_trains[3], self.trainsLine[3], self.trains_length[3], 1)
        self.train4.setColor(Qt.darkMagenta)
        self.train4.setUp(True)
        self.train4.setReverse(True)

    # liczenie skali proporcjonalnej do rzeczywistych wymiarow
    def setscale(self):
        margin = 15
        self.scale = (self.width() - 2 * margin + 0.) / (self.line3.leng_line + 0.)
        self.update_scales()

    def update_scales(self):
        self.line1.set_scale(self.scale)
        self.line2.set_scale(self.scale)
        self.line3.set_scale(self.scale)
        self.line4.set_scale(self.scale)

        self.switch1.set_scale(self.scale)
        self.switch2.set_scale(self.scale)
        self.switch3.set_scale(self.scale)
        self.switch4.set_scale(self.scale)

    def load_image(self, path):
        try:
            image = QImage()
            image.load(path)
            if image.isNull():
                QMessageBox.critical(self.d_QWindow, 'Blad', "Wystapil problem podczas wczytania pliku", QMessageBox.Ok)
                raise Exception('Problem z wczytaniem pliku')
            else:
                return image

        except IOError:
            pass

        return None

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)

        paint.setBrush(Qt.white)
        clip_rect = QRect(0, 0, self.width(), self.height())
        paint.drawRect(clip_rect)

        paint.setPen(Qt.black)
        paint.setFont(QFont('Arial', 10))
        paint.drawText(10, 50, "1. Kierunek OSOWA -> WRZESZCZ")
        paint.drawText(10, 120, "2. Kierunek WRZESZCZ -> OSOWA")
        paint.drawText(10, 190, "3. Kierunek WRZESZCZ -> KIELPINEK")
        paint.drawText(10, 260, "4. Kierunek KIELPINEK -> WRZESZCZ")

        self.draw_legend(20, 320, paint)

        paint.end()

        # rysowanie lini kolejowych
        self.line1.draw_line(self, self.images)
        self.line2.draw_line(self, self.images)
        self.line3.draw_line(self, self.images)
        self.line4.draw_line(self, self.images)

        #self.train1.kalman_train = self.sym_kalman
        #self.train2.kalman_train = self.sym_kalman
        #self.train3.kalman_train = self.sym_kalman
        #self.train4.kalman_train = self.sym_kalman

        # aktualizacja pozycji pociągów na podstawie modelu z kalmana
        self.train1.update_position()
        self.train2.update_position()
        self.train3.update_position()
        self.train4.update_position()

        # rysoanie pociągów
        self.train1.draw(self)
        self.train2.draw(self)
        self.train3.draw(self)
        self.train4.draw(self)


    def draw_legend(self, x, y, paint=QPainter()):
        paint.setBrush(Qt.white)
        legend = QRect(x, y, 250, 120)
        paint.drawRect(legend)

        paint.setPen(Qt.black)
        paint.setFont(QFont('Arial', 11))
        paint.drawText(x+10, y+20, "Opis mapy:")

        leg_line = Railline()
        leg_line.set_scale(1)
        leg_line.draw_station(x+10, y+35, 80, 20, "", self.images[2], paint)
        leg_line.draw_railswitch(x+45, y+52, 10, 6, paint)
        leg_line.draw_sensor(x+50, y+68, 4, paint)
        leg_line.draw_rail(x+10, y+85, 80, self.images[0], paint)
        leg_line.draw_rail(x+10, y+105, 80, self.images[1], paint)

        paint.setPen(Qt.black)
        paint.setFont(QFont('Arial', 9))
        paint.drawText(x + 100, y + 40, "stacja kolejowa")
        paint.drawText(x + 100, y + 57, "zwrotnica")
        paint.drawText(x + 100, y + 73, "czujnik")
        paint.drawText(x + 100, y + 90, "odcinek torow")
        paint.drawText(x + 100, y + 110, "wspolny odcinek torow")



class Railline:
    def __init__(self, x=0, y=0, leng_rails=None, stations=None, map_object=None, railswitch=None, scale=1, neg = False):
        self.x = x
        self.y = y
        self.scale = scale
        self.neg = neg

        # w przypadku braku wartosci ustaw jako pusta liste
        if leng_rails is None: leng_rails = []
        if stations is None: stations = []
        if map_object is None: map_object = []
        if railswitch is None: railswitch = []

        self.leng_rails = leng_rails
        self.stations = stations
        self.map_object = map_object
        self.railswitch = railswitch

        # liczenie dlugosci calej lini kolejowej
        self.leng_line = self.count_leng_line()

    def count_leng_line(self):
        #if type(self.leng_railswitch) == int:
            #n = self.map_object.count(3)
            #leng_line = sum(self.leng_rails) + sum(self.stations[::2]) + n * self.leng_railswitch
        #else:
        leng_switch = []
        for switch in self.railswitch:
            leng_switch.append(switch.length)

        leng_line = sum(self.leng_rails) + sum(self.stations[::2]) + sum(leng_switch)

        return leng_line

    # -----------------------------
    # funkcje do pobierania danych

    # funkcja pobierająca długość DO danego obiektu
    def get_x_fromobj(self, num_obj):
        sum_leng = 0

        stations = 0
        rails = 0
        switches = 0
        for i in range(len(self.map_object)):
            obj = self.map_object[i]
            if i == num_obj:
                return sum_leng
            elif obj == 4 or obj == 0:
                sum_leng += self.leng_rails[rails]
                rails += 1
            elif obj == 1:
                sum_leng += self.stations[stations]
                stations += 2
            elif obj == 3:
                sum_leng += self.railswitch[switches].length
                switches += 1
        return sum_leng


    # funkcja pobierająca długość danego obiektu
    def get_length_fromobj(self, num_obj):
        stations = 0
        rails = 0
        switches = 0
        for i in range(len(self.map_object)):
            obj = self.map_object[i]
            if i == num_obj:
                if obj == 4 or obj == 0:
                    return self.leng_rails[rails]
                elif obj == 1:
                    return self.stations[stations]
                elif obj == 3:
                    return self.railswitch[switches].length
                else:
                    return 0
            if obj == 4 or obj == 0:
                rails += 1
            elif obj == 1:
                stations += 1
            elif obj == 3:
                switches += 1
        return 0

    # funkcja zwracająca numer w mapie obiektów danej zwrotnicy
    def get_numobj_switch(self, switch):
        count_switch = 0
        for i in range(len(self.map_object)):
            if self.map_object[i] == 3:
                if count_switch == switch:
                    return i
                else:
                    count_switch += 1
        return -1


    # --------------------------
    # funkcje wypelniajace listy
    def set_stations(self, stations):
        self.stations = stations
        self.leng_line = self.count_leng_line()

    def set_leng_rails(self, leng_rails):
        self.leng_rails = leng_rails
        self.leng_line = self.count_leng_line()

    def set_map_object(self, map_object):
        self.map_object = map_object
        self.leng_line = self.count_leng_line()

    def set_railswitch(self, railswitch):
        self.railswitch = railswitch
        self.leng_line = self.count_leng_line()

    def set_negation(self, neg):
        self.neg = neg
    # --------------------------
    # funkcje wstawiajace wartosc do listy
    # domyslnie wstawia na koniec listy
    def insert_station(self, leng, name, index=None):
        if index is None: index = len(self.stations)
        self.stations.insert(index, leng)
        self.stations.insert(index, name)

    def insert_leng_rails(self, leng, index=None):
        if index is None: index = len(self.leng_rails)
        self.leng_rails.insert(index, leng)

    def insert_map_object(self, obj, index=None):
        if index is None: index = len(self.map_object)
        if obj in [0, 1, 2, 3]:
            self.map_object.insert(index, obj)

    # ---end---

    # rysowanie calej lini kolejowej
    def draw_line(self, q_window, images = None):
        # tworzenie kopi wektorow
        cstations = self.stations[:]
        crail_leng = self.leng_rails[:]
        cobjects = self.map_object[:]
        cswitchs = self.railswitch[:]

        img_rail = images[0]
        img_railcomb = images[1]
        img_sation = images[2]

        # kopie pozycji x i y
        x = self.x
        y = self.y

        paint = QPainter()
        paint.begin(q_window)
        paint.setRenderHint(QPainter.Antialiasing)

        self.draw_endrail(x, y, paint)

        # -----------------------
        # rysowanie obiektow mapy
        # 0 - odcinek torow
        # 1 - stacja
        # 2 - czujnik
        # 3 - zwrotnica
        # 4 - wspólny odcinek torow
        # -----------------------
        for obj in cobjects:
            if obj == 0:
                leng = crail_leng[0]
                crail_leng.pop(0)
                x, y = self.draw_rail(x, y, leng, img_rail, paint)
            elif obj == 1:
                leng = cstations[0]
                cstations.pop(0)
                name = cstations[0]
                cstations.pop(0)
                x, y = self.draw_station(x, y, leng, 20, name, img_sation, paint)
            elif obj == 2:
                self.draw_sensor(x, y, 3, paint)
            elif obj == 3:
                switch = cswitchs[0]
                cswitchs.pop(0)
                self.draw_rail(x, y, switch.length, img_rail, paint)
                x, y = switch.draw_railswitch(x, y, paint, self.neg)
            elif obj == 4:
                leng = crail_leng[0]
                crail_leng.pop(0)
                x, y = self.draw_rail(x, y, leng, img_railcomb, paint)

        self.draw_endrail(x, y, paint)

        paint.setBrush(Qt.NoBrush)
        #self.draw_train(x_t, y, paint, train_length)

        paint.end()

    # rysowanie stacji kolejowej
    def draw_station(self, x0, y0, leng, height, name="", img=QImage(), paint=QPainter()):
        width_sc = round(self.scale * leng)
        height_sc = round(self.scale * height)
        x1 = x0 + width_sc
        y1 = y0
        dy_text = round(self.scale * 20)

        st_dim = QRect(x0, y0 - height_sc / 2, width_sc, height_sc)
        text_dim = QRect(x0, y0 - height_sc / 2 - dy_text, width_sc, height_sc + 5)

        img = img.scaled(width_sc, height_sc)
        pixmap = QPixmap().fromImage(img)
        paint.drawPixmap(st_dim, pixmap)
        paint.setPen(Qt.black)
        paint.setFont(QFont('Arial', round(10 * self.scale)))
        paint.drawText(text_dim, Qt.AlignCenter, name)

        return x1, y1

    # rysowanie odcinkow torow( leng - dlugosc odcinka torow)
    def draw_rail(self, x0, y0, leng, img = QImage(), paint=QPainter()):
        len_sc = round(self.scale * leng)
        x1 = x0 + len_sc
        y1 = y0

        img = img.scaled(round(float(self.scale * 50)), round(float(self.scale * 35)))
        pixmap = QPixmap().fromImage(img)

        n_pieces = int(len_sc/pixmap.width())
        carry = len_sc - n_pieces*pixmap.width()
        x = x0
        y = y0 - round(pixmap.height()/2)
        for i in range(n_pieces):
            paint.drawPixmap(x, y, pixmap)
            x += pixmap.width()
        if carry > 0.0:
            fragpixmap = pixmap.copy(QRect(0, 0, carry, pixmap.height()))
            paint.drawPixmap(x, y, fragpixmap)

        return x1, y1

    # rysowanie czujnikow
    def draw_sensor(self, x0, y0, R, paint=QPainter()):
        paint.setBrush(Qt.red)
        R_sc = round(self.scale * R)
        d = R_sc*2
        paint.setPen(Qt.black)
        paint.drawEllipse(x0-R_sc, y0-R_sc, d, d)

    # rysowanie zwrotnic
    def draw_railswitch(self, x0, y0, leng, height, paint=QPainter()):
        width_sc = round(self.scale * leng)
        height_sc = round(self.scale * height)
        x1 = x0 + width_sc
        y1 = y0

        switch = QPolygonF()
        switch.append(QPointF(x0, y0 + height_sc))
        switch.append(QPointF(x0, y0 - height_sc))
        switch.append(QPointF(x1, y1))
        paint.setBrush(Qt.green)
        paint.drawPolygon(switch)

        return x1, y1

    # rysowanie końca linni
    def draw_endrail(self, x0, y0, paint=QPainter()):
        leng = round(10.0*self.scale)

        paint.setPen(QPen(Qt.black, round(3*self.scale)))
        paint.drawLine(x0, y0-leng, x0, y0+leng)

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_scale(self, scale):
        self.scale = scale


class Railswitch(QWidget):
    number = 0

    def __init__(self, parent=None, x=0, y=0, length=10.0, height=5, scale=1, turn=Turn.left):
        super(Railswitch, self).__init__(parent)
        self.qwindow = parent
        self.length = length
        self.height = height
        self.scale = scale
        self.turn = turn
        self.status = True
        self.double_switch = None

        self.length_sc = round(self.scale * self.length)
        self.height_sc = round(self.scale * self.height)
        self._x = x
        self._y = y

        #self.setMinimumSize(1, 1)
        self.setGeometry(x, y-self.height_sc, self.length_sc+2, 2*self.height_sc+10)
        #self.setVisible(True)
        Railswitch.number += 1
        self._index = self.number

    def connect_switch(self, switch):
        self.double_switch = switch

    def set_turn(self,turn):
        self.turn = turn

    def set_status(self, status=True):
        if type(self.status) == bool:
            self.status = status

    def neg_status(self):
        self.status = not self.status

    def set_scale(self, scale):
        self.scale = scale
        self.length_sc = round(self.scale * self.length)
        self.height_sc = round(self.scale * self.height)

    # wywolanie funkcji w przypadku nacisnięcia na zwrotnice
    def mousePressEvent(self, event):
        #super(Railswitch, self).mousePressEvent(event)
        self.repaint()
        print("test")
        self.neg_status()

    # event do rysowania zwrotnicy
    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        #self.draw_railswitch(0,0,qp)
        qp.end()

    @staticmethod
    def xor(a, b):
        return (a and not b) or (not a and b)

    # rysowanie zwrotnicy
    def draw_railswitch(self, x0=0, y0=0, paint=QPainter(), neg = False):
        x1 = x0 + self.length_sc
        y1 = y0

        #uaktualnienie pozycji
        self._x = x0
        self._y = y0

        switch = QPolygonF()
        if self.turn == Turn.right:
            switch.append(QPointF(x0, y0 + self.height_sc))
            switch.append(QPointF(x0, y0 - self.height_sc))
            switch.append(QPointF(x1, y1))
        else:
            switch.append(QPointF(x1, y1 + self.height_sc))
            switch.append(QPointF(x1, y1 - self.height_sc))
            switch.append(QPointF(x0, y0))

        str_index = "id: " + str(self._index)
        str_status = "1"
        color_status = Qt.green

        # parametr neg okresla czy zwrotnica ma mieć zanegowany status
        if not self.xor(self.status, neg):
            str_status = "0"
            color_status = Qt.red

        dy_text = round(self.scale * 12)
        text_dim1 = QRect(x0, y0 - self.height_sc - dy_text, self.length_sc, self.height_sc * 2 + 2)
        text_dim2 = QRect(x0 - self.length_sc, y0 + self.height_sc + 2, self.length_sc*3, self.height_sc * 2 + 2)

        paint.setPen(Qt.black)
        paint.setFont(QFont('Arial', round(10 * self.scale)))
        paint.drawText(text_dim1, Qt.AlignCenter, str_status)
        paint.setFont(QFont('Arial', round(8 * self.scale)))
        paint.drawText(text_dim2, Qt.AlignCenter, str_index)

        paint.setBrush(color_status)
        paint.drawPolygon(switch)

        return x1, y1