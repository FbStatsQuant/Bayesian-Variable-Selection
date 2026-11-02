#!/usr/bin/env python3
"""W2-BOOK: exact law of the frozen-run island on the T12 appendix instance (n = 20, p = 2).

Independent re-implementation (written from STATEMENT.md of T12, not from p2_exact.py, which is not in the repo).
No randomness is used: every law is propagated exactly (mpmath, 50 digits). Seed is irrelevant (fixed at 0 for form).

What it computes (component example; scope as in T12(iv.b): N = 1, T = 1, p = 2 is not the production budget):
  1. The instance: BF, pi0, d, Z/Z0, PIP_1.
  2. Exact law of (B, k) for one island I(c), c = (grid (0,1), N = 1, L' = 5, M = 4, flag unset), where
     Zhat/Z0 = exp(D B), B = 1{X0 = {1,2}}, PIPhat_1 = c0 + (c1 - c0) k / 4.
     Checks T12(i.a), (ii): E[Zhat] = Z, E[Zhat PIPhat_1] = Z PIP_1.
     Replicates T12(iv.b): E[Pbar_1] - PIP_1 (locked value -0.173974177850).
  3. Pooled x pooled: E[Zhat * Pbar_1] over four iid islands, by direct enumeration, against the closed form
     Z PIP_1 + (3/4) Z (E[PIPhat_1] - PIP_1)  (Proposition P2(c) of the report).
     Also the pooled island product E[(1/4) sum_r Zhat_r PIPhat_r1] = Z PIP_1.
  4. Run/output split: a stylised wall-time guard (cost of scoring a size-k model = 1 + k^3 units) checked after
     the stage-1 bridge stage, as in the engine (v3_engine.h: guard->check after each final bridge stage).
     Output-available event O_h = {stage-0 + stage-1 cost <= h}. Reports E[Zhat | O_h] / Z and
     E[Zhat PIPhat_1 | O_h] / (Z PIP_1) for every threshold h at which O_h and O_h^c both have positive probability.
"""
import itertools, json, sys
from mpmath import mp, mpf, matrix, det, exp, log, sqrt, eye

mp.dps = 50
SEED = 0  # no Monte Carlo; recorded for protocol compliance

n, p = 20, 2
x1 = [mpf((7 * i) % 20) - mpf('9.5') for i in range(n)]
x2 = [x1[i] + ((5 * i * i) % 7 - 3) for i in range(n)]
yr = [x1[i] - x2[i] + ((3 * i) % 5 - 2) for i in range(n)]

def standardise(v):
    m = sum(v) / n
    c = [vi - m for vi in v]
    s = sqrt(sum(ci * ci for ci in c) / (n - 1))
    return [ci / s for ci in c]

X = [standardise(x1), standardise(x2)]
y = standardise(yr)
a0 = b0 = mpf('0.01')
nu = a0 + mpf(n) / 2
yty = sum(v * v for v in y)

def log_bf(S):
    S = sorted(S)
    if not S:
        return mpf(0)
    k = len(S)
    G = matrix(k, k); z = matrix(k, 1)
    for a in range(k):
        z[a] = sum(X[S[a]][i] * y[i] for i in range(n))
        for b in range(k):
            G[a, b] = sum(X[S[a]][i] * X[S[b]][i] for i in range(n))
    H = (n + 1) * G + eye(k)
    GI = G + eye(k)
    D = det(H) / det(GI)
    Hinv = H ** -1
    Q = yty - n * (z.T * Hinv * z)[0]
    return -log(D) / 2 - nu * (log(2 * b0 + Q) - log(2 * b0 + yty))

# states: 0 = {}, 1 = {1}, 2 = {2}, 3 = {1,2}
STATES = [(), (0,), (1,), (0, 1)]
SIZE = [0, 1, 1, 2]
lb = [log_bf(S) for S in STATES]
b1, b2, b12 = exp(lb[1]), exp(lb[2]), exp(lb[3])
w = [mpf(1) / 2, mpf(1) / 6, mpf(1) / 6, mpf(1) / 6]  # varpi, W_K = 1
gamma0 = [w[0], w[1] * b1, w[2] * b2, w[3] * b1 * b2]
dvec = [mpf(0), mpf(0), mpf(0), lb[3] - lb[1] - lb[2]]
D = dvec[3]
Zb0 = sum(gamma0)
pi0 = [g / Zb0 for g in gamma0]

def gam(phi):
    return [gamma0[s] * exp(phi * dvec[s]) for s in range(4)]

g1 = gam(1)
Z_over_Z0 = sum(g1) / Zb0
pi = [g / sum(g1) for g in g1]
PIP1 = pi[1] + pi[3]

ADD = {(0, 0): 1, (0, 1): 2, (1, 0): 1, (1, 1): 3, (2, 0): 3, (2, 1): 2, (3, 0): 3, (3, 1): 3}  # (state, j) -> S u {j}
REM = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 1, (2, 0): 2, (2, 1): 0, (3, 0): 2, (3, 1): 1}  # (state, j) -> S \ {j}

def cost(k):
    return 1 + k ** 3

# Elementary steps as branching maps: state -> list of (prob, new_state, cost_increment, recording_or_None)
def step(label, s, phi):
    g = gam(phi)
    if label in ('G1', 'G2'):
        j = 0 if label == 'G1' else 1
        up, dn = ADD[(s, j)], REM[(s, j)]
        o = g[up] / (g[up] + g[dn])
        c = cost(SIZE[up]) + cost(SIZE[dn])  # SR: both configurations evaluated
        return [(o, up, c), (1 - o, dn, c)]
    if label in ('U', 'N'):
        # p = 2, B = 1: uniform and neighbour swap coincide (T12 PROOF_v6 §8.2)
        if s in (0, 3):
            return [(mpf(1), s, 0)]
        t = 2 if s == 1 else 1
        acc = min(mpf(1), g[t] / g[s])
        return [(acc, t, cost(1)), (1 - acc, s, cost(1))]
    if label == 'I':
        out = []
        for t in range(4):
            acc = min(mpf(1), exp(phi * (dvec[t] - dvec[s]))) if t != s else mpf(1)
            out.append((pi0[t] * acc, t, cost(SIZE[t])))
            if t != s:
                out.append((pi0[t] * (1 - acc), s, cost(SIZE[t])))
        return out
    raise ValueError(label)

LABELS = ['G1', 'G2', 'U', 'N', 'I']
ORDERS = list(itertools.permutations(LABELS))

def add(dist, key, pr):
    dist[key] = dist.get(key, mpf(0)) + pr

def round_kernel_with_cost(dist, phi, track_cost=False, track_k=False):
    """dist: {(B, state, k, cost): prob}. Applies one uniformly-ordered round."""
    out = {}
    for order in ORDERS:
        cur = {key: pr / len(ORDERS) for key, pr in dist.items()}
        for label in order:
            nxt = {}
            for (B, s, k, c), pr in cur.items():
                kk = k + (1 if (track_k and label == 'G1' and s in (2, 3)) else 0)  # pre-Gibbs-1 state contains 2
                for q, t, dc in step(label, s, phi):
                    if q == 0:
                        continue
                    add(nxt, (B, t, kk, c + dc if track_cost else 0), pr * q)
            cur = nxt
        for key, pr in cur.items():
            add(out, key, pr)
    return out

def island_law(Lp=5, M=4, track_cost=False):
    # stage 0: X0 ~ pi0, scored (cost c(|X0|))
    dist = {}
    for s in range(4):
        add(dist, (1 if s == 3 else 0, s, 0, cost(SIZE[s]) if track_cost else 0), pi0[s])
    # stage 1: weight exp(D B) (recorded in B), trivial resampling (N = 1), one round at phi = 1
    dist = round_kernel_with_cost(dist, mpf(1), track_cost=track_cost)
    if track_cost:
        return dist  # guard is checked here (after the stage-1 bridge stage)
    for _ in range(Lp):
        dist = round_kernel_with_cost(dist, mpf(1))
    for _ in range(M):
        dist = round_kernel_with_cost(dist, mpf(1), track_k=True)
    law = {}
    for (B, s, k, c), pr in dist.items():
        add(law, (B, k), pr)
    return law

c0 = g1[1] / (g1[1] + g1[0])
c1 = g1[3] / (g1[3] + g1[2])
def pip_hat(k, M=4):
    return c0 + (c1 - c0) * mpf(k) / M

def main():
    res = {"D": D, "pi0_12": pi0[3], "c0": c0, "c1": c1, "PIP1": PIP1, "Z_over_Z0": Z_over_Z0}
    law = island_law()
    EZ = sum(pr * exp(D * B) for (B, k), pr in law.items())
    EZP = sum(pr * exp(D * B) * pip_hat(k) for (B, k), pr in law.items())
    EP = sum(pr * pip_hat(k) for (B, k), pr in law.items())
    res["identity_Z_rel"] = (EZ - Z_over_Z0) / Z_over_Z0
    res["identity_ZP_rel"] = (EZP - Z_over_Z0 * PIP1) / (Z_over_Z0 * PIP1)
    res["bias_primary_Pbar"] = EP - PIP1
    # pooled x pooled, direct enumeration over four iid islands
    items = list(law.items())
    EZPbar = mpf(0); Eisl = mpf(0)
    for combo in itertools.product(items, repeat=4):
        pr = combo[0][1] * combo[1][1] * combo[2][1] * combo[3][1]
        Zs = [exp(D * kv[0][0]) for kv in combo]
        Ps = [pip_hat(kv[0][1]) for kv in combo]
        EZPbar += pr * (sum(Zs) / 4) * (sum(Ps) / 4)
        Eisl += pr * sum(Zs[r] * Ps[r] for r in range(4)) / 4
    closed = Z_over_Z0 * PIP1 + mpf(3) / 4 * Z_over_Z0 * (EP - PIP1)
    res["pooled_x_pooled_rel_bias"] = (EZPbar - Z_over_Z0 * PIP1) / (Z_over_Z0 * PIP1)
    res["pooled_x_pooled_minus_closed_form"] = EZPbar - closed
    res["pooled_island_product_rel"] = (Eisl - Z_over_Z0 * PIP1) / (Z_over_Z0 * PIP1)
    # guard counterexample
    cl = island_law(track_cost=True)
    # joint law of (B, cost) at the guard check; the rest of the run depends on the past only through the state
    # at the end of the stage-1 round, so also keep state for E[Zhat PIPhat | O]
    costs = sorted(set(c for (B, s, k, c) in cl))
    # continuation: from each state after stage-1 round, law of k over L' + M rounds
    cont = {}
    for s0 in range(4):
        dist = {(0, s0, 0, 0): mpf(1)}
        for _ in range(5):
            dist = round_kernel_with_cost(dist, mpf(1))
        for _ in range(4):
            dist = round_kernel_with_cost(dist, mpf(1), track_k=True)
        cont[s0] = {}
        for (B, s, k, c), pr in dist.items():
            add(cont[s0], k, pr)
    guard = []
    for h in costs[:-1]:
        PO = sum(pr for (B, s, k, c), pr in cl.items() if c <= h)
        EZO = sum(pr * exp(D * B) for (B, s, k, c), pr in cl.items() if c <= h)
        EZPO = sum(pr * exp(D * B) * sum(q * pip_hat(kk) for kk, q in cont[s].items())
                   for (B, s, k, c), pr in cl.items() if c <= h)
        if PO == 0:
            continue
        guard.append({"h": h, "P_O": PO, "E_Zhat_given_O_over_Z": EZO / PO / Z_over_Z0,
                      "E_ZhatPIPhat_given_O_over_ZPIP": EZPO / PO / (Z_over_Z0 * PIP1),
                      "E_Zhat_1O_over_Z": EZO / Z_over_Z0})
    res["guard"] = guard
    def fmt(v):
        if isinstance(v, list):
            return [{kk: fmt(vv) for kk, vv in d.items()} for d in v]
        return float(v) if not isinstance(v, int) else v
    out = {k: fmt(v) for k, v in res.items()}
    print(json.dumps(out, indent=1))
    # assertions that the report relies on (with wide margins against 50-digit rounding)
    assert abs(res["identity_Z_rel"]) < mpf(10) ** -40
    assert abs(res["identity_ZP_rel"]) < mpf(10) ** -40
    assert abs(res["bias_primary_Pbar"] - mpf('-0.173974177850')) < mpf(10) ** -11
    assert abs(res["pooled_x_pooled_minus_closed_form"]) < mpf(10) ** -35
    assert abs(res["pooled_island_product_rel"]) < mpf(10) ** -40
    assert res["pooled_x_pooled_rel_bias"] < mpf('-0.13')
    assert any(g["E_Zhat_given_O_over_Z"] < mpf('0.9') for g in res["guard"])
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
