#!/usr/bin/env python3
"""Synthetic-fixture tests for compare_overlap_v2.py (= the registered tests + the escalated-T cases of PREREG_ADDENDUM_1).  Stdlib only.

  python3 test_compare_overlap.py [--keep DIR]

Fabricates 10-dataset x 2-arm x 2-seed run directories (p = 200 kept columns) whose JSON is the REAL T5 eval.bin.json
(template_eval.bin.json, schema smcbvs4.eval/1) with the compared fields overwritten, plus a real-format fit.bin
container (pip_eq, pip_T, pip_r, logZ_r, hpm_S, mpm), truth.json, run_manifest.json and cost_<run_id>.json.
Cases: clean, hpm_one (CLEAN, 9/10), hpm_two (NOT CLEAN), hell_fail1 (MARGINAL), hell_fail2 (NOT CLEAN), T_higher_F (NOT CLEAN),
pip_fail (MARGINAL), evidence_fail (MARGINAL), cost_over (MARGINAL), incomplete (INCOMPLETE), pairing (INVALID),
no_cross (INCOMPLETE: the engine has no V-vs-T Hellinger field).
"""
import copy
import hashlib
import importlib.util
import json
import math
import os
import random
import shutil
import struct
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("compare_overlap_v2", os.path.join(HERE, "..", "compare_overlap_v2.py"))
co = importlib.util.module_from_spec(spec)
spec.loader.exec_module(co)

TEMPLATE = json.load(open(os.path.join(HERE, "template_eval.bin.json")))
P = 200
S0 = [10, 30, 50, 70, 90]


def write_bin(path, kind, mode, sections):
    """sections: name -> (dtype, dims tuple, bytes)."""
    names = list(sections)
    off = 128 + 128 * len(names)
    ents, body = [], b""
    for nm in names:
        dt, dims, raw = sections[nm]
        off = (off + 63) // 64 * 64
        pad = off - (128 + 128 * len(names) + len(body))
        body += b"\0" * pad
        d0 = dims[0]
        d1 = dims[1] if len(dims) > 1 else 0
        ent = nm.encode().ljust(48, b"\0") + struct.pack("<IIQQQQ", dt, len(dims), d0, d1, off, len(raw)) + hashlib.sha256(raw).digest() + b"\0" * 8
        ents.append(ent)
        body += raw
        off += len(raw)
    tbl = b"".join(ents)
    total = 128 + len(tbl) + len(body)
    hdr = bytearray(128)
    hdr[:8] = b"SMCBVS4\x00"
    struct.pack_into("<4I", hdr, 8, 1, kind, mode, len(names))
    struct.pack_into("<Q", hdr, 24, total)
    hdr[32:64] = hashlib.sha256(tbl).digest()
    with open(path, "wb") as fh:
        fh.write(bytes(hdr) + tbl + body)


def f64(v):
    import array
    a = array.array("d", v)
    return a.tobytes()


def i32(v):
    import array
    return array.array("i", v).tobytes()


def make_fit(rundir, rid, arm, seed, ds_idx, design, rep, o, rng):
    """o: overrides for this fit."""
    R = 16 if arm == "V" else 4
    null = design == "NULL"
    s0 = [] if null else S0
    base_z = -230.0 - 2.5 * ds_idx
    z_true = base_z + o.get("dz", 0.0)
    lzr = [z_true + rng.gauss(0, 0.035) for _ in range(R)]
    mx = max(lzr)
    zhat = mx + math.log(sum(math.exp(x - mx) for x in lzr) / R)
    zT = zhat - 0.2 - abs(rng.gauss(0, 0.02)) + o.get("dzT", 0.0)
    pip_r = []
    for _ in range(R):
        row = [(0.9998 if (j + 1) in s0 else 0.003) + rng.gauss(0, 0.0004) for j in range(P)]
        pip_r.append([min(max(x, 0.0), 1.0) for x in row])
    pip_eq = [sum(pip_r[r][j] for r in range(R)) / R + (o.get("pip_shift", {}).get(j, 0.0)) for j in range(P)]
    pip_T = [x * 0.999 for x in pip_eq]
    hpm = sorted(o.get("hpm", s0))
    F = -234.2 - ds_idx + o.get("dF", 0.0)
    ev = copy.deepcopy(TEMPLATE)
    ev["data"].update({"p": P, "p_raw": P})
    ev["mode"] = "V" if arm == "V" else "law"
    ev["fit"]["mode"] = ev["mode"]
    m = ev["fit"]["meta"]
    tier = o.get("tier", 0)
    m.update({"N": o.get("N", 2500) if arm == "V" else o.get("N", 10000 * 4 ** tier), "Rp": R, "tier": tier, "mode": ev["mode"], "status": "completed", "fit_state": "completed"})
    m["binary"]["island_isa"] = "sapphirerapids"
    ev["binary"]["sha256"] = ("a" if arm == "V" else "b") * 64
    m["binary"]["sha256"] = ("a" if arm == "V" else "b") * 64
    ev["selection"].update({"hpm": hpm, "mpm": sorted(o.get("mpm", s0)), "F_hpm": F, "hpm_size": len(hpm)})
    ev["evidence"].update({"logZ": zhat, "logZ_T": zT, "logZ_r": lzr, "R_eff": R * 0.999, "sigma_hat": co.sd(lzr)})
    ev["pip"]["eq"]["n_null_gt_0.5"] = o.get("null_hits", 0)
    h2 = 0.0055 + rng.gauss(0, 0.0001)
    ev["dist"]["T"]["predictive"]["h2"] = h2
    ev["dist"]["H"]["plugin"]["h2"] = 0.0047
    ev["dist"]["M"]["plugin"]["h2"] = 0.0047
    os.makedirs(rundir, exist_ok=True)
    json.dump(ev, open(os.path.join(rundir, "eval.bin.json"), "w"))
    dsid = "4-%s-n200-r%02d" % (design, rep)
    xs = hashlib.sha256(("X" + dsid).encode()).hexdigest()
    ys = hashlib.sha256(("y" + dsid).encode()).hexdigest()
    if o.get("bad_pairing"):
        xs = hashlib.sha256(b"other").hexdigest()
    json.dump({"S0": s0, "X_sha256": xs, "y_sha256": ys, "beta": [1] * len(s0), "sigma": 1, "spec": {"design": design, "n": 200, "p": P}},
              open(os.path.join(rundir, "truth.json"), "w"))
    json.dump({"schema": "smcbvs4.run/1", "batch": "FIX", "run_id": rid, "mode": "V" if arm == "V" else "law", "code_commit": "f" * 40,
               "params": {"design": design, "p": P, "n": 200, "N": m["N"], "Rp": R}}, open(os.path.join(rundir, "run_manifest.json"), "w"))
    core_h = o.get("core_h", 6.0 if arm == "V" else 45.0)
    json.dump({"run_id": rid, "billed_core_h": core_h, "stages": {"islands": {"billed_core_h": core_h}}}, open(os.path.join(rundir, "cost_%s.json" % rid), "w"))
    if not o.get("no_fitbin"):
        write_bin(os.path.join(rundir, "fit.bin"), 6, 3 if arm == "V" else 2, {
            "hpm_S": (2, (len(hpm),), i32([h - 1 for h in hpm])),
            "logZ_r": (1, (R,), f64(lzr)),
            "pip_eq": (1, (P,), f64(pip_eq)),
            "pip_T": (1, (P,), f64(pip_T)),
            "pip_r": (1, (R, P), f64([x for row in pip_r for x in row])),
            "mpm": (2, (len(s0),), i32([x - 1 for x in s0]))})


DESIGNS = [("AR", r) for r in (1, 2, 3, 4)] + [("ARweak", 1), ("ARweak", 2), ("ADJOPP", 1), ("ADJOPP", 2), ("IND", 1), ("NULL", 1)]


def build(root, case):
    """returns (cross dict or None)."""
    rng = random.Random(12345)
    shutil.rmtree(root, ignore_errors=True)
    cross = {}
    for idx, (design, rep) in enumerate(DESIGNS):
        dsid = "4-%s-n200-r%02d" % (design, rep)
        cross[dsid] = {str(s): {"h2": 2e-5, "se": 1e-6} for s in (1, 2)}      # d_VT ~ 0.0045 vs d_T ~ 0.074 -> 6%
        for arm in ("V", "T"):
            for seed in (1, 2):
                rid = "%s-%s-s%d" % (dsid, arm, seed)
                o = {}
                if case == "hpm_one" and (design, rep) == ("AR", 2) and arm == "V":
                    o.update({"hpm": S0 + [150], "dF": 1.0})            # V finds a better, larger model; T keeps S0
                if case == "hpm_two" and (design, rep) in (("AR", 2), ("IND", 1)) and arm == "V":
                    o.update({"hpm": S0 + [150], "dF": 1.0})
                if case == "T_higher_F" and (design, rep) == ("AR", 3) and arm == "T" and seed == 1:
                    o.update({"hpm": S0 + [150], "dF": 1.0})
                if case == "pip_fail" and (design, rep) == ("AR", 3) and arm == "T":
                    o["pip_shift"] = {7: 0.2}
                if case == "evidence_fail" and (design, rep) == ("AR", 3) and arm == "T":
                    o["dz"] = 0.6
                if case == "cost_over" and (design, rep) == ("ADJOPP", 1) and arm == "T" and seed == 1:
                    o["core_h"] = 200.0
                if case == "pairing" and (design, rep) == ("AR", 3) and arm == "T" and seed == 2:
                    o["bad_pairing"] = True
                if case in ("escalated_T", "escalated_T_cost") and (design, rep) == ("AR", 1) and arm == "T":
                    o["tier"] = 1                                       # N_final = 40,000 = 10^4 x 4^1
                if case == "escalated_T_cost" and (design, rep) == ("AR", 1) and arm == "T" and seed == 1:
                    o["core_h"] = 200.0                                 # cost rule unchanged: still MARGINAL
                if case == "T_N_not_tier" and (design, rep) == ("AR", 1) and arm == "T" and seed == 1:
                    o.update({"tier": 0, "N": 40000})                   # N escalated but tier 0 recorded: not delivered
                if case == "T_N_wrong_tier" and (design, rep) == ("AR", 1) and arm == "T" and seed == 1:
                    o.update({"tier": 1, "N": 10000})                   # tier 1 recorded but N is the tier-0 value: not delivered
                if case == "V_N_escalated" and (design, rep) == ("AR", 1) and arm == "V" and seed == 1:
                    o.update({"N": 10000})                              # V check unchanged: N must be 2500
                if case == "incomplete" and (design, rep) == ("IND", 1) and arm == "T" and seed == 2:
                    continue
                if case == "incomplete2" and (design, rep) == ("IND", 1) and arm == "T" and seed == 2:
                    o["no_fitbin"] = True
                make_fit(os.path.join(root, "FIX", rid), rid, arm, seed, idx, design, rep, o, rng)
        if case == "hell_fail1" and (design, rep) == ("AR", 2):
            cross[dsid] = {str(s): {"h2": 0.004, "se": 1e-5} for s in (1, 2)}   # d_VT = 0.063 ~ 85% of d_T
        if case == "hell_fail2" and (design, rep) in (("AR", 2), ("IND", 1)):
            cross[dsid] = {str(s): {"h2": 0.004, "se": 1e-5} for s in (1, 2)}
    return {"schema": "overlap1e4.cross_vt/1", "pairs": cross}


EXPECT = {
    "clean": ("CLEAN", True),
    "hpm_one": ("CLEAN", True),
    "hpm_two": ("NOT CLEAN", True),
    "hell_fail1": ("MARGINAL", True),
    "hell_fail2": ("NOT CLEAN", True),
    "T_higher_F": ("NOT CLEAN", True),
    "pip_fail": ("MARGINAL", True),
    "evidence_fail": ("MARGINAL", True),
    "cost_over": ("MARGINAL", True),
    "incomplete": ("INCOMPLETE", True),
    "incomplete2": ("INCOMPLETE", True),
    "pairing": ("INVALID", True),
    "no_cross": ("INCOMPLETE", False),
    # PREREG_ADDENDUM_1: escalated T fits (both seeds of AR r01 at tier 1, N 40,000) are delivered; nothing else relaxed
    "escalated_T": ("CLEAN", True),
    "escalated_T_cost": ("MARGINAL", True),
    "T_N_not_tier": ("INCOMPLETE", True),
    "T_N_wrong_tier": ("INCOMPLETE", True),
    "V_N_escalated": ("INCOMPLETE", True),
}


def main():
    keep = None
    if "--keep" in sys.argv:
        keep = sys.argv[sys.argv.index("--keep") + 1]
    base = keep or tempfile.mkdtemp(prefix="overlap_fix_")
    os.makedirs(base, exist_ok=True)
    fails = 0
    for case, (want, use_cross) in EXPECT.items():
        root = os.path.join(base, case, "records")
        cross = build(root, "clean" if case == "no_cross" else case)
        out = os.path.join(base, case, "out")
        args = ["--records", root, "--out", out]
        if use_cross:
            cf = os.path.join(base, case, "cross.json")
            json.dump(cross, open(cf, "w"))
            args += ["--cross-file", cf]
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            co.main(args)
        v = json.load(open(os.path.join(out, "verdict.json")))
        ok = v["outcome"] == want
        crit = {c["id"]: c["status"] for c in v["criteria"]}
        print("%-14s expected %-10s got %-10s %s   %s" % (case, want, v["outcome"], "OK" if ok else "**MISMATCH**", crit))
        if not ok:
            fails += 1
            print(buf.getvalue())
    # the clean case must have every criterion PASS and per-file outputs present
    out = os.path.join(base, "clean", "out")
    for f in ("per_dataset.csv", "per_fit.csv", "verdict.json", "verdict.md"):
        assert os.path.isfile(os.path.join(out, f)), f
    v = json.load(open(os.path.join(out, "verdict.json")))
    assert all(c["status"] == "PASS" for c in v["criteria"]), [c for c in v["criteria"] if c["status"] != "PASS"]
    print("clean case: all %d criteria PASS" % len(v["criteria"]))
    # escalated-T case: delivered 40/40, tier_final / N_final reported per fit in per_fit.csv, per_dataset.csv, verdict.json
    import csv
    eo = os.path.join(base, "escalated_T", "out")
    ev_ = json.load(open(os.path.join(eo, "verdict.json")))
    assert ev_["summary"]["n_delivered"] == 40 and ev_["outcome"] == "CLEAN", ev_["summary"]
    ft = ev_["fits_tier_N"]
    for rid, x in ft.items():
        esc = rid.startswith("4-AR-n200-r01-T-")
        want = (1, 40000) if esc else (0, 2500 if x["arm"] == "V" else 10000)
        assert (x["tier_final"], x["N_final"]) == want and x["delivered"], (rid, x)
    pf = {r["run_id"]: r for r in csv.DictReader(open(os.path.join(eo, "per_fit.csv")))}
    assert pf["4-AR-n200-r01-T-s1"]["tier_final"] == "1" and pf["4-AR-n200-r01-T-s1"]["N_final"] == "40000"
    assert pf["4-AR-n200-r01-V-s1"]["N_final"] == "2500" and pf["4-IND-n200-r01-T-s2"]["N_final"] == "10000"
    pd_ = {r["dataset"]: r for r in csv.DictReader(open(os.path.join(eo, "per_dataset.csv")))}
    r1 = pd_[[k for k in pd_ if "AR" in k and k.endswith("r01") and "weak" not in k][0]]
    assert r1["tier_final_T_s1"] == "1" and r1["N_final_T_s1"] == "40000" and r1["N_final_V_s2"] == "2500", r1
    print("escalated-T case: 40/40 delivered; tier_final/N_final reported in per_fit.csv, per_dataset.csv, verdict.json")
    # the registered script must still reject the escalated fit (the very mismatch the addendum fixes)
    sp = importlib.util.spec_from_file_location("compare_overlap_reg", os.path.join(HERE, "..", "compare_overlap.py"))
    reg = importlib.util.module_from_spec(sp); sp.loader.exec_module(reg)
    import io as _io, contextlib as _cl
    with _cl.redirect_stdout(_io.StringIO()):
        reg.main(["--records", os.path.join(base, "escalated_T", "records"), "--out", os.path.join(base, "escalated_T", "out_reg"),
                  "--cross-file", os.path.join(base, "escalated_T", "cross.json")])
    rv = json.load(open(os.path.join(base, "escalated_T", "out_reg", "verdict.json")))
    assert rv["outcome"] == "INCOMPLETE" and rv["summary"]["n_delivered"] == 38, rv["summary"]["n_delivered"]
    print("registered script on the same escalated fixture: INCOMPLETE (38/40), as documented in the addendum")
    # --wave-check on a partial set (only AR r01 s1: V and T) must run without a verdict
    wc_root = os.path.join(base, "wave_check", "records")
    shutil.rmtree(os.path.join(base, "wave_check"), ignore_errors=True)
    for arm in ("V", "T"):
        rid = "4-AR-n200-r01-%s-s1" % arm
        make_fit(os.path.join(wc_root, "FIX", rid), rid, arm, 1, 0, "AR", 1, {}, random.Random(7))
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        co.main(["--records", wc_root, "--out", os.path.join(base, "wave_check", "out"), "--wave-check"])
    wrows = list(csv.DictReader(open(os.path.join(base, "wave_check", "out", "wave_check.csv"))))
    assert len(wrows) == 1 and wrows[0]["hpm_equal"] == "True" and wrows[0]["X_y_sha_equal"] == "True", wrows
    assert not os.path.exists(os.path.join(base, "wave_check", "out", "verdict.json"))
    print("wave-check: OK (1 pair, no verdict file)")
    if keep is None:
        shutil.rmtree(base, ignore_errors=True)
    print("FAILED %d" % fails if fails else "ALL TESTS PASSED (%d cases)" % len(EXPECT))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
