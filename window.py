import sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PKM")
        #self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))
        self.home()

    def home(self):
        btn1 = QtGui.QPushButton("Sprawdz pozycje", self)
        btn1.clicked.connect(self.close_application)
        btn1.resize(btn1.minimumSizeHint())
        btn1.move(100, self.height()-30)

        btn2 = QtGui.QPushButton("Ustaw pociagi", self)
        btn2.clicked.connect(self.close_application)
        btn2.resize(btn2.minimumSizeHint())
        btn2.move(10, self.height()-30)

        self.show()

    def check_position(self):
        print()

    def close_application(self):
        sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
    #app.exec_()

run()