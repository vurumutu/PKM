import numpy as np
import matplotlib.pyplot as plt
import time

distances = [203, 230, 624, 272]
times = [53.9750874511, 27.5069689903, 18.1354904881, 7.80411009911]

class train:
    def __init__(self):
        self.dT = 0.1
        #initial state
        self.X = np.mat([[0.],  # x
                        [0.],  # v
                        [0.]], dtype=float)
        self.P = np.mat([[1., 0., 0.],  # initial wariance
                        [0., 1., 0.],
                        [0., 0., 1.]], dtype=float)
        # object model
        self.A = np.mat([[-1.782, -0.7939, 0],
                        [1, 0, 0], # predkosc
                        [0, 1, 0]], dtype=float) # droga
        self.B = np.mat([[28.992],
                        [0.],
                        [0.]], dtype=float)
        self.C = np.mat([[0., 0., 1.],
                        [0., 1., 0.]], dtype=float)
        #variances
        self.Q = np.mat([[0.025, 0., 0.], # process variance
                        [0., 0.025, 0.],
                        [0., 0., 0.025]], dtype=float)
        self.R = np.mat([[0.1, 0.], # sensor variance
                        [0., 1.0]], dtype=float)
        self.motorPower = 45.
        self.updateTime = 0.

    def position(self):
        return self.X[2, 0]

    def velocity(self):
        return self.X[1, 0]

    def simulate(self, time):
        """ podaj czas z przyszlosci do ktorego mam
        symulowac pociag """
        if time < self.updateTime-self.dT:
            raise Exception('Nie cofaj czasu!')
        X, P, t = np.copy(self.X), np.copy(self.P), self.updateTime
        while t < time:
            t += self.dT
            X += (self.A*X + self.B*self.motorPower) * self.dT
            P += (self.A*P*self.A.transpose() + self.Q) * self.dT
        return X, P

    def predict(self, time):
        ''' parametrem jest aktualny czas, zwracana jest macierz,
        nie mozna cofac czasu'''
        X, P = self.simulate(time)
        return self.C*(self.A*X + self.B*self.motorPower)

    def update(self, distance):
        """ aktualizuje system wzgledem aktualnego czasu
        i przejechanej odleglosci jako parametr"""
        dt = time.time() - self.updateTime
        self.updatesym(distance, dt)

    def updatesym(self, distance, dt):
        ''' podaj przejechana odleglosc od ostatniej aktualizacji
        oraz czas jaki minal na jej przejechanie'''
        Xpom = np.mat([[distance],
                        [distance / dt]])
        # predykcja
        Xprio, Pprio = self.simulate(self.updateTime+dt)
        # korekcja
        e = Xpom - self.C*Xprio
        temp = self.C*Pprio*self.C.transpose() + self.R*dt
        K = Pprio*self.C.transpose()*np.linalg.inv(temp)
        # aktualizacja
        I = np.eye(self.A.shape[0])
        self.X = Xprio + K*e
        self.P = (I - K*self.C) * Pprio
        self.updateTime += dt


t = train()
tim = [0.]
X = [0.]
V = [0.]
pom = [0.]
pred = [0.]
vpred = [0.]
vpom = [0.]

for i in range(len(distances)):
    x, p = t.simulate(times[i])
    pred.append(x[2, 0])
    vpred.append(p[1, 0])
    t.updatesym(distances[i], times[i])
    X.append(t.position())
    V.append(t.velocity())

    pom.append(pom[-1]+distances[i])
    vpom.append(distances[i]/times[i])
    tim.append(tim[-1]+times[i])

print('time ', tim)
print('X ', X)
plt.figure(1)
plt.plot(tim, X)
plt.plot(tim, pom, 'o')
plt.plot(tim, pred, 'x')

plt.figure(2)
plt.plot(tim, vpom)
plt.plot(tim, vpred)
#plt.legend()
plt.show()

T = 1
A = np.mat([[1, 0, T, 0],
            [0, 1, 0, T],
            [0, 0, 1, 0],
            [0, 0, 0, 1]])
B = np.mat([[0, 0],
            [0, 0],
            [1, 0],
            [0, 1]])
C = np.mat([[1, 0, 0, 0],
            [0, 1, 0, 0]])
Q = np.mat([[0.025, 0],
            [0, 0.025]])
R = np.mat([[2.0, 0],
            [0, 2.0]])


pom = []
shist = []
Phist = []

with open('lab7_dane/measurements4.txt') as f:
    for l in f.readlines():
        s = l.split()
        pom.append([float(s[0]), float(s[1])])
pom = np.array(pom)

s = np.mat([[pom[0, 0]],
            [pom[0, 1]],
            [0],
            [0]])
P = np.mat([[5, 0, 0, 0],
          [0, 5, 0, 0],
          [0, 0, 5, 0],
          [0, 0, 0, 5]])
xest = 0
shist.append(s)
Phist.append(P)

for z in pom:
    # predykcja
    sest = A*np.mat(shist[-1])
    print(sest)
    Pest = A*np.mat(Phist[-1])*A.transpose() + B*Q*B.transpose()
    # korekcja
    e = np.mat(z).transpose() - C*sest
    S = C*Pest*C.transpose() + R
    K = Pest*C.transpose()*(S**-1)
    # aktualizacja
    shist.append((sest + K*e))
    Phist.append(((np.eye(4) - K*C) * Pest))


x, y = [], []
for s in shist:
    x.append(s[0][0, 0])
    y.append(s[1][0, 0])


plt.plot(pom[:, 0], pom[:, 1], 'x', label='pomiar')
plt.plot(pom[:, 0], pom[:, 1])
plt.plot(x, y, 'o--', label='filtr')
plt.plot(x, y, '--')
plt.grid()
plt.legend()
#plt.show()
