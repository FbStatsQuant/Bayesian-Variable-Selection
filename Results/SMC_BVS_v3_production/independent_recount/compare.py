import csv, sys
rec = {(r["scale"], r["p"], r["scenario"], r["rule"]): (int(r["exact"]), int(r["failed"])) for r in csv.DictReader(open(sys.argv[1]))}
seen = 0; bad = 0
for path, p in ((sys.argv[2], "500"), (sys.argv[3], "1000")):
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        if r["method_id"] != "SMCBVS" or str(int(float(r["p"]))) != p or r.get("scenario") in ("pooled", "", None): continue
        k = (r["scale_key"], p, str(int(float(r["scenario"]))), r["rule_id"])
        if k not in rec: continue
        seen += 1
        got = int(float(r["exact_all_sum"]))
        if got != rec[k][0] or int(float(r["n_missing"])) != 0: bad += 1; print("MISMATCH", k, got, rec[k], r["n_missing"])
print("cells compared", seen, "mismatches", bad)
