# -*- coding: utf-8 -*-
from math import *
import numpy as np
from scipy.optimize import fmin
from scipy import signal


def get_tf(name):
    time = []

    with open(name) as file:
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


    result = fmin(func=lambda params: my_fmin(params, t, velocity), x0=[10, 5, 0.4, 30])

    y_count = []
    for time_1 in t:
        y_count.append(h_prim(time_1, *result))

    #in order: k, T1, T2
    return result[3], result[0], result[1]

p1f = get_tf('p1f.txt')
p1b = get_tf('p1b.txt')
p2f = get_tf('p2f.txt')
p2b = get_tf('p2b.txt')
p5 = get_tf('p5.txt')
p6 = get_tf('p6.txt')
print("p1f: ", p1f)
t1f = signal.TransferFunction(p1f[0], [p1f[1]*p1f[2], (p1f[1]+p1f[2]), 1])
print("p1b: ", p1b)
t1b = signal.TransferFunction(p1b[0], [p1b[1]*p1b[2], (p1b[1]+p1b[2]), 1])
print("p2f: ", p2f)
t2f = signal.TransferFunction(p2f[0], [p2f[1]*p2f[2], (p2f[1]+p2f[2]), 1])
print("p2b: ", p2b)
t2b = signal.TransferFunction(p2b[0], [p2b[1]*p2b[2], (p2b[1]+p2b[2]), 1])
print("p5: ", p5)
t5 = signal.TransferFunction([0, 0, p5[0]], [p5[1]*p5[2], (p5[1]+p5[2]), 1])
print("p6: ", p6)
t6 = signal.TransferFunction(p6[0], [p6[1]*p6[2], (p6[1]+p6[2]), 1])
print("t5:", t5)
# s5 = t5.to_ss()
# print("s5: ", s5)