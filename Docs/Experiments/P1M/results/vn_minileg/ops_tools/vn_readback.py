#!/usr/bin/env python3
"""vn_readback.py <WAVE> -- V-N mini-leg read-back of a collected wave (MINILEG_PLAN 5.4 checklist). Stdlib only; reads records/vn_minileg/<WAVE> and the leg's twins.
Prints a table per fit: delivered, stage states, billed core-h vs class soft/hard, arm (N, refine_m, I_max, I_used, rule) vs the plan, data identity (truth.json X/y sha256 vs vn_refs.json),
build identity (BUILD_F2), PAIRING (calib_meta sections except meta + grid vs the N=2,500 twin of the leg), f (islands wall and billed core-h vs the twin)."""
import glob, hashlib, json, os, re, subprocess, sys
REC = "/home/fb31/SMC_Engineering_Department/records"; STG = "/home/fb31/SMC_Engineering_Department/staging/vn_minileg"
wave = sys.argv[1]; WD = os.path.join(REC, "vn_minileg", wave)
sys.path.insert(0, os.path.join(STG, "tools")); sys.dont_write_bytecode = True
import stop_rules_vn as sr
F2SHA = "da0cf85b5fe014973d15674f0da8e8c12dfdaf465a5e06aa0216b294601f231a"
refs = json.load(open(os.path.join(STG, "vn_refs.json")))
J = lambda p: json.load(open(p))
rows, problems = [], []
twin_dir = lambda rid: next(iter(glob.glob(os.path.join(REC, "precision1e4", "*", rid))), None)
def cost_of(unit_parent, rid):
    for p in glob.glob(os.path.join(unit_parent, "_batch_*", "cost", "cost_%s.json" % rid)): return J(p)
for b in sorted(glob.glob(os.path.join(STG, "current", "scripts", "VN_%s_*" % wave))):
    pr = J(os.path.join(b, "plan.resolved.json"))
    for f in pr["fits"]:
        rid = f["run_id"]; U = os.path.join(WD, rid); r = {"rid": rid, "batch": os.path.basename(b)}; ok = True
        r["delivered"] = all(os.path.exists(os.path.join(U, x)) for x in ("fit.bin", "eval.bin", "eval.bin.json", "calib_meta.json", "truth.json")) and not os.path.exists(os.path.join(U, "INCOMPLETE.txt"))
        sums = subprocess.run("cd %s && sha256sum --quiet -c SHA256SUMS" % U, shell=True, capture_output=True); r["sha_ok"] = sums.returncode == 0
        r["one_sums"] = len(subprocess.run(["find", U, "-name", "SHA256SUMS*"], capture_output=True, text=True).stdout.split()) == 1
        c = cost_of(WD, rid); r["states"] = sorted({s for st in c["stages"].values() for s in st["states"]}) if c else ["?"]; r["cost"] = c["billed_core_h"] if c else None
        r["islands"] = c["stages"]["islands"] if c else None; r["klass"] = sr.klass(rid); t = sr.TABLE.get(r["klass"]); r["soft"], r["hard"] = (t[1], t[2]) if t else (None, None)
        m = J(os.path.join(U, "calib_meta.json")); mm = m["meta"]
        want = dict(N=f.get("N"), refine_m=(f.get("params") or {}).get("refine_m", f.get("refine_m")), I_max=(f.get("params") or {}).get("I_max", f.get("I_max")))
        r["arm"] = {k: mm.get(k) for k in ("N", "refine_m", "I_max", "I_used", "rule")}; r["arm_plan"] = want
        r["arm_ok"] = all(mm.get(k) == v for k, v in want.items() if v is not None) and mm.get("rule") == "bounded" and (want["I_max"] != 0 or mm.get("I_used") == 0)
        r["build_ok"] = mm["binary"]["sha256"] == F2SHA and mm["binary"]["git_commit"].startswith("e993ece2")
        tj = J(os.path.join(U, "truth.json")); key = sr.dataset(rid); rf = refs.get(key)
        r["data_ok"] = rf is None or (tj.get("X_sha256") == rf["X_sha256"] and tj.get("y_sha256") == rf["y_sha256"])
        ev = J(os.path.join(U, "eval.bin.json")); r["logZ_n"] = len(ev["evidence"]["logZ_r"]); r["R"] = f.get("Rp", f.get("R"))
        # pairing with the N = 2,500 twin (N 10^4 fits only)
        r["pair"] = None
        if mm.get("N") == 10000:
            td = twin_dir(sr.twin(rid)); r["twin"] = os.path.basename(td) if td else None
            if td:
                tm = J(os.path.join(td, "calib_meta.json")); sa = {x["name"]: (x["sha256"], x["dims"]) for x in m["sections"] if x["name"] != "meta"}; sb = {x["name"]: (x["sha256"], x["dims"]) for x in tm["sections"] if x["name"] != "meta"}
                diff = sorted(k for k in set(sa) | set(sb) if sa.get(k) != sb.get(k))
                r["pair"] = {"n_sections": len(sa), "differing": diff, "grid_equal": sa.get("grid") == sb.get("grid") and sa.get("grid_unrefined") == sb.get("grid_unrefined"), "twin_N": tm["meta"].get("N"),
                             "meta_diff": sorted(k for k in set(mm) | set(tm["meta"]) if k not in ("binary", "inputs", "threads", "seed") and mm.get(k) != tm["meta"].get(k))}
                tc = cost_of(os.path.dirname(td), os.path.basename(td)); r["twin_islands"] = tc["stages"]["islands"] if tc else None
                r["twin_cost"] = tc["billed_core_h"] if tc else None
                r["twin_tasks_wall"] = (tc or {}).get("stages", {}).get("islands", {}).get("wall_s_max")
        rows.append(r)
print(json.dumps(rows, indent=1, default=str))
