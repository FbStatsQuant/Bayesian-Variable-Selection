# Copied verbatim from theory/W4-T38FULL:theory_campaign/W4-T38FULL/scripts/lh_ls0_check.py (functions reused by scaling.py)
"""W4-T38FULL: numerical check of Proposition LH-LS0 (LS0 scores S0 on the linked-hub family LH,
exact-Gram realisation) and of the lattice progress events D_S used in its proof.

Family LH (W1-EXP PROOF section 4.1): G groups of size g, equicorrelation rho inside groups,
c linked pairs (a_i, b_i) with rank-one hub link psi, one visible group, the rest null.
Truth: theta_{j_a} = beta_i, theta_{j_b} = -psi*beta_i, theta_{j_h} = beta_h.
Exact Gram: X'X = (n-1) Sigma, columns centred.  Blocks = groups (W1-EXP Lemma 4.2; not re-run here).

Checks, per replicate:
  (1) pi0 mode S~0 (exact max-plus over blocks) and pi0(S°) (exact log-sum-exp convolution);
  (2) production local search from S~0 (<= ell moves, then one scan; strict improvement;
      lexicographic tie rule irrelevant a.s.), recording whether S0 is scored;
  (3) the events D_S at every S in Lat(S°) with m(S) >= 1 (best progress neighbour strictly beats S and
      every non-progress neighbour), and the minimal score margin;
  (4) whether S0 is the best model among everything scored (posterior side, pi(S0) > 1/2 not computed:
      p too large to enumerate).
Score: 00_COMMON section 1 (standardised X, y; nu = 0.01 + n/2; 2 b0 = 0.02; BB(1,p) capped at K).
Seed fixed.  Output: lh_ls0_check.txt
"""
import itertools, math, sys
import numpy as np
from scipy.special import gammaln, logsumexp

SEED = 20261102


def lh_sigma(G, g, rho, pairs):
    """pairs: list of (group_a, group_b, psi). Hubs are the first index of each group."""
    p = G * g
    S = np.zeros((p, p))
    for h in range(G):
        idx = slice(h * g, (h + 1) * g)
        S[idx, idx] = rho
    np.fill_diagonal(S, 1.0)
    for (ga, gb, psi) in pairs:
        A = range(ga * g, (ga + 1) * g)
        Bv = range(gb * g, (gb + 1) * g)
        ja, jb = ga * g, gb * g
        for k in A:
            for l in Bv:
                v = psi * S[k, ja] * S[jb, l]
                S[k, l] = S[l, k] = v
    return S


def logw(k, p):
    # w(k) = 1/2 / C(2p-1, k)
    return math.log(0.5) - (gammaln(2 * p) - gammaln(k + 1) - gammaln(2 * p - k))


class Scorer:
    def __init__(self, X, y):
        self.X, self.y = X, y
        self.n, self.p = X.shape
        self.K = min(self.p, self.n // 2)
        self.nu = 0.01 + self.n / 2.0
        self.G = X.T @ X
        self.z = X.T @ y
        self.yy = float(y @ y)
        self.cache = {}
        self.logW = logsumexp([math.lgamma(self.p + 1) - math.lgamma(k + 1) - math.lgamma(self.p - k + 1)
                               + logw(k, self.p) for k in range(self.K + 1)])

    def logm(self, S):
        """log m(S) up to an S-free constant."""
        n = self.n
        if len(S) == 0:
            return -self.nu * math.log(0.02 + self.yy)
        idx = list(S)
        GS = self.G[np.ix_(idx, idx)]
        H = (n + 1) * GS + np.eye(len(idx))
        zS = self.z[idx]
        Q = self.yy - n * float(zS @ np.linalg.solve(H, zS))
        logD = np.linalg.slogdet(H)[1] - np.linalg.slogdet(GS + np.eye(len(idx)))[1]
        return -0.5 * logD - self.nu * math.log(0.02 + Q)

    def F(self, S):
        S = tuple(sorted(S))
        if S not in self.cache:
            self.cache[S] = logw(len(S), self.p) + self.logm(S)
        return self.cache[S]

    def neighbours(self, S):
        S = set(S)
        out = []
        for j in range(self.p):
            if j in S:
                out.append(tuple(sorted(S - {j})))
            elif len(S) < self.K:
                out.append(tuple(sorted(S | {j})))
        for i in sorted(S):
            for j in range(self.p):
                if j not in S:
                    out.append(tuple(sorted((S - {i}) | {j})))
        return out


def local_search(sc, centre, ell):
    scored = set()
    C = tuple(sorted(centre))
    moves = 0
    while True:
        nb = sc.neighbours(C)
        scored.update(nb)
        best = max(nb, key=lambda T: (sc.F(T), [-t for t in T]))
        if sc.F(best) > sc.F(C) and moves < ell:
            C = best
            moves += 1
            continue
        return scored, C, moves


def block_tables(sc, blocks):
    tabs = []
    for blk in blocks:
        t = {}
        for r in range(len(blk) + 1):
            for U in itertools.combinations(blk, r):
                t[U] = sc.logm(U) - sc.logm(())  # log BF(U), tables on the full y
        tabs.append(t)
    return tabs


def pi0_mode_and_mass(sc, blocks, tabs, Sref):
    p, K = sc.p, sc.K
    # per block: best and logsumexp of log r_b by size
    best_by_size, lse_by_size, arg_by_size = [], [], []
    for blk, t in zip(blocks, tabs):
        bb, ll, aa = {}, {}, {}
        for U, v in t.items():
            k = len(U)
            if k not in bb or v > bb[k]:
                bb[k], aa[k] = v, U
            ll.setdefault(k, []).append(v)
        best_by_size.append(bb)
        lse_by_size.append({k: logsumexp(v) for k, v in ll.items()})
        arg_by_size.append(aa)
    # max-plus and log-sum-exp convolution over blocks (capped at K)
    NEG = -np.inf
    mx = np.full(K + 1, NEG); mx[0] = 0.0
    arg = [[] for _ in range(K + 1)]
    ls = np.full(K + 1, NEG); ls[0] = 0.0
    for b in range(len(blocks)):
        nmx = np.full(K + 1, NEG); narg = [None] * (K + 1)
        nls = np.full(K + 1, NEG)
        for k in range(K + 1):
            if mx[k] == NEG and ls[k] == NEG:
                continue
            for j, v in best_by_size[b].items():
                if k + j > K:
                    continue
                if mx[k] + v > nmx[k + j]:
                    nmx[k + j] = mx[k] + v
                    narg[k + j] = arg[k] + list(arg_by_size[b][j])
                nls[k + j] = np.logaddexp(nls[k + j], ls[k] + lse_by_size[b][j])
        mx, arg, ls = nmx, narg, nls
    scores = [mx[k] + logw(k, p) if mx[k] > NEG else NEG for k in range(K + 1)]
    kbest = int(np.argmax(scores))
    mode = tuple(sorted(arg[kbest]))
    logZ0 = logsumexp([ls[k] + logw(k, p) for k in range(K + 1) if ls[k] > NEG])
    def logg0(S):
        S = set(S)
        return logw(len(S), p) + sum(t[tuple(sorted(S & set(blk)))] for blk, t in zip(blocks, tabs))
    return mode, math.exp(logg0(Sref) - logZ0)


def lattice_D_check(sc, Sstar, S0):
    """D_S at every S with Sstar ⊆ S ⊊ S0; returns (all hold, min margin)."""
    M = sorted(set(S0) - set(Sstar))
    ok, minmarg = True, np.inf
    for r in range(len(M)):
        for Mp in itertools.combinations(M, r):
            S = tuple(sorted(set(Sstar) | set(Mp)))
            miss = set(S0) - set(S)
            nb = sc.neighbours(S)
            prog = [T for T in nb if len(set(S0) ^ set(T)) < len(set(S0) ^ set(S))]
            nonp = [T for T in nb if T not in prog] + [S]
            bp = max(sc.F(T) for T in prog)
            marg = bp - max(sc.F(T) for T in nonp)
            minmarg = min(minmarg, marg)
            ok &= marg > 0
    return ok, minmarg


def run(n, c, rep, rng, G=12, g=9, rho=0.7, psi=0.5):
    pairs = [(2 * i, 2 * i + 1, psi) for i in range(c)]
    vis = 2 * c
    Sig = lh_sigma(G, g, rho, pairs)
    p = G * g
    theta = np.zeros(p)
    betas = [1.4, -1.0, 1.2, 0.9][:c]
    for i, (ga, gb, ps) in enumerate(pairs):
        theta[ga * g] = betas[i]
        theta[gb * g] = -ps * betas[i]
    theta[vis * g] = 1.0
    S0 = tuple(sorted(np.flatnonzero(theta)))
    Sstar = tuple(sorted(set(S0) - {gb * g for (_, gb, _) in pairs}))
    # exact Gram centred design: X = sqrt(n-1) Qc L', Qc orthonormal, orthogonal to 1
    A = rng.standard_normal((n, p + 1)); A[:, 0] = 1.0
    Qfull, _ = np.linalg.qr(A)
    Qc = Qfull[:, 1:p + 1]
    L = np.linalg.cholesky(Sig)
    X = math.sqrt(n - 1) * Qc @ L.T
    eps = rng.standard_normal(n)
    yr = X @ theta + eps
    yc = yr - yr.mean()
    y = yc / math.sqrt(yc @ yc / (n - 1))
    sc = Scorer(X, y)
    blocks = [list(range(h * g, (h + 1) * g)) for h in range(G)]
    tabs = block_tables(sc, blocks)
    mode, pi0_ref = pi0_mode_and_mass(sc, blocks, tabs, Sstar)
    ell = math.ceil(math.log2(n + p + 1))
    scored, end, moves = local_search(sc, mode, ell)
    Dok, minmarg = lattice_D_check(sc, Sstar, S0)
    best_scored = max(scored, key=sc.F)
    return dict(n=n, c=c, rep=rep, mode_is_Sstar=(mode == Sstar), pi0_Sstar=pi0_ref,
                ls0_scores_S0=(S0 in scored), moves=moves, end_is_S0=(end == S0),
                D_lattice=Dok, min_margin=minmarg, S0_best_scored=(best_scored == S0))


def main():
    rng = np.random.default_rng(SEED)
    out = []
    for c in (1, 2, 3):
        for n in (200, 800, 3200):
            reps = 10
            rows = [run(n, c, r, rng) for r in range(reps)]
            line = (f"c={c} n={n:5d} reps={reps}: mode=S° {sum(r['mode_is_Sstar'] for r in rows)}/{reps}; "
                    f"median pi0(S°)={np.median([r['pi0_Sstar'] for r in rows]):.4f}; "
                    f"LS0 scores S0 {sum(r['ls0_scores_S0'] for r in rows)}/{reps}; "
                    f"moves {sorted(set(r['moves'] for r in rows))}; "
                    f"D_S on Lat(S°) {sum(r['D_lattice'] for r in rows)}/{reps}; "
                    f"min margin (nats) {min(r['min_margin'] for r in rows):.1f}; "
                    f"S0 best of scored {sum(r['S0_best_scored'] for r in rows)}/{reps}")
            print(line, flush=True)
            out.append(line)
    with open(__file__.replace('.py', '.txt'), 'w') as f:
        f.write("W4-T38FULL lh_ls0_check.py, seed %d, G=12, g=9, rho=0.7, psi=0.5, visible beta=1.0\n" % SEED)
        f.write("\n".join(out) + "\n")


if __name__ == '__main__':
    main()
