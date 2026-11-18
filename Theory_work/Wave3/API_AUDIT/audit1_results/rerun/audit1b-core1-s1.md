# Audit audit1b-core1-s1: Theory_work/Wave3/API_AUDIT/audit1b/REQ_core1.md
claims: core1:B1.SL, core1:B1.IO, core1:B2.SL, core1:B2.IO, core1:B3.SL, core1:B3.IO, core1:B4-UP.SL, core1:B4.IO, core1:B4-LO.SL, core1:B5.SL, core1:B5.IO, core1:B6.SL, core1:B6.IO, core1:B7.SL, core1:B7.IO, core1:DR.SL, core1:SUM.SL, core1:PRIOR.SL, core1:ROW13.SL, core1:SCOPE.IO
stop_reason: end_turn

## core1:B6.SL

**Problem.** The absence claim in `AUDIT.md:42` ("stronger: no counterpart in Thm 3, p. 956, which controls sensitivity only") is contradicted by the texts given.

- **Theorem 3 has a collinearity hypothesis.** Its hypothesis "x_t is identifiable" is Condition 3 (SL p. 955). SL introduce it as the condition "which controls the severeness of multicollinearity through the sequence {ε_n}". It bounds E[exp{−(x_k + Σ b_i x_{j_i})²}] ≤ 1 − δ_n, δ_n ≻ ε_n², for any r̄_n other predictors and any b. That is a vanishing-level no-near-collinearity condition on growing sets, the same type as (A5).
- **Part of (A5) is the sample analogue of Condition 3.** By (F_w) (`STATEMENT.md:71–73`; `READER_VERSIONS.md:109–110`), for every t ∈ S₀, every J with |J| ≤ m♯_n and every b, ‖x_t + X_J b‖² ≥ g₀(1 + ‖b‖²) ≥ g₀. This is Condition 3 in sample form, at level g₀/(n−1) on the normalised scale.
- **On those sets the direction is reversed.** SL's (10), p. 952, gives ε_n² ≻ r̄_n ln(P_n)/n. In the Gaussian sufficient form (pp. 955–956), Condition 3 therefore needs var(x_t + Σ b_i x_{j_i}) ≳ δ_n ≻ ε_n² ≫ 1/n. On truth-anchored sets SL's level is higher than ours, so "stronger" is a direction error there.
- **What survives.** Only the null-only part of (A5) (collinearity among columns outside S₀) has no counterpart in Theorem 3. The other wording under the same id (`TRACK_B.md:125–126` and `:249`: none in Theorems 1–2, since (11) and (14) are on V_ξ) is not broken.

## core1:B7.SL

**Problem.** "Stronger than Condition 1, p. 953 (implies it)" (`TRACK_B.md:140`, `:250`; `AUDIT.md:44`) is a direction error for Theorem 2 as stated.

- **Mismatch in the hypotheses.** Theorem 2 takes rows N_p(m_n, Σ_n) with m_n unrestricted (`READER_VERSIONS.md:269`; `STATEMENT.md:106–107`). SL verify Condition 1 only for "a Gaussian process with zero mean and var(x_i) = 1" (p. 953), and Condition 1 is not translation-invariant.
- **Counterexample.** Take r = 1, a₁ = δ and x_{j₁} ~ N(m, 1). Then E[exp(δ²x²)] = (1 − 2δ²)^{−1/2} exp{δ²m²/(1 − 2δ²)} ≥ exp(δ²m²). If sup_n ‖m_n‖_∞ = ∞ (for example m_{n,1} = n), no constants M, δ > 0 satisfy Condition 1, yet the rows meet Theorem 2's hypothesis.
- **Consequence.** Gaussian rows imply Condition 1 only with bounded (for example zero) means; in general neither condition implies the other.
- **Not checkable here.** The first half of `TRACK_B.md:140` ("Thm 9 (A3) … implies it") cannot be judged: the text of Thm 9 (A3) is not in the material.

AUDIT1 core1:B1.SL VERDICT=NO-FINDING
AUDIT1 core1:B1.IO VERDICT=NO-FINDING
AUDIT1 core1:B2.SL VERDICT=NO-FINDING
AUDIT1 core1:B2.IO VERDICT=NO-FINDING
AUDIT1 core1:B3.SL VERDICT=NO-FINDING
AUDIT1 core1:B3.IO VERDICT=NO-FINDING
AUDIT1 core1:B4-UP.SL VERDICT=NO-FINDING
AUDIT1 core1:B4.IO VERDICT=NO-FINDING
AUDIT1 core1:B4-LO.SL VERDICT=NO-FINDING
AUDIT1 core1:B5.SL VERDICT=NO-FINDING
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