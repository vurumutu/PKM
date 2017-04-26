import numpy as np
import matplotlib.pyplot as plt
import sys


n_iter = 50
sz = (n_iter,)
x = 10
z = np.random.normal(x, 0.5, size=sz) # @param2: sigma
#z = np.array([np.random.normal(x, 0.5, size=sz),
#              np.random.normal(0, 0.5, size=sz)]).transpose()


#sys.exit()
xhat=np.zeros(sz)       # a posteriori estimate of x
P=np.zeros(sz)          # a posteriori error estimate
xhatminus=np.zeros(sz)  # a priori estimate of x
Pminus=np.zeros(sz)     # a priori error estimate
K=np.zeros(sz)          # gain

R = 0.5**2              # estimate of measurement variance
Q = 1e-5

#initial guesses
xhat[0] = 0.0
P[0] = 1.0


for k in range(1, n_iter):
    #time update
    Pminus[k] = P[k-1]+Q

    #measurement update
    K[k] = Pminus[k] / (Pminus[k] + R)
    xhat[k] = xhat[k-1] + K[k]*(z[k]-xhat[k-1])
    P[k] = (1-K[k])*Pminus[k]

plt.figure()
plt.plot(z,'k+',label='noisy measurements')
plt.plot(xhat,'b-',label='a posteri estimate')
plt.axhline(x,color='g',label='truth value')
plt.legend()
plt.title('Estimate vs. iteration step', fontweight='bold')
plt.xlabel('Iteration')
plt.ylabel('Voltage')

plt.figure()
valid_iter = range(1,n_iter) # Pminus not valid at step 0
plt.plot(valid_iter,Pminus[valid_iter],label='a priori error estimate')
plt.title('Estimated a priori error vs. iteration step', fontweight='bold')
plt.xlabel('Iteration')
plt.ylabel('$(Voltage)^2$')
#plt.setp(plt.gca(),'ylim',[0,.01])
plt.show()