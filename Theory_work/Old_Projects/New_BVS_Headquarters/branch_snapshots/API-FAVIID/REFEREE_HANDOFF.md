# API-FAVIID — hand-off for the cross-family referee (synthesis task 9, Part 2 = F-REFEREE R6 remainder)

**Scope of the referee task.** Cross-family (XF) verification of four items of W5-FAVIID: **Lemma X⁺**, **Lemma M**, **Theorem B's
factorisation**, and **Corollaries C1–C3**. A-REV3 already covered W3-PXN P1–P5, Lemma B and P8 (VERIFIED) and P6 (GAP). It did not
cover anything in W5-FAVIID.

**What to read (all frozen at commit `31695b1` on `origin/theory/W5-FAVIID`).**
- `git show 31695b1:theory_campaign/W5-FAVIID/PROOF.md` (434 lines). Line ranges below refer to this file.
- `git show 31695b1:theory_campaign/W5-FAVIID/REPORT.md`, or the amended copy `theory_campaign/API-FAVIID/W5-FAVIID_REPORT_AMENDED.md`.
  The amended copy changes numbers and wording only; no statement, proof or status word is changed.
- Cited inputs: locked T22(i) (`Docs/Theory/proofs/T22_T16_start_aggregation/STATEMENT.md`, lines 20–30: definitions of a_bj, D_b,
  q = (p−s)⁻¹Σ_bD_b and e); W1-EXP Lemmas 1.1–1.2 (`theory/W1-EXP` branch); W3-PXN Lemmas Tr, P2, P8 (`theory/W3-PXN`);
  W2-T26 Lemma 1 and Theorem A (`theory/W2-T26`); locked T03 and T21.

**Status of the items.** All are PROVED (candidate) by the author, W5-FAVIID. API-FAVIID read them once, in the same model family.
That read found no error, and it **does not count as verification**; see §5.

---

## 1. Lemma X⁺ — PROOF.md lines 55–90

**Claim.** For U ⊊ A with λ_min(G_A) ≥ φ²(n−1) and (n+1)φ² ≥ 50:
log BF(A) − log BF(U) ≤ −(j/2)log(n+1) − ν log(RSS_A/RSS_U) + κ⁺, where κ⁺ = j(1+φ⁻²)/(2φ²(n−1)) + ν/((n+1)φ²RSS^y_U).

**Steps to check.**
1. Determinant part. Each step of a one-index chain gets the lower bound of [W1-L1.2], and interlacing makes the bound hold for every
   intermediate set. Check that W1-EXP Lemma 1.2's bound has exactly the form log D_T − log D_{T∖{i}} ≥ log(n+1) − (1+φ⁻²)/(φ²(n−1)),
   for the 00_COMMON definition of D.
2. Q part. Check [W1-L1.1]'s decomposition 0.02 + Q_S = RSS^y_S + a_S, with a_S = 0.02 + t_S/(n+1) + nτ_S/(n+1) and
   0 ≤ τ_S ≤ 1/((n+1)φ²). The key inequality a_A − a_U ≥ −nτ_U/(n+1) needs t_A ≥ t_U (P_U ≼ P_A) and τ_A ≥ 0.
3. The cross-multiplication step (R_U + a_U)/(R_A + a_U − δ) ≤ (R_U + δ)/R_A. API-FAVIID re-derived it: it is equivalent to
   (a_U − δ)(R_U + δ − R_A) ≥ 0, and this needs δ ≤ a_U, which holds because a_U ≥ 0.02 ≥ δ when (n+1)φ² ≥ 50.

**Points to watch (not errors).**
- **κ⁺ = O(1/n) only on an RSS floor.** Since ν ≈ n/2, the term ν/((n+1)φ²RSS^y_U) is O(1/n) only when RSS^y_U ≳ c·n, where
  RSS^y is on the y'y = n−1 scale. Lemma G (G2), lines ~170–185, supplies this for |T| ≤ B and T ⊆ S₀. The REPORT headline
  ("the EXP′ remainder is ≤ O(1/n) from above") should be read with that event in mind.
- The lemma is deterministic. The numerical check (6,000 pairs, max(R⁺ − κ⁺) = −0.005) is in `results/sanity.txt`, item 2.

## 2. Lemma M — PROOF.md lines 137–149

**Claim.** If E[j!a_j] ≤ C₀(Nξ)^j/Γ(j/2+1) for j = 1..N, with C₀ ≥ 1, then E max_j (j!a_j)^{1/j} ≤ c_ML·C₀·Nξ, where
c_ML = min_c c·E_{1/2}(1/c) = 3.8311.

**Steps to check.**
1. The pointwise inequality max_j Y_j ≤ λ(1 + Σ_j (Y_j/λ)^j), then taking expectations.
2. The constant. API-FAVIID checked it independently (`scripts/check_cML.py`, `results/check_cML.txt`): argmin c = 1.6837 and
   c_ML = 3.83114. The closed form e^{x²}erfc(−x) agrees with the series to 1e−15.
3. **What matters downstream.** The hypothesis has to be established in Theorems A and B. There it comes from three facts:
   C(N_K, j) ≤ N_K^j/j!; Lemma Tr′(a) with exponent e₁ = (u+j+3)/2 + 0.01; and (m/n)^{j/2} ≤ 1. API-FAVIID re-derived the exponent
   e₁ = ν − (m−j)/2 + 1 and agrees. Also check that the truncation event in Tr′(b) has family size N_n ≤ Cn^A. B ≤ 16 and |𝒲| ≤ 2^{s₀}
   are constants, so this holds.

**Framing caveat for the paper.** B_n ≤ 16, so 2^B ≤ 65,536 is a constant in any case. "2^B-free" improves the **constant**
(from about 2^{B}·poly(g) to 3.83). It does not improve the rate, and the paper should say this.

## 3. Theorem B's factorisation — PROOF.md lines 277–327, with Lemma S (151–161) and Lemma G (G3) (lines ~163–198)

**Claim.** On Q_n(m) ∩ 𝒢′_n, for every realised packing, q ≤ e^{κ̄_n+ζ_n}Q̄_n. Here Q̄_n = (p−s₀)⁻¹ Σ_K Σ_{W∈𝒲_K(m)} D′_{K,W} is
partition-free, and E Q̄_n ≤ c_ML C′_{0,n}|𝒲(m)|ξ_n.

**Steps to check, in order.**
1. The identity U_b* = U_{K_i,W_i} = 𝒯_{K_i} ∪ W_i holds for every group K_i in a block b on Q_n(m). This gives
   ‖P_{A_i}r‖²/‖r‖² = X′_{K_i,W_i,V_i}: the conditioning set is the same for all groups.
2. (G3): ‖P_{A_i}P_{A_k}‖ ≤ c_n = C_Gε_n, uniformly over group pairs and over U ⊆ S₀, from [C1] alone. Check two things:
   - **(a)** the population Schur complement has zero off-diagonal block, because Σ_UU⁻¹ is block-diagonal over groups;
   - **(b)** the claim that the Schur complement and the cosine matrix are Lipschitz in R̂_T **uniformly** over |T| ≤ k₀ = 2g + s₀,
     with no union bound. This is the least explicit step in the chain; the author lists it in "Needs escalation" item 2.
3. Lemma S. API-FAVIID re-derived it; it is fine as stated. Apply it with r = R ≤ ⌊B/g⌋ groups and c = c_n.
4. The ζ_n bookkeeping uses −log(1−x) ≤ x(1+2x) for x ≤ ½, Σ_i X′_i ≤ Bτ_n on (G5), and x′ ≤ −log(1−x′). The order is
   ζ_n = O(B²t_n(τ_n + c_n)) = O(log^{3/2}n/√n). API-FAVIID agrees.
5. Lemma X⁺ needs (G1) on U_b* ∪ V ⊆ C_b (|C_b| ≤ B) and (G2) on U_b*. κ̄_n is the maximum of κ⁺ over j ≤ B.
6. The multinomial step needs a′_{K,W,j} ≤ D′^j/j! for j ≥ 0 (a′_0 = 1) and e^{(κ̄+ζ)/j} ≤ e^{κ̄+ζ}. Then sum over blocks: each group
   lies in exactly one block, so Σ_b Σ_{K⊆b} = Σ_K. The normalisation (p−s₀)⁻¹ matches locked T22(i)'s q.
7. The deletion term. On Q_n, (U, U_b*∖U) ∈ 𝔙 with Γ = C_b. Then X⁻ and (G4) give e ≤ 2p√(n+1)e^{κ_e}e^{−νx₁/2}, where
   κ_e → 0.52/c_* is O(1), not o(1). That is harmless because of e^{−νx₁/2}.
8. **|𝒲(3)| ≤ 106.** This counts contexts for a null group K, which has up to 14 truth-carrying others; for a truth group the count
   is 92. P(Q_n(3)) → 1 comes from **Lemma P1′** (lines 245–262), which is load-bearing for "unconditional on S3/S4/S6" but is
   **not** on the R6 list. The referee should add it, or the statement should be read as conditional on Q_n(3).

**Numerical support** (W5-FAVIID sweep, re-computed by API-FAVIID):
- max q/Q_real = 0.9957 over 1,200 S3/S4/S6 rows, so the inequality holds even without e^{o(1)};
- Q_n held in 1,598/1,600 designs; the two failures are S6 at n = 200.

## 4. Corollaries C1–C3 — PROOF.md lines 407–434

- **C1 (δ₁ = O_P(√(log n/n)) on FAV).** The claim is that W3-PXN Lemma P2 "applies verbatim" to any Σ with λ_min ≥ λ₀, and that
  W3-PXN P8 (de-randomisation, XF VERIFIED by A-REV3) transfers locked T03(i). **Check the "verbatim" transfer**: A-REV3 verified
  P2 on LH-iid, not on block-equicorrelated Σ. SE is needed for |T| = O(log n), with |T|ε_n → 0.
- **C2 ((P1) on S3/S4/S6).** A composition: Δ_n = max(1 − π₀(S₀), δ₁) (W2-T26 Lemma 1), then Theorem B and C1, then
  T^max = 4max(1000, ℓ²). Check two things:
  - the idealisations (EX-A, EX-S, CAL, START, OUT) are the ones W2-T26 Theorem A uses;
  - "(T^max+1)Δ_n = O_P(log^{5/2}n/√n)" needs ℓ = O(log n). If ℓ is fixed, T^max = 4,000 and the rate is √(log n/n).
- **C3 (Thm 5(a)).** P(S₀ never drawn) ≤ E[(1 − π₀(S₀))^{Q_f}] → 0 under EX-S (iid draws from π₀), then locked T21 route (a).
  This step is short.

## 5. What API-FAVIID did and did not do
- **Did:**
  - recomputed every number in W5-FAVIID REPORT §§1, 4, 8 from the raw jsonl (`scripts/audit_w5faviid.py`, `scripts/audit_tails.py`);
  - fixed the numerical misstatements in a marked copy;
  - checked c_ML independently;
  - read §§1, 4, 5 and 9 and the deletion step line by line, in the same family, and found no error.
- **Did not:**
  - check [W1-L1.1], [W1-L1.2], [C1] or the (G3)/(G4) Lipschitz constants;
  - check Lemma P1′, Proposition N or Proposition B1;
  - check the W3-PXN P2 transfer in C1.

  None of the four items above is upgraded by this hand-off.
