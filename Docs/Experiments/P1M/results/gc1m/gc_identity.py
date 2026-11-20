#!/usr/bin/env python3
"""gc_identity.py -- the F2 identity statement at 1M (GC_PLAN section 2; GC_PREREG section 3): the frozen rep-1 re-run (F2 da0cf85b, I_max 0) against the 11-17 fit (code 2cfaa9e5, I_max 3), from the
RECORDS (the 11-17 setup / calib / island files are gone from NOTS scratch; its sidecars and cost records are in records/F1M_pilot/). READ-ONLY, stdlib, deterministic.

  python3 -I gc_identity.py --old ~/SMC_Engineering_Department/records/F1M_pilot --new <records/gc1m/GC_P/6-AR-n200-r01-V-s1> --out OUTDIR

GATING checks (IDENTITY PASS iff all three hold; a failure = STOP, HQ + Theory: the pair would not be a pure grid contrast):
  I1 data     truth.json X_sha256, y_sha256, raw_content_sha256 equal; run_manifest params design, signal, p, n, data_seed, seed, Rp equal.
  I2 setup    setup.bin.json B, B_blocks, C, J, mode_size, n, p, partition, file_mode equal (the file hash is NOT compared: it carries the binary's provenance).
  I3 pilot    cost/cost_pilot_t0_k0_r0.jsonl (the calibration PILOT island, role R_PILOT, N 512, G 256): header G, N, arith, iter, kernel, m, p, r, role, schema, segment, tier, tile equal, the same number
              of rows, and EVERY row equal on the trajectory-determined counters DET: M, act_cols, act_cols_per_pass, kind, mean_S, particle_rounds, passes, pairs, phi, segment, slow_supports, step,
              store_mean_k, store_size, supports, sweeps (pairs = (support, label) pairs scored, mean_S and store_mean_k are state statistics: the same values in all 34 rows = the same pilot trajectory).
              NOT gated (reported with their row counts and max relative differences): the ACCOUNTING counters flips, flips_per_step, offers, dup_dropped, merges: control runs at 10^5 (the same pilot run in
              two fits of the same seed and data, F2 both; `tools/identity_controls/`) differ in them (flips by <= 0.3 % per row, offers and dup_dropped by <= 7 %, merges by 1-2 events) although every DET counter is equal, so they depend on execution order; timing and memory keys (t_*, wall, hwm_kb, rss_kb) are ignored.
REPORTED (not gating): I4 the new final-island stage count T (island_1.bin.json; expected 27 = the 11-17 final and diagnostic islands' bridge stages) and the arms (I_max 3 -> 0, I_used), binary shas.
"""
import argparse, json, math, os, sys

TIMING = ("wall", "hwm_kb", "rss_kb")
# trajectory-determined counters (GATING): equal in EVERY control pair of the 10^5 records (same seed, data, setup; I_max 0 vs I_max 3 fits and the N 2,500 twin); the ACCOUNTING counters below vary between
# repeated identical runs (execution-order dependent: flips, flips_per_step, offers, dup_dropped, merges) and are only REPORTED, never gated
DET = ("M", "act_cols", "act_cols_per_pass", "kind", "mean_S", "particle_rounds", "passes", "pairs", "phi", "segment", "slow_supports", "step", "store_mean_k", "store_size", "supports", "sweeps")
ACCOUNTING = ("flips", "flips_per_step", "offers", "dup_dropped", "merges")
HDR = ("G", "N", "arith", "iter", "kernel", "m", "p", "r", "role", "schema", "segment", "tier", "tile")
RUNP = ("design", "signal", "p", "n", "data_seed", "seed", "Rp")
SETUP = ("B", "B_blocks", "C", "J", "mode_size", "n", "p", "partition", "file_mode")


def jl(p):
    return json.load(open(p))


def det_keys(row):
    return sorted(k for k in row if k in DET)


def pilot_rows(path):
    L = [json.loads(l) for l in open(path) if l.strip()]
    return L[0]["cost_header"], L[1:]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--old", required=True); ap.add_argument("--new", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    rep = {"old": a.old, "new": a.new, "checks": {}, "detail": {}}
    try:
        to, tn = jl(os.path.join(a.old, "truth.json")), jl(os.path.join(a.new, "truth.json"))
        d = {k: (to.get(k), tn.get(k)) for k in ("X_sha256", "y_sha256", "raw_content_sha256")}
        po, pn = jl(os.path.join(a.old, "run_manifest.json"))["params"], jl(os.path.join(a.new, "run_manifest.json"))["params"]
        d.update({"params." + k: (po.get(k), pn.get(k)) for k in RUNP})
        rep["detail"]["I1"] = d; rep["checks"]["I1_data"] = all(v[0] is not None and v[0] == v[1] for v in d.values())
    except Exception as e:
        rep["detail"]["I1"] = "error: %s" % e; rep["checks"]["I1_data"] = False
    try:
        so, sn = jl(os.path.join(a.old, "setup.bin.json")), jl(os.path.join(a.new, "setup.bin.json"))
        d = {k: (so.get(k), sn.get(k)) for k in SETUP}
        rep["detail"]["I2"] = d; rep["checks"]["I2_setup"] = all(v[0] is not None and v[0] == v[1] for v in d.values())
    except Exception as e:
        rep["detail"]["I2"] = "error: %s" % e; rep["checks"]["I2_setup"] = False
    try:
        ho, ro = pilot_rows(os.path.join(a.old, "cost", "cost_pilot_t0_k0_r0.jsonl")); hn, rn = pilot_rows(os.path.join(a.new, "cost", "cost_pilot_t0_k0_r0.jsonl"))
        hdr_ok = all(ho.get(k) == hn.get(k) for k in HDR); n_ok = len(ro) == len(rn)
        bad = []
        if n_ok:
            for i, (x, y) in enumerate(zip(ro, rn)):
                ks = det_keys(x)
                if ks != det_keys(y):
                    bad.append((i, "keys differ")); continue
                for k in ks:
                    vx, vy = x[k], y[k]
                    same = (vx == vy) or (isinstance(vx, float) and isinstance(vy, float) and math.isnan(vx) and math.isnan(vy)) or (vx == "NaN" and vy == "NaN")
                    if not same:
                        bad.append((i, k, vx, vy))
        acc = {k: {"rows_differing": sum(1 for x, y in zip(ro, rn) if x.get(k) != y.get(k)), "max_rel_diff": max([abs(x[k] - y[k]) / max(abs(x[k]), 1e-300) for x, y in zip(ro, rn) if x.get(k) and isinstance(x.get(k), (int, float)) and isinstance(y.get(k), (int, float))] or [0.0])} for k in ACCOUNTING} if n_ok else None
        rep["detail"]["I3"] = {"header_equal": hdr_ok, "rows": [len(ro), len(rn)], "differences": bad[:10], "n_differences": len(bad), "accounting_counters_reported_not_gating": acc,
                               "sums_old": {k: sum(r[k] for r in ro) for k in ("flips", "offers", "pairs")}, "sums_new": {k: sum(r[k] for r in rn) for k in ("flips", "offers", "pairs")}}
        rep["checks"]["I3_pilot_counters"] = bool(hdr_ok and n_ok and not bad)
    except Exception as e:
        rep["detail"]["I3"] = "error: %s" % e; rep["checks"]["I3_pilot_counters"] = False
    I4 = {}
    try:
        I4["island_1_T_new"] = jl(os.path.join(a.new, "island_1.bin.json")).get("T"); I4["expected_T"] = 27
    except Exception as e:
        I4["island_1_T_new"] = "error: %s" % e
    try:
        co, cn = jl(os.path.join(a.old, "calib.bin.json")), jl(os.path.join(a.new, "calib.bin.json"))
        I4["I_max_old_new"] = (co["settings"].get("I_max"), cn["settings"].get("I_max")); I4["binary_sha256_old_new"] = ((co.get("binary") or {}).get("sha256"), (cn.get("binary") or {}).get("sha256"))
    except Exception as e:
        I4["arms"] = "error: %s" % e
    try:
        cm = jl(os.path.join(a.new, "calib_meta.json")); cm = cm.get("meta", cm); I4["new_I_used"] = cm.get("I_used"); I4["new_I_max"] = cm.get("I_max"); I4["new_N"] = cm.get("N")
    except Exception as e:
        I4["new_calib_meta"] = "error: %s" % e
    rep["detail"]["I4_reported_not_gating"] = I4
    rep["IDENTITY"] = "PASS" if all(rep["checks"].values()) else "FAIL"
    os.makedirs(a.out, exist_ok=True)
    json.dump(rep, open(os.path.join(a.out, "gc_identity.json"), "w"), indent=1, default=str)
    print(json.dumps({"IDENTITY": rep["IDENTITY"], "checks": rep["checks"], "I4": I4}, indent=1, default=str))
    return 0 if rep["IDENTITY"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
