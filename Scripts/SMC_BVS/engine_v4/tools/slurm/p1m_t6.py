#!/usr/bin/env python3
"""p1m_t6.py -- T6 by REAL kills (WP7 O4; WP3_ARCH_REVIEW R5; ENGINEERING_SPEC T6 "restart").

One final island of a fit, run through `smcbvs4 island` on the fit's real data.bin / setup.bin / calib.bin:
  1. reference: the island uninterrupted (no checkpoints);
  2. kill 1 (SIGKILL by PID): after the SECOND checkpoint generation was written (both generations exist);
  3. kill 2 (odd kills: after a second checkpoint of the resumed process; EVEN kills: DURING a checkpoint write,
     detected by the `.tmp.<pid>` file of the writer, then killed at once): a real kill in the middle of a write;
  4. last run: resumes from island_r.ckpt.{a,b} and finishes.
It then checks, and writes a JSON report (exit 0 iff every check holds):
  * each killed process died of SIGKILL (-9) and left no island file;
  * the final run reports `resumed_from_step` >= 1 (it really resumed) and its record is `completed`;
  * the final island's output hash and every non-meta section hash equal the reference's (same binary, same inputs:
    restart equivalence, T6), and the checkpoint files are removed after the completed write;
  * seconds: the reference wall, the final wall, the checkpoint seconds of the final run.
Only the processes started here are killed, by PID (POLICIES: never pkill by pattern).

  p1m_t6.py --bin smcbvs4 --data D --setup S --calib C --seed s --island r --threads k [--mem-budget BYTES]
            [--ckpt-every-s 20] [--kills 2] --work DIR --out report.json
"""
import argparse
import glob
import json
import os
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def island_cmd(a, out, extra):
    cmd = [a.bin, "island", "--data", a.data, "--setup", a.setup, "--calib", a.calib, "--mode", "V", "--seed", str(a.seed),
           "--island", str(a.island), "--threads", str(a.threads), "--out", out]
    if a.mem_budget:
        cmd += ["--mem-budget", str(a.mem_budget)]
    return cmd + extra


def read_json(path):
    with open(path) as f:
        return json.load(f)


def ckpt_state(base):
    """(set of (path, mtime_ns) of finished generations, list of writer tmp files)."""
    gens = set()
    for sfx in (".a", ".b"):
        p = base + ".ckpt" + sfx
        try:
            gens.add((p, os.stat(p).st_mtime_ns))
        except OSError:
            pass
    tmps = glob.glob(base + ".ckpt.a.tmp.*") + glob.glob(base + ".ckpt.b.tmp.*")
    return gens, tmps


def run_until_kill(a, out, kind, log_path, deadline):
    """Start the island and kill it by PID when `kind` happens: 'second_ckpt' (a second checkpoint generation of THIS
    process exists) or 'during_write' (a writer tmp file exists). Returns a dict about the kill."""
    base = out[:-4] if out.endswith(".bin") else out
    before, _ = ckpt_state(base)
    with open(log_path, "ab") as log:
        proc = subprocess.Popen(island_cmd(a, out, ["--ckpt", "1", "--ckpt-every-s", str(a.ckpt_every_s)]), stdout=log, stderr=subprocess.STDOUT)
        seen = set()
        t0 = time.time()
        why = None
        while True:
            rc = proc.poll()
            if rc is not None:
                return {"killed": False, "returncode": rc, "why": "the island ended before the kill condition (%s); lower --ckpt-every-s" % kind}
            gens, tmps = ckpt_state(base)
            seen |= {g for g in gens if g not in before}
            if kind == "second_ckpt" and len(seen) >= 2:
                why = "second checkpoint generation"
                break
            if kind == "during_write" and tmps:
                why = "checkpoint write in progress (%s)" % os.path.basename(tmps[0])
                break
            if time.time() > deadline:
                proc.kill()   # this PID only
                proc.wait()
                return {"killed": False, "returncode": proc.returncode, "why": "deadline reached before %s" % kind}
            time.sleep(0.004)
        os.kill(proc.pid, signal.SIGKILL)
        rc = proc.wait()
    return {"killed": True, "returncode": rc, "why": why, "after_s": round(time.time() - t0, 3), "pid": proc.pid,
            "island_file_exists": os.path.exists(out), "ckpt_files": sorted(os.path.basename(p) for p in glob.glob(base + ".ckpt*"))}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bin", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--setup", required=True)
    ap.add_argument("--calib", required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--island", type=int, default=1)
    ap.add_argument("--threads", type=int, default=1)
    ap.add_argument("--mem-budget", type=int, default=0)
    ap.add_argument("--ckpt-every-s", type=float, default=20.0)
    ap.add_argument("--kills", type=int, default=2)
    ap.add_argument("--max-seconds", type=float, default=2400.0, help="overall budget; each phase has the rest as its deadline")
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    os.makedirs(a.work, exist_ok=True)
    start = time.time()
    deadline = start + a.max_seconds
    rep = {"tool": "p1m_t6.py", "island": a.island, "threads": a.threads, "ckpt_every_s": a.ckpt_every_s, "kills_planned": a.kills,
           "checks": {}, "kills": []}

    # 1. reference
    ref = os.path.join(a.work, "ref_island.bin")
    t0 = time.time()
    with open(os.path.join(a.work, "ref.log"), "wb") as log:
        rc = subprocess.run(island_cmd(a, ref, ["--ckpt", "0"]), stdout=log, stderr=subprocess.STDOUT).returncode
    rep["reference"] = {"returncode": rc, "wall_s": round(time.time() - t0, 2)}
    rep["checks"]["reference_completed"] = rc == 0 and os.path.exists(ref)
    if not rep["checks"]["reference_completed"]:
        return finish(a, rep)
    ref_rec = read_json(ref + ".json")

    # 2. kills, then 3. the resumed run
    out = os.path.join(a.work, "island.bin")
    for pat in glob.glob(out + "*") + glob.glob(os.path.join(a.work, "island.ckpt*")):
        os.remove(pat)
    log_path = os.path.join(a.work, "island.log")
    for k in range(1, a.kills + 1):
        kind = "second_ckpt" if k % 2 == 1 else "during_write"
        info = run_until_kill(a, out, kind, log_path, deadline)
        info["kill"] = k
        info["kind"] = kind
        rep["kills"].append(info)
        if not info["killed"]:
            rep["checks"]["kill_%d_happened" % k] = False
            return finish(a, rep)
        rep["checks"]["kill_%d_sigkill" % k] = info["returncode"] == -signal.SIGKILL
        rep["checks"]["kill_%d_no_island_file" % k] = not info["island_file_exists"]
    t0 = time.time()
    with open(log_path, "ab") as log:
        rc = subprocess.run(island_cmd(a, out, ["--ckpt", "1", "--ckpt-every-s", str(a.ckpt_every_s)]), stdout=log, stderr=subprocess.STDOUT).returncode
    rep["final"] = {"returncode": rc, "wall_s": round(time.time() - t0, 2)}
    rep["checks"]["final_completed"] = rc == 0 and os.path.exists(out)
    if rep["checks"]["final_completed"]:
        rec = read_json(out + ".json")
        rep["final"].update({"resumed_from_step": rec.get("resumed_from_step"), "seconds": rec.get("seconds"), "output_hash": rec.get("output_hash")})
        rep["reference"].update({"output_hash": ref_rec.get("output_hash"), "seconds": ref_rec.get("seconds")})
        rep["checks"]["resumed"] = isinstance(rec.get("resumed_from_step"), (int, float)) and rec["resumed_from_step"] >= 1
        rep["checks"]["status_completed"] = rec.get("status") == "completed"
        rep["checks"]["output_hash_equal"] = rec.get("output_hash") is not None and rec.get("output_hash") == ref_rec.get("output_hash")
        rep["checks"]["ckpt_removed"] = not glob.glob(out[:-4] + ".ckpt*")
        # every non-meta section hash (T6 beyond the summary hash): `smcbvs4 info --meta 1` of both files
        try:
            from p1m_stage_cost import compare_isa, info_meta
            ok, det = compare_isa(info_meta(a.bin, ref), info_meta(a.bin, out))
            rep["sections"] = det
            rep["checks"]["sections_equal"] = ok
        except Exception as e:  # noqa: BLE001 -- reported, the check fails
            rep["sections"] = {"error": str(e)}
            rep["checks"]["sections_equal"] = False
    return finish(a, rep)


def finish(a, rep):
    rep["ok"] = bool(rep["checks"]) and all(rep["checks"].values())
    with open(a.out, "w") as f:
        json.dump(rep, f, indent=1, sort_keys=True)
    print(json.dumps({"ok": rep["ok"], "checks": rep["checks"]}, sort_keys=True))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
