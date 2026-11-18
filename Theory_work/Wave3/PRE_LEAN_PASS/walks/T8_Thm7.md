# T8 — full proof walk: Theorem 7 (card row 3.2; master `W3-RM2-R:RM2-F-plus@1.0.1`)

Walker: Fable-CT-B (Fable 5.2, Claude Third), 2026-11-18. Brief: `Theory_work/Dept/briefs/PRE_LEAN_WALK_BRIEF.md` (origin/dept/theory).
Sources read at origin/main `668b413f`. Read-only; no theory file edited. Abbreviations as in `T6.md`
(RDR, RM2R, RM2, RM, GROW). Steps already walked in `T6.md` are cited by section there and not repeated.

## Findings

| # | severity | file:line | claim | why |
|---|---|---|---|---|
| G1 | MINOR | RM2R `STATEMENT.md:144-148, 161-162`; `Scripts/SMC_BVS/core/v3_fit.R:131, 173-176`, `v3_run.R:246-267` (main 668b413f) | Row 3.2's delivery clause rests on DLV-0 at core pin 72785fe | Same as `T6.md` F2: the core on main is three commits past the pin and ends `v3_fit` with code that has three `stop()` rows not in DLV-0's exit list. I checked that none can fire on an output run. For Theorem 7 there is no recorded or pending result that carries delivery to the new code (the transfer argument in W3-D5P L3 (0.5) is written for LIST-R). The clause is true for the core on main; the record does not say so. |
| G2 | NOTE (Lean) | RM2R `lemmas/Q2_TL_c.md:118-132`; `Theory_work/State_of_Project/sections/04_theory.tex:784-788` | [POST] under (T1-F♭) with the BM(c) branch | The constant c₀(s₀, A) = max{4C_*, 32[s₀(A + 1) + 2]} contains C_*, "the locked T03 proof constant". The reader's Theorem 7 (A1) and Remark (a) say the beta-min constant is explicit in (s₀, A, M, σ², φ₀). A Lean statement of Theorem 7 with BM(c) needs C_* as a defined number; it lives inside SOP:TH09's proof, not in any statement walked here. With the BM-∞ branch nothing is needed. |

(No FATAL, no MAJOR.)

---

## Chain

    reader Thm 7 (RDR:821-857)
      └─ bridges B7.1′–B7.4′, B7.2, B7.3, B7.5 (RDR:881-892); B1.1–B1.4 (RDR:211-214)     §1
          └─ RM2-F-plus (RM2R STATEMENT:166-176; Q6_assembly §1)                          §2
              ├─ [SAND(Q)]: Lemma B1 + SAND-F-c (Q1_sandF_c)                              §3
              ├─ [NA(Q)]: NA-conv, NA-W (RM2 L2_width §1)            — T6 §A4
              ├─ (W) from (W-χ) or (W-loc): sufficient forms (RM2 L2_width §3)            §4
              ├─ [TL(Q)]: TL-F-c (Q2_TL_c §4)                                             §5
              ├─ [POST], [MODE]: POST/MODE-F (Q2_TL_c §6) ⇐ SOP:TH09@1.0.2 (recorded)     §6
              ├─ RM0-plus (a), (b⁺), (c⁺)                            — T6 §A2
              └─ delivery: DLV-0                                     — T6 §A7

## 1. Reader statement → master hypotheses and conclusions

Master hypotheses (RM2R STATEMENT:166-167): Setting F; (T1-F♭), (FL) = (FL-16) + (FL-Q), (V♭), (L^b) with b < β(η, A),
(BM-W⁺), (W).

| master hypothesis | supplied by | check |
|---|---|---|
| Setting F | preamble (fixed design, non-constant raw columns), (S1), (S2) | identical. |
| (T1-F♭): fixed s₀, p ≤ n^A, ‖μ‖² ≤ Mn, SE_λ(j₀), SE_w(m♯_n; g₀), BM-∞ or BM(c), c > c₀ | (A1): Theorem 1's (A2)–(A5) + beta-min; B7.1′ with B1.1–B1.4 | B1.1: ‖Xθ*‖ ≤ s₀θ̄√(n − 1), M = s₀²θ̄². ✓ B1.2: \|S₀ ∪ J\| ≤ (2A + 2)s₀ + 2. ✓ B1.3: re-derived. For i ≥ 1, (p − i)/(2p − 1 − i) ≤ ½, so R_m ≤ C(p, s₀)·2^{−(m − s₀)}, and m♯_n ≤ s₀ + ⌈(log C(p, s₀) + ((s₀ + 2)/2) log n)/log 2⌉; then s₀ + m♯_n ≤ 3(A + 1)(s₀ + 1) log n for n ≥ 3 (1.45As₀ + 2.725s₀ + 2.45 ≤ 3As₀ + 3A + 3s₀ + 3). ✓ B1.4: the reader beta-min is BM(c) with c = C_β²φ₀²; the master's BM(c) is θ*²_min ≥ cσ² log n/(nφ₀²) — same normalisation. ✓ |
| (FL-16), (FL-Q) | (A2) | identical. |
| (V♭): fixed M_V > M_V⁰ = (σ√(2A) + √((2A + 1)C_R))², C_R = 3(M + σ²) | (A3) with Remark (a) | identical (B7.4′). |
| (L-feas), (L-gain) with η ∈ [0, η_A) | (A4) | identical. |
| (L-size^b), b < β(η, A) | (A5)(a): \|Q\| ≤ s₀ + (1 − δ) log n ≤ n^b eventually, for any fixed b ∈ (0, β(η, A)) (β > 0 because η < η_A); (A5)(b): assumed | ✓ |
| (W) | (A5)(a): (W-χ) with δ₁ = δ; (A5)(b): (W-loc) with ν_n = h log₂ n (so ν_n log 2 = h log n), h + b < ½, L_n → 0, L_n² log(\|Q\| + 1) = o(log n) | §4. The variance clause of (W-loc) is not in the reader text; it follows from the ℓ¹ clause, (FL-Q) and L_n → 0 (η_n = L_n²/φ₀²). ✓ |
| (BM-W⁺): √λ_n ≥ 2(d_n + √(2 log n)), λ_n ≥ c_TL log n, c_TL > c_TL⁰ = 8(A + 1) + 4(2A + 1)C_R/σ² | (A5)(a) + (A1): B7.2′; (A5)(b): B7.3′ | B7.2′ recomputed: Lemma d gives d_n² ≤ 2(q + 1) + 4 log(2p) ≤ (2 + 4A − 2δ) log n + O(1) ≤ D log n for any fixed D > 2 + 4A; then 4(d_n + √(2 log n))² ≤ 8(1 + √(D/2))² log n; and λ_n = (n − 1)φ₀²θ*²_min/σ² ≥ ((n − 1)/n)C_β²φ₀² log n, which exceeds max{c_TL, 8(1 + √(D/2))²} log n for large n because the reader's inequality on C_β²φ₀² is strict. ✓ B7.3′ recomputed: with C_Q > 32 and C_Q > 64A + c, ((n − 1)/n)C_Q(q + log n) ≥ 32(q + 1) + 64 log(2p) + c log n for large n, which is (BM-Q♭) with c_TL = c > max{16, c_TL⁰}. ✓ Under the BM-∞ branch with (A5)(a): (BM-W) holds (d_n² = O(log n)) and (BM-W) ⇒ (BM-W⁺). ✓ |
| premises and configuration; (D) | (S3); (S4), B7.5 | identity by reference, as `T6.md` §A0. |

Conclusions: identical in form to Theorem 6's; the master's (C1⁺) gives them (data event 𝒢⁺_n = 𝓜_n ∩ 𝒦_n; under (D)
output for every valid non-degenerate input and P(Ŝ⁺ = S₀) → 1). Validity with probability one in Setting F: X^r is
fixed with non-constant columns, and y^r is constant only if ε lies on a line — a null set for n ≥ 2 (`Q4_core_plus.md`
(c⁺)). ✓ Remark (b) is (c⁺)'s inequality. ✓

Law and quantifiers: probability over the noise only (design fixed); "for large n" in (A3), (A4) and in (BM-W⁺).

**Verdict 1: no finding** (G2 is a note on where the beta-min constant is defined).

## 2. Assembly of RM2-F-plus (RM2R `lemmas/Q6_assembly.md:16-41`)

(T1-F♭) supplies (F0)'s energy bound, p ≤ n^A and fixed s₀; (L-size^b) gives q ≤ n^b, hence q log n/n → 0; (L-feas) gives
q ≤ K. Then: [SAND(Q)] from Lemma B1 and SAND-F-c; [NA(Q)] from NA-W under (F0), (FL-Q), (W); [TL(Q)] from TL-F-c
under (F0), (FL-Q), (BM-W⁺), P(𝒵_n) → 1; [POST], [MODE] from POST/MODE-F; [E4] recorded; RM0-plus with 𝓛′ = 𝓛.
Every hypothesis is used: (T1-F♭) in all four; (FL-16) in SAND-F-c through (G3a); (FL-Q) in NA-W and TL-F-c; (V♭) in
SAND-F-c Step 2(a) only; (L-gain) in SAND-F-c Steps 1 and 2(b); (L-feas) in 2(a) and in |Q| ≤ K; b < β(η, A) in 2(b);
(W) in NA-W and, through 𝒵_n, in TL-F-c; (BM-W⁺) in TL-F-c. Nothing unstated is used.

**Verdict 2: no finding.**

## 3. [SAND(Q)]: Lemma B1 and Lemma SAND-F-c (RM2R `lemmas/Q1_sandF_c.md`; `W3-RM2-R:SAND-F-c@1.0.1`)

* Lemma B1: partition-free ⇒ block-relative forms, for any partition with blocks ≤ 16 (sets inside a block have
  size ≤ 16; U ⊆ C_b ∖ {j} has |U| ≤ 15). ✓ In Setting F the method's partition is a deterministic function of the fixed X.
* Fact 1: P(χ²_d ≥ dτ) ≤ (τe^{1−τ})^{d/2} ≤ (τe^{1−τ})^{1/2} for τ > 1; at most 3^{16} pairs (V, N) per block, at most p blocks. ✓
* Fact 2 (RSS floor in τ-form): from (0.1) of the toolkit and AM–GM 2σ√(n − 1)√Λ_U ≤ (n − 1)τ²_U. ✓
* Step 1 (size ≤ 2k₀): per-block optimality (1.1) with w(k − 1)/w(k) = (2p − k)/k ≥ p/k̃; decomposition
  ‖Πμ + Πε‖² ≤ (1 + ε₁)‖Πε‖² + (1 + 1/ε₁)‖Πμ‖²; ‖Πμ‖² ≤ dητ²_U log n by (L_b) along a chain (each U_{s−1} contains the
  block's truths because S₀ ⊆ Q); this gives W_b ≥ τ_n(k̃) (2.2). Choice of ε₁: Aε₁ + (1 + 1/ε₁)η/2 < ½, possible iff
  √(2Aη) + η/2 < ½, i.e. η < η_A — implied by (B). Tail (2.3) and the dyadic ladder: exponent −ξ/(1 + ε₂) with
  ξ = (1 − η₁)/2 − Aε₂ > 0; geometric sum over the rungs. Re-derived; correct. ✓
* Step 2(a) (the changed step, [R-3]): on 𝓩, |Z| ≤ z_n ≤ z̄_n = √(2A log n) + √(42 log 2 + 2 log log n); with |δ| ≥ √(M_V log n):
  (δ + σZ)² ≥ (√M_V − σ√(2A))² log n − O(√(log n·log log n)); against the cost (A + ½) log n + O(1) after division by 2C_R.
  The bracket (√M_V − σ√(2A))²/(2C_R) − A − ½ is positive iff M_V > M_V⁰. ✓ Feasibility of S̃ ∪ {j} from (L-feas) and k̃ ≤ 2k₀. ✓
* Step 2(b): margin [½ − η/2 − √(2Aη) − b] log n − o(log n) = [β(η, A) − b] log n − o(log n) > 0. ✓
* Probability: P(𝓩ᶜ) ≤ 1/log n (the slowest term), P(𝓔^blkᶜ) → 0, ladder term → 0. Event: every maximiser of γ₀ on Ω.

Constants: ε₁ fixed from (A, η); C₁, C₂ from (A, κ_E, ε₁); n₀ from (A, σ², M, M_V, φ₀, η, b, s₀).

**Verdict 3: no finding.**

## 4. (W) from the reader's two size conditions (RM2 `lemmas/L2_width.md:123-180`; `W3-RM2:W-suff@1.0.3`)

* (i) (W-δ) ⇒ (W): a⁰_n(k) − a_{n,δ₀}(k) ≥ δ₀√(log n)/(2√(2A + 2)). ✓ (as `T6.md` §A5)
* (iii) (W-χ) ⇒ (W-δ): the inequality (u_{T,l}ᵀg)² ≤ (u_{Q_l,l}ᵀg)² + ‖(P_Q − P_{S₀})g‖² (orthogonal split of (I − P_T)x_l and
  Cauchy–Schwarz in ℝ²; range(P_{Q_l} − P_T) ⊆ range(P_Q − P_{S₀})) re-derived; then (G3) over at most p unit vectors and
  E‖(P_Q − P_{S₀})g‖² = |Q ∖ S₀| ≤ (1 − δ₁) log n; the level gains (δ₁ − δ₀) log n − O(log log n). ✓ This is case (A5)(a).
* (v) (W-loc) ⇒ (W-ref): u_{T,l} = v − Σ_t(λ_t‖x_t‖/‖a‖)(x_t/‖x_t‖) with ‖v‖ ≤ (1 + η_n)^{1/2}, atom ℓ¹-norm ≤ L_n/φ₀, at most
  p·2^{ν_n} lines. ✓ (iv) (W-ref) ⇒ (W-unif) with δ = (1 − 2b − 2h)/4: identity 1 − 2b − 2δ = 2h + 2δ; error e_n = o(√log n). ✓
  (ii) (W-unif) ⇒ (W-δ): k + 1 ≤ 2n^b. ✓ This is case (A5)(b); **h + b < ½ is used in (iv)**.
* Standard facts used: (G1)–(G3) of Lemma 0 (maximal inequalities for Gaussians; proved in the file).

**Verdict 4: no finding.**

## 5. [TL(Q)]: Lemma TL-F-c (RM2R `lemmas/Q2_TL_c.md:57-107`; `W3-RM2-R:TL-F-c@1.0.1`)

Identity (4.1) and the probabilities of ℬ_n, 𝒵⁺_n: as `T6.md` §A4 (unchanged from the parent). The changed steps:
* Size [R-4]: |Z_{A,i}| ≤ d_n + √(2 log n) ≤ ½√λ_n by (BM-W⁺)(i), so the first square is ≥ σ²λ_n/4; the subtracted term is
  ≤ σ²(2A + 2) log n; RSS_A − RSS_T ≥ σ²(c_TL/4 − 2A − 2) log n > 0 by (BM-W⁺)(ii). ✓
* Score [R-5]: F(A) − F(T) ≤ (A + ½) log n + (3/2) log 2 + 2κ_E − σ²(λ_n/4 − (2A + 2) log n)/(2C_R) ≤ −γ log n + O(1),
  γ = σ²(c_TL/4 − 2A − 2)/(2C_R) − (A + ½) > 0 iff c_TL > c_TL⁰. ✓ Algebra re-derived.
* Implications [R-2] (a)–(c) into (BM-W⁺): (2(d_n + √(2 log n)))² ≤ 16(d_n² + log n). ✓

Constants: c_TL⁰ depends on (A, M, σ²) through C_R; n₀ on (A, M, σ², φ₀, c_TL), the n₀ of (BM-W⁺) and q log n/n.

**Verdict 5: no finding.**

## 6. [POST], [MODE]: Lemma POST/MODE-F (RM2R `lemmas/Q2_TL_c.md:116-132`)

(T1-F♭) is the hypothesis list of SOP:TH09 with either beta-min branch (card text
`State_of_Project/sections/04_theory.tex:780-788`, read: "BM-∞ … Alternatively BM(c) uses a fixed c > c₀(s₀, A)"; final
statement "1 − π(S₀) = O_P(√(log n/n))"). `SOP:TH09@1.0.2` is recorded ("PROVED-CHECKED (T03♯ only …)"); the walk stops
there. O_P ⇒ [POST] by boundedness; [MODE] by {π(S₀) > ½} ⊆ 𝓜_n and Markov. ✓ See G2 for the constant C_*.

**Verdict 6: no flaw. G2 (NOTE).**

## 7. Core and delivery

RM0-plus (a), (b⁺), (c⁺): `T6.md` §A2 (design-free; applies to Setting F verbatim). DLV-0: `T6.md` §A7; finding G1.

---

WALK COMPLETE (T8: Theorem 7). Findings: 0 FATAL, 0 MAJOR, 1 MINOR (G1), 1 NOTE (G2).
