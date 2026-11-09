# Theorem C — the concentrated bridge (v2, T-free evidence bound)

Status: PROVED (by this seat, unchecked). v2, 2026-11-09 (v1 → v2: sharpness-gate amendment BT1 §1, §4: the evidence bound
no longer depends on T; uniform RB error in expectation; bias and log-evidence corollaries; `reviews/BT1_disposition.md`).
Statement: STATEMENT.md v3 §2 "Theorem C". Uses Lemma MR (MR-a, MR-b, MR-c), Lemma ST, `LT_theorem.md` Steps 1, 2′, 4,
Lemma PC.

Fixed data; island r; given 𝓒 on 𝒜 in localised form (all expectations below are E[· | 𝓒] at the frozen c, transferred
by MR's freezing step); any frozen parameters (T ≥ 1, N_e ≥ 1, L ≥ 0). s := S₀. Notation: X^{(t)} population after the
stage-t round (t = 0: initial draws), A_t := A^{br}_{r,t}, x_t := 1 − A_t, U := Σ_{t=0}^{T}x_t, q̂_t empirical measure of
X^{(t)}, W := W_r, q_t := q_{φ_t}.

## Step 1 (Hölder: the bridge odds never exceed δ̄) — used in C-ii

ω(φ) := q_φ(Ω∖s)/q_φ(s) = Σ_{S≠s}(γ₀(S)/γ₀(s))^{1−φ}(γ₁(S)/γ₁(s))^{φ} ≤ o₀^{1−φ}o₁^{φ} ≤ δ̄ (Hölder, exponents 1/(1−φ),
1/φ; φ ∈ {0,1} by definition). Hence 1 − q_t(s) = ω/(1 + ω) ≤ δ̄/(1 + δ̄) and q_t(s) ≥ 1/(1 + δ̄).

## Step 2 (C-i, deterministic product bound)

For s ≥ 1 the stage factor is q̂_{s−1}(e^{Δ_s d}) ≥ A_{s−1}e^{Δ_s d(s)}; multiplying, Ẑ_{r,t} ≥ Z₀e^{φ_t d(s)}Π_{u<t}A_u, and
Z₀e^{φ_t d(s)}/Z_t = q_t(s)/π₀(s). So W_t := Ẑ_{r,t}/Z_t ≥ (q_t(s)/π₀(s))Π_{u<t}A_u ≥ q_t(s)(1 − Σ_{u<t}x_u)⁺, and at t = T,
W ≥ (π(s)/π₀(s))Π_{t<T}A_t. ∎(C-i)

## Step 3 (C-ii, bridge occupation; T-dependent, kept as a separate statistic)

Fix u ∈ (0,1), V_{t−1} := Σ_{v<t}x_v, Y := Σ_{t=0}^{T}x_t1{V_{t−1} ≤ u}. Pointwise min(U, u) ≤ Y (if U ≤ u, Y = U; else with
τ := min{t : V_t > u}, Y ≥ V_τ > u). On {V_{t−1} ≤ u}, Step 2 and Step 1 give W_t ≥ (1 − u)/(1 + δ̄), so
x_t1{V_{t−1} ≤ u} ≤ ((1 + δ̄)/(1 − u))W_t x_t pointwise; MR-a with h = 1{S ≠ s} gives E[W_t x_t] = 1 − q_t(s) ≤ δ̄/(1 + δ̄).
Hence E[Y] ≤ (T + 1)δ̄/(1 − u); with u = ½ and min(U,1) ≤ 2min(U,½): E[min(U, 1)] ≤ 4(T + 1)δ̄. (Only deterministic-index
stagewise identities and a pointwise inequality; no optional stopping.) ∎(C-ii)

## Step 4 (C-iii, T-free evidence bound; BT1 §1, re-derived)

Put a(S) := d(S) − d(s) and V_t := Ẑ_{r,t}/(Z₀e^{φ_t d(s)}) (V_0 = 1). Since Ẑ_{r,t} = Ẑ_{r,t−1}q̂_{t−1}(e^{Δ_t d})
(`cpp/v3_engine.h:317-322`; W1-N1 Lemma B (B-a)),
  V_t = V_{t−1}·q̂_{t−1}(e^{Δ_t a}).                                                               (1)
*Rescaled MR-a.* MR-a at stage t − 1 with a bounded data-and-c-measurable f: E[Ẑ_{r,t−1}q̂_{t−1}(f)] = Z_{t−1}q_{t−1}(f) =
m(∅)Σ_Sγ₀(S)e^{φ_{t−1}d(S)}f(S); dividing by the constant Z₀e^{φ_{t−1}d(s)} = m(∅)Z̄₀e^{φ_{t−1}d(s)}:
  E[V_{t−1}q̂_{t−1}(f)] = Σ_S π₀(S)e^{φ_{t−1}a(S)}f(S).                                              (2)
*Loss per stage.* With f_t(S) := (1 − e^{Δ_t a(S)})⁺ ∈ [0, 1] (bounded, admissible for MR), (1) gives
(V_{t−1} − V_t)⁺ = V_{t−1}(1 − q̂_{t−1}(e^{Δ_t a}))⁺ ≤ V_{t−1}q̂_{t−1}(f_t) (since (1 − mean)⁺ ≤ mean of (1 − ·)⁺). By (2),
E(V_{t−1} − V_t)⁺ ≤ Σ_Sπ₀(S)e^{φ_{t−1}a(S)}(1 − e^{Δ_t a(S)})⁺ = Σ_{S: a(S)<0}π₀(S)(e^{φ_{t−1}a(S)} − e^{φ_t a(S)}).
Summing over t = 1..T telescopes (φ₀ = 0, φ_T = 1):
  E Σ_t(V_{t−1} − V_t)⁺ ≤ Σ_{S}π₀(S)(1 − e^{a(S)})⁺ =: b₋.                                          (3)
*Mean and deficit.* V_T = 1 − Σ_t(V_{t−1} − V_t) ≥ 1 − Σ_t(V_{t−1} − V_t)⁺, so E(1 − V_T)⁺ ≤ b₋. Let
c := Σ_Sπ₀(S)e^{a(S)} = (Z̄₁/Z̄₀)e^{−d(s)} = π₀(s)/π(s) (because π(s)/π₀(s) = e^{d(s)}Z̄₀/Z̄₁). Then W = V_T/c
(Z = m(∅)Z̄₁) and E V_T = c (E W = 1, MR-a at t = T with h ≡ 1). With b₊ := Σ_Sπ₀(S)(e^{a(S)} − 1)⁺, c − 1 = b₊ − b₋.
Hence, using (c − V_T)⁺ ≤ (1 − V_T)⁺ + (c − 1)⁺,
  E|W − 1| = 2E(1 − W)⁺ = (2/c)E(c − V_T)⁺ ≤ (2/c)(b₋ + (c − 1)⁺) = 2max(b₋, b₊)/c =: β.             (4)
*Bounds on β.* The S = s terms of b₋, b₊ vanish (a(s) = 0). So b₋ ≤ Σ_{S≠s}π₀(S) = δ₀ and
b₊ ≤ Σ_{S≠s}π₀(S)e^{a(S)} = c − π₀(s) = c(1 − π(s)) = cδ. With δ₀/c = δ₀π(s)/π₀(s) = (1 − δ)o₀:
  E|W_r − 1| ≤ β ≤ 2max{δ, (1 − δ)o₀} ≤ 2δ̄.                                                         (5)
Valid for every frozen grid (any T) and every N_e ≥ 1. *Pooled:* Ẑ/Z = ¼Σ_rW_r (CC3), so E|Ẑ/Z − 1| ≤ ¼Σ_rβ_r = β
(β depends on the data only). *Log tail:* for u > 0, {|log(Ẑ/Z)| > u} ⊆ {|Ẑ/Z − 1| > 1 − e^{−u}}, so
P(|log Ẑ − log Z| > u | 𝓒) ≤ min{1, β/(1 − e^{−u})}; the same islandwise. ∎(C-iii)

## Step 5 (C-iv, coded PIPs, MPM, discovery, bias)

Let E_r := ‖p̂_r − 1_s‖_∞ and g := min{1, κ₀ + δ + (1 − δ)λ₀} (≤ 21o₁ by ST: κ₀ ≤ o₁, δ ≤ o₁, λ₀ ≤ 19o₁).
`LT_theorem.md` Step 2′ gives E[W E_r] ≤ g. Since E_r ∈ [0, 1] and E(1 − W) = 0,
  E E_r = E[W E_r] + E[(1 − W)E_r] ≤ g + E(1 − W)⁺ ≤ g + β/2 ≤ 21o₁ + δ̄ ≤ 22δ̄.
*Pooled and MPM.* ‖pip_primary − 1_s‖_∞ ≤ ¼Σ_rE_r, so E‖pip_primary − 1_s‖_∞ ≤ g + β/2; MPM ≠ s forces this ≥ ½
(`LT_theorem.md` Step 4), so P(MPM ≠ S₀ | 𝓒) ≤ 2(g + β/2) ≤ 44δ̄. No union over islands, no independence.
*Discovery.* The N_e initial draws are evaluated (CC1): P(S₀ ∉ 𝓜_r | 𝓒) ≤ (1 − π₀(s))^{N_e} ≤ δ₀ ≤ δ̄.
*Bias against the exact PIPs.* MR-c gives E[W p̂_r(j)] = PIP_j; so |E p̂_r(j) − PIP_j| = |E[(1 − W)p̂_r(j)]| ≤ E(1 − W)⁺ ≤ β/2
(p̂_r(j) ∈ [0, 1] and E(1 − W) = 0), uniformly in j, and the same for pip_primary. ∎(C-iv)

## Step 6 (C-v, asymptotic, joint law)

Assume 1_𝒜δ̄ → 0 in probability, i.e. 1_𝒜o₁ → 0 and 1_𝒜o₀ → 0 (localised concentration and P-START); P-CONC (global)
plus P-START is sufficient, and only the localised form is used (LC2 issue 5). Integrating the conditional
bounds truncated at 1 (bounded convergence): P(𝒜 ∩ {|Ẑ/Z − 1| > ε}) ≤ E[1_𝒜 min(1, 2δ̄/ε)] → 0; the log tail likewise;
P(𝒜 ∩ {‖pip_primary − 1_s‖_∞ > ε}) ≤ E[1_𝒜 min(1, 22δ̄/ε)] → 0; P(𝒜 ∩ {MPM ≠ S₀}) ≤ E[1_𝒜 min(1, 44δ̄)] → 0; NC_r:
P(𝒜 ∩ {W_r < ½}) ≤ E[1_𝒜 min(1, 4δ̄)] → 0; HPM: by PC and `D_theorem.md` §3, P(completed ∩ {Ŝ ≠ S₀}) ≤
P(𝒜 ∩ {δ ≥ ½}) + E[1_𝒜 min(1, δ̄)] → 0. *Rates:* (W3-POST Theorem 1 (Rate), `Theory_work/Wave3/W3-POST/STATEMENT.md:79-80`, gives δ = O_P(r_n), hence
o₁ = δ/(1 − δ) = O_P(r_n).) If 1_𝒜δ̄ = O_P(r_n) with deterministic r_n ↓ 0, the same bounds give,
localised to 𝒜, Ẑ/Z − 1 = O_P(r_n), log Ẑ − log Z = O_P(r_n) and ‖pip_primary − 1_s‖_∞ = O_P(r_n) (probability rates, not
L¹ rates under the joint law). Reported fields: Lemma PC. ∎

## Remarks

- Honest label: the regime in which the start already concentrates (π₀(S₀) → 1); the bridge has no mass to transport.
  No rate for the start mass and no relation to the schedule length are needed (the locked v2 needed T·δ̄ → 0; the source
  BLIND_fable Thm 4(b) needed T²δ̄ → 0). Valid for N_e = 1.
- Linear dependence on δ̄ is natural for N_e = 1, T = 1: one non-truth initial draw already gives an O(1) evidence error
  with probability ≈ δ₀.
- The occupation sum U of C-ii genuinely grows with T (numerics: E min(U,1) → 1 at large T while W → 1); only the evidence
  bound is T-free.

## Numerical falsification

`numerics/RESULTS_v3.txt` (run_checks_v3.py, seed 31): five targets (three artificial incl. cap K = 2; two
regression-realisable with the T12 §0 score/prior and block start) × (T, N) ∈ {(1,1), (4,2), (32,2), (128,1)}: the
telescoping budget E Σ(V_{t−1} − V_t)⁺ ≤ b₋ (nearly attained, e.g. 0.0647 vs 0.0648), E|W − 1| ≤ β, β ≤ 2max(δ, (1−δ)o₀),
E E_r ≤ g + β/2 and max_j bias ≤ β/2 hold in all 20 cells; E|W − 1| decreases in T at fixed target (T-free bound
consistent). C-i and the stopped-sum (C-ii) were tested pointwise in `RESULTS_v2.txt` (all islands). 0 violations.
