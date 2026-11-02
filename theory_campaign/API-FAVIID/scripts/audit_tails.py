"""API-FAVIID: tails behind two median-level claims of W5-FAVIID (Q0/Qreal context effect; q/xi_n moment check).
Deterministic. Usage: python3 audit_tails.py <W5-FAVIID results dir>"""
import json, math, sys, statistics
from collections import defaultdict
sw = [json.loads(l) for l in open(sys.argv[1] + "/sweep.jsonl") if l.strip()]
out = []; P = out.append
qq = [r for r in sw if r["Qreal"]]
for lo, hi in ((0, 0.9), (0.9, 1.1), (1.1, 1.5), (1.5, 1e9)):
    sel = [r for r in qq if lo <= r["Q0"] / r["Qreal"] < hi]
    P("Q0/Qreal in [%g,%g): %d rows; by n: %s" % (lo, hi, len(sel), dict(sorted(defaultdict(int, {n: sum(r["n"] == n for r in sel) for n in (200, 400, 800, 1600, 3200)}).items()))))
for n in (200, 400, 800, 1600, 3200):
    a = [abs(math.log(r["Q0"] / r["Qreal"])) for r in qq if r["n"] == n]
    a.sort()
    P("n=%d: |log(Q0/Qreal)| median %.3f, 90%% %.3f, max %.3f" % (n, statistics.median(a), a[int(0.9 * len(a))], a[-1]))
xi = lambda r: math.sqrt(math.log(r["p"] * 2 ** min(16, math.isqrt(r["n"]))) / (r["n"] + 1))  # as in analyse_sweep.py
cell = defaultdict(list)
for r in sw:
    cell[(r["scen"], r["p"], r["scale"], r["n"])].append(r["q"] / xi(r))
mx = max(cell.items(), key=lambda kv: max(kv[1]))
P("q/xi (analyse_sweep's B=min(16,isqrt n)): cell MEANS over n>=800 in [%.3f, %.3f]; over all n in [%.3f, %.3f]" % (
    min(statistics.mean(v) for k, v in cell.items() if k[3] >= 800), max(statistics.mean(v) for k, v in cell.items() if k[3] >= 800),
    min(statistics.mean(v) for v in cell.values()), max(statistics.mean(v) for v in cell.values())))
P("cell medians over n>=800 in [%.3f, %.3f]" % (min(statistics.median(v) for k, v in cell.items() if k[3] >= 800),
    max(statistics.median(v) for k, v in cell.items() if k[3] >= 800)))
big = sorted(((x, k) for k, v in cell.items() for x in v if x > 3.83), reverse=True)
P("rows with q/xi > 3.83: %d ; largest: %s" % (len(big), big[:6]))
B = defaultdict(int)
for r in sw: B[(r["n"], r["B"])] += 1
P("recorded B by n: %s" % dict(B))
open("../results/audit_tails.txt", "w").write("\n".join(out) + "\n"); print("\n".join(out))
