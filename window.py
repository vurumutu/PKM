#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.Qt import *

import train_map
import train
import train_auto
import kalman
from CAN import *
import CAN as can
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
        self.train_GUI = train.Train()
        self.msg = None
        self.index_t = 4    #numer wybranego pociagu - 1, bo numerujemy tablice od 0
        self.trains = []
        for i in range(1,7):
            self.trains.append(Train(i))

        self.rozklad()

        # utworzenie obiektu tworzacego mape kolejowa
        self.map = train_map.Railmap(0, 30, self.height(), self.width(), self.kalman_train, self)

        # inicjalizacja zwotnic
        #self.initSwitches()
        self.initLayout()
        self.initUI()
        self.show()


    # INICJALIZACJA ZWROTNIC
    def initSwitches(self):
        # adresy używanych zwrotnic
        addr_zwrotnic_main = ['010501F5', '010401FB', '0105006F', '0102000C']
        # adresy zwrotnic ustawianych tylko przy uruchomieiu programu
        addr_zwrotnic_other = ['010501F7', '010501F8', '010501F9', '010501FA',
                               '01050067', '01050134', '0105006C', '0105006D', '0105006E', '01010065', '01010066', '01020001', '01020002', '0102000B']

        addr_zwrotnic = addr_zwrotnic_main + addr_zwrotnic_other
        self.zwrotnice_ = []
        for address in addr_zwrotnic_main:
            find = False
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
                QMessageBox.warning(self, "Zwrotnice", " Nie znalezono zwrotnicy o adresie: " + address, QMessageBox.Ok)

            # poczatkowe ustawienie zwrotnic
            # numer zwrotnicy : zwrot (False - right, True - Left
            defaultDirect = {
                0 : True,
                1 : False,
                2 : True,
                3 : False
            }
            for num_switch in defaultDirect:
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
        l1 = QtGui.QLabel("Speed", self)
        l1.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(l1)

        self.slider_speed = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.slider_speed.setMinimum(0)
        self.slider_speed.setMaximum(127)
        self.slider_speed.setValue(20)
        self.slider_speed.setTickPosition(QtGui.QSlider.TicksBelow)
        self.slider_speed.setTickInterval(5)
        self.slider_speed.sliderReleased.connect(self.tUpdate)
        #self.slider_speed.valueChanged.connect(self.symulate_kalman_slider)
        layout.addWidget(self.slider_speed)

        slider = QtGui.QWidget()
        slider.setLayout(layout)

        return slider

    # **********************************
    # --- FUNKCJE OBSŁUGI PRZYCISKÓW ---
    # **********************************

    #aktualizacjia wyboru pociagu
    def tUpdate(self):
        if self.forward_radio.isChecked():
            direct = direction["Forward"]
        else:
            direct = direction["Backward"]

        if self.btn1.isChecked():
            self.index_t = 0
            self.train_GUI.setValue(self.slider_speed.value(), self.index_t)
            self.lab1.setText(str(self.train_GUI.getValue()[self.index_t]))
            #ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[0].move(self.slider_speed.value(), direct)

        elif self.btn2.isChecked():
            self.index_t = 1
            self.train_GUI.setValue(self.slider_speed.value(),self.index_t)
            self.lab2.setText(str(self.train_GUI.getValue()[self.index_t]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[1].move(self.slider_speed.value(), direct)

        elif self.btn3.isChecked():
            self.index_t = 2
            self.train_GUI.setValue(self.slider_speed.value(),self.index_t)
            self.lab3.setText(str(self.train_GUI.getValue()[self.index_t]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[2].move(self.slider_speed.value(), direct)

        elif self.btn4.isChecked():
            self.index_t = 3
            self.train_GUI.setValue(self.slider_speed.value(),self.index_t)
            self.lab4.setText(str(self.train_GUI.getValue()[self.index_t]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[3].move(self.slider_speed.value(), direct)

        elif self.btn5.isChecked():
            self.index_t = 4
            self.train_GUI.setValue(self.slider_speed.value(),self.index_t)
            self.lab5.setText(str(self.train_GUI.getValue()[self.index_t]))
            # ustawienie predkosci pociagu wlasciwy:
            if self.client.connected:
                self.msg = self.trains[4].move(self.slider_speed.value(), direct)

        elif self.btn6.isChecked():
            self.index_t = 5
            self.train_GUI.setValue(self.slider_speed.value(),self.index_t)
            self.lab6.setText(str(self.train_GUI.getValue()[self.index_t]))
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

        self.t2z2.setEnabled(True)
        self.map.repaint()

    # łączenie i rozłączenie z pociągami
    def connect_disconnect(self):
        if self.client.connected:
            self.client.stop_all_locomotives()
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
        self.enableButtons(False)
        self.autoControl = True
        # -------------
        # TODO Miejsce na uruchomienie rozkładu jazdy
        # -------------

    # ustawienie sterowania pociagiem ręcznie
    def setManualControl(self):
        self.enableButtons(True)
        self.autoControl = False

    def stopTrain(self):
        if self.client.connected:
            self.trains[self.index_t].stop_locomotive()

    def stopAllTrains(self):
        if self.client.connected:
            msg = self.client.stop_all_locomotives()
            self.client.send(msg)

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
        self.timer_glowny = QBasicTimer()
        #self.timer_glowny.start(10, self)

        self.timer_postoj_s_w = QBasicTimer()
        self.timer_postoj_w_s = QBasicTimer()
                                            #zmienilem z 03010068 na 67
        self.trasa1 = ['03050066', '0305006E', '03010067', '03020067', '03020065'] # wrzeszcz -> kielpinek
        self.trasa2 = ['03020065', '03020068', '03010000', '03010068', '0305006D', '03050066']# kielpinek -> wrzeszcz
        self.trasa3 = ['0304012E', '0304012D'] # wrzeszcz -> banino
        self.trasa4 = ['0304012D', '0304012F'] # banino -> wrzeszcz

        self.train_list = []
        self.kalman_train = []

        self.licznik_balis = [0, 0, 0, 0]
        self.etap_trasy = [0, 0, 0, 0]

        self.roznica = 0

        #Pociag nr 1 - trasa 1 - ustawic na Wrzeszczu
        #Pociag nr 5 - trasa 3 - ustawic na Wrzeszczu
        #Pozostale odpowiednio

        #self.client = Client()
        #self.client.connect(TCP_IP, TCP_PORT)

        '''model_train = kalman.Model(1)
        self.kalman_train.append(model_train)
        self.train_list.append(Train(1))

        #1 na Wrzeszczu
        self.kalman_train[0].setpower = 65
        #msg = self.train_list[0].move(65, direction["Forward"])
        #self.client.send(msg)

        model_train = kalman.Model(1)   #UWAGA, ZLY MODEL
        self.kalman_train.append(model_train)
        self.train_list.append(Train(2))

        #2 na Kielpinku
        self.kalman_train[1].setpower = 65
        #msg = self.train_list[1].move(35, direction["Backward"])
        #self.client.send(msg)'''
        '''model_train = kalman.Model(5)
        self.kalman_train.append(model_train)
        self.train_list.append(Train(5))

        self.kalman_train[2].setpower = 65
        msg = self.train_list[2].move(35, direction["Forward"])
        self.client.send(msg)

        model_train = kalman.Model(6)
        self.kalman_train.append(model_train)
        self.train_list.append(Train(6))

        self.kalman_train[3].setpower = 65
        msg = self.train_list[3].move(35, direction["Backward"])
        self.client.send(msg)'''

    def postoj_s_w(self):

        self.timer_postoj_s_w.start(10000, self)

    def postoj_w_s(self):

        self.timer_postoj_w_s.start(10000, self)

    def zamiena_tras(self):
        if self.train_list[0] == Train(1):
            self.train_list[0] = Train(2)
            self.train_list[1] = Train(1)
        else:
            self.train_list[0] = Train(1)
            self.train_list[1] = Train(2)

        self.licznik_balis[0] = 0
        self.licznik_balis[1] = 0
        self.etap_trasy[0] = 0
        self.etap_trasy[1] = 0


        
    def timerEvent(self, event):
        if event.timerId() == self.timer_glowny.timerId():
            c.acquire()
            can_adres = adres
            c.release()
            #print((self.kalman_train[0].get_position()))
            #Kielpinek -> Wrzeszcz
            if (can_adres == self.trasa2[self.licznik_balis[1]]):
                if (self.licznik_balis[1] == 0):        #balisa tuz za peronem
                    self.kalman_train[1].update(124.5)
                    msg = self.train_list[1].move(65, direction["Backward"])   #jedziemy szybciej
                elif (self.licznik_balis[1] == 1):      #balisa kolo wiaduktu
                    self.kalman_train[1].update(279.5)
                elif (self.licznik_balis[1] == 2):      #przed strzyza
                    self.kalman_train[1].update(503)
                    msg = self.train_list[1].move(0, direction["Backward"])    #zatrzymujemy
                    self.postoj_s_w()
                elif (self.licznik_balis[1] == 3):      #za strzyza
                    self.kalman_train[1].update(149)
                    msg = self.train_list[1].move(65, direction["Backward"])   #pedzimy
                elif (self.licznik_balis[1] == 4):      #koniec zjazdu
                    self.kalman_train[1].update(243)
                    msg = self.train_list[1].move(40, direction["Backward"])   #zwalniami bo slalom zaraz bedzie
                elif (self.licznik_balis[1] == 5):
                    self.kalman_train[1].update(215.5)  #to juz peron jest?
                    msg = self.train_list[1].move(0, direction["Backward"])    #jak tak to stajemy
                    self.licznik_balis[1] = 0   #trzeba bedzie zmienic zeby drugi pociag nie odpalil

                self.licznik_balis[1] += 1
                self.etap_trasy[1] += 1
                self.client.send(msg)

            elif (can_adres == self.trasa1[self.licznik_balis[0]]):
                if (self.licznik_balis[0] == 0):        #gdzies przy wrzeszczu
                    self.roznica = self.kalman_train[0].get_position()
                    self.kalman_train[0].setpower = 65
                    self.kalman_train[0].update(self.roznica)
                    msg = self.train_list[0].move(65, direction["Forward"])   #przyspieszamy
                    print('uwaga')
                    self.client.send(msg)
                elif (self.licznik_balis[0] == 1):      #podjazd
                    self.kalman_train[0].update(249)#self.kalman_train[0].update(249)
                    print((self.kalman_train[0].get_position()))
                    #msg = self.train_list[0].move(65, direction["Forward"])   #zwalniamy bo zaraz strzyza
                    #self.client.send(msg)
                elif (self.licznik_balis[0] == 2):      #przed strzyza
                    self.kalman_train[0].update(149)
                    print((self.kalman_train[0].get_position()))
                    #msg = self.train_list[0].move(0, direction["Forward"])    #zatrzymujemy
                    self.postoj_w_s()
                    #self.client.send(msg)
                elif (self.licznik_balis[0] == 3):      #okolice wiaduktu
                    self.kalman_train[0].update(672)
                    print((self.kalman_train[0].get_position()))
                    msg = self.train_list[0].move(40, direction["Forward"])   #zwalniamy
                    self.client.send(msg)
                elif (self.licznik_balis[0] == 4):      #kielpinek
                    self.kalman_train[0].update(278.5)
                    print((self.kalman_train[0].get_position()))
                    msg = self.train_list[0].move(0, direction["Forward"])    #zatrzmujemy
                    self.client.send(msg)

                self.licznik_balis[0] += 1
                #self.etap_trasy[0] += 1

            if self.kalman_train[1].get_position() > 500 and self.etap_trasy[1] == 3:
                msg = self.train_list[1].move(40)
                self.client.send(msg)
                self.etap_trasy[1] += 1     #wynosi wiec 4, a licznik balis nadal 3

            if self.kalman_train[0].get_position() > 440+self.roznica and self.etap_trasy[0] == 0:
                print((self.kalman_train[0].get_position()))
                print('dziala')
                msg = self.train_list[0].move(0, direction["Forward"])
                self.client.send(msg)
                self.etap_trasy[0] += 1

            if self.kalman_train[0].get_position() > 100 and self.etap_trasy[0] == 1:
                print((self.kalman_train[0].get_position()))
                print('dziala')
                msg = self.train_list[0].move(0, direction["Forward"])
                self.client.send(msg)
                self.etap_trasy[0] += 1

        if event.timerId() == self.timer_postoj_s_w.timerId():

            msg = self.train_list[1].move(35)
            self.client.send(msg)
            self.timer_postoj_s_w.stop()

        if event.timerId() == self.timer_postoj_w_s.timerId():

            msg = self.train_list[0].move(40, direction["Forward"])
            self.etap_trasy[0] += 1
            self.client.send(msg)
            model_train = kalman.Model(1)
            self.kalman_train[0] = model_train
            self.kalman_train[0].setpower = 65
            self.timer_postoj_w_s.stop()


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
