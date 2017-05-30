# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import time


class Model:
    """Klasa zawierająca modele poszczególnych pociągów"""
    def __init__(self, train_nr):
        """Domyślne ustawienia klasy

             Args:
                 train_nr (int): Numer  pociągu

         """
        self.dT = 0.01
        # initial state
        self.X = np.mat([[0.],
                         [0.],  # v
                         [0.]],  # x
                        dtype=float)
        self.P = np.mat([[1., 0., 0.],  # initial wariance
                         [0., 1., 0.],
                         [0., 0., 1.]], dtype=float)

        # Modele pociągów
        if train_nr == 11:
            """
            self.A = np.mat([[-1.141, -0.4455, 0],
                             [0.5, 0, 0],  # Prędkość
                             [0, 1, 0]], dtype=float)  # Droga
            self.B = np.mat([[0.0615384615384615],  # [0.44603076],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 4.067],
                             [0., 4.067, 0.]], dtype=float)
            """
            self.A = np.mat([[-1.782, -0.7939, 0],
                             [1, 0, 0],  # Prędkość
                             [0, 1, 0]], dtype=float)  # Droga
            self.B = np.mat([[0.0084904058413992],  # [0.44603076],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)

        if train_nr == 12:
            self.A = np.mat([[-1.684, -0.7092, 0],
                             [1, 0, 0],  # Prędkość
                             [0, 1, 0]], dtype=float)  # Droga
            self.B = np.mat([[0.0096319395114199],  # [0.44603076],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)
        if train_nr == 21:
            self.A = np.mat([[-7.422, -3.443, 0],
                             [1, 0, 0],  # Prędkość
                             [0, 1, 0]], dtype=float)  # Droga
            self.B = np.mat([[0.010564542753384],  # [0.44603076],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)

        if train_nr == 22:
            self.A = np.mat([[-8.483, -4.486, 0],
                             [1, 0, 0],  # Prędkość
                             [0, 1, 0]], dtype=float)  # Droga
            self.B = np.mat([[0.0081996617639522],  # [0.44603076],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)

        if train_nr == 5:
            self.A = np.mat([[-2.67, -1.783, 0],
                             [1, 0, 0],  # Prędkość
                             [0, 1, 0]], dtype=float)  # Droga
            self.B = np.mat([[0.0175874425660079],  # [0.44603076],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)

        if train_nr == 6:
            self.A = np.mat([[-2.152, -1.158, 0],
                             [1, 0, 0],  # Prędkość
                             [0, 1, 0]], dtype=float)  # Droga
            self.B = np.mat([[0.0128930361488501],  # [0.44603076],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)


        # variances
        self.Q = np.mat([[50., 0., 0.],  # process variance
                         [0., 70.0, 0.],
                         [0., 0., 3500.]], dtype=float)
        self.R = np.mat([[3.1, 0.],  # sensor variance
                         [0., 30.1]], dtype=float)

        self.motorPower = 65.0
        self.stopPower = 0.
        self.updateTime = time.time()
        self.updatePosition = 0.
        self.simulateTime = time.time()

    def simulatesym(self, time, updatestate=True):
        """ podaj czas z przyszlosci do ktorego mam symulowac pociag
        jezeli updatestate bedzie false, to zmienne pociagu zostana zachowane"""
        if time < self.simulateTime - self.dT:
            print(time, " < ", self.simulateTime)
            raise Exception('Nie cofaj czasu!')
        X, P, t = np.copy(self.X), np.copy(self.P), self.simulateTime
        while t < time:
            t += self.dT
            X += (self.A * X + self.B * self.motorPower) * self.dT
        P = self.A * P * self.A.transpose() + self.Q * (t - self.updateTime)
        if updatestate:
            self.X = X
            # self.P = P
            self.simulateTime = t
        return X, P

    def simulate(self, updatestate=True):
        self.simulatesym(time.time(), updatestate)

    def predict(self, time):
        """parametrem jest aktualny czas, zwracana jest macierz,
        nie mozna cofac czasu, domyslnie nie aktualizuje zmiennych pociagu"""
        X, P = self.simulatesym(time, updatestate=False)
        return self.C * X

    def get_stop_distance(self, update_time):
        """
                # TODO Jaki czas podać tutaj? Skąd go przypisać?
                actual_time = time.time()
                if actual_time < self.simulateTime - self.dT:
                    print(time, " < ", self.simulateTime)
                    raise Exception('Nie cofaj czasu!')
                X, P, t = np.copy(self.X), np.copy(self.P), self.simulateTime
                # Robimy symulacje bez zapisywania
                while t < actual_time:
                    t += self.dT
                    X += (self.A * X + self.B * self.motorPower) * self.dT
                # Licz dopóki prędkość jest większa równa od zera
                while (self.C * self.X)[1, 0] >= 0:
                    t += self.dT
                    X += (self.A * X + self.B * self.stopPower) * self.dT

                return (self.C * X)[0, 0] - (self.C * self.X)[0, 0]
                """
        """ zwraca dystanc potrzebny do wychamowania. W centymetrach.
        """
        self.simulatesym(update_time, updatestate=True)  # zasymuluj do aktualnej chwili czasu
        power, time, state, P = self.motorPower, self.simulateTime, np.copy(self.X), np.copy(self.P)
        v = self.get_velocity(False)
        self.motorPower = 0  # moc na silniku podczas hamowania
        while v * self.get_velocity(False) > 0.0001:  # > 0, czyli gdy paciag przed i po symulacji jedzie w tym samym kierunku,
            # pamietajmy o cofaniu,
            time += self.dT
            self.simulatesym(time, updatestate=True)  # aktualizujemy stan w celach optymalizacyjnych
        pozycja = self.get_position(False)  # zapisz pozycje gdzie sie pociag zatrzymal
        self.motorPower, self.simulateTime, self.X, self.P = power, time, state, P  # przywroc oryginalny stan
        return pozycja - self.get_position(False)

    def update(self, distance):
        """ aktualizuje system wzgledem aktualnego czasu
        i przejechanej odleglosci jako parametr"""
        dt = time.time() - self.updateTime
        self.updatesym(distance, dt)

    def updatesym(self, distance, dt, freshstate=False):
        """podaj przejechana odleglosc od ostatniej aktualizacji
        oraz czas jaki minal na jej przejechanie"""
        Xpom = np.mat([[self.updatePosition + distance],
                       [distance / dt]])
        # predykcja
        if not freshstate:
            Xprio, Pprio = self.simulatesym(self.updateTime + dt, False)
        else:
            Xprio, Pprio = self.X, self.P
        Pprio = self.A * self.P * self.A.transpose() + self.Q * dt
        # korekcja
        e = Xpom - self.C * Xprio
        temp = self.C * Pprio * self.C.transpose() + self.R * dt
        K = Pprio * self.C.transpose() * np.linalg.inv(temp)
        # aktualizacja
        I = np.eye(self.A.shape[0])
        self.X = Xprio + K * e
        self.P = (I - K * self.C) * Pprio
        self.updateTime += dt
        self.updatePosition = self.get_position(False)

    def get_position(self, simulate=True):
        """Zwraca pozycje pociągu

             Args:
                simulate (bool): Jeżeli True to symuluje model dla aktualnego czasu i aktualizuje go

             Returns:
                (float): Zwraca pozycje pociągu (dystans od startu)

        """
        if simulate:
            self.simulate()
        return (self.C * self.X)[0, 0]

    def get_velocity(self, simulate=True):
        """Zwraca prędkość pociągu

             Args:
                simulate (bool): Jeżeli True to symuluje model dla aktualnego czasu i aktualizuje go

             Returns:
                (float): Zwraca prędkość pociągu

        """
        if simulate:
            self.simulate()
        return (self.C * self.X)[1, 0]

    def set_power(self, power):
        """Ustawia z jaką mocą jedzie pociąg

             Args:
                 power (float): moc od 0.0 - 127.0

         """
        self.motorPower = power


if __name__ == "__main__":
    distances = [203, 230, 624, 272]
    times = [18.1354904881, 27.5069689903, 53.9750874511, 7.80411009911]
    times = [7.08, 6.68, 17.55, 7.9]
    t1 = Model(1)
    t = Model(1)

    # dla symulacji ustaw czas na 0
    t.updateTime = 0
    t.simulateTime = 0
    t1.updateTime = 0
    t1.simulateTime = 0
    print(t1.get_stop_distance(t1.simulateTime + 10.))

    # zmienne do wyswietlania
    tim = [0.]
    timpred = [0.]
    X = [0.]
    V = [0.]
    pom = [0.]
    pred = [0.]
    vpom = [0.]
    vpred = [0.]
    var = [0.]

    # symuluj przejazd
    for i in range(len(distances)):
        temptime = 0
        while temptime < times[i]:
            x, p = t.simulatesym(t.simulateTime + t.dT, updatestate=True)
            pred.append(t.get_position(False))
            vpred.append(t.get_velocity(False))
            timpred.append(t.simulateTime)
            temptime += t.dT
        t.updatesym(distances[i], times[i], freshstate=True)
        X.append(t.get_position(False))
        V.append(t.get_velocity(False))
        var.append(t.P[1, 1])

        pom.append(pom[-1] + distances[i])
        vpom.append(distances[i] / times[i])
        tim.append(tim[-1] + times[i])

    # symuluj dodatkowe kilka probek
    temptime = 0
    while temptime < 3:
        x, p = t.simulatesym(t.simulateTime + t.dT, updatestate=True)
        pred.append(t.get_position(False))
        vpred.append(t.get_velocity(False))
        timpred.append(t.simulateTime)
        temptime += t.dT

    # wyswietl wyniki
    plt.figure(1)
    plt.plot(tim, X, 'x', label='filtr')
    plt.plot(tim, pom, 'o', label='pomiar')
    plt.plot(timpred, pred, label='predykcja')
    plt.legend(loc='best')
    plt.title('droga')

    plt.figure(2)
    plt.plot(tim, V, 'x', label='filtr')
    plt.plot(tim, vpom, 'o', label='pomiar')
    plt.plot(timpred, vpred, label='predykcja')
    plt.legend(loc='best')
    plt.title('predkosc')

    # plt.figure(3)
    # plt.plot(tim, var)
    # plt.title('wariancja predkosci')

    plt.show()
