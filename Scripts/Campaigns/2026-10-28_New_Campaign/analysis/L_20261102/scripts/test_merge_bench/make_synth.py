"""make_synth.py SRC_CASE_DIR OUT_ROOT : synthetic benchmark root for the Sol R1 finding-1 test. Copies the pilot benchmark CSVs of one dev case
to two PRODUCTION cases in different chunks (p0020_S1_r001_c050 in chunk_00, p0020_S1_r051_c050 in chunk_01), relabelling ids, plus .done markers.
Test data only (never a result)."""
import sys, csv, os
src, out = sys.argv[1], sys.argv[2]
for case in ("p0020_S1_r001_c050", "p0020_S1_r051_c050"):
    ds = case[:-5]; d = os.path.join(out, "p0020", case); os.makedirs(d, exist_ok=True)
    for f in sorted(os.listdir(src)):
        if not f.endswith(".csv"): continue
        rows = list(csv.DictReader(open(os.path.join(src, f), encoding="utf-8")))
        for r in rows:
            r["case_id"], r["dataset_id"], r["replicate"] = case, ds, str(int(ds[-3:]))
        with open(os.path.join(d, f), "w", newline="", encoding="utf-8") as h:
            w = csv.DictWriter(h, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_NONNUMERIC); w.writeheader(); w.writerows(rows)
        open(os.path.join(d, f[:-4] + ".done"), "w").close()
print("synthetic root written:", out)
