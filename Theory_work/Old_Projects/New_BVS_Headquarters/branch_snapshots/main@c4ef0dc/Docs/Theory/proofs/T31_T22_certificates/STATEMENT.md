# STATEMENT — T31 (T22), part (i) only

Method: SMC-BVS v3.0 (METHODOLOGY_v3.md, SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c).

## Source text (verbatim, clause (i) of the theorem file)

> (i) Under T12: P_𝓒(Z ≥ αẐ) ≥ 1 − α and E_𝓒 log Ẑ ≤ log Z; so 0.05Ẑ has coverage at least 95% under the ideal
> final-run assumptions; it is not a relative-error interval; conditioning afterwards on final flags does not preserve
> this coverage automatically.

Assumptions listed for the whole file: EX-A, EX-S, CAL. Clause (i) uses T12 (a sibling conjecture), which enters below only
as the explicit hypothesis (H-T12).

## 1. Setting and definitions

Fixed data (X, y), already standardised as in the method (§4): n ≥ 3, ‖y‖² = n − 1 > 0, p ≥ 1 retained columns. All
objects below are deterministic functions of the data unless stated otherwise.

- State space Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋) (finite).
- G_S = X_SᵀX_S, z_S = X_Sᵀy, H_S = (n+1)G_S + I, D_S = det H_S / det(G_S + I), Q_S = yᵀy − n z_SᵀH_S⁻¹z_S,
  ν = 0.01 + n/2, a₀ = b₀ = 0.01;
  m(S) = (2b₀)^{a₀} Γ(ν) / (π^{n/2} Γ(a₀)) · D_S^{−1/2} (2b₀ + Q_S)^{−ν} (for S = ∅: D_∅ = 1, Q_∅ = yᵀy).
- w(k) = ½ / C(2p−1, k); W_K = Σ_{k≤K} C(p,k) w(k); ϖ(S) = w(|S|)/W_K.
- Evidence Z = Σ_{S∈Ω} ϖ(S) m(S). BF(S) = m(S)/m(∅).
- Blocks C₁, …, C_J (a fixed partition of [p] determined by X); tables r_b(A) = BF(A), A ⊆ C_b.
  γ₀(S) = ϖ(S) ∏_b r_b(S ∩ C_b); Z̄₀ = Σ_{S∈Ω} γ₀(S); discrepancy d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b).
- Calibration 𝓒: the random object produced by the calibration phase (grid 0 = φ₀ < φ₁ < … < φ_T = 1, T, L, N_e, tier,
  candidate set and all other frozen settings). A calibration value c is **successful** if it yields a frozen grid, so that
  the method runs its final phase.
- **Final run given c.** For a successful c: 4 islands r = 1, …, 4, each with N_e particles in Ω, run with the frozen grid
  of c and the final streams 10–13 (island r uses stream 9 + r). Writing S_{r,i}^{(t−1)} ∈ Ω for particle i of island r
  at the moment stage t's reweighting is applied (t = 1, …, T), the island evidence is (method §6.12)

  Ẑ_r = m(∅) Z̄₀ ∏_{t=1}^{T} (1/N_e) Σ_{i=1}^{N_e} exp{(φ_t − φ_{t−1}) d(S_{r,i}^{(t−1)})},

  and the pooled evidence is Ẑ = ¼ Σ_{r=1}^{4} Ẑ_r. The reported lower bound is 0.05·Ẑ.
- P_c, E_c: probability and expectation over the final streams 10–13, with the calibration fixed at c. Under CAL and EX-S
  (and joint measurability of the final run in (c, streams)), these give a version of the conditional law and expectation
  given 𝓒, on the event of a successful calibration; the source text writes them P_𝓒, E_𝓒. All conclusions below are
  stated for P_c, for every successful c.
- **Final E2 flag** (method §6.9, recomputed after the final run as a flag only): E2_final is raised iff the standard
  deviation of the four numbers log Ẑ_1, …, log Ẑ_4 exceeds 1 nat. The method does not fix the divisor; both the
  population SD (divisor 4) and the sample SD (divisor 3) are covered below.

## 2. Assumptions

- **EX-A** (declared idealisation): exact scores, sums, products, probabilities and comparisons.
- **EX-S** (declared idealisation): independent ideal uniform random streams with the method's stream separation; the
  algorithm's outputs are measurable functions of the streams.
- **CAL** (method construction): 𝓒 uses streams 0–9 only; streams 10–13 are fresh (independent of 𝓒); escalation is
  decided before any final randomness.
- **(H-T12)** [taken from the sibling conjecture T12 (iii), used here only as a hypothesis]: for every successful
  calibration value c, E_c[Ẑ] = Z. (T12 (i) states E_c[Ẑ_r] = Z for each island, which implies this.)

## 3. Conclusions to prove

Fix any successful calibration value c. Under EX-A, EX-S, CAL and (H-T12):

**(a) Coverage.** For every α ∈ (0, 1): P_c(Z ≥ αẐ) ≥ 1 − α. In particular P_c(Z ≥ 0.05·Ẑ) ≥ 0.95.

**(b) Log bias.** log Ẑ is a well-defined, integrable random variable under P_c, and E_c[log Ẑ] ≤ log Z.

The remaining two conclusions make precise "it is not a relative-error interval" and "conditioning afterwards on final
flags does not preserve this coverage automatically". They are **non-implication statements**: they show that the
properties of Ẑ that yield (a) and (b) do not yield more. Let 𝓛(Z) be the set of joint laws of a vector
(Ẑ_1, …, Ẑ_4) such that the Ẑ_r are independent and identically distributed, each takes finitely many values, all in
(0, ∞), and E[Ẑ_r] = Z; set Ẑ = ¼ Σ_r Ẑ_r and define E2_final from (Ẑ_r) as above. Every law in 𝓛(Z) satisfies (a) and (b)
(by the same proof) and has every property of Ẑ that the proof of (a)–(b) uses (positive, finitely many values,
mean Z). The extra requirements in 𝓛(Z) (i.i.d. islands with islandwise mean Z) are not hypotheses about the actual final
run; they only make the non-implications stronger. These clauses do not assert that any particular data set realises
the laws exhibited, nor that they are not realised. This non-implication reading is the intended one; the per-data-set
reading about the actual estimator would be false: for fixed data the estimator satisfies e^{−Δ}Z ≤ Ẑ ≤ e^{Δ}Z surely,
with Δ = max_Ω d − min_Ω d, a data-dependent constant that is not among the reported quantities listed above and that no
property of 𝓛(Z) supplies (proof, Remark at the end).

**(c) One-sided, not a relative-error interval.** For every c₀ > 0 and every η ∈ (0, 1) there is a law in 𝓛(Z) with
P(Ẑ < c₀Z) ≥ 1 − η. Consequently, for no constants 0 < c₁ ≤ 1 ≤ c₂ < ∞ and γ > 0 does the bound
P(c₁Z ≤ Ẑ ≤ c₂Z) ≥ γ follow from the properties defining 𝓛(Z) (in particular not from those used in (a)–(b)), even though
(a) holds for every such law; the event {Z ≥ αẐ} places no upper limit on Z/Ẑ.

**(d) Conditioning on a final flag.** For every α ∈ (0, 1):
- (d1) there is a law in 𝓛(Z) with P(E2_final raised) > 0 and P(Z ≥ αẐ | E2_final raised) = 0;
- (d2) for every γ > 0 there is a law in 𝓛(Z) with P(E2_final not raised) > 0 and
  P(Z ≥ αẐ | E2_final not raised) < γ.

Both hold for either SD divisor. The source's "final flags" is read existentially: one final flag (E2_final) whose
conditioning breaks the coverage suffices to show that conditioning on final flags does not preserve it automatically
(a flag independent of Ẑ would preserve it). Consequently, coverage at level 1 − α conditional on either value of the final E2 flag
does not follow from the properties defining 𝓛(Z), although (a) holds unconditionally for every such law.

## Approved changes to the statement

None to hypotheses or conclusions. Exposition only (after Stage B review round 1, Opus reviewer findings 1, 2, 5): the
paragraph before (c) and the sentence after (d2) were reworded to state why the non-implication reading is the intended
one, that the extra requirements of 𝓛(Z) are not hypotheses about the actual run, and that "final flags" is read
existentially. Round 2 (both Stage B reviewers): "the only true one" replaced by "the intended one; the per-data-set
reading would be false"; "the method does not report" replaced by "not among the reported quantities listed above";
the P_c ↔ conditional-law sentence now carries the joint-measurability proviso. Versions reviewed: review/
STATEMENT_as_reviewed_r1.md (round 1), review/STATEMENT_as_reviewed_r2.md (round 2).
