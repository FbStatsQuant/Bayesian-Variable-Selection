"""Summarise results/raw/*.jsonl into results/masked_sim.jsonl (concatenation) and results/summary.md (tables).
Deterministic (no randomness). Usage: python summarize.py
Split definition used in the tables: island with W_r < 0.05 (log W_r < log 0.05 = -3.00) AND island PIP error < 0.10.
"""
import os, json, glob
import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
res = os.path.join(here, '..', 'results')
files = sorted(glob.glob(os.path.join(res, 'raw', '*.jsonl')))
order = {('masked', 'G1'): 0, ('masked', 'G2'): 1, ('masked', 'G3'): 2, ('masked8', 'G1'): 3, ('masked8', 'G2'): 4,
         ('masked8', 'G3'): 5}
rows = []
with open(os.path.join(res, 'masked_sim.jsonl'), 'w') as out:
    for fn in files:
        lines = [json.loads(l) for l in open(fn) if l.strip()]
        if not lines:
            continue
        st = lines[0]; isl = [l for l in lines[1:] if l['kind'] == 'island']
        for l in lines:
            out.write(json.dumps(l) + '\n')
        if not isl:
            continue
        lW = np.array([x['logW'] for x in isl]); W = np.exp(lW)
        f = np.array([x['f'] for x in isl]); err = np.array([x['err'] for x in isl])
        Bb = np.array([x['Bbar'] for x in isl]); g = np.array([x['g'] for x in isl])
        reps = sorted(set(x['rep'] for x in isl))
        prim = np.array([[x for x in isl if x['rep'] == r][0]['primary_err'] for r in reps])
        mpm = np.array([[x for x in isl if x['rep'] == r][0]['mpm_correct'] for r in reps])
        d1, u, rb = st['delta1'], st['u_pi'], st['rho_bar']
        I1 = float(np.mean(W * (f > 0.5)))
        I3 = float(np.mean(W * err))
        I2 = float(np.max(err - (Bb + u)))
        split = int(np.sum((W < 0.05) & (err < 0.10)))
        rows.append(dict(key=(order.get((st['design'], st['grid_name']), 9), st['n'], -st['N']), design=st['design'],
                         n=st['n'], N=st['N'], grid=st['grid_name'], T=st['T'], reps=len(reps), islands=len(isl),
                         d1=d1, u=u, rb=rb, pi0=st['pi0_S0'], exerr=st['exact_pip_err'],
                         lWm=lW.mean(), q05=np.quantile(lW, .05), q50=np.quantile(lW, .5), q95=np.quantile(lW, .95),
                         Wm=W.mean(), fcross=np.mean(f > 0.5), fm=f.mean(), gm=g.mean(), err=err.mean(),
                         prim=prim.mean(), mpm=mpm.mean(), Bb=Bb.mean(), I1=I1, I1b=2 * d1, I3=I3, I3b=d1 + rb + u,
                         I2=I2, split=split, grid_list=st['grid'],
                         extra={k: st[k] for k in ('V_size', 'S0_in_V', 'V_has_x3') if k in st}))
rows.sort(key=lambda r: r['key'])


def fm(x, k=3):
    return f'{x:.{k}g}' if isinstance(x, float) else str(x)


L = []
L.append('### Table A: setting constants\n')
L.append('| design | n | N | grid | T | reps (islands) | delta1 | u_pi | rhobar | pi0(S0) | exact PIP err | G3 pilot |')
L.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
for r in rows:
    L.append(f"| {r['design']} | {r['n']} | {r['N']} | {r['grid']} | {r['T']} | {r['reps']} ({r['islands']}) | "
             f"{r['d1']:.4g} | {r['u']:.4g} | {r['rb']:.4g} | {r['pi0']:.3g} | {r['exerr']:.4g} | {r['extra'] or ''} |")
L.append('\n### Table B: evidence ratio and occupancy\n')
L.append('| design | n | N | grid | T | mean log W | q05 | q50 | q95 | mean W | frac f_r>1/2 | mean f_r | mean outside at measured-round starts | mean Bbar |')
L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for r in rows:
    L.append(f"| {r['design']} | {r['n']} | {r['N']} | {r['grid']} | {r['T']} | {r['lWm']:.3g} | {r['q05']:.3g} | "
             f"{r['q50']:.3g} | {r['q95']:.3g} | {r['Wm']:.3g} | {r['fcross']:.3g} | {r['fm']:.3g} | {r['gm']:.3g} | {r['Bb']:.3g} |")
L.append('\n### Table C: PIP accuracy and the three inequalities\n')
L.append('| design | n | N | grid | mean island PIP err | mean primary PIP err | MPM correct | (I1) E[W 1{f>1/2}] | 2 delta1 | (I3) E[W err] | delta1+rhobar+u_pi | (I2) max[err-(Bbar+u_pi)] | split islands (W<0.05, err<0.10) |')
L.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for r in rows:
    L.append(f"| {r['design']} | {r['n']} | {r['N']} | {r['grid']} | {r['err']:.4g} | {r['prim']:.4g} | {r['mpm']:.3g} | "
             f"{r['I1']:.4g} | {r['I1b']:.4g} | {r['I3']:.4g} | {r['I3b']:.4g} | {r['I2']:.3e} | {r['split']}/{r['islands']} |")
L.append('\n### Grids\n')
seen = set()
for r in rows:
    k = (r['design'], r['n'], r['grid'], tuple(r['grid_list']))
    if k in seen:
        continue
    seen.add(k)
    L.append(f"- {r['design']} n={r['n']} {r['grid']} (N={r['N']}): T={r['T']}, phi = "
             + ', '.join(f'{v:.4g}' for v in r['grid_list']))
open(os.path.join(res, 'summary.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
