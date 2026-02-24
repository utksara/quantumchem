import numpy as np

v1 = np.transpose(np.array([1, 1]))
v2 = np.transpose(np.array([1, 0]))

E1 = 2
E2 = 1
A = E1*np.outer(v1, np.transpose(v1)) + E2*np.outer(v2, np.transpose(v2))

print(A)
print(np.linalg.eig(A))