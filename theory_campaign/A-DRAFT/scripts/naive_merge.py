#!/usr/bin/env python3
"""Four-model calculation, not an SMC simulation. Run only via owls_run -j 2.
Gaussian sufficient statistics are sampled exactly for a centered fixed design.
All posterior sums enumerate the four p=2 models using the v3 score.
"""
from pathlib import Path
import csv
import json
import math
import os
os.environ.setdefault('MPLCONFIGDIR', str(Path(__file__).resolve().parents[1] / 'reading' / 'mpl-config'))
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

if 'OWLS_JOB_CORES' not in os.environ:
    raise SystemExit('Run with /home/fb31/.config/bvs-hq/owls/owls_run -j 2 -- python3 ...')
OUT = Path(__file__).resolve().parents[1] / 'results'
OUT.mkdir(exist_ok=True)
SEED = 20261102
RHO, BETA, SIGMA = 0.8, 1.0, 1.0
MODELS = [(), (0,), (1,), (0, 1)]

def normalise(logw):
    v = np.exp(np.asarray(logw) - max(logw))
    return v / v.sum()

def logbf(n, gram, z, yy, model):
    if not model:
        return 0.0
    ix = list(model)
    g = gram[np.ix_(ix, ix)]
    zz = z[ix]
    h = (n + 1) * g + np.eye(len(ix))
    q = yy - n * zz @ np.linalg.solve(h, zz)
    assert q >= yy / (n + 1) - 1e-8
    logd = np.linalg.slogdet(h)[1] - np.linalg.slogdet(g + np.eye(len(ix)))[1]
    return -0.5 * logd - (0.01 + n / 2) * math.log((0.02 + q) / (0.02 + yy))

rows = []
for n in [40, 100, 400, 1600, 6400, 25600]:
    rng = np.random.default_rng(np.random.SeedSequence([SEED, n]))
    gram = (n - 1) * np.array([[1., RHO], [RHO, 1.]])
    chol = np.linalg.cholesky(gram)
    u = rng.normal(size=2)
    cross = SIGMA * chol @ u  # X'epsilon ~ N(0, sigma^2 G)
    beta = np.array([BETA, 0.])
    yy_raw = beta @ gram @ beta + 2 * beta @ cross + SIGMA**2 * (u @ u + rng.chisquare(n - 3))
    z_raw = gram @ beta + cross
    z = z_raw * math.sqrt((n - 1) / yy_raw)
    yy = float(n - 1)
    bfs = np.array([logbf(n, gram, z, yy, m) for m in MODELS])
    prior = np.array([math.log(0.5 / math.comb(3, len(m))) for m in MODELS])
    full = normalise(prior + bfs)
    # Each singleton local analysis has BB(1,1), hence prior odds 1.
    local = [normalise([0., bfs[j]])[1] for j in [1, 2]]
    product = np.array([(1-local[0])*(1-local[1]), local[0]*(1-local[1]),
                        (1-local[0])*local[1], local[0]*local[1]])
    # v3's composite start uses the GLOBAL size prior; it is not product.
    start_logw = prior + np.array([0., bfs[1], bfs[2], bfs[1]+bfs[2]])
    start_logz = max(start_logw) + math.log(np.exp(start_logw-max(start_logw)).sum())
    start = normalise(start_logw)
    # Independent direct covariance likelihood check: det(I+n X(G+I)^-1 X').
    direct = []
    for m in MODELS:
        if not m:
            direct.append(0.0)
            continue
        ix = list(m)
        g, zz = gram[np.ix_(ix, ix)], z[ix]
        a = n * np.linalg.inv(g + np.eye(len(ix)))
        logd = np.linalg.slogdet(np.eye(len(ix)) + a @ g)[1]
        q = yy - zz @ np.linalg.solve(np.linalg.inv(a) + g, zz)
        direct.append(-0.5*logd - (0.01+n/2)*math.log((0.02+q)/(0.02+yy)))
    assert np.max(np.abs(bfs-np.array(direct))) < 1e-8
    for law in [full, product, start]:
        assert abs(law.sum()-1) < 1e-12 and np.all(law >= 0)
    row = dict(n=n, full_pip1=full[1]+full[3], full_pip2=full[2]+full[3],
               full_joint12=full[3], local_pip1=local[0], local_pip2=local[1],
               product_joint12=product[3], start_pip2=start[2]+start[3],
               start_truth=start[1], log_start_truth=start_logw[1]-start_logz, full_truth=full[1],
               union_hpm='12' if min(local) > .5 else 'other',
               union_mpm='12' if min(local) > .5 else 'other',
               full_hpm=['empty', '1', '2', '12'][int(full.argmax())],
               max_score_check_error=float(np.max(np.abs(bfs-np.array(direct)))))
    rows.append(row)
    print(json.dumps(row))
with (OUT / 'naive_merge.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
with (OUT / 'metadata.json').open('w') as f:
    json.dump(dict(seed=SEED, rho=RHO, beta=BETA, sigma=SIGMA,
                   states=4, method='exact four-state sums, floating point',
                   numpy=np.__version__, owls_cores=os.environ['OWLS_JOB_CORES']), f, indent=2)
fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), constrained_layout=True)
ns = [r['n'] for r in rows]
for ax, target, naive, label in [(axes[0], 'full_pip2', 'local_pip2', 'Proxy inclusion probability'),
                                 (axes[1], 'full_joint12', 'product_joint12', 'Joint inclusion probability')]:
    ax.semilogx(ns, [r[target] for r in rows], 'o-', color='#2563eb', label='Full posterior / exact v3')
    ax.semilogx(ns, [r[naive] for r in rows], 's--', color='#dc2626', label='Product of local posteriors')
    ax.set(xlabel='Sample size n', ylabel=label, ylim=(-.03, 1.05))
    ax.grid(alpha=.2)
axes[0].legend(fontsize=8, loc='center right')
fig.suptitle('A correlated proxy is selected locally and rejected globally (rho = 0.8)')
fig.savefig(OUT / 'naive_merge.png', dpi=180)
fig.savefig(OUT / 'naive_merge.svg')
print('Checks passed: score identities, probability normalisation; no SMC fit performed.')
