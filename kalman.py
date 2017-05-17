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
        if train_nr == 1:
            self.A = np.mat([[-1.141, -0.4455, 0],
                             [0.5, 0, 0],  # Prędkość
                             [0, 1, 0]], dtype=float)  # Droga
            self.B = np.mat([[0.0615384615384615],  # [0.44603076],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 4.067],
                             [0., 4.067, 0.]], dtype=float)

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

    def get_stop_distance(self):
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

    t = Model(1)

    # dla symulacji ustaw czas na 0
    t.updateTime = 0
    t.simulateTime = 0

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
        print t.get_stop_distance()
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
