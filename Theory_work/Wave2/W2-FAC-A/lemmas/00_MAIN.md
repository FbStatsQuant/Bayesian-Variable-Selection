# 00_MAIN — proof map for W2-FAC-A (STATEMENT.md v1.2, locked)

| Claim | Proof file | Inputs | Check |
|---|---|---|---|
| (L1) key lemma U: exact decomposition along the residual factor direction; uniform bound over all T; perturbation | L1_uniform_add.md | Laurent–Massart; Gaussian tails | R02 Sol xhigh V-W-A (applied); FU_out, FU5_out |
| (L2) Sand_n (Q = [p]) | L2_sandwich.md | [GEN-L1] block events; (TV) | R03 |
| (L3) NA(𝓛), TL(𝓛); α₀ calculation | L3_NA_TL.md | L1 Corollary U; (E1),(E2),E_Y | R03; FNA_summary |
| (L4) D_n → 0, P(𝒪 ∩ {Ŝ⁺ ≠ S₀}) → 0 | L4_assembly.md | C-GROW L1.2; [OP]; M5(0); T03♯ | R03 |
| (L5) random design; (I) instances; Lemma κ; Lemma P5; certificates | L5_random_instances.md | Lemma CR/[CONC′]; L5.0 uniformity; TV_cert | R04 |
| (D) Proposition F-FAC | L7_delivery.md | Proposition F (A1+A4), A2 template | R04 |
| Part II SHARP | L6_sharp.md | L1 (1.1); order statistics; (E1),(E2) | R04; FNA_summary |
| Part III tools (CS-1D, GAP), Conjecture PATH-CS | L8_frontier.md | — | not claimed |

Dependency chain: L1 → L3 → L4 ← L2; L4 + L5.0 → L5.1; L4/L5.1 + Proposition F → L7; L1 → L6.
Method fidelity: LS0 cap ℓ_n + |S̃₀| (merged), emitted centre = some maximiser of γ₀ (coded routine), Ŝ⁺ = max of the
all-scored set; no new method requirement.
