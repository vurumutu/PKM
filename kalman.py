# -*- coding: utf-8 -*-
import numpy as np
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
        # initial variance
        self.P = np.mat([[1., 0., 0.],
                         [0., 1., 0.],
                         [0., 0., 1.]], dtype=float)

        # MODELE POCIĄGÓW
        # Pociąg 1 do PRZODU
        if train_nr == 11:
            self.A = np.mat([[-1.382, -0.7939, 0],
                             [1, 0, 0],
                             [0, 1, 0]], dtype=float)
            self.B = np.mat([[0.344904058413992],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)
        # Pociąg 1 do TYLU
        if train_nr == 12:
            self.A = np.mat([[-1.382, -0.7939, 0],
                             [1, 0, 0],
                             [0, 1, 0]], dtype=float)
            self.B = np.mat([[0.344904058413992],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)
        # Pociąg 2 do PRZODU
        if train_nr == 21:
            self.A = np.mat([[-0.083, -1.186, 0],
                             [1, 0, 0],
                             [0, 1, 0]], dtype=float)
            self.B = np.mat([[0.41996617639522],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)
        # Pociąg 2 do TYLU
        if train_nr == 22:
            self.A = np.mat([[-0.083, -1.186, 0],
                             [1, 0, 0],
                             [0, 1, 0]], dtype=float)
            self.B = np.mat([[0.41996617639522],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)
        # Pociąg 5
        if train_nr == 5:
            self.A = np.mat([[-0.11, -9.783, 0],
                             [1, 0, 0],
                             [0, 1, 0]], dtype=float)
            self.B = np.mat([[4.2975874425660079],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)
        # Pociąg 6
        if train_nr == 6:
            self.A = np.mat([[-0.11, -9.783, 0],
                             [1, 0, 0],
                             [0, 1, 0]], dtype=float)
            self.B = np.mat([[2.3385874425660079],
                             [0],
                             [0.]], dtype=float)
            self.C = np.mat([[0., 0., 1.],
                             [0., 1., 0.]], dtype=float)

        # VARIANCES
        # process variance
        self.Q = np.mat([[50., 0., 0.],
                         [0., 70.0, 0.],
                         [0., 0., 3500.]], dtype=float)
        # sensor variance
        self.R = np.mat([[3.1, 0.],
                         [0., 30.1]], dtype=float)

        self.motorPower = 0
        self.updateTime = time.time()
        self.updatePosition = 0.
        self.simulateTime = time.time()

    def simulate(self, update_state=True):
        """Zwraca pozycje pociągu

             Args:
                update_state (bool): Jeżeli True to symuluje model dla aktualnego czasu i aktualizuje go, czyli
                                     generalnie zawsze kiedy chcemy sprawdzić aktualną pozycję w danym momencie.

        """
        self.simulate_T(time.time(), update_state)

    def simulate_T(self, time, update_state=True):
        """Zwraca pozycje pociągu

             Args:
                time (float): Przyszły czas do którego ma być symulowany model
                update_state (bool): Jeżeli True to symuluje model dla aktualnego czasu i aktualizuje go, czyli
                                     generalnie zawsze kiedy chcemy sprawdzić aktualną pozycję w danym momencie.

        """
        if time < self.simulateTime - self.dT:
            print(time, " < ", self.simulateTime)
            raise Exception('Nie cofaj czasu!')
        X, P, t = np.copy(self.X), np.copy(self.P), self.simulateTime

        while t < time:
            t += self.dT
            X += (self.A * X + self.B * self.motorPower) * self.dT
        P = self.A * P * self.A.transpose() + self.Q * (t - self.updateTime)

        if update_state:
            self.X = X
            self.simulateTime = t
        return X, P

    def get_stop_distance(self):
        """Zwraca dystans jaki pociąg jeszcze przejedzie jeżeli zacznie się zatrzymywać"""

        self.simulate()  # zasymuluj do aktualnej chwili czasu
        power, time, state, P = self.motorPower, self.simulateTime, np.copy(self.X), np.copy(self.P)
        v = self.get_velocity(False)
        self.motorPower = 0  # moc na silniku podczas hamowania

        while v * self.get_velocity(False) > 0.0001:
            time += self.dT
            self.simulate_T(time, update_state=True)  # aktualizujemy stan w celach optymalizacyjnych

        pozycja = self.get_position(False)  # zapisz pozycje gdzie sie pociąg zatrzymał
        self.motorPower, self.simulateTime, self.X, self.P = power, time, state, P  # przywróć oryginalny stan

        print("Początek zatrzymania: ", self.get_position(False))
        print("Koniec zatrzymania: ", pozycja)
        return pozycja - self.get_position(False)

    def update(self, distance):
        """Aktualizuje model względem aktualnego czasu i przejechanej odległości.

             Args:
                distance (float): Przebyta droga od ostatniego update lub startu

        """
        dt = time.time() - self.updateTime
        Xpom = np.mat([[self.updatePosition + distance], [distance / dt]])

        # predykcja
        Xprio, Pprio = self.simulate_T(self.updateTime + dt, False)
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
                simulate (bool): Jeżeli True to symuluje model dla aktualnego czasu i aktualizuje go, czyli generalnie
                                 zawsze kiedy chcemy sprawdzić aktualną pozycję w danym momencie.

             Returns:
                (float): Zwraca pozycje pociągu (dystans od startu)

        """
        if simulate:
            self.simulate()
        return (self.C * self.X)[0, 0]

    def get_velocity(self, simulate=True):
        """Zwraca prędkość pociągu

             Args:
                simulate (bool): Jeżeli True to symuluje model dla aktualnego czasu i aktualizuje go, czyli generalnie
                                 zawsze kiedy chcemy sprawdzić aktualną pozycję w danym momencie.

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
        if power >= 127:
            self.motorPower = 127
        elif power <= 0:
            self.motorPower = 0
        else:
            self.motorPower = power


# TESTOWANIE
if __name__ == "__main__":
    t = Model(6)
    t.set_power(65)
    # dla symulacji ustaw czas na 0
    time.sleep(10)  # Poruszamy pociągiem przez 10 sekund
    print("Dystans hamowania: ", t.get_stop_distance())
