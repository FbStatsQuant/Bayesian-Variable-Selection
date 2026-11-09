"""C-DLV numerics N1: exact Psi_n, Lambda_V and oracle-V grid construction on LH-type designs (blocks = groups).

Psi_n = sum_{S != S0} (e^{a} + e^{2b-a}) delta^2, a = log g0(S)/g0(S0), b = log g1(S)/g1(S0), delta = b - a,
over all models of size <= KMAX (truncation reported via per-size contributions).
Oracle V = {empty} U top-20p by log g0 U top-20p by log g1 over the enumerated space (V's of the method are subsets
of scored models; this is the 'all models scored' proxy). Grid: exact port of cpp/v3_calib.h build_grid with the
targets given (pilot schedule unknown here: targets {1} = one-jump pilot, and a uniform 10-step pilot).
Usage: python psi_enum.py <design M|F> <seeds> <n1,n2,...>
"""
import sys, os, math, itertools, json
import numpy as np
from scipy.special import logsumexp
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "Wave1", "W1-GEN", "numerics")))
import bvs_core as bc

KMAX = 5
C0 = math.log(10 / 9)


def lse(x):
    m = np.max(x)
    return m + math.log(np.sum(np.exp(x - m)))


def F_V(lg0, d, t):
    return lse(lg0 + t * d)


def rho_V(lg0, d, u, v):
    return math.exp(2 * F_V(lg0, d, v) - F_V(lg0, d, u) - F_V(lg0, d, 2 * v - u))


def build_grid(lg0, d, targets, Te):
    targets = sorted(targets)
    grid = [0.0]; u = 0.0
    while u < 1.0:
        b = next((t for t in targets if t > u), None)
        if b is None:
            return grid, "no_target_above_u"
        if rho_V(lg0, d, u, b) >= 0.90:
            v = b
        else:
            lo, hi, anyp = u, b, False
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if rho_V(lg0, d, u, mid) >= 0.90:
                    lo, anyp = mid, True
                else:
                    hi = mid
            if not anyp:
                return grid, "non_progress"
            v = lo
        if v >= 1.0 - 1e-12:
            v = 1.0
        if not v > u:
            return grid, "non_progress"
        if not rho_V(lg0, d, u, v) >= 0.90:
            return grid, "validation_failed"
        grid.append(v)
        if len(grid) - 1 > Te:
            return grid, "too_many_intervals"
        u = v
    return grid, "ok"


def lam(lg0, d, ts):
    best = 0.0
    for t in ts:
        x = lg0 + t * d
        w = np.exp(x - x.max()); w /= w.sum()
        m = (w * d).sum(); v = (w * (d - m) ** 2).sum()
        best = max(best, v)
    return best


def one(design, n, seed):
    rng = np.random.default_rng(10_000 * seed + n)
    g = 9
    G = 3
    Sigma, info = bc.lh_sigma(G, g, 0.4, [0.2], nvis=1)
    p = G * g
    if design == "M":
        theta = bc.lh_theta(p, info, [0.2], [1.0], 0.0)  # a_hub 1, b_hub -0.2 ; vis hub 0
    else:
        theta = np.zeros(p); theta[info["a_hubs"][0]] = 1.0; theta[info["vis_hubs"][0]] = 0.7
    S0 = tuple(sorted(int(j) for j in np.flatnonzero(theta)))
    X = bc.exact_gram_design(Sigma, n, rng)
    y = bc.make_y_std(X, theta, 1.0, rng)
    prob = bc.Problem(X, y)
    blocks = [list(gr) for gr in info["groups"]]
    bid = bc.block_id_array(blocks, p)
    models = [()]
    for k in range(1, KMAX + 1):
        models += list(itertools.combinations(range(p), k))
    F = prob.F_many(models)
    # log gamma0: prior + sum of block log r (block tables via cache)
    lg0 = np.empty(len(models))
    for i, S in enumerate(models):
        lg0[i] = bc.log_gamma0(prob, blocks, S, bid)
    lg1 = F - prob.logm0  # log varpi + log BF
    d = lg1 - lg0
    i0 = models.index(S0)
    a = lg0 - lg0[i0]; b = lg1 - lg1[i0]; de = b - a
    mask = np.ones(len(models), bool); mask[i0] = False
    sizes = np.array([len(S) for S in models])
    term = (np.exp(np.minimum(a, 700)) + np.exp(np.minimum(2 * b - a, 700))) * de ** 2
    psi = float(term[mask].sum())
    psi_by_k = {int(k): float(term[mask & (sizes == k)].sum()) for k in range(KMAX + 1)}
    top_terms = sorted([(float(term[i]), models[i]) for i in np.flatnonzero(mask)], reverse=True)[:3]
    # oracle V
    o0 = np.argsort(-lg0, kind="stable")[:20 * p]; o1 = np.argsort(-lg1, kind="stable")[:20 * p]
    Vi = sorted(set(o0.tolist()) | set(o1.tolist()) | {0})
    Vi = sorted(Vi, key=lambda i: models[i])
    lV0, dV = lg0[Vi], d[Vi]
    ts = np.linspace(0, 2, 2001)
    LV = lam(lV0, dV, ts)
    ell = math.ceil(math.log2(n + p + 1)); Te = max(1000, ell ** 2)
    g1, r1 = build_grid(lV0, dV, [1.0], Te)
    g10, r10 = build_grid(lV0, dV, [k / 10 for k in range(1, 11)], Te)
    start_mode = models[int(np.argmax(lg0))]; post_mode = models[int(np.argmax(lg1))]
    pi0_S0 = float(math.exp(lg0[i0] - lse(lg0)))
    return dict(design=design, n=n, seed=seed, p=p, S0=list(S0), start_mode=list(start_mode), post_mode=list(post_mode),
                pi0_S0=pi0_S0, psi=psi, psi_by_k=psi_by_k, psi_lt_c0=bool(psi < C0),
                top_terms=[(t, list(S)) for t, S in top_terms], V_size=len(Vi), S0_in_oracleV=bool(i0 in Vi),
                Lambda_V=LV, Lambda_lt_c0=bool(LV < C0), grid1_intervals=len(g1) - 1, grid1_reason=r1,
                grid10_intervals=len(g10) - 1, grid10_reason=r10, Te=Te,
                delta_S0_vs_startmode=float(d[i0] - d[models.index(start_mode)]))


if __name__ == "__main__":
    design = sys.argv[1]; seeds = int(sys.argv[2]); ns = [int(x) for x in sys.argv[3].split(",")]
    out = []
    for n in ns:
        for s in range(1, seeds + 1):
            r = one(design, n, s)
            out.append(r)
            print(json.dumps({k: r[k] for k in ("design", "n", "seed", "start_mode", "post_mode", "pi0_S0", "psi",
                                                  "Lambda_V", "grid1_intervals", "grid10_intervals", "grid1_reason",
                                                  "delta_S0_vs_startmode")}), flush=True)
    with open(os.path.join(HERE, f"N1_psi_{design}.json"), "w") as f:
        json.dump(out, f, indent=1)
