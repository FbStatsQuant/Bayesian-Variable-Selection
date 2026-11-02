"""Summarise ../results/prod_scale.json (output of prod_scale.py) per (scenario, c) and overall."""
import json, sys
from collections import defaultdict

res = json.load(open(sys.argv[1] if len(sys.argv) > 1 else '../results/prod_scale.json'))
cells = defaultdict(list)
for r in res:
    cells[(r['scen'], r['c'])].append(r)
print('| scen | c | N | S0 locmax | R20: M(S) progress frac | R20 lit-TD1 frac | centres | E_LS | reached | reached given E_LS | not reached & E_LS & end >= S0 | all-progress given reached | max moves | limit |')
print('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
tot = defaultdict(int)
for k in sorted(cells):
    rs = cells[k]; N = len(rs)
    lm = sum(r['S0_locmax'] for r in rs)
    prog = sum(v for r in rs for c, v in r['R20_classes'].items() if c in ('add_truth', 'swap_x->t', 'del_extra'))
    allc = sum(v for r in rs for v in r['R20_classes'].values())
    td1 = sum(r['R20_litTD1'] for r in rs)
    C = [c for r in rs for c in r['centres']]
    els = [c for c in C if c['ELS']]
    rch = [c for c in C if c['reached']]
    pat = [c for c in C if (not c['reached']) and c['ELS'] and c['end_minus_S0'] >= 0]
    ap = sum(c['allprog'] for c in rch)
    print('| %d | %.1f | %d | %d/%d | %.3f | %.3f | %d | %.3f | %.3f | %.3f | %d | %s | %d | %d |' % (
        k[0], k[1], N, lm, N, prog / allc, td1 / allc, len(C), len(els) / len(C), len(rch) / len(C),
        (sum(c['reached'] for c in els) / len(els)) if els else float('nan'), len(pat),
        ('%.3f' % (ap / len(rch))) if rch else '-', max(c['moves'] for c in C), sum(c['limit'] for c in C)))
    for key, val in (('N', N), ('lm', lm), ('C', len(C)), ('els', len(els)), ('rch', len(rch)), ('pat', len(pat)), ('ap', ap),
                     ('lm_C', sum(len(r['centres']) for r in rs if r['S0_locmax'])),
                     ('lm_rch', sum(c['reached'] for r in rs if r['S0_locmax'] for c in r['centres'])),
                     ('nlm_rch', sum(c['reached'] for r in rs if not r['S0_locmax'] for c in r['centres'])),
                     ('nonimp', sum(r['R20_litTD1_nonimproving'] for r in rs))):
        tot[key] += val
print()
print('overall:', dict(tot))
print('centres reached S0 when S0 IS a local max: %d/%d; when S0 is NOT a local max: %d/%d' % (
    tot['lm_rch'], tot['lm_C'], tot['nlm_rch'], tot['C'] - tot['lm_C']))
print('CEX-2 pattern (E_LS held, search ended at a model >= S0, not S0): %d of %d centres' % (tot['pat'], tot['C']))
