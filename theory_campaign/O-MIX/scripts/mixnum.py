"""O-MIX numerics: exact small-p comparison of three start fixes for masked-regime discovery.

  base  : v3 start (v3 partition, tables r_b(U) = BF(U), sigma^2 integrated per block)
  (B)   : mixture start 1/2 pi0[base] + 1/2 pi0[P+], P+ = v3 partition with every *linked* block pair merged
          (linked: max cross-block |r_jl| > tau_n = 3 sqrt(log p / n); merge only if merged size <= 16)
  (C)   : common plug-in sigma^2 tables r^C_b(U) = D_U^{-1/2} exp(t_U / (2 s2)), on the v3 partition, for
          s2 in {oracle  = (2b0+Q_S0)/(2nu),  fixpoint = iterate s2 <- (2b0+Q_{mode})/(2nu) from the v3 start mode,
                 null    = (2b0+Q_empty)/(2nu)}
  (C-grid): uniform mixture of (C) over the log-grid s2_k = (2b0+Q_empty)/(2nu) * exp(-k*eta/sqrt(nu)), k = 0..m-1,
          covering down to (2b0 + y'y/(n+1))/(2nu); eta = 1.
Exact pi0 masses via block size-profile convolution (exact normaliser); start modes via max-plus convolution;
exact posterior pi by full enumeration.  Also checks Theorem C1's deterministic bound on the BO family.
Sufficient statistics only (exact-Gram realisation X'X = (n-1) Sigma).  Seeds fixed below.
Usage: python mixnum.py > ../results/mixnum.txt
"""
import itertools
import math
import sys

import numpy as np

sys.path.insert(0, ".")
from w1exp_bvs_exact import log_m, log_m_batch, log_w, make_blocks, block_size_B, A0, B0  # noqa: E402
from w1exp_family import lh_sigma, lh_truth, suff_exact_gram  # noqa: E402


def Qt(S, R, r, n):
    """(Q_S, t_S, log D_S) on standardised data."""
    S = list(S)
    if not S:
        return n - 1.0, 0.0, 0.0
    RS = R[np.ix_(S, S)]
    k = len(S)
    H = (n + 1.0) * (n - 1.0) * RS + np.eye(k)
    G1 = (n - 1.0) * RS + np.eye(k)
    z = (n - 1.0) * r[S]
    t = n * z @ np.linalg.solve(H, z)
    return (n - 1.0) - t, t, np.linalg.slogdet(H)[1] - np.linalg.slogdet(G1)[1]


def tables_v3(blocks, R, r, n):
    l0 = log_m([], R, r, n)
    return [{frozenset(U): log_m(U, R, r, n) - l0 for k in range(len(C) + 1) for U in itertools.combinations(C, k)}
            for C in blocks]


def tables_C(blocks, R, r, n, s2):
    out = []
    for C in blocks:
        t = {}
        for k in range(len(C) + 1):
            for U in itertools.combinations(C, k):
                _, tt, lD = Qt(U, R, r, n)
                t[frozenset(U)] = -0.5 * lD + tt / (2 * s2)
        out.append(t)
    return out


def profiles(blocks, tabs):
    prof = []
    for C, t in zip(blocks, tabs):
        e = np.full(len(C) + 1, -np.inf)
        best = [None] * (len(C) + 1)
        bv = np.full(len(C) + 1, -np.inf)
        for U, v in t.items():
            e[len(U)] = np.logaddexp(e[len(U)], v)
            if v > bv[len(U)]:
                bv[len(U)], best[len(U)] = v, U
        prof.append((e, bv, best))
    return prof


def logZ0(blocks, tabs, p, K):
    conv = np.array([0.0])
    for e, _, _ in profiles(blocks, tabs):
        new = np.full(min(len(conv) + len(e) - 1, K + 1), -np.inf)
        for i, a in enumerate(conv):
            for j, b in enumerate(e):
                if i + j <= K:
                    new[i + j] = np.logaddexp(new[i + j], a + b)
        conv = new
    return np.logaddexp.reduce(np.array([log_w(k, p) + conv[k] for k in range(len(conv))]))


def start_mode(blocks, tabs, p, K):
    """argmax pi0 by max-plus convolution (ties: first found)."""
    conv, arg = np.array([0.0]), [frozenset()]
    for e, bv, best in profiles(blocks, tabs):
        L = min(len(conv) + len(bv) - 1, K + 1)
        new, narg = np.full(L, -np.inf), [None] * L
        for i, a in enumerate(conv):
            for j, b in enumerate(bv):
                if i + j < L and a + b > new[i + j]:
                    new[i + j], narg[i + j] = a + b, arg[i] | best[j]
        conv, arg = new, narg
    vals = [log_w(k, p) + conv[k] for k in range(len(conv))]
    return arg[int(np.argmax(vals))]


def log_pi0(S, blocks, tabs, p, lz):
    S = frozenset(S)
    return log_w(len(S), p) + sum(t[S & frozenset(C)] for C, t in zip(blocks, tabs)) - lz


class Start:
    def __init__(self, blocks, tabs, p, K):
        self.blocks, self.tabs, self.p = blocks, tabs, p
        self.lz = logZ0(blocks, tabs, p, K)
        self.mode = start_mode(blocks, tabs, p, K)

    def lp(self, S):
        return log_pi0(S, self.blocks, self.tabs, self.p, self.lz)


def linked_merge(blocks, R, n, p, cap=16):
    tau = 3 * math.sqrt(math.log(p) / n)
    J = len(blocks)
    parent = list(range(J))

    def f(a):
        while parent[a] != a:
            a = parent[a]
        return a
    for a in range(J):
        for b in range(a + 1, J):
            if np.abs(R[np.ix_(blocks[a], blocks[b])]).max() > tau:
                ra, rb = f(a), f(b)
                if ra != rb:
                    parent[rb] = ra
    comp = {}
    for a in range(J):
        comp.setdefault(f(a), []).append(a)
    out = []
    for members in comp.values():
        merged = sorted(j for a in members for j in blocks[a])
        if len(merged) <= cap:
            out.append(merged)
        else:
            out.extend(blocks[a] for a in members)
    return sorted(out), sum(len(m) > 1 for m in comp.values())


def log_post_S0(R, r, n, S0):
    p = R.shape[0]
    K = min(p, n // 2)
    vals = []
    for k in range(K + 1):
        combs = np.array(list(itertools.combinations(range(p), k)), dtype=int) if k else np.zeros((1, 0), int)
        vals.append(log_m_batch(combs, R, r, n) + log_w(k, p))
    lz = np.logaddexp.reduce(np.concatenate(vals))
    return log_m(S0, R, r, n) + log_w(len(S0), p) - lz


CONFIGS = {
    "LH-A(c=1,p=16)": dict(G=4, g=4, rho=0.7, links=[(0, 1, 0.5)], visible={0: 1.4, 2: 1.8}),
    "LH-B(c=2,p=20)": dict(G=5, g=4, rho=0.7, links=[(0, 1, 0.5), (2, 3, 0.5)], visible={0: 1.4, 2: 1.8}),
    # BO dilution family: no links, three visible truths of moderate size (weak at small n)
    "BO-D(p=16)": dict(G=4, g=4, rho=0.7, links=[], visible={0: 1.5, 1: 1.5, 2: 0.32}),
}
NS = [200, 800, 3200]
REPS = {"LH-A(c=1,p=16)": 12, "LH-B(c=2,p=20)": 6, "BO-D(p=16)": 12}
SIGMA = 1.0


def main(only=None):
    print(__doc__.split("Usage")[0])
    for ci, (name, cfg) in enumerate(CONFIGS.items()):
        if only is not None and ci != only:
            continue
        G, g = cfg["G"], cfg["g"]
        p = G * g
        Sig, groups = lh_sigma(G, g, cfg["rho"], 0, cfg["links"])
        th, S0, M, Sref = lh_truth(G, g, 0, cfg["links"], cfg["visible"])
        S0f = frozenset(S0)
        print(f"\n=== {name}: S0={S0}, masked M={M}, S°={Sref}")
        print("n | med log10 pi0: base, P+, mix(B), C-oracle, C-fix, C-null, C-grid | med pi(S0) | "
              "share(mode_base=S°) | share(mode_C-fix ⊇ S0) | C1 bound held | m_grid | linked pairs found")
        for ni, n in enumerate(NS):
            rng = np.random.default_rng(20261102 + 100 * ci + ni)
            K = min(p, n // 2)
            nu = A0 + n / 2.0
            B = block_size_B(n, p)
            rows = []
            for rep in range(REPS[name]):
                R, r = suff_exact_gram(Sig, th, n, SIGMA, rng)
                bl = make_blocks(R, B)
                base = Start(bl, tables_v3(bl, R, r, n), p, K)
                blp, nlink = linked_merge(bl, R, n, p)
                plus = Start(blp, tables_v3(blp, R, r, n), p, K)
                lmix = np.logaddexp(base.lp(S0f), plus.lp(S0f)) - math.log(2)
                Q0 = Qt(S0, R, r, n)[0]
                s2_or = (2 * B0 + Q0) / (2 * nu)
                s2_null = (2 * B0 + n - 1.0) / (2 * nu)
                # fixpoint plug-in
                mode = base.mode
                for _ in range(10):
                    s2 = (2 * B0 + Qt(mode, R, r, n)[0]) / (2 * nu)
                    Cst = Start(bl, tables_C(bl, R, r, n, s2), p, K)
                    if Cst.mode == mode:
                        break
                    mode = Cst.mode
                C_fix = Cst
                C_or = Start(bl, tables_C(bl, R, r, n, s2_or), p, K)
                C_null = Start(bl, tables_C(bl, R, r, n, s2_null), p, K)
                # grid
                lo = (2 * B0 + (n - 1.0) / (n + 1)) / (2 * nu)
                m = int(math.ceil(math.log(s2_null / lo) * math.sqrt(nu))) + 1
                lg = [float('nan')] if m > 200 else []
                for k in (range(m) if m <= 200 else []):
                    s2k = s2_null * math.exp(-k / math.sqrt(nu))
                    lg.append(Start(bl, tables_C(bl, R, r, n, s2k), p, K).lp(S0f))
                lgrid = np.logaddexp.reduce(np.array(lg)) - math.log(m)
                lpost = log_post_S0(R, r, n, S0)
                # Theorem C1 bound (meaningful under BO): log pi0^C(S0) >= log pi(S0) - nu*psi(u)
                u = (2 * B0 + Q0) / (2 * nu * s2)
                c1 = C_fix.lp(S0f) >= lpost - nu * (u - 1 - math.log(u)) - 1e-9
                rows.append([base.lp(S0f), plus.lp(S0f), lmix, C_or.lp(S0f), C_fix.lp(S0f), C_null.lp(S0f), lgrid,
                             lpost, base.mode == frozenset(Sref), S0f <= C_fix.mode, c1, m, nlink])
            A = np.array(rows, dtype=float)
            med = np.median(A[:, :7], axis=0) / math.log(10)
            print(f"{n} | " + ", ".join(f"{x:.2f}" for x in med) + f" | {np.median(np.exp(A[:, 7])):.3f} | "
                  f"{A[:, 8].mean():.2f} | {A[:, 9].mean():.2f} | {A[:, 10].mean():.2f} | {int(A[0, 11])} | "
                  f"{A[:, 12].mean():.1f}")
            sys.stdout.flush()


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else None)
