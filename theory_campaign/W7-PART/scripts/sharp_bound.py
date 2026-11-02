"""Theorem C (PROOF.md §4): sharp finite-n bound for INDEPENDENT groups, evaluated by Monte Carlo over pairs of
group Gram matrices (each g x g), with the exact null law H0 for the cross terms:
   P(dendrogram not laminar) <= sum_{ordered independent (h,h')} E[ S_L(h,h') + S_N(h,h') ],
   S_L = sum_{A in T_h} sum_{k in h'} Phi_A(max(sigma(A), f_k)),
   S_N = sum_{A, A' non-leaf, not both roots} Phi_A(max(sigma(A), sigma(A'))),
   Phi_A(s) = min{ H0(s), sum_{eps in {+-1}^A, eps_1 = +1} H0(|A| s / ||U_A eps||) },
   H0(s) = P(|null sample correlation| >= s) = I_{1-s^2}((n-2)/2, 1/2).
The bound is rigorous; its numerical value is a Monte Carlo average (standard error reported).
For LH (c linked pairs) the linked pairs are dependent: their contribution P((C*) fails inside the pair) is
estimated by direct Monte Carlo of the 2g columns (an estimate, not a bound).
Usage: python3 sharp_bound.py  -> results/sharp_bound.txt"""
import itertools, math, sys, time
import numpy as np
from scipy.special import betainc
from part_core import correlation, group_tree, gen_groups, cstar_violations


def H0(s, n):
    s = np.asarray(s, float)
    out = np.zeros_like(s)
    m = s < 1
    out[m] = betainc((n - 2) / 2, 0.5, np.clip(1 - s[m] ** 2, 0, 1))
    out[s <= 0] = 1.0
    return out


_signs = {}


def signs(a):
    if a not in _signs:
        _signs[a] = np.array([(1,) + e for e in itertools.product((1, -1), repeat=a - 1)], float)
    return _signs[a]


def tree_info(r):
    """nodes: list of (members, sigma, is_leaf, is_root, norms)."""
    nodes = group_tree(r)
    info = []
    for (mem, h, ph) in nodes:
        a = len(mem)
        sig = -np.inf if np.isinf(ph) else 1.0 - ph
        if a == 1:
            norms = np.array([1.0])
        else:
            E = signs(a)
            R = r[np.ix_(mem, mem)]
            norms = np.sqrt(np.maximum(np.einsum("ij,jk,ik->i", E, R, E), 1e-300))
        info.append((mem, sig, a == 1, np.isinf(ph), norms))
    return info


def Phi(node, s, n):
    """vector over s (array)"""
    mem, sig, leaf, root, norms = node
    s = np.atleast_1d(s)
    single = H0(s, n)
    if leaf:
        return single
    a = len(mem)
    su = H0(a * s[:, None] / norms[None, :], n).sum(axis=1)
    return np.minimum(single, su)


def draw_group(n, g, rho, rng):
    f = rng.standard_normal(n)
    X = math.sqrt(rho) * f[:, None] + math.sqrt(1 - rho) * rng.standard_normal((n, g))
    return correlation(X)


def S_terms(Ti, Tj, n):
    fk = np.array([nd[1] for nd in Tj if nd[2]])  # leaves of h'
    SL = 0.0; SLL = 0.0
    for nd in Ti:
        s = np.maximum(nd[1], fk)
        v = Phi(nd, s, n).sum()
        SL += v
        if nd[2]:
            SLL += v
    SN = 0.0
    nonleaf_j = [nd for nd in Tj if not nd[2]]
    for nd in Ti:
        if nd[2]:
            continue
        sig_j = np.array([m[1] for m in nonleaf_j]); root_j = np.array([m[3] for m in nonleaf_j])
        keep = ~(root_j & nd[3])
        s = np.maximum(nd[1], sig_j[keep])
        SN += Phi(nd, s, n).sum()
    return SL, SN, SLL


def sharp(n, g, rho, reps, seed):
    rng = np.random.default_rng(seed)
    vals = []; ll = []
    for _ in range(reps):
        r1 = draw_group(n, g, rho, rng); r2 = draw_group(n, g, rho, rng)
        T1, T2 = tree_info(r1), tree_info(r2)
        a = S_terms(T1, T2, n); b = S_terms(T2, T1, n)
        vals.append(0.5 * (a[0] + a[1] + b[0] + b[1])); ll.append(0.5 * (a[2] + b[2]))
    vals = np.array(vals); ll = np.array(ll)
    return vals.mean(), vals.std(ddof=1) / math.sqrt(reps), ll.mean()


def linked_pair_mc(n, g, rho, psi, reps, seed):
    """Direct MC of P((C*) fails between the two groups of one LH linked pair)."""
    rng = np.random.default_rng(seed)
    bad = 0
    for _ in range(reps):
        X, groups = gen_groups(n, 2, g, rho, psi, "lh", rng, nlink=1)
        r = correlation(X)
        bad += cstar_violations(r, groups) > 0
    return bad / reps, bad


def draws(n, g, rho, reps, seed):
    """per draw: S for the two ordered pairs (h,h'), (h',h), leaf-leaf parts, and mu = min(m_h, m_h')."""
    rng = np.random.default_rng(seed)
    S = np.empty((reps, 2)); LL = np.empty((reps, 2)); MU = np.empty(reps)
    for i in range(reps):
        r1 = draw_group(n, g, rho, rng); r2 = draw_group(n, g, rho, rng)
        T1, T2 = tree_info(r1), tree_info(r2)
        a = S_terms(T1, T2, n); b = S_terms(T2, T1, n)
        S[i] = (a[0] + a[1], b[0] + b[1]); LL[i] = (a[2], b[2])
        iu = np.triu_indices(g, 1)
        MU[i] = min(np.abs(r1[iu]).min(), np.abs(r2[iu]).min())
    return S, LL, MU


def rigorous_C(n, g, rho, S, alpha=0.05, tau0_grid=None, step=0.0025):
    """Upper bound on E[S] (one ordered pair) valid with MC-confidence 1 - alpha:
       E[S] <= mean_N(min(S, cap(tau0))) + cap(tau0) sqrt(log(K0/alpha)/(2N))      (Hoeffding, Bonferroni over K0 tau0's)
              + sum_i cap(tau_{i+1}) * min(1, 2 C(g,2) P_rho(|r_hat| < tau_i))        (exact peeling, tau_i = tau0 - i*step)
       cap(tau) = K_terms * H0(tau), K_terms = (2g-1) g + (g-1)^2 (each Phi <= H0(s), s >= mu)."""
    from pairlaw import lower
    K = (2 * g - 1) * g + (g - 1) ** 2
    N = S.size
    flat = S.ravel()
    if tau0_grid is None:
        tau0_grid = np.round(np.arange(0.20, rho, 0.025), 4)
    K0 = len(tau0_grid)
    pw_cache = {}

    def P_within_below(t):
        key = round(t, 6)
        if key not in pw_cache:
            pw_cache[key] = float(lower(t, rho, n) - lower(-t, rho, n)) if t > 0 else 0.0
        return pw_cache[key]

    best = None
    for tau0 in tau0_grid:
        cap0 = K * float(H0(np.array([tau0]), n)[0])
        mc = np.minimum(flat, cap0).mean() + cap0 * math.sqrt(math.log(K0 / alpha) / (2 * N))
        peel = 0.0
        taus = np.arange(tau0, -1e-12, -step)
        for i in range(len(taus)):
            nxt = taus[i + 1] if i + 1 < len(taus) else 0.0
            capn = K * float(H0(np.array([max(nxt, 0.0)]), n)[0])
            pb = min(1.0, 2 * (g * (g - 1) // 2) * P_within_below(taus[i]))
            peel += capn * pb
            if pb < 1e-300:
                break
        tot = mc + peel
        if best is None or tot < best[0]:
            best = (tot, tau0, mc, peel)
    return best


if __name__ == "__main__":
    from scipy.stats import beta as Beta
    out = ["Theorem C (independent groups; PROOF.md §4). Per ordered independent group pair:",
           "  point = MC mean of S_L+S_N (an unbiased but heavy-tailed estimate of the bound; NOT itself rigorous);",
           "  rig   = rigorous upper bound on E[S] at MC-confidence 95% (Hoeffding on min(S,cap(tau0)) + exact peeling).",
           "Totals multiply by the number of ordered independent pairs G(G-1) (minus 2c for LH).",
           "LH linked pairs: direct MC of P((C*) fails inside one linked pair); CP95 = Clopper-Pearson 95% upper bound.",
           "n     p     g   rho  | point E[S] | rig E[S] (tau0) | total point | total rigorous | LH c=1: linked MC, CP95 | LH c=1 total rigorous(+CP95)"]
    t0 = time.time()
    cfgs = []
    for (n, p) in [(200, 500), (200, 1000)]:
        for g in (8, 10, 14):
            cfgs.append((n, p, g, 0.7))
        for rho in (0.4, 0.5, 0.85):
            cfgs.append((n, p, 10, rho))
    cfgs += [(400, 1790, 10, 0.7), (800, 4260, 10, 0.7), (100, 500, 10, 0.7)]
    for i, (n, p, g, rho) in enumerate(cfgs):
        G = p // g
        reps = 3000 if g <= 10 else 1000
        S, LL, MU = draws(n, g, rho, reps, 1000 + i)
        point = S.mean()
        rig, tau0, mc, peel = rigorous_C(n, g, rho, S)
        npairs = G * (G - 1)
        lp = ""; lht = ""
        if rho == 0.7 and g == 10:
            q, b = linked_pair_mc(n, g, rho, 0.5, 20000, 5000 + i)
            cp = Beta.ppf(0.95, b + 1, 20000 - b) if b < 20000 else 1.0
            lp = f"{b}/20000, CP95={cp:.2e}"
            lht = f"{(npairs - 2) * rig + cp:.3e}"
        out.append(f"{n:4d} {p:6d} {g:3d} {rho:5.2f} | {point:.2e} | {rig:.2e} ({tau0:.3f}) | {npairs*point:.2e}    | {npairs*rig:.3e}      | {lp:24s} | {lht}")
        print(out[-1], f"[{time.time()-t0:.0f}s]", flush=True)
    open("../results/sharp_bound.txt", "w").write("\n".join(out) + "\n")
