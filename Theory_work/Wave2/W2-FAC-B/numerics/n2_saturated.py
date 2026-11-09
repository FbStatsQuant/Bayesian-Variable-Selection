"""N2: saturated start (p > K = n/2), exact-Gram equicorrelated/one-factor design, aligned truth signs.
usage: python n2_saturated.py r n p c seed"""
import sys, json, math, time, numpy as np
import bvs_core as bc, fac_core as fc
r, n, p, c, seed = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
Sigma, Lam, Psi = fc.factor_sigma(p, math.sqrt(r) * np.ones(p), (1 - r) * np.ones(p))
th = np.zeros(p); S0 = (2, 26, 53, 75); th[list(S0)] = c * np.array([1.4, 1.0, 1.8, 1.2])
rng = np.random.default_rng(seed)
P = fc.ExactGram(Sigma, th, n, rng, Lam=Lam, Psi=Psi)
B = bc.block_size(n, p); blocks = bc.partition_from_corr(Sigma, B)
t0 = time.time(); info = bc.start_mode(P, blocks); St = info.mode
print(json.dumps(dict(n=n, p=p, K=P.K, B=B, start=len(St), has_S0=set(S0) <= set(St), t=round(time.time()-t0,1))), flush=True)
moves = []
def rec(P, T, sc, inf):
    if len(moves) % 25 == 0 or inf.get("move", "").startswith("sw") is False:
        pass
out = fc.ls0_path(P, St, S0, max_moves=5000)
mv = [s.get("move") for s in out["steps"] if "move" in s]
from collections import Counter
cnt = Counter(mv)
first_del = next((i for i, m in enumerate(mv) if m == "-N"), None)
print(json.dumps(dict(moves=out["moves"], counts=cnt, final_is_S0=out["final"] == tuple(sorted(S0)), symdiff=len(set(St) ^ set(S0)),
                      cap_MR1=bc.ell_cap(n, p) + len(St), excess=out["moves"] - len(set(St) ^ set(S0)), first_del_at=first_del,
                      prefix=mv[:40], t=round(time.time()-t0,1))), flush=True)
