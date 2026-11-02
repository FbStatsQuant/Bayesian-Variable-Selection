r"""F-SHARE: the linked-hub (LH) design in exact Gram form, for the small-p engine bvs_core.py (copied from W4-SHARE).

LH (W1-EXP §4, W3-PXN §0): independent equicorrelated groups of size g (within-group correlation rho), plus, per
masked variable, one rank-one 'suppressor edge' between the hub a_i of one group and the hub b_i of another:
corr(a_i, b_i) = psi, corr(k, b_i) = psi*rho for k in group(a_i)\{a_i}, corr(k', a_i) = psi*rho for k' in group(b_i)\{b_i},
corr(k, k') = psi*rho^2.  Coefficients: theta_{a_i} = beta_i, theta_{b_i} = -psi*beta_i (so x_{b_i} has zero marginal
covariance with mu; the whole group of b_i is orthogonal to mu), visible hubs theta_{j_h} = beta_h, nulls 0.
S0 = {a_i, b_i, j_h}, S° = S0 \ M with M = {b_i} the masked hubs.

Two configurations:
  LH16: p = 16, g = 4, c = 1: groups {0-3}, {4-7}, {8-11}, {12-15}; pair (a, b) = (0, 4); visible hub 8; nulls 12-15.
  LH20: p = 20, g = 4, c = 2: groups of 4; pairs (0, 4) and (8, 12); visible hub 16.
rho = 0.7, psi = 0.5, beta = 1 for every hub, sigma = 1 (W1-EXP config A has (1.4, -0.7, 1.8); the mechanism is the
same).  With B = min(floor(sqrt n), floor(sqrt p), 16) = 4 the v3 complete-linkage partition returns the groups.
"""
import numpy as np


def lh_sigma(p, g, pairs, rho=0.7, psi=0.5):
    R = np.eye(p)
    for c0 in range(0, p, g):
        for i in range(c0, c0 + g):
            for j in range(c0, c0 + g):
                if i != j:
                    R[i, j] = rho
    for (a, b) in pairs:
        ga, gb = a - a % g, b - b % g
        A = [k for k in range(ga, ga + g) if k != a]
        Bp = [k for k in range(gb, gb + g) if k != b]
        R[a, b] = R[b, a] = psi
        for k in A:
            R[k, b] = R[b, k] = psi * rho
        for k in Bp:
            R[k, a] = R[a, k] = psi * rho
        for k in A:
            for kk in Bp:
                R[k, kk] = R[kk, k] = psi * rho ** 2
    lam = np.linalg.eigvalsh(R).min()
    assert lam > 0, f"LH correlation matrix not positive definite: lambda_min = {lam}"
    return R


def lh_config(name, rho=0.7, psi=0.5, beta=1.0):
    if name == "LH16":
        p, g, pairs, vis = 16, 4, [(0, 4)], [8]
    elif name == "LH20":
        p, g, pairs, vis = 20, 4, [(0, 4), (8, 12)], [16]
    else:
        raise ValueError(name)
    R = lh_sigma(p, g, pairs, rho, psi)
    theta = np.zeros(p)
    for (a, b) in pairs:
        theta[a] = beta
        theta[b] = -psi * beta
    for j in vis:
        theta[j] = beta
    S0 = sorted([a for a, _ in pairs] + [b for _, b in pairs] + vis)
    M = sorted(b for _, b in pairs)
    Sref = sorted(set(S0) - set(M))
    return dict(name=name, p=p, g=g, pairs=pairs, vis=vis, R=R, theta=theta, S0=S0, M=M, Sref=Sref,
                lam_min=float(np.linalg.eigvalsh(R).min()))


if __name__ == "__main__":
    for nm in ("LH16", "LH20"):
        c = lh_config(nm)
        print(nm, "p =", c["p"], "S0 =", c["S0"], "S° =", c["Sref"], "M =", c["M"], "lambda_min(R) = %.4f" % c["lam_min"])
