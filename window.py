import sys
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *

import train_map

#wyskakujące okno "About" 
class Popup(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        self.setGeometry(50, 100, 1000, 500)
        self.setWindowTitle('About')
        self.initT()
        
    def initT(self):      

        self.text = 'Cos tam cos tam i jeszcze wiecej, wykonawcy'
        self.show()
        
#wpisywanie tekstu tekstu
    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()
        
    def drawText(self, event, qp):
      
        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 1000, 300)
        self.setWindowTitle("PKM")
        self.setWindowIcon(QtGui.QIcon('ictrain.png'))

        toolbar = QtGui.QHBoxLayout()

        #utworzenie obiektu tworzacego mape kolejowa
        self.map = train_map.Railmap(5, 5, self.height()-70, self.width()-10, self)

        #przyciski
        btn1 = QtGui.QPushButton("Sprawdz pozycje", self)
        btn1.clicked.connect(self.close_application)
        btn1.resize(btn1.minimumSizeHint())
        #btn1.move(10, self.height()-30)

        btn2 = QtGui.QPushButton("Ustaw pociagi", self)
        btn2.clicked.connect(self.close_application)
        btn2.resize(btn2.minimumSizeHint())
        #btn2.move(120, self.height()-30)

        toolbar.addWidget(btn1)
        toolbar.addWidget(btn2)
        #-------

        slider = self.create_slider(210,self.height()-50)
        toolbar.addWidget(slider)

        #ustaienie ukladu okienka
        toolbar.setAlignment(QtCore.Qt.AlignBottom)

        central_widget = QtGui.QWidget()
        central_widget.setLayout(toolbar)
        self.setCentralWidget(central_widget)
        self.initUI()
        self.show()
        
      #tworzeie MENU  
    def initUI(self):               
        #Exit
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application') #zamykanie
        exitAction.triggered.connect(self.close_application)
        #About
        helpAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&About', self)
        helpAction.setShortcut('Ctrl+H')
        helpAction.triggered.connect(self.doit) #wywolanie kolejnego okna
        #self.connect(self.helpAction, SIGNAL("clicked()"), self.doit)
        self.w = None
        
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File') #umieszczenie w menu "File"
        fileMenu.addAction(exitAction)
        fileMenu = menubar.addMenu('&Help')
        fileMenu.addAction(helpAction) #umiezczenie w menu "About"
        
        self.setGeometry(300, 300, 1000, 800)
        self.setWindowTitle('PKM')    
        self.show()

    def doit(self):
        
        self.w = Popup()
        self.w.show()

    def create_slider(self, x, y):
        layout = QtGui.QVBoxLayout()
        l1 = QtGui.QLabel("Predkosc", self)
        l1.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(l1)

        slider_speed = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        slider_speed.setMinimum(10)
        slider_speed.setMaximum(30)
        slider_speed.setValue(20)
        slider_speed.setTickPosition(QtGui.QSlider.TicksBelow)
        slider_speed.setTickInterval(5)
        layout.addWidget(slider_speed)

        slider = QtGui.QWidget()
        slider.setLayout(layout)

        return slider

    def resizeEvent(self, event):
        self.map.setSize(self.height()-70, self.width()-10)
        self.map.setscale()

    def paintEvent(self, event):
        self.map.draw()

    def close_application(self):
        sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
    #app.exec_()

run()
