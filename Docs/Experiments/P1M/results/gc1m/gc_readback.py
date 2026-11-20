#!/usr/bin/env python3
"""gc_readback.py -- the G-C / 1M read-back tables (GC_PLAN section 3-4, GC_PREREG sections 4-5): per fit C1 cost / C2 precision (spec 0-v2.3 at 10^6) / C3 memory / C4 completion / C5 flags (the registered
gb_readback.py functions, imported UNEDITED from ../gb/), with the 1M class table, the kill-rule checks, and the G-C2 PILOT verdict. READ-ONLY, stdlib, deterministic.

  python3 -I gc_readback.py --records ROOT [ROOT ...] --cost-dir DIR [DIR ...] --out OUTDIR [--identity gc_identity.json]

1M CLASS TABLE (core-h per fit at N 2,500 unless stated; soft = max(3, 1.5E) report-and-continue, hard = max(3, 2.5E) STOP; the hard line is never re-fitted; basis: 11-17 fit 437.44 measured,
I_max 0 saves its 135.63 calibration down to the P7 pilot island 14.96 -> 317; the rung / G-B measured the I_max 0 calibration at 2-3 % of a 10^5 fit):
  AR-strong n200 (pilot, replicates, seeds) 317 -> 476 / 793 | ADJ-OPP n200 330 -> 495 / 825 | AR-weak n200 317 -> 476 / 793 | the N 10^4 fit (VN10K; E 775 at the 10^5 island factor 2.70) 775 -> 1,163 / 1,938 |
  option D AR n1000 1,087 -> 1,631 / 2,718 | the N 5,000 option (VN5K) 470 -> 705 / 1,175.
REQUESTS (GiB): setup 48, calibrate 128, islands 64, merge 128, eval 16 (option D: setup 64). KILL RULES (pilot; ENGINEERING_SPEC G-C): the calibration > 2 x its model (E 16 -> 32 core-h) or any island
 > 2 x its model (E 16.8 core-h; max task wall > 2 x 792 s) -> STOP. G-C2 PILOT PASS = C1 (<= 1.5 E = 476; the 2.5 E guard 793 is the STOP line) AND C2 (M1 <= 0.05, M2 <= 0.005, evidence within 3 s.e.,
 HPM certified, PIP agreement) AND C3 (peak RSS < request in every stage) AND C4 AND the identity gate (gc_identity.json: IDENTITY PASS) AND no kill-rule trip. HPM vs S0 (truth) is REPORTED beside it.
"""
import argparse, glob, importlib.util, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("gb_readback", os.path.join(os.path.dirname(HERE), "gb", "gb_readback.py"))
gbr = importlib.util.module_from_spec(spec); spec.loader.exec_module(gbr)
gbr.REQ_GIB.update({"setup": 48, "calibrate": 128, "islands": 64, "merge": 128, "eval": 16})

RUN = re.compile(r"^6-(?P<d>AR|ADJOPP|ARweak)-n(?P<n>\d+)-r(?P<r>\d+)-(?P<arm>V|VN10K|VN5K)-s(?P<s>\d+)$")
MODELS = {("AR", 200, 2500): 317, ("ADJOPP", 200, 2500): 330, ("ARweak", 200, 2500): 317, ("AR", 200, 10000): 775, ("AR", 1000, 2500): 1087, ("AR", 200, 5000): 470}
PILOT = "6-AR-n200-r01-V-s1"
CAL_E, ISL_E, ISL_WALL = 16.0, 16.8, 792.0
GIB = 2 ** 30


def c1(rid, rec, total):
    g = RUN.match(rid)
    E = MODELS.get((g["d"], int(g["n"]), rec["N"])) if (g and rec) else None
    return {"billed": total, "model_E": E, "soft": (max(3.0, 1.5 * E) if E else None), "hard": (max(3.0, 2.5 * E) if E else None), "ratio": (total / E if (E and total is not None) else None),
            "verdict": ("NO_MODEL" if not E or total is None else ("OK" if total <= max(3.0, 1.5 * E) else ("SOFT" if total <= max(3.0, 2.5 * E) else "HARD")))}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--records", nargs="+", required=True); ap.add_argument("--cost-dir", nargs="*", default=[]); ap.add_argument("--out", required=True); ap.add_argument("--identity", default=None)
    a = ap.parse_args(argv)
    runs = gbr.find(a.records, RUN)
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
        try:
            kb = json.load(open(os.path.join(dp, "fit.bin.json"))).get("peak_rss_kb")
            r["C3"]["merge_process_peak_gib"] = (kb / 2 ** 20) if kb else None
        except Exception:
            r["C3"]["merge_process_peak_gib"] = None
        st = r["stages"]
        r["kill"] = {"calibrate_billed": (st.get("calibrate") or {}).get("billed"), "calibrate_limit_2xE": 2 * CAL_E, "max_island_wall_s": (st.get("islands") or {}).get("wall_s_max"), "island_wall_limit_2x": 2 * ISL_WALL}
        r["kill"]["trip"] = bool((r["kill"]["calibrate_billed"] or 0) > 2 * CAL_E or (r["kill"]["max_island_wall_s"] or 0) > 2 * ISL_WALL)
        rows[rid] = r
    ident = json.load(open(a.identity)) if a.identity else None
    pv = None
    if PILOT in rows:
        p = rows[PILOT]
        items = {"C1": p["C1"]["verdict"] == "OK", "C2": p["C2"]["verdict"] == "PASS", "C3": p["C3"]["verdict"] in ("PASS", "ADVISORY"), "C4": all(p["C4"].values()), "identity": (ident or {}).get("IDENTITY") == "PASS", "no_kill_trip": not p["kill"]["trip"]}
        pv = {"items": items, "HPM_eq_S0 (reported)": p["science"]["hpm_eq_S0"], "pi_hat_S0": p["science"]["pi_hat_S0"], "billed": p["C1"]["billed"], "ratio": p["C1"]["ratio"],
              "G-C2": ("PASS" if all(items.values()) else ("STOP (C1 hard / kill rule)" if (p["C1"]["verdict"] == "HARD" or p["kill"]["trip"]) else "NOT_PASSED: " + ", ".join(k for k, v in items.items() if not v)))}
    rep = {"script": "gc_readback.py", "models": {"%s n%d N%d" % k: v for k, v in MODELS.items()}, "requests_gib": gbr.REQ_GIB, "fits": rows, "pilot": pv, "identity": ident and ident.get("IDENTITY")}
    os.makedirs(a.out, exist_ok=True)
    json.dump(rep, open(os.path.join(a.out, "gc_readback.json"), "w"), indent=1, default=str)
    f3 = lambda x: "NA" if x is None else ("%.4g" % x)
    L = ["# G-C / 1M read-back (gc_readback.py)", "", "pilot: %s" % (json.dumps(pv, default=str) if pv else "not in the records"), "",
         "| fit | N / I_max | billed (E, ratio) | C1 | C2 | C3 (max %) | C4 | kill trip | M1 | M2 | M3 | HPM = S0 | pi_hat(S0) |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows.values():
        ra = r["recorded_arm"] or {}
        L.append("| %s | %s / %s | %s (%s, %s) | %s | %s | %s (%s) | %s | %s | %s | %s | %s | %s | %s |" % (r["run_id"], ra.get("N"), ra.get("I"), f3(r["C1"]["billed"]), r["C1"]["model_E"], f3(r["C1"]["ratio"]), r["C1"]["verdict"], r["C2"]["verdict"], r["C3"]["verdict"],
                 f3(r["C3"]["max_pct"]), all(r["C4"].values()), r["kill"]["trip"], f3(r["C2"]["M1"]), f3(r["C2"]["M2"]), f3(r["C2"]["M3"]), r["science"]["hpm_eq_S0"], f3(r["science"]["pi_hat_S0"])))
    open(os.path.join(a.out, "gc_readback.md"), "w").write("\n".join(L) + "\n")
    print(json.dumps({"pilot": pv, "fits": len(rows), "identity": rep["identity"]}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
