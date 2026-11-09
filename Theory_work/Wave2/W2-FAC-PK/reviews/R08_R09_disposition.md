# Council round 1 disposition (R08 Sol xhigh 8.6, gate 3 FAIL; R09 Opus high 9.1, all gates PASS) → NOT PASSED
R08 (verbatim reviews/R08_council_sol.md):
1. (MAJOR, REPORT scope) G2 exported as design-free: fixed — REPORT §6 G2 restricted to p ≤ n − 1 (T ⊇ S₀), R08's p = Kn
   counterexample recorded, p ≫ n listed as an extra proof obligation; §5 heuristic qualified.
2. (MINOR) G1 used CS-specific Δ_k: fixed — generic nested-model budget log[w(s₀)/w(k)] + ½(k − s₀)log(n + 1).
3. (MINOR) mechanism paragraph: fixed — p − K − s₀ exclusions, G_sw ≥ M_TV_{jl} (L2.2(iii)), (c_D − ε), budget applied
   after the first truth-containing centre with O(log n) + O(log²n) overheads.
Optional: citation count 38 — fixed.
R09 (verbatim reviews/R09_council_opus.md):
M1 (MINOR) delivery refers to the plumbed method: fixed in STATEMENT (P4)(iii) and L4.2(iii).
E1 L2.2(i) needs neither (PK) nor (PB): noted in L3.4. E2 |E| ≤ 6H̄: fixed. E3 c₅ := min(c₄²/8, ½): fixed.
E4 "(PK′)": fixed. E5 citation count: fixed.
Optional 1 (preflight base cap) added to METHOD_REQUIREMENTS; optional 3 (trend reading) added as L3.5 remark 0;
optional 2 not needed (L2.2(iii) already calls the subtraction conservative via R03); optional 4 (state G2 via |T| ≤ K ≤ n/2)
**not adopted**: R08's counterexample shows |T| ≤ K ≤ n/2 alone does not give a uniform residual floor when p ≫ n; G2 is
kept with p ≤ n − 1 (the two seats' suggestions conflict; the stricter, correct version is kept).
No change to any claim; STATEMENT remains v3.1 (one clarifying sentence added to (P4)(iii)).
