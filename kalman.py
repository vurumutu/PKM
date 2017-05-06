import numpy as np
import matplotlib.pyplot as plt
import time

distances = [203, 230, 143+624, 272]
times = [53.9750874511, 27.5069689903, 18.1354904881, 7.80411009911]

class train:
    def __init__(self):
        T = 1
        #initial state
        self.X = np.mat([[0], # x
                        [0], # v
                        [0]]) # a
        self.P = np.mat([[1, 0, 0], # initial wariance
                        [0, 1, 0],
                        [0, 0, 1]])
        # object model
        self.A = np.mat([[1, T, 0],
                        [0, 1, T],
                        [0, 0, 0]])
        self.B = np.mat([[1, 0],
                        [0, 1],
                        [0, 0]])
        self.C = np.mat([[1, 0, 0],
                        [0, 1, 0]])
        #variances
        self.Q = np.mat([[0.025, 0, 0], # process variance
                        [0, 0.025, 0],
                        [0, 0, 0.025]])
        self.R = np.mat([[0.1, 0], # sensor variance
                        [0, 1.0]])
        self.updateTime = 0

    def position(self):
        return X[0,0]

    def velocity(self):
        return X[1,0]

    def _setTimeInA(self, dt):
        self.A[0,1] = dt
        self.A[1,2] = dt

    def predict(self, time):
        ''' parametrem jest aktualny czas, zwracana jest macierz
        ta funkcja nie modyfikuje zadnych zmiennych '''
        dt = time - self.updateTime
        self._setTimeInA(dt)
        print("Time {}".format(dt))
        return self.C*self.A*self.X

    def update(self, distance):
        dt = time.time() - self.updateTime
        self.updateSym(distance, dt)

    def updateSym(self, distance, dt):
        ''' podaj przejechana odleglosc od ostatniej zlapanej balisy'''
        Xpom = np.mat([[distance],
                        [distance / dt]])
        self.updateTime += dt
        self._setTimeInA(dt)
        #predykcja
        Xprio = self.A*self.X
        Pprio = self.A*self.P*self.A.transpose() + self.Q # self.B*self.Q*self.B.transpose()
        #korekcja
        e = Xpom - self.C*Xprio
        temp = self.C*Pprio*self.C.transpose() + self.R
        K = Pprio*self.C.transpose()*np.linalg.inv(temp)
        #aktualizacja
        self.X = Xprio + K*e
        self.P = (np.eye(np.sqrt(np.size(self.A))) - K*self.C) * Pprio


t = train()
tim = [0]
X = [0]
pom = [0]
pred = [0]

print(t.A)
t.A[0,1] = 11
print(t.A)

for i in range(len(distances)):
    pred.append(t.predict(times[i])[0,0])
    t.updateSym(distances[i], times[i])
    X.append(t.X[0,0])
    pom.append(pom[-1]+distances[i])
    tim.append(tim[-1]+times[i])

print(tim)
print(X)
plt.plot(tim, X)
plt.plot(tim, pom, 'o')
plt.plot(tim, pred, 'x')
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
    #predykcja
    sest = A*np.mat(shist[-1])
    print(sest)
    Pest = A*np.mat(Phist[-1])*A.transpose() + B*Q*B.transpose()
    #korekcja
    e = np.mat(z).transpose() - C*sest
    S = C*Pest*C.transpose() + R
    K = Pest*C.transpose()*(S**-1)
    #aktualizacja
    shist.append((sest + K*e))
    Phist.append(((np.eye(4) - K*C) * Pest))


x, y = [], []
for s in shist:
    x.append(s[0][0,0])
    y.append(s[1][0,0])


plt.plot(pom[:, 0], pom[:,1], 'x', label='pomiar')
plt.plot(pom[:, 0], pom[:, 1])
plt.plot(x, y, 'o--', label='filtr')
plt.plot(x, y, '--')
plt.grid()
plt.legend()
plt.show()
