"""R06 scratch: classify the 3 jstar/cs_core mismatches as float near-ties. Writes only l3_neartie_out.json."""
import sys, json
sys.dont_write_bytecode = True
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np
import l3_diag as L
rows = []
for n, c, s0, seed in [(2000, .9, 2, 1), (2000, .98, 1, 3), (2000, .98, 2, 1)]:
    p = int(c * n); th = np.zeros(p); th[:s0] = 1
    P = L.cs.CS(.5, th, n, rng=np.random.default_rng(seed)); S = L.singleton_start(P)
    res = L.my_phase(P, S); z, xi = P.z, P.xi
    inT = np.zeros(p, bool); inT[list(S)] = True
    for r in res['rec']:
        if 'jo' not in r: break
        k = int(inT.sum()); A = float(z[inT] @ z[inT]); B = float(z[inT].sum()); FT = float(P.F_stats(k, A, B))
        if not r['jstar_matches']:
            li = r['li']; cand = np.flatnonzero(inT & (np.arange(p) >= s0))
            Fv = P.F_stats(np.full(len(cand), k), A - z[cand] ** 2 + z[li] ** 2, B - z[cand] + z[li])
            gam = P.be / (P.al + k * P.be); tgt = gam * (xi[li] - r['xT']) / (1 + gam)
            dist = np.abs(xi[cand] - r['xT'] - tgt); jstar = int(cand[np.argmin(dist)])
            Fch = float(Fv[list(cand).index(r['jo'])]); Fjs = float(Fv[list(cand).index(jstar)])
            rows.append(dict(case=[n, c, s0, seed], step=r['step'], chosen=r['jo'], jstar=jstar,
                             F_chosen_minus_jstar=Fch - Fjs, gain=Fch - FT, xi_chosen=float(xi[r['jo']]), xi_jstar=float(xi[jstar]),
                             dist_chosen=float(dist[list(cand).index(r['jo'])]), dist_jstar=float(dist.min())))
        inT[r['jo']] = False; inT[r['li']] = True
(HERE / 'l3_neartie_out.json').write_text(json.dumps(rows, indent=1), encoding='utf8')
for r in rows: print(r)
