#!/usr/bin/env python3
"""make_waves_vn.py -- plans of the V-N mini-leg (results/vn_minileg/MINILEG_PLAN.md) from the F2 tools. OPS tool; writes plans and a dry-run script tree only; never submits,
never ssh. Stdlib only. The generator (p1m_cells.py at F2) is NOT modified; the corrections are applied here, as make_waves_prec.py did for the precision leg.

  make_waves_vn.py --wt <worktree of F2 = e993ece2> --code-commit e993ece226b355058e26400f05f9faad6daf16ca --out <dir> [--dept /home/fb31/SMC_Engineering_Department]

Fits (15; MINILEG_PLAN section 2): the 12 held N = 10^4 fits mapped to the frozen configuration, XB2, and the r04 check.
  N = 10^4, m 1, I_max 3 (6 fits; the registered precision_freeze.py scores them verbatim) and N = 10^4, m 1, I_max 0 (6 fits; the FROZEN configuration). 3 datasets x 2 replicates.
  PAIRED SEEDS: each N = 10^4 fit takes the engine seed of its N = 2,500 twin from the precision leg (I_max 3: k = 10, 11; I_max 0: k = 18, 19), so calibration (H = 512, N-independent,
  D-26) reproduces the twin's grid bit for bit and the contrast isolates the final islands' N. (The generator's seeds k = 14..17 for these arms are not used.)
  XB2: the leg fit 4-AR-n200-r01-P-N2500-m1-I0-c1-s1 re-run on F2 (same seed, N 2,500), compared bit for bit with the F record.
  r04 (HQ H-33 (1), report-only): the I_max = 3 twin of 4-ADJOPP-n200-r04-V-s1 (tag VI3) and a seed-2 I_max = 0 fit (4-ADJOPP-n200-r04-V-s2). R' 16, N 2,500.
The m = 4 held arms (6 fits) are NOT planned: m is frozen at 1 (precision freeze, KEEP).
"""
import argparse, hashlib, json, math, os, subprocess, sys

DEPT = "/home/fb31/SMC_Engineering_Department"
S16 = {"setup": ("8", "8G", "00:15:00"), "calibrate": ("16", "8G", "00:30:00"), "islands": ("4", "4G", "00:30:00"), "merge": ("8", "4G", "00:15:00"), "eval": ("8", "8G", "00:20:00")}


def shape(**over):
    s = dict(S16); s.update(over)
    return {k: {"cpus": int(v[0]), "mem": v[1], "time": v[2]} for k, v in s.items()}


# islands limit set EXPLICITLY (PR #88 F7: the driver's DEFAULT_RES do not scale with N): measured N = 10^4 island on 4 CPUs ~ 4.5 min at T = 20 (Owls), 3.85 x the N = 2,500 island;
# T up to ~30 for AR/ADJ-OPP, so 0:45 is >= 5 x. precision-leg shapes otherwise (R' = 64: merge 16G).
SHAPES = {"vn": shape(setup=("8", "8G", "00:10:00"), calibrate=("16", "8G", "00:20:00"), islands=("4", "4G", "00:45:00"), merge=("8", "16G", "00:20:00"), eval=("8", "8G", "00:15:00")),
          "prec": shape(setup=("8", "8G", "00:10:00"), calibrate=("16", "8G", "00:20:00"), islands=("4", "4G", "00:30:00"), merge=("8", "16G", "00:20:00"), eval=("8", "8G", "00:15:00")),
          "s200": shape()}
THROTTLE = {"vn": 32, "prec": 32, "s200": 8}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--wt", required=True); ap.add_argument("--code-commit", required=True); ap.add_argument("--out", required=True); ap.add_argument("--dept", default=DEPT)
    a = ap.parse_args()
    gen = os.path.join(a.out, "gen")
    slurm = os.path.join(a.wt, "Scripts/SMC_BVS/engine_v4/tools/slurm")
    r = subprocess.run([sys.executable, os.path.join(slurm, "p1m_cells.py"), "--plans", gen, "--only", "1e4", "--code-commit", a.code_commit], capture_output=True, text=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    if r.returncode:
        sys.exit("p1m_cells failed: " + r.stdout + r.stderr)
    sys.path.insert(0, slurm); sys.dont_write_bytecode = True
    import p1m_driver
    fits, head = {}, None
    for fn in sorted(os.listdir(gen)):
        p = json.load(open(os.path.join(gen, fn)))
        if fn.startswith(("precision", "science1e4")):
            head = head or {k: v for k, v in p.items() if k not in ("fits", "batch", "core_h_cap", "kind", "resources", "max_task_hours")}
            fits.update({f["run_id"]: f for f in p["fits"]})
    assert head["mode"] == "V" and head.get("island_isa") == "sapphirerapids"
    new = {}
    for ds in ("AR", "ARweak", "ADJOPP"):
        for c in (1, 2):
            base = lambda I: "4-%s-n200-r01-P-N2500-m1%s-c%d-s1" % (ds, "-I0" if I == 0 else "", c)
            for I in (3, 0):
                tw = fits[base(3)] if I == 3 else None
                src = dict(fits["4-%s-n200-r01-P-N10000-m1-c%d-s1" % (ds, c)])                   # N 10^4, R' 64 (generator arm a4 / a5)
                src["run_id"] = "4-%s-n200-r01-P-N10000-m1%s-c%d-s1" % (ds, "-I0" if I == 0 else "", c)
                src["seed"] = src["data_seed"] + 100 * (10 + c - 1 if I == 3 else 18 + c - 1)    # PAIRED with the N = 2,500 twin of the precision leg
                src["params"] = {"refine_m": 1, "I_max": I}
                assert src["N"] == 10000 and src["Rp"] == 64
                new[src["run_id"]] = src
    xb = dict(fits["4-AR-n200-r01-P-N2500-m1-c1-s1"]); xb["run_id"] = "4-AR-n200-r01-P-N2500-m1-I0-XB2-s1"; xb["seed"] = xb["data_seed"] + 1800; xb["params"] = {"refine_m": 1, "I_max": 0}
    new[xb["run_id"]] = xb
    s1 = dict(fits["4-ADJOPP-n200-r04-V-s1"]); assert s1["Rp"] == 16 and s1["N"] == 2500
    t = dict(s1); t["run_id"] = "4-ADJOPP-n200-r04-VI3-s1"; t["params"] = {"refine_m": 1, "I_max": 3}
    u = dict(s1); u["run_id"] = "4-ADJOPP-n200-r04-V-s2"; u["seed"] = s1["data_seed"] + 100; u["params"] = {"refine_m": 1, "I_max": 0}
    new[t["run_id"]] = t; new[u["run_id"]] = u
    assert len(new) == 15
    N4 = lambda ds, I, c: "4-%s-n200-r01-P-N10000-m1%s-c%d-s1" % (ds, "-I0" if I == 0 else "", c)
    waves = {"V0": [([N4("AR", 0, 1), N4("AR", 3, 1)], "vn"), (["4-AR-n200-r01-P-N2500-m1-I0-XB2-s1"], "prec"), (["4-ADJOPP-n200-r04-VI3-s1", "4-ADJOPP-n200-r04-V-s2"], "s200")],
             "V1": [([N4("AR", 0, 2), N4("AR", 3, 2)], "vn"), ([N4("ARweak", 0, 1), N4("ARweak", 0, 2)], "vn")],
             "V2": [([N4("ARweak", 3, 1), N4("ARweak", 3, 2)], "vn"), ([N4("ADJOPP", 0, 1), N4("ADJOPP", 0, 2)], "vn"), ([N4("ADJOPP", 3, 1), N4("ADJOPP", 3, 2)], "vn")]}
    assert sorted(r for w in waves.values() for b, _ in w for r in b) == sorted(new)
    os.makedirs(os.path.join(a.out, "plans"), exist_ok=True)
    table, wj = [], {}
    for w, bs in waves.items():
        wj[w] = {"batches": []}
        for i, (b, kl) in enumerate(bs, 1):
            name = "VN_%s_%d" % (w, i)
            plan = dict(head); plan.update(batch=name, kind="gated (V-N mini-leg; release per MINILEG_PLAN)", max_task_hours=2.0, resources=SHAPES[kl], island_throttle=THROTTLE[kl], fits=[new[x] for x in b])
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
            res = json.load(open(os.path.join(sd, "plan.resolved.json")))
            rs = SHAPES[kl]; peak = len(b) * max(rs["calibrate"]["cpus"], min(THROTTLE[kl], new[b[0]]["Rp"]) * rs["islands"]["cpus"])
            table.append((w, name, len(b), res["n_tasks"], res["worst_case_core_h"], plan["core_h_cap"], peak, res.get("warnings")))
            wj[w]["batches"].append({"batch": name, "plan_sha256": hashlib.sha256(open(pf, "rb").read()).hexdigest(), "tasks": res["n_tasks"], "worst_case_core_h": res["worst_case_core_h"],
                                     "core_h_cap": plan["core_h_cap"], "fits": [{k: new[x][k] for k in ("run_id", "design", "n", "Rp", "N", "seed", "data_seed")} | {"params": new[x]["params"]} for x in b]})
    json.dump(wj, open(os.path.join(a.out, "waves_vn.json"), "w"), indent=1)
    print("%-3s %-9s %5s %6s %9s %9s %8s  warnings" % ("wv", "batch", "fits", "tasks", "worst", "cap", "peakCPU"))
    for r in table:
        print("%-3s %-9s %5d %6d %9.1f %9.1f %8d  %s" % r)
    by = {}
    for r in table:
        x = by.setdefault(r[0], [0, 0, 0, 0.0, 0]); x[0] += 1; x[1] += r[2]; x[2] += r[3]; x[3] += r[4]; x[4] += r[6]
    print("\nper wave: batches fits tasks worst(limit sum) peakCPU(sum of batches)")
    for w, x in by.items():
        print("%-3s %d %2d %4d %8.1f %d" % ((w,) + tuple(x)))
    print("total fits %d, batches %d" % (sum(x[1] for x in by.values()), sum(x[0] for x in by.values())))


if __name__ == "__main__":
    main()
