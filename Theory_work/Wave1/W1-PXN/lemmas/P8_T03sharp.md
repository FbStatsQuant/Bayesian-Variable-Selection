# Lemma P8♯ — posterior concentration on LH-iid via T03♯ (repair of PROOF §9, dependency point D1)

Status: PROVED (by this seat); XF VERIFIED WITH MINOR FIXES (R19, Codex gpt-6.1-sol), minor fix applied — v2, 2026-11-08. Replaces the [T03] citation in API-PXNGAP PROOF §9
(`NBH/branch_snapshots/API-PXNGAP/PROOF.md:403-417`). NBH = `Theory_work/Old_Projects/New_BVS_Headquarters/`.

## Why a repair
PROOF §9 applies "locked T03(i) (PROVED-LOCKED): under G, R, SE, BM-∞" (PROOF.md:24). The locked statement
(`NBH/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/STATEMENT.md` §2-§3) has a further
hypothesis H-T02 (= T02(i), "unproved v3 conjecture, used as hypothesis"), which PROOF §9 does not discharge; T01–T03
are moreover "SAME-FAMILY-ONLY" (registry TH09). The restated theorem T03♯ (W1-T03R) needs no H-T02 and carries
"T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED"
(`Theory_work/State_of_Project/sections/04_theory.tex:765`).

## Cited input
**[T03♯]** theorem of record TH128 = `NBH/branch_snapshots/W6-FIXREV2/STATEMENTS.md:19-60` ("V03 and A-REV2: VERIFIED under exactly these hypotheses"); final card TH09 (`04_theory.tex:763-818`).
Hypotheses: R1 (fixed-design triangular array, s₀ fixed, p_n ≤ n^A, s₀ ≤ K eventually); G (ε ~ N(0, σ²I_n), design fixed);
R (‖μ‖² ≤ Mn, λ_min(R_{S₀}) ≥ φ₀²); SE_λ(j₀): λ_min(R_{S₀∪J}) ≥ φ₀² for all J ⊆ [p]∖S₀, |J| ≤ j₀ := ⌈(2A+1)s₀⌉+1;
SE_w(m♯_n; g₀): λ_min(G_{S₀∪J}) ≥ g₀ > 0 for all |J| ≤ m♯_n; BM-∞: θ*²_min nφ₀²/(σ² log n) → ∞.
Conclusion (i): 1 − π(S₀) = O_{P₀}(√(log n/n)).
m♯_n bound (W1-T03R/REPORT.md:40): m♯_n ≤ min{K, s₀ + ⌈(log C(p,s₀) + ((s₀+1)/2) log n + ½ log n)/log 2⌉}.

## Statement
On LH-iid (STATEMENT.md §1) with 18 ≤ p_n ≤ n^A, A ≥ 1 fixed: δ₁ := 1 − π(S₀) = O_P(√(log n/n)) under the joint law of
(X^r, ε). Hence E δ₁ → 0 and P(π(S₀) > ½) → 1.

## Proof
1. *Sizes.* m♯_n is defined exactly as in TH128 (`NBH/branch_snapshots/W6-FIXREV2/STATEMENTS.md:22-26`):
   q_k := C(p,k)w(k), R_m := Σ_{k=max(m+1,0)}^{K} q_k/w(s₀), m♯_n := min{m ≥ s₀ : R_m ≤ n^{−(s₀+2)/2}}.
   *Bound (proved here).* C(p,k)/C(2p−1,k) = ∏_{i<k}(p−i)/(2p−1−i); the i = 0 factor is ≤ 1 and each i ≥ 1 factor is ≤ ½
   (2(p−i) ≤ 2p−1−i ⇔ i ≥ 1), so q_k = ½C(p,k)/C(2p−1,k) ≤ 2^{−k}. Also 1/w(s₀) = 2C(2p−1,s₀) ≤ 2(2p)^{s₀}. Hence
   R_m ≤ 2(2p)^{s₀}Σ_{k>m}2^{−k} = 2^{1−m}(2p)^{s₀}, and R_m ≤ n^{−(s₀+2)/2} as soon as
   m ≥ 1 + s₀ log₂(2p) + ((s₀+2)/2) log₂ n. With p ≤ n^A: m♯_n ≤ k_n := max{s₀, ⌈1 + s₀ + (As₀ + (s₀+2)/2) log₂ n⌉} = O(log n).
   The locked cutoff m_n = ⌈(s₀ log(2p) + (s₀+1)(log n)/2 + ½ log n)/log 2⌉ (used by PROOF P2) is also O(log n).
   Put **L_n := s₀ + max{m_n, k_n, j₀, g, s₀+2} = O(log n)**: every set used by T03♯ (|T∖S₀| ≤ max(j₀, m♯_n)), by
   PROOF P2(a) (|T| ≤ m_n + s₀), by Lemma E on within-group sets (|T| ≤ g) and on 𝔉_n (|T| ≤ s₀+2) has size ≤ L_n.
2. *Design event.* Let ℰ♯_n be the X-event on which
   (a) λ_min(R̂_T) ≥ φ₀² := λ₀/2 for every nonempty T ⊆ [p] with |T| ≤ L_n (not only sets anchored at S₀), where λ₀ := λ_min(Σ) ≥ (1−ψ̄)(1−ρ) (PROOF F4);
   (b) ‖μ‖²/n ≤ M := 2θᵀΣθ + 1;
   (c) min_{j∈S₀} θ*_j² ≥ b_min := ½ min_i,h(β_i²ψ_i², β_i², (β^vis_h)²) (θ*_j = θ_j·sd_j, sd_j the sample SD);
   (d) s₀ ≤ K (deterministic: K = min(p, ⌊n/2⌋) ≥ s₀ once p_n ≥ s₀ and n ≥ 2s₀ + 1; p_n → ∞).
   P(ℰ♯_n) → 1: (a) ‖R̂_T − Σ_T‖_op ≤ |T| max_{j≠k}|r̂_jk − Σ_jk| ≤ L_n δ_n = O((log n)^{3/2}/√n) → 0
   with probability ≥ 1 − 3n^{−2} by [CONC′] (`lemmas/CR_corr_tails.md`, δ_n = 32√(2(A+1) log n/(n−1))), and λ_min(Σ_T) ≥ λ₀ by interlacing, so λ_min(R̂_T) ≥ λ₀ − o(1) ≥ λ₀/2;
   (b), (c): the finitely many columns of 𝒮𝒱 (|𝒮𝒱| = gs₀) satisfy the SLLN; ‖μ‖²/n → θᵀΣθ and sd_j → 1 a.s.
   (This is PROOF P2 with the size range enlarged from m_n + s₀ to L_n; the proof is unchanged.)
3. *Hypotheses of T03♯ on ℰ♯_n.* Fix a deterministic sequence x_n ∈ ℰ♯_n (n ≥ n₀) and work under P(· | X^r = x_n);
   since ε ⊥ X^r, this is the fixed-design model y^r = x_nθ + ε with Gaussian noise: G holds. R1: s₀ fixed,
   p_n ≤ n^A, s₀ ≤ K by (d). R: by (b) and (a) with T = S₀. SE_λ(j₀): |S₀ ∪ J| ≤ s₀ + j₀ ≤ L_n, so (a) (and every nonempty subset, as TH128's equivalent form requires).
   SE_w(m♯_n; g₀) with g₀ := φ₀²: |S₀ ∪ J| ≤ s₀ + m♯_n ≤ L_n, so λ_min(G_{S₀∪J}) = (n−1)λ_min(R̂_{S₀∪J}) ≥ (n−1)φ₀² ≥ φ₀².
   BM-∞: θ*²_min nφ₀²/(σ² log n) ≥ b_min nφ₀²/(σ² log n) → ∞, a deterministic lower bound common to all sequences.
   All constants (A, s₀, M, φ₀, g₀, σ²) are fixed and do not depend on the sequence. T03♯(i) gives
   1 − π(S₀) = O_P(√(log n/n)) under P(· | X^r = x_n).
4. *De-randomisation.* PROOF §9's lemma (PROOF.md:405-410) with 𝒜′_n := ℰ♯_n, Z_n := δ₁, r_n := √(log n/n): its
   hypothesis is exactly step 3 for every deterministic sequence in ℰ♯_n; conditional probabilities given X^r = x are
   evaluations of the ε-integral at x (ε ⊥ X^r). Hence δ₁ = O_P(r_n) unconditionally. δ₁ ∈ [0,1], δ₁ → 0 in
   probability ⇒ E δ₁ → 0 (bounded convergence); P(δ₁ ≥ ½) → 0. ∎

## Remarks
- **A > 1.** Nothing requires p ≤ n: SE ranges only over sets of size L_n = O(log n) ≪ n; A enters j₀, k_n (hence L_n),
  the BM(c) constant c₀(s₀, A) (not used: BM-∞ holds), and T03♯'s unnamed onset.
- **What changed vs PROOF §9.** Input [T03] → [T03♯]; P2(a)'s size range m_n + s₀ → L_n (both O(log n)); g₀ added.
  The rate and the de-randomisation argument are unchanged.
- **Status of the input.** T03♯ is XF VERIFIED (A-REV2) as a fixed-design theorem; its card's repair row says "no
  random-design ... extension" (04_theory.tex TH09 card), which is why step 4 is needed; step 4 is this file's (and
  PROOF §9's) own argument and must be checked.
