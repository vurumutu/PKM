#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *

# import requests
import json

from pade.misc.utility import display_message
from pade.misc.common import set_ams, start_loop
from pade.core.agent import Agent
from pade.acl.aid import AID
import thread
import twisted.internet

import agent

import train_map
import train
import train_auto
import kalman
#from CAN import *
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
        if (self.textName.text() == '' and
                    self.textPass.text() == ''):
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

        self.autoControl = False
        self.timerTable = train_auto.TimeTable(self)

        # tworzenie klienta do polaczenia
        self.client = Client()

        #utworzenie obektu zapwierajacego informacje o pociagach
        #self.train_GUI = train.Train()
        self.msg = None
        self.index_t = 4    #numer wybranego pociagu - 1, bo numerujemy tablice od 0
        self.trains = []
        for i in range(1,7):
            self.trains.append(Train(i))

        self.createTimers()

        self.kalman_train = [0,0,0,0]

        self.zwrotnice_ = []
        self.trains_speed = [0, 0, 0, 0, 0, 0]

        # utworzenie obiektu tworzacego mape kolejowa
        self.map = train_map.Railmap(0, 30, self.height(), self.width(), self.kalman_train, self)

        # inicjalizacja zwotnic
        self.initRequest()
        self.initAgentSystem()

        #print(len(can.zwrotnica))
        #self.initSwitches()
        self.initLayout()
        self.initUI()
        self.show()
        self.setAutoControl()

    def initAgentSystem(self):
        set_ams('localhost', 8001, debug=False)

        self.agentsList = list()

        agente_train_1 = agent.AgenteHelloWorld(AID(name='agente_hello1'))
        agente_train_1.ams = {'name': 'localhost', 'port': 8001}
        self.agentsList.append(agente_train_1)

        agente_train_2 = agent.AgenteHelloWorld(AID(name='agente_hello2'))
        agente_train_2.ams = {'name': 'localhost', 'port': 8001}
        self.agentsList.append(agente_train_2)

        agente_train_3 = agent.AgenteHelloWorld(AID(name='agente_hello5'))
        agente_train_3.ams = {'name': 'localhost', 'port': 8001}
        self.agentsList.append(agente_train_3)

    def initRequest(self):

        self.timer_requests = QBasicTimer()
        try:
            self.my_requests = requests.get('http://127.0.0.1:8000/trains/')
            print("Connect to http://127.0.0.1:8000/trains/")
            self.timer_requests.start(2000,self)
        except:
            print("http://127.0.0.1:8000/trains/ does not respond")

    # INICJALIZACJA ZWROTNIC
    def initSwitches(self):
        # adresy używanych zwrotnic
        addr_zwrotnic_main = ['010501F5', '010401FB', '0105006F', '0102000C']
        # adresy zwrotnic ustawianych tylko przy uruchomieiu programu
        addr_zwrotnic_other = ['010501F7', '010501F8', '010501F9', '010501FA',
                               '01050067', '01050134', '0105006C', '0105006D', '0105006E', '01010065', '01010066', '01020001', '01020002', '0102000B']

        addr_zwrotnic = addr_zwrotnic_main + addr_zwrotnic_other

        for address in addr_zwrotnic_main:
            find = False
            print("test")
            for zwrot in can.zwrotnica:
                if zwrot.agent.address.lower() == address.lower():
                    self.zwrotnice_.append(zwrot)
                    find = True
                    break
            # sprawdza czy znalazł zwrotnice
            # gdy jej nie znalazł to wpisz wartośc None
            # oraz wyswietl komunikat
            if not find:
                self.zwrotnice_.append(None)
                print(" Nie znalezono zwrotnicy o adresie: " + address)
                #QMessageBox.warning(self, "Zwrotnice", " Nie znalezono zwrotnicy o adresie: " + address, QMessageBox.Ok)


        # poczatkowe ustawienie zwrotnic
        # numer zwrotnicy : zwrot (False - right, True - Left
        defaultDirect = [True,False,True,True]
        for num_switch in range(len(defaultDirect)):
            sleep(0.2)
            print("test: " + str(num_switch))
            if defaultDirect[num_switch]:
                #left
                self.zwrotnice_[num_switch].lewo()
            else:
                #right
                self.zwrotnice_[num_switch].prawo()

    # INICJALIZACJA LAYOUTU
    def initLayout(self):
        # ustawienie rozmieszczenia mapy i toolbara w oknie
        centarl_layout = QtGui.QVBoxLayout()
        # stworznie toolbara wraz z jego podrupami
        toolbar = QtGui.QHBoxLayout()

        toolbar.addWidget(self.toolbar_trainmovement())
        toolbar.addWidget(self.toolbar_speedcontrol())
        toolbar.addWidget(self.toolbar_switches())
        toolbar.addWidget(self.tooolbar_traincontrol())
        toolbar.setAlignment(QtCore.Qt.AlignBottom)

        centarl_layout.addWidget(self.map, 1)
        centarl_layout.addLayout(toolbar)

        # ustawienie układu okna
        central_widget = QtGui.QWidget()
        central_widget.setLayout(centarl_layout)

        self.setCentralWidget(central_widget)

    # ****************************
    # --- PODGRUPY PRZYBORNIKA ---
    # ****************************

    # podgrupa kontrolek wyboru ruchu pociagu
    def toolbar_trainmovement(self):
        Group_trainmovement = QtGui.QGroupBox(self)
        Group_trainmovement.setTitle("Train movement")
        Group_trainmovement.setMinimumSize(200, 100)

        self.forward_radio = QtGui.QRadioButton("Forward", Group_trainmovement)
        self.forward_radio.resize(self.forward_radio.sizeHint())
        self.forward_radio.move(20, 40)
        self.forward_radio.setChecked(True)

        self.backward_radio = QtGui.QRadioButton("Backward", Group_trainmovement)
        self.backward_radio.resize(self.backward_radio.sizeHint())
        self.backward_radio.move(20, 70)

        self.stop_button = QtGui.QPushButton("Stop train", Group_trainmovement)
        self.stop_button.clicked.connect(self.stopTrain)
        self.stop_button.resize(80, 30)
        self.stop_button.move(20, 100)

        self.stopall_button = QtGui.QPushButton("Stop all", Group_trainmovement)
        self.stopall_button.clicked.connect(self.stopAllTrains)
        self.stopall_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        self.stopall_button.resize(70, 70)
        self.stopall_button.move(115, 50)

        return Group_trainmovement

    # podgrupa kontrolek do sterowania prędkością pociagu
    def toolbar_speedcontrol(self):
        self.slider = self.create_slider()

        speedcontrol_space = QtGui.QVBoxLayout()
        button_space = QtGui.QHBoxLayout()
        label_space = QtGui.QHBoxLayout()

        speedcontrol_space.addWidget(self.slider)
        speedcontrol_space.addLayout(button_space)
        speedcontrol_space.addLayout(label_space)

        Group_speedcontrol = QtGui.QGroupBox(self)
        Group_speedcontrol.setTitle("Speed control")
        Group_speedcontrol.setLayout(speedcontrol_space)

        # radiobuttons
        self.btn1 = QtGui.QRadioButton("Train 1", self)
        self.btn1.clicked.connect(self.tUpdate)  # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        self.btn2 = QtGui.QRadioButton("Train 2", self)
        self.btn2.clicked.connect(self.tUpdate)  # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        self.btn3 = QtGui.QRadioButton("Train 3", self)
        self.btn3.clicked.connect(self.tUpdate)  # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        self.btn4 = QtGui.QRadioButton("Train 4", self)
        self.btn4.clicked.connect(self.tUpdate)  # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        self.btn5 = QtGui.QRadioButton("Train 5", self)
        self.btn5.clicked.connect(self.tUpdate)  # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        self.btn6 = QtGui.QRadioButton("Train 6", self)
        self.btn6.clicked.connect(self.tUpdate)  # TO DO - funkcja zmieniająca poaciąg (sterowanie jego predkoscia)

        button_space.addWidget(self.btn1)
        button_space.addWidget(self.btn2)
        button_space.addWidget(self.btn3)
        button_space.addWidget(self.btn4)
        button_space.addWidget(self.btn5)
        button_space.addWidget(self.btn6)

        self.lab1 = QtGui.QLabel(str(self.trains[0].velocity))
        self.lab2 = QtGui.QLabel(str(self.trains[1].velocity))
        self.lab3 = QtGui.QLabel(str(self.trains[2].velocity))
        self.lab4 = QtGui.QLabel(str(self.trains[3].velocity))
        self.lab5 = QtGui.QLabel(str(self.trains[4].velocity))
        self.lab6 = QtGui.QLabel(str(self.trains[5].velocity))

        label_space.addWidget(self.lab1)
        label_space.addWidget(self.lab2)
        label_space.addWidget(self.lab3)
        label_space.addWidget(self.lab4)
        label_space.addWidget(self.lab5)
        label_space.addWidget(self.lab6)

        return Group_speedcontrol

    # podgrupa kontrolek do sterowania zwrotnicami
    def toolbar_switches(self):
        Group_switch = QtGui.QGroupBox(self)
        Group_switch.setTitle("Switches")
        Group_switch.setMinimumSize(400, 100)
        marginX = 0
        marginY = 20

        # tor 1
        lbl1 = QtGui.QLabel("Route: Osowa <-> Wrzeszcz: ", Group_switch)
        lbl1.move(10+marginX, 25+marginY)
        lbl1.resize(200, 20)

        self.t1z1 = QtGui.QPushButton('Switch 1', Group_switch)
        self.t1z1.clicked.connect(self.change_state_switch1)
        self.t1z1.resize(self.t1z1.sizeHint())
        self.t1z1.move(200+marginX, 20+marginY)

        self.t1z2 = QtGui.QPushButton('Switch 2', Group_switch)
        self.t1z2.clicked.connect(self.change_state_switch2)
        self.t1z2.resize(self.t1z2.sizeHint())
        self.t1z2.move(300+marginX, 20+marginY)

        # tor 2
        lbl2 = QtGui.QLabel("Route: Kielpinek <-> Wrzeszcz:", Group_switch)
        lbl2.move(10+marginX, 65+marginY)
        lbl2.resize(200, 20)

        self.t2z1 = QtGui.QPushButton('Switch 3', Group_switch)
        self.t2z1.clicked.connect(self.change_state_switch3)
        self.t2z1.resize(self.t2z1.sizeHint())
        self.t2z1.move(200+marginX, 60+marginY)

        self.t2z2 = QtGui.QPushButton('Switch 4', Group_switch)
        self.t2z2.clicked.connect(self.change_state_switch4)
        self.t2z2.resize(self.t2z2.sizeHint())
        self.t2z2.move(300+marginX, 60+marginY)

        self.target = QtGui.QComboBox(Group_switch)
        self.target.addItem('dziala')
        self.target.addItem('dziala_bardziej')

        #self.target.currentIndex()

        self.system_start = QtGui.QPushButton('Start system', Group_switch)
        self.system_start.clicked.connect(self.RUN_system_RUN)

        return Group_switch

    # podgrupa kontrolek do łączenia się z pociągami oraz wyboru typu sterowania
    def tooolbar_traincontrol(self):
        Group_traincontrol = QtGui.QGroupBox(self)
        Group_traincontrol.setTitle("Train control")
        Group_traincontrol.setMinimumSize(170, 100)

        lbl1 = QtGui.QLabel("Connection with trains: ", Group_traincontrol)
        lbl1.resize(200, 20)
        lbl1.move(30, 15)

        self.conn_button = QtGui.QPushButton('Connect', Group_traincontrol)
        self.conn_button.clicked.connect(self.connect_disconnect)
        self.conn_button.resize(100, 30)
        self.conn_button.move(35, 35)

        lbl2 = QtGui.QLabel("Control type: ", Group_traincontrol)
        lbl2.resize(200, 20)
        lbl2.move(15, 70)

        self.auto_btn = QtGui.QPushButton('Auto', Group_traincontrol)
        self.auto_btn.clicked.connect(self.setAutoControl)
        self.auto_btn.resize(70, 20)
        self.auto_btn.move(10, 95)

        self.manual_btn = QtGui.QPushButton('Manual', Group_traincontrol)
        self.manual_btn.clicked.connect(self.setManualControl)
        self.manual_btn.resize(70, 20)
        self.manual_btn.move(90, 95)

        return Group_traincontrol
    # ********************************

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

        self.slider_speed = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_speed.setMinimum(0)
        self.slider_speed.setMaximum(427)
        self.slider_speed.setValue(0)
        self.slider_speed.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slider_speed.setTickInterval(5)
        #self.slider_speed.sliderReleased.connect(self.tUpdate)
        self.slider_speed.valueChanged.connect(self.symulate_kalman_slider)

        self.speed_label = QtGui.QLabel("Speed: " +  str(self.slider_speed.value()), self)
        self.speed_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.speed_label)
        layout.addWidget(self.slider_speed)

        slider = QtGui.QWidget()
        slider.setLayout(layout)

        return slider

    # **********************************
    # --- FUNKCJE OBSŁUGI PRZYCISKÓW ---
    # **********************************

    #aktualizacjia wyboru pociagu
    def tUpdate(self):
        self.speed_label.setText("Speed: " +  str(self.slider_speed.value()))
        if self.forward_radio.isChecked():
            direct = direction["Forward"]
        else:
            direct = direction["Backward"]

        if self.btn1.isChecked():
            self.index_t = 0
            self.trains_speed[0] = self.slider_speed.value()
            self.lab1.setText(str(self.trains_speed[0]))
            #ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[0].move(self.slider_speed.value(), direct)

        elif self.btn2.isChecked():
            self.index_t = 1
            self.trains_speed[1] = self.slider_speed.value()
            self.lab2.setText(str(self.trains_speed[1]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[1].move(self.slider_speed.value(), direct)

        elif self.btn3.isChecked():
            self.index_t = 2
            self.trains_speed[2] = self.slider_speed.value()
            self.lab3.setText(str(self.trains_speed[2]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[2].move(self.slider_speed.value(), direct)

        elif self.btn4.isChecked():
            self.index_t = 3
            self.trains_speed[3] = self.slider_speed.value()
            self.lab4.setText(str( self.trains_speed[3]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[3].move(self.slider_speed.value(), direct)

        elif self.btn5.isChecked():
            self.index_t = 4
            self.trains_speed[4] = self.slider_speed.value()
            self.lab5.setText(str(self.trains_speed[4]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[4].move(self.slider_speed.value(), direct)

        elif self.btn6.isChecked():
            self.index_t = 5
            self.trains_speed[5] = self.slider_speed.value()
            self.lab6.setText(str(self.trains_speed[5]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[5].move(self.slider_speed.value(), direct)

        self.map.repaint()
        if self.msg is not None and self.client.connected:
            self.client.send(self.msg)
            sleep(1)  # Czekaj 1s
            self.msg = None

    def change_state_switch1(self):
        self.t1z1.setEnabled(False)
        # zmiana zwrotnicy w GUI
        self.map.switch1.neg_status()
        self.map.repaint()
        # rzeczywista zmiana zwrotnicy
        try:
            if self.map.switch1.status:
                self.zwrotnice_[0].lewo()
            else:
                self.zwrotnice_[0].prawo()
        except Exception as message:
            QMessageBox.warning(self, 'Zwrotnica', str(message), QMessageBox.Ok)
        sleep(0.2)
        self.t1z1.setEnabled(True)

    def change_state_switch2(self):
        self.t1z2.setEnabled(False)
        # zmiana zwrotnicy w GUI
        self.map.switch2.neg_status()
        # rzeczywista zmiana zwrotnicy
        try:
            if self.map.switch2.status:
                self.zwrotnice_[1].lewo()
            else:
                self.zwrotnice_[1].prawo()
        except Exception as message:
            QMessageBox.warning(self, 'Zwrotnica', str(message), QMessageBox.Ok)
        sleep(0.2)
        self.t1z2.setEnabled(True)
        self.map.repaint()

    def change_state_switch3(self):
        self.t2z1.setEnabled(False)
        # zmiana zwrotnicy w GUI
        self.map.switch3.neg_status()
        # rzeczywista zmiana zwrotnicy
        try:
            if self.map.switch3.status:
                self.zwrotnice_[2].lewo()
            else:
                self.zwrotnice_[2].prawo()
        except Exception as message:
            QMessageBox.warning(self, 'Zwrotnica', str(message), QMessageBox.Ok)
        sleep(0.2)
        self.t2z1.setEnabled(True)
        self.map.repaint()

    def change_state_switch4(self):
        self.t2z2.setEnabled(False)
        # zmiana zwrotnicy w GUI
        self.map.switch4.neg_status()
        # rzeczywista zmiana zwrotnicy
        try:
            if self.map.switch4.status:
                self.zwrotnice_[3].lewo()
            else:
                self.zwrotnice_[3].prawo()
        except Exception as message:
            QMessageBox.warning(self, 'Zwrotnica', str(message), QMessageBox.Ok)
        sleep(0.2)
        self.t2z2.setEnabled(True)
        self.map.repaint()


    def checkLinesAvaliability(self, trainNumber, start, destination, train1, train2):
        self.part_left, self.part_up, self.part_down, self.part_right = 1; #wolne

        if(start == "Wrzeszcz"):
            if(destination == "Strzyza"):
                if(trainNumber == 5):
                    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
                elif(trainNumber == 1):
                    train2place = self.map.train2.actualTrack.getActualTrack()
                    if(train2place[0] == "PART_LEFT"):
                        self.part_left = 0 # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif(train2place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif(train2place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down= 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne

                else:
                    train1place = self.map.train1.actualTrack.getActualTrack()
                    if (train1place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train1place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train1place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne


        if (start == "Wrzeszcz"):
            if (destination == "Kielpinek"):
                if (trainNumber == 5):
                    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
                elif (trainNumber == 1):
                    train2place = self.map.train2.actualTrack.getActualTrack()
                    if (train2place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train2place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train2place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne
                else:
                    train1place = self.map.train1.actualTrack.getActualTrack()
                    if (train1place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train1place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train1place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne
        if (start == "Strzyza"):
            if (destination == "Kielpinek"):
                if (trainNumber == 5):
                    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
                elif (trainNumber == 1):
                    train2place = self.map.train2.actualTrack.getActualTrack()
                    if (train2place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train2place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train2place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne
                else:
                    train1place = self.map.train1.actualTrack.getActualTrack()
                    if (train1place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train1place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train1place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne
        if (start == "Kielpinek"):
            if (destination == "Strzyza"):
                if (trainNumber == 5):
                    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
                elif (trainNumber == 1):
                    train2place = self.map.train2.actualTrack.getActualTrack()
                    if (train2place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train2place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train2place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne
                else:
                    train1place = self.map.train1.actualTrack.getActualTrack()
                    if (train1place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train1place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train1place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne
        if (start == "Kielpinek"):
            if (destination == "Wrzeszcz"):
                if (trainNumber == 5):
                    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
                elif (trainNumber == 1):
                    train2place = self.map.train2.actualTrack.getActualTrack()
                    if (train2place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train2place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train2place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne
                else:
                    train1place = self.map.train1.actualTrack.getActualTrack()
                    if (train1place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train1place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train1place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne
        if (start == "Strzyza"):
            if (destination == "Wrzeszcz"):
                if (trainNumber == 5):
                    self.part_left, self.part_up, self.part_down, self.part_right = 1;  # wolne
                elif (trainNumber == 1):
                    train2place = self.map.train2.actualTrack.getActualTrack()
                    if (train2place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train2place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train2place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne
                else:
                    train1place = self.map.train1.actualTrack.getActualTrack()
                    if (train1place[0] == "PART_LEFT"):
                        self.part_left = 0  # zajete
                        self.part_up, self.part_down, self.part_right = 1;  # wolne
                    elif (train1place[0] == "PART_RIGHT"):
                        self.part_right = 0  # zajete
                        self.part_up, self.part_down, self.part_left = 1;  # wolne
                    elif (train1place[0] == "PART_UP"):
                        self.part_up = 0  # zajete
                        self.part_right, self.part_down, self.part_left = 1;  # wolne
                    else:
                        self.part_down = 0  # zajete
                        self.part_right, self.part_up, self.part_left = 1;  # wolne

        if (start == "Wrzeszcz"):
            if (destination == "Osowa"):
                    self.part_right, self.part_up, self.part_left, self.part_down = 1;  # wolne
        if (start == "Osowa"):
            if (destination == "Wrzeszcz"):
                    self.part_right, self.part_up, self.part_left, self.part_down = 1;  # wolne

        return self.part_right, self.part_up, self.part_left, self.part_down

    def RUN_system_RUN(self):
        print("index", self.target.currentIndex())
        #if(self.map.train1.actual_track_section_l0 == 23):
        self.tablicaPPPP = [self.map.train1,self.map.train2,self.map.train3,self.map.train4]
        tab_length = len(self.tablicaPPPP)
        for i in range(tab_length):
            if(i == 0):
                if(self.tablicaPPPP[i].actual_track_section_l0 != 23 and self.tablicaPPPP[i].actual_track_section_l1 != 23):
                    text11 = "Stacja Kielpinek wolna"
                    print('Stacja Kielpinek wolna')
                else:
                    text11 = "Stacja Kielpinek zajeta"
                    print("Stacja Kielpinek zajeta")
                if(self.tablicaPPPP[i].actual_track_section_l0 != 0 and self.tablicaPPPP[i].actual_track_section_l1 != 0):
                    text12 = "Stacja Wrzeszcz wolna"
                else:
                    text12 = "Stacja Wrzeszcz zajeta"
                if(self.tablicaPPPP[i].actual_track_section_l0 >=20 and self.tablicaPPPP[i].actual_track_section_l0 < 23 and self.tablicaPPPP[i].actual_track_section_l1 >=20 and self.tablicaPPPP[i].actual_track_section_l1 < 23):
                    text13 = "odcinek od zwrotnicy do stacji Kilpinek jest zajety" #za zwrotnica, zwortnica: 19
                else:
                    text13 = "odcinek od zwrotnicy do stacji Kilpinek jest wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 > 13 and self.tablicaPPPP[i].actual_track_section_l0 < 19):
                    text14 = "odcinek od stacji Strzyza do zwrotnicy jest zajety"
                else:
                    text14 = "odcinek od zwrotnicy do stacji Strzyza jest wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 >= 6 and self.tablicaPPPP[i].actual_track_section_l0 <= 12):
                    text15 = "odcinek od zwrotnicy do stacji Strzyza jest zajety"  #od balisy przed zwrotnica(6)
                else:
                    text15 = "odcinek od zwrotnicy do stacji Kilpinek jest wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 > 0 and self.tablicaPPPP[i].actual_track_section_l0 <= 6 and self.tablicaPPPP[i].actual_track_section_l1 <= 6 and self.tablicaPPPP[i].actual_track_section_l1 > -1):
                    text16 = "odcinek od stacji Wrzeszcz do zwrotnicy jest zajety"
                else:
                    text16 = "odcinek od stacji Wrzeszcz do zwrotnicy jest wolny"
                if (self.tablicaPPPP[i].actual_track_section_l0 == 13 and self.tablicaPPPP[i].actual_track_section_l1 == -1):
                    text17 = "stacja Strzyza jest zajeta"
                else:
                    text17 = "stacja Strzyza jest wolna"

            elif(i == 1):
                if(self.tablicaPPPP[i].actual_track_section_l0 != 0 and self.tablicaPPPP[i].actual_track_section_l1 != 0):
                    text21 = "Stacja Wzreszcz wolna"
                    print("Stacja Wzreszcz wolna")
                else:
                    text21 = "Stacja Wzreszcz zajeta"
                    print("Stacja Wzreszcz zajeta")
                if (self.tablicaPPPP[i].actual_track_section_l0 >= 20 and self.tablicaPPPP[i].actual_track_section_l0 < 23 and self.tablicaPPPP[i].actual_track_section_l1 >= 20 and self.tablicaPPPP[i].actual_track_section_l1 < 23):
                    text22 = "odcinek od stacji Kilpinek do zwrotnicy jest zajety"  # za zwrotnica, zwortnica: 19
                else:
                    text22 = "odcinek od stacji Kilpinek do zwrotnicy jest wolny"
                if (self.tablicaPPPP[i].actual_track_section_l0 > 13 and self.tablicaPPPP[i].actual_track_section_l0 < 19):
                    text23 = "odcinek od zwrotnicy do stacji Strzyza jest zajety"
                else:
                    text23 = "odcinek od zwrotnicy do stacji Strzyza jest wolny"
                if (self.tablicaPPPP[i].actual_track_section_l0 >= 6 and self.tablicaPPPP[i].actual_track_section_l0 <= 12):
                    text24 = "odcinek od stacji Strzyza do zwrotnicy jest zajety"  # od balisy przed zwrotnica(6)
                else:
                    text24 = "odcinek od stacji Strzyza do zwrotnicy jest wolny"
                if (self.tablicaPPPP[i].actual_track_section_l0 > 0 and self.tablicaPPPP[i].actual_track_section_l0 <= 6 and self.tablicaPPPP[i].actual_track_section_l1 <= 6 and self.tablicaPPPP[i].actual_track_section_l1 > -1):
                    text25 = "odcinek od zwrotnicy do stacji Wrzeszcz jest zajety"
                else:
                    text25 = "odcinek od zwrotnicy do stacji Wrzeszcz jest wolny"
                if (self.tablicaPPPP[i].actual_track_section_l0 == 23 and self.tablicaPPPP[i].actual_track_section_l1 == 23):
                    text26 = "stacja Kielpinek jest zajeta"
                else:
                    text26 = "stacja Kielpinek jest wolna"
                if (self.tablicaPPPP[i].actual_track_section_l0 == 13 and self.tablicaPPPP[i].actual_track_section_l1 == -1):
                    text27 = "stacja Strzyza jest zajeta"
                else:
                    text27 = "stacja Strzyza jest wolna"


            elif(i == 2):
                if(self.tablicaPPPP[i].actual_track_section_l0 != 27 and self.tablicaPPPP[i].actual_track_section_l1 != 15):
                    text31 = "Stacja Wzreszcz jest wolna"
                else:
                    text31 = "Stacja Wzreszcz jest zajeta"
                if(self.tablicaPPPP[i].actual_track_section_l0 != 22 and self.tablicaPPPP[i].actual_track_section_l1 != 22):
                    text32 = "Stacja Osowa jest wolna"
                else:
                    text32 = "Stacja Osowa jest zajeta"
                if(self.tablicaPPPP[i].actual_track_section_l0 <=4 and self.tablicaPPPP[i].actual_track_section_l1 <=4 and self.tablicaPPPP[i].actual_track_section_l1 > -1):
                    text33 = "odcinek od stacji Wrzeszcz do zwrotnicy jest zajety"
                else:
                    text33 = "odcinek od stacji Wrzeszcz do zwrotnicy jest wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 > 4 and self.tablicaPPPP[i].actual_track_section_l0 <19 and self.tablicaPPPP[i].actual_track_section_l1 == -1):
                    text34 = "odcinek od zwrotnicy do balisy przed stacją Osowa zajety"
                else:
                    text34 = "odcinek od zwrotnicy do balisy przed stacją Osowa wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 > 20 and self.tablicaPPPP[i].actual_track_section_l0 < 22 and self.tablicaPPPP[i].actual_track_section_l1 == -1):
                    text35 = "odcinek od balisy przed stacją Osowa do Stacji Osowa zajety"
                else:
                    text35 = "odcinek od balisy przed stacją Osowa do Stacji Osowa wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 > 22 and self.tablicaPPPP[i].actual_track_section_l0 < 24 and self.tablicaPPPP[i].actual_track_section_l1 == -1):
                    text36 = "odcinek od stacji Osowa do zwrotnicy zajety"
                else:
                    text36 = "odcinek od stacji Osowa do zwrotnicy wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 > 24 and self.tablicaPPPP[i].actual_track_section_l0 <= 27 and self.tablicaPPPP[i].actual_track_section_l1 == 15):
                    text37 = "odcinek od zwrotnicy do konca toru jest zajety"
                else:
                    text37 = "odcinek od zwrotnicy do konca toru jest wolny"

            elif(i == 3):
                if(self.tablicaPPPP[i].actual_track_section_l0 < 27 and self.tablicaPPPP[i].actual_track_section_l0 > 24 and self.tablicaPPPP[i].actual_track_section_l1 < 15 and self.tablicaPPPP[i].actual_track_section_l1 > 13):
                    text41 = "odcinek od zwrotnicy do konca toru jest zajety"
                else:
                    text41 = "odcinek od zwrotnicy do konca toru jest wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 > 22 and self.tablicaPPPP[i].actual_track_section_l0 < 24 and self.tablicaPPPP[i].actual_track_section_l1 == -1):
                    text42 = "odcinek od stacji Osowa do zwrotnicy zajety"
                else:
                    text42 = "odcinek od stacji Osowa do zwrotnicy wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 != 22 and self.tablicaPPPP[i].actual_track_section_l1 != 22):
                    text43 = "Stacja Osowa jest wolna"
                else:
                    text43 = "Stacja Osowa jest zajeta"
                if(self.tablicaPPPP[i].actual_track_section_l0 > 20 and self.tablicaPPPP[i].actual_track_section_l0 < 22 and self.tablicaPPPP[i].actual_track_section_l1 == -1):
                    text44 = "odcinek od Stacji Osowa do balisy przed stacją Osowa zajety"
                else:
                    text44 = "odcinek od Stacji Osowa do balisy przed stacją Osowa wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 > 4 and self.tablicaPPPP[i].actual_track_section_l0 < 19 and self.tablicaPPPP[i].actual_track_section_l1 == -1):
                    text45 = "odcinek od balisy przed stacją Osowa do zwrotnicy zajety"
                else:
                    text45 = "odcinek od balisy przed stacją Osowa do zwrotnicy wolny"
                if(self.tablicaPPPP[i].actual_track_section_l0 <= 4 and self.tablicaPPPP[i].actual_track_section_l1 <= 4 and self.tablicaPPPP[i].actual_track_section_l1 > -1):
                    text46 = "odcinek od zwrotnicy do stacji Wrzeszcz jest zajety"
                else:
                    text46 = "odcinek od zwrotnicy do stacji Wrzeszcz jest wolny"
                if (self.tablicaPPPP[i].actual_track_section_l0 != 0 and self.tablicaPPPP[i].actual_track_section_l1 != 0):
                    text43 = "Stacja Wrzeszcz jest wolna"
                else:
                    text43 = "Stacja Wrzeszcz jest zajeta"


    # łączenie i rozłączenie z pociągami
    def connect_disconnect(self):
        if self.client.connected:
            self.stopAllTrains()
            #self.client.stop_all_locomotives()
            self.client.disconnect()
            self.conn_button.setText("Connect")
        else:
            try:
                self.client.connect(TCP_IP, TCP_PORT)
                if not self.client.connected: raise Exception('Proba polaczenia nie powiodla sie.')
                self.conn_button.setText("Disconnect")
            except Exception as message:
                QMessageBox.warning(self, 'Polaczenie', str(message) +
                                    "\nStrona nie odpowiedziala poprawnie po ustalonym czasie lub utworzone polaczenie nie powiodlo sie," +
                                    " poniewaz polaczony host nie odpowiada.", QMessageBox.Ok)

    # ustawienie sterowania pociagiem automatycznie
    def setAutoControl(self):
        #self.enableButtons(False)
        self.autoControl = True

        #self.rozklad()
        self.map.kalman_trains = self.kalman_train
        self.map.createTrains()
        self.map.setAutoControl(self.autoControl)

    # ustawienie sterowania pociagiem ręcznie
    def setManualControl(self):
        self.stopAllTrains()
        self.enableButtons(True)
        self.autoControl = False
        self.map.setAutoControl(self.autoControl)

    def stopTrain(self):
        if self.client.connected:
            self.slider_speed.setValue(0)
            self.msg = self.trains[self.index_t].move(0, 0)
            self.client.send(self.msg)
            sleep(1)  # Czekaj 1s

    def stopAllTrains(self):
        if self.client.connected:
            #msg = self.client.stop_all_locomotives()
            for i in  range(6):
                msg = Train(i).move(0)
                self.client.send(msg)
            for i in range(4):
                self.kalman_train[i] = None
            self.stop_all_timers()

    def enableButtons(self, state):
        # radiobuttony
        self.btn1.setEnabled(state)
        self.btn2.setEnabled(state)
        self.btn3.setEnabled(state)
        self.btn4.setEnabled(state)
        self.btn5.setEnabled(state)
        self.btn6.setEnabled(state)
        # przyciskizwrotnic
        self.t1z1.setEnabled(state)
        self.t1z2.setEnabled(state)
        self.t2z1.setEnabled(state)
        self.t2z2.setEnabled(state)
        # przyciski sterowania ruchem pociagu
        self.stop_button.setEnabled(state)
        self.forward_radio.setEnabled(state)
        self.backward_radio.setEnabled(state)
        # suwak prędkości
        self.slider_speed.setEnabled(state)

    # ***************************************

    def resizeEvent(self, event):
        self.map.setscale()

    def symulate_kalman_slider(self):
        self.map.sym_kalman = 4*self.slider_speed.value()
        self.map.repaint()

    def rozklad(self):
        self.timer_glowny.start(50, self)

        self.trasa1 = ['03050066', '0305006E', '03010067', '03020067', '03020065'] # wrzeszcz -> kielpinek
        self.trasa2 = ['03020065', '03020068', '03010000', '03010068', '0305006D', '03050066']# kielpinek -> wrzeszcz
        self.trasa3 = ['0304012E', '0304012D'] # wrzeszcz -> osowa
        self.trasa4 = ['0304012D', '0304012F'] # osowa -> wrzeszcz

        self.train_list = []
        self.map.switch1.neg_status()
        self.map.switch3.neg_status()
        #self.kalman_train = []

        self.licznik_balis = [0, 0, 0, 0]
        self.etap_trasy = [0, 0, 0, 0]
        self.dojechal = [False, False]
        self.dojechal2 = [False, False]
        self.hamowanie = [50,0]

        self.poc2sw = True
        self.poc5sw = True

        #Pociag nr 1 - trasa 1 - ustawic na Wrzeszczu

        self.train_list.append(Train(1))
        self.train_list.append(Train(2))
        self.train_list.append(Train(5))
        self.train_list.append(Train(6))

        self.kalman_train = None
        self.kalman_train = []
        model_train = kalman.Model(11)
        self.kalman_train.append(model_train)
        model_train = kalman.Model(22)
        self.kalman_train.append(model_train)
        model_train = kalman.Model(5)
        self.kalman_train.append(model_train)
        model_train = kalman.Model(6)
        self.kalman_train.append(model_train)

        print((self.kalman_train[0].get_position()), (self.kalman_train[1].get_position()), (self.kalman_train[2].get_position()), (self.kalman_train[3].get_position()))

        #1 na Wrzeszczu
        self.kalman_train[0].set_power(65)
        msg = self.train_list[0].move(65, direction["Forward"])
        self.client.send(msg)

        #2 na Kielpinku
        self.kalman_train[1].set_power(65)
        msg = self.train_list[1].move(65, direction["Backward"])
        self.client.send(msg)

        #pociag 5 wykoleja sie na zwrotnicy przy Wrzeszczu, wiec nie uzywac
        '''#5 na Wrzeszczu
        self.kalman_train[2].set_power(65)
        msg = self.train_list[2].move(65, direction["Backward"])
        self.client.send(msg)'''

        #zeby nr 6 zczal jezdzic na swojej trasie trzeba odkomentowac fragment ponizej
        #6 na osowej
        #self.kalman_train[3].set_power(65)
        #msg = self.train_list[3].move(65, direction["Forward"])
        #self.client.send(msg)

        #self.zwrotnice_[3].prawo()                                                              #UWAGA ZWROTNICA

    def createTimers(self):
        self.timer_glowny = QBasicTimer()
        self.timer_postoj_s_w = QBasicTimer()
        self.timer_postoj_w_s = QBasicTimer()
        self.timer_postoj_s = QBasicTimer()
        self.timer_postoj_w = QBasicTimer()
        self.timer_postoj_wrzeszcz = QBasicTimer()
        self.timer_postoj_osowa = QBasicTimer()
        self.timer_postoj_w_o = QBasicTimer()
        self.timer_postoj_o_w = QBasicTimer()

    def stop_all_timers(self):
        self.timer_glowny.stop()
        self.timer_postoj_s_w.stop()
        self.timer_postoj_w_s.stop()
        self.timer_postoj_s.stop()
        self.timer_postoj_w.stop()
        self.timer_postoj_wrzeszcz.stop()
        self.timer_postoj_osowa.stop()
        self.timer_postoj_w_o.stop()
        self.timer_postoj_o_w.stop()

    def postoj_s_w(self):
        self.timer_postoj_s_w.start(10000, self)

    def postoj_w_s(self):
        self.timer_postoj_w_s.start(10000, self)

    def postoj_s(self):
        self.timer_postoj_s.start(10000, self)

    def postoj_w(self):
        self.timer_postoj_w.start(10000, self)

    def postoj_wrzeszcz(self):
        self.timer_postoj_wrzeszcz.start(10000, self)

    def postoj_osowa(self):
        self.timer_postoj_osowa.start(10000, self)

    def postoj_w_o(self):
        self.timer_postoj_w_o.start(10000, self)

    def postoj_o_w(self):
        self.timer_postoj_o_w.start(10000, self)

    def zamiena_tras(self):
        if self.poc2sw:
            self.poc2sw = False
            model_train = kalman.Model(21)  #model
            self.kalman_train[0] = model_train
            self.etap_trasy[0] = 0
            self.licznik_balis[0] = 0
            self.train_list[0] = Train(2)   #xpressnet
            model_train = kalman.Model(12)
            self.kalman_train[1] = model_train
            self.etap_trasy[1] = 0
            self.licznik_balis[1] = 0
            self.train_list[1] = Train(1)   #xpressnet
            self.hamowanie = [0,50]
            #---------------------------
            # zmiana rysowania w GUI
            self.map.train1.kalman_train = self.kalman_train[1]
            self.map.train2.kalman_train = self.kalman_train[0]
            self.map.train1.negReverse()
            self.map.train2.negReverse()
            temp = self.map.train1.x_init
            self.map.train1.x_init = self.map.train2.x_init
            self.map.train2.x_init = temp
            #---------------------------
        else:
            self.poc2sw = True
            model_train = kalman.Model(22)  #model
            self.kalman_train[1] = model_train
            self.etap_trasy[1] = 0
            self.licznik_balis[1] = 0
            self.train_list[1] = Train(2)   #xpressnet
            model_train = kalman.Model(11)
            self.kalman_train[0] = model_train
            self.etap_trasy[0] = 0
            self.licznik_balis[0] = 0
            self.train_list[0] = Train(1)   #xpressnet
            self.hamowanie = [50,0]
            #---------------------------
            # zmiana rysowania w GUI
            self.map.train1.kalman_train = self.kalman_train[0]
            self.map.train2.kalman_train = self.kalman_train[1]
            self.map.train1.negReverse()
            self.map.train2.negReverse()
            temp = self.map.train1.x_init
            self.map.train1.x_init = self.map.train2.x_init
            self.map.train2.x_init = temp
            #---------------------------

    #wrzeszcz - osowa
    def zamiena_tras2(self):
        #odkomentowanie dwoch fragmentow ponizej umozliwia dolaczenie do tej trasy pociagu nr 5 (por. rozklad)
        if self.poc5sw:
            self.poc5sw = False
            model_train = kalman.Model(6)  #model
            self.kalman_train[2] = model_train
            self.etap_trasy[2] = 0
            self.licznik_balis[2] = 0
            self.train_list[2] = Train(6)   #xpressnet
            '''model_train = kalman.Model(5)  #model
            self.kalman_train[3] = model_train
            self.etap_trasy[3] = 0
            self.licznik_balis[3] = 0
            self.train_list[3] = Train(5)   #xpressnet'''

            #---------------------------
            # zmiana rysowania w GUI
            self.map.train3.kalman_train = self.kalman_train[3]
            self.map.train4.kalman_train = self.kalman_train[2]
            self.map.train3.negReverse()
            self.map.train4.negReverse()
            temp = self.map.train3.x_init
            self.map.train3.x_init = self.map.train4.x_init
            self.map.train4.x_init = temp
            #---------------------------
        else:
            self.poc5sw = True
            model_train = kalman.Model(6)  #model
            self.kalman_train[3] = model_train
            self.etap_trasy[3] = 0
            self.licznik_balis[3] = 0
            self.train_list[3] = Train(6)   #xpressnet
            '''model_train = kalman.Model(5)  #model
            self.kalman_train[2] = model_train
            self.etap_trasy[2] = 0
            self.licznik_balis[2] = 0
            self.train_list[2] = Train(5)   #xpressnet'''
            #---------------------------
            # zmiana rysowania w GUI
            self.map.train3.kalman_train = self.kalman_train[2]
            self.map.train4.kalman_train = self.kalman_train[3]
            self.map.train3.negReverse()
            self.map.train4.negReverse()
            temp = self.map.train3.x_init
            self.map.train3.x_init = self.map.train4.x_init
            self.map.train4.x_init = temp

    def timerEvent(self, event):
        if event.timerId() == self.timer_glowny.timerId():
            c.acquire()
            can_adres = adres
            c.release()
            self.map.repaint()

            #Kielpinek -> Wrzeszcz
            if (can_adres == self.trasa2[self.licznik_balis[1]]):
                if (self.licznik_balis[1] == 0):        #balisa tuz za peronem
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 1 tuz za peronem')
                    self.kalman_train[1].update(10.5)
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 1 tuz za peronem')
                elif (self.licznik_balis[1] == 1):      #balisa kolo wiaduktu
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 2 kolo wiaduktu')
                    self.kalman_train[1].update(279.5)
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 2 kolo wiaduktu')
                elif (self.licznik_balis[1] == 2):      #przed strzyza
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 3 przed strzyza')
                    self.kalman_train[1].update(503)
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 3 przed strzyza')
                elif (self.licznik_balis[1] == 3):      #za strzyza
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 4 za strzyza')
                    self.kalman_train[1].update(149)
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 4 za strzyza')
                elif (self.licznik_balis[1] == 4):      #koniec zjazdu
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 5 koniec zjazdu')
                    self.kalman_train[1].update(243)
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 5 koniec zjazdu')
                elif (self.licznik_balis[1] == 5):
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 6 wrzeszcz peron')
                    self.kalman_train[1].update(215.5)
                    print((self.kalman_train[1].get_position()), ' k -> w balisa 6 wrzeszcz peron')
                    self.licznik_balis[1] = 0

                self.licznik_balis[1] += 1

            #Wrzeszcz -> Kielpinek
            if (can_adres == self.trasa1[self.licznik_balis[0]]):
                if (self.licznik_balis[0] == 0):        #gdzies przy wrzeszczu
                    print((self.kalman_train[0].get_position()), ' w -> k balisa 1 tuz za peronem')
                    self.kalman_train[0].update(5)
                    print((self.kalman_train[0].get_position()), ' w -> k balisa 1 tuz za peronem')
                elif (self.licznik_balis[0] == 1):      #podjazd
                    print((self.kalman_train[0].get_position()), ' w -> k balisa 2 podjazd')
                    self.kalman_train[0].update(215.5)
                    print((self.kalman_train[0].get_position()), ' w -> k balisa 2 podjazd')
                elif (self.licznik_balis[0] == 2):      #przed strzyza
                    print((self.kalman_train[0].get_position()), ' w -> k balisa 3 przed strzyza')
                    self.kalman_train[0].update(249)
                    print((self.kalman_train[0].get_position()), ' w -> k balisa 3 przed strzyza')
                elif (self.licznik_balis[0] == 3):      #okolice wiaduktu
                    print((self.kalman_train[0].get_position()), ' w -> k balisa 4 okolice wiaduktu')
                    self.kalman_train[0].update(672)
                    print((self.kalman_train[0].get_position()), ' w -> k balisa 4 okolice wiaduktu')
                elif (self.licznik_balis[0] == 4):      #kielpinek
                    print((self.kalman_train[0].get_position()), ' w -> k balisa 5 stacja kielpinek')
                    self.kalman_train[0].update(278.5)
                    print((self.kalman_train[0].get_position()), ' w -> k balisa 5 stacja kielpinek')
                    self.licznik_balis[0] = 0

                self.licznik_balis[0] += 1

            if self.kalman_train[1].get_position() > 888 - self.hamowanie[1] and self.etap_trasy[1] == 0:
                print('na strzyza dojechal z kielpinka')
                print((self.kalman_train[1].get_position()))
                msg = self.train_list[1].move(0)
                self.client.send(msg)
                self.kalman_train[1].set_power(0)
                self.etap_trasy[1] = 1     #wynosi wiec 4, a licznik balis nadal 3
                self.postoj_s_w()

            if self.kalman_train[1].get_position() > 1459 - self.hamowanie[1] and self.etap_trasy[1] == 1:
                print('na wrzeszcz dojechal')
                print((self.kalman_train[1].get_position()))
                msg = self.train_list[1].move(0)
                self.client.send(msg)
                self.kalman_train[1].set_power(0)
                self.etap_trasy[1] = 2     #wynosi wiec 4, a licznik balis nadal 3
                self.dojechal[1] = True
                print(self.dojechal)

            if self.kalman_train[0].get_position() > 530 - self.hamowanie[0] and self.etap_trasy[0] == 0:
                print('na strzyza dojechal z wrzeszcza')
                print((self.kalman_train[0].get_position()))
                msg = self.train_list[0].move(0, direction["Forward"])
                self.client.send(msg)
                self.kalman_train[0].set_power(0)
                self.etap_trasy[0] = 1
                self.postoj_w_s()

            if self.kalman_train[0].get_position() > 1479 - self.hamowanie[0] and self.etap_trasy[0] == 1:   #1415 balisa przed kielpinkiem
                print('na kielpinek dojechal')
                print((self.kalman_train[0].get_position()))
                self.kalman_train[0].set_power(0)
                msg = self.train_list[0].move(0, direction["Forward"])
                self.client.send(msg)
                self.etap_trasy[0] = 2
                self.dojechal[0] = True
                print(self.dojechal)

            if self.dojechal[0] and self.dojechal[1]:
                self.dojechal[0] = False
                self.dojechal[1] = False
                self.postoj_w()
                self.postoj_s()
                self.zamiena_tras()


    ##wrzeszcz - osowa (poc 5)
            if (can_adres == self.trasa3[self.licznik_balis[2]]):
                if (self.licznik_balis[2] == 0):
                    print((self.kalman_train[2].get_position()))
                    self.kalman_train[2].update(580)
                elif (self.licznik_balis[2] == 1):
                    print((self.kalman_train[2].get_position()))
                    self.kalman_train[2].update(905)
                    self.licznik_balis[2] = 0

                self.licznik_balis[2] += 1

            if self.kalman_train[2].get_position() > 915 and self.etap_trasy[2] == 0:
                msg = self.train_list[2].move(0, direction["Backward"])
                print((self.kalman_train[3].get_position()))
                self.kalman_train[2].set_power(0)
                self.client.send(msg)
                self.etap_trasy[2] = 1
                self.postoj_o_w()

    ############Osowa - Wrzeszcz (poc 6)
            if (can_adres == self.trasa4[self.licznik_balis[3]]):
                if (self.licznik_balis[3] == 0):
                    print((self.kalman_train[3].get_position()))
                    self.postoj_osowa()
                    self.licznik_balis[3] += 1
                    #self.dojechal2[0] = True
                elif (self.licznik_balis[3] == 1):
                    print((self.kalman_train[3].get_position()))
                    self.kalman_train[3].update(340)
                    self.licznik_balis[3] = 0

            if self.kalman_train[3].get_position() > 100 and self.etap_trasy[3] == 0:
                msg = self.train_list[3].move(0, direction["Forward"])
                print((self.kalman_train[3].get_position()))
                self.kalman_train[3].set_power(0)
                self.client.send(msg)
                self.postoj_osowa()
                self.etap_trasy[3] = 1

            if self.kalman_train[3].get_position() > 940 and self.etap_trasy[3] == 1:
                msg = self.train_list[3].move(0, direction["Forward"])
                print((self.kalman_train[3].get_position()))
                self.kalman_train[3].set_power(0)
                self.client.send(msg)
                self.postoj_w_o()
                self.etap_trasy[3] = 2

        #Ruszanie po postoju na peronie
        if event.timerId() == self.timer_postoj_s_w.timerId():

            msg = self.train_list[1].move(65)
            self.kalman_train[1].set_power(65)
            self.client.send(msg)
            self.timer_postoj_s_w.stop()
            self.change_state_switch3()

        if event.timerId() == self.timer_postoj_w.timerId():

            msg = self.train_list[0].move(65, direction["Forward"])
            self.kalman_train[0].set_power(65)
            self.client.send(msg)
            self.timer_postoj_w.stop()
            self.change_state_switch3()

        if event.timerId() == self.timer_postoj_s.timerId():

            msg = self.train_list[1].move(65)
            self.kalman_train[1].set_power(65)
            self.client.send(msg)
            self.timer_postoj_s.stop()
            self.change_state_switch4()

        if event.timerId() == self.timer_postoj_w_s.timerId():

            msg = self.train_list[0].move(65, direction["Forward"])
            self.client.send(msg)
            self.kalman_train[0].set_power(65)
            self.timer_postoj_w_s.stop()
            self.change_state_switch4()

        if event.timerId() == self.timer_postoj_w_o.timerId():

            self.zamiena_tras2()
            msg = self.train_list[2].move(65)
            self.kalman_train[2].set_power(65)
            self.kalman_train[2].update(0)
            self.timer_postoj_w_o.stop()
            self.client.send(msg)
            #self.change_state_switch4()
            self.change_state_switch1()

        if event.timerId() == self.timer_postoj_o_w.timerId():

            self.zamiena_tras2()
            msg = self.train_list[3].move(65, direction["Forward"] )
            self.kalman_train[3].set_power(65)
            self.client.send(msg)
            self.timer_postoj_o_w.stop()
            self.change_state_switch2()

        if event.timerId() == self.timer_postoj_osowa.timerId():

            msg = self.train_list[3].move(65, direction["Forward"])
            self.kalman_train[3].set_power(65)
            self.client.send(msg)
            self.timer_postoj_osowa.stop()
            self.change_state_switch2()
            self.change_state_switch1()


        if event.timerId() == self.timer_requests.timerId():
            r_buff = self.my_requests.text
            j = json.loads(r_buff)
            x = j[-1]
            velocity =  x['velocity']
            print ('velocity:', int(velocity))
            train_identificator =  x['train_identificator']
            print ('train_identificator:', int(train_identificator))

            #{"device_type": "0", "velocity": 3, "train_identificator": 2}

            self.agentsList[train_identificator].newOrder()
            #for i in range(3):
            #    if i != train_identificator:
            #        self.agentsList[i].react()

            self.trains_speed[train_identificator] = velocity
            if self.client.connected:
                if velocity > 0:
                    self.msg = self.trains[train_identificator].move(velocity, 'Forward')
                else:
                    self.msg = self.trains[train_identificator].move(velocity, 'Backward')

            if self.msg is not None and self.client.connected:
                #self.client.send(self.msg)
                sleep(1)  # Czekaj 1s
                self.msg = None

def close_application():
    sys.exit()

def run():
    app = QtGui.QApplication(sys.argv)
    #login = Login()
    #if login.exec_() == QtGui.QDialog.Accepted:
    GUI = Window()
    GUI.show()
    sys.exit(app.exec_())

run()

