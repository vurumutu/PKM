# -*- coding: utf-8 -*-


class Train(object):
    # Klasa do obsługi sterownia pociągów
    def __init__(self, address):
        self.order = None
        self.locomotive = address
        self.velocity = 0
        self.course = True
        pass

    # Wybór rozkazu
    @staticmethod
    def header(order):
        if order == 1:
            header = 'E410 '
            return header
        elif order == 2:
            # TODO Dodać pozostałe rozkazy
            return 2
        else:
            return 0

    # Wybór lokomotywy
    @staticmethod
    def address(locomotive):
        address = '00 0' + str(hex(locomotive)[2]) + ' '
        return address

    # Określenie prędkości
    @staticmethod
    def speed(velocity):
        if velocity == 1:
            # TODO Dodać określenie odpowiedniej komendy dla danej prędkości
            return '1'
        elif velocity == 2:
            return 2
        else:
            return 0

    # Określenie kierunku
    @staticmethod
    def direction(course):
        if course == 1:
            # TODO Dodać określenie odpowiedniej komendy dla danego kierunku
            return '1'
        elif course == 2:
            return 2
        else:
            return 0

    def move(self, velocity, course=0):
        command = self.header(1) + self.address(self.locomotive) + self.direction(course) + self.speed(velocity)
        # TODO Dodać xor do komendy
        return command

    @staticmethod
    def menu():
        print("1. Do przodu - max prędkość")
        print("2. Do tylu - max prędkość")
        print("3. Do przodu - ustal prędkość")
        print("4. Do tylu - ustal prędkość")
        print("5. Stop - zerowa prędkość")
        print("0. Zakończ")
