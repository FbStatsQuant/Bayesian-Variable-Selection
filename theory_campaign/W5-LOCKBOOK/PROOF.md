# W5-LOCKBOOK — PROOF.md

Run W5-LOCKBOOK, 2026-11-02. **Nothing here has been reviewed.** Each PROVED is a candidate that I checked line by
line; it is not adopted. Notation: `Docs/Theory/theorems/00_COMMON.md`, METHODOLOGY_v3 §3 budgets. Code references
are to `Scripts/SMC_BVS/core/` at commit 9db8748 (see `AUDIT.md` for fingerprints).

Contents: §T32 the score-evaluation ceiling (task goal 4); §R1 referee notes on W2-BOOK; §R2 referee notes on
W2-T26 (the verdict tables are in REPORT.md).

---

## §T32. Theorem T32(i): the score-evaluation ceiling of the SMC branch. PROVED.

### Definitions (new symbols)

- Budgets (METHODOLOGY §3, `v3_preprocess.R:19–33`): K = min(p, ⌊n/2⌋), B = min(⌊√n⌋, ⌊√p⌋, 16),
  ℓ = ⌈log₂(n + p + 1)⌉, L = max(4, ⌈log₂(n + 1)⌉), (N_e, H_e, T_e) = 4^e(N₀, H₀, T₀) for e ∈ {0, 1},
  N₀ = max(2500, n, p), H₀ = ⌈512N₀/2500⌉, T₀ = max(1000, ℓ²); m = p + B + 2.
- **M_p := max_{0≤k≤K} [p + k(p − k)] = p + k_*(p − k_*)**, k_* = min(K, ⌊p/2⌋) (k(p − k) is increasing in the
  integer k up to ⌊p/2⌋).
- **An evaluation** is one call of `Engine::eval` (`cpp/v3_engine.h:89`) or one direct call of `Scorer::score`
  (`cpp/v3_start.h:93`, `cpp/v3_core.cpp:417, 682`). Every call of the scorer made by `v3_fit` on the SMC branch is
  one of these (AUDIT §0), and an `eval` calls the scorer at most once (a cache hit calls it zero times). So
  **C_score ≤ C_eval**, where C_score is the number of scorer calls and C_eval the number of evaluations.
- **A logical score event** is one call of `Ledger::event` (`cpp/v3_ledger.h:102`); it adds the `held` events of SR
  to the evaluations of `eval`. C_log denotes their number.

### Statement

**Theorem T32(i).** Assume EX-A (used only in step 2(a): the pilot has at most T_e stages). For every valid input on
the SMC branch, every seed and every realisation of the streams and of the clock, the fit makes

  C_eval ≤ Σ_b 2^{|C_b|}
        + Σ_{e∈𝔈} { (1 + 4ℓ)·H_e·[1 + m(T_e + L + 4)] + (ℓ + 1)·[1 + (ℓ + 1)M_p] + (ℓ + 1)(40p + 1) }
        + 4N_{e*}·[1 + m(T_{e*} + L + 4)] + (80p + 1) + [1 + (ℓ + 1)M_p],

where 𝔈 ⊆ {0, 1} is the set of calibration tiers run and e* the final tier (the last two lines are absent if the
fit stops before the final run). In particular, with 𝔈 = {0, 1}, e* = 1,

  C_eval ≤ Σ_b 2^{|C_b|} + Σ_{e=0}^{1}(1 + 4ℓ)H_e[1 + m(T_e + L + 4)] + 4N₁[1 + m(T₁ + L + 4)]
        + (2ℓ + 3)[1 + (ℓ + 1)M_p] + 2(ℓ + 1)(40p + 1) + 80p + 1,                                     (T32-a)

with Σ_b 2^{|C_b|} ≤ p·2^B/B. The bound is deterministic (a sure bound). Counting logical score events instead,
C_log satisfies the same bound with every m(T_e + L + 4) replaced by (m + p)(T_e + L + 4) ≤ 2m(T_e + L + 4).

The pieces: **per particle-round ≤ m evaluations**; **per stage one round per particle**; per island N[1 + m(T + L + 4)]
with T ≤ T_e; the pilot and ≤ 4ℓ diagnostic islands of H_e particles per tier; 4 final islands of N_{e*}; **at most
2ℓ + 3 local searches, each ≤ 1 + (ℓ + 1)M_p evaluations**; plus the table scores, the V rescorings and the inherited
rescoring, which T32's conjectured form omits.

**Corollary T32(i-lit). PROVED.** The conjectured right-hand side of T32(i) (theorem file
`theorems/T32_T23C_resource_counts.md`),
  Σ_b2^{|C_b|} + Σ_{e=0}^{1}(1 + 4ℓ)H_e[1 + 2m(T_e + L + 4)] + 4N₁[1 + 2m(T₁ + L + 4)] + (8ℓ + 3)(ℓ + 1)M_p,
is ≥ the right side of (T32-a); so the conjectured inequality holds for C_eval (hence for C_score). It is **not**
established for C_log by this argument (see Remark 3).

**Corollary T32(c) (cost corollary of Thm 5(c)). PROVED.** With p ≤ n^A (A ≥ 1 w.l.o.g.) and n ≥ 3,
C_eval ≤ c_A · n^{2A} · log²n for an absolute-in-n constant c_A; in general C_eval = O(max(n, p)·p·log²(n + p)
+ p²log²(n + p)). So the number of score evaluations is polynomial in (n, p), deterministically. (The arithmetic
cost per evaluation, O(nK² + K³) per score under the fallback route, is T32(ii) and is not claimed here.)

### Proof

All references are to AUDIT.md §§0–6 and the code lines cited there.

**Step 1 (per particle-round ≤ m evaluations; per stage one round per particle).** A round applies the m labelled
steps once each (`one_round`, `cpp/v3_engine.h:202–214`; the order is a permutation of the m labels, `:195–200`).
Gibbs-j evaluates at most one model (the other configuration, only if feasible: `:119–123`); the held state is a
logical event, not an evaluation (`:118`, `:103–105`). A uniform swap evaluates at most one proposal (`:148–153`), a
neighbour swap at most one (`:165–174`), the independence step exactly one (`:186`; the π₀ draw is not a score).
So a round makes at most p + 1 + B + 1 = m evaluations and at most p + m logical events. A stage applies one
`population_round` to the resampled population (`:324–331`), i.e. one round per particle; resampling evaluates
nothing (`:234–259`).

**Step 2 (per island).** An island with N particles and T bridge stages (`run_island_s`, `:274–368`) makes N
evaluations for the initial draws (`:286–292`), N rounds per stage for T stages, L burn-in rounds and Hm = 4 measured
rounds per particle (`:343–360`): in total ≤ N[1 + m(T + L + 4)] evaluations.
(a) *Pilot*: adaptive schedule. Under EX-A every pilot step either reaches 1, or has lo − φ ≥ 1/T_e (the non-forced
branch, `cpp/v3_calib.h:38`), or is forced to min(1, φ + 1/T_e) (`:41`). So φ_k ≥ min(1, k/T_e) and the pilot ends
after at most T_e stages. (In floating point the snap at 1 − 10⁻¹² of `:42` is what keeps a fully forced pilot at
exactly T_e stages; not needed under EX-A.)
(b) *Diagnostic and final islands* run on a grid returned by `build_grid` with `ok = TRUE` (`v3_calib.R:84–86`;
`v3_calib.R:120, 153, 168` for the frozen grid), and a successful grid has at most T_e intervals
(`cpp/v3_calib.h:94`: failure as soon as the count exceeds T_e). So T ≤ T_e for the tier the grid was built at; the
final grid is the last grid of the final tier e*.

**Step 3 (calibration, per tier e).** `v3_cal_tier` (`v3_calib.R:28–131`) runs: one pilot island of H_e particles
(`:44`), then at most ℓ diagnostic iterations (`:85`), each with 4 islands of H_e particles (`cpp/v3_core.cpp:634–650`).
Islands: ≤ (1 + 4ℓ)H_e[1 + m(T_e + L + 4)] evaluations by Step 2. Local searches: one after the pilot
(`cpp/v3_core.cpp:610`) and one per diagnostic iteration (`:657`), so ≤ ℓ + 1. V rebuilds: the preliminary one
(`v3_calib.R:79`) and at most one per iteration (`:111`), so ≤ ℓ + 1, each rescoring |V| ≤ 20p + 20p + 1 models
(`cpp/v3_core.cpp:673–684`; the leader stores have capacity 20p and the top store 40p + 1, `cpp/v3_ledger.h:76`).
A stop at any point only removes evaluations.

**Step 4 (tiers).** `v3_calibrate` (`v3_calib.R:135–150`) runs tier e₀ = 0 (the default), and tier 1 only if a trigger
fired at tier 0; it never runs a tier twice (`:146`, `:149`). So 𝔈 ⊆ {0, 1}.

**Step 5 (final run).** `cpp_final_run` (`cpp/v3_core.cpp:388–486`): the inherited models are rescored once each
(`:415–419`), and their number is at most |top| + |lead0| + |lead1| ≤ (40p + 1) + 20p + 20p = 80p + 1
(`cpp_cal_export`, `:696–703`); then 4 islands of N_{e*} particles on the frozen grid (`:434–443`), ≤
4N_{e*}[1 + m(T_{e*} + L + 4)] by Step 2; then one local search (`:447`).

**Step 6 (local searches).** By Steps 3–5 there are at most 2(ℓ + 1) + 1 = 2ℓ + 3 local searches. Each evaluates its
centre once (`cpp/v3_engine.h:381`) and performs at most ℓ + 1 scans (moves ≤ ℓ, `:408`, `:411`); a scan of a centre
of size k ≤ K evaluates at most p flips and exactly k(p − k) swaps (`:393–405`), so at most M_p models. Hence each
local search makes ≤ 1 + (ℓ + 1)M_p evaluations.

**Step 7 (tables).** `build_tables` (`cpp/v3_start.h:83–97`) scores every U ⊆ C_b with |U| ≤ K, at most 2^{|C_b|} per
block. Since 2^c/c is nondecreasing on the integers c ≥ 1 and |C_b| ≤ B, 2^{|C_b|} ≤ |C_b|·2^B/B, and summing over the
partition gives Σ_b 2^{|C_b|} ≤ p·2^B/B.

**Step 8 (nothing else scores).** The remaining scorer call sites are the exact branch (`cpp/v3_core.cpp:506`, `:131`)
and user interfaces not called by `v3_fit` (`:112`, `:255`) (AUDIT §0). The SMC preflight is memory-only and scores
nothing (`v3_fit.R:16, 45`); `cut_group`, duplicate components and the neighbour graph read the Gram only.

Adding Steps 3–7 gives the displayed bound; taking 𝔈 = {0, 1}, e* = 1 and N₀ ≤ N₁, T₀ ≤ T₁ gives (T32-a). For C_log,
replace m by m + p per round in Step 1 (tables and inherited models are logical events one-for-one, `cpp/v3_core.cpp:381,
418`; the centre with `emit_centre = false` is not a logical event, so C_log's local-search term is ≤ that of C_eval). ∎

*Proof of Corollary T32(i-lit).* Write the conjectured right side minus (T32-a) as
  Σ_e(1 + 4ℓ)H_e·m(T_e + L + 4) + 4N₁m(T₁ + L + 4) + [(8ℓ + 3) − (2ℓ + 3)](ℓ + 1)M_p − (2ℓ + 3) − 2(ℓ + 1)(40p + 1) − (80p + 1).
Since M_p ≥ 1 and ℓ ≥ 1, the local-search part 6ℓ(ℓ + 1)M_p − (2ℓ + 3) ≥ 6ℓ² + 4ℓ − 3 > 0. For the rest, H₀ ≥ 512, m ≥ p + 3, T₀ ≥ 1000 give
(1 + 4ℓ)H₀m(T₀ + L + 4) ≥ 5ℓ·512·p·1000 ≥ 2.5·10⁶ ℓp, while 2(ℓ + 1)(40p + 1) + 80p + 1 ≤ 4ℓ·41p + 81p ≤ 245ℓp
(using ℓ ≥ 1, p ≥ 1). So the difference is positive. ∎ (`scripts/t32_count.py` checks the difference on a grid of
(n, p); the smallest value found is 1.09·10⁹ > 0.)

*Proof of Corollary T32(c).* ℓ ≤ log₂(n + p + 1) + 1, so T_e ≤ 4·max(1000, ℓ²) = O(log²(n + p)); L = O(log n);
H_e ≤ 4⌈512N₀/2500⌉ ≤ 4N₀ ≤ 4·max(2500, n, p); N₁ = 4N₀; m ≤ p + 18; M_p ≤ p + p²/4; B ≤ 16 so Σ_b2^{|C_b|} ≤ 4096p.
Each term of (T32-a) is then O(max(n, p)·p·log²(n + p)) (the islands), O(log²(n + p)·p²) (local searches),
O(p log(n + p)) (V and inherited rescoring) or O(p) (tables). With p ≤ n^A, A ≥ 1: O(n^{2A}log²n). ∎

### Remarks

1. **Numbers** (`scripts/t32_count.py` → `results/t32_count.txt`). At n = 200, p = 500: C_eval ≤ 2.68·10¹¹ with both
   tiers (1.62·10¹⁰ if no escalation); 23 local searches with ≤ 1.02·10⁷ evaluations in all. The conjectured form is
   5.35·10¹¹, which is exactly the theorem file's provisional Sol J9 figure: it is (T32-a) with the held states
   counted, i.e. about twice C_eval. At p = 1000: 5.62·10¹¹ (2.7·10⁷ in local searches).
2. **Corrections to the conjectured statement.** (a) It omits three scoring sources: the V rescorings
   (≤ 2(ℓ + 1)(40p + 1)), the inherited rescoring (≤ 80p + 1) and the local-search centres (≤ 2ℓ + 3). They are
   negligible and absorbed by its factor 2 (Corollary T32(i-lit)). (b) Its (8ℓ + 3)(ℓ + 1) counts more local searches
   than exist: the true number is ≤ 2ℓ + 3 (one per pilot and per diagnostic *iteration*, not per island).
   (c) "Both Gibbs alternatives counted" is a count of logical events; the held state is not re-evaluated (SR), so
   the cost-relevant count is m per round, not 2m.
3. **C_log and the literal 2m form.** For logical events the round term is (m + p)(T + L + 4) ≤ 2m(T + L + 4) with
   slack only (B + 2) per round, which does not absorb the V/inherited terms for every (n, p) by the argument above.
   I did not try to close this; it is cosmetic.
4. **What this makes of Thm 5(c).** The cost corollary "polynomially many score evaluations" is now a theorem
   (deterministic, every input on the SMC branch). On the exact branch the count is Σ_{k≤K}C(p, k) ≤ (5H₀ + 4N₀)p
   enumeration scores plus 200 timing scores (`v3_fit.R:10–14`, `cpp/v3_core.cpp:121–135`), also polynomial.
5. **Scope.** Only counts. Wall time, arithmetic per score, storage (T32(ii)–(iii)) and floating point are not
   claimed. The bound is an implementation contract for the code at this commit: any change to the loops (LS0
   adds one local search: replace 2ℓ + 3 by 2ℓ + 4) changes the constant.

---
