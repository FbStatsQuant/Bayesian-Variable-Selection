"""Summarise results/lh_premises_all.json into the REPORT table (W2-PREM)."""
import json, statistics as st
R = json.load(open(__file__.replace("scripts/lh_table.py", "results/lh_premises_all.json")))
rows = {}
for r in R["runs"]:
    q = r["SH"]
    rows.setdefault(r["n"], []).append((float(r["pi0_ref"]), q))
print("| n | 1−π₀(S°) | η₁♯ total | phase-1 junk (TL♯) | phase-1 U (substitutes) | I-move | η₂ total | phase-2 null additions (NL0) | ε_del | c₂ | c_*♯ | H′ | P(Bin(H′,c_*) < 8) | H′·η |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
f = lambda xs: "–".join(f"{v:.3g}" for v in sorted(set(round(x, 12) for x in xs))) if len(set(xs)) > 1 else f"{xs[0]:.3g}"
for n in sorted(rows):
    L = rows[n]
    g = lambda key, sub=None: [float(q[key][sub]) if sub else float(q[key]) for _, q in L]
    print(f"| {n} | {f([1 - p for p, _ in L])} | {f(g('eta1'))} | {f(g('eta1_parts', 'gibbs_null'))} | {f(g('eta1_parts', 'U'))} | "
          f"{f(g('eta1_parts', 'I'))} | {f(g('eta2'))} | {f(g('eta2_parts', 'gibbs_null'))} | {f(g('eps_del'))} | {f(g('c2'))} | "
          f"{f(g('c_star'))} | {L[0][1]['Hprime']} | {f(g('Binom_tail'))} | {f(g('Hprime_eta'))} |")
