# -*- coding: utf-8 -*-


class Train(object):
    # Klasa do obsługi sterownia pociągów
    def __init__(self):
        self.order = None
        self.locomotive = None
        self.velocity = 0
        self.course = True
        pass

    # Wybór rozkazu
    def header(self, order):
        if order == 1:
            return 1
        elif order == 2:
            return 2
        else:
            return 0

    # Wybór lokomotywy
    def address(self, locomotive):
        if locomotive == 1:
            return 1
        elif locomotive == 2:
            return 2
        else:
            return 0

    # Określenie prędkości
    def speed(self, velocity):
        if velocity == 1:
            return 1
        elif velocity == 2:
            return 2
        else:
            return 0

    # Określenie kierunku
    def direction(self, course):
        if course == 1:
            return 1
        elif course == 2:
            return 2
        else:
            return 0

    def move(self, order, locomotive, velocity, course):
        command = self.header(order) + self.address(locomotive) + self.speed(velocity) + self.direction(course)
        return command
