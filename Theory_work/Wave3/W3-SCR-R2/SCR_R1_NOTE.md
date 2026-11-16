# SCR_R1_NOTE — is rider SCR-R1 (A1 with "fixed" dropped; n-dependent κ_n, b_n, M_n, σ_n) a short corollary of SCR-A?

W3-SCR-R2 coordinator, 2026-11-16 01:26 CST (`date`). Read of the frozen tree (MANIFEST_R2 96488f34…); no new proof;
paths under `Theory_work/Wave3/W3-SCR/`.

**Answer: YES, with one side condition stated in the rider.** Without that condition, the A1 route does not cover it.

1. A1's proof (lemmas/L3_screening.md:70–75) is SCR-A in its (A∞) form (L3:26–35, STATEMENT.md:87–90) plus Lemma B2d
   (STATEMENT.md:154, L4_bridges.md:49–51) plus arithmetic that holds n by n: τ_n² ≤ M_n² + σ_n² (L3:70),
   Γ_n ≥ κ_n²b_n²n/16 (L3:72), the squared denominator ≤ 4τ_*²c₁,ₙn (L3:74), so ρ_n² ≥ 200/64 for each such n (L3:75).
2. The (A∞) reduction (L3:28–35) has o(1) terms that depend only on n, p and q_n (T_n, a_{x_n}, r_n). They are
   relative to τ_n√(2 log p + log n), with σ ≤ τ_n. So a per-n bound ρ_n ≥ √(200/64) for all large n gives liminf > 1
   with no fixedness of κ, b, M or σ. SCR-A itself (STATEMENT.md:79–85) is non-asymptotic.
3. Fixedness enters A1 at exactly one step: L3:71, "Let n be so large that √(κ(n−1))·b ≥ 2M/√(n+1)". This is B2d's
   precondition √(φ(n−1))θ_min ≥ 2c_θ with c_θ ≤ M/√(n+1).
4. With n-dependent parameters, the growth condition (q_n+1)log p + log n ≤ c₁,ₙn gives κ_n²b_n²n ≥ 200M_n² log n.
   Hence κ_n b_n²(n²−1) ≥ 4M_n² whenever κ_n ≤ 50(n²−1)log n / n. That holds automatically when q_n ≥ s₀−1: then
   S = S₀∖{t} is admissible in φ^d, so κ_n ≤ 1 (STATEMENT.md:72). It is not automatic in general. For example,
   take q_n = 0 and s₀ > n²/4 identical true columns with equal coefficients: then κ_n = s₀, M_n = s₀b_n, and the
   precondition n² ≥ 4s₀ fails while the growth condition can hold. The SCR-A conclusion still holds there by direct
   computation of Γ_n(0), but not by the A1 argument.
5. So SCR-R1 = SCR-A(A∞) + B2d + L3:70–75 read per n, provided the rider adds "κ_n b_n²(n²−1) ≥ 4M_n² for all large
   n", or the sufficient κ_n ≤ 50(n²−1)log n/n (implied by M_n/b_n ≤ 50(n²−1)log n/n, since κ_n ≤ M_n/b_n at S = ∅;
   cf. R2 Opus BT1), or q_n ≥ s₀−1. The polynomial-p clause (L3:76, STATEMENT.md:162–163)
   needs c₁ bounded below and does not carry over: there the rider keeps only the explicit growth condition.
   This is a reading, not a checked proof: the rider still needs its own line check before it carries any label.
