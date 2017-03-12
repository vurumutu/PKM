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

    def setSize(self, height, width):
        self.height = height
        self.width = width

    def setPosition(self, x, y):
        self.x = x
        self.y = y

