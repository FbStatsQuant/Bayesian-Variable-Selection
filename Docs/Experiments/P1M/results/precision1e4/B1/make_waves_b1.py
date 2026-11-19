#!/usr/bin/env python3
"""make_waves_b1.py -- plans of the boundary add-on B1 (results/precision1e4/ADDENDUM_1_BOUNDARY.md): AR-weak, p = 10^4, n = 100, ONE dataset
(4-ARweak-n100-r91), V x seeds {1, 2} and T x seeds {1, 2} = 4 fits. OPS tool; writes plans + a dry-run script tree only; never submits, never ssh.
Stdlib only. Reuses, unchanged: the overlap's make_waves.py constants (T_ARM, T shapes of the W3 override = shapes_W3.json) and the leg's make_waves_prec.py
V shapes (class s100) -- nothing is re-typed. The generator knows no rep 91 and no n = 100 T fit, so the 4 fit dicts are COPIED from generated fits
(V: 4-ARweak-n100-r01-V-s1 of the science block; T: 4-ARweak-n200-r01-T-s1 of the overlap) with run_id / n / data_seed / seed replaced.

  make_waves_b1.py --wt <engine worktree at b89cba4d> --code-commit <F, 40 hex> --out <dir> [--dept /home/fb31/SMC_Engineering_Department]
"""
import argparse, hashlib, json, math, os, subprocess, sys

DEPT = "/home/fb31/SMC_Engineering_Department"
OV_TOOLS = DEPT + "/staging/overlap1e4/tools"
LEG_PREC = "/home/fb31/BVS-wt/P1M/Docs/Experiments/P1M/results/precision1e4"
SHAPES_W3 = DEPT + "/staging/overlap1e4/shapes_W3.json"
REP, DATA_SEED, N_DATA = 91, 403010091, 100          # R=4, D=3 (AR-weak), n/100 = 1, rep 91; engine seeds: s1 = data seed, s2 = data seed + 100
ENG_SEED = {1: DATA_SEED, 2: DATA_SEED + 100}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--wt", required=True); ap.add_argument("--code-commit", required=True); ap.add_argument("--out", required=True); ap.add_argument("--dept", default=DEPT)
    a = ap.parse_args()
    sys.dont_write_bytecode = True
    sys.path.insert(0, OV_TOOLS); sys.path.insert(0, LEG_PREC)
    import make_waves as ovw, make_waves_prec as lw          # constants only; their main() is not run
    slurm = os.path.join(a.wt, "Scripts/SMC_BVS/engine_v4/tools/slurm")
    sys.path.insert(0, slurm)
    import p1m_driver
    gen = os.path.join(a.out, "gen")
    r = subprocess.run([sys.executable, os.path.join(slurm, "p1m_cells.py"), "--plans", gen, "--only", "1e4", "--code-commit", a.code_commit],
                       capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    if r.returncode:
        sys.exit("p1m_cells failed: " + r.stdout + r.stderr)
    fits, head = {}, {}
    for fn in sorted(os.listdir(gen)):
        p = json.load(open(os.path.join(gen, fn)))
        h = {k: v for k, v in p.items() if k not in ("fits", "batch", "core_h_cap", "kind", "resources", "max_task_hours")}
        if fn.startswith("overlap1e4") and p["mode"] == "law":
            head["T"] = h
        elif fn.startswith("science1e4") and p["mode"] == "V":
            head["V"] = h
        for f in p["fits"]:
            if (fn.startswith("overlap1e4") and p["mode"] == "law") or fn.startswith(("science1e4", "overlap1e4")):
                fits[f["run_id"]] = f
    used = {f["data_seed"] for f in fits.values()} | {f["seed"] for f in fits.values()}
    for s in ENG_SEED.values():      # collision check: against EVERY generated fit (overlap, precision, science) and its engine seeds data + 100 k
        assert s not in used, "seed collision %d" % s
    allseeds = set()
    for fn in os.listdir(gen):
        for f in json.load(open(os.path.join(gen, fn)))["fits"]:
            allseeds |= {f["data_seed"], f["seed"]}
    assert not (set(ENG_SEED.values()) & allseeds) and not any(("-r%02d-" % REP) in rid for rid in fits), "rep 91 / seed collision"
    assert head["V"]["island_isa"] == "sapphirerapids" and head["T"]["mode"] == "law"
    arms = {}
    for arm, tmpl in (("V", "4-ARweak-n100-r01-V-s1"), ("T", "4-ARweak-n200-r01-T-s1")):
        sel = []
        for s in (1, 2):
            f = dict(fits[tmpl])
            f.update(run_id="4-ARweak-n100-r%02d-%s-s%d" % (REP, arm, s), n=N_DATA, data_seed=DATA_SEED, seed=ENG_SEED[s])
            if arm == "T":
                f.update(ovw.T_ARM)                                  # law mode, N = 10^4, R' = 4 (as the overlap's make_waves forces it)
            else:
                assert (f["N"], f["Rp"]) == (2500, 16)               # V-1M class A, as in the overlap and the leg (default m = 1, I_max = 3: no params)
            sel.append(f)
        arms[arm] = sel
    shapes_T = json.load(open(SHAPES_W3))["T"]                       # the overlap's W3 settings: calibrate 5:00 (max_task_hours 5.0), the rest as W0-W2
    os.makedirs(os.path.join(a.out, "plans"), exist_ok=True)
    rows = []
    for i, (arm, shp, mth, thr) in enumerate((("V", lw.SHAPES["s100"], 2.0, lw.THROTTLE["s100"]), ("T", shapes_T, 5.0, None)), 1):
        plan = dict(head[arm]); plan.update(batch="PL_B1_%d" % i, kind="gated (HQ 09e24da1 boundary add-on B1, %s arm; leg precision1e4)" % arm,
                                            max_task_hours=mth, resources=shp, fits=arms[arm])
        if thr:
            plan["island_throttle"] = thr
        wc = p1m_driver.resolve(dict(plan, core_h_cap=1e12))["worst_case_core_h"]
        plan["core_h_cap"] = math.ceil((wc + 0.05) * 10 - 1e-9) / 10
        plan = {k: plan[k] for k in ("batch", "mode", "code_commit", "method_tag", "core_tree", "binary", "max_task_hours", "island_isa", "kind",
                                     "island_throttle", "core_h_cap", "resources", "fits") if k in plan}
        pf = os.path.join(a.out, "plans", plan["batch"] + ".json")
        json.dump(plan, open(pf, "w"), indent=1); open(pf, "a").write("\n")
        sd = os.path.join(a.out, "scripts", plan["batch"])
        d = subprocess.run([sys.executable, os.path.join(slurm, "p1m_driver.py"), "--plan", pf, "--out", sd, "--dept", a.dept, "--strict"],
                           capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        if d.returncode:
            sys.exit("driver --strict failed for %s: %s%s" % (plan["batch"], d.stdout, d.stderr))
        res = json.load(open(os.path.join(sd, "plan.resolved.json")))
        rows.append((plan["batch"], arm, len(plan["fits"]), res["n_tasks"], res["worst_case_core_h"], plan["core_h_cap"], res.get("warnings"),
                     hashlib.sha256(open(pf, "rb").read()).hexdigest()))
        print("%s (%s): %d fits, %d tasks, worst %.1f core-h, cap %.1f, warnings %s, plan sha256 %s" % rows[-1])
        print("   run ids:", ", ".join(f["run_id"] for f in plan["fits"]), "| seeds:", [f["seed"] for f in plan["fits"]], "| N, Rp:", plan["fits"][0]["N"], plan["fits"][0]["Rp"])
    print("sum of worst cases (limit sum, a ledger figure, not an estimate): %.1f core-h" % sum(r[4] for r in rows))


if __name__ == "__main__":
    main()
