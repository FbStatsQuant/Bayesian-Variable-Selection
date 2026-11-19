#!/usr/bin/env python3
"""xeval self-check (B = truth) vs the engine's eval.bin.json dist.T.predictive.h2 for the 12 W3 fits (bit-exact comparison)."""
import json, glob, os
REC = os.path.expanduser("~/SMC_Engineering_Department/records/overlap1e4/W3"); here = os.path.dirname(os.path.abspath(__file__))
nb = 0; n = 0
for f in sorted(glob.glob(here + "/cross/selfchk_*.json")):
    base = os.path.basename(f)[len("selfchk_"):-5]  # 4-AR-n200-r02_T_s1
    ds, arm, s = base.rsplit("_", 2); run = "%s-%s-%s" % (ds, arm, s)
    x = json.load(open(f))["xeval"]["h2"]; e = json.load(open(os.path.join(REC, run, "eval.bin.json")))["dist"]["T"]["predictive"]["h2"]
    st = json.load(open(f))["status"]; n += 1; eq = (x == e); nb += eq
    print("%-28s status %s xeval %r engine %r %s%s" % (run, st, x, e, "BIT-EQUAL" if eq else "DIFFERENT", "" if eq else "  diff %.4e" % (x - e)))
print("%d of %d bit-equal" % (nb, n))
