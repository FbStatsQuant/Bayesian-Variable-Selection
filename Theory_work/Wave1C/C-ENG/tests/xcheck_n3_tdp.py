"""xcheck_n3_tdp.py -- compare the new core's start_mode (cap 1 => TDP-E fallback; cap 1e6 => enumeration) with W1-N3's
exact-arithmetic reference TDP (Theory_work/Wave1/W1-N3/numerics/tdp.py) on integer tables exported by xcheck_n3_tdp.R.
Usage: python xcheck_n3_tdp.py <instances.json> <out.txt>
"""
import json, os, sys
N3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "Wave1", "W1-N3", "numerics")
sys.path.insert(0, os.path.abspath(N3))
from n3lib import Inst  # noqa: E402
from tdp import tdp     # noqa: E402

inst = json.load(open(sys.argv[1]))
bad1 = bad6 = badv = 0
for k, d in enumerate(inst):
    rho = [{c: v for c, v in enumerate(b)} for b in d["rho"]]
    I = Inst(d["p"], d["K"], [list(b) for b in d["blocks"]], list(d["lam"]), rho, 10**6, "x%d" % k)
    V, kstar, S = tdp(I)
    if list(d["new_cap1"]) != list(S): bad1 += 1
    if list(d["new_cap1e6"]) != list(S): bad6 += 1
    if float(V) != float(d["lg0"]): badv += 1
lines = ["W1-N3 reference TDP (exact) vs new core start_mode on %d integer-table instances" % len(inst),
         "  cap 2 (TDP-E fallback when |E| >= 2) != reference S*: %d" % bad1,
         "  cap 1e6 (enumeration)   != reference S*: %d" % bad6,
         "  lg0 != reference V*: %d" % badv]
open(sys.argv[2], "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
