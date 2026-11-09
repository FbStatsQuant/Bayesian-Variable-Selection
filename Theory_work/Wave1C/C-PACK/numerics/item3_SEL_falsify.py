"""Read-only generator/SEL audit; writes only the adjacent *_out.txt file.

Run with Python 3.13 + numpy/scipy. Twelve independent seeds, exact enumeration
of ALL admissible T in the actual data-dependent blocks. No response noise is
needed: SEL is an X-only claim. Gaussian block-factor draws have exactly the
covariance law of gen_dev_data.R, but do not reproduce its R random stream.
"""
import os
os.environ["OPENBLAS_NUM_THREADS"] = "2"
os.environ["OMP_NUM_THREADS"] = "2"
from pathlib import Path
import time
import numpy as np
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import squareform
from threadpoolctl import threadpool_limits


def truth(step):
    k = np.arange(14)
    pos = np.array([3, 2, 4, 1, 5, 3])
    pat = np.array([1.4, -1.0, 1.8, -1.2, 0.8, -1.6])
    return 5 * step * k + pos[k % 6] - 1, pat[k % 6]


def design(n, p, scenario, rng):
    if scenario == 1:
        raw = rng.normal(size=(n, p))
    else:
        rho = ({3: np.full(p // 5, .7), 4: np.full(p // 5, .85),
                6: .4 + .1 * (np.arange(p // 5) % 6)})[scenario]
        rho = np.repeat(rho, 5)
        raw = (rng.normal(size=(n, p)) * np.sqrt(1 - rho)
               + np.repeat(rng.normal(size=(n, p // 5)), 5, axis=1)
               * np.sqrt(rho))
    raw -= raw.mean(axis=0)
    raw /= np.sqrt(np.sum(raw ** 2, axis=0) / (n - 1))
    return raw


def make_blocks(corr, n):
    """Complete linkage, smaller-minimum-index child first; next-fit whole nodes.

    Continuous draws make exact distance ties probability zero. scipy's
    complete-linkage distance update is max, as in v3_blocks.h.
    """
    p = len(corr)
    cap = min(int(np.sqrt(n)), int(np.sqrt(p)), 16)
    d = np.clip(1 - abs(corr), 0, 1)
    np.fill_diagonal(d, 0)
    tree = linkage(squareform(d, checks=False), method="complete")
    sizes = np.ones(2 * p - 1, dtype=int)
    mins = np.arange(2 * p - 1)
    children = {}
    for k, row in enumerate(tree):
        a, b = map(int, row[:2])
        if mins[a] > mins[b]:
            a, b = b, a
        nd = p + k
        children[nd] = (a, b)
        sizes[nd] = sizes[a] + sizes[b]
        mins[nd] = mins[a]

    def leaves(nd):
        if nd < p:
            return [nd]
        a, b = children[nd]
        return leaves(a) + leaves(b)

    clusters, stack = [], [2 * p - 2]
    while stack:
        nd = stack.pop()
        if sizes[nd] <= cap:
            clusters.append(leaves(nd))
        else:
            a, b = children[nd]
            stack.extend([b, a])
    blocks, cur = [], []
    for cluster in clusters:
        if len(cur) + len(cluster) > cap:
            blocks.append(np.array(sorted(cur)))
            cur = []
        cur += cluster
    if cur:
        blocks.append(np.array(sorted(cur)))
    return blocks, cap


def exhaustive_block(corr, xmu, mu2, block, active, n, h, scenario):
    """All T = (S0 intersect block) union a subset of the block's nulls.

    Schur complements enumerate every subset; the last coordinate is mu.
    Normalized covariances use n-1. Also check a few states by direct solves.
    """
    mandatory = block[np.isin(block, active)]
    nulls = block[~np.isin(block, active)]
    m = len(nulls)
    if not m:
        return np.array([]), 0., 0., 0., 0, 0.
    allcols = np.r_[nulls, mandatory]
    base = np.empty((len(allcols) + 1, len(allcols) + 1))
    base[:-1, :-1] = corr[np.ix_(allcols, allcols)]
    base[:-1, -1] = base[-1, :-1] = xmu[allcols]
    base[-1, -1] = mu2
    if len(mandatory):
        keep = np.r_[np.arange(m), len(allcols)]
        cond = np.arange(m, len(allcols))
        base = (base[np.ix_(keep, keep)]
                - base[np.ix_(keep, cond)]
                @ np.linalg.solve(base[np.ix_(cond, cond)], base[np.ix_(cond, keep)]))
    states = base[None, :, :]
    for k in range(m):
        col = states[:, :, k]
        added = states - col[:, :, None] * col[:, None, :] / states[:, k, k, None, None]
        added[:, k, :] = 0.
        added[:, :, k] = 0.
        states = np.concatenate((states, added), axis=0)
    # Cross-check empty, full, and one intermediate conditioning set directly.
    solve_error = 0.
    for mask in [0, (1 << m) - 1, ((1 << m) - 1) // 3]:
        chosen = [k for k in range(m) if mask & (1 << k)]
        direct = base.copy()
        if chosen:
            direct -= base[:, chosen] @ np.linalg.solve(base[np.ix_(chosen, chosen)], base[chosen, :])
        solve_error = max(solve_error, float(np.max(abs(states[mask] - direct))))
    masks = np.arange(1 << m)
    active_groups = set(active // 5)
    maxima = np.empty(m)
    max_delta = max_q0 = max_excess = 0.
    triples = 0
    for k, l in enumerate(nulls):
        valid_masks = masks[(masks & (1 << k)) == 0]
        v = states[valid_masks, k, k]
        lam = np.maximum(states[valid_masks, -1, -1], 0.)
        cov = states[valid_masks, k, -1]
        delta = (n - 1) * cov ** 2 / v
        q = np.divide(cov ** 2, v * lam, out=np.zeros_like(lam), where=lam > 1e-10)
        exponent = np.minimum((n - 1) * q / 2,
                              delta / (2 * (1 + lam)) + np.sqrt(delta) * h / (1 + lam))
        # The singletons convention for S1 is supplied by the caller.
        own_and_signal = 0
        for j, col in enumerate(nulls):
            if (col // 5 == l // 5) or (col // 5 in active_groups):
                own_and_signal |= 1 << j
        if scenario == 1:
            own_and_signal = 0  # all T0 columns are mandatory truths
        t0masks = valid_masks & own_and_signal
        lam0 = np.maximum(states[t0masks, -1, -1], 0.)
        var0 = states[t0masks, k, k]
        cov0 = states[t0masks, k, -1]
        q0 = np.divide(cov0 ** 2, var0 * lam0, out=np.zeros_like(lam0), where=lam0 > 1e-10)
        max_excess = max(max_excess, float(np.max(exponent - (n - 1) * q0 / 2)))
        maxima[k] = np.max(exponent)
        max_delta = max(max_delta, float(np.max(delta)))
        max_q0 = max(max_q0, float(np.max(q0)))
        triples += len(valid_masks)
    return maxima, max_delta, max_q0, max_excess, triples, solve_error


def run():
    global SCENARIO
    lines = []
    start = time.perf_counter()

    def emit(s):
        print(s, flush=True)
        lines.append(s)
        Path(__file__).with_name("item3_SEL_falsify_out.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    emit("SEL falsification experiment: exact exhaustive actual-block leakage triples")
    emit("12 independent seeds; Gaussian covariance-law port; c=1, sigma=1, A=2, epsilon0=1.")
    emit("p(n)=5*ceil(max(1000,n/2)/5); both fixed support layouts exercised.")
    emit("No simulations of response noise or claims about start-mode recovery.")
    emit("Q0 maximum is over T0 induced by actual blocks, not the entire enlarged deterministic family.")
    emit("Numerics target n^(3/8) only asymptotically; finite-n exceedances alone do not refute SEL.")
    emit("S n p step seed B J whole_groups avg_exp avg/n^.375 max_delta2/logn max_Q0*n/logn max_positive_E_minus_base triples solve_err seconds")
    for ni, n in enumerate([200, 800, 3200]):
        p = 5 * int(np.ceil(max(1000, n / 2) / 5))
        assert p <= n ** 2
        for si, SCENARIO in enumerate([1, 3, 4, 6]):
            t0 = time.perf_counter()
            seed = 31001 + 4 * ni + si
            step = [7, 13][(ni + si) % 2]
            active, beta = truth(step)
            rng = np.random.default_rng(seed)
            x = design(n, p, SCENARIO, rng)
            mu = x[:, active] @ beta
            corr = (x.T @ x) / (n - 1)
            xmu, mu2 = (x.T @ mu) / (n - 1), float(mu @ mu / (n - 1))
            del x
            blocks, cap = make_blocks(corr, n)
            whole = all(all(np.count_nonzero(block // 5 == g) == 5 for g in set(block // 5)) for block in blocks)
            h = np.sqrt(2 * 3 * np.log(n))
            exps, md, mq, me, count, err = [], 0., 0., 0., 0, 0.
            for block in blocks:
                vals, d, q, e, c, se = exhaustive_block(corr, xmu, mu2, block, active, n, h, SCENARIO)
                exps.extend(vals)
                md, mq, me, count, err = max(md, d), max(mq, q), max(me, e), count + c, max(err, se)
            assert len(exps) == p - 14
            avg = float(np.mean(np.exp(exps)))
            emit(f"S{SCENARIO} {n} {p} {step} {seed} {cap} {len(blocks)} "
                 f"{whole if SCENARIO != 1 else 'NA'} {avg:.8g} {avg/n**.375:.8g} "
                 f"{md/np.log(n):.8g} {mq*n/np.log(n):.8g} {me:.8g} {count} {err:.3g} {time.perf_counter()-t0:.2f}")
    emit(f"Elapsed seconds: {time.perf_counter()-start:.2f}")
    emit("Exact-T maxima computed for every null l in each realized partition. No tail-probability inference from 12 draws.")


if __name__ == "__main__":
    with threadpool_limits(limits=2):
        run()
