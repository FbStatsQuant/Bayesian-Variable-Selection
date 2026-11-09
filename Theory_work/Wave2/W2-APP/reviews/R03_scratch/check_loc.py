"""Independent algebra checks for R03; numerical checks are not proofs."""
import numpy as np

rng = np.random.default_rng(20261109)
p, n = 28, 400
# A banded covariance with non-banded precision (not AR(1)).
B = np.eye(p) + 0.27 * np.eye(p, k=1) - 0.11 * np.eye(p, k=2)
S = B @ B.T
sd = np.sqrt(np.diag(S))
S = S / sd[:, None] / sd[None, :]
W = rng.multivariate_normal(np.zeros(p), S, size=n)
T, A, l = [3, 4, 8, 9, 11, 12, 15, 20], [9, 11], 10
F = [j for j in T if j not in A]

def beta(J):
    return np.linalg.solve(S[np.ix_(J, J)], S[J, l])

def centered(V):
    return V - V.mean(axis=0)

eT, eA = W[:, l] - W[:, T] @ beta(T), W[:, l] - W[:, A] @ beta(A)
D = W[:, T] @ beta(T) - W[:, A] @ beta(A)
QT = np.linalg.qr(centered(W[:, T]), mode='reduced')[0]
def residual(v):
    return v - QT @ (QT.T @ v)

print('residual identity max error:', np.max(np.abs(residual(centered(W[:, l])) - residual(centered(eA)))))
print('decomposition max error:', np.max(np.abs(eA - eT - D)))
M = S[np.ix_(F, F)] - S[np.ix_(F, A)] @ np.linalg.solve(S[np.ix_(A, A)], S[np.ix_(A, F)])
c = S[F, l] - S[np.ix_(F, A)] @ np.linalg.solve(S[np.ix_(A, A)], S[A, l])
v_formula = c @ np.linalg.solve(M, c)
b = np.zeros(p)
b[T] = beta(T)
b[A] -= beta(A)
v_direct = b @ S @ b
print('D variance formula:', v_formula)
print('D direct linear-combination variance:', v_direct)
print('D variance absolute error:', abs(v_formula - v_direct))

# Nonzero raw means invalidate the uncentered chi-square assertion.
n2 = 100000
w1 = rng.normal(3.0, 1.0, size=n2)
print('noncentral countercheck ||W_1||^2/n (claimed central limit 1; threshold 4):', w1 @ w1 / n2)

# Radius one does not reproduce L6's nearest-selected-neighbour innovation.
rho = 0.5
print('AR1 l=2, T={4}, radius=1: limiting variance of Z-Zprime:', 2 * (1 - np.sqrt(1-rho**4)))
