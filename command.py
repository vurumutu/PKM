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
        return command

    def stop_all_locomotives(self):
        command = '80'
        return command

    def stop_chosen_locomotive(self, locomotive):
        command = '92000' + locomotive
        return command

    def off_energy(self):
        command = '2180'
        return command

    def get_soft_version(self):
        command = '2121'
        return command

    def get_status(self):
        command = '2124'
        return command

    # TODO: dodanie pozostalych metod sterujcych pociągiem

    @staticmethod
    def menu():
        # TODO Usunąć kiedy scalono w train_controller
        print("1. Do przodu - max prędkość")
        print("2. Do tylu - max prędkość")
        print("3. Do przodu - ustal prędkość")
        print("4. Do tylu - ustal prędkość")
        print("5. Stop - zerowa prędkość")
        print("6. Wyłącz zasilanie pociągów") #klawisz off na pilocie
        print("0. Zakończ")
