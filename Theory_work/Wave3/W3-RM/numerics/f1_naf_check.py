r"""f1_naf_check.py -- falsification attempt for Lemma NA-F and Lemma N-loc (lemmas/L2_NAF.md). OBSERVATIONS ONLY.

Checks, on small fixed designs where the whole lattice [S0, Q] can be enumerated:
 (A) Lemma N-loc identity/bound: for every (T, l), N = T & N_l, a = (I-P_T)x_l, b = (P_T-P_N)x_l:
       a _|_ b,  ||u_{T,l} - u_{N,l}||^2 = 2(1 - (1+t^2)^(-1/2)) <= t^2,  t = ||b||/||a||.
 (B) Decomposition (2.1): |Z_{T,l}| <= |v^T eps| + ||u_{T,l}-v|| * ||Pi_l eps||  with v = u_{N,l}, Pi_l = proj on span X_{Q u {l}}.
 (C) The Step-3 bound: max_{T,l} Z^2 <= a^2 + 2 a rho sqrt(G) + rho^2 G on the event E1 & E2, where
       a^2 = max_v (v^T eps)^2 over the approximant set, G = max_l ||Pi_l eps||^2, rho = max ||u - v||
     (this is the deterministic implication used in Step 3, checked with the realised a^2 and G).
Designs: (D1) iid Gaussian columns; (D2) AR(1) columns rho=0.6 (Q = a window around S0, N_l = the 2 nearest members of Q on
each side); (D3) one-factor columns (worst case for locality: rho is NOT small; the checks (A)-(C) are identities/inequalities
and must still hold). sigma = 1. n = 120, p = 40, |Q| = 9, s0 = 2, 20 seeds each.
Output: f1_naf_out.txt (counts of violations; max slack).
"""
import itertools, sys
import numpy as np

def proj(X, idx):
    if len(idx) == 0:
        return np.zeros((X.shape[0], X.shape[0]))
    A = X[:, sorted(idx)]
    Qm, _ = np.linalg.qr(A)
    return Qm @ Qm.T

def unit(v):
    return v / np.linalg.norm(v)

def design(kind, n, p, rng):
    if kind == "iid":
        W = rng.standard_normal((n, p))
    elif kind == "ar1":
        r = 0.6
        W = np.empty((n, p)); W[:, 0] = rng.standard_normal(n)
        for j in range(1, p):
            W[:, j] = r * W[:, j - 1] + np.sqrt(1 - r * r) * rng.standard_normal(n)
    else:
        f = rng.standard_normal((n, 1))
        W = 0.7 * f + np.sqrt(1 - 0.49) * rng.standard_normal((n, p))
    W = W - W.mean(0)
    return W / W.std(0, ddof=1)

def run(kind, seed, n=120, p=40, out=None):
    rng = np.random.default_rng(seed)
    X = design(kind, n, p, rng)
    S0 = [10, 20]
    Q = sorted(set(S0) | {8, 9, 11, 12, 19, 21, 22})
    Pset = [t for t in Q if t not in S0]
    eps = rng.standard_normal(n)
    I = np.eye(n)
    # N_l: the (up to) 4 members of Q nearest to l in index distance, l excluded
    Nl = {l: sorted(sorted([t for t in Q if t != l], key=lambda t: abs(t - l))[:4]) for l in range(p)}
    PQ = proj(X, Q)
    viol = dict(A_orth=0, A_ident=0, A_bound=0, B=0, C=0)
    pairs = 0; rho_max = 0.0; a2 = 0.0; G = 0.0; Zmax2 = 0.0; slackB = np.inf
    cacheP = {}
    def P(idx):
        k = tuple(sorted(idx))
        if k not in cacheP: cacheP[k] = proj(X, k)
        return cacheP[k]
    Pil = {l: (PQ if l in Q else proj(X, Q + [l])) for l in range(p)}
    for r in range(len(Pset) + 1):
        for ex in itertools.combinations(Pset, r):
            T = sorted(S0 + list(ex)); PT = P(T)
            for l in range(p):
                if l in T: continue
                N = sorted(set(T) & set(Nl[l])); PN = P(N)
                a = (I - PT) @ X[:, l]; b = (PT - PN) @ X[:, l]
                u = unit(a); v = unit(a + b)
                t = np.linalg.norm(b) / np.linalg.norm(a)
                d2 = float(np.sum((u - v) ** 2))
                if abs(a @ b) > 1e-8 * np.linalg.norm(a) * max(np.linalg.norm(b), 1e-300): viol["A_orth"] += 1
                if abs(d2 - 2 * (1 - (1 + t * t) ** -0.5)) > 1e-8: viol["A_ident"] += 1
                if d2 > t * t + 1e-10: viol["A_bound"] += 1
                Z = float(u @ eps); ve = float(v @ eps); pe = float(np.linalg.norm(Pil[l] @ eps))
                rhs = abs(ve) + np.sqrt(d2) * pe
                slackB = min(slackB, rhs - abs(Z))
                if abs(Z) > rhs + 1e-9: viol["B"] += 1
                rho_max = max(rho_max, np.sqrt(d2)); a2 = max(a2, ve * ve); G = max(G, pe * pe); Zmax2 = max(Zmax2, Z * Z)
                pairs += 1
    boundC = a2 + 2 * np.sqrt(a2) * rho_max * np.sqrt(G) + rho_max ** 2 * G
    if Zmax2 > boundC + 1e-9: viol["C"] += 1
    line = (f"{kind:4s} seed={seed:2d} pairs={pairs} rho_max={rho_max:.4f} maxZ2={Zmax2:.3f} boundC={boundC:.3f} "
            f"min_slack_B={slackB:.3e} violations={viol}")
    print(line); out.write(line + "\n")
    return viol

if __name__ == "__main__":
    tot = {}
    with open("f1_naf_out.txt", "w") as out:
        for kind in ("iid", "ar1", "fac"):
            for seed in range(20):
                v = run(kind, seed, out=out)
                for k, x in v.items(): tot[k] = tot.get(k, 0) + x
        s = f"TOTAL violations over 60 runs: {tot}"
        print(s); out.write(s + "\n")
