"""Read every saved N4 output/CSV cell; reconcile raw records and summary."""
import ast
import csv
import re
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parents[2] / "numerics"
rows = []
for suffix in ("", "_n8000"):
    csv_path = root / f"n4_r2_pseudo_results{suffix}.csv"
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        batch = list(csv.DictReader(f))
    by_key = {(r["design"], r["n"], r["seed"]): r for r in batch}
    txt = (root / f"n4_r2_pseudo_out{suffix}.txt").read_text(encoding="utf-8-sig")
    seen = set()
    fields = 0
    for line in txt.splitlines():
        if not line.startswith("design="):
            continue
        parts = list(re.finditer(r"(?:^| )([A-Za-z0-9_]+)=", line))
        raw = {m.group(1): line[m.end():parts[i+1].start() if i+1 < len(parts) else len(line)] for i, m in enumerate(parts)}
        key = raw["design"], raw["n"], raw["seed"]
        assert key not in seen
        seen.add(key)
        saved = by_key[key]
        assert saved.keys() == raw.keys()
        for k, v in saved.items():
            try:
                obj = ast.literal_eval(v)
                expected = v if isinstance(obj, (dict, list)) else str(round(obj, 2) if isinstance(obj, float) else obj)
            except (ValueError, SyntaxError):
                expected = v
            assert raw[k] == expected, (key, k, raw[k], expected)
            fields += 1
    assert seen == by_key.keys()
    print(csv_path.name, len(batch), "records;", fields, "raw/CSV fields agree")
    rows.extend(batch)

assert len(rows) == 120
assert Counter((r["design"], r["n"]) for r in rows) == {(d, str(n)):20 for d in ("PC1", "PC2") for n in (500,2000,8000)}
for k in ("S0_in_mode", "sand_R1", "sand_R2", "sand_R3", "ls_final_eq_S0", "ls_certified", "na_fail_lat", "na_true_fail", "path_na_fail", "scr_final_eq_complete", "scr_path_eq_complete"):
    print(k, sum(r[k] == "True" for r in rows))
for r in rows:
    assert (r["na_true_fail"] == "True") == (float(r["na_true_maxgain"]) > 0)
    assert (r["na_fail_lat"] == "True") == (float(r["lattice_sup_h"]) > float(r["c_n"]))
    assert float(r["tl_min"]) <= float(r["tl_del_min"]) + 1e-8
    assert (r["ls_final_eq_S0"] == "True") == (ast.literal_eval(r["ls_final"]) == ast.literal_eval(r["S0"]))
print("All row flags internally consistent; minimum TL", min(float(r["tl_min"]) for r in rows))

# Execute only the summary helpers, avoiding imports of the component port and
# avoiding the script's main block, which writes outside the permitted scratch.
tree = ast.parse((root / "n4_r2_pseudo.py").read_text(encoding="utf-8"))
helpers = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name in ("_conv", "load_rows", "summarize")]
import os
import numpy as np
scope = {"csv": csv, "os": os, "np": np}
exec(compile(ast.Module(body=helpers, type_ignores=[]), "n4_summary_helpers", "exec"), scope)
actual = scope["summarize"]([str(root / f"n4_r2_pseudo_results{s}.csv") for s in ("", "_n8000")])
recorded = (root / "n4_r2_pseudo_summary.txt").read_text(encoding="utf-8-sig")
assert actual.rstrip() == recorded.rstrip()
print("Full current summary exactly reproduced from all CSV rows.")
