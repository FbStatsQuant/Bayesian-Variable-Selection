"""Aggregate cells_p*_S*.csv into prediction-vs-observed tables (markdown) for REPORT.md."""
import csv, glob, os, sys
from collections import defaultdict
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..', '..'))
obs = {}
for p in ('0500', '1000'):
    with open(f'{root}/Results/SMC_BVS_v3_production/p{p}/exact_recovery_long.csv') as f:
        for r in csv.DictReader(f):
            if r['method_id'] == 'SMCBVS' and r['rule_id'] == 'hpm' and r['scenario'] != 'pooled' \
               and int(r['p']) == int(p) and r['scale_key'] in ('c100', 'c050'):
                fail = int(r['err_failed']); ex = float(r['exact_all_sum'])
                obs[(int(p), int(r['scenario']), r['scale_key'])] = dict(
                    exact=ex, fail=fail, miss=100 - ex - fail, extra=int(r['err_extra_only']),
                    missed=int(r['err_missed_only']), mixed=int(r['err_mixed']))
cells = defaultdict(list)
for fn in sorted(glob.glob(os.path.join(here, '..', 'out', 'cells_p*_S*.csv'))):
    with open(fn) as f:
        for r in csv.DictReader(f):
            cells[(int(r['p']), int(r['scenario']), r['scale'])].append(r)
def S(rows, k): return sum(float(r[k]) for r in rows)
out = []
for sc in ('c100', 'c050'):
    out.append(f"\n### c = {'1' if sc=='c100' else '0.5'}\n")
    out.append("| p | S | obs SMC misses | realised 1-move (exact y) | MC P(L) ×100 | T1 indep ×100 | T1-lo cluster-max ×100 | obs extra / missed / mixed | realised add / drop / swap | MC add / drop / swap | T1 add / drop / swap |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|")
    tot = defaultdict(float)
    for p in (500, 1000):
        for s in range(1, 7):
            rows = cells.get((p, s, sc));
            if not rows: continue
            o = obs[(p, s, sc)]
            k = len(rows); f = 100.0 / k
            real = sum(float(r['real_best_gap']) > 0 for r in rows) * f
            rt = {t: sum(r['real_type'] == t for r in rows) * f for t in ('add', 'drop', 'swap')}
            mc = S(rows, 'MC_any') * f
            mct = [S(rows, 'MC_' + t) * f for t in ('add', 'drop', 'swap')]
            t1 = S(rows, 'A_ind') * f; lo = S(rows, 'A_lo') * f
            t1t = [S(rows, 'A_ind_' + t) * f for t in ('add', 'drop', 'swap')]
            out.append(f"| {p} | S{s} | {o['miss']:.0f} | {real:.0f} | {mc:.1f} | {t1:.1f} | {lo:.1f} | {o['extra']} / {o['missed']} / {o['mixed']} | "
                       f"{rt['add']:.0f} / {rt['drop']:.0f} / {rt['swap']:.0f} | {mct[0]:.1f} / {mct[1]:.1f} / {mct[2]:.1f} | {t1t[0]:.1f} / {t1t[1]:.1f} / {t1t[2]:.1f} |")
            for kk, v in (('obs', o['miss']), ('real', real), ('mc', mc), ('t1', t1), ('lo', lo)): tot[(p, kk)] += v
    for p in (500, 1000):
        if (p, 'obs') in tot:
            out.append(f"| {p} | all | {tot[(p,'obs')]:.0f} | {tot[(p,'real')]:.0f} | {tot[(p,'mc')]:.0f} | {tot[(p,'t1')]:.0f} | {tot[(p,'lo')]:.0f} | | | | |")
txt = '\n'.join(out)
print(txt)
open(os.path.join(here, '..', 'out', 'TABLES.md'), 'w').write(txt + '\n')
