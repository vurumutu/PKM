from math import *
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin

time = []

with open("p1f.txt") as file:
    for line in file.readlines():
        lines = line.split()
        time = np.append(time, float(lines[2].strip()))

t = []
a = 0
for i in range(0, len(time)):
    a += time[i]
    t = np.append(t, a)

time = time[1:]
velocity = 20/time  # cm per second
# prędkość początkowa 0
velocity = np.insert(velocity, 0, 0)


def step_response(t, T1, T2):
    return 1 - (T1/(T1-T2))*e**(-t/T1) + (T2/(T1-T2))*e**(-t/T2)


def impulse_response(t, T1, T2):
    return (e**(-t/T1) - e**(-t/T2)) * (1/(T1-T2))


def my_fmin(param, time, y):
    cost = 0
    for i, t in enumerate(time):
        try:
            cost += (y[i] - h_prim(t, param[0], param[1], param[2], param[3])) ** 2
        except:
            cost += inf
    return cost


def h_prim(t, T1, T2, tau_z, k):
    return k * (tau_z * impulse_response(t, T1, T2) + step_response(t, T1, T2))

# aproksymacja do wielomianu
z = np.polyfit(t, velocity, 4)
p = np.poly1d(z)
xp = np.linspace(min(t), (max(t)), 200)
yp = p(xp)

result = fmin(func=lambda params: my_fmin(params, t, velocity), x0=[10, 5, 0.4, 30])

y_count = []
for time_1 in t:
    y_count.append(h_prim(time_1, *result))
print("       k              T1          T2              Tz")
print(result[3], result[0], result[1], result[2])
plt.plot(t, velocity, 'r.')
plt.plot(t, y_count)
#plt.plot(xp, yp, 'bx')
plt.title("Odpowiedz skokowa")
plt.show()