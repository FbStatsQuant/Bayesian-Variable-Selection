# W3-PSHARP — PLAN (v1.0, 2026-11-11)

Target: three sharpness records for the posterior theorem (BRIEF.md; TRIAGE §2 T3). All proofs start from the
definition of π ([W3P] §0); no consumed claim enters a proof (the parents are only what is sharpened).

## Proof routes
- **Lemma S** (`lemmas/S_one_step.md`): Schur complement of H_{S∪{j}} and of G_{S∪{j}} + I on the new column →
  D ratio = s_{S,j}/(n − gᵀ(G+I)⁻¹g) ≤ n (eigenvalue-wise: (n+1)²/((n+1)λ+1) ≥ n/(λ+1)); block inverse →
  Q_S − Q_{S∪{j}} = n(x_jᵀρ̃_S)²/s_{S,j}; (1 − x)^{−ν} ≥ e^{νx}; sum over disjoint one-step supersets.
- **Claim A** (`lemmas/A_log_factor.md`): Lemma S(4) + lower bound νγ_j ≥ κ_n ζ_j/2 with ζ_j iid and κ_n ≥ 1 − c_n
  w.p. → 1, c_n log N_n → 0:
  - (W-orth): x_j ⟂ col X_{S₀} ⇒ s = n², x_jᵀρ̃ = x_jᵀε/s_y, ζ_j = (u_jᵀε/σ*)² iid χ²₁; κ_n = 2ν(n−1)σ*²/(nV),
    V = s_y²(2b₀ + Q_{S₀}) ≤ 2b₀s_y² + ‖Cε‖² + (‖μ‖² + ‖θ*‖²)/n (variational form of Q with ϑ = θ*).
  - (W-sph): ζ_j = (n−1)⟨ω_j, ρ̃/‖ρ̃‖⟩² iid (n−1)·Beta(½, (n−2)/2), independent of ε; κ′_n ≥ ‖ρ̃‖²/(2b₀ + Q_{S₀}),
    Q_{S₀} − ‖ρ̃‖² = yᵀP_H((n+1)⁻¹I + I − P_H)y = O_P(1 + s₀) under (C).
  - Truncated weak law (Lemma W): τ = 2 log N; E[e^{ζ/2}; ζ ≤ τ] = √(2τ/π) (χ²₁; exact), second moment
    ≤ √(2τ/π)e^{τ/2}; Chebyshev. Sphere law: density ratio to N(0,1) on t² ≤ τ within e^{±O(τ²/n)} (Wendel).
    (Re-derived, per the brief: tail P(e^{χ²₁/2} > w) ~ 1/(w√(π log w)); truncated mean at w = p exactly 2√(log p/π);
    truncated second moment ~ p/√(π log p) — the proof uses the cruder 2p√(log p/π), which suffices.)
- **Claim B** (`lemmas/B_sparsity.md`): ratio identity; Q_{S₀∪J} ≤ Q_{S₀} and D ratio ≤ n^{|J|} (Lemma S(1),(2)
  iterated); count C(p − s₀, j) supersets per size; prior ratio in closed form.
- **Claim C** (`lemmas/C_counterexample.md`): (1) algebra; (2) q_j ≤ 2^{−j}·(2/3)... ⇒ R^T_m ≤ 4p²2^{−m};
  (3) for |S| ≤ ⌊k/2⌋: ≥ k/2 columns of T′ missing; projection onto their span gives
  min_ϑ{‖μ − X_Sϑ‖² + ‖ϑ‖²/n} ≥ b²(n−1)d/(2k); s_y²Q_S ≥ ‖Cε‖² − 2‖P_𝒳ε‖² + ½(that); s_y²Q_{T′} ≤ ‖Cε‖² + b²;
  prior × Occam × count ≤ e^{O(log² n)} against fit ≤ e^{−c n b²}.

## Numerics (local only; `py -3.13 -I`)
- `numerics/a_orth.py`: orthogonal design; **exact** δ_n for large p by the Gamma-integral + elementary-symmetric
  DP (validated against brute-force enumeration at p ≤ 12); report δ_n/Λ_n, one-step sum/Λ_n, δ_n√n.
- `numerics/a_sph.py`: iid Gaussian design, p ≫ n; exact one-step sum Σ_j π(S₀∪{j})/π(S₀) (a rigorous lower bound
  for δ/(1−δ)) against Λ_n; brute-force check of Lemma S formulas.
- `numerics/b_check.py`: falsification search for Corollary B (random/adversarial small designs, exact enumeration),
  table of 𝒪^{lb}_n.
- `numerics/c_counter.py`: design 𝔇_n, exact enumeration (structure: orthogonal block + one coupled column; 2^k
  subset sums), exact cutoffs; control arm with a bounded-coefficient signal.

## Pipeline
CP1: STATEMENT v1.0 → statement lock L01 (gpt-6.1-sol high, codex, blind) ∥ numerics → ASSUMPTION_MAP → break review
K01 (gpt-6-astra high, codex, blind; also asked for a strictly stronger record) → dispositions → STATEMENT locked →
CHECKPOINT_1, commit.
CP2: lemma files → line checks (gpt-6.1-sol high, one per file group) → fixes → freeze MANIFEST_R1 → council R1
(seat sol: gpt-6.1-sol high codex; seat opus: Claude Opus 5.5 high claudeAgent; blind) → if needed one fix round +
reconciliation → REPORT.md with registry blocks → CHECKPOINT_2, commit. Stop at CP2.
Stop rule: STUCK, or a review not clean after one fix round → early checkpoint.
