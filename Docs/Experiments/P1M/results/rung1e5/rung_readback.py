#!/usr/bin/env python3
"""rung_readback.py -- the 10^5 RUNG read-back tables (RUNG_PLAN section 6): per-fit C1 cost / C2 precision / C3 memory / C4 completion / C5 flags (the registered gb_readback.py functions, imported
UNEDITED from ../gb/), with the C1 models of the RUNG class table (committed in RUNG_PLAN section 3), the G-C completion count (>= 11 of the 12 rung fits delivered) and the forced-kill restart (T6)
check. READ-ONLY, stdlib, deterministic.

  python3 -I rung_readback.py --records ROOT [ROOT ...] --cost-dir DIR [DIR ...] --out OUTDIR [--t6 t6.json] [--t6-ref-hash 0x4e4fd6a2e6135cfb]

C1 RUNG CLASS TABLE (core-h per fit; soft = max(3, 1.5 E), hard = max(3, 2.5 E); the hard line is never re-fitted; G-B measured AR 76.4 / ADJ-OPP 65.7 at N 10^4, I_max 0):
  (AR, n200, N10^4) 76 -> 114 / 190 | (ADJOPP, n200, N10^4) 66 -> 99 / 165 | (AR, n400, N10^4) 76 (1.0x, unmeasured at 10^5) -> 114 / 190 | (IND, n200, N10^4) 76 (1.0x AR, assumption) -> 114 / 190
  continuity twins (N 2,500, I_max 0): (AR, n200) 32 -> 48 / 80 | (ADJOPP, n200) 28 -> 42 / 70 | T6 restart test (N 10^4, one island at 48 CPUs): 12 -> 18 / 30.
RUNG PASS ITEMS: C1 per fit (OK / SOFT / HARD), C2 per fit (reported; a miss is a target miss, never an estimator switch), C3 (peak RSS < request in each of the 5 stages), C4, and the G-C items:
  completion >= 11 of 12 rung fits (the two G-B pilots count) and T6 PASS. T6 PASS = p1m_t6.py `ok` (every check true) AND the resumed island's output_hash == the uninterrupted reference's ==
  --t6-ref-hash (the G-B pilot's OWN island 1 of the same inputs, pre-declared 0x4e4fd6a2e6135cfb for source GB_G1a / `5-AR-n200-r01-V-s1`; omit the third equality for the fallback source RG_1a).
"""
import argparse, glob, importlib.util, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("gb_readback", os.path.join(os.path.dirname(HERE), "gb", "gb_readback.py"))
gbr = importlib.util.module_from_spec(spec); spec.loader.exec_module(gbr)

MODELS = {("AR", 200, 10000, 0): 76, ("ADJOPP", 200, 10000, 0): 66, ("AR", 400, 10000, 0): 76, ("IND", 200, 10000, 0): 76, ("AR", 200, 2500, 0): 32, ("ADJOPP", 200, 2500, 0): 28}
RUNG_IDS = (["5-AR-n200-r%02d-V-s1" % r for r in range(1, 6)] + ["5-AR-n400-r%02d-V-s1" % r for r in range(1, 4)] + ["5-IND-n200-r%02d-V-s1" % r for r in (1, 2)] + ["5-ADJOPP-n200-r%02d-V-s1" % r for r in (1, 2)])
T6_REF_HASH = "0x4e4fd6a2e6135cfb"


def c1(rid, rec, total):
    g = gbr.RUN.match(rid)
    key = (g["d"], int(g["n"]), rec["N"], rec["I"]) if (g and rec) else None
    E = MODELS.get(key)
    return {"billed": total, "model_E": E, "soft": (max(3.0, 1.5 * E) if E else None), "hard": (max(3.0, 2.5 * E) if E else None), "ratio": (total / E if (E and total is not None) else None),
            "verdict": ("NO_MODEL" if not E or total is None else ("OK" if total <= max(3.0, 1.5 * E) else ("SOFT" if total <= max(3.0, 2.5 * E) else "HARD")))}


def t6_check(path, ref_hash):
    j = json.load(open(path))
    fh, rh = (j.get("final") or {}).get("output_hash"), (j.get("reference") or {}).get("output_hash")
    out = {"p1m_t6_ok": bool(j.get("ok")), "checks": j.get("checks"), "kills": [{kk: k.get(kk) for kk in ("kill", "kind", "returncode", "killed", "island_file_exists")} for k in j.get("kills", [])],
           "resumed_from_step": (j.get("final") or {}).get("resumed_from_step"), "reference_wall_s": (j.get("reference") or {}).get("wall_s"), "final_wall_s": (j.get("final") or {}).get("wall_s"),
           "final_hash": fh, "reference_hash": rh, "expected_hash": ref_hash, "final_eq_reference": bool(fh and fh == rh), "final_eq_expected": (bool(fh and fh == ref_hash) if ref_hash else None)}
    out["PASS"] = bool(out["p1m_t6_ok"] and out["final_eq_reference"] and (out["final_eq_expected"] in (True, None)))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--records", nargs="+", required=True); ap.add_argument("--cost-dir", nargs="*", default=[]); ap.add_argument("--out", required=True)
    ap.add_argument("--t6", default=None); ap.add_argument("--t6-ref-hash", default=T6_REF_HASH)
    a = ap.parse_args(argv)
    runs = gbr.find(a.records, gbr.RUN)
    costs = {}
    for d in a.cost_dir:
        for p in glob.glob(os.path.join(d, "cost_*.json")):
            j = json.load(open(p))
            if "stages" in j:
                costs[j["run_id"]] = j
    rows = {}
    for rid, (dp, ev) in sorted(runs.items()):
        r = gbr.fit_row(rid, dp, ev, costs)
        r["C1"] = c1(rid, r["recorded_arm"], r["C1"]["billed"])
        rows[rid] = r
    deliv = [rid for rid in RUNG_IDS if rid in rows and all(rows[rid]["C4"].values()) and (rows[rid]["recorded_arm"] or {}).get("N") == 10000 and (rows[rid]["recorded_arm"] or {}).get("I") == 0]
    comp = {"rung_fits_delivered": len(deliv), "of": 12, "rule": ">= 11 of 12 (G-C: 10^5 >= 90 % complete)", "PASS": len(deliv) >= 11, "missing": [x for x in RUNG_IDS if x not in deliv]}
    t6 = t6_check(a.t6, a.t6_ref_hash) if a.t6 else None
    v1 = [r["C1"]["verdict"] for r in rows.values()]; v3 = [r["C3"]["verdict"] for r in rows.values()]
    verdict = {"completion": comp, "C1_hard_trips": [k for k, r in rows.items() if r["C1"]["verdict"] == "HARD"], "C1_soft_trips": [k for k, r in rows.items() if r["C1"]["verdict"] == "SOFT"],
               "C2_misses": [k for k, r in rows.items() if r["C2"]["verdict"] not in ("PASS",)], "C3_fails": [k for k, r in rows.items() if r["C3"]["verdict"] == "FAIL"], "T6": (t6 or {}).get("PASS", "NOT_RUN")}
    rep = {"script": "rung_readback.py", "models": {"%s n%d N%d I%d" % k: v for k, v in MODELS.items()}, "fits": rows, "rung": verdict, "t6": t6}
    os.makedirs(a.out, exist_ok=True)
    json.dump(rep, open(os.path.join(a.out, "rung_readback.json"), "w"), indent=1, default=str)
    f3 = lambda x: "NA" if x is None else ("%.4g" % x)
    L = ["# 10^5 rung read-back (rung_readback.py)", "", "completion %d of 12 (%s); C1 hard trips %s; soft trips %s; C2 misses %s; C3 fails %s; T6 %s" % (comp["rung_fits_delivered"], "PASS" if comp["PASS"] else "FAIL", verdict["C1_hard_trips"], verdict["C1_soft_trips"], verdict["C2_misses"], verdict["C3_fails"], verdict["T6"]), "",
         "| fit | N / I_max | billed (E, ratio) | C1 | C2 | C3 (max %) | C4 | M1 | M2 | M3 | HPM = S0 | pi_hat(S0) |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows.values():
        ra = r["recorded_arm"] or {}
        L.append("| %s | %s / %s | %s (%s, %s) | %s | %s | %s (%s) | %s | %s | %s | %s | %s | %s |" % (r["run_id"], ra.get("N"), ra.get("I"), f3(r["C1"]["billed"]), r["C1"]["model_E"], f3(r["C1"]["ratio"]), r["C1"]["verdict"], r["C2"]["verdict"], r["C3"]["verdict"],
                 f3(r["C3"]["max_pct"]), all(r["C4"].values()), f3(r["C2"]["M1"]), f3(r["C2"]["M2"]), f3(r["C2"]["M3"]), r["science"]["hpm_eq_S0"], f3(r["science"]["pi_hat_S0"])))
    if t6:
        L += ["", "T6 (forced-kill restart): **%s**; kills %s; resumed from step %s; final hash %s = reference %s = expected %s" % ("PASS" if t6["PASS"] else "FAIL", [(k["kind"], k["returncode"]) for k in t6["kills"]], t6["resumed_from_step"], t6["final_hash"], t6["reference_hash"], t6["expected_hash"])]
    open(os.path.join(a.out, "rung_readback.md"), "w").write("\n".join(L) + "\n")
    print(json.dumps({"completion": comp["rung_fits_delivered"], "T6": verdict["T6"], "C1_hard": verdict["C1_hard_trips"], "C3_fails": verdict["C3_fails"], "fits": len(rows)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
