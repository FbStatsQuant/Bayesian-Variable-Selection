#!/usr/bin/env python3
"""gc_nots_inventory.py <runs_root> <batch>... -- runs ON NOTS (stdlib, read-only, nice 19, detached): per batch / run dir the sizes by FILE CLASS (island_*.bin, calib.bin, setup.bin, data.bin, raw.bin, fit.bin, law.bin, eval.bin, checkpoints, other), the file counts and the oldest / newest atime (days to the 14-day purge). Prints one JSON. Nothing is written or deleted."""
import json, os, re, sys, time
CL = [("islands", re.compile(r"^island_\d+\.bin$")), ("island_ckpt", re.compile(r"\.ckpt")), ("calib.bin", re.compile(r"^calib\.bin$")), ("setup.bin", re.compile(r"^setup\.bin$")), ("data.bin", re.compile(r"^data\.bin$")),
      ("raw.bin", re.compile(r"^raw\.bin$")), ("fit.bin", re.compile(r"^fit\.bin$")), ("law.bin", re.compile(r"^law\.bin$")), ("eval.bin", re.compile(r"^eval\.bin$"))]
now = time.time(); out = {}
for b in sys.argv[2:]:
    bd = os.path.join(sys.argv[1], b)
    if not os.path.isdir(bd): out[b] = None; continue
    r = {}
    for run in sorted(os.listdir(bd)):
        rd = os.path.join(bd, run)
        if not os.path.isdir(rd): continue
        sz, n, at = {}, {}, []
        for root, _, fs in os.walk(rd):
            for f in fs:
                p = os.path.join(root, f)
                try: st = os.stat(p)
                except OSError: continue
                c = next((nm for nm, rx in CL if rx.search(f)), "other")
                sz[c] = sz.get(c, 0) + st.st_size; n[c] = n.get(c, 0) + 1; at.append(st.st_atime)
        r[run] = {"bytes": sz, "files": n, "oldest_atime_age_days": round((now - min(at)) / 86400, 2) if at else None, "newest_atime_age_days": round((now - max(at)) / 86400, 2) if at else None}
    out[b] = r
json.dump(out, sys.stdout)
