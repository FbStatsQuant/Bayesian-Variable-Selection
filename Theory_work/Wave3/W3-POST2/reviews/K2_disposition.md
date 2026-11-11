# K2 (line check of C v2, D v2, E1 v2, gpt-6.1-sol high) — disposition

Verdicts: C VERIFIED; D VERIFIED-WITH-AMENDMENTS; E VERIFIED-WITH-AMENDMENTS. 0 FATAL / 0 MAJOR / 1 MINOR / 1 NIT.

| # | finding | action |
|---|---|---|
| 1 MINOR | D3: S₀ cross term only O_P(1) on an event claimed deterministic; variance constant needs uniform closeness | Same gap as M01-1, found independently; already fixed with the same argument (a₀ ∈ col X_{c,S₀}, (G2*), deterministic sup_S|Ev/σ*² − 1| ≤ 1/4, exact IG variance ≤ 4σ*⁴/n). K2 read the file before that fix. |
| 2 NIT | E remark 5 still speaks of Δ_S only | Reworded: interface is L_S, projection masking Δ_S ≤ L_S. |
