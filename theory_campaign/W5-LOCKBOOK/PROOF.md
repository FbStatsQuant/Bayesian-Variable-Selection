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
## §R1. Referee notes on W2-BOOK (line-by-line checks behind the REPORT verdict table)

**RO (Lemma RO).** Items 1–4 checked. The one step that needs the code is "𝒪 = 𝒢ᶜ ∩ 𝒪̄": 𝒪 ⊆ 𝒢ᶜ because
`resource_limit` ∉ {exact, completed}, and on 𝒢ᶜ status = st̄ by GUARD; for 𝒪_H = Uᶜ it is the definition
U = 𝒢 ∪ (𝒢ᶜ ∩ Ū). Both hold (AUDIT IMPL-GUARD). Item 5 / §0.3 counterexample: reproduced exactly by my own code
(`scripts/frozen_run_indep.py`, tensor form of the round; `results/frozen_run_indep.txt`): h = 33 gives P(𝒪) = 0.997834,
E[Ẑ | 𝒪]/Z = 0.97392; h = 32 gives 0.990674, 0.79784; h = 30 gives 0.961367, 0.01123, matching W2-BOOK's table to
every digit shown. **Robustness (new):** under the engine-faithful cost (AUDIT §3: the held state is not
re-evaluated, a Gibbs step costs one evaluation) the counterexample persists: h = 19 stops 0.32% of runs and gives
E[Ẑ | 𝒪]/Z = 0.9752; h = 16 stops 3.0% and gives 1.0014 (an *upward* bias). So the sign of the completion bias is
not fixed, which strengthens W2-BOOK's "direction is design dependent".

**Prop 2.** (a), (b), (d) are locked T12(iii) and linearity. (c): the expansion
E_𝓒[Ẑ·P̄_j] = (1/16)Σ_{r,s}E_𝓒[Ẑ_rPIP̂_{sj}], 4 diagonal terms Z·PIP_j (T12(iii)), 12 off-diagonal terms Z·μ_j
(T12(iv.c): islands independent and identically distributed given 𝓒), and μ_j − PIP_j = −Cov/Z from
E[Ẑ₁PIP̂₁] = Cov + Zμ — checked; numerically, Cov/Z gives ¾Cov/Z = 0.130481 and E[ẐP̄₁]/(Z·PIP₁) − 1 = −0.131716, both
reproduced to 10⁻⁵⁸ against a 4-island convolution. (e1)–(e3): checked; the exact branch contributes nothing because
Ẑ = Z there. (f): **wording GAP, fixable.** The inclusion {αẐ^fp > Z} ∩ G_fp ∩ 𝒪_E ⊆ 𝒜 ∩ {αe^ηẐ̄ > Z} needs that on
G_fp the *exact-arithmetic* potential run is itself on 𝒜 (calibration succeeded in exact arithmetic, so Ẑ̄ exists
and is that run's value). A floating-point calibration can in principle succeed where the exact one fails or freeze a
different 𝓒. Repair: put into VAL-FP(η, ε) "on G_fp, the exact-arithmetic run on the same streams has the same status
and the same 𝓒, and |log Ẑ^fp − log Ẑ̄| ≤ η". W2-BOOK's sufficient condition ("same discrete decisions") already
implies this if "decisions" includes the calibration's; the statement should say so.

**Run/output split edits.** T11(iii), T14(i), T15, T25(iv), T31, T34: checked as statement edits; no proof reads the
guard. **T23(ii-d) output form: scope GAP, fixable.** "P(𝒪_Eᶜ ∪ {MPM̂ ≠ S₀}) ≤ P(𝒢) + P(𝒜ᶜ) + 2E[1_𝒜𝓑_n]" is false
as written on the exact branch, where 𝒪_E holds and MPM̂ = MPM can differ from S₀ while 𝒜 (an SMC-branch event) is
empty. Restrict the left side to the SMC branch, or add P(exact branch, MPM ≠ S₀). (T23 itself concerns the SMC final
run, so the edit is only to the output corollary.)

**Prop 1.** (i′) checked: with w̃(s₀) = 1, w̃(k) = ε < m₀/M elsewhere, every |S| ≠ s₀ has w̃m ≤ εM < m₀, every
|S| = s₀ has m ≤ m₀, and S₀ is ≺-least among the size-s₀ maximisers; the prior is positive on 0..K because s₀ ≤ K.
(iii′) checked (same size ⇒ same prior ⇒ m(S′) > m(S₀) ⇒ S*_{s₀} ≠ S₀ ⇒ T07(i)). **Amendment for use on data:** the
certificate is about exact scores. In the study it certifies a miss only if F(S′) − F(S₀) exceeds the numerical
error of the two scores (the engine reports a heuristic bound `error_bound`, `cpp/v3_score.h:242–246`, explicitly
"not a validated interval bound"). With margins of order 10⁻⁶ nat or more this is immaterial, but the paper sentence
should say "strict, beyond numerical error". T06(i) "outer products" wording: correct against locked T06(i)(a);
the register's one-liner ("projection matrices X_S X_S′ agree") is the wording to fix.

**Thm 4.** (C1′): checked (locked C1 inclusion on R̄, plus GUARD on Uᶜ = 𝒢ᶜ ∩ Ūᶜ). It needs the convention
𝒢 ⊆ U (AUDIT caveat G1): a stopped fit returns an incomplete HPM that is not R̄'s. Route (a): Q_f = N(T + L + 5) draws
per island (N initial draws and one independence proposal per particle-round, T + L + 4 rounds) — checked against
`run_island_s`. Route (d): needs that every scan completes, which is IMPL-LS(a) on R̄; also S₀ ⊆ C_b makes S₀ a table
model (`build_tables` scores every U ⊆ C_b with |U| ≤ K). Route (e′)/(e-M): compared with W2-VT24G §6's three edits.
(1) Statement: W2-BOOK selects X_sel past-measurably on A_F with eligibility = feasibility s₀ + a(x) ≤ K — this is
W2-VT24G's edit 1 plus Theorem B's own feasibility premise (W1-T24G common setting), so W2-BOOK's eligibility set is the
right one; W2-VT24G's "any x ≠ S₀" should also carry feasibility. (2) Asymptotic paragraph: W2-BOOK's premise
(c_*(X_sel) ≥ c > 0, v ≤ v̄, Hη → 0) implies W2-VT24G's (Hc_* → ∞, v bounded, Hη → 0) because H = L + 4 → ∞; consistent
(slightly stronger premise). (3) Hypothesis list: E21-B2 deletes H24 and adds H-TB — matches. H ≤ L + 5 matches
W2-VT24G's note and the code (stage-T round at φ_T = 1 after the last resampling, L burn-in, 4 measured rounds).
(e-M) needs conditional independence of the H-round trajectories: Lemma STREAM (AUDIT §4) proves it for the
sequential single-stream implementation under EX-S. (d⁺): checked as an implication; **sharpening:** because the
last scan is completed before the limit test, a greedy path from a centre c reaches distance 1 after Φ(c) − 1 moves
and the next scan scores S₀, so the cap term is 1{ℓ < s₀ + d − 1}, not 1{ℓ < s₀ + d} (W4-T38FULL (b1) already uses
ℓ ≥ Φ(S°) − 1). The "541 fits" paragraph is interpretation and stays so.

**Reproduction of `frozen_run_exact.py`.** All seven locked/claimed numbers reproduced independently (REPORT §4):
D = 8.14676240634, π₀({1,2}) = 0.0279141173179, c₀ = 0.0694711126908, c₁ = 0.998708337452, PIP₁ = 0.990618012243,
E[P̄₁] − PIP₁ = −0.173974177850, E[ẐP̄₁]/(Z·PIP₁) − 1 = −0.131716; identities to 10⁻⁶⁰.

## §R2. Referee notes on W2-T26

**Lemma 1.** Checked: T22(iv-b) gives sup_{φ∈[0,1]}(1 − q_φ(S₀)) ≤ max of the endpoint deficits; φ ∈ {0, 1} gives ≥.
My reproduction found Δ_grid = Δ exactly (201-point grid) in every row (REPORT §4.2).

**Lemma 2.** Checked: π-reversibility gives K_e(x, y) ≤ π(y)/π(x); Gibbs-j at S₀ only reaches S₀Δ{j} (distinct over j),
so the Gibbs labels contribute ≤ u_π in total; the other B + 2 labels ≤ u_π each. The exact form
ρ̄ = 1 − ∏_e(1 − K_e(S₀, Ω∖{S₀})) is correct because, given the order, the path stays at S₀ iff each step in turn
stays, with probability 1 − K_{σ(k)}(S₀, Ω∖{S₀}) at step k, and the product does not depend on the order.

**Lemma 3 and the use of T15 at a terminal-round prefix (the step flagged for review). CORRECT.**
- B_{i,h} is T23's bad-round indicator (path of measured round h *including its start* X_{i,L+h−1}); the split
  B_{i,h} ≤ 1{X_{i,L+h−1} ≠ S₀} + 1{X_{i,L+h−1} = S₀, round L + h departs} is exact.
- The second term has conditional probability 1{X = S₀}·ρ̄ given everything before the round, by (R3). (R3) holds in
  the implementation: Lemma STREAM (AUDIT §4).
- The position "start of measured round h" is the population after the stage-T round followed by L + h − 1 complete
  rounds at φ = 1. T12(i.b) is stated exactly for "after stage T, any fixed finite sequence of operations, each a round
  at φ = 1 (or a unit-weight resampling)": with L + h − 1 rounds (L is a function of n, hence fixed given 𝓒) it gives
  E_c[Ẑ q̂(f)] = Zπ(f) at that position. This is T15's position class 𝒯(b) ("any fixed elementary prefix within the
  L + 4 terminal rounds"; a round boundary is such a prefix). The register closes H-T12 for T15 at 𝒯(b) by T12(i.b).
- W_r = Ẑ_r/Z is the same random variable at every terminal position (no factor after stage T), so the single L¹ bound
  b(𝓒) from T14 serves T15(iii) at every h.
- 𝔄 = {S₀} is deterministic, hence fixed given 𝓒, as T15 requires.
So E_𝓒 g_{r,h} ≤ min{1, 2δ₁ + 2b(𝓒)} for each h, and the frozen second premise (L+4)ρ* → 0 is indeed redundant.
I see no gap. (Independent confirmation that the redundancy is not cosmetic: in my reproduction at n = 40,960 the
median of (L + 4)ρ* is ≥ 1.6 in all three designs while ρ̄ + u_π ≈ 0.04; REPORT §4.2.)

**Theorem A.** (A-0)(a) T14(i-b) with S° = S₀: η_t ≤ Δ_n, ε_* ≤ Δ_n, so 2(T+1)Δ_n/(1−Δ_n) — checked. (b) T15(iii)+(i)
with c = ½ — checked (π(𝔄ᶜ)/c = 2δ₁, B/(1 − c) = 2b). (c) T23(ii-a, b) + Lemma 3 — checked; the primary PIP by
averaging. (d) Markov at ½ — checked. (A-i)/(A-ii): on A_x, Δ ≤ x/2, b ≤ 16x/7 < 3x, δ₁ ≤ x/2, u_π ≤ 4x/7 ≤ x,
ρ̄ ≤ 19x; 2δ₁ + 2b + ρ̄ + u_π ≤ 27x; union over 4 islands; logs via |log(1+u)| ≤ 2|u| for |u| ≤ ½ — all checked.
Exact branch through (P1-ex) with |PIP_j − 1{j ∈ S₀}| ≤ δ₁ — checked. **Output form:** OUT holds in the code with
"reported outputs" = the estimate fields (AUDIT IMPL-OUT); the reported MPM is uncapped (`v3_run.R:130`), and Theorem A
only uses it on {all PIP errors < ½}, where capped and uncapped coincide (s₀ ≤ K) — consistent. **T^max**: T ≤ T_e ≤
T₁ = 4T₀ on 𝒢_n is IMPL-T (`cpp/v3_calib.h:94`), so W2-T26's deterministic cap is correct.

**Theorem B.** Composition checked: T^max = O(log²n); δ₁ = O_P(r_n) by T03; within-block SE from SE once
m_n + s₀ ≥ 16 (00_COMMON's SE ranges over |T| ≤ min(p, m_n + s₀), and m_n ≥ log n/(2 log 2)); T22(iii) item 3; Lemma 1.
It is CONDITIONAL exactly as W2-T26 says (EXP′, VIS, NL_η, NL_avg are T22(iii)'s premises; T03 + T02(i) combined
unreviewed). One improvement since W2-T26: F-REFINE Card 3 reports EXP′ as a theorem (W1-EXP, verified by W3-VEXP),
which would remove EXP′ from the list; I did not re-check W1-EXP.

**Proposition C (ORTH), PROOF SKETCH — status kept.** I re-did the algebra: H_T = n²I, G_T + I = nI, D_T = n^k,
0.02 + Q_T = ρ_T + a_T with a_T = 0.02 + ‖z_T‖²/(n(n − 1)) ∈ [0.02, 1.02], |log(1+u) − log(1+v)| ≤ max(u, v), and a
noncentral χ²_{n−1−|C_b|} stochastically dominates the central one, so a χ² lower tail plus a union over ≤ p ≤ n
blocks gives ρ_min ≥ cn with probability → 1. The steps are standard and I found no error, but the constants were not
written out; it remains a PROOF SKETCH.

**Reproduction of the premise scan** (task: three sizes): REPORT §4.2.
