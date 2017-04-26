#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *

import train_map
import train
import train_auto
#import CAN as can
import CAN_const as can_const
from xpressnet import Client
from xpressnet import Train
from time import sleep

TCP_IP = '192.168.210.200'
TCP_PORT = 5550
direction = {"Forward": 1, "Backward": 0}

#Okno logowania
class Login(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setGeometry(1000, 500, 500, 500)
        self.setWindowTitle('Logowanie')
        self.textName = QtGui.QLineEdit(self)
        self.textPass = QtGui.QLineEdit(self)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
        
#login i hasło
    def handleLogin(self):
        if (self.textName.text() == 'user' and
            self.textPass.text() == 'user1'):
            self.accept()
        else:
            QtGui.QMessageBox.warning(
                self, 'Error', 'Bad user or password')
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

        self.timerTable = train_auto.TimeTable(self)

        toolbar = QtGui.QHBoxLayout()

        # utworzenie obiektu tworzacego mape kolejowa
        self.map = train_map.Railmap(5, 30, self.height()-120, self.width()-10, self)

        # tworzenie klienta do polaczenia
        self.client = Client()

        #utworzenie obektu zapwierajacego informacje o pociagach
        self.train = train.Train()
        self.msg = None
        self.index_t = 4    #numer wybranego pociagu - 1, bo numerujemy tablice od 0
        self.trains = []
        for i in range(1,7):
            self.trains.append(Train(i))

        
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

        self.lab1 = QtGui.QLabel(str(self.train.getValue()[0]))
        self.lab2 = QtGui.QLabel(str(self.train.getValue()[1]))
        self.lab3 = QtGui.QLabel(str(self.train.getValue()[2]))
        self.lab4 = QtGui.QLabel(str(self.train.getValue()[3]))
        self.lab5 = QtGui.QLabel(str(self.train.getValue()[4]))
        self.lab6 = QtGui.QLabel(str(self.train.getValue()[5]))

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
        # przycisk polaczenie
        self.conn_button = QtGui.QPushButton('Polacz z pociagami', self)
        self.conn_button.clicked.connect(self.connect_disconect)
        self.conn_button.resize(150, 40)
        self.conn_button.move(720, 360)

        self.initUI()
        self.show()
        
    def przyciski_zwrotnice(self):
        Group_switch = QtGui.QGroupBox(self)
        Group_switch.setTitle("Zwrotnice")
        Group_switch.setGeometry(300,330,400,100)
# tor 3
        self.lbl1 = QtGui.QLabel("Trasa: Osowa <-> Wrzeszcz: ", Group_switch)
        self.lbl1.move(10, 25)
        self.lbl1.resize(200, 20)
        
        t3z1 = QtGui.QPushButton('Zwrotnica 1', Group_switch)
        t3z1.clicked.connect(self.change_state_switch1)
        t3z1.resize(t3z1.sizeHint())
        t3z1.move(200, 20)
        
        t3z2 = QtGui.QPushButton('Zwrotnica 2', Group_switch)
        t3z2.clicked.connect(self.change_state_switch2)
        t3z2.resize(t3z2.sizeHint())
        t3z2.move(300, 20)
# tor 4    
        self.lbl2 = QtGui.QLabel("Trasa: Kielpinek <-> Wrzeszcz:", Group_switch)
        self.lbl2.move(10, 65)
        self.lbl2.resize(200, 20)
        
        t4z1 = QtGui.QPushButton('Zwrotnica 3', Group_switch)
        t4z1.clicked.connect(self.change_state_switch3)
        t4z1.resize(t4z1.sizeHint())
        t4z1.move(200, 60)
        
        t4z2 = QtGui.QPushButton('Zwrotnica 4', Group_switch)
        t4z2.clicked.connect(self.change_state_switch4)
        t4z2.resize(t4z2.sizeHint())
        t4z2.move(300, 60)
        
    # tworzeie MENU
    def initUI(self):
        # Exit
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application') #zamykanie
        exitAction.triggered.connect(close_application)
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
        self.slider_speed.setMinimum(0)
        self.slider_speed.setMaximum(127)
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
            self.index_t = 0
            self.train.setValue(self.slider_speed.value(), self.index_t)
            self.lab1.setText(str(self.train.getValue()[self.index_t]))
            #ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[1].speed(self.slider_speed.value(), direction["Forward"])

        elif self.btn2.isChecked():
            self.index_t = 1
            self.train.setValue(self.slider_speed.value(),self.index_t)
            self.lab2.setText(str(self.train.getValue()[self.index_t]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[2].speed(self.slider_speed.value(), direction["Forward"])

        elif self.btn3.isChecked():
            self.index_t = 2
            self.train.setValue(self.slider_speed.value(),self.index_t)
            self.lab3.setText(str(self.train.getValue()[self.index_t]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[3].speed(self.slider_speed.value(), direction["Forward"])

        elif self.btn4.isChecked():
            self.index_t = 3
            self.train.setValue(self.slider_speed.value(),self.index_t)
            self.lab4.setText(str(self.train.getValue()[self.index_t]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[4].speed(self.slider_speed.value(), direction["Forward"])

        elif self.btn5.isChecked():
            self.index_t = 4
            self.train.setValue(self.slider_speed.value(),self.index_t)
            self.lab4.setText(str(self.train.getValue()[self.index_t]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[5].speed(self.slider_speed.value(), direction["Forward"])

        elif self.btn6.isChecked():
            self.index_t = 5
            self.train.setValue(self.slider_speed.value(),self.index_t)
            self.lab4.setText(str(self.train.getValue()[self.index_t]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[6].speed(self.slider_speed.value(), direction["Forward"])

        self.repaint()
        if self.msg is not None and self.client.connected:
            self.client.send(self.msg)
            sleep(1)  # Czekaj 1s
            self.msg = None

    def change_state_switch1(self):
        self.map.switch1.neg_status()
        self.repaint()
        if self.map.switch1.status:
            can.zwrotnica[0].lewo()
        else:
            can.zwrotnica[0].prawo()

    def change_state_switch2(self):
        self.map.switch2.neg_status()
        self.repaint()
        if self.map.switch1.status:
            can.zwrotnica[1].lewo()
        else:
            can.zwrotnica[1].prawo()

    def change_state_switch3(self):
        self.map.switch3.neg_status()
        self.repaint()
        if self.map.switch1.status:
            can.zwrotnica[2].lewo()
        else:
            can.zwrotnica[2].prawo()

    def change_state_switch4(self):
        self.map.switch4.neg_status()
        self.repaint()
        if self.map.switch1.status:
            can.zwrotnica[3].lewo()
        else:
            can.zwrotnica[3].prawo()

    #łączenie i rozłączenie z pociągami
    def connect_disconect(self):

        if self.client.connected:
            self.client.stop_all_locomotives()
            self.client.disconnect()
            self.conn_button.setText("Polacz z pociagami")
        else:
            self.client.connect(TCP_IP, TCP_PORT)
            self.conn_button.setText("Rozlacz z pociagami")

    def resizeEvent(self, event):
        self.map.set_size(self.height()-120, self.width()-10)
        self.map.setscale()

    def paintEvent(self, event):
        self.train.setValue(self.slider_speed.value(), self.index_t)
        self.map.draw(self.train.getValue(), self.train.getLength())

    def timerEvent(self, event):
        for i in range(4):
            if event.timerId() == self.timerTable.timers[i].timerId():
                self.timerTable.updateTimers(i)
                self.train.setValue(self.timerTable.positionTable[i][self.timerTable.licznik[i]],i)
                self.repaint()

def close_application():
    sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    login = Login()
    if login.exec_() == QtGui.QDialog.Accepted:
        GUI = Window()
        GUI.show()
        sys.exit(app.exec_())

run()
