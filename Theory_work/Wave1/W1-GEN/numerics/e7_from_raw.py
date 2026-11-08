"""Rebuild E7_summary.md (main part) from E7_raw.csv (used if the extra E7b run is cut off)."""
import csv, sys
import exp_common as ec
import e7_proxy_flood as e7

def conv(v):
    if v in ("True", "False"):
        return v == "True"
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v
src = sys.argv[1] if len(sys.argv) > 1 else "E7_raw.csv"
rows = [{k: conv(v) for k, v in r.items()} for r in csv.DictReader(open(src))]
summ = e7.summarise(rows, ["p", "d", "n"])
open(src.replace("_raw.csv", "_summary_main.md"), "w").write(
    "## E7 proxy flood (x1 truth theta=1; d proxies with corr .6 to x1, mutual corr .36; remaining nulls independent; exact Gram) -- 20 seeds per row\n\n" + ec.md_table(summ, e7.COLS))
print(ec.md_table(summ, e7.COLS))
