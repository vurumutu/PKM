#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
#from train_map import Railline

class SectionTrack:
    def __init__(self, line0, line1, partLine=None, number=None):
        self.line0 = line0
        self.line1 = line1

        # nowa mapa obiektow bez czujnikow dla linii 0
        self.newMapObject0 = self.removeSensorFromMapObject(self.line0.map_object)
        # nowa mapa obiektow bez czujnikow dla linii 1
        self.newMapObject1 = self.removeSensorFromMapObject(self.line1.map_object)

        self.actual_track = None
        # tablica zawierajaca mozliwe czesci lini
        # PART_LEFT - część po lewej stronie linii kolejowej(mapy) przed pierwsza zwrotnica
        # PART_UP - górna część linii kolejowej (część którą rozdziela zwrotnica)
        # PART_DOWN - dolna część linii kolejowej (część którą rozdziela zwrotnica)
        # PART_LEFT - część po prawej stronie linii kolejowej(mapy) po drugiej zwrotnicy
        self.partsLine = ['PART_LEFT', 'PART_UP', 'PART_DOWN', 'PART_RIGHT']
        self.lineMap = {'PART_LEFT': [], 'PART_UP': [], 'PART_DOWN': [], 'PART_RIGHT': []}  # inicjalizacja nowej mapy
        self.createLineMap() # tworzy nowa mape

        if partLine is None and number is None:
            self.setActualTrack('PART_LEFT', 1)
        else:
            self.exceptionTrack(partLine, number)
            if partLine is None:
                self.setActualTrack('PART_LEFT', number)
            if number is None:
                self.setActualTrack(partLine, 1)


    # funkcja zwraca nową mapę obiektów bez czujników
    # paramtry funkcji:
    # listLine - lista z mapy obiektów
    @staticmethod
    def removeSensorFromMapObject(listLine):
        newMapObject = []

        for i in range(len(listLine)):
            if listLine[i] == 2:
                continue
            newMapObject.append(listLine[i])

        return newMapObject

    # funkcja zwraca liczbe czujników z mapy do danego numeru
    # paramtry funkcji:
    # listLine - lista z mapy obiektów
    # index - dokad funkcja ma liczyc liczbę sensorow
    @staticmethod
    def countSensorFromMapObject(listLine, index):
        number_of_sensor = 0

        for i in range(index):
            if listLine[i] == 2:
                number_of_sensor = number_of_sensor + 1

        return number_of_sensor

    # sprawdzanie czy część i numer lini
    # mają odpowiednie typy oraz czy sa zgodne z nową mapa
    # jeśli coś się nie zgadza funkcja wyrzuca wyjątek (błąd)
    def exceptionTrack(self, partLine, number):
        if not type(partLine) == str:
            raise Exception('arg0(partLine) niewłaściwy typ (wymagany str)')
        if partLine not in self.partsLine:
            raise Exception('arg0(partLine) niewłaściwa część lini')
        if not type(number) == int:
            raise Exception('arg1(number) niewłaściwy typ (wymagany int)')
        if number not in self.lineMap[partLine]:
            raise Exception('arg1(number) część lini nie zawiera takiego odcinka')

    # funkcja tworzy nową mapę z numerami odcinków (bardziej intuicyjna)
    # mapa jest zamieszczona w słowniku gdzie:
    # - klucze to częsci (left, up, down, right) lini mapy
    # - wartości to tablica zawierające numery codcinków lini danej częśći
    # numeracja w tablicy zaczyna się od 1
    def createLineMap(self):
        end_left = None
        end_up = None

        k = 0
        for i in range(len(self.newMapObject0)):
            k = k + 1
            self.lineMap['PART_LEFT'].append(k)
            if self.newMapObject0[i] == 3:
                end_left = i
                break

        k = 0
        for i in range(end_left+1, len(self.newMapObject0)):
            if self.newMapObject0[i] == 3:
                end_up = i
                break
            k = k + 1
            self.lineMap['PART_UP'].append(k)


        k = 0
        for i in range(end_left+1, len(self.newMapObject1)):
            if self.newMapObject1[i] == 3:
                break
            k = k + 1
            self.lineMap['PART_DOWN'].append(k)

        k = 0
        for i in range(end_up, len(self.newMapObject0)):
            k = k + 1
            self.lineMap['PART_RIGHT'].append(k)

        print(self.lineMap)

    # funkcja sprawdza czy podany odcinek zgadza się z odcinkiem aktualnym
    # jesli tak to True jesli nie to False
    def checkAtualTrack(self, partLine, number):
        self.exceptionTrack(partLine, number)
        if self.actual_track[0] == partLine and self.actual_track[1] == number:
            return True
        return False

    # funkcja sprawdza czy podany odcinek zgadza się z odcinkiem aktualnym
    # jesli tak to True jesli nie to False
    def checkAtualTrackPartLine(self, partLine):
        self.exceptionTrack(partLine, self.actual_track[1])
        if self.actual_track[0] == partLine:
            return True
        return False


    ###########################################
    # ---------- get i set --------------------
    ###########################################

    # ustawia aktualna część oraz numer lini
    def setActualTrack(self, partLine, number):
        self.exceptionTrack(partLine, number)
        self.actual_track = [partLine, number]

    # zwraca aktualna część oraz numer lini
    def getActualTrack(self):
        return self.actual_track

    # ustawia aktualna część lini
    def setActualTrackPartLine(self, partLine):
        self.exceptionTrack(partLine, self.actual_track[1])
        self.actual_track[0] = partLine

    # zwraca aktualna część lini
    def getActualTrackPartLine(self):
        return self.actual_track[0]

    # ustawia aktualny numer lini
    def setActualTrackNumber(self, number):
        self.exceptionTrack(self.actual_track[0], number)
        self.actual_track[1] = number

    # zwraca aktualny numer lini
    def getActualTrackNumber(self):
        return self.actual_track[1]

    def setActualTrackOld(self, dual, number):
        print(number)
        self.convertOldPartLineToNew(dual)
        if dual == 1:
            self.convertOldNumberToNew(number, 0)
        elif dual == 2:
            self.convertOldNumberToNew(number, 1)
        else:
            self.convertOldNumberToNew(number, 0)

    def convertOldPartLineToNew(self, dual):
        if dual == -1:
            self.actual_track[0] = 'PART_LEFT'
        elif dual == -2:
            self.actual_track[0] = 'PART_RIGHT'
        elif dual == 1:
            self.actual_track[0] = 'PART_UP'
        elif dual == 2:
            self.actual_track[0] = 'PART_DOWN'
        else:
            raise Exception('arg0(dual) nieznana część lini')

    def convertOldNumberToNew(self, number, line):
        if line == 0:
            sensors = self.countSensorFromMapObject(self.line0.map_object, number)
            length_line = len(self.lineMap['PART_UP'])
        elif line == 1:
            sensors = self.countSensorFromMapObject(self.line1.map_object, number)
            length_line = len(self.lineMap['PART_DOWN'])
        else:
            raise Exception('arg1(line) nieznana linia')

        number = number - sensors
        if number <= len(self.lineMap['PART_LEFT']) - 1:
            self.actual_track[1] = number + 1
        elif number <= len(self.lineMap['PART_LEFT']) + length_line - 1:
            self.actual_track[1] = number - len(self.lineMap['PART_LEFT']) + 1
        else:
            self.actual_track[1] = number - len(self.lineMap['PART_LEFT']) - length_line + 1



    # zwraca długość podanego odcinka lini(część odcinka + numer)
    # jesli odcinek nie jest podany to zwraca dlugość odcinka aktualnego (z self.actual_track)
    def getLenghtActualTrack(self, partLine=None, number=None):
        if partLine is None:
            partLine = self.actual_track[0]
        if number is None:
            number = self.actual_track[1]
        self.exceptionTrack(partLine, number)

        if partLine == 'PART_LEFT':
            for i in range(len(self.line0.lines_sections)):
                if i == number - 1:
                    return self.line0.lines_sections[i]
        elif partLine == 'PART_UP':
            for i in range(len(self.line0.lines_sections)):
                if i == number + len(self.lineMap['PART_LEFT']) - 1:
                    return self.line0.lines_sections[i]
        elif partLine == 'PART_DOWN':
            for i in range(len(self.line1.lines_sections)):
                if i == number + len(self.lineMap['PART_LEFT']) - 1:
                    return self.line1.lines_sections[i]
        elif partLine == 'PART_RIGHT':
            for i in range(len(self.line0.lines_sections)):
                if i == number + len(self.lineMap['PART_LEFT']) + len(self.lineMap['PART_UP']) - 1:
                    return self.line0.lines_sections[i]
        else:
            return None

    # zwraca długość DO podanego odcinka lini(część odcinka + numer)
    # jesli odcinek nie jest podany to zwraca dlugość DO odcinka aktualnego (z self.actual_track)
    def getLenghtToActualTrack(self, partLine=None, number=None):
        if partLine is None:
            partLine = self.actual_track[0]
        if number is None:
            number = self.actual_track[1]
        self.exceptionTrack(partLine, number)

        sumLength = 0
        if partLine == 'PART_LEFT':
            for i in range(len(self.line0.lines_sections)):
                sumLength = sumLength + self.line0.lines_sections[i]
                if i == number - 1:
                    return sumLength
        elif partLine == 'PART_UP':
            for i in range(len(self.line0.lines_sections)):
                sumLength = sumLength + self.line0.lines_sections[i]
                if i == number + len(self.lineMap['PART_LEFT']) - 1:
                    return sumLength
        elif partLine == 'PART_DOWN':
            for i in range(len(self.line1.lines_sections)):
                sumLength = sumLength + self.line1.lines_sections[i]
                if i == number + len(self.lineMap['PART_LEFT']) - 1:
                    return sumLength
        elif partLine == 'PART_RIGHT':
            for i in range(len(self.line0.lines_sections)):
                sumLength = sumLength + self.line0.lines_sections[i]
                if i == number + len(self.lineMap['PART_LEFT']) + len(self.lineMap['PART_UP']) - 1:
                    return sumLength
        else:
            return None

    ###########################################