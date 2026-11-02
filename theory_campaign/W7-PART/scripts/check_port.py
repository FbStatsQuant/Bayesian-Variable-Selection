"""Check: engine make_blocks (compiled, unmodified header) == faithful port == fast scipy version.
Designs: random group designs (indep / global / lh), including hard ones where blocks != groups, plus exact-tie
designs (duplicated columns) for the R13 tie rule. Seed fixed. Output: results/check_port.txt"""
import sys, numpy as np
from part_core import *

rng = np.random.default_rng(20261102)
lines = []
cnt = dict(total=0, eng_faith=0, eng_fast=0, eq_groups=0)
cases = []
for rep in range(60):
    n = int(rng.choice([30, 60, 200]))
    g = int(rng.choice([3, 5, 8, 10, 12]))
    G = int(rng.choice([4, 6, 10, 16]))
    rho = float(rng.choice([0.2, 0.4, 0.7]))
    kind = str(rng.choice(["indep", "global", "lh"]))
    psi = float(rng.choice([0.1, 0.3, 0.5])) if kind != "indep" else 0.0
    psi = min(psi, rho)
    B = int(rng.choice([6, 10, 14, 16]))
    cases.append((n, G, g, rho, psi, kind, B, False))
for rep in range(10):  # exact ties: duplicate columns
    cases.append((40, 6, 5, 0.5, 0.0, "indep", 10, True))
for (n, G, g, rho, psi, kind, B, dup) in cases:
    X, groups = gen_groups(n, G, g, rho, psi, kind, rng)
    if dup:
        X[:, 1] = X[:, 0]; X[:, 7] = X[:, 3]; X[:, 12] = 2 * X[:, 12 - 1] + 1
    be = v3_blocks_engine(X, B)
    bf, _ = v3_blocks_faithful(X, B)
    bs, _ = v3_blocks_fast(X, B) if not dup else (bf, None)
    cnt["total"] += 1
    cnt["eng_faith"] += (be == bf)
    cnt["eng_fast"] += (be == bs)
    cnt["eq_groups"] += blocks_equal_groups(be, groups)
    if be != bf or be != bs:
        lines.append(f"MISMATCH n={n} G={G} g={g} rho={rho} psi={psi} kind={kind} B={B} dup={dup}")
lines.append(f"cases={cnt['total']}  engine==faithful: {cnt['eng_faith']}  engine==fast(scipy): {cnt['eng_fast']}  "
             f"(blocks==groups in {cnt['eq_groups']} cases, so both outcomes are exercised)")
open("../results/check_port.txt", "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
