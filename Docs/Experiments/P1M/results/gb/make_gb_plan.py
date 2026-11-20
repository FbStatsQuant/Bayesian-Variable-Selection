#!/usr/bin/env python3
"""make_gb_plan.py -- the G-B pilot-set plans (results/gb/GB_PLAN.md section 2) from the F2 tools. OPS tool: writes plans and a dry-run script tree only; never submits, never ssh.
Stdlib only. The generator (p1m_cells.py at F2) is NOT modified: it emits no I_max and N 2,500 for 10^5, so the corrections are applied here (as make_waves_prec.py / make_waves_vn.py did).

  make_gb_plan.py --wt <worktree of F2 = e993ece2> --code-commit e993ece226b355058e26400f05f9faad6daf16ca --out <dir> [--dept /home/fb31/SMC_Engineering_Department]

Fits (4; GB_PLAN 2.1): the 10^5 AR n200 r01 (seed 502020001) and ADJ-OPP n200 r01 (seed 505020001) datasets of the rung, N = 10^4 (N*, HQ H-38), m 1, R' 16, F2:
  `5-<design>-n200-r01-V-s1`   I_max 0 (the frozen configuration, the pilot)      `5-<design>-n200-r01-VI3-s1`  I_max 3 (its twin: same data, same engine seed)
EXPLICIT params in every fit: top-level N (the driver refuses a params.N that disagrees, Sol M2), params {refine_m, I_max}. After the driver runs, EVERY generated manifest that
carries the arm (run_manifests/*.json and each stage manifest) is read back and asserted to hold N = 10000, refine_m = 1 and the plan's I_max (no silent engine default).
Batches (one fit each; <= 150 tasks): GB_G1a AR pilot, GB_G1b AR twin (wave G1); GB_G2a ADJ-OPP pilot, GB_G2b ADJ-OPP twin (wave G2). Island arrays throttled %8.
Shapes (GB_PLAN 2.2): setup 32 CPU 16G 0:30; calibrate 64 CPU 16G (pilot 0:30, twin 1:00); islands 48 CPU 12G (AR 0:45, ADJ-OPP 1:00); merge 16 CPU 24G 0:30; eval 8 CPU 16G 0:45.
"""
import argparse, glob, hashlib, json, math, os, subprocess, sys

DEPT = "/home/fb31/SMC_Engineering_Department"
N_STAR = 10000


def shape(cal_time, isl_time):
    return {"setup": {"cpus": 32, "mem": "16G", "time": "00:30:00"}, "calibrate": {"cpus": 64, "mem": "16G", "time": cal_time},
            "islands": {"cpus": 48, "mem": "12G", "time": isl_time}, "merge": {"cpus": 16, "mem": "24G", "time": "00:30:00"}, "eval": {"cpus": 8, "mem": "16G", "time": "00:45:00"}}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--wt", required=True); ap.add_argument("--code-commit", required=True); ap.add_argument("--out", required=True); ap.add_argument("--dept", default=DEPT)
    a = ap.parse_args()
    gen = os.path.join(a.out, "gen")
    slurm = os.path.join(a.wt, "Scripts/SMC_BVS/engine_v4/tools/slurm")
    r = subprocess.run([sys.executable, os.path.join(slurm, "p1m_cells.py"), "--plans", gen, "--only", "1e5", "--code-commit", a.code_commit], capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    if r.returncode:
        sys.exit("p1m_cells failed: " + r.stdout + r.stderr)
    sys.path.insert(0, slurm); sys.dont_write_bytecode = True
    import p1m_driver
    fits, head = {}, None
    for fn in sorted(os.listdir(gen)):
        p = json.load(open(os.path.join(gen, fn)))
        if fn.startswith("rung1e5"):
            head = head or {k: v for k, v in p.items() if k not in ("fits", "batch", "core_h_cap", "kind", "resources", "max_task_hours")}
            fits.update({f["run_id"]: f for f in p["fits"]})
    assert head["mode"] == "V" and head.get("island_isa") == "sapphirerapids" and head["code_commit"] == a.code_commit
    new = {}
    for ds, rid0 in (("AR", "5-AR-n200-r01-V-s1"), ("ADJOPP", "5-ADJOPP-n200-r01-V-s1")):
        src = fits[rid0]
        assert src["p"] == 100000 and src["n"] == 200 and src["Rp"] == 16 and src["seed"] == src["data_seed"]
        for I, tag in ((0, "V"), (3, "VI3")):
            f = dict(src); f["run_id"] = "5-%s-n200-r01-%s-s1" % (ds, tag); f["N"] = N_STAR; f["params"] = {"refine_m": 1, "I_max": I}
            new[f["run_id"]] = f
    assert len(new) == 4 and {f["data_seed"] for f in new.values()} == {502020001, 505020001}
    batches = [("GB_G1a", "G1", "5-AR-n200-r01-V-s1", shape("00:30:00", "00:45:00")), ("GB_G1b", "G1", "5-AR-n200-r01-VI3-s1", shape("01:00:00", "00:45:00")),
               ("GB_G2a", "G2", "5-ADJOPP-n200-r01-V-s1", shape("00:30:00", "01:00:00")), ("GB_G2b", "G2", "5-ADJOPP-n200-r01-VI3-s1", shape("01:00:00", "01:00:00"))]
    os.makedirs(os.path.join(a.out, "plans"), exist_ok=True)
    wj, table = {}, []
    for name, wave, rid, res in batches:
        plan = dict(head); plan.update(batch=name, kind="gated (G-B pilot set; self-release per HQ H-38)", max_task_hours=2.0, resources=res, island_throttle=8, fits=[new[rid]])
        wc = p1m_driver.resolve(dict(plan, core_h_cap=1e12))["worst_case_core_h"]
        plan["core_h_cap"] = math.ceil((wc + 0.05) * 10 - 1e-9) / 10
        plan = {k: plan[k] for k in ("batch", "mode", "code_commit", "method_tag", "core_tree", "binary", "max_task_hours", "island_isa", "kind", "island_throttle", "core_h_cap", "resources", "fits") if k in plan}
        pf = os.path.join(a.out, "plans", name + ".json")
        json.dump(plan, open(pf, "w"), indent=1); open(pf, "a").write("\n")
        sd = os.path.join(a.out, "scripts", name)
        d = subprocess.run([sys.executable, os.path.join(slurm, "p1m_driver.py"), "--plan", pf, "--out", sd, "--dept", a.dept, "--strict"], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        if d.returncode:
            sys.exit("driver --strict failed for %s: %s%s" % (name, d.stdout, d.stderr))
        resd = json.load(open(os.path.join(sd, "plan.resolved.json")))
        assert not resd.get("warnings"), resd.get("warnings")
        # EXPLICIT N / m / I_max in every generated manifest that runs the method (the silent-default guard): the run manifest and the calibrate, island, merge and setup
        # stage manifests must each carry all three keys with the planned values (a missing key = the engine default would apply = FAIL); gen / eval / post do not take them
        f = new[rid]; want = {"N": N_STAR, "refine_m": 1, "I_max": f["params"]["I_max"]}
        bad, stage_ok = [], 0
        rm = glob.glob(os.path.join(sd, "run_manifests", "*.json"))
        assert len(rm) == 1, rm
        mans = [("run_manifest", json.load(open(rm[0]))["params"])]
        sdir = glob.glob(os.path.join(sd, "manifests", "*"))
        assert len(sdir) == 1, sdir
        for st in ("setup", "calibrate", "island", "merge"):
            mans.append((st, json.load(open(os.path.join(sdir[0], st + ".json")))["params"]))
        for lab, pr in mans:
            for k, v in want.items():
                if pr.get(k) != v:
                    bad.append((lab, k, pr.get(k), v))
            stage_ok += lab != "run_manifest"
        if bad:
            sys.exit("EXPLICIT-ARM CHECK FAILED for %s: %s" % (name, bad))
        peak = min(8, 16) * res["islands"]["cpus"]
        wj[name] = {"wave": wave, "plan_sha256": hashlib.sha256(open(pf, "rb").read()).hexdigest(), "tasks": resd["n_tasks"], "worst_case_core_h": resd["worst_case_core_h"], "core_h_cap": plan["core_h_cap"],
                    "fit": {k: f[k] for k in ("run_id", "design", "p", "n", "Rp", "N", "seed", "data_seed")} | {"params": f["params"]}, "explicit_arm_checked": {"want": want, "run_manifest_and_stage_manifests": ["run_manifest", "setup", "calibrate", "island", "merge"]}}
        table.append((wave, name, rid, resd["n_tasks"], resd["worst_case_core_h"], plan["core_h_cap"], peak, stage_ok))
    json.dump(wj, open(os.path.join(a.out, "waves_gb.json"), "w"), indent=1)
    print("%-3s %-8s %-26s %5s %9s %9s %8s %s" % ("wv", "batch", "run_id", "tasks", "worst", "cap", "peakCPU", "stage manifests with explicit arm"))
    for t in table:
        print("%-3s %-8s %-26s %5d %9.1f %9.1f %8d %d" % t)
    print("sets: 4 fits, 4 batches, %d tasks, worst (limit sum) %.1f core-h" % (sum(t[3] for t in table), sum(t[4] for t in table)))


if __name__ == "__main__":
    main()
