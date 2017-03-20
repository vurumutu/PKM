from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Train:

    def __init__(self, x_t):
        self.x_t = x_t  #pozycja pociagu

    def setValue(self, x_t):
        self.x_t = x_t

    def getValue(self):
        return self.x_t
