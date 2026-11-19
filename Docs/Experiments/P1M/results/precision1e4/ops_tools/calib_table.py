#!/usr/bin/env python3
"""calib_table.py <records_wave_dir>... -- O-7: per fit N, refine_m, I_max, I_used, grid_unconverged (from calib_meta.json), island T (island_1.bin.json), the number of
cost_diag files and their largest index. These fields are in calib.bin meta only (not in calib.bin.json): the table is the 'reported per fit' item of PREREG §5 C7."""
import glob, json, os, re, sys
print("%-46s %6s %3s %5s %6s %6s %5s %6s %9s" % ("run_id", "N", "m", "Imax", "Iused", "gridUC", "T", "ndiag", "maxdiagk"))
for w in sys.argv[1:]:
    for u in sorted(glob.glob(os.path.join(w, "4-*"))):
        try:
            m = json.load(open(os.path.join(u, "calib_meta.json")))["meta"]
        except Exception:
            print("%-46s  (no calib_meta.json)" % os.path.basename(u)); continue
        try:
            T = json.load(open(os.path.join(u, "island_1.bin.json"))).get("T")
        except Exception:
            T = None
        ks = [int(x.group(1)) for f in os.listdir(os.path.join(u, "cost")) for x in [re.match(r"cost_diag_t\d+_k(\d+)_r\d+\.jsonl$", f)] if x] if os.path.isdir(os.path.join(u, "cost")) else []
        print("%-46s %6s %3s %5s %6s %6s %5s %6d %9s" % (os.path.basename(u), m.get("N"), m.get("refine_m"), m.get("I_max"), m.get("I_used"),
              (m.get("flags") or {}).get("grid_unconverged"), T, len(ks), max(ks) if ks else "-"))
