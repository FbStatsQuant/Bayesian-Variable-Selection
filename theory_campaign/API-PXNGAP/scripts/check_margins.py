"""Population D_S margins on LH-iid (API-PXNGAP §8.3): brute-force enumeration vs the closed-form c2.
For each lattice state S (S° plus a subset of masked hubs, not S0) and every neighbour type, compute
lambda(A) - lambda(P*) with lambda(B) = Var(mu | X_B) from the population Sigma; check >= c2 for non-progress neighbours.
Seed 20261102 for the random parameter draws."""
import itertools, math
import numpy as np

def sigma_lh(g, c, v, rho, psis):
    G = 2 * c + v + 1  # one null group suffices for the neutral/null cases
    p = G * g
    S = np.zeros((p, p))
    for h in range(G):
        blk = slice(h * g, (h + 1) * g)
        S[blk, blk] = rho; np.fill_diagonal(S[blk, blk], 1.0)
    for i in range(c):
        a, b = 2 * i, 2 * i + 1
        ja, jb = a * g, b * g
        ca = S[a * g:(a + 1) * g, ja]; cb = S[jb, b * g:(b + 1) * g]
        S[a * g:(a + 1) * g, b * g:(b + 1) * g] = psis[i] * np.outer(ca, cb)
        S[b * g:(b + 1) * g, a * g:(a + 1) * g] = psis[i] * np.outer(cb, ca)
    return S

def lam(S, theta, B):
    B = sorted(B)
    v = theta @ S @ theta
    if not B: return v
    SBB = S[np.ix_(B, B)]; SB = S[B] @ theta
    return v - SB @ np.linalg.solve(SBB, SB)

def run(g, c, v, rho, psis, betas, bvis):
    S = sigma_lh(g, c, v, rho, psis); p = S.shape[0]
    theta = np.zeros(p)
    ja = [2 * i * g for i in range(c)]; jb = [(2 * i + 1) * g for i in range(c)]
    for i in range(c): theta[ja[i]] = betas[i]; theta[jb[i]] = -psis[i] * betas[i]
    jv = [(2 * c + h) * g for h in range(v)]
    for h in range(v): theta[jv[h]] = bvis[h]
    S0 = set(ja + jb + jv); Sref = set(ja + jv); M = set(jb)
    G = [psis[i] ** 2 * betas[i] ** 2 * (1 - psis[i] ** 2) for i in range(c)]
    eta = [rho ** 2 * (1 - psis[i] ** 2) / (1 - psis[i] ** 2 * rho ** 2) for i in range(c)]
    lam0 = (1 - max(abs(x) for x in psis)) * (1 - rho)
    c4 = min([betas[i] ** 2 * (1 - psis[i] ** 2) ** 2 for i in range(c)] + [betas[i] ** 2 * (1 - psis[i] ** 2) for i in range(c)]
             + G + [b ** 2 for b in bvis])
    c2 = min([min(G), min(G) * (1 - max(eta)), c4] + [betas[i] ** 2 * (1 - psis[i] ** 2) ** 2 for i in range(c)]
             + [lam0 * betas[i] ** 2 for i in range(c)] + [b ** 2 * (1 - rho ** 2) for b in bvis])
    worst = math.inf; worstL = math.inf
    # representative variables: enough to cover every neighbour class (all columns of the first copy of each kind)
    cols = list(range(p))
    for r in range(c):  # lattice states: S° plus r of the masked hubs, r < c
        for Mp in itertools.combinations(sorted(M), r):
            St = Sref | set(Mp); I = [i for i in range(c) if jb[i] not in St]
            istar = max(I, key=lambda i: G[i]); Pstar = St | {jb[istar]}
            lP = lam(S, theta, Pstar)
            progress = {frozenset(St | {jb[i]}) for i in I}
            nbrs = [St]
            for l in cols:
                if l not in St: nbrs.append(St | {l})
            for k in St:
                nbrs.append(St - {k})
                for l in cols:
                    if l not in St: nbrs.append((St - {k}) | {l})
            for A in nbrs:
                if frozenset(A) in progress: continue
                worst = min(worst, lam(S, theta, A) - lP)
    # (L): deletions/swaps of S0 vs c5
    c5 = min([betas[i] ** 2 * (1 - psis[i] ** 2) for i in range(c)] + G + [b ** 2 for b in bvis] + [min(G) * (1 - max(eta))]
             + [lam0 * betas[i] ** 2 for i in range(c)] + [b ** 2 * (1 - rho ** 2) for b in bvis])
    for k in S0:
        worstL = min(worstL, lam(S, theta, S0 - {k}))
        for l in cols:
            if l not in S0: worstL = min(worstL, lam(S, theta, (S0 - {k}) | {l}))
    return worst, c2, worstL, c5

rng = np.random.default_rng(20261102)
bad = 0; rows = []
for t in range(60):
    c = int(rng.integers(1, 4)); v = int(rng.integers(0, 3)); g = int(rng.integers(3, 6))
    rho = float(rng.uniform(0.3, 0.9)); psis = [float(rng.uniform(0.1, rho - 0.05)) * rng.choice([-1, 1]) for _ in range(c)]
    betas = [float(rng.uniform(0.3, 2.0)) * rng.choice([-1, 1]) for _ in range(c)]
    bvis = [float(rng.uniform(0.3, 2.0)) for _ in range(v)]
    w, c2, wL, c5 = run(g, c, v, rho, psis, betas, bvis)
    ok = (w >= c2 - 1e-9) and (wL >= c5 - 1e-9)
    bad += (not ok)
    rows.append((c, v, g, rho, w, c2, wL, c5, ok))
    print(f"c={c} v={v} g={g} rho={rho:.2f} min non-progress margin={w:.4f} c2={c2:.4f} ratio={w/c2:.2f} | (L) min={wL:.4f} c5={c5:.4f} {'OK' if ok else 'VIOLATION'}")
print("settings:", len(rows), "violations:", bad)
