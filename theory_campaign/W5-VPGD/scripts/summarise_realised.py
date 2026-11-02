"""Summarise results/realised.jsonl -> results/realised_summary.md.
eta_pop (population PGD constant on R_{2,2}(D), D = truth-block mates) from results/study_pop_A.json / _B.json."""
import json, collections
import numpy as np

A = json.load(open('../results/study_pop_A.json')); B = json.load(open('../results/study_pop_B.json'))
eta_pop = {1: A['S1']['scan a=2 d=2']['eta'], 3: A['S3']['scan a=2 d=2']['eta'], 4: A['S4']['scan a=2 d=2']['eta'],
           6: A['S6']['scan a=2 d=2']['eta'], 2: B['S2']['eta'], 5: B['S5']['eta']}
recs = [json.loads(l) for l in open('../results/realised.jsonl')]
cell = collections.defaultdict(list)
for r in recs:
    cell[(r['scen'], r['n'])].append(r)
lines = ["| scen | n | designs | eta_pop | median eta_hat [min, max] | PGD(eta_pop/2) | eta_hat > 0 | TD'_P c=1 | TD'_P c=0.5 | (L) c=1 / c=0.5 | median #failing states c=1 / c=0.5 | failing (m,e) classes c=0.5 | binding non-progress (c=0.5) |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
for (s, n) in sorted(cell):
    rs = cell[(s, n)]
    eh = np.array([r['eta_hat'] for r in rs]); ep = eta_pop[s]
    td1 = sum(r['c1']['TD'] for r in rs); td5 = sum(r['c05']['TD'] for r in rs)
    L1 = sum(r['c1']['L'] for r in rs); L5 = sum(r['c05']['L'] for r in rs)
    f1 = np.median([r['c1']['fail_states'] for r in rs]); f5 = np.median([r['c05']['fail_states'] for r in rs])
    me = collections.Counter(); bd = collections.Counter()
    for r in rs:
        me.update(r['c05']['fail_by_me']); bd.update(r['c05']['binding'])
    me_s = ', '.join(f"{k}:{v}" for k, v in sorted(me.items())) or '-'
    bd_s = ', '.join(f"{k}:{v}" for k, v in bd.most_common(3)) or '-'
    k = len(rs)
    lines.append(f"| S{s} | {n} | {k} | {ep:.4f} | {np.median(eh):.4f} [{eh.min():.4f}, {eh.max():.4f}] | {int((eh >= ep / 2).sum())}/{k} | "
                 f"{int((eh > 0).sum())}/{k} | {td1}/{k} | {td5}/{k} | {L1}/{k} / {L5}/{k} | {f1:.0f} / {f5:.0f} | {me_s} | {bd_s} |")
txt = '\n'.join(lines)
print(txt)
open('../results/realised_summary.md', 'w').write("# Realised-design transfer (p = 500, R_{2,2}(D), D = 56 truth-block mates; 167,685 states with m >= 1, 169,281 with S0 excluded for D_S)\n\n" + txt + '\n')
