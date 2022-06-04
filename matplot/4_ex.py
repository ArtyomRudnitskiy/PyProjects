import numpy as np

A = np.array([[1, 2, 3], [2, 1, -1], [3, 3, 2]])
B = np.array([4, 3, 3])

X = np.linalg.solve(A, B)
print(X)
