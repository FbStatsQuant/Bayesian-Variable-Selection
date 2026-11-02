"""Summarise results/realised_T.jsonl -> results/realised_T_summary.md (per design x n: counts of realised T, medians)."""
import json, sys, os, collections
import numpy as np
here = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results')
rows = [json.loads(l) for l in open(os.path.join(here, 'realised_T.jsonl')) if l.strip()]
g = collections.defaultdict(list)
for r in rows: g[(r['design'], r['n'])].append(r)
order = ['fav_iid', 'fav_cor', 'orth', 'masked']
L = ['| design | n | runs | H | T_V values (count) | T_full values | N_pilot values | bisect_V max | S0∈V | med Δ_n | med (T_V+1)Δ_n | (T_e+1)Δ_n | med χ²(π‖π₀) | med R(0) | med R(2) | η* (min / med; - = R(0)>ε₀) | Thm G bound holds | max bound_G | Lemma P holds | med D̄ | max bound_P |',
     '|' + '---|' * 21]
viol = []
for des in order:
    for n in sorted({k[1] for k in g if k[0] == des}):
        rs = g[(des, n)]
        cT = collections.Counter(r['T_V'] for r in rs); cF = collections.Counter(r['T_full'] for r in rs)
        cP = collections.Counter(r['N_pilot'] for r in rs)
        fmt = lambda c: ', '.join(f'{k}({v})' for k, v in sorted(c.items(), key=lambda kv: (kv[0] is None, kv[0] or 0)))
        etas = [r['eta_star'] for r in rs if r['eta_star'] is not None]
        okG = [r for r in rs if r['eta_star'] and r['S0_in_V'] and r['T_V'] is not None]
        holdsG = all(r['T_V'] <= r['bound_G'] and r['T_full'] <= r['bound_G'] for r in okG)
        for r in okG:
            if r['T_V'] > r['bound_G']: viol.append(('G', r))
        holdsP = all(r['lemmaP_ok'] and r['N_pilot'] <= r['bound_P'] for r in rs)
        for r in rs:
            if not (r['lemmaP_ok'] and r['N_pilot'] <= r['bound_P']): viol.append(('P', r))
        med = lambda k: float(np.median([r[k] for r in rs if r.get(k) is not None])) if any(r.get(k) is not None for r in rs) else float('nan')
        L.append(f"| {des} | {n} | {len(rs)} | {rs[0]['H']} | {fmt(cT)} | {fmt(cF)} | {fmt(cP)} | {max(r['bisect_V'] for r in rs)} | "
                 f"{sum(r['S0_in_V'] for r in rs)}/{len(rs)} | {med('Delta'):.3g} | {med('P1_TV'):.3g} | {med('P1_Te'):.3g} | "
                 f"{med('chi2_pi_pi0'):.3g} | {med('R0'):.3g} | {med('R2'):.3g} | "
                 f"{(f'{min(etas):.2f} / {np.median(etas):.2f}' if etas else '-')} ({len(etas)}/{len(rs)}) | "
                 f"{'yes' if holdsG else 'NO'} ({len(okG)} applicable) | {max([r['bound_G'] for r in okG], default='-')} | "
                 f"{'yes' if holdsP else 'NO'} | {med('Dbar'):.3g} | {max(r['bound_P'] for r in rs)} |")
allT = collections.Counter(r['T_V'] for r in rows if r['design'] != 'masked')
L.append(f"\nFavourable designs (fav_iid, fav_cor, orth), all n: realised T_V counts {dict(allT)}; runs {sum(allT.values())}.")
L.append(f"Violations of Theorem G / Lemma P: {len(viol)}" + ''.join(f"\n- {k}: {r['design']} n={r['n']} seed={r['seed']}" for k, r in viol))
open(os.path.join(here, 'realised_T_summary.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
