#!/usr/bin/env python3
"""make_gc_plan.py -- the G-C / 1M plans (results/gc1m/GC_PLAN.md) from the F2 tools. OPS tool: writes plans and a dry-run script tree only; never submits, never ssh.
Stdlib only. The generator (p1m_cells.py at F2) is NOT modified: it emits no I_max, N 2,500 and plan-value shapes; the corrections are applied here (as make_rung_plan.py did).

  make_gc_plan.py --wt <worktree of F2 = e993ece2> --code-commit e993ece226b355058e26400f05f9faad6daf16ca --out <dir> [--dept /home/fb31/SMC_Engineering_Department]

Every fit: F2, m 1, I_max 0, R' 16, class A, bounded calibration, resampling off ("not tested"); explicit top-level N and params {refine_m, I_max}; after the driver runs, the run manifest and the
setup / calibrate / island / merge stage manifests of EVERY fit are read back and asserted to carry the planned N, refine_m = 1, I_max = 0.
Batches (2 fits per batch = "2 fits at a time"; <= 150 tasks; every task <= 2 h):
  GC_P   the G-C2 pilot = the FROZEN rep-1 re-run `6-AR-n200-r01-V-s1` (data + engine seed 602020001; run ALONE first)
  GC_W1  AR r02 + ADJ-OPP r01 | GC_W2 .. GC_W10  AR r03..r20 in pairs   (S2: AR-strong replicates 2-20, ADJ-OPP x 1)
  GC_X1a AR-weak r01 (gated, H-10) | GC_X1b the ONE N 10^4 fit on the rep-1 data `6-AR-n200-r01-VN10K-s1` (pairs with the pilot; calibration identical by pairing)
  GC_D   option D: AR-strong n = 1,000 `6-AR-n1000-r01-V-s1` (D1-D3 passed; RELEASED by HQ H-44; runs ALONE after the pilot is clean and the n = 1,000 --plan-only gate)
  GC_S1 .. GC_S10   the conditional 20 SEEDS (H-34): seeds 2..20 on the rep-1 data, `6-AR-n200-r01-V-s<i>`, engine seed = data seed + 100 (i - 1); seed 1 = the pilot (no double cost)
  GC_N5  the N 5,000 self-check `6-AR-n200-r01-VN5K-s1` (NOT in S2: H-38 replaced it by the N 10^4 fit; generated as an option only)
Shapes (GB_PLAN / RUNG_PLAN conventions, measured 11-17 at 10^6): setup 48 CPU 48 G; calibrate 96 CPU 128 G; islands 96 CPU 64 G; merge 32 CPU 128 G (until a 1M `peak_rss_kb` is read); eval 8 CPU 16 G.
"""
import argparse, glob, hashlib, json, math, os, subprocess, sys

DEPT = "/home/fb31/SMC_Engineering_Department"


def shape(setup=("48", "48G", "00:45:00"), cal=("96", "128G", "01:30:00"), isl=("96", "64G", "01:00:00"), merge=("32", "128G", "01:30:00"), ev=("8", "16G", "01:00:00")):
    f = lambda t: {"cpus": int(t[0]), "mem": t[1], "time": t[2]}
    return {"setup": f(setup), "calibrate": f(cal), "islands": f(isl), "merge": f(merge), "eval": f(ev)}


STD = shape()
N10K = shape(isl=("96", "64G", "01:30:00"))
# option D (n = 1,000; HQ H-44 released): the correlation pass dominates setup and does not scale with threads (WP2 count-only at 10^6: 4,069 s at 3 threads for n = 1,000, 897 s for n = 200; the 11-17 setup at 48 threads took 780 s for
# n = 200), so 48 CPUs for <= 1:45 (billed ~55 core-h, not 96 CPUs); islands at 2-3.4x the n = 200 wall (13 min) get 1:30; every task <= 2 h
# eval at n = 1,000 reads an 8 GB data.bin (1.6 GB at n = 200): 32 G (Opus G-C check; memory is not billed)
OPTD = shape(setup=("48", "64G", "01:45:00"), cal=("96", "128G", "02:00:00"), isl=("96", "64G", "01:30:00"), ev=("8", "32G", "01:00:00"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--wt", required=True); ap.add_argument("--code-commit", required=True); ap.add_argument("--out", required=True); ap.add_argument("--dept", default=DEPT)
    a = ap.parse_args()
    gen = os.path.join(a.out, "gen")
    slurm = os.path.join(a.wt, "Scripts/SMC_BVS/engine_v4/tools/slurm")
    r = subprocess.run([sys.executable, os.path.join(slurm, "p1m_cells.py"), "--plans", gen, "--only", "1e6", "--code-commit", a.code_commit], capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    if r.returncode:
        sys.exit("p1m_cells failed: " + r.stdout + r.stderr)
    sys.path.insert(0, slurm); sys.dont_write_bytecode = True
    import p1m_driver
    fits, head = {}, None
    for fn in sorted(os.listdir(gen)):
        p = json.load(open(os.path.join(gen, fn)))
        head = head or {k: v for k, v in p.items() if k not in ("fits", "batch", "core_h_cap", "kind", "resources", "max_task_hours")}
        fits.update({f["run_id"]: f for f in p["fits"]})
    assert head["mode"] == "V" and head.get("island_isa") == "sapphirerapids" and head["code_commit"] == a.code_commit
    ar1 = fits["6-AR-n200-r01-V-s1"]
    assert ar1["data_seed"] == 602020001 and ar1["seed"] == 602020001 and ar1["p"] == 1000000 and ar1["n"] == 200 and ar1["Rp"] == 16

    def mk(src, rid, N=2500, seed=None):
        f = dict(src); f["run_id"] = rid; f["N"] = N; f["params"] = {"refine_m": 1, "I_max": 0}
        if seed is not None:
            f["seed"] = seed
        return f
    ar = lambda r: mk({**ar1, "data_seed": 602020000 + r, "seed": 602020000 + r}, "6-AR-n200-r%02d-V-s1" % r)
    pilot = mk(ar1, "6-AR-n200-r01-V-s1")
    adj = mk(fits["6-ADJOPP-n200-r01-V-s1"], "6-ADJOPP-n200-r01-V-s1")
    weak = mk(fits["6-ARweak-n200-r01-V-s1"], "6-ARweak-n200-r01-V-s1")
    n10k = mk(ar1, "6-AR-n200-r01-VN10K-s1", N=10000)
    n5k = mk(ar1, "6-AR-n200-r01-VN5K-s1", N=5000)
    optd = mk(fits["6-AR-n1000-r01-V-s1"], "6-AR-n1000-r01-V-s1")
    B = [("GC_P", "P", [pilot], STD)]
    reps = [ar(r) for r in range(2, 21)]
    B.append(("GC_W1", "W1", [reps[0], adj], STD))
    rest = reps[1:]
    assert len(rest) == 18
    for i in range(9):
        B.append(("GC_W%d" % (i + 2), "W%d" % (i + 2), rest[2 * i:2 * i + 2], STD))
    B += [("GC_X1a", "X1", [weak], STD), ("GC_X1b", "X1", [n10k], N10K), ("GC_D", "D", [optd], OPTD)]
    seeds = [mk(ar1, "6-AR-n200-r01-V-s%d" % i, seed=602020001 + 100 * (i - 1)) for i in range(2, 21)]
    for j in range(10):
        B.append(("GC_S%d" % (j + 1), "S%d" % (j + 1), seeds[2 * j:2 * j + 2], STD))
    B.append(("GC_N5", "opt", [n5k], STD))
    # seed hygiene: run ids unique; engine seeds on dataset 602020001 are exactly data_seed + 100 k, k = 0..19 (k = 0 pilot), and the intended shared pairs only
    allf = [f for _, _, fl, _ in B for f in fl]
    assert len({f["run_id"] for f in allf}) == len(allf)
    s_r1 = sorted(f["seed"] for f in allf if f["data_seed"] == 602020001 and f["N"] == 2500)
    assert s_r1 == [602020001 + 100 * k for k in range(20)], s_r1
    assert all(f["seed"] in (f["data_seed"], ) or f["data_seed"] == 602020001 for f in allf)
    os.makedirs(os.path.join(a.out, "plans"), exist_ok=True)
    wj, table = {}, []
    for name, wave, fl, res in B:
        plan = dict(head); plan.update(batch=name, kind="gated (G-C / 1M; release per GC_PLAN)", max_task_hours=2.0, resources=res, island_throttle=16, fits=fl)
        wc = p1m_driver.resolve(dict(plan, core_h_cap=1e12))["worst_case_core_h"]
        plan["core_h_cap"] = math.ceil((wc + 0.05) * 10 - 1e-9) / 10
        plan = {k: plan[k] for k in ("batch", "mode", "code_commit", "method_tag", "core_tree", "binary", "max_task_hours", "island_isa", "kind", "island_throttle", "core_h_cap", "resources", "fits") if k in plan}
        pf = os.path.join(a.out, "plans", name + ".json")
        json.dump(plan, open(pf, "w"), indent=1); open(pf, "a").write("\n")
        sd = os.path.join(a.out, "scripts", name)
        d = subprocess.run([sys.executable, os.path.join(slurm, "p1m_driver.py"), "--plan", pf, "--out", sd, "--dept", a.dept, "--strict"], capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        if d.returncode:
            sys.exit("driver --strict failed for %s: %s%s" % (name, d.stdout, d.stderr))
        resd = json.load(open(os.path.join(sd, "plan.resolved.json")))
        assert not resd.get("warnings"), resd.get("warnings")
        bad, nchk = [], 0
        for f in fl:
            want = {"N": f["N"], "refine_m": 1, "I_max": 0}
            rm = json.load(open(os.path.join(sd, "run_manifests", f["run_id"] + ".json")))["params"]
            mans = [("run_manifest", rm)] + [(st, json.load(open(os.path.join(sd, "manifests", f["run_id"], st + ".json")))["params"]) for st in ("setup", "calibrate", "island", "merge")]
            for lab, pr in mans:
                nchk += 1
                for k, v in want.items():
                    if pr.get(k) != v:
                        bad.append((f["run_id"], lab, k, pr.get(k), v))
                if lab == "run_manifest" and pr.get("seed") != f["seed"]:
                    bad.append((f["run_id"], lab, "seed", pr.get("seed"), f["seed"]))
        if bad:
            sys.exit("EXPLICIT-ARM CHECK FAILED for %s: %s" % (name, bad[:6]))
        shp = res["islands"]
        wj[name] = {"wave": wave, "plan_sha256": hashlib.sha256(open(pf, "rb").read()).hexdigest(), "tasks": resd["n_tasks"], "worst_case_core_h": resd["worst_case_core_h"], "core_h_cap": plan["core_h_cap"],
                    "island_cpus": shp["cpus"], "island_limit": shp["time"], "fits": [{k: f[k] for k in ("run_id", "design", "p", "n", "Rp", "N", "seed", "data_seed")} | {"params": f["params"]} for f in fl], "explicit_arm_manifests_checked": nchk}
        table.append((wave, name, len(fl), resd["n_tasks"], resd["worst_case_core_h"], plan["core_h_cap"]))
    json.dump(wj, open(os.path.join(a.out, "waves_gc.json"), "w"), indent=1)
    print("%-4s %-8s %4s %6s %9s %9s" % ("wv", "batch", "fits", "tasks", "worst", "cap"))
    for t in table:
        print("%-4s %-8s %4d %6d %9.1f %9.1f" % t)
    s2 = [t for t in table if t[0] not in ("opt",) and not t[0].startswith("S")]
    print("S2 (no seeds, no N5): %d fits, %d batches, %d tasks, worst (limit sum) %.1f" % (sum(t[2] for t in s2), len(s2), sum(t[3] for t in s2), sum(t[4] for t in s2)))
    ss = [t for t in table if t[0].startswith("S")]
    print("H-34 seed block: %d fits, %d batches, %d tasks, worst %.1f" % (sum(t[2] for t in ss), len(ss), sum(t[3] for t in ss), sum(t[4] for t in ss)))


if __name__ == "__main__":
    main()
