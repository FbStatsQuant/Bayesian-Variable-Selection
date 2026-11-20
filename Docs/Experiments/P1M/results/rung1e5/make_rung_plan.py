#!/usr/bin/env python3
"""make_rung_plan.py -- the 10^5 RUNG plans (results/rung1e5/RUNG_PLAN.md) from the F2 tools. OPS tool: writes plans and a dry-run script tree only; never submits, never ssh.
Stdlib only. The generator (p1m_cells.py at F2) is NOT modified: it emits no I_max and N 2,500 for 10^5; the corrections are applied here (as make_gb_plan.py did).

  make_rung_plan.py --wt <worktree of F2 = e993ece2> --code-commit e993ece226b355058e26400f05f9faad6daf16ca --out <dir> [--dept /home/fb31/SMC_Engineering_Department]

Fits (HQ H-40): the REMAINING 10 of the 12 MANIFEST rung fits at (F2, N 10^4, m 1, I_max 0, R' 16); the 2 other rung fits are the G-B pilots (AR r01 = GB_G1a, ADJ-OPP r01 = GB_G2a, done):
  AR n200 r02..r05 (RG_2a) | AR n400 r01 (RG_1a, the n-scaling pilot) and r02..r03 (RG_2b) | IND n200 r01..r02 (RG_3a) | ADJ-OPP n200 r02 (RG_3b)
plus the 2 CONTINUITY TWINS (report-only) at N 2,500, I_max 0 on the SAME data and seeds as the pilots AR r01 / ADJ-OPP r01 (RG_1b; arm tag VN25, outside the registered patterns):
  5-AR-n200-r01-VN25-s1, 5-ADJOPP-n200-r01-VN25-s1
plus two forced-kill restart test (T6) batches, ONE of which is submitted: RG_T6 (source = the G-B pilot's inputs, GB_G1a) or the fallback RG_T6b (source = RG_1a's AR n400 r01 inputs).
EXPLICIT params in every fit (top-level N; params {refine_m, I_max}); after the driver runs, the run manifest and the setup / calibrate / island / merge stage manifests of every fit are
read back and asserted to carry the planned N, refine_m = 1 and I_max = 0. T6 plans are t6_only (one task; the driver's p1m_t6.py kills by PID inside the job).
Island arrays are throttled per batch (peak CPUs per wave stay under the 1,536 QOS cap).
"""
import argparse, glob, hashlib, json, math, os, subprocess, sys

DEPT = "/home/fb31/SMC_Engineering_Department"


def shape(cal="00:30:00", isl="00:45:00", cpus_isl=48, mem_isl="12G"):
    return {"setup": {"cpus": 32, "mem": "16G", "time": "00:30:00"}, "calibrate": {"cpus": 64, "mem": "16G", "time": cal},
            "islands": {"cpus": cpus_isl, "mem": mem_isl, "time": isl}, "merge": {"cpus": 16, "mem": "24G", "time": "00:30:00"}, "eval": {"cpus": 8, "mem": "16G", "time": "00:45:00"}}


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
    assert len(fits) == 12 and head["mode"] == "V" and head.get("island_isa") == "sapphirerapids" and head["code_commit"] == a.code_commit

    def mk(rid, N=10000, tag=None):
        f = dict(fits[rid]); assert f["p"] == 100000 and f["Rp"] == 16 and f["seed"] == f["data_seed"]
        f["N"] = N; f["params"] = {"refine_m": 1, "I_max": 0}
        if tag:
            f["run_id"] = rid.replace("-V-s1", "-%s-s1" % tag)
        return f
    ids = lambda d, n, rs: ["5-%s-n%d-r%02d-V-s1" % (d, n, r) for r in rs]
    # (batch, wave, fit ids, N, tag, shape, throttle)
    B = [("RG_1a", "R1", ids("AR", 400, [1]), 10000, None, shape("00:30:00", "01:00:00"), 8),
         ("RG_1b", "R1", ["5-AR-n200-r01-V-s1", "5-ADJOPP-n200-r01-V-s1"], 2500, "VN25", shape("00:30:00", "00:20:00"), 8),
         ("RG_2a", "R2", ids("AR", 200, [2, 3, 4, 5]), 10000, None, shape("00:30:00", "00:45:00"), 12),
         ("RG_2b", "R2", ids("AR", 400, [2, 3]), 10000, None, shape("00:30:00", "01:00:00"), 8),
         ("RG_3a", "R3", ids("IND", 200, [1, 2]), 10000, None, shape("00:30:00", "01:00:00"), 8),
         ("RG_3b", "R3", ["5-ADJOPP-n200-r02-V-s1"], 10000, None, shape("00:30:00", "01:00:00"), 8)]
    os.makedirs(os.path.join(a.out, "plans"), exist_ok=True)
    wj, table = {}, []

    def gen_scripts(name, plan):
        pf = os.path.join(a.out, "plans", name + ".json")
        json.dump(plan, open(pf, "w"), indent=1); open(pf, "a").write("\n")
        sd = os.path.join(a.out, "scripts", name)
        d = subprocess.run([sys.executable, os.path.join(slurm, "p1m_driver.py"), "--plan", pf, "--out", sd, "--dept", a.dept, "--strict"], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        if d.returncode:
            sys.exit("driver --strict failed for %s: %s%s" % (name, d.stdout, d.stderr))
        resd = json.load(open(os.path.join(sd, "plan.resolved.json")))
        assert not resd.get("warnings"), resd.get("warnings")
        return pf, sd, resd

    for name, wave, rids, N, tag, res, thr in B:
        fl = [mk(x, N, tag) for x in rids]
        plan = dict(head); plan.update(batch=name, kind="gated (10^5 rung; self-release per HQ H-40)", max_task_hours=2.0, resources=res, island_throttle=thr, fits=fl)
        wc = p1m_driver.resolve(dict(plan, core_h_cap=1e12))["worst_case_core_h"]
        plan["core_h_cap"] = math.ceil((wc + 0.05) * 10 - 1e-9) / 10
        plan = {k: plan[k] for k in ("batch", "mode", "code_commit", "method_tag", "core_tree", "binary", "max_task_hours", "island_isa", "kind", "island_throttle", "core_h_cap", "resources", "fits") if k in plan}
        pf, sd, resd = gen_scripts(name, plan)
        # EXPLICIT N / m / I_max in every manifest that runs the method
        bad, nchk = [], 0
        for f in fl:
            want = {"N": N, "refine_m": 1, "I_max": 0}
            rm = json.load(open(os.path.join(sd, "run_manifests", f["run_id"] + ".json")))["params"]
            mans = [("run_manifest", rm)] + [(st, json.load(open(os.path.join(sd, "manifests", f["run_id"], st + ".json")))["params"]) for st in ("setup", "calibrate", "island", "merge")]
            for lab, pr in mans:
                nchk += 1
                for k, v in want.items():
                    if pr.get(k) != v:
                        bad.append((f["run_id"], lab, k, pr.get(k), v))
        if bad:
            sys.exit("EXPLICIT-ARM CHECK FAILED for %s: %s" % (name, bad[:6]))
        peak = thr * res["islands"]["cpus"]
        wj[name] = {"wave": wave, "plan_sha256": hashlib.sha256(open(pf, "rb").read()).hexdigest(), "tasks": resd["n_tasks"], "worst_case_core_h": resd["worst_case_core_h"], "core_h_cap": plan["core_h_cap"],
                    "island_throttle": thr, "peak_island_cpus": peak, "fits": [{k: f[k] for k in ("run_id", "design", "p", "n", "Rp", "N", "seed", "data_seed")} | {"params": f["params"]} for f in fl], "explicit_arm_manifests_checked": nchk}
        table.append((wave, name, len(fl), resd["n_tasks"], resd["worst_case_core_h"], plan["core_h_cap"], peak))
    # forced-kill restart test (T6): one task, kills by PID inside the job (p1m_t6.py); two alternative sources, ONE is submitted
    t6s = [("RG_T6", "GB_G1a", "5-AR-n200-r01-V-s1", 200), ("RG_T6b", "RG_1a", "5-AR-n400-r01-V-s1", 400)]
    for name, src, rid, n in t6s:
        f = mk(rid, 10000)
        plan = dict(head); plan.update(batch=name, kind="gate T6 at 1e5 (G-C item): restart by REAL kills (WP7 O4); one island of %s inputs; t6_only (HQ H-40)" % src, max_task_hours=2.0, t6_only=True,
                                       t6={"source_batch": src, "island": 1, "kills": 2, "ckpt_every_s": 60, "cpus": 48, "mem": "24G", "time": "01:30:00"}, resources={"setup": shape()["setup"]}, fits=[f])
        wc = 48 * 1.5
        plan["core_h_cap"] = math.ceil((wc + 0.05) * 10 - 1e-9) / 10
        plan = {k: plan[k] for k in ("batch", "mode", "code_commit", "method_tag", "core_tree", "binary", "max_task_hours", "island_isa", "kind", "core_h_cap", "t6_only", "t6", "resources", "fits") if k in plan}
        pf, sd, resd = gen_scripts(name, plan)
        assert os.path.isfile(os.path.join(sd, "stage_t6.sbatch")) and os.path.isfile(os.path.join(sd, "submit_t6.sh"))
        rp = json.load(open(os.path.join(sd, "run_manifests", rid + ".json")))["params"]
        assert rp["N"] == 10000 and rp["refine_m"] == 1 and rp["I_max"] == 0, rp
        wj[name] = {"wave": "R1", "plan_sha256": hashlib.sha256(open(pf, "rb").read()).hexdigest(), "tasks": resd["n_tasks"], "worst_case_core_h": resd["worst_case_core_h"], "core_h_cap": plan["core_h_cap"],
                    "t6": plan["t6"], "fit": {k: f[k] for k in ("run_id", "N", "seed", "data_seed")} | {"params": f["params"]}, "explicit_arm_checked": ["run_manifest"],
                    "submitted": "ONE of RG_T6 / RG_T6b (RG_T6 unless the G-B pilot's inputs are gone from NOTS scratch)"}
        table.append(("R1", name, 1, resd["n_tasks"], resd["worst_case_core_h"], plan["core_h_cap"], 48))
    json.dump(wj, open(os.path.join(a.out, "waves_rung.json"), "w"), indent=1)
    print("%-3s %-8s %4s %6s %9s %9s %8s" % ("wv", "batch", "fits", "tasks", "worst", "cap", "peakCPU"))
    for t in table:
        print("%-3s %-8s %4d %6d %9.1f %9.1f %8d" % t)
    live = [t for t in table if t[1] != "RG_T6b"]
    print("rung plans (RG_T6 chosen): %d fits + 1 T6 task, %d tasks, worst (limit sum) %.1f core-h" % (sum(t[2] for t in live if not t[1].startswith("RG_T6")), sum(t[3] for t in live), sum(t[4] for t in live)))


if __name__ == "__main__":
    main()
