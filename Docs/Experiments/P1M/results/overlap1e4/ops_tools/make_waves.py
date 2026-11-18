#!/usr/bin/env python3
"""make_waves.py -- build the 10^4 T-vs-V overlap wave plans (OV_W<k>_<T|V>) from p1m_cells.py's generated overlap plans.

OPS tool of the overlap rung (OVERLAP_1e4_SUBMISSION_PLAN §1-§2, DECISIONS H-18). Writes plans only; never submits, never ssh.
Stdlib only. Run from anywhere:

  make_waves.py --wt <worktree of the freeze head> --code-commit <F> --out <dir> [--waves W0,W1] [--dept /home/fb31/SMC_Engineering_Department]

Steps: (1) p1m_cells.py --plans <out>/gen --only 1e4 --code-commit F (verifies the method pin); (2) per wave and arm, pick the
fits by run_id from the generated plans, force the T-arm definition (law mode, N = 10^4, R' = 4: plan §1) and the resource
shapes of plan §2, set core_h_cap = the batch worst case rounded UP to 0.1 (after +0.05, the generator's rule); (3) resolve with the driver --strict into
<out>/scripts/OV_W<k>_<T|V>/ (dry run) and print the worst cases. The batch id is flat (OV_W0_T): the driver's safe_id forbids '/'.
"""
import argparse, json, math, os, subprocess, sys

DEPT = "/home/fb31/SMC_Engineering_Department"
# plan §1: fits per wave as (run_id tag, rep, seeds); each fit is run in both arms
WAVES = {
    "W0": [("AR", 1, (1,)), ("ADJOPP", 1, (1,))],
    "W1": [("IND", 1, (1, 2)), ("NULL", 1, (1, 2)), ("ARweak", 1, (1, 2))],
    "W2": [("ARweak", 2, (1, 2)), ("ADJOPP", 1, (2,)), ("ADJOPP", 2, (1, 2)), ("AR", 1, (2,))],
    "W3": [("AR", 2, (1, 2)), ("AR", 3, (1, 2)), ("AR", 4, (1, 2))],
}
# plan §2 resource shapes (billed CPUs = allocated threads). W1-W3 are re-sized after W0 by a measured-based override file.
SHAPES = {
    "V": {"setup": {"cpus": 8, "mem": "8G", "time": "00:15:00"}, "calibrate": {"cpus": 16, "mem": "8G", "time": "00:30:00"},
          "islands": {"cpus": 4, "mem": "4G", "time": "00:30:00"}, "merge": {"cpus": 8, "mem": "4G", "time": "00:15:00"},
          "eval": {"cpus": 8, "mem": "8G", "time": "00:20:00"}},
    "T": {"setup": {"cpus": 8, "mem": "8G", "time": "00:15:00"}, "calibrate": {"cpus": 48, "mem": "16G", "time": "03:00:00"},
          "islands": {"cpus": 24, "mem": "16G", "time": "00:45:00"}, "merge": {"cpus": 8, "mem": "8G", "time": "00:20:00"},
          "eval": {"cpus": 8, "mem": "8G", "time": "00:30:00"}},
}
T_ARM = {"N": 10000, "Rp": 4}          # plan §1: N = max(2500, n, p) = 10^4, R' = 4 (EXPERIMENT_PLAN A1, D-26)
MAX_TASK_H = {"V": 2.0, "T": 3.0}      # H-18 (b): one-off exception to the 2-h task rule for T calibrate (3 h)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--wt", required=True); ap.add_argument("--code-commit", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--waves", default="W0"); ap.add_argument("--dept", default=DEPT)
    ap.add_argument("--arms", default="T,V", help="batch arms to write: T, V, or a rebuild T2 / V2 (= the T / V fits and shapes in a fresh batch "
                    "OV_<wave>_T2 / _V2, built from the git clone of F; fresh run dirs). Default T,V.")
    ap.add_argument("--shapes", help="JSON file {T: {...}, V: {...}} replacing the plan-§2 shapes (post-W0 re-size)")
    a = ap.parse_args()
    slurm = os.path.join(a.wt, "Scripts/SMC_BVS/engine_v4/tools/slurm")
    sys.path.insert(0, slurm); sys.dont_write_bytecode = True
    import p1m_driver
    shapes = json.load(open(a.shapes)) if a.shapes else SHAPES
    gen = os.path.join(a.out, "gen")
    r = subprocess.run([sys.executable, os.path.join(slurm, "p1m_cells.py"), "--plans", gen, "--only", "1e4", "--code-commit", a.code_commit],
                       capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    print(r.stdout.strip());
    if r.returncode: sys.exit("p1m_cells failed: " + r.stderr)
    fits, head = {}, {}
    for fn in sorted(os.listdir(gen)):
        if not fn.startswith("overlap1e4_"):
            continue
        p = json.load(open(os.path.join(gen, fn)))
        head[p["mode"]] = {k: v for k, v in p.items() if k not in ("fits", "batch", "core_h_cap")}
        for f in p["fits"]:
            fits[f["run_id"]] = f
    assert len(fits) == 40, "expected 40 overlap fits, got %d" % len(fits)
    g = fits["4-AR-n200-r01-T-s1"]
    print("GENERATOR T arm (what the freeze branch emits): N=%s Rp=%s; plan keys: %s; max_task_hours=%s -> %s"
          % (g["N"], g["Rp"], sorted(k for k in head["law"] if k in ("resources", "island_isa")), head["law"]["max_task_hours"],
             "T-arm fix PRESENT in p1m_cells.py" if (g["N"], g["Rp"]) == (10000, 4) else "T-arm fix MISSING in p1m_cells.py (overridden here by make_waves T_ARM; the freeze PR must carry it)"))
    os.makedirs(os.path.join(a.out, "plans"), exist_ok=True)
    rows = []
    for wave in a.waves.split(","):
        for barm in a.arms.split(","):
            arm = barm[0]                       # T2 -> T, V2 -> V: same fits, same shapes, same caps
            sel = []
            for tag, rep, seeds in WAVES[wave]:
                for s in seeds:
                    rid = "4-%s-n200-r%02d-%s-s%d" % (tag, rep, arm, s)
                    f = dict(fits[rid])
                    if arm == "T":
                        f.update(T_ARM)
                    else:
                        assert f["N"] == 2500 and f["Rp"] == 16, f
                    sel.append(f)
            plan = dict(head["law" if arm == "T" else "V"])
            plan.update(batch="OV_%s_%s" % (wave, barm), kind="gated (HQ H-18, overlap 1e4 %s %s)" % (wave, barm),
                        max_task_hours=MAX_TASK_H[arm], resources=shapes[arm], fits=sel)
            wc = p1m_driver.resolve(dict(plan, core_h_cap=1e12))["worst_case_core_h"]
            plan["core_h_cap"] = math.ceil((wc + 0.05) * 10 - 1e-9) / 10   # resolve() rounds wc to 0.1 (449.33 -> 449.3): +0.05 as p1m_cells does
            plan = {k: plan[k] for k in ("batch", "mode", "code_commit", "method_tag", "core_tree", "binary", "max_task_hours",
                                         "island_isa", "kind", "core_h_cap", "resources", "fits") if k in plan}
            pf = os.path.join(a.out, "plans", plan["batch"] + ".json")
            json.dump(plan, open(pf, "w"), indent=1); open(pf, "a").write("\n")
            sd = os.path.join(a.out, "scripts", plan["batch"])
            d = subprocess.run([sys.executable, os.path.join(slurm, "p1m_driver.py"), "--plan", pf, "--out", sd, "--dept", a.dept, "--strict"],
                               capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            if d.returncode:
                sys.exit("driver --strict failed for %s: %s%s" % (plan["batch"], d.stdout, d.stderr))
            res = json.load(open(os.path.join(sd, "plan.resolved.json")))
            rows.append((plan["batch"], len(sel), res["n_tasks"], res["worst_case_core_h"], plan["core_h_cap"], res.get("warnings")))
            print("%s: %d fits, %d tasks, worst %.1f core-h, cap %.1f, warnings %s" % rows[-1])
    print("sum of worst cases: %.1f core-h" % sum(r[3] for r in rows))


if __name__ == "__main__":
    main()
