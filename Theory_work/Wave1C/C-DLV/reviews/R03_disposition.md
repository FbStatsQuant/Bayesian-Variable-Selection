# R03 (L3 + L5, Codex gpt-6.1-sol xhigh, key-lemma check) — disposition, 2026-11-08 22:25

Verdicts: 3.1, 3.2, 3.2′, 3.3, 3.5(a), 5.1 VERIFIED; 3.4, 3.5(b), 5.0, 5.2, 5.2′ VERIFIED-WITH-AMENDMENTS; Corollary 5.3
ERROR (as first written). Verbatim: R03_L3L5_codex.md (it reviewed the version containing Lemma 5.2′).
1. FATAL-tagged (Cor 5.3 used N̄_b under the shorter-range hypothesis; checked three-model counterexample overflowing at
   interval 1001) — FIXED: Cor 5.3 v2 uses the applicable bound N̄ (N̄_b or N̄_b′ = N̄_b + ⌈log_{4/3}((1+η)/η)⌉) and records
   the counterexample. STATEMENT (P5)(b), (C1) updated. The error was in the corollary only; Lemmas 5.2/5.2′ stand.
2. MAJOR (capacity ≠ success; non_progress only conditional) — FIXED: Cor 5.3(a) "cannot fail through
   too_many_intervals"; (b) β excluded iff (b−u)2⁻⁶⁰ ≤ s₀/D at each trial, sufficient D ≤ s₀2⁶⁰; (c) γ not excluded
   (reviewer's modest-D example recorded).
3. MINOR (N_b^try vs N_b^app) — FIXED in L5 header, L3 3.4(b)/3.5(b), L4 Theorem D (α).
4. MINOR (bisection trajectory not monotone) — FIXED: L3 3.4(c) argument rewritten as suggested.
5. MINOR (snapping in target-visitation; v_raw) — FIXED: L3 3.4(b), L5 Lemma 5.0 (v_raw).
6. MINOR (rounded constants) — FIXED: exact form N̄_b = 22 + ⌈log_{4/3} max{1,(−x₀−λ_θ)/(2s₀)}⌉; rounded form disclaimed.
7. MINOR (1 + 2⁻⁵⁹ ≤ 1 + η false for small η) — FIXED: 2m − u ≤ b ≤ 1.
Numerics: N2 (numerics/N2_grid_lemmas.txt) and N2b (numerics/N2b_pilot_and_counts.txt): 0 violations.
