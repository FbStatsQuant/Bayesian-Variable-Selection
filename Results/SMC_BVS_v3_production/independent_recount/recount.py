"""Independent recount of exact recovery (no pipeline code): HPM and pip05 support vs truth 'active' set."""
import csv, sys, collections
from pathlib import Path
truth_manifest, root = Path(sys.argv[1]), Path(sys.argv[2])
truth = {r["dataset_id"]: set(map(int, r["active"].split(";"))) for r in csv.DictReader(open(truth_manifest))}
cnt = collections.Counter(); n = collections.Counter(); fail = collections.Counter()
for run in ("prod_p0500_20261023T1227Z", "prod_p1000_20261023T1227Z"):
    for f in sorted((root / run).glob("p*/*/SMCBVS.csv")):
        for r in csv.DictReader(open(f, newline="", encoding="utf-8")):
            key = (r["scale_key"], int(r["p"]), int(r["scenario"]), r["rule_id"])
            n[key] += 1
            if r["status"] not in ("ok", "warning"):
                fail[key] += 1; continue
            sup = set(map(int, r["support"].split(";"))) if r["support"] else set()
            cnt[key] += sup == truth[r["dataset_id"]]
w = csv.writer(sys.stdout)
w.writerow(["scale", "p", "scenario", "rule", "n", "exact", "failed"])
for k in sorted(n):
    w.writerow([*k, n[k], cnt[k], fail[k]])
