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

    def draw(self):
        paint = QPainter()
        paint.begin(self.d_QWindow)

        paint.setRenderHint(QPainter.Antialiasing)

        paint.setBrush(Qt.white)
        clip_rect = QRect(self.x, self.y, self.width, self.height)
        paint.drawRect(clip_rect)
        paint.end()
        self.stations()
        
    def stations(self): 
        
        startx1=self.x+20
        starty1=self.y+100
        startx2=85*self.width/100
        starty2=self.y+100
        szer = self.width/8
        wys = self.height/12
        
        paint = QPainter()
        paint.begin(self.d_QWindow)
        paint.setRenderHint(QPainter.Antialiasing)
        paint.setBrush(Qt.gray)
        stc1 = QRect(startx1, starty1, szer, wys)
        stc2 = QRect(startx2, starty2, szer, wys)
        paint.drawRect(stc1)
        paint.drawRect(stc2)
        paint.drawText(2*self.width/100,starty1-10, "Gdank Wrzeszcz" )
        paint.drawText(84*self.width/100,starty2-10, "Gdansk Oliwa" )
        paint.end()
        self.rails(startx1,startx2,wys,szer)
        
    def rails(self, x, y, h, w):
        
        paint = QPainter()
        paint.begin(self.d_QWindow)
        paint.drawLine(x+w,h/2+100,y,h/2+100)
        paint.drawLine(x,h+300,y+w,h+300)
        paint.end()

    def setSize(self, height, width):
        self.height = height
        self.width = width

    def setPosition(self, x, y):
        self.x = x
        self.y = y

