from matplotlib import pyplot as plt
from scipy.signal import *
from scipy.integrate import odeint
from scipy.optimize import fmin

def read(name):
    time = []
    y = []
    with open(name) as plik:
        for line in plik.readlines():
            linie = line.split()
            time.append(float(linie[0].strip()))
            y.append(float(linie[1].strip()))
    return time, y

def sumData(data):
    for i in range(1, len(data)):
        data[i] = data[i]+data[i-1]
    return data

timeT1F, yT1F = read('Train1Forward.txt')
timeT1B, yT1B = read('Train1Backward.txt')
timeT2F, yT2F = read('Train2Forward.txt')
timeT2B, yT2B = read('Train2Backward.txt')
timeT5, yT5 = read('Train5.txt')
timeT6, yT6 = read('Train6.txt')
timeT1F = sumData(timeT1F)
timeT1B = sumData(timeT1B)
timeT2F = sumData(timeT2F)
timeT2B = sumData(timeT2B)
timeT5 = sumData(timeT5)
timeT6 = sumData(timeT6)


