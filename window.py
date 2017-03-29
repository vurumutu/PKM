#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *

import train_map
import train

class About(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setGeometry(50, 100, 1000, 500)
        self.setWindowTitle('About')
        self.initT()

    def initT(self):

        self.text = ('Projekt na zaliczenie przedmiotu Roboty Inteligentne 2017\n'
                     'Program umozliwiajacy sterowanie makieta PKM \n'
                     'oraz uruchamianie wczesniej ustalonego harmonogramu')
        self.show()

# tworzenie tekstu
    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):

        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)

#okno authors
class Authors(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setGeometry(50, 100, 1000, 500)
        self.setWindowTitle('Authors')
        self.initT()

    def initT(self):

        self.text = ('Sklad grupy:\n\n' 
                     'Wojciech Zgliniecki - Leader\n '
                     'Dworakowski Karol\n'
                     'Filipkiewicz Marlena\n'
                     'Pawlowski Franciszek\n'
                     'Rogaszewski Pawel\n'
                     'Sendrowicz Mateusz\n'
                     'Sternicki Pawel\n'
                     'Trzcinski Karol\n'
                     'Zbikowski Bartosz\n')
        self.show()

# tworzenie tekstu
    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()

    def drawText(self, event, qp):

        qp.setPen(QtGui.QColor(0, 0, 0))
        qp.setFont(QtGui.QFont('Calibri', 12))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 1000, 300)
        self.setWindowTitle("PKM")
        self.setWindowIcon(QtGui.QIcon('ictrain.png'))

        toolbar = QtGui.QHBoxLayout()

        # utworzenie obiektu tworzacego mape kolejowa
        self.map = train_map.Railmap(5, 30, self.height()-120, self.width()-10, self)

        #utworzenie obektu zapwierajacego informacje o pociagach
        self.train = train.Train()
        self.index_t = 1    #numer wybranego pociagu
        
        #rozmieszczenie radiobuttonow i slidera
        button_space = QtGui.QHBoxLayout()
        toolbar = QtGui.QVBoxLayout()
        label_space =QtGui.QHBoxLayout()
        button_space.setContentsMargins(100, 0, 100, 20)
        label_space.setContentsMargins(100, 0, 100, 20)
        toolbar.setContentsMargins(100, 400, 100, 100)
        
        # radiobuttons
        self.btn1 = QtGui.QRadioButton("Pociag nr 1", self)
        self.btn1.clicked.connect(self.tUpdate)    # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        self.btn2 = QtGui.QRadioButton("Pociag nr 2", self)
        self.btn2.clicked.connect(self.tUpdate)    # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        self.btn3 = QtGui.QRadioButton("Pociag nr 3", self)
        self.btn3.clicked.connect(self.tUpdate)    # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        self.btn4 = QtGui.QRadioButton("Pociag nr 4", self)
        self.btn4.clicked.connect(self.tUpdate)    # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        self.btn5 = QtGui.QRadioButton("Pociag nr 5", self)
        self.btn5.clicked.connect(self.tUpdate)    # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        self.btn6 = QtGui.QRadioButton("Pociag nr 6", self)
        self.btn6.clicked.connect(self.tUpdate)    # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)


        button_space.addWidget(self.btn1)
        button_space.addWidget(self.btn2)
        button_space.addWidget(self.btn3)
        button_space.addWidget(self.btn4)
        button_space.addWidget(self.btn5)
        button_space.addWidget(self.btn6)

        self.lab1 = QtGui.QLabel(str(self.train.getValue(1)))
        self.lab2 = QtGui.QLabel(str(self.train.getValue(2)))
        self.lab3 = QtGui.QLabel(str(self.train.getValue(3)))
        self.lab4 = QtGui.QLabel(str(self.train.getValue(4)))
        self.lab5 = QtGui.QLabel(str(self.train.getValue(5)))
        self.lab6 = QtGui.QLabel(str(self.train.getValue(6)))

        label_space.addWidget(self.lab1)
        label_space.addWidget(self.lab2)
        label_space.addWidget(self.lab3)
        label_space.addWidget(self.lab4)
        label_space.addWidget(self.lab5)
        label_space.addWidget(self.lab6)
        # -------
        
        slider = self.create_slider()
        toolbar.addWidget(slider)

        # ustaienie ukladu okienka
        toolbar.setAlignment(QtCore.Qt.AlignCenter)

        central_widget = QtGui.QWidget()
        central_widget.setLayout(toolbar)
        toolbar.addLayout(button_space)
        toolbar.addLayout(label_space)
        self.setCentralWidget(central_widget)
        
        self.przyciski_zwrotnice()

        self.initUI()
        self.show()
        
    def przyciski_zwrotnice(self):  
# tor 1     
        '''self.lbl1 = QtGui.QLabel("Tor 1", self)
        self.lbl1.move(620, 320)
        
        t1z1 = QtGui.QPushButton('Zwrotnica 1', self)
        t1z1.clicked.connect(QtCore.QCoreApplication.instance().quit) 
        t1z1.resize(t1z1.sizeHint())
        t1z1.move(600, 350)       
        
        t1z2 = QtGui.QPushButton('Zwrotnica 2', self)
        t1z2.clicked.connect(QtCore.QCoreApplication.instance().quit)
        t1z2.resize(t1z2.sizeHint())
        t1z2.move(600, 380)
# tor 2    
        self.lbl2 = QtGui.QLabel("Tor 2", self)
        self.lbl2.move(720, 320)
        
        t2z1 = QtGui.QPushButton('Zwrotnica 1', self)
        t2z1.clicked.connect(QtCore.QCoreApplication.instance().quit)
        t2z1.resize(t2z1.sizeHint())
        t2z1.move(700, 350) 
        
        t2z2 = QtGui.QPushButton('Zwrotnica 2', self)
        t2z2.clicked.connect(QtCore.QCoreApplication.instance().quit)
        t2z2.resize(t2z2.sizeHint())
        t2z2.move(700, 380) '''
# tor 3      
        self.lbl1 = QtGui.QLabel("Trasa: Oliwa <-> Wrzeszcz", self)
        self.lbl1.move(715, 320)
        self.lbl1.resize(200, 20)
        
        t3z1 = QtGui.QPushButton('Zwrotnica 1', self)
        t3z1.clicked.connect(self.change_state_switch1)
        t3z1.resize(t3z1.sizeHint())
        t3z1.move(745, 350)
        
        t3z2 = QtGui.QPushButton('Zwrotnica 2', self)
        t3z2.clicked.connect(self.change_state_switch2)
        t3z2.resize(t3z2.sizeHint())
        t3z2.move(745, 380)
# tor 4    
        self.lbl2 = QtGui.QLabel("Trasa: Osowa <-> Wrzeszcz", self)
        self.lbl2.move(855, 320)
        self.lbl2.resize(200, 20)
        
        t4z1 = QtGui.QPushButton('Zwrotnica 3', self)
        t4z1.clicked.connect(self.change_state_switch3)
        t4z1.resize(t4z1.sizeHint())
        t4z1.move(900, 350) 
        
        t4z2 = QtGui.QPushButton('Zwrotnica 4', self)
        t4z2.clicked.connect(self.change_state_switch4)
        t4z2.resize(t4z2.sizeHint())
        t4z2.move(900, 380)
        
    # tworzeie MENU
    def initUI(self):
        # Exit
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application') #zamykanie
        exitAction.triggered.connect(self.close_application)
        # About
        helpAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&About', self)
        helpAction.setShortcut('Ctrl+H')
        helpAction.triggered.connect(self.doit) #wywolanie kolejnego okna
        # Authors
        authorsAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Authors', self)
        authorsAction.setShortcut('Ctrl+A')
        authorsAction.triggered.connect(self.doitA)
        self.w = None
        self.a = None

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File') #umieszczenie w menu "File"
        fileMenu.addAction(exitAction)
        fileMenu2 = menubar.addMenu('&Help')
        fileMenu2.addAction(helpAction) #umiezczenie w menu "About"
        fileMenu2.addAction(authorsAction) #umiezczenie w menu "Authors"

        self.setGeometry(300, 200, 1000, 600)
        self.setWindowTitle('PKM')
        self.show()

    def doit(self):
        self.w = About()
        self.w.show()
        
    def doitA(self):
        self.a = Authors()
        self.a.show()
        
    def create_slider(self):
        layout = QtGui.QVBoxLayout()
        l1 = QtGui.QLabel("Predkosc", self)
        l1.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(l1)

        self.slider_speed = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_speed.setMinimum(10)
        self.slider_speed.setMaximum(30)
        self.slider_speed.setValue(20)
        self.slider_speed.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slider_speed.setTickInterval(5)
        self.slider_speed.valueChanged.connect(self.tUpdate)
        layout.addWidget(self.slider_speed)

        slider = QtGui.QWidget()
        slider.setLayout(layout)

        return slider

    #aktualizacjia wyboru pociagu
    def tUpdate(self):
        if self.btn1.isChecked():
            self.index_t = 1
            self.train.setValue(self.slider_speed.value(), self.index_t)
            self.lab1.setText(str(self.train.getValue(self.index_t)))
            self.repaint()
        elif self.btn2.isChecked():
            self.index_t = 2
            self.train.setValue(self.slider_speed.value(),self.index_t)
            self.lab2.setText(str(self.train.getValue(self.index_t)))
            self.repaint()
        elif self.btn3.isChecked():
            self.index_t = 3
            self.train.setValue(self.slider_speed.value(),self.index_t)
            self.lab3.setText(str(self.train.getValue(self.index_t)))
            self.repaint()
        elif self.btn4.isChecked():
            self.index_t = 4
            self.train.setValue(self.slider_speed.value(),self.index_t)
            self.lab4.setText(str(self.train.getValue(self.index_t)))
            self.repaint()
        elif self.btn5.isChecked():
            self.index_t = 5
            self.train.setValue(self.slider_speed.value(),self.index_t)
            self.lab4.setText(str(self.train.getValue(self.index_t)))
            self.repaint()
        elif self.btn6.isChecked():
            self.index_t = 6
            self.train.setValue(self.slider_speed.value(),self.index_t)
            self.lab4.setText(str(self.train.getValue(self.index_t)))
            self.repaint()

    def change_state_switch1(self):
        self.map.switch1.neg_status()
        self.repaint()

    def change_state_switch2(self):
        self.map.switch2.neg_status()
        self.repaint()

    def change_state_switch3(self):
        self.map.switch3.neg_status()
        self.repaint()

    def change_state_switch4(self):
        self.map.switch4.neg_status()
        self.repaint()

    def resizeEvent(self, event):
        self.map.set_size(self.height()-120, self.width()-10)
        self.map.setscale()

    def paintEvent(self, event):
        self.train.setValue(self.slider_speed.value(), self.index_t)
        self.map.draw(self.train.getValue(self.index_t), self.train.getLength(self.index_t))

    @staticmethod
    def close_application():
        sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
