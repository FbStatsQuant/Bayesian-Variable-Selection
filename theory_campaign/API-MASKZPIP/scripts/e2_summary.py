"""E2(b) check: over all grids, sets A and stages t, the fraction of islands with {miss at t-1} and W > kappa_t(A)/0.05
(Markov bound: <= 0.05 in expectation). Also reports E[W 1_miss] vs kappa (heavy-tailed MC; informational)."""
import json, glob, os
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
for f in sorted(glob.glob(os.path.join(base, 'check_*.jsonl'))):
    worst, cnt, nmiss = 0.0, 0, 0
    for l in open(f):
        d = json.loads(l)
        if d['kind'] != 'grid' or 'E2' not in d:
            continue
        for k, v in d['E2'].items():
            for t in range(d['T']):
                cnt += 1
                nmiss += v['P_miss'][t] > 0
                worst = max(worst, v['frac_W_gt_kappa_over_eta'][t])
    if cnt:
        print(os.path.basename(f), 'cases', cnt, 'cases with misses', nmiss, 'max frac(miss & W > 20 kappa) =', worst, '(Markov: <= 0.05; 40 islands)')
