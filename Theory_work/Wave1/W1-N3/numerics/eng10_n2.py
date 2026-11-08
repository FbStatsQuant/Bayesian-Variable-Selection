"""eng10_n2.py -- n = 2 boundary (ENG10 companion): the full coded pipeline data_init -> make_blocks(B = 1) ->
build_tables -> build_start -> start_mode at n = 2 (K = min(p,1) = 1), p = 1..12, against brute force.
Note: production preprocessing rejects n < 3 (v3_preprocess.R:106); this exercises the start-mode routine only."""
import os, sys, random, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n3lib import run_data, predict, ghat, all_sets
rng = random.Random(2)
def standardise(v):
    n = len(v); mu = sum(v) / n; c = [x - mu for x in v]; ss = math.sqrt(sum(x * x for x in c) / (n - 1)); return [x / ss for x in c]
cases = []
for p in range(1, 13):
    for rep in range(3):
        cols = [standardise([rng.gauss(0, 1), rng.gauss(0, 1)]) for _ in range(p)]
        y = standardise([rng.gauss(0, 1), rng.gauss(0, 1)])
        cases.append((f"n2-p{p}-r{rep}", 2, p, 1, 10**6, [v for c in cols for v in c], y))
ok = 0
for I, R in run_data(cases):
    P = predict(I)
    singles = sorted(set(I.rho[b][1] for b in range(len(I.blocks))))
    good = (R["S"] == P["Sstar"] == P["S"]) and R["ties"] == P["ties"] and R["truncated"] == 0
    ok += good
    print(I.iid, "K=%d J=%d" % (I.K, len(I.blocks)), "distinct singleton log r:", [float.hex(s) for s in singles],
          "lambda(1)-lambda(0)=%.6f" % (I.lam[1] - I.lam[0]), "code S:", R["S"], "ties:", R["ties"], "S*:", P["Sstar"], "OK" if good else "FAIL")
print("OK", ok, "of", len(cases))
