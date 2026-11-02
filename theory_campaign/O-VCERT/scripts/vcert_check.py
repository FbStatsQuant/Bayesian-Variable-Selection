# O-VCERT independent checks of O-CERT's Lemma M, Thm C4 (box bound), C4 branch-and-bound,
# C1/C2 identities, and the C1(b)/C6 "unscored mass" wording.  Exact target of 00_COMMON §1.
# Written from 00_COMMON.md only (not from O-CERT's cert_lib.R).  Usage: python -I vcert_check.py [seed]
import sys, itertools, math
import numpy as np
from scipy.special import gammaln

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 20261102)
TOL = 1e-9

def lse(v):
    v = np.asarray(v, float); m = v.max()
    return m + math.log(np.exp(v - m).sum()) if np.isfinite(m) else -np.inf

def standardise(Xr, yr):
    n = Xr.shape[0]
    X = Xr - Xr.mean(0); X = X / np.sqrt((X ** 2).sum(0) / (n - 1))
    y = yr - yr.mean(); y = y / math.sqrt((y ** 2).sum() / (n - 1))
    return X, y

class Target:
    def __init__(s, X, y):
        s.X, s.y = X, y; s.n, s.p = X.shape; s.K = min(s.p, s.n // 2)
        s.a0 = s.b0 = 0.01; s.nu = s.a0 + s.n / 2
        s.lCn = s.a0 * math.log(2 * s.b0) + gammaln(s.nu) - (s.n / 2) * math.log(math.pi) - gammaln(s.a0)
        k = np.arange(s.p + 1)
        s.lw = math.log(0.5) - (gammaln(2 * s.p) - gammaln(k + 1) - gammaln(2 * s.p - k))   # log w(k), k=0..p
        lchp = gammaln(s.p + 1) - gammaln(k + 1) - gammaln(s.p - k + 1)
        s.lWK = lse(lchp[: s.K + 1] + s.lw[: s.K + 1]); s.lchp = lchp
        s.yy = float(y @ y); s.cache = {}
    def QD(s, S):
        """Q_S and log D_S from the k x k definition (00_COMMON): H = (n+1)G + I, D = det H / det(G+I)."""
        S = tuple(sorted(S))
        if S in s.cache: return s.cache[S]
        if not S: r = (s.yy, 0.0)
        else:
            XS = s.X[:, S]; G = XS.T @ XS; z = XS.T @ s.y; k = len(S)
            H = (s.n + 1) * G + np.eye(k)
            Q = s.yy - s.n * z @ np.linalg.solve(H, z)
            lD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(G + np.eye(k))[1]
            r = (float(Q), float(lD))
        s.cache[S] = r; return r
    def QD_n(s, S):
        """Lemma M(d): n x n forms."""
        M = s.X[:, list(S)] @ s.X[:, list(S)].T if S else np.zeros((s.n, s.n)); I = np.eye(s.n)
        A = I + (s.n + 1) * M
        Q = s.yy / (s.n + 1) + (s.n / (s.n + 1)) * s.y @ np.linalg.solve(A, s.y)
        lD = np.linalg.slogdet(A)[1] - np.linalg.slogdet(I + M)[1]
        return float(Q), float(lD)
    def F(s, S):
        if len(S) > s.K: return -np.inf
        Q, lD = s.QD(S)
        return s.lw[len(S)] - s.lWK + s.lCn - 0.5 * lD - s.nu * math.log(2 * s.b0 + Q)
    def Phi(s, L, U):
        return s.lw[len(L)] - s.lWK + s.lCn - 0.5 * s.QD(L)[1] - s.nu * math.log(2 * s.b0 + s.QD(U)[0])
    def Mb(s, L, U):
        kL, kU = len(L), min(len(U), s.K); m = len(U) - len(L)
        ks = np.arange(kL, kU + 1)
        lc = gammaln(m + 1) - gammaln(ks - kL + 1) - gammaln(m - ks + kL + 1)
        return lse(lc + s.lw[ks]) - s.lWK + s.lCn - 0.5 * s.QD(L)[1] - s.nu * math.log(2 * s.b0 + s.QD(U)[0])

def subsets(U):
    U = list(U)
    for r in range(len(U) + 1):
        for c in itertools.combinations(U, r): yield c

def design(kind, n, p):
    if kind == "iid": Xr = rng.standard_normal((n, p))
    elif kind == "ar09":
        Xr = np.empty((n, p)); Xr[:, 0] = rng.standard_normal(n)
        for j in range(1, p): Xr[:, j] = 0.9 * Xr[:, j - 1] + math.sqrt(1 - 0.81) * rng.standard_normal(n)
    elif kind == "dup":
        Xr = rng.standard_normal((n, p)); Xr[:, 1] = Xr[:, 0]; Xr[:, 3] = -2 * Xr[:, 2] + 1
    elif kind == "neardup":
        Xr = rng.standard_normal((n, p)); Xr[:, 1] = Xr[:, 0] + 1e-4 * rng.standard_normal(n)
    elif kind == "factor":
        f = rng.standard_normal((n, 2)); Xr = f @ rng.standard_normal((2, p)) + 0.3 * rng.standard_normal((n, p))
    beta = np.zeros(p); act = rng.choice(p, size=min(3, p), replace=False)
    beta[act] = rng.choice([-1, 1], size=len(act)) * rng.uniform(0.2, 1.5, size=len(act))
    yr = Xr @ beta + rng.uniform(0.3, 2.0) * rng.standard_normal(n)
    return standardise(Xr, yr)

out = []
def log(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

# ---------- 1. Lemma M (a)(b)(c)(d), exhaustive over all S, S+j ----------
log("== 1. Lemma M: exhaustive single-addition checks (implies all S <= S' by induction) ==")
tot = dict(pairs=0, Qviol=0, Dviol=0, dviol=0, Qfloor=0, maxdQ=-np.inf, maxdD=-np.inf, maxd=0.0)
cases = [(k, n, p) for k in ["iid", "ar09", "dup", "neardup", "factor"]
         for (n, p) in [(30, 8), (12, 9), (6, 9), (5, 10), (40, 10)]]
for rep in range(6):
    for kind, n, p in cases:
        X, y = design(kind, n, p); T = Target(X, y)
        for S in subsets(range(p)):
            Q, lD = T.QD(S)
            if Q < T.yy / (T.n + 1) - 1e-9 * T.yy: tot["Qfloor"] += 1
            if rep == 0 and len(S) <= 6 and kind != "dup":
                Qn, lDn = T.QD_n(S); tot["maxd"] = max(tot["maxd"], abs(Qn - Q) / T.yy, abs(lDn - lD))
            for j in range(p):
                if j in S: continue
                Q2, lD2 = T.QD(S + (j,)); tot["pairs"] += 1
                tot["maxdQ"] = max(tot["maxdQ"], (Q2 - Q) / T.yy); tot["maxdD"] = max(tot["maxdD"], lD - lD2)
                if Q2 > Q + TOL * T.yy: tot["Qviol"] += 1
                if lD2 < lD - 1e-7: tot["Dviol"] += 1
        # (c): w non-increasing on 0..K, size marginal C(p,k)w(k) is NOT monotone
        lw = T.lw[: T.K + 1]
        assert np.all(np.diff(lw) <= 1e-12), "w not monotone"
log(f"datasets={6*len(cases)}  (S,S+j) pairs={tot['pairs']}  Q increases={tot['Qviol']}  D decreases={tot['Dviol']}")
log(f"  max rel. increase of Q on addition = {tot['maxdQ']:.3e} (<=0 expected); max decrease of log D = {tot['maxdD']:.3e}")
log(f"  Q < y'y/(n+1) occurrences = {tot['Qfloor']};  max |(d) n x n form - k x k form| = {tot['maxd']:.2e}")
T = Target(*design("iid", 30, 8))
sm = T.lchp[: T.K + 1] + T.lw[: T.K + 1]
log(f"  size-prior marginal log C(p,k)w(k), p=8 (not monotone): {np.round(sm,3).tolist()}; per-model log w(k): {np.round(T.lw[:T.K+1],3).tolist()}")

# ---------- 2. Thm C4 box bounds, exhaustive over all boxes L <= U ----------
log("== 2. C4: F(S) <= Phi(L,U) and sum_[L,U] e^F <= e^M(L,U), all 3^p boxes ==")
nb = viol_phi = viol_M = 0; slack_min = np.inf; tight = 0
for rep in range(4):
    for kind, n, p in [(k, n, p) for k in ["iid", "ar09", "dup", "factor"] for (n, p) in [(30, 8), (10, 8), (6, 8)]]:
        X, y = design(kind, n, p); T = Target(X, y)
        Fall = {S: T.F(S) for S in subsets(range(p))}
        for U in subsets(range(p)):
            for L in subsets(U):
                if len(L) > T.K: continue
                rest = [j for j in U if j not in L]
                members = [tuple(sorted(L + c)) for c in subsets(rest)]
                fv = np.array([Fall[S] for S in members]); nb += 1
                ph = T.Phi(L, U); mb = T.Mb(L, U)
                if fv.max() > ph + 1e-8: viol_phi += 1
                if lse(fv) > mb + 1e-8: viol_M += 1
                slack_min = min(slack_min, ph - fv.max())
                if L == U: tight += abs(ph - fv.max()) < 1e-9
log(f"boxes={nb}  Phi violations={viol_phi}  M violations={viol_M}  min slack Phi-max F={slack_min:.2e}  (singleton boxes exact: {tight})")

# 2b. adversarial: a box bound built with the size MARGINAL (C(p,k)w(k)) or with F(U) fails
X, y = design("iid", 30, 8); T = Target(X, y)
bad_FU = 0; tested = 0
for U in subsets(range(8)):
    for L in subsets(U):
        if len(L) > T.K: continue
        rest = [j for j in U if j not in L]
        fmax = max(T.F(tuple(sorted(L + c))) for c in subsets(rest)); tested += 1
        if max(T.F(L), T.F(U) if len(U) <= T.K else -np.inf) < fmax - 1e-9: bad_FU += 1
log(f"  sanity: endpoints max(F(L),F(U)) underestimate the box max in {bad_FU}/{tested} boxes (F itself is not monotone; Phi is needed)")

# ---------- 3. C4 branch and bound vs brute force ----------
log("== 3. C4 branch-and-bound (my implementation) vs brute force over 2^U ==")
def bnb(T, Shat, U, mode="opt", tau=-12.0, max_nodes=10 ** 6):
    Fh = T.F(Shat); stack = [((), tuple(U))]; nodes = 0; better = []; rest = -np.inf
    while stack:
        L, Up = stack.pop(); nodes += 1
        if nodes > max_nodes: return None
        if len(L) > T.K: continue
        if tuple(sorted(L)) != tuple(sorted(Shat)):
            fL = T.F(tuple(sorted(L)))
            if fL > Fh: better.append((tuple(sorted(L)), fL))
        else: fL = -np.inf
        free = [j for j in Up if j not in L]
        if not free:
            if mode == "mass": rest = lse([rest, fL - Fh])
            continue
        if mode == "opt" and T.Phi(L, Up) <= Fh: continue
        if mode == "mass":
            mb = T.Mb(L, Up)
            if mb <= Fh + tau: rest = lse([rest, mb - Fh]); continue
        j = free[0]
        stack.append((L, tuple(x for x in Up if x != j))); stack.append((L + (j,), Up))
    return dict(better=better, rest=rest, nodes=nodes)
agree = dis = 0; mass_ok = mass_bad = 0; nodes_list = []
for rep in range(40):
    kind = ["iid", "ar09", "factor", "dup"][rep % 4]
    X, y = design(kind, 40, 13); T = Target(X, y)
    allS = list(subsets(range(13))); Fv = {S: T.F(S) for S in allS}
    Sstar = max(allS, key=lambda S: (Fv[S], -len(S)))
    for Shat in [Sstar, max([S for S in allS if S != Sstar], key=lambda S: Fv[S])]:
        U = list(range(13)); r = bnb(T, Shat, U)
        cert = len(r["better"]) == 0; truth = all(Fv[S] <= Fv[Shat] for S in allS)
        agree += cert == truth; dis += cert != truth; nodes_list.append(r["nodes"])
        if Shat == Sstar:
            rm = bnb(T, Shat, U, "mass"); lb = 1 / (1 + math.exp(rm["rest"]))
            exact = math.exp(Fv[Shat] - lse([Fv[S] for S in allS if len(S) <= T.K]))
            if lb <= exact + 1e-12: mass_ok += 1
            else: mass_bad += 1
log(f"opt-certificate agrees with brute force: {agree}/{agree+dis}; mass lower bound valid: {mass_ok}/{mass_ok+mass_bad}; "
    f"nodes median {int(np.median(nodes_list))} (2^13 = 8192 leaves)")

# ---------- 4. C1 / C2 identities and the 'unscored' wording ----------
log("== 4. C1/C2 deterministic identities; C1(b)/C6 'unscored mass' wording ==")
X, y = design("factor", 40, 10); T = Target(X, y)
allS = [S for S in subsets(range(10)) if len(S) <= T.K]; Fv = np.array([T.F(S) for S in allS]); lZ = lse(Fv)
order = np.argsort(-Fv); worst = 0
for m in [1, 3, 10, 50]:
    Tset = order[:m]; lZT = lse(Fv[Tset])
    for lZh in lZ + np.linspace(-3, 6, 37):
        for a in [0.05, 0.2, 0.5]:
            u = Fv - max(lZT, math.log(a) + lZh)
            bad_any = np.any(Fv - lZ > u + 1e-12); bad_Z = lZ < math.log(a) + lZh - 1e-12
            worst += bad_any != bad_Z
log(f"C1(b) identity {{exists S: pi(S)>u_a(S)}} == {{Z < a Zhat}}: mismatches = {worst}")
# unscored-mass wording: every model scored (exact branch-like), T = top-m store, Zhat = Z exactly (good event)
for m, a in [(3, 0.5), (10, 0.5), (50, 0.2)]:
    lZT = lse(Fv[order[:m]]); claim = 1 - math.exp(lZT - math.log(a) - lZ); outside = 1 - math.exp(lZT - lZ)
    log(f"  m={m}, a={a}: Z >= aZhat holds (Zhat=Z); claimed 'unscored' mass >= {claim:.3f}; true unscored mass = 0; "
        f"true mass outside T = {outside:.3f} (>= claim: {outside >= claim - 1e-12})")
# Cantelli tightness for C2: two-point W with mean 1, var v: P(W <= 1-eps) attains v/(v+eps^2)
v, eps = 0.25, 0.5; pr = v / (v + eps ** 2); lo = 1 - eps; hi = 1 + v / eps  # P(W=lo)=pr
mean = pr * lo + (1 - pr) * hi; var = pr * (lo - mean) ** 2 + (1 - pr) * (hi - mean) ** 2
log(f"  Cantelli two-point check (C2): mean={mean:.6f} var={var:.6f} P(W<=1-eps)={pr:.4f} = (B/4)/(B/4+eps^2) with B/4={v}")

open(sys.argv[2] if len(sys.argv) > 2 else "vcert_check.txt", "w").write("\n".join(out) + "\n")
