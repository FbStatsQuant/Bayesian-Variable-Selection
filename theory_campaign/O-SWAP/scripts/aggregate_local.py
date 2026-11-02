"""Aggregate ../out/local_p*_S*.csv into prediction-vs-observed tables -> ../out/TABLES_local.md."""
import csv, glob, os
from collections import defaultdict
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..', '..'))
obs = {}
for p in ('0500', '1000'):
    with open(f'{root}/Results/SMC_BVS_v3_production/p{p}/exact_recovery_long.csv') as f:
        for r in csv.DictReader(f):
            if r['method_id'] == 'SMCBVS' and r['rule_id'] == 'hpm' and r['scenario'] != 'pooled' \
               and int(r['p']) == int(p) and r['scale_key'] in ('c100', 'c050') and int(r['n_success']) > 0:
                obs[(int(p), int(r['scenario']), r['scale_key'])] = dict(
                    n=int(r['n_success']), miss=int(r['n_success']) - float(r['exact_all_sum']),
                    extra=int(r['err_extra_only']), missed=int(r['err_missed_only']), mixed=int(r['err_mixed']))
cells = defaultdict(list)
for fn in sorted(glob.glob(os.path.join(here, '..', 'out', 'local_p*_S*.csv'))):
    with open(fn) as f:
        for r in csv.DictReader(f):
            cells[(int(r['p']), int(r['scenario']), r['scale'])].append(r)
t2 = {}
for fn in sorted(glob.glob(os.path.join(here, '..', 'out', 't2_p*_S*.csv'))):
    with open(fn) as f:
        for r in csv.DictReader(f):
            t2[(int(r['p']), int(r['scenario']), r['scale'], int(r['rep']))] = r
for key, rows in cells.items():
    for r in rows:
        r.update({k: v for k, v in t2[(key[0], key[1], key[2], int(r['rep']))].items() if k.startswith(('T2', 'lecam'))})
S = lambda rows, k: sum(float(r[k]) for r in rows)
import math
def z(o, rows, k):  # observed count vs sum of per-design Bernoulli(p_i)
    ps = [float(r[k]) for r in rows]; m = sum(ps); v = sum(q * (1 - q) for q in ps)
    return (o - m) / math.sqrt(max(v, 1e-9))
zs = defaultdict(list)
out = []
tot = defaultdict(float)
for sc in ('c100', 'c050'):
    out.append(f"\n#### c = {'1' if sc == 'c100' else '0.5'}  (counts per 100 datasets; observed = SMC-BVS v3 HPM)\n")
    out.append("| p | S | **observed** miss (extra/missed/mixed) | realised on study y (extra/missed/mixed) | MC P(miss) (extra/missed/mixed) | MC P(L) one-move | **T2** (add / drop+swap) | T1 indep. | T1-lo | z(obs vs T2) | z(obs vs MC) | Le Cam floor |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for p in (500, 1000):
        for s in range(1, 7):
            rows = cells.get((p, s, sc))
            if not rows: continue
            o = obs[(p, s, sc)]; f = 100.0 / len(rows); fo = 100.0 / o['n']
            real = sum(int(r['real_miss']) for r in rows) * f
            rt = [sum(r['real_type'] == t for r in rows) * f for t in ('extra', 'missed', 'mixed')]
            mc = S(rows, 'MC_miss') * f; mct = [S(rows, 'MC_' + t) * f for t in ('extra', 'missed', 'mixed')]
            mcl = S(rows, 'MC_one') * f
            t1 = S(rows, 'A_ind') * f; lo = S(rows, 'A_lo') * f
            T2 = S(rows, 'T2') * f; T2a = S(rows, 'T2_add') * f; T2d = S(rows, 'T2_dropswap') * f
            lc = S(rows, 'lecam_floor') * f
            zt = z(o['miss'] * fo, rows, 'T2'); zm = z(o['miss'] * fo, rows, 'MC_miss'); zs[sc].append((zt, zm))
            out.append(f"| {p} | S{s} | **{o['miss']*fo:.0f}** ({o['extra']}/{o['missed']}/{o['mixed']}) | {real:.0f} ({rt[0]:.0f}/{rt[1]:.0f}/{rt[2]:.0f}) | "
                       f"{mc:.1f} ({mct[0]:.1f}/{mct[1]:.1f}/{mct[2]:.1f}) | {mcl:.1f} | **{T2:.1f}** ({T2a:.1f} / {T2d:.1f}) | {t1:.1f} | {lo:.1f} | {zt:+.1f} | {zm:+.1f} | {lc:.1f} |")
            for kk, v in (('obs', o['miss'] * fo), ('real', real), ('mc', mc), ('mcl', mcl), ('t1', t1), ('lo', lo), ('t2', T2)):
                tot[(sc, p, kk)] += v
            tot[(sc, p, 'k')] += 1
    for p in (500, 1000):
        if tot[(sc, p, 'k')]:
            k = tot[(sc, p, 'k')]
            out.append(f"| {p} | sum ({k:.0f} cells) | **{tot[(sc,p,'obs')]:.0f}** | {tot[(sc,p,'real')]:.0f} | {tot[(sc,p,'mc')]:.0f} | {tot[(sc,p,'mcl')]:.0f} | **{tot[(sc,p,'t2')]:.0f}** | {tot[(sc,p,'t1')]:.0f} | {tot[(sc,p,'lo')]:.0f} | | | |")
    zz = zs[sc]; out.append(f"\nRMS z (obs vs T2) = {math.sqrt(sum(a*a for a,_ in zz)/len(zz)):.2f}; RMS z (obs vs MC) = {math.sqrt(sum(b*b for _,b in zz)/len(zz)):.2f} over {len(zz)} cells.")
txt = '\n'.join(out)
print(txt)
open(os.path.join(here, '..', 'out', 'TABLES_local.md'), 'w', encoding='utf-8').write(txt + '\n')
