import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

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


z = np.polyfit(t, velocity, 3)

p = np.poly1d(z)
xp = np.linspace(min(t), (max(t)), 200)
y = p(xp)
print(y)
plt.plot(t, velocity, '.', xp, p(xp), 'g')
plt.show()
