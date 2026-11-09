"""d2_lattice.py -- summarise lattice-NA checks of D2 (d_exact.py fields lat_rand_*, lat_adv_*) -> D2_lattice.md"""
import json, glob, math
L = ["# D2 lattice NA checks (exact-Gram simulator, d_exact.py)", "",
     "Random lattice sets: 20 random T = S0 ∪ E per run (|E| uniform). One-sided sets: T = S0 ∪ {top-m nulls by the noise "
     "vector Sigma^{1/2}g}, m in {1,2,4,...,256,|N|/2}. A failure = max_l F(T∪l) − F(T) > 0 (NA violated at T).", "",
     "| design | p | n | log p/log n | runs | random sets failing | one-sided sets failing (runs with ≥1) | max one-sided add gain |", "|---|---|---|---|---|---|---|---|"]
for fn in sorted(glob.glob("D2_*_x_raw.jsonl")):
    rr = [json.loads(l) for l in open(fn)]
    for p in (100, 200, 400):
        for n in (10**4, 10**5, 10**6, 10**7):
            s = [r for r in rr if r["p"] == p and r["n"] == n and "lat_adv" in r]
            if not s: continue
            rf = sum(r["lat_rand_NA_fail"] for r in s); rn = sum(r["lat_rand_n"] for r in s)
            af = sum(r["lat_adv_NA_fail"] > 0 for r in s)
            mx = max(max(g for _, g in json.loads(r["lat_adv"])) for r in s)
            L.append("| %s | %d | %d | %.3f | %d | %d/%d | %d/%d | %.2f |" % (s[0]["design"], p, n, math.log(p)/math.log(n), len(s), rf, rn, af, len(s), mx))
open("D2_lattice.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
