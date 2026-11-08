"""extra_stats.py: median / max of 1-pi0(S*) by design and n (E2,E3,E6) -- reading aid for SUMMARY.md"""
import csv, collections, statistics
out = ["## Extra: 1-pi0(S*) (start-law deficit), median / max over all runs pooled by design family and n\n",
       "| experiment | n | runs | median 1-pi0(S*) | max 1-pi0(S*) | share with pi0(S*)>1/2 | start=S* |", "|---|---|---|---|---|---|---|"]
def load(fn):
    return list(csv.DictReader(open(fn)))
def fam(name, rows, keyfn):
    g = collections.defaultdict(list)
    for r in rows:
        g[keyfn(r)].append(r)
    for k in sorted(g):
        rs = g[k]
        v = [float(r["one_minus_pi0_Sstar"]) for r in rs]
        out.append("| %s | %s | %d | %.3f | %.3f | %d/%d | %d/%d |" % (name, k, len(rs), statistics.median(v), max(v), sum(1 for x in v if x < 0.5), len(v),
                   sum(1 for r in rs if r["start_eq_Sstar"] == "True"), len(rs)))
fam("E2 LH exact", load("E2_raw.csv"), lambda r: int(r["n"]))
rows = load("E3_raw.csv")
fam("E3 LH-iid p=108", [r for r in rows if r["p"] == "108"], lambda r: int(r["n"]))
fam("E3 LH-iid p=396", [r for r in rows if r["p"] == "396"], lambda r: int(r["n"]))
rows = load("E6_raw.csv")
for s in range(1, 7):
    fam("E6 S%d" % s, [r for r in rows if r["scen"] == str(s)], lambda r: int(r["n"]))
open("EXTRA_stats.md", "w").write("\n".join(out) + "\n")
print("\n".join(out))

# ---- pooled flag totals by experiment and n
flags = [("blocks_eq_groups", "blocks=groups"), ("start_eq_Sstar", "start=S*"), ("path_in_V", "path in V"), ("S0_scored", "S0 scored"),
         ("certified", "certified"), ("final_eq_S0", "final=S0"), ("hpm_eq_S0", "HPM=S0")]
out2 = ["\n## Extra: pooled flag totals by experiment and n (all configurations pooled, 20 seeds each)\n",
        "| experiment | n | runs | " + " | ".join(l for _, l in flags) + " | LS0 moves max | LS0 local_limit |", "|---|---|---|" + "---|" * (len(flags) + 2)]
import os
def pooled(name, rows, nkey="n"):
    g = collections.defaultdict(list)
    for r in rows:
        g[int(r[nkey])].append(r)
    for n in sorted(g):
        rs = g[n]
        cells = []
        for k, _ in flags:
            vals = [r[k] for r in rs if r.get(k) not in ("", "None", None)]
            cells.append("%d/%d" % (sum(1 for v in vals if v == "True"), len(vals)) if vals else "-")
        out2.append("| %s | %d | %d | %s | %d | %d |" % (name, n, len(rs), " | ".join(cells), max(int(r["moves"]) for r in rs), sum(1 for r in rs if r["local_limit"] == "True")))
pooled("E2", load("E2_raw.csv"))
rows3 = load("E3_raw.csv")
pooled("E3 p=108", [r for r in rows3 if r["p"] == "108"])
pooled("E3 p=396", [r for r in rows3 if r["p"] == "396"])
for fn, nm in (("E4i_raw.csv", "E4(i)"), ("E4ii_raw.csv", "E4(ii)"), ("E4iii_raw.csv", "E4(iii)")):
    pooled(nm, load(fn))
rows6 = load("E6_raw.csv")
for s in range(1, 7):
    pooled("E6 S%d" % s, [r for r in rows6 if r["scen"] == str(s)])
for dsg in ("iid", "exact"):
    pooled("E5 S5 " + dsg, [r for r in load("E5_raw.csv") if r["design"] == dsg])
open("EXTRA_stats.md", "a").write("\n".join(out2) + "\n")
print("\n".join(out2))
