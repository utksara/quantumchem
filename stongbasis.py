import numpy as np
from math import pi, pow,exp

import matplotlib.pyplot as plt

def sto_ng(alpha, r, N):
    m = len(alpha)
    psi = np.zeros((N, m))

    dr = r/N
    for i in range(0, m):
        a = alpha[i]
        for j in range(0, N):
            psi[j][i] = pow(2*a/pi, 0.75)*exp(-a*j*j*dr*dr)

    return psi

psi = sto_ng([0.1, 0.2, 0.3], 1, 10)
c = np.array([0.3, 0.4, 0.3])
plt.plot(psi)
state = psi*c
print(state)
plt.show()


