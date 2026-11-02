"""LH-iid generator (copied from W3-PXN scripts/lh_iid.py gen_lh, with return_theta added)."""
import math
import numpy as np

def gen_lh(n, G, g, rho, psi, pairs, visible, rng, sigma=1.0, return_theta=False):
    p = G * g
    X = np.empty((n, p))
    linked_b = {b: (a, beta) for (a, b, beta) in pairs}
    for h in range(G):
        if h in linked_b:
            continue
        f = rng.standard_normal(n)
        X[:, h * g:(h + 1) * g] = math.sqrt(rho) * f[:, None] + math.sqrt(1 - rho) * rng.standard_normal((n, g))
    for b, (a, beta) in linked_b.items():
        hub = psi * X[:, a * g] + math.sqrt(1 - psi ** 2) * rng.standard_normal(n)
        X[:, b * g] = hub
        f = rng.standard_normal(n)
        X[:, b * g + 1:(b + 1) * g] = (rho * hub[:, None] + math.sqrt(rho * (1 - rho)) * f[:, None]
                                       + math.sqrt(1 - rho) * rng.standard_normal((n, g - 1)))
    theta = np.zeros(p)
    M = []
    for (a, b, beta) in pairs:
        theta[a * g] = beta
        theta[b * g] = -psi * beta
        M.append(b * g)
    for (h, beta) in visible:
        theta[h * g] = beta
    y = X @ theta + sigma * rng.standard_normal(n)
    S0 = sorted(np.flatnonzero(theta).tolist())
    Sref = sorted(set(S0) - set(M))
    groups = [list(range(h * g, (h + 1) * g)) for h in range(G)]
    if return_theta:
        return X, y, groups, S0, Sref, sorted(M), theta
    return X, y, groups, S0, Sref, sorted(M)
