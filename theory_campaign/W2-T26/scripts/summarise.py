"""Summarise results/premise_scan*.csv into a markdown table (medians over seeds) -> results/premise_summary.md"""
import csv, os, glob
import numpy as np

here = os.path.join(os.path.dirname(__file__), '..', 'results')
rows = []
for f in sorted(glob.glob(os.path.join(here, 'premise_scan*.csv'))):
    rows += list(csv.DictReader(open(f)))
keys = sorted({(r['design'], int(r['n'])) for r in rows}, key=lambda k: (['fav_iid', 'fav_cor', 'masked'].index(k[0]), k[1]))
cols = ['one_minus_pi0', 'delta1', 'Delta', 'T_ideal', 'P1_Tideal', 'P1_Tmax', 'rho_bar_bound', 'u_pi', 'P2']
out = ['| design | n | seeds | med 1−π₀(S₀) | med δ₁ | med Δ_n | max |Δ_grid−Δ| | med T_ideal | med (T_ideal+1)Δ | '
       'med (T^max+1)Δ | med ρ̄-bound+u_π | med (L+4)ρ* (frozen P2) | frac S₀=HPM | frac S₀=start mode |',
       '|' + '---|' * 14]
for d, n in keys:
    rs = [r for r in rows if r['design'] == d and int(r['n']) == n]
    med = lambda c: float(np.median([float(r[c]) for r in rs]))
    gap = max(abs(float(r['Delta_grid']) - float(r['Delta'])) for r in rs)
    pip = float(np.median([min(1.0, float(r['rho_bar_bound'])) + float(r['u_pi']) for r in rs]))
    out.append(f"| {d} | {n} | {len(rs)} | {med('one_minus_pi0'):.2e} | {med('delta1'):.2e} | {med('Delta'):.2e} | "
               f"{gap:.1e} | {med('T_ideal'):.0f} | {med('P1_Tideal'):.2e} | {med('P1_Tmax'):.2e} | {pip:.2e} | "
               f"{med('P2'):.2e} | {np.mean([int(r['S0_is_HPM']) for r in rs]):.2f} | "
               f"{np.mean([int(r['S0_is_start_mode']) for r in rs]):.2f} |")
open(os.path.join(here, 'premise_summary.md'), 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))
