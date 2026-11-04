"""PC2 check of R1_C §E card D14 (K102): deterministic clause osc d <= D_* and its moment corollaries.

Exact enumeration of every |S| <= K at p <= 10, actual target, coded partition (complete linkage / cut / next-fit)
and also arbitrary partitions.  Designs: (i) genuinely correlated random designs with weak non-zero cross-block
correlation (data matrices, n in [12, 3000]); (ii) adversarial random Gram matrices; (iii) a scaled-down analogue of
Seat C's §E family.  Reports any case with a, delta_A, delta_H, r < 1 and osc d > D_* (a counterexample).
Also checks E_pi0[(pi/pi0)^2] <= e^{osc d} and chi2(q_{u+D}||q_u) <= e^{D osc d} - 1 on a grid.
Seeds fixed; runs in ~1-3 minutes.
"""
import math
import sys
import numpy as np
from bvs_common import (suff_from_data, method_sizes, coded_partition, d_table, card_Dstar, exact_gram_suff,
                        log_prior_w, A0)


def block_corr(p, groups, rho_in, eps_cross, rng, rand_sign=True):
    S = np.eye(p)
    gid = np.empty(p, int)
    start = 0
    for g, sz in enumerate(groups):
        gid[start:start + sz] = g
        start += sz
    for i in range(p):
        for j in range(i + 1, p):
            if gid[i] == gid[j]:
                v = rho_in
            else:
                v = eps_cross * (rng.choice([-1, 1]) if rand_sign else 1) * rng.uniform(0.5, 1.0)
            S[i, j] = S[j, i] = v
    return S, gid


def moments_check(models, d, p, K):
    # pi0 propto prior * prod r_b; pi propto pi0 * e^d.  Weighted by log prior + log prod r = lbf - d.
    return None


def check_case(G, z, Y, n, blocks, K, p, lbf=None, models=None, d=None):
    if models is None:
        models, d, lbf = d_table(G, z, Y, n, blocks, K)
    osc = float(d.max() - d.min())
    cs = card_Dstar(G, z, Y, n, blocks, K)
    # moments: log gamma0 = log prior + (lbf - d)
    lp = np.array([log_prior_w(p, len(S)) for S in models])
    lg0 = lp + lbf - d
    lpi0 = lg0 - np.logaddexp.reduce(lg0)
    lpi = lpi0 + d - np.logaddexp.reduce(lpi0 + d)
    m2 = float(np.exp(np.logaddexp.reduce(2 * (lpi - lpi0) + lpi0)))
    mom_ok = m2 <= math.exp(osc) * (1 + 1e-9)
    chi_ok = True
    for u in np.linspace(0, 1, 11)[:-1]:
        for Dl in (0.05, 0.1, 0.3):
            lq = lpi0 + u * d
            lq -= np.logaddexp.reduce(lq)
            lw = Dl * d
            onepchi = math.exp(np.logaddexp.reduce(2 * lw + lq) - 2 * np.logaddexp.reduce(lw + lq))
            if onepchi - 1 > math.exp(Dl * osc) - 1 + 1e-9:
                chi_ok = False
    return osc, cs, mom_ok, chi_ok, m2


def main():
    rng = np.random.default_rng(20261104)
    rows = []
    viol = []
    nmom = nchi = 0
    # (i) genuinely correlated random data designs, coded partition
    for it in range(120):
        p = int(rng.integers(5, 11))
        n = int(rng.choice([12, 20, 40, 100, 300, 1000, 3000]))
        K, B = method_sizes(n, p)
        B = max(B, 2)
        ng = int(math.ceil(p / B))
        sizes = [B] * (p // B) + ([p % B] if p % B else [])
        Sig, gid = block_corr(p, sizes, rng.uniform(0.2, 0.6), rng.choice([0.01, 0.03, 0.08, 0.15]), rng)
        if np.linalg.eigvalsh(Sig).min() < 0.05:
            continue
        L = np.linalg.cholesky(Sig)
        X = rng.standard_normal((n, p)) @ L.T
        theta = np.zeros(p)
        nz = rng.choice(p, size=int(rng.integers(1, 4)), replace=False)
        theta[nz] = rng.choice([-1, 1], size=len(nz)) * rng.uniform(0.05, 1.0, size=len(nz)) * n ** rng.uniform(-0.5, 0)
        y = X @ theta + rng.standard_normal(n)
        G, z, Y, nn = suff_from_data(X, y)
        blocks = coded_partition(G, B)
        osc, cs, mo, co, m2 = check_case(G, z, Y, n, blocks, K, p)
        nmom += (not mo)
        nchi += (not co)
        rows.append(('data', p, n, K, B, osc, cs['Dstar'], cs['a'], cs['dA'], cs['dH'], cs.get('r', np.nan)))
        if cs['ok'] and osc > cs['Dstar'] * (1 + 1e-9) + 1e-9:
            viol.append(rows[-1])
    # (ii) adversarial: random Gram (Wishart, small n) and arbitrary partitions
    for it in range(120):
        p = int(rng.integers(4, 9))
        n = int(rng.integers(max(p + 2, 8), 60))
        K, _ = method_sizes(n, p)
        X = rng.standard_normal((n, p)) @ rng.standard_normal((p, p)) * rng.uniform(0.2, 1)
        X += rng.standard_normal((n, p))
        y = X @ rng.standard_normal(p) * rng.uniform(0, 0.3) + rng.standard_normal(n)
        G, z, Y, nn = suff_from_data(X, y)
        perm = rng.permutation(p)
        cuts = sorted(rng.choice(np.arange(1, p), size=int(rng.integers(1, p)), replace=False))
        blocks = [list(map(int, c)) for c in np.split(perm, cuts)]
        osc, cs, mo, co, m2 = check_case(G, z, Y, n, blocks, K, p)
        nmom += (not mo)
        nchi += (not co)
        rows.append(('adv', p, n, K, len(blocks), osc, cs['Dstar'], cs['a'], cs['dA'], cs['dH'], cs.get('r', np.nan)))
        if cs['ok'] and osc > cs['Dstar'] * (1 + 1e-9) + 1e-9:
            viol.append(rows[-1])
    # (iii) scaled analogue of §E: groups of g, within 1/4, cross eps = 1/(n p) and larger, two n^{-1/4} signals
    for n in (50, 200, 1000, 5000, 20000, 100000):
        for eps_tag in ('1/(np)', 'n^-1/2', '0.05'):
            p, g = 8, 4
            eps = {'1/(np)': 1.0 / (n * p), 'n^-1/2': n ** -0.5, '0.05': 0.05}[eps_tag]
            Sig, gid = block_corr(p, [g, g], 0.25, eps, rng, rand_sign=False)
            theta = np.zeros(p)
            theta[0] = theta[g] = n ** -0.25
            G, z, Y, nn = exact_gram_suff(Sig, theta, n, 1.0, rng)
            K = min(p, n // 2)
            blocks = [list(range(g)), list(range(g, p))]
            osc, cs, mo, co, m2 = check_case(G, z, Y, n, blocks, K, p)
            nmom += (not mo)
            nchi += (not co)
            rows.append(('E-analog ' + eps_tag, p, n, K, 2, osc, cs['Dstar'], cs['a'], cs['dA'], cs['dH'],
                         cs.get('r', np.nan)))
            if cs['ok'] and osc > cs['Dstar'] * (1 + 1e-9) + 1e-9:
                viol.append(rows[-1])
    ok = [r for r in rows if np.isfinite(r[6])]
    print(f"cases: {len(rows)}; hypotheses (a,dA,dH,r<1) hold in {len(ok)}")
    print(f"violations osc d > D_*: {len(viol)}")
    for v in viol:
        print('  VIOLATION', v)
    print(f"moment failures E_pi0[(pi/pi0)^2] > e^osc: {nmom}; chi2 failures: {nchi}")
    if ok:
        ratio = np.array([r[5] / r[6] if r[6] > 0 else 0 for r in ok])
        print(f"osc/D_* among valid: min {ratio.min():.3g} median {np.median(ratio):.3g} max {ratio.max():.3g}")
    print("\nE-analog rows (tag, p, n, K, J, osc d, D_*, a, dA, dH, r):")
    for r in rows:
        if r[0].startswith('E-analog'):
            print('  ', r[0], r[2], f"osc={r[5]:.4g}", f"D*={r[6]:.4g}", f"a={r[7]:.3g}", f"dA={r[8]:.3g}",
                  f"dH={r[9]:.3g}", f"r={r[10]:.3g}")
    print("\nsample valid data rows:")
    for r in [x for x in ok if x[0] == 'data'][:12]:
        print('  ', r[0], 'p', r[1], 'n', r[2], 'K', r[3], 'B', r[4], f"osc={r[5]:.4g} D*={r[6]:.4g} a={r[7]:.3g}"
              f" dA={r[8]:.3g} dH={r[9]:.3g}")


if __name__ == '__main__':
    main()
