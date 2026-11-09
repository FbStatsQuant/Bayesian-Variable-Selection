# R08 — Council round 1, seat B (Claude Opus 5.5) — W2-FAC-A

**Verdict: all six gates PASS. Score: 8.9 / 10.** No FATAL or MAJOR findings. Two editorial fixes are required; they do not affect any gate.

## What I read and checked

I read STATEMENT.md v1.2 and all the proof files (00_MAIN and L1–L8). I checked each citation against its source:
- C-GROW lemmas L0.2(c) and L1.1–L1.2, and C-GROW L4 "Inputs"
- [GEN-L1] L1.1–L1.4 and GEN L5 [OP]
- PXN CR_corr_tails [CONC′] (constant 32√(2(A+1)log n/(n−1)) and 3n⁻²)
- FINAL s1 (score, γ₀ = w·∏r_b, block rule B = min(⌊√n⌋, ⌊√p⌋, 16), LS0, Ŝ⁺)
- FINAL s3 (the T03♯ hypotheses: R, SE_λ, SE_w, BM-∞)
- FINAL s6 and A1–A4 (the status strings)
- DLV L4_delivery:60–77 (the pathwise claim)
- the methodology document's cut and packing rule (top-down split of nodes with more than B leaves; whole-cluster next-fit), as used by Lemma P5

I formed my view before reading the review trail. I then read R01–R06 and their dispositions. I did not read LOG.md, or R07, which is the other seat's review.

**Independent computations** (in-memory Python, nothing written to the repository):
- **L1 (1.1) and (1.2):** random one-factor model with random positive definite Ψ blocks (p = 9, groups of 3, 200 replicates, every T with |T| ≤ 4). The largest gap between the direct innovation and formula (1.1) was 4.0e-15. The bound (1.2) was violated in 0 of 204,800 cases.
- **Lemma κ:** closed form for λ̃²/(ψ·c_min) and c_min = ρ_b/(1−ρ_b), checked at three (ρ_b, ρ_w, group size) settings; error ≤ 2e-16.
- **α₀:** α₀(κ̄) = 1/(2κ̄(κ̄+2)) agrees with a grid maximisation at κ̄ ∈ {1, 1.5, 2}, giving 1/6, 2/21 and 1/16.
- **S5 diagnostic certificate:** brute force with direct linear algebra over 665,664 (j, block, U) configurations. The truth's group plus up to two other groups were drawn from the three other truth groups and two null groups, with all U. The minimum τ was 0.0622461538…, which equals 2023/32500. The minimiser is j = 26, block {g(26), g(75)}, U = {75}.
- **(GC-CS) exact minima** in Fraction arithmetic, for s₀ = 4 and s₀ = 14 and a ∈ {1/10, 3/10, 1/2, 7/10, 9/10}: 39/50 and 7/25; 17/50 and 1/125; 0 and 0; 8/85 and 1/295; 4/95 and 1/95. All match L5.3, including the exact zero at a = 1/2.

## Gate verdicts

### Gate 1 — Correctness of every step: PASS

- **L1 U(a).** Correct. 𝓗_T ⊆ 𝓚_T with codimension 1. ω_T ⊥ 𝓗_T because E[ω_Tγ_j] = λ_j − λ_TᵀΨ_TT⁻¹Ψ_Tj = 0. The innovation therefore splits orthogonally into the idiosyncratic Schur residual and the component along W_T. Block-diagonality is what makes the first term depend on T only through U = T ∩ g(l). Confirmed numerically.
- **L1 U(b).**
  - Cauchy–Schwarz in the Ψ⁻¹ inner product, then over groups, gives |λ_TᵀΨ_TT⁻¹ζ_T| ≤ √s_T·√(ΣQ_g).
  - s_T ≥ c_min·h_T gives √s_T/(1+s_T) ≤ 1/√(c_min·h_T).
  - The monotonicity q_V ≤ Q_g follows from the variational form.
  - The κ' and κ bookkeeping (κ'_bd ≤ κ̄/√ψ₀) is correct.
- **L1 U(c).**
  - There are ≤ p·2^{γ̄−1} local pairs.
  - Laurent–Massart is applied with D ≤ hγ̄, using monotonicity of the threshold in D.
  - The size-dependent x_h = log C(G,h) + 2 log(h+1) + log log n gives total failure ≤ (π²/6 − 1)/log n.
  - a_h and the ϱ_n reduction are correct, using r_h ≤ 2 log 2 + log log n and log(eG/h_T) ≤ log(eγ̄p/|T|).
  - The 2^p factor variables W_T are handled deterministically, not by counting. This is the key step and it is valid.
- **L1 U(d) and Corollary U.**
  - The Schur-complement perturbation constants and the square-root perturbation bound are correct.
  - The coupling ξ₀ := bᵀγ + √(1−λᵀΣ⁻¹λ)·V has variance 1, Cov(ξ₀, ζ) = 0 and Cov ζ = Ψ (checked).
  - The probability bookkeeping on the enlarged space is correct (R02 item 5).
- **L2.**
  - The γ₀ factorisation matches FINAL s1.
  - The step uses C-GROW L0.2(c) and [GEN-L1] L1.4(b): ν·log(RSS_U/RSS_{U∪j}) ≥ Δ/(2C_R).
  - (δ + σZ)² ≥ δ²/2 − σ²Z².
  - The count 2^{20}p for 𝓩 is right.
  - The case "k̃ = K ⇒ S̃ = [p]" is handled correctly.
- **L3.**
  - (E1) and (E2) are correct algebraically.
  - On E_Y, the RSS floor for T ⊇ S₀ is correct; s_Y² cancels in the Z² term and is bounded above elsewhere.
  - The α₀ step is exact: (√(2P) + κ̄√(2x_k))² = 2P[(1+κ̄s)² − s²] + 2x_k ≤ P/α₀ + 2x_k. The ε/α₁ margin argument closes it uniformly in (T, l).
  - The prior budget bound 2 log((2p−1−k)/(k+1)) ≥ 2x_k − 2 log 2 holds for 1 ≤ k ≤ p−1.
  - TL: the deletion/swap algebra and a² − b² = ‖(I − P_{B∪l})x_i‖² ≥ (n−1)φ² are correct. Under BM-∞ the cross term is o(θ²n).
- **L4.** A correct assembly through [OP], GROW L1.2 with Q = [p] (needs only |Q| ≤ K, and K = p eventually), M5(0) and T03♯. The cap ℓ_n + |S̃₀| ≥ τ.
- **L5.**
  - [CONC′] gives δ_n = p·δ'_n with p^{3/2}δ'_n√(log log n) → 0 for p ≤ n^{α₁}, α₁ < 1/6.
  - The TV transfer through f(R̂_V) is Lipschitz on the design event.
  - Lemma P5 is correct for the specified top-down cut and whole-cluster next-fit packing. I confirmed the rule against the methodology document: under strict separation each group is a dendrogram subtree of 5 ≤ B leaves, so it is never split.
  - Lemma TVF follows from Woodbury.
  - The CS partial covariance identity is correct.
- **L6 (SHARP).**
  - The Step 1 closed form for Z_{T,l} is correct: 1/(k+c), √c/(k+c), and the denominator √(1 + 1/(k+c)).
  - The order-statistic thresholds have N'Φ̄(t) → ∞, and for the m-th largest, ≫ m.
  - So Z² ≥ (8 − o(1))·log p.
  - Step 2 uses only the algebraic (E1) and (E2) plus the Laurent–Massart events.
  - The result is 2ΔF ≥ (6 − o(1))·log p − log(n+1) − O(1).
- **L7.**
  - Step 3's 𝒦_n route is the correct direction; it is not inferred from D_n.
  - D′'s pathwise scored-set claim is cited accurately (DLV L4:65–77).
  - Q_S ≥ yᵀy/(n+1) holds.

### Gate 2 — Hypotheses used = hypotheses stated, per clause: PASS

- **(L2):** model G, energy, (AG) ⇒ (G3a), (P) ⇒ p ≤ n^A and K = p, and (TV). This matches the STATEMENT.
- **(L3):** G, s₀ ≥ 1, energy, (AG), (P), and BM-∞ for TL only. All are within (H0) + (AG) + (P).
- **(L4):** adds (TV) and the §1 premises. Only "some maximiser" is used, as stated.
- **(L5):** iid Gaussian rows, (P), (TV-pop), fixed s₀, σ² and θ*. (H0) and (TV) are derived on 𝒜_n with common envelopes.
- **(D):** Proposition F's premises, listed explicitly. CAL is not used.
- **(I)(a):** (GC-CS) is used exactly as stated, with the feasible-u restriction (R05 item 3).

### Gate 3 — No hidden assumptions: PASS

- **Method assumptions** are all explicit: the block rule (including B ≥ 5 via p = 5G_n, G_n ≥ 5), the LS0 semantics, the merged cap, the Ŝ⁺ order, and the score.
- **Noise:** Gaussian, with the coupling done on an enlarged space and the events stated in the original space.
- **Design:** the correlation-matrix normalisation of Σ_n, λ_l ≠ 0, λ_min(Ψ) ≥ ψ₀, and fixed γ̄.
- **Exact Gram:** p ≤ n−1 is stated.
- **K = p:** derived from (P), not assumed.

### Gate 4 — Cited lemmas have adequate status: PASS

- Every status string I checked matches its source verbatim:
  - M5(0)/T38-(0), T03♯, [OP], GROW L1.2 (R03 VERIFIED, inside PROVED-CHECKED), [GEN-L1] (R02 VERIFIED-WITH-AMENDMENTS), and Lemma CR/[CONC′].
  - Proposition F "PROVED-CHECKED for the patched calibration law", A1 (round 3 PASSED), A4 "OK-WITH-FIXES", and A2 "PROVED (A2), checked by A3".
- Nothing is upgraded. This ticket's own lemmas stay "PROVED (by this seat, unchecked)" with their R02–R04 checks recorded.
- The inherited qualifications are carried forward: [OP] unchecked, e4/N3 OPEN, S.3 an audit.
- The GROW sandwich is correctly re-proved rather than cited, because (G1) fails for Q = [p].

### Gate 5 — Constants and rates tracked: PASS

- **Uniformity over 2^p sets.** Achieved by the deterministic U(b) plus a union over group subsets with size-dependent thresholds; the error terms are explicit.
- **α₀.** Derived exactly, attained by the worst case s = 1, and matched by SHARP at κ̄ = 1.
- **o(·) terms.** ε_n = o(√log n) comes from explicit pieces: O(√(log log n)), ϱ_n = O((log p)^{1/4} + (log log n)^{1/2}), and L_ψδ_n√(5(p+1) log log n) → 0.
- **n₀ dependencies.** Listed in L5.0 for the de-randomisation.
- **Exact certificates.** S5 τ₀ and the (GC-CS) g₀ are exact rationals (I reproduced both independently).

### Gate 6 — Fidelity to the method as coded/specified: PASS

- The method is v3.1 + LS0 from the start mode, with cap ℓ_n + |S̃₀| (merged at 4676af6).
- The emitted centre is "some maximiser" for consistency, and e4 + TDP-IMPL for delivery.
- Ŝ⁺ is the strict-order maximum of the all-scored set.
- The block partition follows the documented complete-linkage / top-down / next-fit rule with B = min(⌊√n⌋, ⌊√p⌋, 16).
- The total tier-1 fallback is used for (D) only.
- No new method requirement is introduced.

### Scope honesty: satisfactory

- **Narrowing flagged.** The narrowing from the brief (p ≤ n^A, fixed k) to limsup log p/log n < α₀ (1/6 for block compound symmetry incl. S5) with one global factor is flagged in §0 and repeated in §5.
- **Part II is correctly limited.** It is a necessity statement for NA over the full lattice, in exact-Gram CS only. It is explicitly not a method-inconsistency claim, and nothing is claimed at equality. L6's note that p ≤ K is not used is a strengthening and is recorded.
- **Part III is properly fenced.** It is evidence only; the heuristic steps are labelled HEURISTIC; the F2r swap exception is reported.
- **a = 1/2 limit disclosed.** The (GC-CS) zero at a = 1/2 for the study patterns is stated openly as a gap in the instance's coverage.

### Review trail

The R01–R06 dispositions are honest: each MAJOR finding (R04 item 1, R05 item 1) was actually repaired, and I re-verified both repairs (feasible-u restriction; exact certificate). I spot-checked R06 items 1–4, 6, 13 and 17 in the current files; all are applied.

## Score: 8.9 / 10

The proof architecture is sound and fully worked out. The key lemma is correct, sharp, and confirmed numerically. The α₀ exponent is matched by a separate optimality proposition. Citations and statuses are exact, and the instance certificates are exact. Points come off only for:
- the editorial issues below;
- the "checked by inspection" form of the L5.0 uniformity remark, which is acceptable but thin;
- the heavy density of the STATEMENT.

## Required fixes (editorial; none affects a gate)

1. **00_MAIN.md line 1** says "STATEMENT.md v1.1, locked". The locked file is v1.2. Update the reference.
2. **STATEMENT.md §0, diagnosis (ii):** change "into a idiosyncratic normal" to "into an idiosyncratic normal".

## Optional suggestions

1. **L5.1(ii) energy bound:** the factor "(1 + s₀δ'_n)s₀" is unnecessary and reads oddly. Every entry of R̂_{S₀S₀} is at most 1 in absolute value, so ‖R̂_{S₀S₀}‖ ≤ s₀ and ‖μ‖² ≤ (n−1)s₀‖θ*‖² directly.
2. **L5.0:** replace "checked by inspection" with a short table listing, for each n₀ and each probability bound in L1–L4, the constants it depends on. This would make the de-randomisation step auditable at a glance.
3. **REPORT.md** (not yet present): make sure it flags (a) the L6 strengthening (p ≤ K not used), (b) the (GC-CS) gap at a = 1/2 for the study patterns, and (c) the narrowing vs the brief. STATEMENT's header promises this.
4. **Evidence presentation:** FNA_summary records NA failures below 1/6 at n = 10⁶ (e.g. a = 0.3, s₀ = 4, α = 0.10, p = 7: 1/10 runs and 6/500 random sets). These are consistent with an asymptotic claim, since bounded constants such as C_ω dominate when log p is small. A one-line note in STATEMENT diagnosis (iii) or L6 would stop a reader from misreading the 1/6 boundary as a finite-n threshold. This is evidence wording only, not a limitation.
5. **(I)(d):** Lemma P5 needs B ≥ g, i.e. p ≥ g² and n ≥ g². Stating this next to the S5 assumption "G_n ≥ 5" would make the two instances read uniformly.
