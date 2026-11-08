"""n8: end-to-end LS0-route diagnostic for W1-PXN (LH-iid, SIZE holds, p > n).  ASCII only.

Pipeline per fit: LH-iid draw -> standardise -> score F -> partition (complete linkage, top-down cut,
next-fit packing) -> block tables r_b(U) -> exact start law pi0 (max-plus / log-sum-exp convolution over
blocks with total size as state) -> start mode S~0 -> LS0 (production local search) -> diagnostics.
Self-contained (does not import lhcommon, so nothing is written outside n8/).
"""
import itertools
import math
import os
import sys
import time

import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
from scipy.special import gammaln, logsumexp

HERE = os.path.dirname(os.path.abspath(__file__))
B0 = 0.01
NEG = -np.inf


# ------------------------------------------------------------------ design
def build_sigma(p, g, c, rho, psi):
    Sigma = np.eye(p)
    G = p // g
    A = (1 - rho) * np.eye(g) + rho * np.ones((g, g))
    for h in range(G):
        Sigma[h * g:(h + 1) * g, h * g:(h + 1) * g] = A
    u = np.full(g, rho)
    u[0] = 1.0
    for i in range(c):
        a, b = 2 * i, 2 * i + 1
        blk = psi[i] * np.outer(u, u)
        Sigma[a * g:(a + 1) * g, b * g:(b + 1) * g] = blk
        Sigma[b * g:(b + 1) * g, a * g:(a + 1) * g] = blk.T
    return Sigma


def build_theta(p, g, c, v, psi, beta, betavis):
    th = np.zeros(p)
    for i in range(c):
        th[2 * i * g] = beta[i]
        th[(2 * i + 1) * g] = -psi[i] * beta[i]
    for h in range(v):
        th[(2 * c + h) * g] = betavis[h]
    return th


def standardise(Xr, yr):
    n = Xr.shape[0]
    Xc = Xr - Xr.mean(0)
    X = Xc / np.linalg.norm(Xc, axis=0) * np.sqrt(n - 1)
    Y = yr - yr.mean()
    y = Y / np.linalg.norm(Y) * np.sqrt(n - 1)
    return X, y


# ------------------------------------------------------------------ score
def log_w(k, p):
    N = 2 * p - 1
    k = np.asarray(k, dtype=float)
    return np.log(0.5) - (gammaln(N + 1) - gammaln(k + 1) - gammaln(N - k + 1))


class Scorer:
    """F(S) = log w(|S|) + log m(S) (constants -log W_K and the (2b0)^a0 Gamma factors dropped; they cancel
    in every comparison and in pi0).  Batched over sets of equal size."""

    def __init__(self, X, y):
        self.n, self.p = X.shape
        self.Gram = X.T @ X
        self.z = X.T @ y
        self.yy = float(y @ y)
        self.nu = 0.01 + self.n / 2.0
        self.K = min(self.p, self.n // 2)
        self.lm0 = -self.nu * np.log(2 * B0 + self.yy)  # log m(empty), constant dropped
        self.nscored = 0

    def logm_batch(self, idx):
        """idx: int array (m, k), k >= 1.  Returns log m (const dropped) for each row."""
        n = self.n
        m, k = idx.shape
        self.nscored += m
        G = self.Gram[idx[:, :, None], idx[:, None, :]]
        z = self.z[idx]
        I = np.eye(k)[None]
        H = (n + 1) * G + I
        LH = np.linalg.cholesky(H)
        LG = np.linalg.cholesky(G + I)
        logD = 2 * (np.log(np.diagonal(LH, axis1=1, axis2=2)).sum(1) - np.log(np.diagonal(LG, axis1=1, axis2=2)).sum(1))
        sol = np.linalg.solve(H, z[:, :, None])[:, :, 0]
        Q = self.yy - n * (z * sol).sum(1)
        return -0.5 * logD - self.nu * np.log(2 * B0 + Q)

    def F_sets(self, sets):
        """sets: list of sorted tuples (any sizes).  Returns np array of F."""
        out = np.empty(len(sets))
        by = {}
        for i, s in enumerate(sets):
            by.setdefault(len(s), []).append(i)
        for k, ii in by.items():
            if k == 0:
                out[ii] = log_w(0, self.p) + self.lm0
            else:
                idx = np.array([sets[i] for i in ii], dtype=np.int64)
                out[ii] = log_w(k, self.p) + self.logm_batch(idx)
        return out


# ------------------------------------------------------------------ partition
def make_blocks(X, B):
    n, p = X.shape
    R = np.corrcoef(X, rowvar=False)
    D = 1.0 - np.abs(R)
    D = (D + D.T) / 2
    np.fill_diagonal(D, 0.0)
    D[D < 0] = 0.0
    Z = linkage(squareform(D, checks=False), method="complete")
    members = {i: (i,) for i in range(p)}
    kids = {}
    for r in range(p - 1):
        a, b = int(Z[r, 0]), int(Z[r, 1])
        if min(members[a]) > min(members[b]):
            a, b = b, a
        members[p + r] = tuple(sorted(members[a] + members[b]))
        kids[p + r] = (a, b)
    root = 2 * p - 2
    stack = [root]
    retained = []
    while stack:
        nd = stack.pop()
        if len(members[nd]) > B:
            a, b = kids[nd]
            stack.append(b)
            stack.append(a)
        else:
            retained.append(members[nd])
    bins, cur = [], []
    for cl in retained:
        if len(cur) + len(cl) <= B:
            cur = cur + list(cl)
        else:
            bins.append(sorted(cur))
            cur = list(cl)
    if cur:
        bins.append(sorted(cur))
    return [tuple(b) for b in bins]


# ------------------------------------------------------------------ block tables, pi0
class BlockTable:
    def __init__(self, sc, members, cap):
        self.members = members
        sz = len(members)
        self.cap = min(sz, cap, sc.K)
        self.truncated = self.cap < sz
        self.vals = {}   # k -> array of log r_b(U)
        self.sets = {}   # k -> list of global sorted tuples
        self.lookup = {}  # tuple(global) -> log r
        for k in range(0, self.cap + 1):
            combs = list(itertools.combinations(range(sz), k))
            glob = [tuple(members[j] for j in cb) for cb in combs]
            if k == 0:
                vals = np.zeros(1)
            else:
                idx = np.array(glob, dtype=np.int64)
                vals = sc.logm_batch(idx) - sc.lm0
            self.vals[k] = vals
            self.sets[k] = glob
            for gs, vv in zip(glob, vals):
                self.lookup[gs] = vv
        self.best_val = np.array([self.vals[k].max() for k in range(self.cap + 1)])
        self.best_arg = [int(np.argmax(self.vals[k])) for k in range(self.cap + 1)]  # first = lex smallest
        self.lse = np.array([logsumexp(self.vals[k]) for k in range(self.cap + 1)])

    def best_set(self, k):
        return self.sets[k][self.best_arg[k]]


def pi0_machinery(sc, tables):
    K = sc.K
    nb = len(tables)
    # max-plus DP with backpointers
    dp = np.full(K + 1, NEG)
    dp[0] = 0.0
    choices = []
    E = np.full(K + 1, NEG)
    E[0] = 0.0
    for tb in tables:
        new = np.full(K + 1, NEG)
        ch = np.full(K + 1, -1, dtype=np.int64)
        newE = np.full(K + 1, NEG)
        for k in range(tb.cap + 1):
            if k > K:
                break
            cand = np.full(K + 1, NEG)
            cand[k:] = dp[:K + 1 - k] + tb.best_val[k]
            better = cand > new  # strict: smaller k wins ties
            new = np.where(better, cand, new)
            ch = np.where(better, k, ch)
            ce = np.full(K + 1, NEG)
            ce[k:] = E[:K + 1 - k] + tb.lse[k]
            newE = np.logaddexp(newE, ce)
        dp, E = new, newE
        choices.append(ch)
    lw = log_w(np.arange(K + 1), sc.p)
    tot = lw + dp
    t_star = int(np.argmax(tot))  # first max = smallest size
    # backtrack
    S = []
    t = t_star
    for b in range(nb - 1, -1, -1):
        k = int(choices[b][t])
        S.extend(tables[b].best_set(k))
        t -= k
    S0t = tuple(sorted(S))
    logZ = logsumexp(lw + E)
    return S0t, logZ, lw


def log_pi0(sc, tables_of, blocks, lw, logZ, S):
    """log pi0(S) via block lookup; tables_of: dict block-index per element."""
    per = {}
    for j in S:
        per.setdefault(tables_of[j], []).append(j)
    tot = 0.0
    for bi, el in per.items():
        key = tuple(sorted(el))
        tb = blocks[bi]
        if key not in tb.lookup:
            return NEG
        tot += tb.lookup[key]
    return float(lw[len(S)] + tot - logZ)


# ------------------------------------------------------------------ local search
def neighbours(S, p, K):
    """All flips and swaps of centre S (sorted tuple).  Returns list of sorted tuples."""
    Sset = set(S)
    out = []
    for j in range(p):
        if j in Sset:
            out.append(tuple(sorted(Sset - {j})))
        elif len(S) + 1 <= K:
            out.append(tuple(sorted(Sset | {j})))
    for k in S:
        base = Sset - {k}
        for l in range(p):
            if l not in Sset:
                out.append(tuple(sorted(base | {l})))
    return out


class LS:
    def __init__(self, sc):
        self.sc = sc
        self.cache = {}   # centre -> (Fc, nbrs list, F array)
        self.scored = set()

    def scan(self, S):
        if S in self.cache:
            return self.cache[S]
        sc = self.sc
        nb = neighbours(S, sc.p, sc.K)
        F = sc.F_sets([S] + nb)
        res = (F[0], nb, F[1:])
        self.cache[S] = res
        return res

    def run(self, S0t, ell):
        S = S0t
        moves = 0
        scored = {S}
        path = [S]
        certified = limit = False
        for k in range(ell + 1):
            Fc, nb, F = self.scan(S)
            scored.update(nb)
            mx = F.max()
            if mx > Fc:
                cands = [nb[i] for i in np.nonzero(F == mx)[0]]
                best = min(cands)  # lexicographic
                if k < ell:
                    S = best
                    moves += 1
                    path.append(S)
                else:
                    limit = True
            else:
                certified = True
                break
        return S, moves, certified, limit, scored, path


def role(j, g):
    return f"{j}[G{j // g}{'h' if j % g == 0 else 'm'}]"


def diff_desc(S, A, g):
    a = sorted(set(A) - set(S))
    r = sorted(set(S) - set(A))
    return "".join("+" + role(j, g) for j in a) + "".join("-" + role(j, g) for j in r) or "self"


def margin_at(ls, S, missing_b, g=9):
    """(D_S) margin at lattice state S: F(best progress nbr) - max(F(S), non-progress nbrs).
    Returns (margin, description of the best competitor relative to S)."""
    Fc, nb, F = ls.scan(S)
    prog = {tuple(sorted(set(S) | {b})) for b in missing_b}
    pm = []
    npm = [(Fc, S)]
    for A, f in zip(nb, F):
        if A in prog:
            pm.append(f)
        else:
            npm.append((f, A))
    best = max(npm, key=lambda t: t[0])
    return max(pm) - best[0], diff_desc(S, best[1], g)


# ------------------------------------------------------------------ one fit
def one_fit(n, p, g, c, v, rho, psi, beta, betavis, sigma, seed):
    rng = np.random.default_rng([seed, n, p, c, v, int(1000 * psi[-1])])
    Sigma = build_sigma(p, g, c, rho, psi)
    L = np.linalg.cholesky(Sigma)
    theta = build_theta(p, g, c, v, psi, beta, betavis)
    Xr = rng.standard_normal((n, p)) @ L.T
    yr = Xr @ theta + sigma * rng.standard_normal(n)
    X, y = standardise(Xr, yr)
    sc = Scorer(X, y)
    Bn = min(int(math.isqrt(n)), int(math.isqrt(p)), 16)
    blocks_m = make_blocks(X, Bn)
    groups = [tuple(range(h * g, (h + 1) * g)) for h in range(p // g)]
    eq = set(blocks_m) == set(groups)
    S0 = tuple(sorted(j for j in range(p) if theta[j] != 0))
    Mset = [(2 * i + 1) * g for i in range(c)]
    Sdeg = tuple(sorted(set(S0) - set(Mset)))
    s_ref = len(Sdeg)
    tables = [BlockTable(sc, bm, 12 if len(bm) <= 12 else 7) for bm in blocks_m]
    trunc = any(t.truncated for t in tables)
    tables_of = {}
    for bi, bm in enumerate(blocks_m):
        for j in bm:
            tables_of[j] = bi
    S0t, logZ, lw = pi0_machinery(sc, tables)
    lp_ref = log_pi0(sc, tables_of, tables, lw, logZ, Sdeg)
    lp_S0 = log_pi0(sc, tables_of, tables, lw, logZ, S0)
    lp_t = log_pi0(sc, tables_of, tables, lw, logZ, S0t)
    ell = math.ceil(math.log2(n + p + 1))
    ls = LS(sc)
    Sfin, moves, cert, lim, scored, path = ls.run(S0t, ell)
    # margins along visited lattice states
    lat_states = []
    for r in range(c):
        for sub in itertools.combinations(Mset, r):
            lat_states.append(tuple(sorted(set(Sdeg) | set(sub))))
    vis_margins = []
    for S in path:
        if S in lat_states:
            miss = [b for b in Mset if b not in S]
            vis_margins.append(margin_at(ls, S, miss, g))
    all_m = [margin_at(ls, S, [b for b in Mset if b not in S], g) for S in lat_states]
    all_margins = [m[0] for m in all_m]
    worst_all = min(all_m, key=lambda t: t[0])
    # (L) at S0
    F0, nb0, Fn0 = ls.scan(S0)
    L_gap = F0 - Fn0.max()
    L_comp = diff_desc(S0, nb0[int(np.argmax(Fn0))], g)
    rec = dict(
        blocks_eq_groups=eq, truncated=trunc, nblocks=len(blocks_m), maxblock=max(len(b) for b in blocks_m),
        start_eq_ref=(S0t == Sdeg), start=S0t, one_minus_pi0ref=(-np.expm1(lp_ref) if np.isfinite(lp_ref) else 1.0),
        lp_S0=lp_S0, lp_start=lp_t, S0_scored=(S0 in scored), certified_S0=(cert and Sfin == S0),
        final_eq_S0=(Sfin == S0), moves=moves, limit=lim,
        n_vis_lat=len(vis_margins), vis_margin=(min(m[0] for m in vis_margins) if vis_margins else np.nan),
        all_margin=min(all_margins), DS_comp=worst_all[1], L_comp=L_comp, path=path, L_holds=bool(L_gap > 0), L_gap=L_gap, ell=ell, Bn=Bn,
        nscored=sc.nscored, F_S0_minus_Fref=float(sc.F_sets([S0])[0] - sc.F_sets([Sdeg])[0]),
    )
    return rec


# ------------------------------------------------------------------ driver
class Tee:
    def __init__(self, name):
        self.path = os.path.join(HERE, name)
        self.lines = []

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        self.lines.append(s)

    def close(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines) + "\n")


from scipy.stats import chi2


def fmt(x, d=3):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "nan"
    return f"{x:.{d}f}"


def main():
    nseeds = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    out = Tee("n8_route.txt")
    g, rho, sigma = 9, 0.7, 1.0
    cells = []
    for (n, p) in [(150, 270), (300, 540)]:
        for c in (1, 2):
            for v in (0, 1):
                cells.append((n, p, c, v, tuple([0.5] * c)))
    cells.append((300, 540, 2, 1, (0.5, 0.3)))
    cells.append((150, 270, 2, 1, (0.5, 0.3)))
    out("n8 end-to-end LS0 route; g=9 rho=0.7 beta=1 beta_vis=1 sigma=1; seeds per cell =", nseeds)
    out("cols: A=blocks==groups, E=S~0==S0ref(Sref), Sc=S0 scored by LS0, Ce=S0 returned+certified, L=(L) holds at S0,")
    out("      DSvis=min over visited lattice states of (D_S) margin, DSall=min over all lattice states (visited or not)")
    hdr = ("n,p,c,v,psi | A | E | Sc | Ce | L | moves(mean) | 1-pi0(Sref) med/max | log pi0(S0)+c log p+(c/2)log n  med (pred) | "
           "DSvis min/med | DSall min/med | Lgap min/med")
    out(hdr)
    allfits = []
    t0 = time.time()
    for (n, p, c, v, psi) in cells:
        recs = []
        for sd in range(nseeds):
            r = one_fit(n, p, g, c, v, rho, psi, [1.0] * c, [1.0] * v, sigma, sd)
            r["seed"] = sd
            recs.append(r)
        allfits.append(((n, p, c, v, psi), recs))
        k = len(recs)
        cnt = lambda key: sum(1 for r in recs if r[key])
        s = c + v
        cent = [r["lp_S0"] + c * math.log(p) + (c / 2) * math.log(n) for r in recs]
        pc = sum(math.log((s + i) / 2) for i in range(1, c + 1))
        pred = pc + c / 2
        predmed = pc + 0.5 * chi2.ppf(0.5, c)
        om = np.array([r["one_minus_pi0ref"] for r in recs])
        vm = np.array([r["vis_margin"] for r in recs], dtype=float)
        am = np.array([r["all_margin"] for r in recs])
        lg = np.array([r["L_gap"] for r in recs])
        mv = np.mean([r["moves"] for r in recs])
        out(f"{n},{p},{c},{v},{psi} | {cnt('blocks_eq_groups')}/{k} | {cnt('start_eq_ref')}/{k} | {cnt('S0_scored')}/{k} | "
            f"{cnt('certified_S0')}/{k} | {cnt('L_holds')}/{k} | {mv:.2f} | {fmt(np.median(om),4)}/{fmt(om.max(),4)} | "
            f"{fmt(float(np.median(cent)),2)} (pred med {fmt(predmed,2)}, mean {fmt(pred,2)}; obs mean {fmt(float(np.mean(cent)),2)}) | {fmt(np.nanmin(vm) if np.isfinite(vm).any() else np.nan,2)}/"
            f"{fmt(np.nanmedian(vm) if np.isfinite(vm).any() else np.nan,2)} | {fmt(am.min(),2)}/{fmt(np.median(am),2)} | "
            f"{fmt(lg.min(),2)}/{fmt(np.median(lg),2)}   [{time.time()-t0:.0f}s]")
    out("")
    out("Per-fit detail (cell; seed; blocks==groups; start==Sref; 1-pi0(Sref); log pi0(S0); S0 scored; certified; moves; limit; "
        "DSvis; DSall; Lgap; F(S0)-F(Sref); nblocks; maxblock; trunc)")
    for (cell, recs) in allfits:
        for r in recs:
            out(f"{cell} s{r['seed']} A={int(r['blocks_eq_groups'])} E={int(r['start_eq_ref'])} 1-pi0={r['one_minus_pi0ref']:.3e} "
                f"lpS0={r['lp_S0']:.2f} Sc={int(r['S0_scored'])} Ce={int(r['certified_S0'])} mv={r['moves']} lim={int(r['limit'])} "
                f"DSvis={fmt(r['vis_margin'],2)} DSall={fmt(r['all_margin'],2)} Lgap={fmt(r['L_gap'],2)} "
                f"dF={fmt(r['F_S0_minus_Fref'],2)} DSworst_competitor={r['DS_comp']} L_best_nbr={r['L_comp']} nb={r['nblocks']} mb={r['maxblock']} tr={int(r['truncated'])}"
                + ("" if r["start_eq_ref"] else f" START={r['start']}"))
    out(f"total runtime {time.time()-t0:.0f}s; cells={len(cells)}; seeds/cell={nseeds}")
    out.close()


if __name__ == "__main__":
    main()
