# Theorem TR — terminal repair under global overlap (alternative to NC_r)

Status: PROVED (by this seat, unchecked). v1, 2026-11-09. Source: BT1 §2 (`reviews/BT1_better_theorem_astra.md`),
re-derived by the lead. Statement: STATEMENT.md v3 §2 "Theorem TR". Uses KERNEL, Lemma ST, T12 (R3), Lemma PC, CC1–CC3.

## Setting

Fixed data. w(S) := π(S)/π₀(S); **M := max_{S∈Ω} w(S)** (≥ 1, since Σπ = Σπ₀ = 1); e_0 := 1 and e_L := (1 − 1/M)^L for L ≥ 1 (LC2 issue 4). S₀ ∈ Ω, δ, o₁,
κ₀, λ₀ as in STATEMENT §0/ST; g := min{1, κ₀ + δ + (1 − δ)λ₀} ≤ min{1, 21·o₁}. Given 𝓒 on 𝒜, island r, any frozen
parameters and **any** bridge outcome.

## Statement

- (TR-a) For every order σ, the round kernel K_σ := K_{σ(1)}⋯K_{σ(m)} at φ = 1 satisfies K_σ(x, ·) ≥ M⁻¹π(·) for every x;
  hence so does the round kernel K₁ (average over σ), and sup_x ‖K₁^L(x, ·) − π‖_TV ≤ e_L.
- (TR-b) E[‖p̂_r − 1_{S₀}‖_∞ | 𝓒] ≤ g + e_L and E[1 − A_{r,q} | 𝓒] ≤ δ + e_{L+q} ≤ δ + e_L (q = 0..4).
- (TR-c) E[‖pip_primary − 1_{S₀}‖_∞ | 𝓒] ≤ g + e_L; P(MPM ≠ S₀ | 𝓒) ≤ 2(g + e_L); P(S₀ ∉ 𝓜_r | 𝓒) ≤ δ + e_L.
- (TR-d, asymptotic) Under P-CONC and **P-OVL∞: P(𝒜 ∩ {L/M ≤ c}) → 0 for every c > 0** (Q := L/M on 𝒜, ∞ off 𝒜,
  Q → ∞ in probability; MP1 issue 1): for every ε > 0,
  P(𝒜 ∩ {‖pip_primary − 1_{S₀}‖_∞ > ε}) → 0, P(𝒜 ∩ {MPM ≠ S₀}) → 0, P(completed ∩ {Ŝ ≠ S₀}) → 0 — with no condition on
  Ẑ (NC_r not assumed), the bridge, N_e, or the grid. Production corollary: L = max(4, ⌈log₂(n+1)⌉), so P-OVL∞ means, localised to 𝒜,
  M = o_P(log n) on 𝒜.

## Proof

(TR-a) *Independence kernel.* At φ = 1 the I step proposes y ~ π₀ and accepts with probability min{1, w(y)/w(x)}. For
y ≠ x: K_I(x, y) = π₀(y)min{1, w(y)/w(x)} = min{π₀(y), π(y)/w(x)} ≥ min{π(y)/M, π(y)/M} = π(y)/M, using π₀(y) = π(y)/w(y)
≥ π(y)/M and w(x) ≤ M. For y = x: K_I(x, x) ≥ π₀(x) (the proposal x is accepted with probability 1) ≥ π(x)/M. So
K_I(x, ·) ≥ M⁻¹π. *Round.* Fix σ and let k be the position of I; write K_σ = K_pre K_I K_post. Every elementary kernel is
π-invariant at φ = 1 (KERNEL), so πK_post = π and K_σ(x, ·) = Σ_z K_pre(x, z)Σ_y K_I(z, y)K_post(y, ·) ≥
Σ_z K_pre(x, z)·M⁻¹(πK_post)(·) = M⁻¹π(·). Averaging over the order law preserves the bound. *Doeblin.* Write
K₁ = M⁻¹π + (1 − M⁻¹)Q with Q a Markov kernel (Q := (K₁ − M⁻¹π)/(1 − M⁻¹) if M > 1; if M = 1 then π = π₀ and K₁ = π
already). Since πK₁ = π, for any law μ: μK₁ − π = (1 − M⁻¹)(μQ − πQ), and ‖μQ − πQ‖_TV ≤ ‖μ − π‖_TV. Induction gives
‖μK₁^L − π‖_TV ≤ (1 − 1/M)^L‖μ − π‖_TV ≤ e_L.

(TR-b) Fix c. Let 𝓗 be everything up to the end of the bridge (stage-T round) and 𝓗′ everything before measured round 1.
For a particle, let φ_i := ¼Σ_{q=1}^{4}1{(q, i) bad} with "bad" as in `LT_theorem.md` Step 1 (enters round q away from S₀,
or enters at S₀ and leaves during it). By (1) of `LT_theorem.md`, ‖p̂_r − 1_{S₀}‖_∞ ≤ min{1, κ₀ + (1/N_e)Σ_iφ_i}.
*Per-particle chain.* By T12 (R3) (W1-N1 Lemma B (B-b)), given 𝓗′ each particle's subsequent rounds form a Markov chain
with kernel K₁ started at its entering state (orders fresh and independent of the past); hence E[φ_i | 𝓗′] = ψ(X_i′), with
X_i′ particle i's state entering measured round 1 and ψ(x) := E_x[¼Σ_q 1{round q bad}] ∈ [0, 1].
*Stationary value.* Under X′ ~ π the entering state of every measured round is π-distributed (πK₁ = π); round q is bad
with probability ≤ π(Ω∖S₀) + π(S₀)λ₀ = δ + (1 − δ)λ₀ (ST-c applies to a particle entering at S₀, whatever happened
before). So π(ψ) ≤ δ + (1 − δ)λ₀.
*Burn-in.* Given 𝓗, X_i′ ~ K₁^L(X_i^{(T)}, ·) (L rounds at φ = 1, R3), so E[ψ(X_i′) | 𝓗] = (K₁^Lψ)(X_i^{(T)}) ≤ π(ψ) + e_L by
(TR-a), since ψ ∈ [0, 1]. Hence E[(1/N_e)Σ_iφ_i] ≤ δ + (1 − δ)λ₀ + e_L, and by concavity of min{1, ·},
E‖p̂_r − 1_{S₀}‖_∞ ≤ min{1, κ₀ + δ + (1 − δ)λ₀ + e_L} ≤ g + e_L. The same argument with ψ(x) := K₁^q(x, Ω∖S₀) gives
E[1 − A_{r,q}] ≤ δ + e_{L+q}. These are bounded measurable functionals of the record, so the freezing lemma transfers them to
"given 𝓒" in localised form (as in `MR_identities.md` Step 4). No weighting by W and no independence across particles are
used.

(TR-c) ‖pip_primary − 1_{S₀}‖_∞ ≤ ¼Σ_r‖p̂_r − 1_{S₀}‖_∞; MPM ≠ S₀ forces this ≥ ½ (`LT_theorem.md` Step 4), so Markov gives
2(g + e_L). Every particle state was evaluated (CC1–CC2), so {S₀ ∉ 𝓜_r} ⊆ {A_{r,0} = 0} and P ≤ E[1 − A_{r,0}] ≤ δ + e_L.

(TR-d) e_L ≤ e^{−L/M}, so 1_𝒜e_L ≤ e^{−Q} → 0 in probability (Q as in P-OVL∞), and 1_𝒜g ≤ 21·1_𝒜o₁ → 0; integrate the truncated conditional bounds
(bounded convergence). HPM via Lemma PC and `D_theorem.md` §3: P(completed ∩ {Ŝ ≠ S₀}) ≤ P(S† ≠ S₀) +
E[1_𝒜 min(1, δ + e_L)] → 0, where S† := the hpm_better-maximiser of F over Ω and P(S† ≠ S₀) ≤ P(δ ≥ ½) → 0. ∎

## Remarks (honest label)

- P-OVL∞ involves no final-particle statistic; it is a condition on (π, π₀) relative to the executed burn-in L (on (π, π₀)
  alone once L is the production budget; MP1 issue 2). It is a **global overlap** condition: M is a
  maximum over all of Ω, not computed by the method. Since M ≥ w(S₀) = π(S₀)/π₀(S₀), P-OVL∞ forces π₀(S₀) ≥ π(S₀)/M, i.e. π₀(S₀)·L → ∞ (π(S₀) → 1).
- Start mass alone does not control M (BT1 §2): with π(s) = π₀(s) = 1 − ε, a second state of posterior mass ε/2 and start
  mass εe^{−H}, M ≥ e^{H}/2 for any H. So TR and C are not nested: C needs π₀(S₀) → 1, TR needs M = o(L).
- TR does not repair W: the evidence is not updated in the terminal rounds. In the "near" example
  (`numerics/RESULTS_v1_sec4b.txt`) the PIPs are repaired while W stays collapsed.
- Improves BLIND_astra2 Thm 5 in the concentrating regime: no log(p+1)/N_e → 0 condition and no union over coordinates.

## Numerical falsification

`numerics/RESULTS_v3.txt` (run_checks_v3.py): exact minorization check min_{x,y} K_σ(x, y)/π(y) ≥ 1/M for random fixed orders σ on the test targets and
E‖p̂_r − 1‖_∞ ≤ g + e_L by simulation, including collapsed-W runs.
