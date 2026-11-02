#!/usr/bin/env python3
"""W5-LOCKBOOK: independent re-derivation of W2-BOOK's exact frozen-run numbers (T12(iv.b) component instance).

Written from the T12 STATEMENT (Docs/Theory/proofs/T12_T8_frozen_run_identities/STATEMENT.md, sections 0-2 and the
appendix), not from W2-BOOK's frozen_run_exact.py. Differences in method from W2-BOOK:
  * the Bayes factors use explicit 2x2 closed forms (no matrix library);
  * each elementary step is a 4x4 stochastic matrix; a round is handled through the exact tensor
        J[x, y, z] = (1/m!) sum_sigma  Prefix_sigma[x, y] * Suffix_sigma[y, z],
    where y is the state immediately before the Gibbs-1 step (the recording position) and z the round's end state;
  * the island law of (B, k) is propagated with these tensors (k = number of measured rounds whose pre-G1 state
    contains variable 2), and the 4-island pooled quantities are computed both by the closed form and by
    convolution of four independent copies.
No Monte Carlo: SEED is recorded only for protocol form. mpmath at 60 digits.

Also re-derives the stylised guard COUNTEREXAMPLE of W2-BOOK PROOF.md section 0.3 under (a) W2-BOOK's cost
convention (Gibbs pays both configurations) and (b) the engine-faithful convention found in AUDIT.md section 3
(the held state is not re-evaluated: a Gibbs step pays one evaluation, the other configuration).
"""
import itertools, json
from mpmath import mp, mpf, sqrt, log, exp

mp.dps = 60
SEED = 0

n = 20
x1r = [mpf((7 * i) % 20) - mpf(19) / 2 for i in range(n)]
x2r = [x1r[i] + ((5 * i * i) % 7 - 3) for i in range(n)]
yrr = [x1r[i] - x2r[i] + ((3 * i) % 5 - 2) for i in range(n)]

def std(v):
    mu = sum(v) / n
    c = [a - mu for a in v]
    s = sqrt(sum(a * a for a in c) / (n - 1))
    return [a / s for a in c]

x1, x2, y = std(x1r), std(x2r), std(yrr)
dot = lambda a, b: sum(p * q for p, q in zip(a, b))
yty = dot(y, y)                      # = n - 1
r12 = dot(x1, x2)                    # G_12 (G_11 = G_22 = n - 1)
z1, z2 = dot(x1, y), dot(x2, y)
a0 = b0 = mpf(1) / 100
nu = a0 + mpf(n) / 2
g = n - 1

def logBF_single(z):
    # k = 1: H = (n+1)(n-1) + 1 = n^2, G + I = n, D = n^2 / n = n; Q = y'y - n z^2 / n^2
    D = mpf(n * n) / n
    Q = yty - z * z / n
    return -log(D) / 2 - nu * (log(2 * b0 + Q) - log(2 * b0 + yty))

def logBF_pair():
    # H = (n+1)G + I with G = [[g, r],[r, g]]: H = [[h, c],[c, h]], h = (n+1)g + 1, c = (n+1) r
    h = (n + 1) * g + 1; c = (n + 1) * r12
    detH = h * h - c * c
    gi = g + 1
    detGI = gi * gi - r12 * r12
    D = detH / detGI
    # z' H^{-1} z = (h z1^2 - 2 c z1 z2 + h z2^2) / detH
    quad = (h * z1 * z1 - 2 * c * z1 * z2 + h * z2 * z2) / detH
    Q = yty - n * quad
    return -log(D) / 2 - nu * (log(2 * b0 + Q) - log(2 * b0 + yty))

L1, L2, L12 = logBF_single(z1), logBF_single(z2), logBF_pair()
# states 0 = {}, 1 = {1}, 2 = {2}, 3 = {1,2}; p = 2, K = 2, BB(1, p) prior capped at K = p (W_K = 1)
# w(k) = 1/2 / C(2p - 1, k): w(0) = 1/2, w(1) = 1/6, w(2) = 1/6
w = [mpf(1) / 2, mpf(1) / 6, mpf(1) / 6, mpf(1) / 6]
blocks_logr = [mpf(0), L1, L2, L1 + L2]           # blocks {1}, {2} (B = 1)
logBF = [mpf(0), L1, L2, L12]
d = [logBF[s] - blocks_logr[s] for s in range(4)]  # d = 0 except d({1,2}) = D
D = d[3]
gam0 = [w[s] * exp(blocks_logr[s]) for s in range(4)]
Zb0 = sum(gam0)
pi0 = [v / Zb0 for v in gam0]
def gam(phi):
    return [gam0[s] * exp(phi * d[s]) for s in range(4)]
g1 = gam(1)
Z_over_Z0 = sum(g1) / Zb0          # Z / (m(empty) Zbar_0)
pi = [v / sum(g1) for v in g1]
PIP1 = pi[1] + pi[3]

SIZE = [0, 1, 1, 2]
def has(s, j):  # j in {0, 1} for variables 1, 2
    return bool(s & (1 << j))

def zeros():
    return [[mpf(0)] * 4 for _ in range(4)]

def K_gibbs(j, phi):
    G = gam(phi); M = zeros()
    for s in range(4):
        up, dn = s | (1 << j), s & ~(1 << j)
        o = G[up] / (G[up] + G[dn])
        M[s][up] += o; M[s][dn] += 1 - o
    return M

def K_swap(phi):
    # uniform swap and neighbour swap coincide at p = 2, B = 1 (N(1) = {2}, N(2) = {1}, ratio |N(j)\S|/|N(l)\S'| = 1)
    G = gam(phi); M = zeros()
    for s in range(4):
        if SIZE[s] in (0, 2):
            M[s][s] = mpf(1); continue
        t = 3 - s
        a = min(mpf(1), G[t] / G[s])
        M[s][t] += a; M[s][s] += 1 - a
    return M

def K_indep(phi):
    M = zeros()
    for s in range(4):
        for t in range(4):
            a = min(mpf(1), exp(phi * (d[t] - d[s])))
            M[s][t] += pi0[t] * a; M[s][s] += pi0[t] * (1 - a)
    return M

def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def eye():
    M = zeros()
    for i in range(4): M[i][i] = mpf(1)
    return M

def round_tensor(phi):
    Ks = {'G1': K_gibbs(0, phi), 'G2': K_gibbs(1, phi), 'U': K_swap(phi), 'N': K_swap(phi), 'I': K_indep(phi)}
    labels = list(Ks)
    J = [[[mpf(0)] * 4 for _ in range(4)] for _ in range(4)]
    perms = list(itertools.permutations(labels))
    for sig in perms:
        k = sig.index('G1')
        P = eye()
        for lab in sig[:k]: P = mm(P, Ks[lab])
        S = eye()
        for lab in sig[k:]: S = mm(S, Ks[lab])
        for x in range(4):
            for yy in range(4):
                if P[x][yy] == 0: continue
                for z in range(4):
                    J[x][yy][z] += P[x][yy] * S[yy][z] / len(perms)
    Kround = [[sum(J[x][yy][z] for yy in range(4)) for z in range(4)] for x in range(4)]
    return J, Kround

J1, K1 = round_tensor(mpf(1))
o1 = [g1[s | 1] / (g1[s | 1] + g1[s & ~1]) for s in range(4)]   # recorded o_1 before G1 at state s
c0, c1 = o1[0], o1[2]  # 2 not in S, 2 in S

def island_law(Lp=5, M=4):
    # stage 0: X0 ~ pi0, B = 1{X0 = {1,2}}; stage 1 (phi_1 = 1, N = 1): weight, trivial resampling, one round
    dist = {}
    for s in range(4):
        dist[(1 if s == 3 else 0, s, 0)] = dist.get((1 if s == 3 else 0, s, 0), 0) + pi0[s]
    def apply_round(dist, record):
        out = {}
        for (B, x, k), pr in dist.items():
            for yy in range(4):
                for z in range(4):
                    q = J1[x][yy][z]
                    if q == 0: continue
                    kk = k + (1 if (record and has(yy, 1)) else 0)
                    key = (B, z, kk)
                    out[key] = out.get(key, 0) + pr * q
        return out
    dist = apply_round(dist, False)          # stage-1 round
    for _ in range(Lp): dist = apply_round(dist, False)
    for _ in range(M): dist = apply_round(dist, True)
    law = {}
    for (B, x, k), pr in dist.items():
        law[(B, k)] = law.get((B, k), 0) + pr
    return law

law = island_law()
Zh = lambda B: exp(D * B)                     # Zhat / Z0
Ph = lambda k: c0 + (c1 - c0) * mpf(k) / 4    # PIPhat_1
EZ = sum(pr * Zh(B) for (B, k), pr in law.items())
EZP = sum(pr * Zh(B) * Ph(k) for (B, k), pr in law.items())
EP = sum(pr * Ph(k) for (B, k), pr in law.items())
cov = EZP - EZ * EP
res = dict(D=D, pi0_12=pi0[3], c0=c0, c1=c1, PIP1=PIP1, Z_over_Z0=Z_over_Z0,
           rel_err_EZ=(EZ - Z_over_Z0) / Z_over_Z0, rel_err_EZP=(EZP - Z_over_Z0 * PIP1) / (Z_over_Z0 * PIP1),
           bias_Pbar=EP - PIP1, bias_formula_minus_cov_over_Z=(EP - PIP1) + cov / Z_over_Z0)
# pooled: closed form (3/4 covariance) and convolution of four independent islands
closed = Z_over_Z0 * PIP1 - mpf(3) / 4 * cov
items = list(law.items())
EZPbar = 0; Eisl = 0
for combo in itertools.product(items, repeat=4):
    pr = 1
    for kv in combo: pr *= kv[1]
    Zs = [Zh(kv[0][0]) for kv in combo]; Ps = [Ph(kv[0][1]) for kv in combo]
    EZPbar += pr * sum(Zs) / 4 * sum(Ps) / 4
    Eisl += pr * sum(Zs[r] * Ps[r] for r in range(4)) / 4
res.update(pooledxpooled_rel_bias=(EZPbar - Z_over_Z0 * PIP1) / (Z_over_Z0 * PIP1),
           pooledxpooled_minus_closed=EZPbar - closed,
           pooled_island_product_rel=(Eisl - Z_over_Z0 * PIP1) / (Z_over_Z0 * PIP1),
           three_quarters_cov_over_Z=mpf(3) / 4 * cov / Z_over_Z0)

# ---------------- stylised guard counterexample ----------------
def cost(k):
    return 1 + k ** 3

def stage1_cost_law(convention):
    """Joint law of (B, end state, cost) after stage 0 draw + stage-1 round; costs per W2-BOOK section 0.3.
    convention 'both': Gibbs pays c(|S u j|) + c(|S \\ j|); 'flip': Gibbs pays c(|S Delta j|) only (engine, SR)."""
    phi = mpf(1)
    Gm = gam(phi)
    def steps(label, s):
        if label in ('G1', 'G2'):
            j = 0 if label == 'G1' else 1
            up, dn = s | (1 << j), s & ~(1 << j)
            o = Gm[up] / (Gm[up] + Gm[dn])
            other = dn if has(s, j) else up
            c = cost(SIZE[up]) + cost(SIZE[dn]) if convention == 'both' else cost(SIZE[other])
            return [(o, up, c), (1 - o, dn, c)]
        if label in ('U', 'N'):
            if SIZE[s] in (0, 2): return [(mpf(1), s, 0)]
            t = 3 - s; a = min(mpf(1), Gm[t] / Gm[s])
            return [(a, t, cost(1)), (1 - a, s, cost(1))]
        out = []
        for t in range(4):
            a = min(mpf(1), exp(phi * (d[t] - d[s])))
            out.append((pi0[t] * a, t, cost(SIZE[t])))
            out.append((pi0[t] * (1 - a), s, cost(SIZE[t])))
        return out
    labels = ['G1', 'G2', 'U', 'N', 'I']
    perms = list(itertools.permutations(labels))
    out = {}
    for s0 in range(4):
        for sig in perms:
            cur = {(s0, cost(SIZE[s0])): pi0[s0] / len(perms)}
            for lab in sig:
                nxt = {}
                for (s, c), pr in cur.items():
                    for q, t, dc in steps(lab, s):
                        if q == 0: continue
                        nxt[(t, c + dc)] = nxt.get((t, c + dc), 0) + pr * q
                cur = nxt
            for (s, c), pr in cur.items():
                key = (1 if s0 == 3 else 0, c)
                out[key] = out.get(key, 0) + pr
    return out

guard = {}
for conv in ('both', 'flip'):
    cl = stage1_cost_law(conv)
    hs = sorted(set(c for (B, c) in cl))
    rows = []
    for h in hs[:-1]:
        PO = sum(pr for (B, c), pr in cl.items() if c <= h)
        EZO = sum(pr * Zh(B) for (B, c), pr in cl.items() if c <= h)
        rows.append(dict(h=h, P_O=PO, E_Zhat_given_O_over_Z=EZO / PO / Z_over_Z0, E_Zhat_1O_over_Z=EZO / Z_over_Z0))
    guard[conv] = rows

def f(v):
    if isinstance(v, (list, tuple)): return [f(x) for x in v]
    if isinstance(v, dict): return {k: f(x) for k, x in v.items()}
    return v if isinstance(v, int) else float(v)

print(json.dumps(f(res), indent=1))
for conv in guard:
    print(f"guard convention {conv}: rows with stop share in (0.1%, 5%)")
    for r in guard[conv]:
        if mpf('0.95') < r['P_O'] < mpf('0.999'):
            print("  h=%d P(O)=%.6f E[Zhat|O]/Z=%.5f E[1_O Zhat]/Z=%.5f" % (r['h'], r['P_O'], r['E_Zhat_given_O_over_Z'], r['E_Zhat_1O_over_Z']))
# assertions
assert abs(res['rel_err_EZ']) < mpf(10) ** -50 and abs(res['rel_err_EZP']) < mpf(10) ** -50
assert abs(res['bias_Pbar'] - mpf('-0.173974177850')) < mpf(10) ** -11
assert abs(res['bias_formula_minus_cov_over_Z']) < mpf(10) ** -50
assert abs(res['pooledxpooled_minus_closed']) < mpf(10) ** -45
assert abs(res['pooled_island_product_rel']) < mpf(10) ** -50
print("ALL CHECKS PASSED")
