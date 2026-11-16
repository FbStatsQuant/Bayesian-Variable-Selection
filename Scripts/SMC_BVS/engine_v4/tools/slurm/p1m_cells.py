#!/usr/bin/env python3
"""p1m_cells.py -- the executable cell/seed manifest (Sol F7; REVIEW_disposition_sol F3/F7) for the P1M experiment.

One table of CELLS (below) is the single source. This tool expands it into one row per fit (run id, seeds, mode, N,
islands, planning cost) and into Slurm-driver plans (p1m_driver.py) grouped into batches of <= 150 tasks with one
resource shape each. Docs/Experiments/P1M/MANIFEST_CELLS.md documents the same table and the totals this tool prints.

  p1m_cells.py --tsv fits.tsv [--plans DIR] [--only RUNG]     (writes files; never submits)
  p1m_cells.py --summary                                       (cost per rung / block, PLANNING VALUES)

Seed rule (deterministic, collision-free, all < 2^31 - 1):
  data_seed   = R * 10^8 + D * 10^6 + (n / 100) * 10^4 + rep           R = log10 p (3 = the 5k anchor / exact block)
  engine seed = data_seed (seed 1), data_seed + 50 (seed 2, same data)  D: 1 IND, 2 AR-strong, 3 AR-weak, 4 BLK,
  calibration seed (precision study) = data_seed + 70 + c                  5 ADJ-OPP, 6 NULL
Costs are PLANNING VALUES (ENGINEERING_SPEC §0-v2.5 and the owner sheet; n-scaling c(n) = 3 c_s + 30 ns,
c_s = 30 + 60 n/200 ns), replaced after the SPR sweep and gate T5 by measured core-h per fit.
"""
import argparse
import json
import os
import sys
from collections import OrderedDict

DESIGN_CODE = {"IND": 1, "AR": 2, "AR-weak": 3, "BLK": 4, "ADJ-OPP": 5, "NULL": 6}
# planning core-h per fit at n = 200 (V = V-1M class A, precise; T = theory mode in the new engine, law mode, bit form)
COST_V = {4: 10.0, 5: 96.0, 6: 963.0}
COST_T = {4: 115.0, 5: 6100.0}          # 10⁴: upper end of 52–115 (escalating coded calibration)
COST_V_N1E4 = {6: 3600.0}               # the 1M N = 10⁴ doubling fit
COST_6_BY_N = {200: 963.0, 500: 1800.0, 1000: 3300.0}   # owner sheet option D


def n_factor(n):
    c = lambda m: 3 * (30 + 60 * m / 200.0) + 30
    return c(n) / c(200)


def fit_cost(rung, n, mode, N=2500, islands=16):
    if rung == 6 and mode == "V" and N == 10000:
        return COST_V_N1E4[6]
    if rung == 6:
        return COST_6_BY_N.get(n, COST_V[6] * n_factor(n))
    base = (COST_T if mode == "law" else COST_V)[rung] * n_factor(n)
    # a fit = R′ islands + ≈ 3 island-equivalents of bounded calibration (19 for R′ = 16; OD-2); both scale with N
    return base * (N / 2500.0) * ((islands + 3) / 19.0)


# CELLS: (block, rung, design, n, reps, arms, note). arms: list of dicts {mode, seeds, N, islands, params, tag}.
V1 = [{"mode": "V", "seeds": 1, "tag": "V"}]
V2 = [{"mode": "V", "seeds": 2, "tag": "V"}]                        # seed 1 + seed 2 on the same data
TV2 = [{"mode": "law", "seeds": 2, "tag": "T"}, {"mode": "V", "seeds": 2, "tag": "V"}]
PREC = [{"mode": "V", "seeds": 1, "N": N, "islands": 64, "params": {"grid_refine_m": m, "calib_seed_index": c},
         "tag": "P-N%d-m%d-c%d" % (N, m, c)} for N in (2500, 10000) for m in (1, 4) for c in (1, 2)]
CELLS = [
    # --- exact reference T8 (p <= 25; SMC branch forced; 400 islands per fixture): costed as a block, not per fit
    ("T8 exact", 1, "AR", 200, 20, [{"mode": "V", "seeds": 1, "tag": "T8", "fixed_cost": 2.5}], "20 fixtures x 400 islands (< 50 core-h)"),
    # --- 10⁴ overlap (§0-v2.7): T (law mode) vs V, 2 seeds each, the same 10 datasets
    ("overlap 1e4", 4, "AR", 200, 4, TV2, "AR-strong"),
    ("overlap 1e4", 4, "AR-weak", 200, 2, TV2, "AR-weak (a = 0.6)"),
    ("overlap 1e4", 4, "ADJ-OPP", 200, 2, TV2, "ADJ-OPP (WP1 layout)"),
    ("overlap 1e4", 4, "IND", 200, 1, TV2, ""),
    ("overlap 1e4", 4, "NULL", 200, 1, TV2, "a = 0"),
    # --- precision study (Sol F6, mandatory): 64 islands; N x grid refinement x 2 calibration seeds; 3 overlap datasets
    ("precision", 4, "AR", 200, 1, PREC, "on overlap dataset AR-strong rep 1"),
    ("precision", 4, "AR-weak", 200, 1, PREC, "on overlap dataset AR-weak rep 1"),
    ("precision", 4, "ADJ-OPP", 200, 1, PREC, "on overlap dataset ADJ-OPP rep 1"),
    # --- 10⁴ science (n-trend, designs, null, ablations, second seed, partition)
    ("science 1e4", 4, "AR", 100, 10, V1, ""), ("science 1e4", 4, "AR", 200, 10, V2, "second seed on all 10"),
    ("science 1e4", 4, "AR", 400, 10, V1, ""), ("science 1e4", 4, "AR", 800, 10, V1, ""),
    ("science 1e4", 4, "AR-weak", 100, 20, V1, ""), ("science 1e4", 4, "AR-weak", 200, 20, V1, ""),
    ("science 1e4", 4, "AR-weak", 400, 10, V1, ""), ("science 1e4", 4, "AR-weak", 800, 10, V1, ""),
    ("science 1e4", 4, "IND", 100, 5, V1, ""), ("science 1e4", 4, "IND", 200, 5, V1, ""), ("science 1e4", 4, "IND", 400, 5, V1, ""),
    ("science 1e4", 4, "BLK", 100, 5, V1, ""), ("science 1e4", 4, "BLK", 200, 5, V1, ""), ("science 1e4", 4, "BLK", 400, 5, V1, ""),
    ("science 1e4", 4, "ADJ-OPP", 200, 5, V1, "mandatory (Sol F7)"), ("science 1e4", 4, "ADJ-OPP", 400, 5, V1, "mandatory (Sol F7)"),
    ("science 1e4", 4, "NULL", 200, 5, V1, "null control"),
    ("science 1e4", 4, "AR", 200, 10, [{"mode": "V", "seeds": 1, "tag": "A3-exactlink", "params": {"partition": "exact_linkage"}}],
     "A3: exact complete linkage vs the 1M rule on the same data (AR)"),
    ("science 1e4", 4, "BLK", 200, 10, [{"mode": "V", "seeds": 1, "tag": "A3-exactlink", "params": {"partition": "exact_linkage"}}],
     "A3: exact complete linkage vs the 1M rule on the same data (BLK)"),
    # --- 10⁵ rung (12 fits)
    ("rung 1e5", 5, "AR", 200, 5, V1, "n-trend; pi(S0) trend gates option D"), ("rung 1e5", 5, "AR", 400, 3, V1, "n-trend"),
    ("rung 1e5", 5, "IND", 200, 2, V1, ""), ("rung 1e5", 5, "ADJ-OPP", 200, 2, V1, "mandatory (Sol F7)"),
    # --- 10⁶ rung (OD-14 / D-10): rep 1 is the pilot (counts only if the frozen configuration is unchanged)
    ("rung 1e6", 6, "AR", 200, 3, V1, "rep 1 = pilot"), ("rung 1e6", 6, "ADJ-OPP", 200, 1, V1, ""),
    ("rung 1e6", 6, "AR-weak", 200, 1, V1, ""),
    ("rung 1e6", 6, "AR", 200, 1, [{"mode": "V", "seeds": 1, "N": 10000, "tag": "N1e4"}], "self-check: N = 10⁴ on AR rep 1's data"),
    ("option D", 6, "AR", 1000, 1, V1, "conditional on the 10⁵ pi(S0) trend (H-1)"),
]
# block-level costs not expanded into fits (PLANNING VALUES; ENGINEERING_SPEC §0-v2.8 and REVIEW_disposition_sol)
FIXED = OrderedDict([
    ("gates + benchmarks (T1–T11 on NOTS, G0)", 400.0),
    ("T5 end-to-end NOTS gate (Sol F3)", 200.0),
    ("5k anchor (revision D unmodified vs new engine compat vs V; 20-seed law test at 2k)", 300.0),
    ("ablations (start mode / + LS0 / pilot + local) once per distinct 10⁴–10⁶ dataset (ESTIMATE 6% of its V fit)", None),   # computed
    ("competitors (all rungs) + acceptance runs (Sol F8)", 400.0),
])
OPTIONAL = [("1M second seed on AR rep 1 (Sol F7: named, NOT in A + D)", 963.0)]
CONTINGENCY = 0.25


def expand():
    """One row per distinct fit. A fit that two blocks name (same data seed, mode, arm and engine seed; e.g. an overlap
    dataset that is also a 10⁴-science replicate) is run once, costed to the first block, and noted in the second."""
    rows = []; seen = {}
    for block, rung, design, n, reps, arms, note in CELLS:
        dcode = DESIGN_CODE[design]
        for rep in range(1, reps + 1):
            data_seed = rung * 10**8 + dcode * 10**6 + (n // 100) * 10**4 + rep
            for arm in arms:
                for s in range(1, arm.get("seeds", 1) + 1):
                    N = arm.get("N", 2500); isl = arm.get("islands", 16)
                    cost = arm["fixed_cost"] if "fixed_cost" in arm else fit_cost(rung, n, arm["mode"], N, isl)
                    params = dict(arm.get("params") or {})
                    if "calib_seed_index" in params:
                        params["calib_seed"] = data_seed + 70 + params.pop("calib_seed_index")
                    p = 25 if rung == 1 else (5000 if rung == 3 else 10**rung)
                    gdesign = "AR" if design == "AR-weak" else design
                    signal = "weak" if design == "AR-weak" else ("null" if design == "NULL" else "strong")
                    rid = "%s-%s-n%d-r%02d-%s-s%d" % ({1: "x", 4: "4", 5: "5", 6: "6"}[rung], design.replace("-", ""), n, rep, arm["tag"], s)
                    if rid in seen:
                        seen[rid]["note"] = (seen[rid]["note"] + "; " if seen[rid]["note"] else "") + "also " + block
                        continue
                    rows.append(OrderedDict([
                        ("block", block), ("run_id", rid), ("p", p), ("design", gdesign), ("signal", signal), ("n", n), ("rep", rep),
                        ("mode", arm["mode"]), ("N", N), ("Rp", isl), ("data_seed", data_seed),
                        ("seed", data_seed + (50 if s == 2 else 0)), ("params", json.dumps(params, sort_keys=True)),
                        ("core_h_planning", round(cost, 1)), ("note", note)]))
                    seen[rid] = rows[-1]
    ids = [r["run_id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate run ids"
    for r in rows:
        assert 1 <= r["seed"] <= 2**31 - 1 and 1 <= r["data_seed"] <= 2**31 - 1
    return rows


def summary(rows):
    blocks = OrderedDict()
    for r in rows:
        b = blocks.setdefault(r["block"], {"fits": 0, "core_h": 0.0})
        b["fits"] += 1; b["core_h"] += r["core_h_planning"]
    fixed = OrderedDict(FIXED)
    ds = {}
    for r in rows:   # one ablation set per distinct dataset (data seed), costed at 6% of a V fit there (pilot ≈ 1/19, setup shared)
        if r["block"] in ("T8 exact", "option D", "precision") or r["mode"] != "V" or r["Rp"] != 16 or r["N"] != 2500:
            continue
        ds[r["data_seed"]] = r["core_h_planning"]
    fixed["ablations (start mode / + LS0 / pilot + local) once per distinct 10⁴–10⁶ dataset (ESTIMATE 6% of its V fit)"] = round(0.06 * sum(ds.values()), 1)
    planned = sum(v["core_h"] for k, v in blocks.items() if k != "option D") + sum(fixed.values())
    d = blocks.get("option D", {"core_h": 0.0})["core_h"]
    return blocks, fixed, planned, d


def plans(rows, outdir, only=None):
    """Driver plans: one per (block, p, n, mode, N, Rp) group, split so that each batch has <= 150 tasks."""
    os.makedirs(outdir, exist_ok=True)
    groups = OrderedDict()
    for r in rows:
        if r["block"] == "T8 exact" or (only and str(r["p"]) != str(only)):
            continue
        key = (r["block"], r["p"], r["n"], r["mode"], r["N"], r["Rp"])
        groups.setdefault(key, []).append(r)
    written = []
    for (block, p, n, mode, N, Rp), rs in groups.items():
        per_fit = 4 + Rp
        cap = max(1, 150 // per_fit)
        for b in range(0, len(rs), cap):
            chunk = rs[b:b + cap]
            name = "%s_p%d_n%d_%s_N%d_R%d_b%d" % (block.replace(" ", "").replace("⁴", "4").replace("⁵", "5").replace("⁶", "6"), p, n, mode, N, Rp, b // cap + 1)
            plan = {"batch": name[:64], "mode": mode, "code_commit": "UNSET-fill-at-freeze", "max_task_hours": 2.0,
                    "kind": "gated (needs HQ go)", "fits": []}
            for r in chunk:
                f = {"run_id": r["run_id"], "design": "NULL" if r["signal"] == "null" else r["design"], "p": r["p"], "n": r["n"],
                     "signal": r["signal"], "data_seed": r["data_seed"], "seed": r["seed"], "Rp": r["Rp"], "N": r["N"]}
                pr = json.loads(r["params"])
                if pr:
                    f["params"] = pr
                plan["fits"].append(f)
            path = os.path.join(outdir, name[:64] + ".json")
            with open(path, "w") as fh:
                json.dump(plan, fh, indent=1)
            written.append(path)
    return written


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tsv"); ap.add_argument("--plans"); ap.add_argument("--only"); ap.add_argument("--summary", action="store_true")
    a = ap.parse_args(argv)
    rows = expand()
    if a.tsv:
        with open(a.tsv, "w") as fh:
            fh.write("\t".join(rows[0].keys()) + "\n")
            for r in rows:
                fh.write("\t".join(str(v) for v in r.values()) + "\n")
    if a.plans:
        w = plans(rows, a.plans, a.only)
        print("wrote %d driver plans to %s" % (len(w), a.plans))
    if a.summary or not (a.tsv or a.plans):
        blocks, fixed, planned, d = summary(rows)
        print("%-14s %6s %10s" % ("block", "fits", "core-h"))
        for k, v in blocks.items():
            print("%-14s %6d %10.0f" % (k, v["fits"], v["core_h"]))
        for k, v in fixed.items():
            print("  + %-88s %8.0f" % (k, v))
        print("planned (excl. option D): %.0f; with %d%% contingency: %.0f" % (planned, CONTINGENCY * 100, planned * (1 + CONTINGENCY)))
        print("option D: %.0f; with contingency: %.0f" % (d, d * (1 + CONTINGENCY)))
        print("A + D with contingency: %.0f (H-1 envelope ~24.6k)" % ((planned + d) * (1 + CONTINGENCY)))
        for k, v in OPTIONAL:
            print("optional, not in the total: %s %.0f" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
