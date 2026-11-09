# C-ENG — PLAN: merge LS0 and the e4 tie-aware DP into the production core

Ticket C-ENG, Theory Wave 1C. Branch `w1c/ls0-merge`. Lead: Claude Opus 5.5 (Claude Work). Written 2026-11-08 ~21:45 CST.
Status: v1.1 (2026-11-08 21:45 CST) = v1.0 + all fixes of plan review R01 (`reviews/R01_plan_review_raw.md`, verdict REJECT as
written; disposition `reviews/R01_disposition.md`). v1.1 sent to a fresh reviewer (R02) in parallel with implementation.
v1.2 (22:30 CST): R02 findings (REJECT on plan text; R01 all RESOLVED) dispositioned in `reviews/R02_disposition.md`:
study-adapter compatibility (already in code 9b9d234), public-path forced-stop gate (test variant `paths`), wording.

Path aliases: `CORE/` = `Scripts/SMC_BVS/core/`; `STUDY/` = `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/core/`;
`SPEC` = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/MEET-v31/METHOD_v3.1_FINAL.md`;
`SoP/` = `Theory_work/State_of_Project/sections/`; `N3/` = `Theory_work/Wave1/W1-N3/`.

## 0. Which code is "the production core"

* `CORE/` is the production v3 core ("SMC-BVS v3 production core", `CORE/README.md:1`). Its public entry is `v3_fit(X, y,
  seed, allocation)` (`CORE/v3_fit.R:49`); final run `cpp_final_run` (`CORE/cpp/v3_core.cpp:388-486`), assembly
  `v3_assemble_final` (`CORE/v3_run.R:95-168`).
* `STUDY/` is the frozen study core (v2.2.1) cited by the State-of-Project document. Ignoring CRLF/LF, it equals `CORE/`
  plus two additive pieces: plain PIPs (`pip_plain*`, engine + `v3_run.R:167-169`) and a scored-set registry
  (`v3_registry.h`, `cpp_registry_*`, `keep_scored_set`). `v3_start.h`, `v3_score.h`, `v3_blocks.h`, `v3_calib.h`,
  `v3_runtime.h`, `v3_holder.h`, `Makevars.v3`, `v3_calib.R` (except the registry argument) are identical (checked with
  `diff --strip-trailing-cr`, see LOG.md).
* **Decision:** implement in `CORE/` only. `STUDY/` is a frozen campaign snapshot and is not edited. The changes are
  local to `start_mode`, `local_search`'s phase label, `cpp_final_run`, the ledger enum and the R assembly, so a later
  port to a v2.2.1-based core is mechanical (listed in REPORT as not done).
* Production calls `start_mode` nowhere: the header keeps it (`CORE/cpp/v3_start.h:178-240`), the Rcpp export was removed
  (`CORE/README.md:13`, SoP/02_method.tex:789). The O-LS0 test export (`theory/O-LS0:theory_campaign/O-LS0/scripts/ls0_exports.cpp`,
  `cpp_final_run_ls0`) is the prototype for the integration; it used `start_mode` with the default cap and
  `local_search(S̃₀, ell, tier, emit_centre = true, iter = -2)` on the same ledger and cache, after the final local search.

## 1. What the spec requires (verbatim sources)

SPEC:150 (#8, LS0), SPEC:136 (#6 GUARD-W), SPEC:151 (#9), SPEC:152 (#10), SPEC:162 (#15), SPEC:183 (#26 e4); restated in
SoP/02_method.tex:490-506. Requirements extracted:

R1. **When.** "After the final local search (and after the extra search from c₄ when R′ > 4), run one local search with the
    §6.10 rules from the start mode S̃₀". Production has R′ = 4 fixed (`v3_run_settings`, `CORE/v3_run.R:88`), so LS0
    runs immediately after the final local search, only on the SMC branch, only in the final run (not in calibration),
    and only if the final run has status "completed" after the final local search's guard check.
R2. **Centre.** S̃₀ = argmax γ₀ "computed exactly by the block DP, with the size-then-lexicographic tie rule"
    (smallest |S|, then lexicographically smallest sorted index vector; `lex_less`, `CORE/cpp/v3_util.h:117-119`).
R3. **§6.10 rules.** Same `Engine::local_search` (`CORE/cpp/v3_engine.h:378-418`): flips then swaps, centre frozen per
    scan, best neighbour by F with plain-lex ties, strict improvement only, at most ℓ moves then one further scan,
    `local_limit` iff that scan still improves. ℓ = the production `ell` = ⌈log₂(n+p+1)⌉ (`CORE/v3_preprocess.R:23`), the
    same value passed to the final local search (`ro$ell`); tier = the frozen final tier. **emit_centre = true**: the
    centre S̃₀ is scored as a score event (it is not necessarily already scored, unlike the final search's centre, which
    is the HPM). (W3-VT38E caveat cited in the O-LS0 export: "LS0 must emit its centre".)
R4. **No uniforms.** LS0 and the start-mode computation read no random variates (local search uses none; `start_mode`
    uses none). Stream endpoints 10–13 are therefore unchanged.
R5. **Ledger.** "Every model it scores joins the all-scored set and the stores": LS0 runs on the final run's own `Ledger`
    and `ScoreCache` (`cpp_final_run`), so every fresh LS0 score is offered to the running HPM and to the three stores
    (`Ledger::event`, `CORE/cpp/v3_ledger.h:102-111`). Cache hits are already in the stores (existing invariant,
    `v3_ledger.h:94-96`). Top store after LS0 = top_c(old ∪ added) (#9) — automatic.
R6. **Provenance.** "Models first scored by LS0 have provenance `ls0`": new phase `PH_LS0` (name "ls0") appended to the
    `Phase` enum (`v3_ledger.h:9`), mechanism `ME_LOCAL` ("local_scan"). `local_search` gets a phase parameter
    (default `PH_LOCAL`, so existing calls are unchanged). LS0 events: phase ls0, island 0, iter −1, tier = final tier.
    The HPM provenance is the event at which the model became the best (= its first score), so an HPM first scored by
    LS0 gets `hpm_provenance$phase == "ls0"`.
R7. **ls0_improved.** "set if LS0 raised the best score": `ls0_improved = F(HPM after LS0) > F(HPM before LS0)`
    (strict). Also reported: `ls0_hpm_changed` = the HPM model changed during LS0 (includes an equal-F tie-rule change,
    which does not raise the best score). Both in `fit$flags`.
R8. **E3 unchanged.** "An LS0 improvement does not fire E3. E3 refers only to the final local search from the HPM
    centre." Today E3 = `out$hpm_F > hb$F` (`CORE/v3_run.R:151`) with `out$hpm_F` the final HPM. After the merge `out$hpm_F`
    includes LS0, so E3 must be computed from the HPM **after the final local search and before LS0**
    (`hpm_before_ls0$F > hpm_before_local$F`). C++ returns `hpm_before_ls0` (model, F, provenance).
R9. **Certificate on the returned Ŝ (#10).** "`local_certified` and card item L1 are evaluated on the finally returned Ŝ,
    from whichever search ended on it (final search … or LS0)." Today: `local_certified = ls$local_certified &&
    hpm == ls$returned` (`v3_run.R:146`). New: `local_certified = (final$local_certified && hpm == final$returned) ||
    (ls0$local_certified && hpm == ls0$returned)`; `local_certified_by` ∈ {"final", "ls0", "both", "none"}. "A completed
    LS0 that ends on its move cap (`local_limit`) gives L1 = 'n/a'; the fit's output is still returned": reported as
    `ls0_local_limit` (fit and flags) and `local_certified` stays whatever the rule above gives (the LS0 branch
    contributes FALSE at a cap, because `local_certified` is false at `move_limit`). The certificate card L1 itself is
    not implemented in production (spec-only POST HOC item, SoP/02_method.tex:802), so no L1 field is added; the L1
    rule "capped LS0 ⇒ L1 = n/a" is documented and exposed as `ls0_local_limit`.
    **v1.1 (R01 #4, Q1):** public `local_limit` (fit and flags) = final search capped OR LS0 capped; attribution in
    `final_local_limit` and `ls0_local_limit`. With LS0 off, `local_limit` keeps its v3 value and the new fields are absent.
R10. **Other flags recomputed for the returned model (#9).** near ties, `near_tie_truncated` (from the top store after
    LS0), E1 (`island_best < hpm_F − 1`, island bests are not touched by LS0 because LS0 events have island 0) use the
    final HPM after LS0. `checks_passed_final` keeps its formula !(E1||E2||E3||lowESS).
R11. **GUARD-W (#6).** "Any worker stop, LS0 stop or guard stop ⇒ no output. … an LS0 stop is an operational
    interruption (worker, guard or resource stop) before LS0 completes. A completed LS0 that ends on its move cap is
    not a stop." Implementation: (a) after LS0 completes, the stop-only runtime guard is checked once with the LS0
    duration (start-mode DP + search), checkpoint "ls0", event phase ls0 (same pattern as the final search's
    checkpoint "local_search", `v3_core.cpp:450`); exceeded ⇒ status `resource_limit` ⇒ `v3_assemble_final` takes the
    no-estimate branch (`v3_run.R:111-116`: `estimates_available = FALSE`, `partial_results = TRUE`, no log_Z/PIP/MPM
    fields assigned). (b) A `NumericalFailure` inside LS0 ⇒ status `numerical_failure` ⇒ same branch. (c) LS0 is not
    started if the run is already stopped (`status != "completed"`). (d) `local_limit` at the LS0 cap is not a stop.
    (e) The serial core has no workers. **v1.1 (R01 #1, BLOCKER):** #15 is implemented in v3.1 mode (switch on): a
    shared helper `v3_unavailable_estimates()` sets every estimate field to NA **by exact name** (`log_Z`, `log_Z_r`,
    `log_Z_lower95`, `log_Z_rel_m0`, `log_Z_r_rel_m0`, `pip_primary`, `pip_r`, `mpm`) on every public `v3_fit` return
    with `estimates_available` not TRUE (all statuses), so `fit$log_Z` can no longer partial-match `log_Zbar0`.
    Partial island values stay only in labelled archives (`partial_final`, `stage_record`). Tested with both
    `fit[["log_Z", exact = TRUE]]` and `fit$log_Z`. Switch off ⇒ old behaviour (fields absent).
R12. **e4.** "Start-mode ties: keep the enumeration fast path (cap 10⁶, `cpp/v3_start.h:183`). On truncation, use a
    deterministic tie-aware DP that returns the prescribed smallest-size, lexicographically smallest maximiser without
    enumerating ties." W1-N3 proved (N3/STATEMENT.md §3(b)-(d)) that the enumeration visits the ≺_DFS-first min(N, cap)
    smallest-size maximisers and is wrong when N > cap (counterexample p = 44, K = 22, `N3/numerics/cex_default_cap.py`),
    and gave TDP (N3/lemmas/L7_tie_aware_dp.md).

## 2. e4 design: TDP restricted to the enumeration's tie set (TDP-E)

Floating point matters: N3 (e) notes that the enumeration follows per-block **exact** maximisers (`arg[b][j]`) and exact
prefix equalities `v == M[b][r]`, so in binary64 the set it visits, E := {S : per-block codes in `arg[b][j_b]`, size path
(j_b) tight in the DP from (J, k̂*) to (0, 0)}, can be a strict subset of the ĝ-maximisers of size k̂* (rounding ties).
L7 warns that an implementation "must compare Φ with V* using the same evaluation order as the code's ĝ, or the
lexicographic guarantee holds only under EX-A".

To keep the fast path and the fallback consistent bit for bit, the fallback computes **lex-min E** (= what `start_mode`
would return with cap = ∞), greedily, without enumerating E:

* Precompute (already in `start_mode`) `mb[b][j]`, `arg[b][j]` (per-block per-size exact maxima and their codes), the DP
  table `M[b][k]`, `kbest` = k̂*. Tight edge (b, r, j): `M[b−1][r−j] != −inf` and `(j == 0 ? M[b−1][r−j] :
  M[b−1][r−j] + mb[b−1][j]) == M[b][r]` (identical expression to the enumeration, `v3_start.h:230-232`).
* State IN, OUT (disjoint index sets). allowed[b][j] := ∃ c ∈ arg[b][j] with IN∩C_b ⊆ c and c ∩ OUT = ∅ (bitmask tests).
* feasible(IN, OUT) := (J, k̂*) reaches (0, 0) through tight edges with allowed[b−1][j] (boolean DP over (b, r), cost
  O(Σ_b (K+1)(t_b+1))).
* For i = 0..p−1 (internal index order = original order, N3/STATEMENT §1): if feasible(IN ∪ {i}, OUT) then IN ∪= {i}
  else OUT ∪= {i} (only block blk[i]'s allowed row changes; recompute that row). Return IN.
* Claim (proof and hypotheses in `lemmas/TDP_E.md`; contract bounded per R01 #2/#6: lex_min(E) in binary64, = S* under
  EX-A; NOT lexicographic optimality over all rounded ĝ-maximisers, which neither the fast path nor the fallback
  provides — see the 2⁵⁴ example of R01 #2): TDP-E returns lex_min(E). Invariant IN = S_E ∩ {0..i−1} with
  S_E := lex_min E; same argument as L7, with 𝒜* replaced by E and Φ = V* replaced by "E ∩ 𝒮(IN, OUT) ≠ ∅", which the
  reachability DP decides exactly (E is a product of per-block code sets over tight size paths; IN/OUT constraints are
  per element hence per block). No arithmetic is done by TDP-E beyond reusing M and mb, so the claim holds in binary64.
  Under EX-A, E = 𝒜* (N3 (b)), so TDP-E = S* = TDP.
* Consequence: the new `start_mode` returns lex_min(E) for every N; for N ≤ cap... more precisely whenever the enumeration
  is not truncated the code path and result are byte-identical to the old ones; when truncated (count ≥ cap) the result
  is TDP-E's (equal to the old result when N == cap). `ModeResult` gains `tie_dp_used` (bool); `ties`/`truncated` keep
  their meaning (enumeration count, truncation flag).
* Switch: `start_mode(st, cap, tie_dp = true)`; `tie_dp = false` reproduces the old function exactly.
* Cost: (p + 1) feasibility passes × O(J (K+1)(B+1)) + row recomputations O(2^B) each; p = 1000, K = 100, B = 16,
  J ≈ 63: ≈ 10⁸ elementary ops worst case, only on truncation (0/2,400 study fits truncated, SPEC:150).

## 3. Code changes (planned)

1. `CORE/cpp/v3_start.h`: `start_mode(st, cap, tie_dp)` with TDP-E fallback; helper `start_mode_tie_dp(...)` also callable
   directly (tests).
2. `CORE/cpp/v3_ledger.h`: append `PH_LS0` (name "ls0") after `PH_TEST`.
3. `CORE/cpp/v3_engine.h`: `local_search(..., int iter = -1, int phase = PH_LOCAL)`; sets `ev.phase = phase`.
4. `CORE/cpp/v3_core.cpp`:
   * `cpp_final_run`: read `ro$ls0` (absent ⇒ false), `ro$ls0_tie_dp` (absent ⇒ true), `ro$ls0_ell` (absent ⇒ `ro$ell`;
     hook for an HQ-forwarded ℓ_n schedule). After the final search and its guard check, if completed and ls0: record
     `hpm_before_ls0`; time t1; `ModeResult m = start_mode(st, 1000000, tie_dp)`; `A0 = E.local_search(m.S, ls0_ell, tier,
     true, -1, PH_LS0)`; guard check (`"ls0"`, phase ls0). Outputs `ls0`, `hpm_before_ls0`, `start_mode`
     (model, log_gamma0, ties, truncated, tie_dp_used), `seconds_ls0`. When ls0 is off, none of these fields is added.
   * `counter_matrix`: include the `ls0` row only when the final run has ls0 on (calibration ledgers never include it),
     so switch-off output is byte-identical to the old output.
   * `local_event` helper gets a phase argument (runtime.h) or a new `ls0_event`.
   * Test-only exports are **not** added to production (README policy); they go in a test file appended to a testing copy
     (`Theory_work/Wave1C/C-ENG/tests/ceng_exports.cpp`): direct `start_mode` with arbitrary tables/cap/tie_dp, brute force,
     direct local search.
5. `CORE/v3_run.R`: `v3_run_settings(setup, frozen, ls0 = getOption("v3.ls0", TRUE))` adds `ls0 = TRUE`, `ls0_ell`,
   `ls0_tie_dp` to `ro` only when on; `v3_final_run(..., ls0 = ...)`; `v3_assemble_final`: E3 from `hpm_before_ls0`,
   `local_certified` per R9, flags `ls0_improved`, `ls0_hpm_changed`, `ls0_local_limit`; fields `ls0` (archive with
   phase "ls0"), `hpm_before_ls0`, `start_mode`, `timings$ls0`.
6. `CORE/v3_fit.R`: `v3_fit(X, y, seed, allocation, ls0 = getOption("v3.ls0", TRUE))` passes it on. Default ON (v3.1);
   `ls0 = FALSE` (or `options(v3.ls0 = FALSE)`) = old behaviour.
7. `CORE/README.md`, `CORE/source_manifest.json`: document; manifest hashes updated by `build/update_core_manifest.py` if
   it runs locally (else recorded as not done).

## 4. Tests (all local, Windows R 4.6.1 + Rtools45; outputs in `numerics/` and `tests/`)

(a) TDP unit tests: random small instances (integer and real tables; K binding; duplicates/ties) — new `start_mode` with
    small caps (1, 2, 3, …) vs uncapped enumeration (lex_min E) for ALL kinds; vs brute force over Ω_K (lex-min of the
    smallest-size maximisers) ONLY for integer-valued tables (exact binary64 sums); for real tables only value lg0 and
    size |S| are compared with brute force (R01 #2); explicit rounding-tie fixtures (R01 #2 2⁵⁴ example; prefix and
    prior rounding); boundary fixtures (K binding, interleaved blocks, j = 0, NaN beyond K) (R01 #6); N3's p = 44, K = 22 counterexample tables at cap = 10⁶ (old returns ≠ S*, new returns S*), and
    the family D_m at small caps; cross-check with `N3/numerics/tdp.py` on integer tables.
(b) LS0 behaviour: centre emitted (logical count of phase ls0 ≥ 1, centre in the scanned list, centre score fresh when
    not previously scored); every LS0-scored model offered to the ledger (top store ∋ best LS0 neighbour when it
    qualifies; HPM after LS0 = hpm_better-max of HPM before LS0 and all LS0-scored F); provenance "ls0" on an HPM first
    found by LS0 (constructed case: inherited/grid settings where LS0 finds a better model, or a synthetic setup where the
    start mode is far from where the islands go); E3 unaffected by LS0; `ls0_improved`; GUARD-W: (i) allocation set so
    the guard trips at the ls0 checkpoint ⇒ status resource_limit, estimates_available FALSE, every estimate field present
    with NA by exact name and `fit$log_Z` NA (v1.2, R02 #3);
    (ii) LS0 capped (`ls0_ell = 0` via ro) ⇒ completed output with ls0_local_limit TRUE.
(c) Regression on S1–S6 (small n/p, a few seeds) with the study generator (or a local equivalent): `v3_fit` old core vs new
    core with ls0 = FALSE (expect identical deterministic outputs: every field except the named operational
    measurements timings/seconds/elapsed/peak memory, on completed runs with ample allocation — R01 #7) and new core with ls0 = TRUE (expect: islands, Ẑ, PIPs,
    stage tables, stream endpoints identical; HPM either identical or hpm_better than the old; stores = top_c(old ∪ added)
    checked where the scored set is small; E3 identical; report every change).
(c2) **Merged-LS0 replay (R01 #3, SPEC:399):** new core (LS0 on) vs the O-LS0 prototype `cpp_final_run_ls0`
    (export appended to a testing copy of the OLD core, `ls0_enable_integrated()`), same data/seed: islands, Ẑ, PIPs,
    HPM, stores, flags, E3, stream endpoints, LS0 archive and counters must agree after normalising the intended
    metadata differences (prototype: phase `local`, iter −2, counted in the `local` row; new: phase `ls0`, iter −1,
    own row). On all p = 30 regression datasets, and on the 3 replay designs (S1 r001, S4 r001, S5 r002) with the dev
    generator at p = 500, c100, if local runtime allows; otherwise recorded as an unmet gate.
(c3) **Deterministic fixtures (R01 #5):** low-N direct `cpp_final_run` runs (testing copy) chosen so that the start mode
    is unscored before LS0 (exact LS0 event count = 1 + n_evaluated, fresh centre event, centre wins HPM so omission
    is observable); a case with a strict improving neighbour and `ls0_ell = 0` (⇒ `ls0_local_limit`, output returned);
    an equal-F HPM tie change by LS0 (duplicated column); a returned HPM different from both endpoints; store eviction;
    forced guard stop at checkpoint "ls0" and forced NumericalFailure inside LS0 (test injection in the testing copy) ⇒
    no estimates, NA fields; every fixture asserts `branch_run == "smc"` / LS0 archive present.
(c4) **Public-path gate (v1.2, R02 #2; SPEC:400):** 10 public `v3_fit` forced stops (allocation 0.05 s; local analogue of
    API-AUDIT's table, whose inputs are not in the repository) and every early return (invalid seed, y_constant,
    no_predictors, preflight stop, exact branch, completed), each with the 8 NA fields / finite estimates as appropriate
    and consumed by the study adapter.
(c5) **Study adapter (v1.2, R02 #1):** `smcbvs_outputs` reads a scalar NA estimate marker as absent
    (`smcbvs_estimate()`), keeps validating supplied values; tested on stopped, early-return, exact and completed fits.
(d) Existing tests: `Scripts/SMC_BVS/tests` (prototype-vs-production bit comparison harness, Owls-oriented) and
    `build/check_smokes.R` (inspects saved Owls smoke records) — run what can run locally; record exactly what cannot
    and why.

## 4b. Switch-off branch (R01 #7)
`ls0 = FALSE`: `ro` carries no LS0 fields; `cpp_final_run` runs no LS0 and serialises ledgers without the `ls0` counter
row; `v3_assemble_final` keeps the v3 E3 (`out$hpm_F > hb$F`), certificate, `local_limit`, flags and field layout and
emits no LS0 metadata; `v3_fit` adds no NA fields. Calibration ledgers never carry the `ls0` row (LS0 never runs in
calibration) in either mode. `mode_tie_dp` checks its root feasibility and stops with an error (never an empty model)
if the invariant fails (R01 #6).

## 5. Questions for the plan reviewer (answered in R01: Q1 public local_limit = either cap; Q2 yes; Q3 yes under EX-A, bounded binary64 claim; Q4 yes)

Q1. Should the fit-level `local_limit` flag become "local_limit of the search that ended on Ŝ" or stay = final search,
    with LS0's cap in a separate `ls0_local_limit`? (Plan: separate field.)
Q2. E1 after LS0: use the final HPM (after LS0) as #9 "flags … recomputed for the returned model" suggests? (Plan: yes.)
Q3. Is TDP-E (lex-min of the enumeration's tie set) an acceptable reading of e4 "the prescribed smallest-size,
    lexicographically smallest maximiser"? It equals S* under EX-A and keeps the fast path and fallback consistent in
    binary64.
Q4. ℓ for LS0 = production ℓ (same as final search)?
