# Validate p_swap (general lambda) against closed form at lambda=1 and against direct MC.
import numpy as np
from analytic import *
rng = np.random.default_rng(20261102)
n = 200
for delta, rho, lam in [(4.0, 0.85, 1.0), (4.0, 0.85, 1.002), (6.0, 0.5, 0.998), (3.0, -0.7, 1.001), (8.0, 0.9, 1.0)]:
    a = p_swap(np.array([lam]), np.array([delta]), np.array([rho]), np.array([185.0]), n)[0]
    c = p_swap_closed(delta, rho)
    z = rng.multivariate_normal([delta, rho * delta], [[1, rho], [rho, 1]], size=400000)
    A, B = z[:, 0], z[:, 1]
    v = (A**2 - 2*rho*A*B + B**2) / (1 - rho**2)
    E = rng.chisquare(185, size=len(A))
    ev = (n/(n+1))*(lam*B**2 - A**2) - (lam-1)*(E + v) > 0
    print(f"delta={delta} rho={rho} lam={lam}: quad={a:.5f} closed(lam=1)={c:.5f} MC={ev.mean():.5f}")
# p_add / p_drop vs MC
lam = 1.071; m = 184; om = 5.0
B = rng.standard_normal(400000); E = rng.chisquare(m, 400000)
print('add', p_add(np.array([lam]), m, om, n)[0], ((B**2)*(1-lam/(n+1)) > (lam-1)*(E+om)).mean())
Lam = 1.07; dl = 4.5
A = dl + rng.standard_normal(400000)
print('drop', p_drop(np.array([Lam]), np.array([dl]), m, np.array([om]), n)[0], ((A**2)*(1-Lam/(n+1)) < (Lam-1)*(E+om)).mean())
