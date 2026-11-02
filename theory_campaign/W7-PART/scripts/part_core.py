"""W7-PART core: a port of the v3 partition (Scripts/SMC_BVS/core/cpp/v3_blocks.h, M §6.3) and the designs.

Two implementations of the partition:
  * v3_blocks_faithful(X, B): line-by-line port of complete_linkage + make_blocks, including the R13 tie rule
    (lexicographic order of the sorted union) and the left-child = smaller-minimum-index convention.
  * v3_blocks_fast(X, B): scipy complete linkage (same merge sequence whenever no two candidate merges tie, which
    has probability 0 for continuous data; a tie is detected and the faithful port is used instead), then the
    identical cut and next-fit packing.
The partition reads only the Gram matrix of the standardised columns of X: no y enters (M §6.3, v3_blocks.h).
"""
import math
import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform


def isqrt(x):
    return math.isqrt(int(x))


def block_size(n, p):
    """M §3 / v3_preprocess.R: B = min(isqrt(n), isqrt(p), 16)."""
    return min(isqrt(n), isqrt(p), 16)


def correlation(X):
    """Engine's correlation: standardise (divide by max |.|, centre, divide by sd with n-1), Gram, r = G/sqrt(GjjGll)."""
    X = np.asarray(X, float)
    Xs = X / np.abs(X).max(axis=0)
    Xs = Xs - Xs.mean(axis=0)
    Xs = Xs / Xs.std(axis=0, ddof=1)
    G = Xs.T @ Xs
    s = np.sqrt(np.diag(G))
    return G / np.outer(s, s)


# ----------------------------------------------------------------------------------------------- faithful port
def _union_lex_less(a, b, c, d):
    u = sorted(a + b)
    v = sorted(c + d)
    return u < v  # Python list order = lexicographic with proper prefix first


def complete_linkage_faithful(r):
    p = r.shape[0]
    left = [-1] * (2 * p - 1); right = [-1] * (2 * p - 1)
    size = [1] * (2 * p - 1); minidx = list(range(p)) + [0] * (p - 1)
    height = [0.0] * (2 * p - 1)
    if p == 1:
        return dict(left=left, right=right, size=size, minidx=minidx, height=height, root=0)
    dist = 1.0 - np.abs(r)
    D = dist.copy()
    np.fill_diagonal(D, np.inf)
    mem = [[j] for j in range(p)]
    node = list(range(p))
    active = np.ones(p, bool)
    nxt = p
    for step in range(p - 1):
        m = D.min()
        ii, jj = np.nonzero(D == m)
        cand = [(i, j) for i, j in zip(ii, jj) if i < j]
        if len(cand) == 1:
            a, b = cand[0]
        else:  # R13 tie rule: smallest sorted union, lexicographically
            a, b = cand[0]
            for (i, j) in cand[1:]:
                if _union_lex_less(mem[i], mem[j], mem[a], mem[b]):
                    a, b = i, j
        h = D[a, b]
        na, nb = node[a], node[b]
        L, R = (na, nb) if minidx[na] < minidx[nb] else (nb, na)
        nn = nxt; nxt += 1
        left[nn], right[nn] = L, R
        size[nn] = size[na] + size[nb]
        minidx[nn] = min(minidx[na], minidx[nb]); height[nn] = h
        mem[a] = sorted(mem[a] + mem[b]); mem[b] = []
        active[b] = False; node[a] = nn
        v = np.maximum(D[:, a], D[:, b])
        v[~active] = np.inf; v[a] = np.inf
        D[:, a] = v; D[a, :] = v
        D[b, :] = np.inf; D[:, b] = np.inf
    return dict(left=left, right=right, size=size, minidx=minidx, height=height, root=nxt - 1)


def _subtree_leaves(T, nd, p):
    out, st = [], [nd]
    while st:
        x = st.pop()
        if x < p:
            out.append(x); continue
        st.append(T["right"][x]); st.append(T["left"][x])
    return out


def cut_and_pack(T, p, B):
    clusters, st = [], [T["root"]]
    while st:
        x = st.pop()
        if T["size"][x] <= B:
            clusters.append(_subtree_leaves(T, x, p)); continue
        st.append(T["right"][x]); st.append(T["left"][x])
    blocks, cur = [], []
    for c in clusters:
        if len(cur) + len(c) > B:
            blocks.append(cur); cur = []
        cur = cur + c
    if cur:
        blocks.append(cur)
    return [sorted(b) for b in blocks], [sorted(c) for c in clusters]


def v3_blocks_faithful(X, B, r=None):
    r = correlation(X) if r is None else r
    T = complete_linkage_faithful(r)
    return cut_and_pack(T, r.shape[0], B)


# ----------------------------------------------------------------------------------------------- fast version
def tree_from_scipy(Z, p):
    left = [-1] * (2 * p - 1); right = [-1] * (2 * p - 1)
    size = [1] * (2 * p - 1); minidx = list(range(p)) + [0] * (p - 1)
    height = [0.0] * (2 * p - 1)
    for s in range(p - 1):
        a, b = int(Z[s, 0]), int(Z[s, 1])
        nn = p + s
        L, R = (a, b) if minidx[a] < minidx[b] else (b, a)
        left[nn], right[nn] = L, R
        size[nn] = size[a] + size[b]; minidx[nn] = min(minidx[a], minidx[b]); height[nn] = Z[s, 2]
    return dict(left=left, right=right, size=size, minidx=minidx, height=height, root=2 * p - 2)


def v3_blocks_fast(X, B, r=None):
    r = correlation(X) if r is None else r
    p = r.shape[0]
    d = 1.0 - np.abs(r)
    np.fill_diagonal(d, 0.0)
    d = np.maximum(d, 0.0)
    dv = squareform(d, checks=False)
    Z = linkage(dv, method="complete")
    h = Z[:, 2]
    if np.any(np.diff(np.sort(h)) == 0):  # possible tie: use the faithful port
        return v3_blocks_faithful(X, B, r)
    return cut_and_pack(tree_from_scipy(Z, p), p, B)


# ----------------------------------------------------------------------------------------------- margins
def margins(r, groups):
    """Per-group local margin: min within-h |r| minus max_{j in h, k not in h} |r|. Global margin likewise."""
    p = r.shape[0]
    A = np.abs(r).copy()
    np.fill_diagonal(A, np.nan)
    lab = np.empty(p, int)
    for h, C in enumerate(groups):
        lab[C] = h
    loc = []
    win_all, cr_all = np.inf, -np.inf
    for h, C in enumerate(groups):
        sub = A[np.ix_(C, C)]
        w = np.nanmin(sub)
        mask = lab != h
        c = A[np.ix_(C, np.flatnonzero(mask))].max()
        loc.append(w - c)
        win_all = min(win_all, w); cr_all = max(cr_all, c)
    return float(min(loc)), float(win_all - cr_all)


# ----------------------------------------------------------------------------------------------- designs
def gen_groups(n, G, g, rho, psi=0.0, kind="indep", rng=None, sizes=None):
    """Rows iid N(0, Sigma). Groups of size g (or `sizes`), within-group correlation rho.
    kind = 'indep'  : groups independent (cross correlation 0);
           'global' : one common factor, cross correlation psi for every cross pair (S5-like), needs 0 <= psi <= rho;
           'lh'     : W3-PXN linked hubs: groups paired (0,1),(2,3),..; corr(hub_a, hub_b) = psi, cross correlations
                      psi (hub-hub), rho*psi (hub-member), rho^2*psi (member-member), 0 elsewhere. Needs G even.
    """
    sizes = [g] * G if sizes is None else list(sizes)
    p = sum(sizes)
    starts = np.cumsum([0] + sizes)
    groups = [list(range(starts[h], starts[h + 1])) for h in range(len(sizes))]
    X = np.empty((n, p))
    if kind in ("indep", "global"):
        f0 = rng.standard_normal(n) if kind == "global" else np.zeros(n)
        c0 = math.sqrt(psi) if kind == "global" else 0.0
        cg = math.sqrt(rho - (psi if kind == "global" else 0.0))
        for h, C in enumerate(groups):
            fh = rng.standard_normal(n)
            X[:, C] = (c0 * f0 + cg * fh)[:, None] + math.sqrt(1 - rho) * rng.standard_normal((n, len(C)))
    elif kind == "lh":
        assert len(groups) % 2 == 0
        for h in range(0, len(groups), 2):
            Ca, Cb = groups[h], groups[h + 1]
            f = rng.standard_normal(n)
            X[:, Ca] = math.sqrt(rho) * f[:, None] + math.sqrt(1 - rho) * rng.standard_normal((n, len(Ca)))
            hub = psi * X[:, Ca[0]] + math.sqrt(1 - psi ** 2) * rng.standard_normal(n)
            X[:, Cb[0]] = hub
            f2 = rng.standard_normal(n)
            X[:, Cb[1:]] = (rho * hub[:, None] + math.sqrt(rho * (1 - rho)) * f2[:, None]
                            + math.sqrt(1 - rho) * rng.standard_normal((n, len(Cb) - 1)))
    else:
        raise ValueError(kind)
    return X, groups


def population_sigma(G, g, rho, psi=0.0, kind="indep", sizes=None):
    sizes = [g] * G if sizes is None else list(sizes)
    p = sum(sizes)
    starts = np.cumsum([0] + sizes)
    lab = np.repeat(np.arange(len(sizes)), sizes)
    S = np.where(lab[:, None] == lab[None, :], rho, 0.0)
    if kind == "global":
        S = np.where(lab[:, None] == lab[None, :], rho, psi)
    if kind == "lh":
        for h in range(0, len(sizes), 2):
            Ca = np.arange(starts[h], starts[h + 1]); Cb = np.arange(starts[h + 1], starts[h + 2])
            ha, hb = Ca[0], Cb[0]
            for j in Ca:
                for k in Cb:
                    v = psi * (1 if j == ha else rho) * (1 if k == hb else rho)
                    S[j, k] = S[k, j] = v
    np.fill_diagonal(S, 1.0)
    return S


def blocks_equal_groups(blocks, groups):
    return sorted(map(tuple, blocks)) == sorted(map(tuple, groups))


def blocks_are_group_unions(blocks, groups):
    lab = {}
    for h, C in enumerate(groups):
        for j in C:
            lab[j] = h
    for b in blocks:
        hs = {lab[j] for j in b}
        if sum(len(groups[h]) for h in hs) != len(b):
            return False
    return True


# ----------------------------------------------------------------------------------------------- the real engine
import os, subprocess, tempfile
ENGINE_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine_blocks.cpp")
ENGINE_BIN = os.environ.get("W7_ENGINE_BIN", os.path.join(tempfile.gettempdir(), "w7part_engine_blocks"))


def build_engine():
    if not os.path.exists(ENGINE_BIN):
        subprocess.check_call(["g++", "-O2", "-std=c++17", "-o", ENGINE_BIN, ENGINE_SRC])
    return ENGINE_BIN


def v3_blocks_engine(X, B):
    """Run the unmodified engine make_blocks (v3_blocks.h) on the Gram matrix of the standardised columns."""
    build_engine()
    X = np.asarray(X, float)
    Xs = X / np.abs(X).max(axis=0)
    Xs = Xs - Xs.mean(axis=0)
    Xs = Xs / Xs.std(axis=0, ddof=1)
    G = np.asfortranarray(Xs.T @ Xs)
    p = G.shape[0]
    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as f:
        f.write(np.array([p, B], dtype=np.int32).tobytes())
        f.write(G.T.astype(np.float64).tobytes())  # column-major: G is symmetric anyway
        fn = f.name
    out = subprocess.check_output([ENGINE_BIN, fn]).decode()
    os.unlink(fn)
    return [sorted(map(int, line.split())) for line in out.strip().splitlines()]
