# O-STAGES — REPORT: how many bridge stages the v3 grid produces

Run of 2026-11-02, branch `theory/O-STAGES` (Opus 5.5, laptop). All results are **candidates**: not reviewed, not adopted.
Scripts: `scripts/` (deterministic or fixed seeds). Raw outputs: `results/`. Notation: `00_COMMON.md`, F-DRAFT
`NEW_TARGETS.md` §0, T13.

## 1. Headline

1. **PROVED (structure).** For any finite candidate set V, the ESS step criterion is monotone in both endpoints. So the
   bisection finds the exact frontier, which settles W′'s open obligation (1) for every V. The greedy rule also produces
   the **shortest** valid grid: no grid whose every step has ESS ≥ 0.9 has fewer intervals. The v3 construction, which
   refines the pilot's points, is optimal among grids that refine those points, and max(T*_V, T_P) ≤ T_grid ≤ T*_V + T_P.
2. **PROVED (key identity).** For every state R, ρ(u, v) = q_u(R)·q_{2v−u}(R)/q_v(R)². The ESS of a stage is set by the
   mass of one state at the extrapolated temperature w = 2v − u, and this produces a **halving law**. In the favourable
   regime this gives a deterministic two-sided bound on T* through q_w(S₀), w ∈ [1, 2] (Theorem F). Given Theorem W's
   layer law, that bound becomes **W′ with |T* − ⌈log₂(1 + 1/g)⌉| ≤ 1** (PROVED conditional on the layer law, which is
   a PROOF SKETCH in F-DRAFT).
3. **COUNTEREXAMPLE to W″ as stated; corrected form PROVED (two-state) / PROOF SKETCH (families).** A masked crossing
   costs **log₂ A₀ + O(1)** stages, where A₀ = log[π₀(S°)/π₀(S₀)] is the start's masking depth. It does not depend on the
   posterior-side gap A₁. The 3π window count is only the O(1) part. Exact numerics give T* = log₂A₀ + 7.7 ± 0.4. That
   reproduces F-DRAFT's proxy-split counts 14 and 16, and gives 18 at n = 3200. The proxy masking (A₀ = Θ(n)) costs
   log₂n + O(1) stages. LH/T27 masking (A₀ = c log p + (c/2)log n) costs O(log log n) stages.
4. **Path length is the right quantity only for fine grids.** We PROVED √c·T*(c) → L = ∫₀¹ sd_{q_φ}(d)dφ as c → 0, with
   two-sided κ-regularity bounds. At the production c = log(10/9), the two-state family has L ≤ π while T* → ∞, so the
   length does not determine T_n.
5. **T26 and T38(c).** In the favourable regime, (T_n+1)Δ_n → 0 holds whenever Δ_n → 0 and the over-corrected law
   q_{1+g₀} still puts mass 0.9/(1−Δ_n) on S₀. On BO with p ≤ n^A, T* = O(1), so P1 needs nothing beyond Δ_n → 0. In the
   masked regime P1 fails anyway, because Δ_n → 1. The cost term N_nT_n(p+B+2) carries T_n = O(1) on favourable BO,
   log₂n + O(1) on proxy masking, O(log log n) on LH masking, and ≤ T_e = O(log²(n+p)) always.

## 2. Model of the grid rule (from `cpp/v3_calib.h`, METHODOLOGY_v3 §§6.6–6.7)

- F_V(t) := log Σ_{S∈V} γ₀(S)e^{t d(S)} for t ∈ [0, 2], with q^V_t ∝ γ₀e^{td} on V. Population version: V = Ω, F = log Z̄_t.
- Φ_V(u, v) := F_V(u) − 2F_V(v) + F_V(2v − u) = −log ρ_V(u, v) = log(1 + χ²(q_v‖q_u)) = D₂(q_v‖q_u), the Rényi-2
  divergence. A step is accepted iff Φ_V ≤ c := log(10/9) ≈ 0.10536, i.e. ρ ≥ 0.90.
- **Pilot (population, H → ∞):** from u, take v = 1 if it passes; otherwise bisect on (u, 1]. The floor 1/T_e is
  inactive in every case below. This is the greedy grid on Ω, and we write T*_Ω for its number of intervals.
- **Candidate grid:** the pilot points P are the targets. From u, take b = min{P ∩ (u, 1]}; append b if Φ_V(u, b) ≤ c,
  otherwise bisect on (u, b]. The construction fails beyond T_e intervals, so **T_n ≤ T_e on success** (deterministic).
- T26's T_n and T38's T_n are the final run's interval count, which is T_grid of the last accepted construction.

## 3. Statements and proofs

**Lemma 0 (reference-state identity). PROVED.** For every R ∈ V and u < v, writing w = 2v − u:
ρ_V(u, v) = q_u(R)·q_w(R)/q_v(R)². Equivalently, Φ_V(u, v) = ℓ_R(u) + ℓ_R(w) − 2ℓ_R(v), where ℓ_R(t) := −log q^V_t(R) ≥ 0.
*Proof.* γ_t(R) = γ₀(R)e^{td(R)} is log-affine in t, so γ_v(R)² = γ_u(R)γ_w(R). Then
q_u q_w/q_v² = [γ_uγ_w/γ_v²]·Z_v²/(Z_uZ_w) = Z_v²/(Z_uZ_w) = ρ. ∎
(Φ is invariant under adding an affine function of t to F, which is why "relative to R" costs nothing.)

**Lemma 1 (monotonicity). PROVED.** ∂_vΦ = 2[F′(2v−u) − F′(v)] ≥ 0 and ∂_uΦ = F′(u) − F′(2v−u) ≤ 0, because F is
convex (F″ = Var_{q_t}(d)). The inequalities are strict unless d is constant on V. Consequences:
(a) {v ∈ (u, 1] : ρ_V(u, v) ≥ 0.9} = (u, v*(u)], so 60 halvings return v*(u) up to (1−u)2^{−60};
(b) every sub-step [u′, v′] ⊆ [u, v] of a valid step is valid;
(c) v*(u) is nondecreasing in u.

**Theorem G (greedy optimality). PROVED** for the exact-frontier rule; the 2^{−60} bisection slack is ignored.
(i) Let T*_V(c) be the greedy count. Every grid 0 = u₀ < … < u_m = 1 whose steps all satisfy Φ_V ≤ c has m ≥ T*_V(c).
(ii) The target-constrained construction is the greedy rule for "valid and refines P". Its count T_grid is minimal over
such grids, and max(T*_V, T_P) ≤ T_grid ≤ T*_V + T_P, where T_P is the number of pilot intervals.
(iii) T*_V(c) is nonincreasing in c. If |Φ_V − Φ_Ω| ≤ η for all 0 ≤ u < v ≤ 1 (a uniform COVER condition, T13(ii)),
then T*_Ω(c + η) ≤ T*_V(c) ≤ T*_Ω(c − η).
*Proof.* (i) By induction g_k ≥ u_k: g_{k+1} = v*(g_k) ≥ v*(u_k) ≥ u_{k+1} by Lemma 1(c). (ii) The same induction with
u_{k+1} ≤ min(v*(u_k), nxt_P(u_k)) ≤ min(v*(g_k), nxt_P(g_k)) = g_{k+1}. Here nxt_P is nondecreasing, and a grid that
refines P cannot skip a point of P. For the upper bound, the union of the greedy V-grid and P is valid by
Lemma 1(b) and refines P. (iii) Monotonicity in c is immediate; a grid valid for Ω at level c − η is valid for V at
level c. ∎

**Theorem L (path length). PROVED.** Let L := ∫₀¹ √F″(t) dt = ∫₀¹ sd_{q_t}(d) dt, the thermodynamic (Fisher–Rao) length.
(i) For any valid step, Φ(u, v) = ∫₀^Δ∫₀^Δ F″(u+s+r) ds dr ∈ [Δ² inf_{[u,w]}F″, Δ² sup_{[u,w]}F″], with Δ = v − u.
(ii) Let κ_G be the largest ratio sup/inf of F″ over the windows [u, 2v−u] of the greedy grid. Then
T*(c) ≥ L/√(κ_G c). Let κ′ be the same ratio over the grid built with Δ(u) = sup{Δ : Δ² sup_{[u,u+2Δ]}F″ ≤ c}. Then
T*(c) ≤ L√(κ′/c) + 1.
(iii) If d is nonconstant on V, then √c·T*(c) → L as c ↓ 0.
(iv) Worst case: T* ≤ ⌈D/(2√c)⌉ = ⌈1.54·D⌉, where D := max_V d − min_V d.
*Proof.* (i) Expand the second difference. (ii) On a greedy step, (∫_u^v√F″)² ≤ Δ² sup_{[u,v]}F″ ≤ κ_G Δ² inf_{[u,w]}F″
≤ κ_G c. Summing over steps gives L ≤ T*√(κ_G c). For the upper bound, every full step of the explicit grid has
∫_u^v √F″ ≥ Δ√(sup/κ′) = √(c/κ′), and that grid is valid by (i), so Theorem G(i) applies. (iii) inf_{[0,2]}F″ > 0
gives Δ ≤ √(c/inf F″) → 0 uniformly. Uniform continuity of log F″ gives κ_G, κ′ → 1. (iv) Popoviciu gives
F″ ≤ D²/4, so steps of size 2√c/D are valid. ∎
*Why this is not the answer at the production c:* in the approach to a crossing, F″ grows like e^{Dt} across a window
of size Δ = Θ(1). Then κ_G = e^{Θ(D)} and (ii) is vacuous. See Theorem M.

**Halving count.** For w̄ > 1, let N(w̄) be the minimal number of intervals of a grid on [0, 1] whose every step
satisfies 2v − u ≤ w̄. Then **N(w̄) = max{1, ⌈log₂(w̄/(w̄ − 1))⌉}**, with N = 1 for w̄ ≥ 2, and N(w̄) = ∞ for w̄ ≤ 1.
*Proof.* The constraint v ≤ (u + w̄)/2 is monotone in u, so the greedy argument of Theorem G applies. The greedy
sequence u_k = w̄(1 − 2^{−k}) halves the gap to w̄. The final step to 1 is allowed iff u ≥ 2 − w̄, which happens iff
2^k ≥ w̄/(2(w̄ − 1)). ∎

**Theorem F (favourable regime: deterministic sandwich). PROVED.** Let Δ := 1 − inf_{t∈[0,1]} q_t(S₀). By T22(iv-b)
(T26 Lemma 1), Δ = max{1 − π₀(S₀), 1 − π(S₀)}. Assume (1 − Δ)² ≥ 0.9, i.e. Δ ≤ 0.0513. Define:
- w₋ := sup{w ∈ [1, 2] : q_s(S₀) ≥ 0.9/(1 − Δ) for all s ∈ [1, w]}, with w₋ := 1 if q₁(S₀) < 0.9/(1 − Δ);
- w₊ := sup{w ∈ [1, 2] : q_w(S₀) ≥ 0.9(1 − Δ)²}.

Then **N(w₊) ≤ T*_Ω ≤ N(w₋)**. The same holds for V in place of Ω, with q^V.
*Proof.* Apply Lemma 0 with R = S₀, and note u, v ∈ [0, 1]. Sufficiency: ρ ≥ q_u q_w ≥ (1 − Δ)q_w(S₀). This is ≥ 0.9
if w ≤ 1 (since (1−Δ)² ≥ 0.9) or if w ∈ [1, w₋]. So the halving grid toward w₋ is valid, and Theorem G gives the upper
bound. Necessity: ρ ≥ 0.9 implies q_w(S₀) ≥ 0.9 q_v²/q_u ≥ 0.9(1 − Δ)². So every valid step has 2v − u ≤ w₊, and the
halving count gives the lower bound. ∎
Note that q_w ∝ π·(π/π₀)^{w−1} is the "over-corrected" posterior, and
1/q_w(S₀) − 1 = Σ_{S≠S₀} [π(S)/π(S₀)]·[(π(S)/π₀(S))/(π(S₀)/π₀(S₀))]^{w−1}. The stage count is decided by how far past
φ = 1 the bridge can be extrapolated before this tilted sum reaches about 1/9.

**Corollary W′ (BO favourable). PROVED conditional on (LL).** Hypothesis (LL), the layer law of F-DRAFT Theorem W steps
2–5 at general w: with λ_n := R² log p → ∞, Δ_n → 0, and some g_n > 0,
1/q_w(S₀) − 1 = ε_n(w) with |log(9ε_n(w)) − λ_n(w − 1 − g_n)| ≤ r_n uniformly on [1, 2], where r_n = o(λ_n g_n).
Then w± = 1 + g_n(1 + o(1)), so T* = N(1 + g_n(1 + o(1))) and, with probability → 1,
**|T* − ⌈log₂(1 + 1/g_n)⌉| ≤ 1**. Here g_n = (log(√n/9) − log L_n)/(R² log p), and L_n is the slowly varying factor of
Theorem W(c). If p ≤ n^A, then g_n ≥ (1 − o(1))/(2AR²), so **T* ≤ ⌈log₂(1 + 2AR²)⌉ + 1 = O(1)**.
*Proof.* Theorem F, then the continuity of log₂((1+g)/g) in g. ∎ Status of (LL): PROOF SKETCH. It is exactly Theorem
W(b)/(c)'s computation with exponent (1 + κ(w−1))Z²/2 in place of (1 + κ)Z²/2, so W(b)'s crux (second-moment aggregation
over multi-extra layers) carries over unchanged.

**Theorem M (masked two-state crossing). PROVED.** Two states S°, S₀ with
log[γ_t(S₀)/γ_t(S°)] = −A₀ + t(A₀ + A₁). Here A₀ = log[π₀(S°)/π₀(S₀)] is the start masking depth and
A₁ = log[π(S₀)/π(S°)]. If A₀ ≥ 3 and A₁ ≥ 2.2, then
**log₂(A₀ − 1.48) − 0.95 ≤ T* ≤ log₂(A₀ − 2.2) + 11**, with no dependence on A₁.
*Proof.* Work in s = (A₀ + A₁)t − A₀ and take ℓ(s) = log(1 + e^s) relative to S°; by Lemma 0, Φ = ℓ(s_u) + ℓ(s_w) − 2ℓ(s_v).
Upper bound: Φ ≤ ℓ(s_w) because ℓ is increasing and ≥ 0. So the halving steps s_v = (s_u + σ₀)/2, with
σ₀ = log(1/9) = −2.197, are valid. After ⌈log₂(A₀ − 2.197)⌉ steps, s ∈ [σ₀ − 1, σ₀]. Steps with |Δs| = 2√c are valid
(ℓ″ ≤ ¼ and Theorem L(i)), so ⌈5.39/0.649⌉ = 9 of them reach s ≥ 2.197. Relative to S₀, ℓ̃(s) = log(1 + e^{−s}) is
decreasing, so Φ ≤ ℓ̃(s_u) ≤ c and one final step reaches t = 1.
Lower bound (K = 3):
- While s_v ≤ −K: Φ ≥ ℓ(s_w) − 2e^{−K}. Validity forces s_w ≤ σ_K = log(e^{c+2e^{−3}} − 1) = −1.481, so the gap
  σ_K − s at most halves per step.
- A valid step cannot go from s_u ≤ −K to s_v > 0: there Φ ≥ −s_u − 2 ≥ 1.
- A step landing in (−K, 0] has Φ ≥ e^{s_v}(Δs/2 − 1), so Δs ≤ 2 + 2ce^K = 6.23.
- Hence the last halving index j satisfies (A₀ − 1.481)/2^j ≤ σ_K + K + 6.23 = 7.75. At least two more steps follow,
  one into (−K, 0] and one to t = 1.
Theorem G turns these into bounds on T*. ∎

**Lemma P (perturbation). PROVED.** If |F − F₂| ≤ η₀ on [0, 2], then |Φ_F − Φ_{F₂}| ≤ 4η₀, so
T*_{F₂}(c + 4η₀) ≤ T*_F(c) ≤ T*_{F₂}(c − 4η₀). Take F₂ to be the pair log-normaliser, so that
η₀ = sup_{t∈[0,2]} −log q_t({S°, S₀}). Theorem M's argument goes through for every level c′ ∈ (0, 2c), with constants
continuous in c′.

**Corollary W″′ (corrected W″). PROOF SKETCH for the families; PROVED given PAIR.** Hypothesis PAIR:
sup_{t∈[0,2]} q_t(Ω ∖ {S°, S₀}) → 0. Under PAIR, **T* = log₂ A₀ + O(1)**, and T* does not depend on A₁.
- *Proxy split (Prop NM):* A₀ = (n/2)log[1/(1 − r²θ²/(σ²+θ²))](1 + o_P(1)) = Θ(n), so T* = log₂ n + O(1).
- *LH-iid / T27 (W3-PXN P4):* A₀ = c log p + (c/2)log n + O_P(1), so T* = log₂(c log p + (c/2) log n) + O_P(1).
  This is proved for c = 1 given PAIR. For c ≥ 2, the intermediate states S° ∪ M′ may create a chain of crossings, and
  the count is OPEN.
- PAIR itself is unproven: T22(iv-b)'s endpoint argument does not extend to pairs, because mid-path states can carry
  mass. It is supported numerically (pair_out_max falls with n, see §4).

## 4. Evidence (exact population grid, 60 halvings, V = Ω)

- `results/two_state.txt` (Theorem M). T* − log₂A₀ ∈ [6.0, 8.1] for A₀ from 0.5 to 10⁶ and A₁ from 5 to 10⁵, so the
  count is independent of A₁. At fixed t* = ½, T* = 9, 13, 17, 20, 23, 27, 30 for D = 10, …, 10⁷: it grows like
  log₂(D/2) + 7.7, which contradicts W″'s "O(1)". The crossing window |s| ≤ 3 always contains 6–7 grid points, which is
  W″'s correct part.
- `results/families.txt` (p = 12, two blocks of 6, exact 2¹² enumeration):
  - **BO favourable:** T* ∈ {1, 2, 4} at n = 200 and T* = 1 at n ≥ 3200. N(w₊) ≤ T* in all 36 runs, and T* ≤ N(w₋)
    wherever Δ ≤ 0.0513. At p = 12, ⌈log₂(1+1/g)⌉ overestimates (it predicts 2–3 where T* = 1), because log p = 2.5 is too
    small for the asymptotic constant.
  - **Proxy split:** T* = 14, 14 | 16, 16 | 18, 18 at n = 200 | 800 | 3200, against log₂A₀ + 7.7 = 14.1, 14.1 | 16.1, 16.0
    | 18.0, 18.1. This matches F-DRAFT's 14 and 16, and the increment of +2 per ×4 in n is the log₂ n law.
  - **Cancellation pair (LH-like, c = 1):** T* = 9–10 for all n from 200 to 12800, with A₀ = 5.0 → 6.6 and predicted
    10.0–10.4. This is O(log log n).
  - pair_out_max falls with n (0.38 → 0.04 for proxy, 0.52 → 0.03 for cancellation), which supports PAIR.
- `results/layer_model.txt` (W′ at p up to 10⁵ under the layer law, s₀ = 2, R² ∈ {0.5, 0.9}). T* ≤ 5 everywhere.
  |T* − ⌈log₂(1+1/g)⌉| ≤ 1 in 39 of 40 cells. The one miss (T* = 2 against 4) is at p = 100, n = 200, R² = 0.9, where
  Δ is not small.
- **Study stage counts:** `Results/SMC_BVS_v3_production/` holds runtimes and flag rates only (`smc_runtime.csv`,
  `analysis_T5_runtime.csv`, `smc_flag_rates.csv`). It has no per-fit stage counts, so we could not compare against the
  study. Recommendation: export `length(frozen$grid) − 1` and the pilot count.

## 5. What fails and why

- *Path length as the governing quantity.* It holds only for c → 0 (Theorem L(iii)). At c = log(10/9), the Rényi-2
  criterion extrapolates to 2v − u. In the large-deviation regime this gives halving rather than length-proportional
  steps, and the two-state family has L ≤ π with T* → ∞.
- *A lower bound by length without regularity.* No uniform constant exists, because the kernel min(x, 2Δ − x) vanishes
  at u. The family F″(u + x) = x^{−a}, a ↑ 2, makes (∫√F″)²/Φ unbounded.
- *Extending T22(iv-b) to a pair.* q_t(pair) need not be monotone or endpoint-controlled (Hölder fails, see §3), hence
  the PAIR hypothesis.

## 6. Needs escalation

- (LL) at general w ∈ [1, 2]: the second-moment aggregation crux of Theorem W(b). It turns Corollary W′ into a full
  theorem; O-WSTAB may supply it.
- PAIR on LH-iid and on proxy split, and the c ≥ 2 chain of crossings.
- Pilot fidelity: the finite-H pilot is an empirical ESS. Its relation to T*_Ω (a V12-type sampling statement) is OPEN.
  Theorem G(ii) needs T_P only as an input count.
- An independent check of Theorem M's constants (a numerical check is in `two_state.py`).

## 7. Outside scope

- Lemma 0 gives one-line proofs of T13-type statements: the restricted ESS is a ratio of single-model masses. It also
  suggests a cheap COVER diagnostic, comparing q^V_w(R) with the empirical occupancy of R.
- Theorem G(ii) shows the grid can only add stages to the pilot: T_grid ≥ T_P always.
- Only one quantity feeds T38's cost here, the masking depth A₀, and it already appears in T11/T27. A start with a
  smaller A₀ (mixture partitions, Prop P(ii)) shortens the bridge logarithmically.

## 8. Confidence card

| Target | Refined statement | True | Provable cheaply | Crux | Method change |
|---|---|---|---|---|---|
| Grid structure | Lemma 0, Lemma 1, Theorem G | high | done (PROVED) | none | no |
| T_n vs length | Theorem L (c → 0 limit, κ-bounds, worst case ⌈1.54D⌉) | high | done (PROVED) | none | no |
| W′ | T* ∈ [N(w₊), N(w₋)] (PROVED); \|T* − ⌈log₂(1+1/g)⌉\| ≤ 1 given (LL); T* = O(1) for p ≤ n^A | high | medium | (LL) = Theorem W(b) crux | no |
| W″ | FALSE as "O(1)"; T* = log₂A₀ + O(1), independent of A₁ (PROVED two-state; families given PAIR) | high | medium (PAIR) | PAIR; c ≥ 2 chains | no |
| T26 P1 | favourable: (T_n+1)Δ_n → 0 automatic once Δ_n → 0 and w₋ − 1 ≥ g₀ > 0 (BO: given LL); always via T_n ≤ T_e if Δ_n = o(log⁻²n); masked: P1 fails (Δ_n → 1) | high | high (cap route) / medium (sharp) | pilot fidelity for the method's T_n | no |
| T38(c) | cost O(N_n T_n(p+B+2) + ℓ_n p): T_n = O(1) (BO favourable), log₂n + O(1) (proxy), O(log log n) (LH, c = 1), ≤ T_e = O(log²(n+p)) always | medium-high | medium | PAIR, LL, pilot fidelity | no |

## Summary (8 lines)

1. The greedy ESS grid is provably the shortest valid grid; the v3 pilot-refining grid satisfies max(T*_V, T_P) ≤ T_grid ≤ T*_V + T_P (PROVED).
2. Key identity: ρ(u,v) = q_u(R)q_{2v−u}(R)/q_v(R)² for every state R, so stage counts follow a halving law at the extrapolated point (PROVED).
3. Favourable regime: N(w₊) ≤ T* ≤ N(w₋) through q_w(S₀), w ∈ [1,2] (PROVED); W′ follows within ±1 given Theorem W's layer law; T* = O(1) for p ≤ n^A.
4. W″ is false as stated: a masked crossing costs log₂A₀ + O(1) stages (two-state PROVED; exact numerics 14/16/18 = log₂A₀ + 7.7), independent of A₁.
5. Path length governs T* only as c → 0 (√c·T* → L, PROVED); at c = log(10/9) the two-state family has L ≤ π and T* → ∞.
6. T26: P1 is automatic in the favourable regime once Δ_n → 0 (sharp form on BO given LL; the T_e cap route needs Δ_n = o(log⁻²n)); masked: Δ_n → 1, so P1 fails regardless.
7. T38(c): T_n = O(1) on favourable BO, log₂n + O(1) on proxy masking, O(log log n) on LH masking, ≤ T_e = O(log²(n+p)) always; the study tables have no stage counts.
8. Head SHA: see the commit that adds this report on `theory/O-STAGES` (the report's own SHA is given in the run's final message).
