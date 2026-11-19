#!/usr/bin/env python3
"""rebuild_times.py -- per-rebuild wall times of every collected T calibration (W0 + W1 + W2), from cost-file mtimes
(rsync keeps the NOTS mtimes; resolution ~1 s, each k has 4 sequential diagnostic islands r1..r4).
Read-only on records/. Output: one row per (fit, tier): n rebuilds, pilot->k1 gap, mean/min/max gap between k's."""
import os, re, sys, glob, statistics as st
ROOT = "/home/fb31/SMC_Engineering_Department/records/overlap1e4"
pat = re.compile(r"cost_(diag|pilot)_t(\d)_k(\d+)_r(\d+)\.jsonl")
print("wave,fit,tier,rebuilds,pilot_to_k1_end_s,mean_k_gap_s,min_k_gap_s,max_k_gap_s,tier_span_s")
for wave in ("W0", "W1", "W2"):
    for fit in sorted(glob.glob(f"{ROOT}/{wave}/*-T-s*")):
        cd = os.path.join(fit, "cost")
        if not os.path.isdir(cd):
            continue
        ev = {}
        for f in os.listdir(cd):
            m = pat.match(f)
            if not m:
                continue
            kind, t, k, r = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
            ev.setdefault(t, {}).setdefault((kind, k), []).append(os.path.getmtime(os.path.join(cd, f)))
        for t in sorted(ev):
            pil = max(ev[t].get(("pilot", 0), [float("nan")]))
            ks = sorted(k for (kind, k) in ev[t] if kind == "diag")
            ends = [max(ev[t][("diag", k)]) for k in ks]
            gaps = [b - a for a, b in zip(ends, ends[1:])]
            p2k1 = ends[0] - pil if ks else float("nan")
            span = ends[-1] - pil if ks else float("nan")
            g = (st.mean(gaps), min(gaps), max(gaps)) if gaps else (float("nan"),) * 3
            print(f"{wave},{os.path.basename(fit)},{t},{len(ks)},{p2k1:.0f},{g[0]:.0f},{g[1]:.0f},{g[2]:.0f},{span:.0f}")
