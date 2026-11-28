# Audit audit1b-core1-s2: Theory_work/Wave3/API_AUDIT/audit1b/REQ_core1.md
claims: core1:B1.SL, core1:B1.IO, core1:B2.SL, core1:B2.IO, core1:B3.SL, core1:B3.IO, core1:B4-UP.SL, core1:B4.IO, core1:B4-LO.SL, core1:B5.SL, core1:B5.IO, core1:B6.SL, core1:B6.IO, core1:B7.SL, core1:B7.IO, core1:DR.SL, core1:SUM.SL, core1:PRIOR.SL, core1:ROW13.SL, core1:SCOPE.IO
stop_reason: end_turn

## core1:B5.SL

**Problem.** The claim "on smaller sets" (TRACK_B.md:101 and :248) fails for the Theorem 2 floor along sequences that Song–Liang admit.

- **Our side.** Theorem 2 (A3) asks a fixed level φ² on every S with |S| ≤ 5(A+1)(s₀+1) log n (READER_VERSIONS.md:274–275). The master form also needs a floor ψ_n on sets of size k̄_n = O(log n) (W3-POST/STATEMENT.md:108–109).
- **Song–Liang side.** Condition 3 (p. 955) quantifies over r̄_n other predictors, so its sets have size r̄_n + 1. Their hypotheses force only r_n ≻ 1 (Theorem 2, p. 953) and r_n ≤ r̄_n (condition (12), p. 952). Corollary 1 (p. 954) explicitly admits r̄_n ≺ log^k(n) for any k > 0.
- **Counterexample.** Take P_n = n², V_ξ = cI, r_n = r̄_n = ⌈log log n⌉ and ε_n² = (log n)²/n. Conditions (9)–(14), strict sparsity (4) and r_n ≻ 1 all hold. Song–Liang's sets then have size log log n + 1 = o(log n), at a level ≻ ε_n² → 0. Ours are of size c·log n at a fixed level φ², or in the master at ψ_n ≫ (log n)^{3/2}/√n ≫ ε_n².

So for Theorem 2 the floor is stronger in level and on larger sets. "Smaller sets" is correct only for the bounded-size conditions (Theorem 1 (A4), Theorem 1′ (A4′), master LSF(i)), or when r̄_n grows at least like log n. "Fixed against vanishing" and "stronger conclusion" stand.

## core1:B6.SL

**Problem.** The absence claim in AUDIT.md:42, "no counterpart in Thm 3, p. 956", is contradicted by the texts.

- Theorem 3 (p. 956) has the hypothesis "x_t is identifiable". That is Condition 3 (p. 955), introduced "to control the severeness of multicollinearity".
- Since e^{−u} ≥ 1 − u, Condition 3 itself (not only its sufficient forms) gives E(x_t + Σ b_i x_{j_i})² ≥ δ_n ≻ ε_n² for every choice of r̄_n other predictors and every b.
- That is a no-near-collinearity requirement on r̄_n + 1 columns at a vanishing level. With nε_n² → ∞ (p. 953), that level is ≫ 1/n.
- Our (A5), normalised, is λ_min(X_SᵀX_S/n) ≥ g₀/n on O(log n) columns (READER_VERSIONS.md:109–110; STATEMENT.md:71–73).

So for sets that contain a true predictor (and r̄_n ≥ |S|), Theorem 3 does have a counterpart, and at a higher level than ours (theirs population, ours sample). Only for sets of null columns alone is there none. "Stronger: no counterpart" is therefore not correct as stated.

Two further points:
- TRACK_B.md:125 and :249 attribute the absence to Theorems 1–2, where (11) and (14) are indeed conditions on V_ξ. That is consistent with the texts, but it is not the claim made in AUDIT.md:42; the two files cite different theorems.
- TRACK_B.md:126 calls (A5) the "population twin" of the ridge term. (A5) and (F_w) are conditions on the sample Gram matrix.

## core1:B7.SL

**Problem.** "Stronger than Condition 1 (implies it)" (TRACK_B.md:140 and :250; AUDIT.md:44) is false for the Gaussian rows of Theorem 2 as stated.

- Theorem 2 takes rows N_p(m_n, Σ_n) with no restriction on m_n (READER_VERSIONS.md:269; STATEMENT.md:106–107).
- Condition 1 (p. 953) needs constants M and δ. Song–Liang's Gaussian sufficient case is stated for "zero mean and var(x_i) = 1"; the audit has dropped the zero-mean part.
- **Counterexample.** Take Σ_n = I and m_{n,1} = n. With r = 1 and a₁ = δ, E exp{(δx₁)²} = (1 − 2δ²)^{−1/2} exp{δ²n²/(1 − 2δ²)} → ∞ (and it is infinite if δ² ≥ ½). No fixed M exists, so Condition 1 fails while every hypothesis of Theorem 2 holds.

The implication holds only with sup_n max_j |m_{n,j}| < ∞. The "Thm 9 (A3)" half of TRACK_B.md:140 cannot be judged, because that text is not supplied; the Gaussian-row half already refutes the verdict.

AUDIT1 core1:B1.SL VERDICT=NO-FINDING
AUDIT1 core1:B1.IO VERDICT=NO-FINDING
AUDIT1 core1:B2.SL VERDICT=NO-FINDING
AUDIT1 core1:B2.IO VERDICT=NO-FINDING
AUDIT1 core1:B3.SL VERDICT=NO-FINDING
AUDIT1 core1:B3.IO VERDICT=NO-FINDING
AUDIT1 core1:B4-UP.SL VERDICT=NO-FINDING
AUDIT1 core1:B4.IO VERDICT=NO-FINDING
AUDIT1 core1:B4-LO.SL VERDICT=NO-FINDING
AUDIT1 core1:B5.SL VERDICT=REFUTED
AUDIT1 core1:B5.IO VERDICT=NO-FINDING
AUDIT1 core1:B6.SL VERDICT=REFUTED
AUDIT1 core1:B6.IO VERDICT=NO-FINDING
AUDIT1 core1:B7.SL VERDICT=REFUTED
AUDIT1 core1:B7.IO VERDICT=NO-FINDING
AUDIT1 core1:DR.SL VERDICT=NO-FINDING
AUDIT1 core1:SUM.SL VERDICT=NO-FINDING
AUDIT1 core1:PRIOR.SL VERDICT=NO-FINDING
AUDIT1 core1:ROW13.SL VERDICT=NO-FINDING
AUDIT1 core1:SCOPE.IO VERDICT=NO-FINDING