"""R06 scratch: (a) tie check for the one all_jstar_match=False case; (b) n=4000 full-matrix rows (diag stopped at 1200 s).
Writes only l3_diag_tail_out.jsonl."""
import sys, json, math
sys.dont_write_bytecode = True
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import numpy as np
import l3_diag as L
out = (HERE / 'l3_diag_tail_out.jsonl').open('w', encoding='utf8')
# (a) n=2000,c=.98,s0=2,seed=1: at tie steps, is the square-completion minimiser among the tied maximisers?
n, c, s0, seed = 2000, .98, 2, 1
p = int(c * n); th = np.zeros(p); th[:s0] = 1
P = L.cs.CS(.5, th, n, rng=np.random.default_rng(seed)); S = L.singleton_start(P)
res = L.my_phase(P, S)
bad = [r for r in res['rec'] if 'jo' in r and not r['jstar_matches']]
chk = []
z, xi = P.z, P.xi
inT = np.zeros(p, bool); inT[list(S)] = True
for r in res['rec']:
    if 'jo' not in r: break
    if not r['jstar_matches']:
        k = int(inT.sum()); A = float(z[inT] @ z[inT]); B = float(z[inT].sum()); li = r['li']
        cand = np.flatnonzero(inT & (np.arange(p) >= s0))
        Fv = P.F_stats(np.full(len(cand), k), A - z[cand] ** 2 + z[li] ** 2, B - z[cand] + z[li])
        tied = set(cand[Fv == Fv.max()].tolist())
        gam = P.be / (P.al + k * P.be); tgt = gam * (xi[li] - r['xT']) / (1 + gam)
        dist = np.abs(xi[cand] - r['xT'] - tgt); jstar = int(cand[np.argmin(dist)])
        chk.append(dict(step=r['step'], chosen=r['jo'], jstar=jstar, n_tied=len(tied), jstar_in_tied=jstar in tied,
                        chosen_in_tied=r['jo'] in tied, dist_gap=float(np.sort(dist)[1] - np.sort(dist)[0])))
    inT[r['jo']] = False; inT[r['li']] = True
out.write(json.dumps(dict(tiecheck=chk, n_mismatch=len(bad))) + '\n'); out.flush(); print(chk, flush=True)
# (b) n=4000 rows
for c in (.6, .9, .98):
    for s0 in (1, 2):
        p = int(c * 4000); th = np.zeros(p); th[:s0] = 1
        P = L.cs.CS(.5, th, 4000, rng=np.random.default_rng(0)); S = L.singleton_start(P); res = L.my_phase(P, S)
        rec = res['rec']; sw = [r for r in rec if 'jo' in r]
        row = dict(n=4000, c=c, s0=s0, seed=0, W=res['W'], first_other=res['first_other'], reexport=res['reexport'],
                   M_min=min(r['M'] for r in rec), M_max=max(r['M'] for r in rec), max_drift=max(r['drift'] for r in rec),
                   min_best_null_del_over_logn=min(r['best_null_del_gain'] for r in rec) / math.log(4000),
                   max_truth_del_gain=max(r['truth_del_gain'] for r in rec), max_truth_out_swap_gain=max(r['truth_out_swap_gain'] for r in rec),
                   min_tau_l2_over_req=min(r['tau_l2'] / r['tau_l2_req'] for r in sw), max_abs_tau_j=max(abs(r['tau_j']) for r in sw),
                   all_jstar_match=all(r['jstar_matches'] for r in sw), any_swap_ties=any(r['nties'] > 1 for r in sw),
                   swap_gain_ge_null_del=all(r['best_swap_gain'] >= r['best_null_del_gain'] for r in sw))
        out.write(json.dumps(row) + '\n'); out.flush(); print(json.dumps(row), flush=True)
