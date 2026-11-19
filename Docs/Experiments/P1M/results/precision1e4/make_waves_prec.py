#!/usr/bin/env python3
"""make_waves_prec.py -- build the plans of the precision-study + 10^4-science leg (results/precision1e4/LEG_PLAN.md) from
p1m_cells.py's generated plans. OPS tool of the leg; writes plans and a dry-run script tree only; never submits, never ssh.
Stdlib only. Nothing in the engine or in tools/slurm is modified: the plan-side corrections below are applied HERE (the way
overlap1e4/ops_tools/make_waves.py forced the T arm), so the generator stays as committed.

  make_waves_prec.py --wt <worktree of the engine head> --code-commit <F, 40 hex> --out <dir> [--dept /home/fb31/SMC_Engineering_Department]

Corrections applied to the generator's fits (LEG_PLAN section 2; each one verified on the F-equivalent binary, section 1):
  C1  precision params {"grid_refine_m": m, "calib_seed": s} -> {"refine_m": m, "I_max": 3}. The engine reads `refine_m` and `I_max`
      (calib_run.cpp:133); `grid_refine_m` and `calib_seed` are read by nothing (a silent no-op: m = 4 would have run as m = 1).
      B1: F requires the island seed to equal the calibration's seed (island_cmd.cpp:221-222), so each arm has ONE seed, the
      final seed k = 10 + a (the manifest's calibration seed k = 20 + a is dropped).
  C2  new arms I_max = 0 (the OPEN item of MANIFEST_CELLS section 2): N = 2,500, m = 1, 2 replicates, arms a = 8, 9 (final seeds k = 18, 19).
  C3  A3 fits: partition "exact_linkage" -> "exact" (the engine accepts truncated | exact; "exact_linkage" is refused, setup_run.cpp:214-217).
  C4  explicit resource shapes (the generator's defaults are the 1e4 DEFAULT_RES: islands 16 CPUs x 15 min, 4x over-sized), island_throttle.
N = 10^4 arms (12 fits) are HELD (B2: V's N is the constant calib::V_N = 2500); they are written as waves H1-H3 and never submitted
without HQ's ruling on B2.
"""
import argparse, json, math, os, re, subprocess, sys

DEPT = "/home/fb31/SMC_Engineering_Department"
K_FINAL = 10
# resource shapes (cpus = billed threads; V overlap measured wall max: setup 16 s, calibrate 247 s, islands 111 s (T <= 21), merge 26 s, eval 16 s)
S16 = {"setup": ("8", "8G", "00:15:00"), "calibrate": ("16", "8G", "00:30:00"), "islands": ("4", "4G", "00:30:00"),
       "merge": ("8", "4G", "00:15:00"), "eval": ("8", "8G", "00:20:00")}
def shape(**over):
    s = dict(S16); s.update({k: v for k, v in over.items()})
    return {k: {"cpus": int(v[0]), "mem": v[1], "time": v[2]} for k, v in s.items()}
SHAPES = {
    "prec": shape(setup=("8", "8G", "00:10:00"), calibrate=("16", "8G", "00:20:00"), islands=("4", "4G", "00:30:00"),   # R'=64; m = 4 islands ~3x m = 1
                  merge=("8", "16G", "00:20:00"), eval=("8", "8G", "00:15:00")),
    "s100": shape(), "s200": shape(),
    "a3": shape(setup=("8", "16G", "00:30:00")),                                   # exact linkage at p = 10^4: unmeasured, canary first
    "s400": shape(calibrate=("16", "8G", "00:45:00"), islands=("4", "4G", "00:45:00")),
    "s800": shape(calibrate=("16", "16G", "01:00:00"), islands=("4", "8G", "01:00:00"), merge=("8", "8G", "00:20:00")),
}
THROTTLE = {"prec": 32, "s100": 8, "s200": 8, "a3": 8, "s400": 8, "s800": 8}   # island array %throttle: peak CPUs per wave stay < ~1,000 (QOS cap 1,536)
MAX_BATCH_TASKS, MAX_WAVE_BATCHES = 150, 4


def run_gen(wt, commit, gen):
    slurm = os.path.join(wt, "Scripts/SMC_BVS/engine_v4/tools/slurm")
    r = subprocess.run([sys.executable, os.path.join(slurm, "p1m_cells.py"), "--plans", gen, "--only", "1e4", "--code-commit", commit],
                       capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    if r.returncode:
        sys.exit("p1m_cells failed: " + r.stdout + r.stderr)
    return slurm


def klass(f):
    if f["Rp"] == 64:
        return "prec"
    if "-A3-" in f["run_id"]:
        return "a3"
    return {100: "s100", 200: "s200", 400: "s400", 800: "s800"}[f["n"]]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--wt", required=True); ap.add_argument("--code-commit", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--dept", default=DEPT)
    a = ap.parse_args()
    gen = os.path.join(a.out, "gen")
    slurm = run_gen(a.wt, a.code_commit, gen)
    sys.path.insert(0, slurm); sys.dont_write_bytecode = True
    import p1m_driver
    fits, head = {}, None
    for fn in sorted(os.listdir(gen)):
        p = json.load(open(os.path.join(gen, fn)))
        if fn.startswith(("precision", "science1e4")):
            head = head or {k: v for k, v in p.items() if k not in ("fits", "batch", "core_h_cap", "kind", "resources", "max_task_hours")}
            for f in p["fits"]:
                fits[f["run_id"]] = f
    assert head and head["mode"] == "V" and head.get("island_isa") == "sapphirerapids"
    # C1 / C2 / C3 ----------------------------------------------------------------------------------------------------
    for rid, f in list(fits.items()):
        if "-P-N" in rid:
            m = int(re.search(r"-m(\d+)-c", rid).group(1))
            f["params"] = {"refine_m": m, "I_max": 3}
        elif "-A3-" in rid:
            assert f["params"] == {"partition": "exact_linkage"}, f["params"]
            f["params"] = {"partition": "exact"}
    for ds in ("AR", "ARweak", "ADJOPP"):
        for c in (1, 2):
            src = dict(fits["4-%s-n200-r01-P-N2500-m1-c%d-s1" % (ds, c)])
            a_idx = 8 + c - 1
            src["run_id"] = "4-%s-n200-r01-P-N2500-m1-I0-c%d-s1" % (ds, c)
            src["seed"] = src["data_seed"] + 100 * (K_FINAL + a_idx)
            src["params"] = {"refine_m": 1, "I_max": 0}
            assert src["run_id"] not in fits and src["seed"] not in {g["seed"] for g in fits.values()}
            fits[src["run_id"]] = src
    assert len(fits) == 24 + 156 + 6, len(fits)
    sel = lambda pred: [fits[r] for r in sorted(fits) if pred(r)]
    P = lambda ds, tag: "4-%s-n200-r01-P-%s-s1" % (ds, tag)
    waves = {   # wave id -> list of batches, each a list of run ids
        "A0": [[P("AR", "N2500-m4-c1"), P("AR", "N2500-m1-I0-c1")], ["4-AR-n200-r01-A3-exactlink-s1"]],
        "P1": [[P("AR", "N2500-m1-c1"), P("AR", "N2500-m1-c2")], [P("AR", "N2500-m4-c2"), P("AR", "N2500-m1-I0-c2")]],
        "P2": [[P("ARweak", t) for t in ("N2500-m1-c1", "N2500-m1-c2")], [P("ARweak", t) for t in ("N2500-m4-c1", "N2500-m4-c2")]],
        "P3": [[P("ARweak", t) for t in ("N2500-m1-I0-c1", "N2500-m1-I0-c2")], [P("ADJOPP", t) for t in ("N2500-m1-c1", "N2500-m1-c2")]],
        "P4": [[P("ADJOPP", t) for t in ("N2500-m4-c1", "N2500-m4-c2")], [P("ADJOPP", t) for t in ("N2500-m1-I0-c1", "N2500-m1-I0-c2")]],
        "H1": [[P("AR", "N10000-m%d-c%d" % (m, c)) for c in (1, 2)] for m in (1, 4)],
        "H2": [[P("ARweak", "N10000-m%d-c%d" % (m, c)) for c in (1, 2)] for m in (1, 4)],
        "H3": [[P("ADJOPP", "N10000-m%d-c%d" % (m, c)) for c in (1, 2)] for m in (1, 4)],
    }
    used = {r for bs in waves.values() for b in bs for r in b}
    assert all(r in fits for r in used), [r for r in used if r not in fits]
    # science: batches per (class) of <= 150 // (4 + 16) = 7 fits; waves of <= 4 batches; the first wave of n = 400 and n = 800 is a one-batch pilot
    sci = [r for r in sorted(fits) if r not in used]
    byc = {}
    for r in sci:
        byc.setdefault(klass(fits[r]), []).append(r)
    cap = MAX_BATCH_TASKS // (4 + 16)
    def batches(rs):
        k = math.ceil(len(rs) / cap); q = math.ceil(len(rs) / k)       # balanced batches
        return [rs[i:i + q] for i in range(0, len(rs), q)]
    seq = [("s200", 0), ("a3", 0), ("s100", 0), ("s400", 1), ("s800", 1)]   # (class, pilot batch first)
    sw = 0
    cur = []
    def flush():
        nonlocal cur, sw
        if cur:
            sw += 1; waves["S%d" % sw] = cur; cur = []
    for kl, pilot in seq:
        bs = batches(byc[kl])
        if pilot:
            flush(); sw += 1; waves["S%d" % sw] = [bs[0]]; bs = bs[1:]
        for b in bs:
            cur.append(b)
            if len(cur) == MAX_WAVE_BATCHES:
                flush()
        flush()
    assert sorted(r for w in waves.values() for b in w for r in b) == sorted(fits), "every fit is in exactly one wave"
    os.makedirs(os.path.join(a.out, "plans"), exist_ok=True)
    table, wavejson = [], {}
    for w, bs in waves.items():
        wavejson[w] = {"batches": []}
        for i, b in enumerate(bs, 1):
            kl = klass(fits[b[0]])
            assert all(klass(fits[r]) == kl for r in b) or w == "A0", (w, i)
            kls = {klass(fits[r]) for r in b}
            kl = "prec" if "prec" in kls else kl
            name = "PL_%s_%d" % (w, i)
            plan = dict(head); plan.update(batch=name, kind="gated (leg precision1e4: HQ H-25; %s)" % ("HELD B2" if w.startswith("H") else "release per LEG_PLAN"),
                                          max_task_hours=2.0, resources=SHAPES[kl], island_throttle=THROTTLE[kl], fits=[fits[r] for r in b])
            wc = p1m_driver.resolve(dict(plan, core_h_cap=1e12))["worst_case_core_h"]
            plan["core_h_cap"] = math.ceil((wc + 0.05) * 10 - 1e-9) / 10
            plan = {k: plan[k] for k in ("batch", "mode", "code_commit", "method_tag", "core_tree", "binary", "max_task_hours", "island_isa", "kind",
                                         "island_throttle", "core_h_cap", "resources", "fits") if k in plan}
            pf = os.path.join(a.out, "plans", name + ".json")
            json.dump(plan, open(pf, "w"), indent=1); open(pf, "a").write("\n")
            sd = os.path.join(a.out, "scripts", name)
            d = subprocess.run([sys.executable, os.path.join(slurm, "p1m_driver.py"), "--plan", pf, "--out", sd, "--dept", a.dept, "--strict"],
                               capture_output=True, text=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            if d.returncode:
                sys.exit("driver --strict failed for %s: %s%s" % (name, d.stdout, d.stderr))
            res = json.load(open(os.path.join(sd, "plan.resolved.json")))
            rs = SHAPES[kl]
            peak = len(b) * max(rs["calibrate"]["cpus"], min(THROTTLE[kl], fits[b[0]]["Rp"]) * rs["islands"]["cpus"])   # all calibrations, or all throttled island arrays, at once (phases of one batch)
            table.append((w, name, len(b), res["n_tasks"], res["worst_case_core_h"], plan["core_h_cap"], peak, res.get("warnings")))
            wavejson[w]["batches"].append({"batch": name, "plan_sha256": __import__("hashlib").sha256(open(pf, "rb").read()).hexdigest(),
                                           "fits": [{k: fits[r][k] for k in ("run_id", "design", "n", "Rp", "N", "seed", "data_seed")} | {"params": fits[r].get("params", {}), "klass": klass(fits[r])} for r in b],
                                           "tasks": res["n_tasks"], "worst_case_core_h": res["worst_case_core_h"], "core_h_cap": plan["core_h_cap"]})
    json.dump(wavejson, open(os.path.join(a.out, "waves.json"), "w"), indent=1)
    print("%-4s %-9s %5s %6s %9s %9s %8s  warnings" % ("wave", "batch", "fits", "tasks", "worst", "cap", "peakCPU"))
    for r in table:
        print("%-4s %-9s %5d %6d %9.1f %9.1f %8d  %s" % r)
    byw = {}
    for r in table:
        x = byw.setdefault(r[0], [0, 0, 0.0, 0, 0, 0]); x[0] += 1; x[1] += r[2]; x[2] += r[4]; x[3] += r[3]; x[5] += r[6]
    print("\nper wave: batches, fits, tasks, worst-case core-h (limit sum), peak CPUs (sum over the wave's batches of the larger phase)")
    for w, x in byw.items():
        print("%-4s %2d batches %3d fits %4d tasks worst %8.1f  peak<=%d" % (w, x[0], x[1], x[3], x[2], x[5]))
    print("total fits %d; waves %d" % (sum(x[1] for x in byw.values()), len(byw)))


if __name__ == "__main__":
    main()
