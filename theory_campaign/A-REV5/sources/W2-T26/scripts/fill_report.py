"""Fill the numeric tables of REPORT.md from results/ (run once, after all numerics finish)."""
import csv, glob, json, os
import numpy as np

here = os.path.join(os.path.dirname(__file__), '..')
rows = []
for f in sorted(glob.glob(os.path.join(here, 'results', 'premise_scan*.csv'))):
    rows += list(csv.DictReader(open(f)))
order = ['fav_iid', 'fav_cor', 'masked']
keys = sorted({(r['design'], int(r['n'])) for r in rows}, key=lambda k: (order.index(k[0]), k[1]))
lines = []
for d, n in keys:
    rs = [r for r in rows if r['design'] == d and int(r['n']) == n]
    med = lambda c: float(np.median([float(r[c]) for r in rs]))
    pip = float(np.median([min(1.0, float(r['rho_bar_bound'])) + float(r['u_pi']) for r in rs]))
    lines.append(f"| {d} | {n} | {med('one_minus_pi0'):.2e} | {med('delta1'):.2e} | {med('Delta'):.2e} | "
                 f"{med('T_ideal'):.0f} | {med('P1_Tideal'):.2e} | {med('P1_Tmax'):.2e} | {pip:.2e} | {med('P2'):.2e} |")
gap = max(abs(float(r['Delta_grid']) - float(r['Delta'])) for r in rows)
orth = list(csv.DictReader(open(os.path.join(here, 'results', 'orth_check.csv'))))
ol = ['| n | p | B | max|R| (max over seeds) | median 1−π₀(S₀) | median (T^max+1)(1−π₀(S₀)) |', '|---|---|---|---|---|---|']
for n in sorted({int(r['n']) for r in orth}):
    rs = [r for r in orth if int(r['n']) == n]
    ol.append(f"| {n} | {rs[0]['p']} | {rs[0]['B']} | {max(float(r['maxR']) for r in rs):.3f} | "
              f"{np.median([float(r['one_minus_pi0']) for r in rs]):.3e} | {np.median([float(r['P1start']) for r in rs]):.1f} |")
sl = ['| design | n | N | reps | T | Δ_n | E|W_r−1| | bound b | E occupancy (end T / round starts) | its bound | '
      'E max_j PIP err (island) | bound (A-0)(c) | old (L+5/2)ρ̄ bound | exact-posterior PIP err | MPM wrong |',
      '|' + '---|' * 15]
for l in open(os.path.join(here, 'results', 'smc_sim.jsonl')):
    d = json.loads(l)
    sl.append(f"| {d['design']} | {d['n']} | {d['N']} | {d['reps']} | {d['T']} | {d['Delta']:.3g} | "
              f"{d['mean_abs_W_minus_1']:.2e} | {d['bound_b']:.2e} | {d['mean_f']:.3f} / {d['mean_round_start_f']:.3f} | "
              f"{d['bound_f']:.3f} | {d['mean_island_pip_err']:.2e} | {d['bound_pip']:.2e} | {d['bound_pip_old']:.2f} | "
              f"{d['exact_pip_err']:.2e} | {d['mpm_wrong_frac']:.2f} |")
p = os.path.join(here, 'REPORT.md')
s = open(p).read()
s = s.replace('SCAN_TABLE', '\n'.join(lines)).replace('SCAN_COUNT', str(len(rows)))
s = s.replace('ORTH_TABLE', '\n'.join(ol)).replace('SIM_TABLE', '\n'.join(sl))
s = s.replace('(max |Δ_grid − Δ| = 0)', f'(max |Δ_grid − Δ| = {gap:.1e})')
open(p, 'w').write(s)
print('filled', len(rows), 'scan rows;', len(orth), 'orth rows')
