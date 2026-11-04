# API-T26BUD REPORT: task R5 (T26-BUDGET), Theorem 6 with a proved stage count

Run API-T26BUD, branch `theory/API-T26BUD`, 2026-11-02. Every result here is a **candidate**; none is reviewed or adopted. Full statements
and proofs are in `PROOF.md`; scripts are in `scripts/`, raw outputs in `results/`. (The task file names the folder `T26-BUDGET/`;
per the run instructions everything is under `API-T26BUD/`.)

## 1. Headline

- **Theorem G (grid stage count). PROVED, deterministic.** This applies to `v3_calib.h::build_grid`. On any successful construction
  with S₀ ∈ V, the realised count is T = N^pil + k^bis, with k^bis ≤ ⌈log₂(1/η_n)⌉. Here N^pil is the number of pilot
  stages, and η_n is the largest η ≤ 1 with R(0) ≤ ε₀ and R(1+η) ≤ ε₀, where R(t) = (1 − q_t(S₀))/q_t(S₀) and
  ε₀ = 0.9^{−1/2} − 1. The grid can over-refine only through the pilot, or when the bridge extrapolated past φ = 1 leaves S₀.
- **Theorem 1 (one-stage regime). PROVED, given its inputs.** If 1 − π₀(S₀) → 0, 1 − π(S₀) → 0, χ²(π‖π₀) → 0 and the HPM of π
  is S₀ w.p. → 1, then the pilot jumps 0 → 1 and the grid is {0, 1}: **T_n = 1 w.p. → 1**. So (P1) holds and Theorem 6
  (A-i)(A-ii) follow with no premise on the run. The proof uses only the iid first pilot stage, so no occupancy control
  is needed.
- **ORTH (Proposition O). PROOF SKETCH.** R(1+η) = O_P(n^{−1/2+Aη(1−λ*)} polylog) with 1 − λ* ≤ R²₀. So χ²(π‖π₀) → 0, and
  T_n = 1 w.p. → 1, when A·(1 − λ*) < ½ (in particular for p ≤ n^A with A < 1/(2R²₀)). Otherwise k^bis = O(1), but the
  number of pilot stages is only CONJECTURED to be O_P(1) (Conjecture P). The missing piece is occupancy control under the
  adaptive pilot.
- **Rule CAP. PROVED.** Under the cap "more than min{T_e, T^cap_n} intervals → fail" with T^cap_nΔ_n →_P 0 (e.g. ⌈log₂ n⌉),
  (P1) holds deterministically on 𝒢_n, and the cap costs nothing in Theorem A. The existing T_e = O(log²n) already gives
  the asymptotic statement (W2-T26 Theorem B). Only its constant 1000 makes it vacuous at finite n.
- **Numerics (exact p = 18, the actual pilot and grid rules).** [filled in §4]

## 2. Statements (full versions in PROOF.md)

Notation: q_t ∝ γ₀e^{td} for real t; r_S = γ₀(S)/γ₀(S₀); e_S = d(S) − d(S₀); R(t) = Σ_{S≠S₀} r_S e^{te_S}. Exact identity:
1 + χ²(π‖π₀) = [π(S₀)²/π₀(S₀)](1 + R(2)). The other quantities are N^pil, k^bis, η_n, ε₀, D_k, a = 0.5124 and T^cap_n (PROOF.md §0).

- **Fact 1 (PROVED).** ρ_V(u, ·) and the pilot's population ESS are monotone, so both bisections find the frontier of an interval.
- **Fact 2 (PROVED).** If S₀ ∈ V, then −log ρ_V(u, v) ≤ log(1 + R_V(u)) + log(1 + R_V(2v − u)), with R_V ≤ R, and R is convex.
- **Theorem G (PROVED).** On a successful construction with S₀ ∈ V: N^pil ≤ T ≤ N^pil + ⌈log₂(1/η_n)⌉. If η_n = 1, then T = N^pil.
- **Lemma P (PROVED).** A pilot stage advances by ≥ min{1 − φ, a/D_k} (D_k = 2 %-trimmed d-range of the population), and by
  ≥ 1/T_e. So N^pil ≤ 1 + ⌈D̄/a⌉ and N^pil ≤ T_e.
- **Corollary 1 (PROVED).** T_n ≤ min{T_e, 1 + ⌈D̄_n/a⌉ + ⌈log₂(1/η_n)⌉} on 𝒢_n ∩ {S₀ ∈ V}. Hence (P1) holds if
  P(𝒢_n, S₀ ∉ V) → 0 (true under T03 + 1 − π₀(S₀) → 0), η_n is bounded below w.p. → 1, and (N^pil + 1)Δ_n →_P 0.
- **Theorem 1 (PROVED given inputs).** Under 1 − π₀(S₀), 1 − π(S₀), χ²(π‖π₀) → 0 in probability and P(HPM(π) = S₀) → 1:
  P(𝒢_n ∩ {T_n ≠ 1}) → 0.
- **Rule CAP / Corollary 2 (PROVED).** Under CAP with T^cap_nΔ_n →_P 0, (P1) holds deterministically.
- **Proposition O (PROOF SKETCH).** On ORTH-F (Gaussian errors, p ≤ n^A), for η(1 − λ*)A < ½: R(1+η) → 0 in probability.
- **Conjecture P (CONJECTURE).** On ORTH-F, N^pil = O_P(1).

**Restated Theorem 6 premise (proposal for the paper).** "(P1) holds on every family where 1 − π₀(S₀) → 0, the HPM of π is S₀,
and χ²(π‖π₀) → 0. There T_n = 1 eventually (Theorem 1). On ORTH this holds for p ≤ n^A with A(1 − λ*) < ½ (Prop. O,
sketch). Under Rule CAP, (P1) holds on every family where Δ_n = O_P(r_n) and T^cap_n r_n → 0." If neither route is
acceptable, state Theorem 6 with the realised T_n, which is the fallback in the response plan.

## 3. Proofs

See PROOF.md §§1–6. The crux of Theorem G: in the second difference F_V(u) + F_V(2v−u) − 2F_V(v), the affine part of the
log-normaliser cancels. What remains is log(1 + R_V), which is ≤ log(1 + ε₀) wherever S₀ dominates the tilted law. So every
step whose reflected point 2v − u stays in [0, 1 + η] passes. Each bisection step therefore at least halves the remaining gap
1 − u beyond η, which gives the log₂(1/η) count. The crux of Theorem 1: the first pilot stage is iid π₀, and its population
ESS at δ = 1 is ≥ Ĝ²/(Ĝ + M̂) with E[M̂ | data] = π₀(S₀)R(2).

## 4. Evidence

[filled in after the sweep]

## 5. What fails and why

- **A bound of the form T_n ≤ C₁ + C₂ log(1/Δ_n) does not follow from the rules alone.** The pilot advances by a/D_k, and
  D_k is the d-range of an arbitrary particle population. One particle on a model with d − d(S₀) of order n forces a step
  of order 1/n. Excluding this needs occupancy control of the adaptive pilot, which is not available: T15 and T12 need a
  frozen grid. Theorem 1 avoids this by using only the iid first stage. Conjecture P is where it stays open.
- **The bisection count is controlled by the bridge past φ = 1, not by Δ_n.** Δ_n controls R only on [0, 1], while the
  last step from u to 1 evaluates F_V at 2 − u > 1. So the right quantity is η_n, i.e. R(1+η), a Rényi-type moment of π
  against π₀. It is not a function of Δ_n. On ORTH it is bounded below by a constant depending on A and R²₀ (Prop. O),
  which gives O(1) bisections, better than log(1/Δ_n).

## 6. Needs escalation

- Prop. O steps (1)–(4) (PROOF.md §6): uniform h-expansions, a T02-type truncation for the tilted law q_{1+η}, M×E
  cross-terms, and the σ̂ plug-in. A stronger prover could make this PROVED.
- Conjecture P: an occupancy bound for an adaptive SMC schedule (pilot), or a high-probability bound on the trimmed d-range of
  every pilot population.
- An independent check of Theorem G's count argument (it is short, but it is the main new claim).

## 7. Outside scope

- [filled in]

## 8. Confidence card

| target | refined statement | true? | provable at reasonable cost? | crux | method change? |
|---|---|---|---|---|---|
| T26 (P1) via the realised count | Theorem G + Theorem 1: T_n = 1 w.p. → 1 when χ²(π‖π₀) → 0 | high | done (candidate) for Theorem G and Theorem 1; ORTH input is a sketch (medium–high) | R(2) → 0 on the family | no |
| T26 (P1), general favourable families | T_n ≤ N^pil + ⌈log₂(1/η_n)⌉, N^pil = O_P(1) | medium–high | medium (Conjecture P needs adaptive-schedule occupancy) | pilot occupancy | no |
| T26 (P1) under Rule CAP | deterministic, T^cap = ⌈log₂ n⌉ | high | done (candidate) | none beyond Δ_n's rate | yes, a one-line change to the interval cap; inactive in the study |
