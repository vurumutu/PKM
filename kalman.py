import numpy as np
import matplotlib.pyplot as plt
import time


class train:
    def __init__(self):
        self.dT = 0.01
        #initial state
        self.X = np.mat([[0.],
                        [0.],  # v
                        [0.]], # x
                        dtype=float)
        self.P = np.mat([[1., 0., 0.],  # initial wariance
                        [0., 1., 0.],
                        [0., 0., 1.]], dtype=float)
        # object model
        self.A = np.mat([[-1.141, -0.4455, 0],
                        [0.5, 0, 0], # predkosc
                        [0, 1, 0]], dtype=float) # droga
        self.B = np.mat([[0.0615384615384615],#[0.44603076],
                        [0],
                        [0.]], dtype=float)
        self.C = np.mat([[0., 0., 4.067],
                        [0., 4.067, 0.]], dtype=float)
        #variances
        self.Q = np.mat([[50., 0., 0.], # process variance
                        [0., 70.0, 0.],
                        [0., 0., 3500.]], dtype=float)
        self.R = np.mat([[3.1, 0.], # sensor variance
                        [0., 30.1]], dtype=float)
        self.motorPower = 65.0
        self.updateTime = time.time()
        self.updatePosition = 0.
        self.simulateTime = time.time()

    def simulatesym(self, time, updatestate=True):
        """ podaj czas z przyszlosci do ktorego mam symulowac pociag
        jezeli updatestate bedzie false, to zmienne pociagu zostana zachowane"""
        if time < self.simulateTime-self.dT:
            print(time, " < ", self.simulateTime)
            raise Exception('Nie cofaj czasu!')
        X, P, t = np.copy(self.X), np.copy(self.P), self.simulateTime
        while t < time:
            t += self.dT
            X += (self.A*X + self.B*self.motorPower) * self.dT
        P = self.A*P*self.A.transpose() + self.Q * (t-self.updateTime)
        if updatestate:
            self.X = X
            #self.P = P
            self.simulateTime = t
        return X, P

    def simulate(self, updatestate=True):
        self.simulatesym(time.time(), updatestate)

    def predict(self, time):
        ''' parametrem jest aktualny czas, zwracana jest macierz,
        nie mozna cofac czasu, domyslnie nie aktualizuje zmiennych pociagu'''
        X, P = self.simulate(time, updatestate=False)
        return self.C*X

    def update(self, distance):
        """ aktualizuje system wzgledem aktualnego czasu
        i przejechanej odleglosci jako parametr"""
        dt = time.time() - self.updateTime
        self.updatesym(distance, dt)

    def updatesym(self, distance, dt, freshstate=False):
        ''' podaj przejechana odleglosc od ostatniej aktualizacji
        oraz czas jaki minal na jej przejechanie'''
        Xpom = np.mat([[self.updatePosition + distance],
                        [distance / dt]])
        # predykcja
        if not freshstate:
            Xprio, Pprio = self.simulate(self.updateTime+dt, False)
        else:
            Xprio, Pprio = self.X, self.P
        Pprio = self.A*self.P*self.A.transpose() + self.Q * dt
        # korekcja
        e = Xpom - self.C*Xprio
        temp = self.C*Pprio*self.C.transpose() + self.R*dt
        K = Pprio*self.C.transpose()*np.linalg.inv(temp)
        # aktualizacja
        I = np.eye(self.A.shape[0])
        self.X = Xprio + K*e
        self.P = (I - K*self.C) * Pprio
        self.updateTime += dt
        self.updatePosition = self.position(False)

    def position(self, simulate=True):
        if simulate:
            self.simulate()
        return (self.C*self.X)[0, 0]

    def velocity(self, simulate=True):
        if simulate:
            self.simulate()
        return (self.C*self.X)[1, 0]

    def setpower(self, motor):
        self.motorPower = motor


if __name__ == "__main__":
    distances = [203, 230, 624, 272]
    times = [18.1354904881, 27.5069689903, 53.9750874511, 7.80411009911]
    times = [7.08, 6.68, 17.55, 7.9]

    t = train()

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
            pred.append(t.position(False))
            vpred.append(t.velocity(False))
            timpred.append(t.simulateTime)
            temptime += t.dT
        t.updatesym(distances[i], times[i], freshstate=True)
        X.append(t.position(False))
        V.append(t.velocity(False))
        var.append(t.P[1, 1])

        pom.append(pom[-1]+distances[i])
        vpom.append(distances[i]/times[i])
        tim.append(tim[-1]+times[i])

    #symuluj dodatkowe kilka probek
    temptime = 0
    while temptime < 3:
        x, p = t.simulatesym(t.simulateTime + t.dT, updatestate=True)
        pred.append(t.position(False))
        vpred.append(t.velocity(False))
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

    #plt.figure(3)
    #plt.plot(tim, var)
    #plt.title('wariancja predkosci')

    plt.show()
