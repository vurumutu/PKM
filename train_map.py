#import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Railmap:

    def __init__(self, x, y, height, width, q_window):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.d_QWindow = q_window

        #lista rzeczywistych odcinkow torow w cm
        self.leng_rails1 = [25,5,90,50,20,20,20,20,20,300,200,10,5,40]
        self.leng_rails2 = [25,5,90,450,200,10,5,40]
        self.leng_rails3 = [80,100,5,135,5,35,570,245,20,10]

        # lista stacji (dlugosc peronu, nazwa stacji)
        self.stations1 = [100,"Wrzeszcz",100,"Oliwa"]
        self.stations2 = [100, "Wrzeszcz", 100, "Strzyza", 100, "Osowa"]
        self.leng_railswitch = 10

        # mapy obiektow - wektor
        # 0 - odcinek torow
        # 1 - stacja
        # 2 - czujnik
        # 3 - zwrotnica
        self.map_object1 = [1,0,2,0,3,0,2,0,2,0,2,0,2,0,2,0,2,0,2,0,2,0,1,0,3,0,2,0]
        self.map_object2 = [1,0,2,0,3,0,2,0,2,0,1,0,3,0,2,0]
        self.map_object3 = [1,2,0,2,0,2,0,3,0,2,0,1,0,2,0,2,0,3,0,2,0,1]

        self.leng_line = sum(self.leng_rails3) + sum(self.stations2[::2]) + 2*self.leng_railswitch

        self.setscale()

    #liczenie skali proporcjonalnej do rzeczywistych wymiarow
    def setscale(self):
        margin = 5
        self.scale = (self.width - 2 * margin + 0.) / (self.leng_line + 0.)
        #debug
        #print(self.leng_line)
        #print(self.width)
        #print(self.scale)

    def draw(self):
        paint = QPainter()
        paint.begin(self.d_QWindow)
        paint.setRenderHint(QPainter.Antialiasing)

        paint.setBrush(Qt.white)
        clip_rect = QRect(self.x, self.y, self.width, self.height)
        paint.drawRect(clip_rect)

        paint.setPen(Qt.black)
        paint.setFont(QFont('Arial', 10))
        paint.drawText(10, 20, "1. Kierunek OLIWA -> WRZESZCZ")
        paint.drawText(10, 80, "2. Kierunek WRZESZCZ -> OLIWA")
        paint.drawText(10, 140, "3. Kierunek WRZESZCZ -> OSOWA")

        paint.end()

        #rysowanie lini kolejowych

        self.draw_line(self.stations1, self.leng_rails1, self.map_object1, 10, 50)
        self.draw_line(self.stations1, self.leng_rails2, self.map_object2, 10, 110)
        self.draw_line(self.stations2, self.leng_rails3, self.map_object3, 10, 170)

    def draw_line(self, stations=[], rail_leng=[], objects=[],  x = 0, y = 0):
        #tworzenie kopi wektorow
        cstations = stations[:]
        crail_leng = rail_leng[:]

        paint = QPainter()
        paint.begin(self.d_QWindow)
        paint.setRenderHint(QPainter.Antialiasing)

        #-----------------------
        #rysowanie obiektow mapy
        #0 - odcinek torow
        #1 - stacja
        #2 - czujnik
        #3 - zwrotnica
        #-----------------------
        for obj in objects:
            if obj == 0 :
                len = crail_leng[0]
                crail_leng.pop(0)
                x, y = self.draw_rail(x, y, len, paint)
            elif obj == 1 :
                len = cstations[0]
                cstations.pop(0)
                name = cstations[0]
                cstations.pop(0)
                x, y = self.draw_station(x, y, len, 10, name, paint)
            elif obj == 2 :
                self.draw_sensor(x, y, paint)
            elif obj == 3 :
                x, y = self.draw_railswitch(x, y, self.leng_railswitch, 10, paint)

        paint.end()

    def draw_station(self, x0, y0, leng, height, name, paint = QPainter()):
        # wys = width
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
        paint.setFont(QFont('Arial', round(10*self.scale)))
        paint.drawText(text_dim, Qt.AlignCenter, name)

        return x1, y1

    def draw_rail(self, x0, y0, leng, paint = QPainter()):
        len_sc = round(self.scale * leng)
        x1 = x0 + len_sc
        y1 = y0

        paint.setPen(Qt.black)
        paint.drawLine(x0, y0, x1, y1)

        return x1, y1

    def draw_sensor(self, x0, y0, paint = QPainter()):
        pen = QPen()
        pen.setColor(Qt.red)
        pen.setWidth(5)

        paint.setPen(pen)
        paint.drawPoint(x0, y0)

    def draw_railswitch(self, x0, y0, leng, height, paint = QPainter()):
        width_sc = round(self.scale * leng)
        height_sc = round(self.scale * height)
        x1 = x0 + width_sc
        y1 = y0

        sw_dim = QRect(x0, y0 - height_sc / 2, width_sc, height_sc)

        paint.setBrush(Qt.green)
        paint.drawRect(sw_dim)

        return x1, y1

    def setSize(self, height, width):
        self.height = height
        self.width = width

    def setPosition(self, x, y):
        self.x = x
        self.y = y