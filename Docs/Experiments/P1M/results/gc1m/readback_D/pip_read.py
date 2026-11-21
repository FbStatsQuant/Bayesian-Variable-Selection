#!/usr/bin/env python3
"""pip_read.py -- descriptive read of the per-variable PIPs of a 1M fit (read-only; the registered reader compare_overlap_v2.read_sections, unedited, sha 4f402e51..., is imported).
Reports, per estimator (PIP_eq = pip_primary, PIP_T): the PIPs of the 5 true variables, the maximum null PIP (and its index), the counts of null variables above 0.5 and 0.1, and sum PIP.
python3 -I pip_read.py FIT.bin TRUTH.json OUT.json"""
import importlib.util, json, sys
CO = "/home/fb31/BVS-wt/P1M/Docs/Experiments/P1M/results/overlap1e4/compare_overlap_v2.py"
sp = importlib.util.spec_from_file_location("co", CO); co = importlib.util.module_from_spec(sp); sp.loader.exec_module(co)
fit, truth, out = sys.argv[1:4]
S0 = json.load(open(truth))["S0"]
s = co.read_sections(fit, ["pip_eq", "pip_T", "orig"], verify=True)
res = {"sections": sorted(s.keys()), "S0": S0}
orig = list(s["orig"][0]) if "orig" in s else None
res["orig_len"] = len(orig) if orig else None
for nm in ("pip_eq", "pip_T"):
    if nm not in s:
        continue
    v = list(s[nm][0]); n = len(v)
    idx = orig if orig else list(range(1, n + 1))   # original columns are 1-based (S0 = 100000, ...); a fit.bin without `orig` keeps all columns
    pos = {int(c): i for i, c in enumerate(idx)}
    res[nm] = {"n": n, "true": {str(j): (v[pos[j]] if j in pos else (v[pos[j - 1]] if (j - 1) in pos else None)) for j in S0}}
    ts = set(pos[j] if j in pos else pos.get(j - 1) for j in S0)
    nulls = [(v[i], idx[i]) for i in range(n) if i not in ts]
    mx = max(nulls)
    res[nm].update({"max_null": mx[0], "max_null_index": mx[1], "n_null_gt_0.5": sum(1 for x, _ in nulls if x > 0.5), "n_null_gt_0.1": sum(1 for x, _ in nulls if x > 0.1), "sum_pip": sum(v),
                    "min_true": min(res[nm]["true"].values())})
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res, indent=1))
