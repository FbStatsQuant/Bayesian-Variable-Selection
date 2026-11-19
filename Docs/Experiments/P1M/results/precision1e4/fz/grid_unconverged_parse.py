#!/usr/bin/env python3
"""Parse the single read-only NOTS dump (grid_unconverged_remote_info.sh -> nots_info_raw.txt, `smcbvs4 info calib.bin --meta 1` per overlap calib.bin) into grid_unconverged_overlap.csv.
python3 -I grid_unconverged_parse.py <nots_info_raw.txt> <out.csv>   (raw dump kept in ~/SMC_Engineering_Department/tmp/20261119-fz/, 676 KB)"""
import csv, json, re, sys
raw = open(sys.argv[1]).read()
rows = []
for b, rid, txt in re.findall(r"@@@ (\S+) (\S+)\n(.*?)\n@@@END", raw, re.S):
    m = json.loads(txt[txt.find("{"):]); m = m.get("meta", m); f = m["flags"]
    tr0 = [t for t in m["tiers"] if t["tier"] == 0][0]
    rows.append(dict(batch=b, run_id=rid, mode=m["mode"], rule=m["rule"], I_max_field=m["I_max"], ell=m["ell"], tier_final=m["tier"], N=m["N"], escalated=m["escalated"], I_used=m["I_used"],
                     grid_unconverged_final=f["grid_unconverged"], triggers_final=";".join(f["triggers_fired"]), tier0_converged=tr0["converged"], tier0_rebuilds=tr0["rebuilds"], tier0_triggers=";".join(tr0["triggers"])))
w = csv.DictWriter(open(sys.argv[2], "w", newline=""), fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
u = {}
for r in rows:
    u[r["run_id"]] = r
for mode in ("V", "law"):
    us = [r for r in u.values() if r["mode"] == mode]
    print(mode, "unique fits", len(us), "final grid_unconverged", sum(r["grid_unconverged_final"] for r in us), "tier-0 grid_unconverged trigger", sum("grid_unconverged" in r["tier0_triggers"] for r in us),
          "escalated", sum(r["escalated"] for r in us))
