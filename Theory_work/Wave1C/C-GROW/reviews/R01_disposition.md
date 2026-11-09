# R01 disposition (statement lock, Codex gpt-6.1-sol high, verdict LOCK-WITH-CHANGES)

| # | Required change | Disposition |
|---|---|---|
| 1 | G1 feasibility boundary (C5(b) violated s₀+|𝒫|+1 ≤ K) | Applied: (G1) now |Q| ≤ K and either Q = [p] or K ≥ 2|Q| + 32s₀ + 1 (implies min(p,|Q|+1) ≤ K). L3 handles Q = [p] (saturated K = p mode contains S₀). |
| 2 | Global size ladder explicit in C3, incl. saturated modes, all maximisers | Applied: (C3) states the obligation; lemmas/L3 §L3.2 proves it by a Markov count of junk-carrying blocks with a dyadic ladder in |S̃| (all maximisers simultaneously; no untruncated exp(Z²/2) expectation used). |
| 3 | Exact BB ratio, uniform null-add expansion, separate G4-χ / G4-dir arguments | Applied: (C2) text; lemmas/L2 §L2.2 (exact ratio (k+1)/(2p−1−k)), §L2.3(a) Pythagorean bound with one common χ², §L2.3(b) direction count. |
| 4 | Explicit AR(1) radius; p_n regime | Applied: d_n := ⌈log n/(2 log(1/|ρ|))⌉ (leakage O(1)); any p_n ≤ n − 1; lower bound |𝒫_n| ≥ min(d_n, p − s₀) − s₀ stated. |
| 5 | S5 layout defined; finite TV check | Applied: layout named as a diagnostic layout (not the generator's declared truth); TV made an explicit finite check (numerics F2) on which (C5)(b) is conditional until reported. |
| 6 | Scope/diagnostic language | Applied: §0 "Scope actually targeted"; MC3 wording "consistent with posterior concentration"; S5 superset only from n = 3200; random design excluded. |
| 7 | Self-contained hypotheses | Applied: §1 writes out score, prior ratio, K, centring/scaling, partition, premises, U_n := 𝒪ᶜ; §2 writes out (H0) with constants. |
| 8 | C3(b) → C4(b), endpoint certification, METHOD_REQUIREMENTS.md | Applied (§1, (C1)); METHOD_REQUIREMENTS.md written. |
| 9 | PLAN: L1 reuse is not "only constants" | Applied: PLAN item L0 reworded; lemmas/L0 adjusts t_n for the χ²-rank factor 2^{J/2} with J = O(log n) and rechecks the RSS floor/remainder. |

Optional suggestions adopted: truth inclusion and size ladder proved separately (L3.2, L3.3); strict η margin kept;
exact-Gram direction-count identity stated separately (L5(a)); finite-n LS0 cap failure distinguished from the full
method's D_n (§0, D4).
