# -*- coding: utf-8 -*-

# TODO Scalić TCP_connection i command w jeden plik train_controller po ukończeniu wszystkich testów sterownika
# TODO Dodać do metod docstring


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
            header = 'E410'  # 14
            return header
        elif order == 2:
            header = 'E411'  # 27
            return header
        elif order == 3:
            header = 'E412'  # 28
            return header
        elif order == 4:
            header = 'E413'  # 127
            return header
        else:
            return 0

    # Wybór lokomotywy
    @staticmethod
    def address(locomotive):
        address = '000' + str(hex(locomotive)[2]) + ' '
        return address

    # Określenie prędkości i kierunku
    @staticmethod
    def speed(velocity, course):
        msg = hex(course * 128 + velocity)[2:]
        if len(msg) == 1:
            msg = '0' + msg
        return msg

    # Tworzenie komendy do sterowania pociagiem
    def move(self, velocity, course=0):
        command = self.header(4) + self.address(self.locomotive) + self.speed(velocity, course)
        xor = self.xor(command)
        command += xor
        return command

    # Tworzenie xora do komendy
    def xor(self, command):
        parts = []
        xor = ''
        while command:
            parts.append(int(command[:2], 16))
            command = command[2:]
        for i in range(1, len(parts)):
            if i == 1:
                xor = parts[i - 1] ^ parts[i]
            else:
                xor ^= parts[i]
        if len(parts) == 1:
            xor = parts[0]
        if xor < 16:
            xor = hex(xor)[2:]
            xor = '0' + xor
        else:
            xor = hex(xor)[2:]
        return xor

    @staticmethod
    def menu():
        # TODO Usunąć kiedy scalono w train_controller
        print("1. Do przodu - max prędkość")
        print("2. Do tylu - max prędkość")
        print("3. Do przodu - ustal prędkość")
        print("4. Do tylu - ustal prędkość")
        print("5. Stop - zerowa prędkość")
        print("0. Zakończ")
