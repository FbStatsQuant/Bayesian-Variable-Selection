# MEET-THM → HQ · Definitions for AMENDMENT_HQ_02 (reporting and growth-rate amendment to METHOD_v3.1_FINAL)

Chair, 2026-11-04. HQ asked for these at close (ruling Q4, `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`).

The full theorem card is S-REP in `THEOREM_LIST_FINAL.md`, copied verbatim from `R3_C.md` §S2 "S-REP". Decisions are in `MINUTES.md` §2.2–§2.3.

Nothing below changes the method's law, its random numbers, its calibration, its schedule or its decision.

## A. Reporting fields (POST HOC; HQ Q4 conditions)

The conditions, all met by every field below:
- inputs are only quantities the run already computes;
- no random numbers are read;
- nothing feeds back into the run.

### A1. Ĵ: the Jeffreys-divergence estimate (decided: the B/C/D form, unanimous in Round 3)

**Inputs, from the final islands r = 1…R′:**
- **Initial records.** A_r = N⁻¹ Σ_{i=1}^{N} d(S^{(0)}_{ri}), over each final island's initial iid start particles. These are not reweighted.
- **Endpoint records.** B_r = (4N)⁻¹ Σ_{k=1}^{4} Σ_{i=1}^{N} d(S^{(k)}_{ri}), at the four prescribed measured endpoints. These are plain discrepancy means, not RB records.
- **The potential d.** d(S) = log BF(S) − Σ_b log r_b(S_b) is the bridge potential the run already evaluates. It is fixed from (X, y, blocks, tables) before final randomness.

**Estimator:**

  Ĵ = Σ_r Ẑ_r·B_r / Σ_r Ẑ_r − (1/R′)·Σ_r A_r,

reported in nats, with its signed value preserved.

**Target and statement:**
- J = KL(π‖π₀) + KL(π₀‖π) = E_π d − E_{π₀} d.
- For ε > 0: P(|Ĵ − J| > ε | 𝒞) ≤ min{1, 4(M₂ − 1)/R′ + 16D²M₂/(R′ε²) + D²/(R′Nε²)}, where D = max_Ω d − min_Ω d.
- The bound can equal 1 at the default R′ = 4. There is no default-budget accuracy claim.

**Label:** "Post hoc Monte Carlo estimate of Jeffreys divergence; not a certificate; floating-point error unvalidated." The exact branch may report NA.

**Implementation:**
- A read-only accumulator of d at initialisation and at the four measured endpoints. Per-particle d values exist during execution but are not retained today.
- No new draws, transitions or scores.
- Historical fits report NA. Absent records are not reconstructed.

**Declared list:** d becomes a default member of the declared summary list 𝓗 (METHOD §6.11b). It is fixed before stream 10 and reads no uniforms (Seats A and B: R3_A §S5, R3_B §S5). Because 𝓗 is defined as [0,1]-valued, **raw d is recorded**, and theorems (M1) apply to the globally range-scaled (d − min_Ω d)/D, with D = max_Ω d − min_Ω d > 0. If D = 0, then Ĵ = J = 0 (S-REP card).

### A2. ε̂_×: the cross-block correlation proxy, with companions

- **ε̂_×** = max over b ≠ c, j ∈ C_b, k ∈ C_c of |X_jᵀX_k|/(n − 1), on the standardised columns and the built blocks. The empty maximum is 0.
  - Field: `cross_block_rmax`.
  - Label: "Descriptive maximum cross-block correlation proxy; not signal leakage or a confidence bound; floating-point error unvalidated."
- **Companions:**
  - κ̂ = min_b λ_min(G_{C_b}/(n − 1));
  - if κ̂ > 0, δ̂ = (K − 1)·ε̂_×/κ̂;
  - ū̂ = Σ_b max_{U⊆C_b} x_b(U), from the block tables. This is a global envelope, **not** a maximum over V (MINUTES §2.2, C's objection adopted).
- **Domain:** κ̂ > 0, δ̂ < 1, ū̂ < 1 and δ̂·ū̂ < (1 − δ̂)(1 − ū̂). Outside it, η̂ is printed **"n/a"**.
- **Derived envelope:**
  - r̂ = δ̂ū̂/[(1 − δ̂)(1 − ū̂)];
  - η̂ = K·log(1/(1 − δ̂)) + ν·log(1/(1 − r̂)).
  - On the domain: sup_{S∈Ω} |d(S) − d_σ(S)| ≤ η̂.
  - For nonempty S: ε_S ≤ (|S| − 1)·ε̂_×/κ̂.
- **Not claimed:** no lower bound of order n·ε̂_×·|β_jβ_k| (refuted in check wave 2), and no global rescaling from V.

## B. Growth-rate edit (ground rule 5: growth rates as explicit functions of (n, p) only)

**Two optional stacking configurations** for the number of final islands R′. They are used on families where D_* = O_P(1), with D_* as defined in M2(a):
- **(i)** R′_n = 4⌈log₂(n + p + 1)⌉, for consistency of any fixed finite set of declared summaries;
- **(ii)** R′_n = 4⌈(n + p)⁶/4⌉, for simultaneous control of ≤ (n + p)² declared summaries.

**Unchanged:**
- The shipped default R′ = 4 is unchanged. It carries only the fixed-R′ statements.
- ℓ = ⌈log₂(n + p + 1)⌉, L = max{4, ⌈log₂(n + 1)⌉} and N need no edit.

**Basis:**
- `SYNTH_R2.md` §2.6, confirmed by all four seats in Round 3.
- Check wave 2 found both rates TRUE-AS-WRITTEN on the exhibited family: W2_PC1 item 6; W2_PC2 §6.
