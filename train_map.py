from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Railmap:

    def __init__(self, x, y, height, width, q_window):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.d_QWindow = q_window
        self.scale = 1

        # utworzenie lini OLIWA -> WRZESZCZ
        self.line1 = Railline(10, 80)
        self.line1.set_stations([100, "Wrzeszcz", 100, "Oliwa"])  # lista rzeczywistych odcinkow torow w cm
        self.line1.set_leng_rails([25, 5, 90, 50, 20, 20, 20, 20, 20, 300, 200, 10, 5, 40])  # lista stacji (dlugosc peronu, nazwa stacji)
        self.line1.set_map_object([1, 0, 2, 0, 3, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 1, 0, 3, 0, 2, 0])  # mapy obiektow - wektor

        # utworzenie lini WRZESZCZ -> OLIWA
        self.line2 = Railline(10, 140)
        self.line2.set_stations([100, "Wrzeszcz", 100, "Oliwa"])  # lista rzeczywistych odcinkow torow w cm
        self.line2.set_leng_rails([25, 5, 90, 450, 200, 10, 5, 40])  # lista stacji (dlugosc peronu, nazwa stacji)
        self.line2.set_map_object([1, 0, 2, 0, 3, 0, 2, 0, 2, 0, 1, 0, 3, 0, 2, 0])  # mapy obiektow - wektor

        # utworzenie lini WRZESZCZ -> OSOWA
        self.line3 = Railline(10, 200)
        self.line3.set_stations([100, "Wrzeszcz", 100, "Strzyza", 100, "Osowa"])  # lista rzeczywistych odcinkow torow w cm
        self.line3.set_leng_rails([80, 100, 5, 135, 5, 35, 570, 245, 20, 10])  # lista stacji (dlugosc peronu, nazwa stacji)
        self.line3.set_map_object([1, 2, 0, 2, 0, 2, 0, 3, 0, 2, 0, 1, 0, 2, 0, 2, 0, 3, 0, 2, 0, 1])  # mapy obiektow - wektor
        self.line3.set_leng_railswitch([20, 10])
        self.setscale()

    # liczenie skali proporcjonalnej do rzeczywistych wymiarow
    def setscale(self):
        margin = 5
        self.scale = (self.width - 2 * margin + 0.) / (self.line3.leng_line + 0.)
        self.update_scales()

    def update_scales(self):
        self.line1.set_scale(self.scale)
        self.line2.set_scale(self.scale)
        self.line3.set_scale(self.scale)

    def draw(self, x_t):
        paint = QPainter()
        paint.begin(self.d_QWindow)
        paint.setRenderHint(QPainter.Antialiasing)

        paint.setBrush(Qt.white)
        clip_rect = QRect(self.x, self.y, self.width, self.height)
        paint.drawRect(clip_rect)

        paint.setPen(Qt.black)
        paint.setFont(QFont('Arial', 10))
        paint.drawText(10, 50, "1. Kierunek OLIWA -> WRZESZCZ")
        paint.drawText(10, 110, "2. Kierunek WRZESZCZ -> OLIWA")
        paint.drawText(10, 170, "3. Kierunek WRZESZCZ -> OSOWA")

        paint.end()

        # rysowanie lini kolejowych
        self.line1.draw_line(self.d_QWindow, x_t)
        self.line2.draw_line(self.d_QWindow, x_t)
        self.line3.draw_line(self.d_QWindow, x_t)

    # ustawienie wielkosci obszaru rysowania
    def set_size(self, height, width):
        self.height = height
        self.width = width

    # ustawienie pozycji obszaru rysowania
    def set_position(self, x, y):
        self.x = x
        self.y = y

        # def draw_legend(self):
        # TODO


class Railline:
    def __init__(self, x=0, y=0, leng_rails=None, stations=None, map_object=None, leng_railswitch=10, scale=1):
        self.x = x
        self.y = y
        self.leng_railswitch = leng_railswitch
        self.scale = scale

        # w przypadku braku wartosci ustaw jako pusta liste
        if leng_rails is None: leng_rails = []
        if stations is None: stations = []
        if map_object is None: map_object = []

        self.leng_rails = leng_rails
        self.stations = stations
        self.map_object = map_object

        # liczenie dlugosci calej lini kolejowej
        self.leng_line = self.count_leng_line()

        # uwaga pociag, dlugosci pociagow
        self.leng_train1 = 15
        self.leng_train2 = 30
        self.leng_train3 = 70

    def count_leng_line(self):
        if type(self.leng_railswitch) == int:
            n = self.map_object.count(3)
            leng_line = sum(self.leng_rails) + sum(self.stations[::2]) + n * self.leng_railswitch
        else:
            leng_line = sum(self.leng_rails) + sum(self.stations[::2]) + sum(self.leng_railswitch)

        return leng_line

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

    def set_leng_railswitch(self, leng_railswitch):
        self.leng_railswitch = leng_railswitch
        self.leng_line = self.count_leng_line()

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
    def draw_line(self, q_window, x_t):
        # tworzenie kopi wektorow
        cstations = self.stations[:]
        crail_leng = self.leng_rails[:]
        cobjects = self.map_object[:]
        if type(self.leng_railswitch) != int:
            cswitch = self.leng_railswitch[:]

        # kopie pozycji x i y
        x = self.x
        y = self.y

        paint = QPainter()
        paint.begin(q_window)
        paint.setRenderHint(QPainter.Antialiasing)

        # uwaga pociag
        self.draw_train(x_t, 200, paint)

        # -----------------------
        # rysowanie obiektow mapy
        # 0 - odcinek torow
        # 1 - stacja
        # 2 - czujnik
        # 3 - zwrotnica
        # -----------------------
        for obj in cobjects:
            if obj == 0:
                leng = crail_leng[0]
                crail_leng.pop(0)
                x, y = self.draw_rail(x, y, leng, paint)
            elif obj == 1:
                leng = cstations[0]
                cstations.pop(0)
                name = cstations[0]
                cstations.pop(0)
                x, y = self.draw_station(x, y, leng, 10, name, paint)
            elif obj == 2:
                self.draw_sensor(x, y, paint)
            elif obj == 3:
                if type(self.leng_railswitch) == int:
                    x, y = self.draw_railswitch(x, y, self.leng_railswitch, 10, paint)
                else:
                    leng = cswitch[0]
                    cswitch.pop(0)
                    x, y = self.draw_railswitch(x, y, leng, 10, paint)

        paint.end()

    # rysowanie stacji kolejowej
    def draw_station(self, x0, y0, leng, height, name, paint=QPainter()):
        width_sc = round(self.scale * leng)
        height_sc = round(self.scale * height)
        x1 = x0 + width_sc
        y1 = y0
        dy_text = round(self.scale * 15)

        st_dim = QRect(x0, y0 - height_sc / 2, width_sc, height_sc)
        text_dim = QRect(x0, y0 - height_sc / 2 - dy_text, width_sc, height_sc + 5)

        paint.setBrush(Qt.darkBlue)
        paint.drawRect(st_dim)
        paint.setPen(Qt.darkGray)
        paint.drawLine(x0, y0, x1, y1)
        paint.setPen(Qt.black)
        paint.setFont(QFont('Arial', round(10 * self.scale)))
        paint.drawText(text_dim, Qt.AlignCenter, name)

        return x1, y1

    # rysowanie odcinkow torow
    def draw_rail(self, x0, y0, leng, paint=QPainter()):
        len_sc = round(self.scale * leng)
        x1 = x0 + len_sc
        y1 = y0

        paint.setPen(Qt.black)
        paint.drawLine(x0, y0, x1, y1)

        return x1, y1

    # rysowanie czujnikow
    @staticmethod
    def draw_sensor(x0, y0, paint=QPainter()):
        pen = QPen()
        pen.setColor(Qt.red)
        pen.setWidth(5)

        paint.setPen(pen)
        paint.drawPoint(x0, y0)

    # rysowanie zwrotnic
    def draw_railswitch(self, x0, y0, leng, height, paint=QPainter()):
        width_sc = round(self.scale * leng)
        height_sc = round(self.scale * height)
        x1 = x0 + width_sc
        y1 = y0

        sw_dim = QRect(x0, y0 - height_sc / 2, width_sc, height_sc)

        paint.setBrush(Qt.green)
        paint.drawRect(sw_dim)

        # ryswanie zwrotnic w postaci trojkatow
        # TODO

        return x1, y1

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_scale(self, scale):
        self.scale = scale

    # class Railswitch:
    # TODO

    #uwaga pociag
    def draw_train (self, x0, y0, paint):

        width_sc = round(self.leng_train3)
        height_sc = round(20)

        y0 = y0 + 200

        x1 = x0 + width_sc
        y1 = y0

        st_dim = QRect(x0, y0 - height_sc / 2, width_sc, height_sc)

        paint.setBrush(Qt.yellow)
        paint.drawRect(st_dim)
        paint.setPen(Qt.darkGray)
