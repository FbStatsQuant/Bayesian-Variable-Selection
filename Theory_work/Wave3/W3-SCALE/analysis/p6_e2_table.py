"""E2 flag (sd of the four final log Zhat_r above 1) by (n, p) in the W3-P6 run records on NOTS (read-only).

Source: /scratch/fb31/theory_w3/*/raw/fits.jsonl (one JSON line per fit, written by the W3-P6 driver p6_fit.R). The
P6 records do not store log_Z_r, only the flag. Inclusion: every line with status == "completed" (completed fits of
every design, s0, arm and tier pooled). Caveats written into the table header: designs and arms are mixed; the tier
differs (escalated fits use N = 4 N0); P6 is a small-n study (n <= 100), so these counts say nothing about fixed-N
scaling at n = 200.
Usage (on NOTS): python3 p6_e2_table.py > p6_E2_by_np.tsv
"""
import collections, glob, json

rows = []
for f in sorted(glob.glob("/scratch/fb31/theory_w3/*/raw/fits.jsonl")):
    run = f.split("/")[-3]
    for line in open(f):
        try:
            r = json.loads(line)
        except Exception:
            continue
        r["_run"] = run
        rows.append(r)
c = collections.defaultdict(lambda: collections.Counter())
for r in rows:
    if r.get("status") != "completed":
        continue
    k = (r["n"], r["p"])
    c[k]["completed"] += 1
    c[k]["E2"] += bool(r.get("flags_E2"))
    c[k]["escalated"] += bool(r.get("cal_escalated"))
    c[k]["E2_and_escalated"] += bool(r.get("flags_E2")) and bool(r.get("cal_escalated"))
    c[k]["runs:" + r["_run"]] += 1
    c[k]["design:" + str(r.get("design"))] += 1
print("# source: /scratch/fb31/theory_w3/*/raw/fits.jsonl; completed fits only; designs, arms and tiers pooled; lines read: %d" % len(rows))
print("n\tp\tcompleted\tE2_sd_gt_1\tE2_share\tescalated\tE2_and_escalated\truns\tdesigns")
for k in sorted(c):
    v = c[k]
    runs = ",".join("%s=%d" % (x[5:], v[x]) for x in sorted(v) if x.startswith("runs:"))
    des = ",".join("%s=%d" % (x[7:], v[x]) for x in sorted(v) if x.startswith("design:"))
    print("%d\t%d\t%d\t%d\t%.3f\t%d\t%d\t%s\t%s" % (k[0], k[1], v["completed"], v["E2"], v["E2"] / v["completed"], v["escalated"], v["E2_and_escalated"], runs, des))
