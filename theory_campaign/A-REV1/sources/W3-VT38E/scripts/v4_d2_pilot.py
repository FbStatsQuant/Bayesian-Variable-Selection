#!/usr/bin/env python3
"""W3-VT38E: independent check of W1-T38E Theorem D2 on CF(1) by (a) recomputing its bound in full (including
the Hoeffding term and P(NB^c), which W1's reported number omits) and (b) simulating the pilot's first stage
exactly as the engine does it (iid pi0 draws, pilot_next_phi, multinomial resampling, one random-order round of
p Gibbs + 1 uniform swap + B neighbour swaps + 1 independence proposal per particle) and recording whether S0 is
scored during that first stage.

Usage: python3 v4_d2_pilot.py n seed reps    (seed = -1: W1's design via env W1DIR; else independent design)
Fixed simulation seed 777 + seed.
"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cfi

n, seed, reps = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
c = 1
if seed < 0:
    sys.path.insert(0, os.environ.get('W1DIR', '.'))
    import cf_family as w1
    D = w1.build(n, c); X, y = D['X'], D['y']; info = dict(n=n, p=D['p'], B=D['B'], S0=D['S0'], cl=D['cl'], c=c)
    src = "W1 design"
else:
    X, y, info = cfi.build_cf(n, c, seed); src = "independent design seed %d" % seed
M = cfi.Model(X, y, info); p, B, S0 = info['p'], info['B'], info['S0']
blocks, R = cfi.complete_linkage_blocks(X, B)
st = cfi.Start(M, blocks, S0)
Nb = cfi.neighbour_graph(R, n, B)
N0 = max(2500, n, p); H = math.ceil(512 * N0 / 2500); ell = math.ceil(math.log2(n + p + 1)); Te = max(1000, ell ** 2)
x0 = (0,); j = 1
Dset = [l for l in range(p) if info['cl'][l] == 1 and l != j]

lg0c, dc = {}, {}
def lg0(S):
    v = lg0c.get(S)
    if v is None: v = st.lg0(S); lg0c[S] = v
    return v
def dd(S):
    v = dc.get(S)
    if v is None: v = (M.logm(S) - M.lm0) - (lg0(S) - M.lprior[len(S)]); dc[S] = v
    return v
def flip(S, l):
    return tuple(x for x in S if x != l) if l in S else tuple(sorted(S + (l,)))

# ---- (a) D2 bound
def odds(S, l):
    T = flip(S, l)
    if len(T) > M.K: return 0.0, 0.0
    o0 = math.exp(lg0(T) - lg0(S)); o1 = math.exp(lg0(T) + dd(T) - lg0(S) - dd(S))
    return o0, o1
dep = 0.0; dep_all = 0.0; top = []
for l in range(p):
    if l == j: continue
    o0, o1 = odds(x0, l); mm = max(o0, o1); dep_all += mm
    if l in Dset: continue
    dep += mm; top.append((mm, l + 1))
top.sort(reverse=True)
b = math.exp(st.lpi0(x0)); beta = max(0.0, 1 - dep) / (len(Dset) + B + 3)
g = lambda f: f - math.sqrt(f * (1 - f)) / 3
ts = np.linspace(1e-4, b - 0.1 - 1e-6, 4000)
vals = np.exp(-2 * H * ts ** 2) + np.exp(-H * beta * np.array([g(b - t) for t in ts]))
it = int(np.argmin(vals))
print("== D2 on CF(1) n=%d p=%d B=%d H=%d T_e=%d [%s]" % (n, p, B, H, Te, src))
print("pi0(x0={1}) = b = %.4f ; |D| = %d ; Dep (off D) = %.4f ; Dep incl. D = %.3e ; largest off-D terms %s" % (
    b, len(Dset), dep, dep_all, [(l, round(m, 4)) for m, l in top[:3]]))
print("beta = %.4f ; W1's reported third term exp(-H beta g(b)) = %.3e ; full D2 bound without NB term: min_t [e^{-2Ht^2} + "
      "exp(-H beta g(b-t))] = %.3e at t = %.3f" % (beta, math.exp(-H * beta * g(b)), vals[it], ts[it]))

# ---- (b) simulation of NB and of the pilot's first stage
rng = np.random.default_rng(777 + seed)
rstar = (2.2 + math.sqrt(2.2 ** 2 - 4 * 0.81)) / 1.8
def ess(dv, delta):
    x = delta * np.asarray(dv); m = x.max(); w = np.exp(x - m); return w.sum() ** 2 / (w ** 2).sum()
def pilot_next_phi(dv, phi):
    thr = 0.9 * H
    if ess(dv, 1.0 - phi) >= thr: return 1.0, False
    lo, hi = phi, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if ess(dv, mid - phi) >= thr: lo = mid
        else: hi = mid
    if lo - phi < 1.0 / Te: return min(1.0, phi + 1.0 / Te), True
    return lo, False
def lgphi(S, phi): return lg0(S) + phi * dd(S)

def one_round(S, phi, hit):
    """engine one_round for one particle; hit[0] set to the mechanism that first evaluated S0."""
    m = p + B + 2; order = rng.permutation(m)
    for lab in order:
        if lab < p:                                   # Gibbs
            l = int(lab); inS = l in S
            if not inS and len(S) >= M.K: continue
            T = flip(S, l)
            if T == S0 and hit[0] is None: hit[0] = 'gibbs'
            Sp, Sm = (S, T) if inS else (T, S)
            a = lgphi(Sp, phi) - lgphi(Sm, phi); o = 1 / (1 + math.exp(-a)) if a > -700 else 0.0
            inc = rng.random() < o
            if inc != inS: S = T
        elif lab == p:                                # uniform swap
            k = len(S)
            if k == 0 or k == p: continue
            jj = S[int(rng.random() * k)]; out = [x for x in range(p) if x not in S]; ll = out[int(rng.random() * len(out))]
            T = tuple(sorted(tuple(x for x in S if x != jj) + (ll,)))
            if T == S0 and hit[0] is None: hit[0] = 'uswap'
            if rng.random() < math.exp(min(0.0, lgphi(T, phi) - lgphi(S, phi))): S = T
        elif lab <= p + B:                            # neighbour swap
            k = len(S)
            if k == 0: continue
            jj = S[int(rng.random() * k)]; cand = [x for x in Nb[jj] if x not in S]
            if not cand: continue
            ll = cand[int(rng.random() * len(cand))]
            T = tuple(sorted(tuple(x for x in S if x != jj) + (ll,)))
            back = sum(1 for x in Nb[ll] if x not in T)
            if T == S0 and hit[0] is None: hit[0] = 'nswap'
            la = lgphi(T, phi) - lgphi(S, phi) + math.log(len(cand)) - math.log(back)
            if rng.random() < math.exp(min(0.0, la)): S = T
        else:                                         # independence proposal
            T = st.draw(rng)
            if T == S0 and hit[0] is None: hit[0] = 'indep'
            if rng.random() < math.exp(min(0.0, phi * (dd(T) - dd(S)))): S = T
    return S

nb_fail = 0; found = 0; found_init = 0; phis = []; forced = 0; per_particle = []; mech = {}
for r in range(reps):
    P = [st.draw(rng) for _ in range(H)]
    dv = np.array([dd(S) for S in P])
    init_hit = S0 in P
    if not init_hit and (dv.max() - dv.min()) > Te * math.log(rstar): nb_fail += 1
    phi1, frc = pilot_next_phi(dv, 0.0); phis.append(phi1); forced += frc
    lw = phi1 * dv; w = np.exp(lw - lw.max()); w /= w.sum()
    anc = rng.choice(H, size=H, p=w)
    nhit = 0; any_hit = init_hit
    for i in anc:
        h = [None]; one_round(P[i], phi1, h)
        if h[0] is not None: nhit += 1; mech[h[0]] = mech.get(h[0], 0) + 1
    found_init += init_hit
    found += init_hit or nhit > 0
    per_particle.append(nhit / H)
if reps > 0: print("pilot first stage, %d replications: P(NB^c) est = %d/%d ; S0 among initial draws in %d ; S0 scored by end of stage 1 in %d/%d ;"
      " phi_1 range [%.4g, %.4g], forced %d ; fraction of particles scoring S0 in the stage-1 round: mean %.3f min %.3f ; mechanisms %s" % (
      reps, nb_fail, reps, found_init, found, reps, min(phis), max(phis), forced, np.mean(per_particle), np.min(per_particle), mech))
