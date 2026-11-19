#!/usr/bin/env python3
"""p1m_calib_n.py -- the final islands' N (and the merge manifest's N record) in theory mode (law / compat): calib.bin's frozen N, at STAGE time.

The coded calibration (D-26; v3's tiers) may escalate tier 0 -> 1, which freezes N = 4 x N0 (N0 = max(2500, n, p)), so the N
the engine demands of an island (`island: N differs from calib.bin's frozen N`) is not always the plan's N. The driver's manifest
templates carry the plan's N (the pre-calibration record); the stage scripts of a batch with a theory-mode fit call, on the
compute node and after p1m_manifest.py fill:

  p1m_calib_n.py set-n    --manifest M.json --calib CALIB.bin.json
        the filled island / merge manifest M: params.N = the frozen N_final read from the calibration record. When it differs from
        the manifest's (the plan's) N, both are logged on stderr. A manifest whose mode is V is left alone (a mixed batch).
        A missing / unreadable / incomplete record, or one without a valid N_final, refuses (exit != 0) before the engine starts.
  p1m_calib_n.py record-n --manifest T.json --calib CALIB.bin.json --run-manifest RUN_MANIFEST.json
        (calibrate stage) writes {N_plan, N_final, tier_final, differs, source} into the run manifest under calib_N; the plan's
        params.N stays there as the pre-calibration record. A V-mode manifest T.json is a no-op.

The record is the engine's own sidecar <out>.json: "tier_final" and settings.tiers[tier_final].N_final (calib_run.cpp).
Stdlib only; Python >= 3.6.
"""
import argparse
import json
import math
import os
import sys


def calib_n(path):
    """(N_final, tier_final) of the calibration record `path`; SystemExit with one clear line on anything unusable."""
    def refuse(why):
        raise SystemExit("p1m_calib_n: calibration record %s: %s: refusing to start (the final islands and the merge need calib.bin's frozen N)"
                         % (path, why))
    try:
        with open(path) as fh:
            rec = json.load(fh)
    except (OSError, ValueError) as e:
        refuse("cannot read it (%s)" % str(e).replace("\n", " "))
    if not isinstance(rec, dict):
        refuse("not a JSON object")
    if rec.get("status") != "completed":
        refuse("status is %r, not 'completed'" % (rec.get("status"),))

    def whole(v, what, lo, hi):
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) or v != int(v) or not (lo <= v <= hi):
            refuse("%s is %r, not a whole number in [%d, %d]" % (what, v, lo, hi))
        return int(v)
    tier = whole(rec.get("tier_final"), "tier_final", 0, 1)
    try:
        v = rec["settings"]["tiers"][tier]["N_final"]
    except (KeyError, IndexError, TypeError):
        refuse("no settings.tiers[%d].N_final" % tier)
    return whole(v, "settings.tiers[%d].N_final" % tier, 1, 1 << 24), tier


def update_json(path, fn):
    with open(path) as fh:
        d = json.load(fh)
    fn(d)
    tmp = path + ".tmp.%d" % os.getpid()
    with open(tmp, "w") as fh:
        json.dump(d, fh, indent=1)
        fh.write("\n")
    os.replace(tmp, path)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["set-n", "record-n"])
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--calib", required=True)
    ap.add_argument("--run-manifest")
    a = ap.parse_args(argv)
    with open(a.manifest) as fh:
        m = json.load(fh)
    if m.get("mode") == "V":
        return 0
    n, tier = calib_n(a.calib)
    if a.cmd == "set-n":
        plan_n = (m.get("params") or {}).get("N")
        if plan_n != n:
            print("p1m_calib_n: params.N: plan %s, calib.bin frozen N_final %d (tier %d): using calib's" % (plan_n, n, tier), file=sys.stderr)
        update_json(a.manifest, lambda d: d.setdefault("params", {}).__setitem__("N", n))
        return 0
    if not a.run_manifest:
        ap.error("record-n needs --run-manifest")

    def put(rm):
        n_plan = (rm.get("params") or {}).get("N")
        rm["calib_N"] = {"N_plan": n_plan, "N_final": n, "tier_final": tier, "differs": n_plan != n, "source": os.path.basename(a.calib)}
    update_json(a.run_manifest, put)
    print("p1m_calib_n: run manifest records calib N_final = %d (tier %d)" % (n, tier), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
