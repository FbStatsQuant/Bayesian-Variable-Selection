# Patch P-SEL — to `Theory_work/Wave1/W1-GEN/lemmas/L6_instances.md` §(d) (and STATEMENT.md (C5)(d))

Source: dedicated check R31 (`reviews/R31_SEL_check_sol.md`, Codex gpt-6.1-sol xhigh), verdict VERIFIED-WITH-AMENDMENTS,
FATAL 0 / MAJOR 0 / MINOR 1 / NIT 2. All three accepted by the lead (texts are R31's repairs); independently re-checked by R37 (`reviews/R37_patch_recheck_sol.md`, VERIFIED-WITH-AMENDMENTS 0/0/1/1, amendments applied below and in I2 §4). Wave1 files are not edited.
Together with item 2's [CONC′] replacement (`lemmas/I2_LHiid_unconditional.md` §4, last paragraph), which changes every
"C√(log p/n)" in L6(d) to O(√(log n/n)) with no effect on the orders used.

## P-SEL.1 (R31 #1, MINOR) — localise the Markov step
Location: `L6_instances.md:166-167` (step (iv)). Replace (iv) by:
> (iv) *Average.* Put F_n := 𝒢_n ∩ 𝒦_n ∩ {‖μ‖²/n ≤ M}, A_n^leak := (p − s₀)⁻¹Σ_{l∉S₀} max_T exp(E_{T,l}), and
> B_n^leak := (p − s₀)⁻¹Σ_{l∉S₀}Σ_{T₀∈𝒯₀(l)} exp((n − 1)Q_{T₀,l}/2).
> On F_n, A_n^leak ≤ exp(ω_n) B_n^leak. Unconditionally, E B_n^leak ≤ C·2^{75}n^{1/4}, with C independent of n, p, l, T₀.
> Therefore P(A_n^leak > n^{3/8}) ≤ P(F_nᶜ) + C·2^{75}exp(ω_n)n^{−1/8} → 0. This is NL_avg(1/8). No conditional moment
> assertion is used. ∎(SEL)
Reason: the domination max_T e^{E} ≤ e^{ω_n}Σ_{T₀} e^{(n−1)Q/2} holds on the event of (iii), not pointwise; the moment
bound is for the fixed-family sum. The sum is over l ∉ S₀ as in NL_avg's definition.

## P-SEL.2 (R31 #2, NIT) — sign of the scale
Location: `L6_instances.md:117, :132`; `STATEMENT.md:138`. Replace "fixed scale c" (L6:117) and "fixed signal scale c" (STATEMENT:138) by "a fixed scale c > 0 (in
particular any of the five study scales)" (or allow fixed c ≠ 0 and write θ*_min = 0.8|c|). A scale c = c_n → 0 is not
covered.
R37 #1 (MINOR) addendum: If the signed-scale alternative c ≠ 0 is used, also replace L6_instances.md:181's covariance
assertion by "on 𝒢_n every null-group column satisfies |⟨x_l, μ⟩|/(n − 1) ≥ 0.12|c| eventually", and replace the lower
bound at :188 by "|q| ≥ |c|(1 − Σ_{k<14}|β^pat_k|2^{−32}) > 0". These additional edits are unnecessary for the c > 0
version (recommended).

## P-SEL.3 (R31 #3, NIT) — embed the 14 coefficients
Location: `L6_instances.md:116-118, :138, :170`. Write μ = cX_{S₀}β^pat, θ*_{S₀} = cβ^pat, θ*_{S₀ᶜ} = 0, and
M := 2c²(β^pat)ᵀΣ_s[S₀,S₀]β^pat + 1; in S1/S3/S4/S6, Σ_s[S₀,S₀] = I₁₄ (one truth per group, groups independent), so
M = 49.28c² + 1 (Σ(β^pat)² = 24.64).

## Wording note (R31 audit, not a finding)
SEL delivers NL_C (C_L = 32(A + 3)M/σ²) and NL_avg(1/8), not NL_η; L6(d) already says NL_C — keep it so.

## Numerics (R31)
`numerics/item3_SEL_falsify.py` / `_out.txt`: 12 draws (S1/S3/S4/S6 × n ∈ {200, 800, 3200}, p ∈ {1000, 1000, 1600}),
actual data-dependent blocks (whole-group property held in all 9 correlated draws), 68,617,536 leakage triples
enumerated exactly. max induced Q·n/log n = 4.16 (bound 80). The averaged statistic exceeds n^{3/8} in 5 of 12 draws
(e.g. S4 n = 200: 109.7 vs 7.29; S6 n = 3200: 24.26 vs 20.63): **no finite-n reading of NL_avg(1/8) is supported**; this is
consistent with an asymptotic lemma (Markov slack n^{−1/8}, constant 2^{75}) and is not a counterexample to it.

## Effect on W1-GEN
No hypothesis or conclusion of Theorem GEN changes; (C5)(d) S1/S3/S4/S6 now has a dedicated XF check
(VERIFIED-WITH-AMENDMENTS, R31) in addition to sweep R10 and council R11/R12. Finite-n disclaimer reinforced.
