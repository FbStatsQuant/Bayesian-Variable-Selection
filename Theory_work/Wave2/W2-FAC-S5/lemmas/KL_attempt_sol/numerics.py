"""Falsification checks for the restricted CC proof and champion lemma.

Run: py -3.13 Theory_work/Wave2/W2-FAC-S5/lemmas/KL_attempt_sol/numerics.py
All outputs stay beside this script. No imports from repository numerics.
"""
from pathlib import Path
import json
import math
import numpy as np

OUT = Path(__file__).resolve().parent


def frozen_checks(rng):
    failures = []
    trials = 0
    for v in range(2, 11):
        for _ in range(20000):
            b, d = np.exp(rng.uniform(-4, 3, 2))
            z = rng.normal(size=v) * np.exp(rng.uniform(-3, 3))
            x = b * z.sum() / (d + v * b)
            if np.argmax(np.abs(z)) == np.argmin(np.abs(z - x)):
                failures.append(dict(v=v, b=b, d=d, z=z.tolist()))
            trials += 1
    return dict(trials=trials, failures=failures[:3], n_failures=len(failures))


def cs_path(rng, p, lam, alpha=.49):
    # Fixed anchor B=O_P(1). Every deletable coordinate is a singleton.
    z = rng.normal(size=p)
    B = float(rng.normal())
    keep = np.ones(p, bool)
    sm = float(z.sum())
    H = math.sqrt(2 * math.log(p))
    # p here counts nulls; total p differs by the four truths.
    total_p = p + 4
    logn = math.log(total_p) / alpha
    Hq = math.sqrt(2 * math.log(32 * total_p) + 2 * math.log(logn))
    worst_ratio = 0.
    max_neighbour = 0.
    max_visited = 0.
    level_decreases = 0
    prev = -1.
    snapshots = []
    for m in range(p, -1, -1):
        x = (sm + B) / (m + lam)
        idx = np.flatnonzero(keep)
        neigh = (sm - z[idx] + B) / (m - 1 + lam) if m else np.empty(0)
        em = max(abs(x), float(np.max(np.abs(neigh))) if m else 0.)
        k = m + 4
        rhs = logn + 2 * math.log((2 * total_p - k) / (k + 1))
        worst_ratio = max(worst_ratio, (Hq + em) ** 2 / rhs)
        max_visited = max(max_visited, abs(x) / H)
        max_neighbour = max(max_neighbour, em / H)
        if m <= 5:
            snapshots.append(dict(m=m, imbalance=int(np.sign(z[idx]).sum()),
                                  x_over_H=x / H, neighbour_over_H=em / H))
        if not m:
            break
        j = int(idx[np.argmin(np.abs(z[idx] - x))])
        level = abs(z[j] - x) / math.sqrt(1 - 1 / (m + lam))
        if level < prev - 1e-10:
            level_decreases += 1
        prev = level
        keep[j] = False
        sm -= z[j]
    return dict(p=p, lam=lam, alpha=alpha, worst_CC_ratio=worst_ratio,
                max_visited_over_H=max_visited, max_neighbour_over_H=max_neighbour,
                level_decreases=level_decreases, end=snapshots)


def bcs_path(rng, p=1000, q=5, rb=.3, rw=.7):
    b, d, a = rw - rb, 1 - rw, 1 - rb
    grp = np.arange(p) // q
    G = int(grp[-1]) + 1
    y = math.sqrt(b) * rng.normal(size=G)[grp] + math.sqrt(d) * rng.normal(size=p)
    h = math.sqrt(rb) * float(rng.normal())
    truth = np.zeros(p, bool)
    truth[np.linspace(0, G - 1, 6, dtype=int)[1:-1] * q] = True
    keep = np.ones(p, bool)
    H = math.sqrt(2 * math.log(p))
    original_champion = np.array([g * q + np.argmax(np.abs(y[g*q:min((g+1)*q, p)])) for g in range(G)])
    champion_counterexample = None
    local_champion_failures = 0
    record = 0.
    for _ in range(p - int(truth.sum())):
        ids = np.flatnonzero(keep)
        u = np.bincount(grp[ids], minlength=G)
        sy = np.bincount(grp[ids], weights=y[ids], minlength=G)
        phi = 1 / (d + b * u)
        V = 1 / (1 / rb + np.sum(u * phi))
        e = V * (h / rb - np.sum(sy * phi))
        # Precision representation: Sigma_T^-1 g_T = B_T^-1(y_T+e).
        z = y[ids] + e
        t = (z - b * phi[grp[ids]] * (sy[grp[ids]] + u[grp[ids]] * e)) / d
        pd = (1 - b * phi[grp[ids]]) / d - V * phi[grp[ids]] ** 2
        tau = t / np.sqrt(pd)
        tau[truth[ids]] = np.inf
        j = int(ids[np.argmin(np.abs(tau))])
        gj = int(grp[j])
        members = ids[grp[ids] == gj]
        if len(members) >= 2 and not truth[members].any():
            if j == members[np.argmax(np.abs(y[members] + e))]:
                local_champion_failures += 1
            if j == original_champion[gj] and champion_counterexample is None:
                champion_counterexample = dict(j=j, y=y[members].tolist(), e=e,
                                              shifted=(y[members] + e).tolist())
        record = max(record, abs(e) / math.sqrt(a) / H)
        keep[j] = False
    return dict(max_e_over_H=record, local_champion_failures=local_champion_failures,
                original_champion_counterexample=champion_counterexample)


def main():
    rng = np.random.default_rng(20261109)
    frozen = frozen_checks(rng)
    cs = [cs_path(rng, p, lam, alpha) for p in (100, 1000, 5000)
          for lam in (217/57, 19/3) for alpha in (.2, .35, .49)
          for _ in range(4)]
    bcs = [bcs_path(rng) for _ in range(60)]
    a0, b0, r = .9995, .51, 4/7
    J = a0*a0 + (b0-r*a0)**2/(1-r*r)
    c = 114/331
    summary = dict(
        frozen=frozen,
        cs_n=len(cs),
        cs_worst_CC_ratio=max(x['worst_CC_ratio'] for x in cs),
        cs_smallest_CC_ratio=min(x['worst_CC_ratio'] for x in cs),
        cs_by_alpha={str(alpha): dict(
            n=sum(x['alpha'] == alpha for x in cs),
            min_ratio=min(x['worst_CC_ratio'] for x in cs if x['alpha'] == alpha),
            max_ratio=max(x['worst_CC_ratio'] for x in cs if x['alpha'] == alpha),
            passes=sum(x['worst_CC_ratio'] < 1 for x in cs if x['alpha'] == alpha),
        ) for alpha in (.2, .35, .49)},
        cs_paths_with_level_decrease=sum(x['level_decreases'] > 0 for x in cs),
        bcs_n=len(bcs),
        bcs_local_champion_failures=sum(x['local_champion_failures'] for x in bcs),
        bcs_original_champion_failures=sum(x['original_champion_counterexample'] is not None for x in bcs),
        first_original_champion_counterexample=next((x['original_champion_counterexample'] for x in bcs if x['original_champion_counterexample']), None),
        protected_shell_exponent=J,
        protected_shell_field_margin=(a0+b0)/2-.75,
        S5_anchor_lambda_min=217/57,
        S5_neighbour_coefficient=c,
        S5_end_CC_ratio_at_alpha_half=(1+c)**2/2,
        S5_end_alpha_cutoff=1/(2*c*(2+c)),
    )
    (OUT / 'numerics_raw.json').write_text(json.dumps(dict(cs=cs, bcs=bcs), indent=2), encoding='utf-8')
    (OUT / 'numerics_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
