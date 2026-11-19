#!/usr/bin/env python3
"""Read-only: single-pair I_max=0 (VF) / I_max=3 (overlap V) ratios of M1-M3 at 10^4, R'=16, same data + same engine seed (GB_PLAN operating-characteristics input)."""
import glob, json, math, os, re, sys
R = os.path.expanduser("~/SMC_Engineering_Department/records")
def ev(dp):
    for n in ("eval.bin.json", "eval.json"):
        p = os.path.join(dp, n)
        if os.path.isfile(p):
            return json.load(open(p))
def met(e):
    fm = e["fit"]["meta"]
    m1 = next(x["sd_log_Z_occ_r"] for x in fm["occ"] if x["M"] == 1000)
    return (m1, e["pip"]["island_spread"]["max_sd"], e["evidence"]["sigma_hat"], tuple(e["selection"]["hpm"]), len(e["evidence"]["logZ_r"]))
vf = sorted(glob.glob(R + "/precision1e4/S*/4-*-VF-s?"))
rows = []
for d in vf:
    rid = os.path.basename(d); base = rid.replace("-VF-", "-V-")
    cands = [p for p in glob.glob(R + "/overlap1e4/W*/" + base) if os.path.isdir(p)]
    if not cands: print("NO PARTNER", rid); continue
    a, b = met(ev(d)), met(ev(cands[0]))
    rows.append((rid, a, b))
print("pairs", len(rows))
lr = [[], [], []]
for rid, a, b in rows:
    r = [a[i] / b[i] for i in range(3)]
    for i in range(3): lr[i].append(math.log(r[i]))
    print("%-28s R'=%d/%d HPMsame=%s  r(M1,M2,M3)= %.3f %.3f %.3f   I0: %.4f %.5f %.4f  I3: %.4f %.5f %.4f" % (rid, a[4], b[4], a[3] == b[3], *r, a[0], a[1], a[2], b[0], b[1], b[2]))
n = len(rows)
for i, nm in enumerate(("M1", "M2", "M3")):
    x = lr[i]; mu = sum(x) / n; sd = (sum((v - mu) ** 2 for v in x) / (n - 1)) ** .5
    print(nm, "gmean r %.3f  sd(log r) %.3f  frac r<=1.15 %.2f  frac r<=1.30 %.2f" % (math.exp(mu), sd, sum(v <= math.log(1.15) for v in x) / n, sum(v <= math.log(1.30) for v in x) / n))
ok15 = sum(all(lr[i][k] <= math.log(1.15) for i in range(3)) for k in range(n)); ok30 = sum(all(lr[i][k] <= math.log(1.30) for i in range(3)) for k in range(n))
print("all three <=1.15: %d/%d ; all three <=1.30: %d/%d" % (ok15, n, ok30, n))
