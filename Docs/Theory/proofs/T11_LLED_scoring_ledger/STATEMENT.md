# STATEMENT — T11(iii): iid π₀ draws of the final run

Source: `theorems/T11_LLED_scoring_ledger.md`, part (iii) only. Method: SMC-BVS v3.0, METHODOLOGY_v3.md
(SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c). Shared definitions: `theorems/00_COMMON.md`.

Original wording (the file's preamble to all parts): "Fix S* ∈ Ω measurable w.r.t. data and 𝓒 (before final
randomness)." Original wording of (iii): "P(S* absent from the final iid draws | 𝓒) = (1 − π₀(S*))^{Q_f} ≤ e^{−Q_fπ₀(S*)}.
The adaptive calibration draw count is never a fixed exponent."

Statement changes: **none.** The items under "Setting" make explicit what the original wording leaves implicit;
none adds a hypothesis beyond the file's assumptions (EX-A, EX-S, CAL) and the method's own specification (item 5
transcribes the method's description of the final run; aborts imposed by the computing environment are outside the
idealised model, as everywhere in this theory).

## Setting

1. **Data.** The data (X, y) are fixed (all probabilities are over the algorithm's randomness given the data). p, n, K,
   the blocks C_1, …, C_J, the tables r_b, γ₀, Z̄₀ and π₀ = γ₀/Z̄₀ on Ω = {S ⊆ [p] : |S| ≤ K} are then fixed
   (they are functions of the data only; METHODOLOGY §6.3). The definitions (00_COMMON §§1–2, METHODOLOGY §5, §6.3):
   - K = min(p, ⌊n/2⌋); the blocks C_1, …, C_J partition [p];
   - size prior ϖ(S) = w(|S|)/W_K for |S| ≤ K, with w(k) = ½/C(2p−1, k) > 0 and W_K = Σ_{k≤K} C(p,k) w(k);
   - tables r_b(U) = m(U)/m(∅) for U ⊆ C_b, where m(·) > 0 is the marginal likelihood, so every r_b(U) > 0;
   - γ₀(S) = ϖ(S) ∏_b r_b(S ∩ C_b) for S ∈ Ω, Z̄₀ = Σ_{S∈Ω} γ₀(S), π₀ = γ₀/Z̄₀.
   Hence π₀(S) > 0 for every S ∈ Ω.
2. **Randomness (EX-S).** The algorithm's randomness is a countable family of independent streams, each an iid sequence
   of Uniform(0,1) variables, with the method's stream separation: the calibration uses streams 0–9 only and the final
   run uses streams 10–13 only. Every random choice of the algorithm is made by reading not-yet-read values from the
   streams; which value is read next is determined by the data and the values read so far. Random operations are
   executed one at a time (each, e.g. one call of the π₀ sampler, completes before the next begins). All maps are Borel
   measurable.
3. **Exactness (EX-A).** Scores, convolutions, probabilities and comparisons are exact. In particular, each call of the
   π₀ sampler (METHODOLOGY §6.3: total size, then block sizes backwards, then each block's sub-model within its size
   class) maps the values it reads to its output by a measurable map (which may depend on the run's state when the
   call starts), and, when the values it reads are iid Uniform(0,1), its output has law exactly π₀.
4. **Calibration output (CAL).** 𝓒 := (grid 0 = φ₀ < … < φ_T = 1, T, L, N_e, tier e, candidate set V, every
   V-independent setting) is a measurable function of the data and streams 0–9; it includes the indicator of the event
   Λ = {the final run is launched} (SMC branch, preflight passed, a grid was produced; all decided before any final
   randomness). On Λ, T ≥ 1 is finite.
5. **Final run** (on Λ; METHODOLOGY §6.8, §6.5). 4 islands, each with N_e particles started from π₀ draws; the frozen
   grid; one move round per stage t = 1, …, T, then L burn-in rounds and 4 measured rounds at φ = 1; so each particle of
   each island goes through T + L + 4 rounds, and each round contains exactly one independence step, whose proposal is a
   π₀ draw (accepted or not). The **final iid draws** are these 4N_e initial draws and 4N_e(T + L + 4) independence
   proposals, in total
   Q_f := 4N_e(T + L + 5),
   a function of 𝓒. A launched final run executes all these rounds (no early stop; aborts imposed by the computing
   environment, such as wall time, are outside the idealised model).
6. **Target model.** S* is an Ω-valued random variable that is a measurable function of the data and 𝓒 (the file's
   "measurable w.r.t. data and 𝓒 (before final randomness)").

## Claim (iii)

On Λ, almost surely,

  P(S* is not among the Q_f final iid draws | 𝓒) = (1 − π₀(S*))^{Q_f} ≤ exp(−Q_f π₀(S*)).

## Scope note (the clause "the adaptive calibration draw count is never a fixed exponent")

The identity is asserted only for the final draws, with the 𝓒-measurable exponent Q_f. Nothing is asserted about the
calibration's π₀ draws: their number is adaptive (it depends on the calibration's own randomness, e.g. through the
rebuild loop and the escalation decision), so the identity is **not** claimed with the calibration draw count in place
of Q_f.

## Method facts quoted verbatim (METHODOLOGY_v3.md), used only to justify Setting item 5 and the scoring corollary

- §2, statuses: "`numerical_failure` (scoring failed after the fallback; estimates unavailable; the best scored model
  returned, labelled incomplete) · `resource_limit` (preflight predicts the memory or time allocation will be exceeded;
  estimates of the inputs returned)"; "`schedule_limit` (no admissible schedule within the stage ceiling at the highest
  tier; the best scored model is returned, evidence and PIPs unavailable)".
- §7 pseudocode: "preflight (§8.6) → maybe return"; "if grid construction failed at e = 1: return schedule_limit (best
  scored model)"; then "islands r = 1..4 (streams 10..13): FINAL_ISLAND(grid, N_e)    # bridge + L burn-in + 4 measured rounds".
- §6.13: "On a Cholesky failure, refactor from scratch, then use an augmented QR on X_S; if that fails, stop with
  `numerical_failure`".
- §6.5: "Independence proposal: S′ ~ π₀ (exact draw), accepted with 1 ∧ e^{φ[d(S′) − d(S)]}. Every proposal is scored,
  accepted or not."
