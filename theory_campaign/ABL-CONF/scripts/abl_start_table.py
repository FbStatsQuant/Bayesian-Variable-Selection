"""abl_start_table.py -- ABL-CONF dry-run input (i): the existing 12-design ABL-START table in the rule's format.
Usage: python3 abl_start_table.py <item1_per_fit.csv> <out_dir>
Source: origin/theory/MEET-v31:theory_campaign/MEET-v31/evidence/item1_per_fit.csv (12 designs x 1 seed, arms A-D).
STAND-IN reference (dry run only; ABL-START has no reserved-seed reference): per design, log Z_ref = log of the mean of
the arm-A and arm-B fit-level Zhat (arm A alone if B did not finish); se_ref = 0.05 (nominal); K set to 99 so that the
rule's reference-size check passes; no guard pool (KB = 0 -> guard unavailable). pip_zw_max = ABL-START's
pip_zw_maxerr (against its leave-one-arm-out reference). The three arm-B fits that never finished (S3 r001 c100 stopped
after > 3 h, S4 r001 c100 and S4 r002 c050 still running after > 4 h) are entered as status 'capped' (they exceeded
the 75-min cap) with wall_s = 4500.
Writes three views:
  per_design/  the 12 designs as 12 designs with n = 1 pair each (the rule's own reading of that table);
  pooled/      the 12 designs pooled as 12 pairs (k = 1..12) of one pseudo-design 'ALL' (guard unavailable);
  pooled_guardpass/  as pooled, but with a guard pool forced to agree (hypothetical; exercises the LICENSED path).
"""
import csv, math, os, sys

src, out = sys.argv[1], sys.argv[2]
rows = [r for r in csv.DictReader(open(src)) if r["arm"] in "ABC"]
designs = sorted({(r["id"], r["scale"]) for r in rows})
by = {(r["id"], r["scale"], r["arm"]): r for r in rows}
lse = lambda xs: max(xs) + math.log(sum(math.exp(x - max(xs)) for x in xs))
COLS = ["name", "design", "scen", "role", "arm", "k", "status", "wall_s", "log_Z", "log_Zref", "se_ref", "err_logZ",
        "pip_zw_max", "sd_logZ_r"]
per, refs = [], []
for i, (idd, sk) in enumerate(designs, 1):
    d = f"{idd} {sk}"; sc = idd.split("_")[1]
    lz = [float(by[(idd, sk, a)]["log_Z"]) for a in "AB" if (idd, sk, a) in by]
    lzref = lse(lz) - math.log(len(lz))
    refs.append(dict(design=d, scen=sc, K=99, log_Zref=lzref, se_ref=0.05, KB=0, log_ZrefB="NA", se_refB="NA"))
    for a in "ABC":
        r = by.get((idd, sk, a))
        if r is None or r["status"] != "completed":
            per.append(dict(name=f"{idd}_{sk}_{a}", design=d, scen=sc, role="test", arm=a, k=i, status="capped",
                            wall_s=4500, log_Z="NA", log_Zref=lzref, se_ref=0.05, err_logZ="NA", pip_zw_max="NA",
                            sd_logZ_r="NA"))
        else:
            per.append(dict(name=f"{idd}_{sk}_{a}", design=d, scen=sc, role="test", arm=a, k=i, status="completed",
                            wall_s=float(r["sec_total"]), log_Z=float(r["log_Z"]), log_Zref=lzref, se_ref=0.05,
                            err_logZ=float(r["log_Z"]) - lzref, pip_zw_max=r["pip_zw_maxerr"], sd_logZ_r=r["sd_logZ_r"]))

def write(sub, P, R):
    os.makedirs(os.path.join(out, sub), exist_ok=True)
    with open(os.path.join(out, sub, "per_fit.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(P)
    with open(os.path.join(out, sub, "reference.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(R[0])); w.writeheader(); w.writerows(R)

write("per_design", [dict(r, k=1) for r in per], refs)
pooled = [dict(r, design="ALL", scen="ALL") for r in per]
write("pooled", pooled, [dict(design="ALL", scen="ALL", K=99, log_Zref="NA", se_ref=0.05, KB=0, log_ZrefB="NA", se_refB="NA")])
write("pooled_guardpass", pooled, [dict(design="ALL", scen="ALL", K=99, log_Zref=0.0, se_ref=0.05, KB=4, log_ZrefB=0.0,
                                        se_refB=0.05)])
