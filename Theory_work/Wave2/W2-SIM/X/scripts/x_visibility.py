"""x_visibility.py -- W2-SIM family X, brief question 2 (FAC-XA C2 visibility constant).
FAC-XA STATEMENT (locked v1): c(U, j) = Cov(x_j, mu | x_U) on the population Sigma scale, mu = sum_{i in S0} theta_i x_i,
c0 = inf_n min |c(U, j)| over |U| <= 15, j not in U, and (j in S0 or U does not contain S0).
One-factor Sigma = lam lam' + diag(psi), psi = 1 - lam^2, l_i = lam_i/sqrt(psi_i). Exact closed form (Woodbury; derived
here, verified numerically below against direct linear algebra on random U):
   Q_U = sum_{i in U} l_i^2,  a_V = sum_{i in V} lam_i theta_i (V = U cap S0),  m = sum_{i in S0} lam_i theta_i,
   null j (U must miss a truth):  c(U, j) = lam_j (m - a_V) / (1 + Q_U)
   truth j not in U:              c(U, j) = psi_j theta_j + lam_j (m - a_V) / (1 + Q_U)
So c depends on U only through (V, Q_U); Q_U = Q_V + (sum of l^2 over the |U| - |V| <= 15 - |V| nulls in U).
For finitely many loading classes the attainable Q_U are enumerated exactly (class counts); for continuous loadings the
attainable set is reported as the interval [Q_V, Q_V + top-(15-|V|) null l^2 sum] (dense as p grows), and c0 over it
is the min |c| on the interval (0 if c changes sign inside).
Theta: the design's coefficients (raw beta = standardized theta since Sigma has unit diagonal).
Usage: python x_visibility.py OUT.json"""
import sys, json, math, itertools
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import x_paths as xp


def c_direct(lam, theta_full, U, j):
    p = len(lam)
    Sig = np.outer(lam, lam) + np.diag(1 - lam ** 2)
    U = list(U)
    s_jmu = Sig[j] @ theta_full
    if not U:
        return float(s_jmu)
    s_Umu = Sig[U] @ theta_full
    return float(s_jmu - Sig[j, U] @ np.linalg.solve(Sig[np.ix_(U, U)], s_Umu))


def c_closed(lam, theta_full, S0, U, j):
    l2 = lam ** 2 / (1 - lam ** 2)
    m = float(sum(lam[i] * theta_full[i] for i in S0))
    V = [i for i in U if i in S0]
    a = float(sum(lam[i] * theta_full[i] for i in V))
    Q = float(sum(l2[i] for i in U))
    base = lam[j] * (m - a) / (1 + Q)
    return float(base + ((1 - lam[j] ** 2) * theta_full[j] if j in S0 else 0.0))


def c0_design(lam, theta_full, S0, umax=15):
    p = len(lam)
    l2 = lam ** 2 / (1 - lam ** 2)
    S0 = list(S0)
    nulls = [i for i in range(p) if i not in S0]
    m = float(sum(lam[i] * theta_full[i] for i in S0))
    classes = np.unique(np.round(lam[nulls], 12))
    finite = len(classes) <= 4
    best = dict(c0=np.inf, arg=None)
    for r in range(0, len(S0) + 1):
        for V in itertools.combinations(S0, r):
            a = float(sum(lam[i] * theta_full[i] for i in V))
            QV = float(sum(l2[i] for i in V))
            rest = umax - len(V)
            if finite:
                cnt = [sum(1 for i in nulls if abs(lam[i] - c) < 1e-9) for c in classes]
                cl2 = [c * c / (1 - c * c) for c in classes]
                Qs = set()
                for combo in itertools.product(*[range(0, min(rest, k) + 1) for k in cnt]):
                    if sum(combo) <= rest:
                        Qs.add(QV + sum(k * q for k, q in zip(combo, cl2)))
                Qset = sorted(Qs)
                qint = None
            else:
                top = np.sort(l2[nulls])[::-1][:rest].sum()
                qint = (QV, QV + float(top)); Qset = None
            targets = [("null", j) for j in ([nulls[0]] if finite and len(classes) == 1 else nulls)] if len(V) < len(S0) else []
            targets += [("truth", j) for j in S0 if j not in V]
            # null j: |c| = lam_j |m - a| / (1 + Q) minimal at max Q; any null works, smallest lam_j
            if len(V) < len(S0):
                lmin = float(lam[nulls].min())
                Qmax = (max(Qset) if Qset is not None else qint[1])
                v = lmin * abs(m - a) / (1 + Qmax)
                if v < best["c0"]:
                    best = dict(c0=v, arg=dict(kind="null", V=list(V), Q=Qmax, lam_j=lmin))
            for j in S0:
                if j in V:
                    continue
                f = lambda Q: (1 - lam[j] ** 2) * theta_full[j] + lam[j] * (m - a) / (1 + Q)
                if Qset is not None:
                    for Q in Qset:
                        v = abs(f(Q))
                        if v < best["c0"]:
                            best = dict(c0=v, arg=dict(kind="truth", j=int(j), V=list(V), Q=Q))
                else:
                    lo, hi = qint
                    if f(lo) * f(hi) <= 0:
                        v = 0.0
                    else:
                        v = min(abs(f(lo)), abs(f(hi)))
                    if v < best["c0"]:
                        best = dict(c0=v, arg=dict(kind="truth", j=int(j), V=list(V), Qint=qint, sign_change=v == 0.0))
    return best


if __name__ == "__main__":
    out = {}
    rng = np.random.default_rng(5)
    # closed form check
    errs = []
    for kind in ("cs", "two03_09", "unif02_09"):
        lam = xp.loadings(60, kind, 0.5)
        th = xp.truth_beta(60)
        S0 = list(np.flatnonzero(th))
        for _ in range(300):
            k = int(rng.integers(0, 16))
            U = sorted(rng.choice(60, size=k, replace=False).tolist())
            j = int(rng.choice([i for i in range(60) if i not in U]))
            errs.append(abs(c_direct(lam, th, U, j) - c_closed(lam, th, S0, U, j)))
    out["closed_form_check_max_abs_err"] = max(errs)
    rows = []
    for kind, rho in (("cs", 0.3), ("cs", 0.5), ("cs", 0.7), ("two03_09", None), ("two05_095", None), ("unif02_09", None)):
        for coef in ("std", "rev"):
            for p in (500, 2000, 5000):
                lam = xp.loadings(p, kind, rho if rho else 0.5)
                th = xp.truth_beta(p, coef)
                S0 = list(np.flatnonzero(th))
                b = c0_design(lam, th, S0)
                rows.append(dict(load=kind, rho=rho, coef=coef, p=p, c0=b["c0"], argmin=b["arg"],
                                 truth_lam=[float(lam[i]) for i in S0]))
                print(kind, rho, coef, p, "c0 = %.4g" % b["c0"], b["arg"], flush=True)
    out["rows"] = rows
    json.dump(out, open(sys.argv[1], "w"), indent=1, default=float)
    print("closed-form check max abs err", out["closed_form_check_max_abs_err"])
