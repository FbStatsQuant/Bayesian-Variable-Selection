# Q5 — Lemma DLV-0: deterministic delivery at the pinned code (claim W3-RM2-R:DLV-0; STATEMENT (C-D))

Status: **PROVED (by this seat, unchecked)**; LC-B (Sol) VERIFIED-WITH-AMENDMENTS, amendments [LCB-1..3] applied (re-check pending); relative to the code-reading audits it inherits (C-DLV P1 inventory and
Lemma S.3, "AUDITED (code reading)") and to the re-audit of §2 below (a code reading by this seat) — 2026-11-16, lead
Claude Opus 5.5. Ticket W3-RM2-R; statement: `../STATEMENT.md` v1.0 §2 ((D), IDEAL-W⁺, 𝔇, valid non-degenerate input),
§3 (C-D). New file; no new mathematics: it restates the design-free delivery step of the cited sources as a statement
about every input and re-audits the exits against the code as pinned.

**Pin.** Branch `theory/W3-RM2-R` at 2aeb860 (= `origin/main` for the core); `Scripts/SMC_BVS/core/` last changed at
72785fe. CORE := `Scripts/SMC_BVS/core/`. DLV := `Theory_work/Wave1C/C-DLV/`; FIN := `Theory_work/Wave1C/FINAL/sections/`.

**Sources (statuses verbatim; only their delivery / law-free parts are used).**
* DLV Theorem D (`lemmas/L4_delivery.md:13-42`) — C-DLV:Thm-D@1.0.0 "PROVED-CHECKED (relative to the P1/P3 audits)":
  the exit walk of `v3_fit`. In it the data law enters only through Lemma S.1.
* DLV Lemma S.2 (`lemmas/L2_degenerate.md:20-35`) — C-DLV:L2-S2@1.0.0 "PROVED-CHECKED": under EX-A the scorer never
  fails, for any input with yᵀy > 0 (a deterministic statement). Lemma S.3 (`:37-67`) — C-DLV:L2-S3 "AUDITED (code reading)".
* DLV Lemma R, Corollary R (`lemmas/L1_resources.md:70-81, 129-143`) — C-DLV:L1-R@1.0.0, C-DLV:Cor-R@1.0.0
  "PROVED-CHECKED (council round 2)": "for valid inputs …, every seed and uniform realisation" (deterministic).
* DLV grid Lemmas 3.3, 3.4 (`lemmas/L3_grid.md:30-56`) — "PROVED-CHECKED": every pilot schedule and every successful
  construction starts at 0, ends at 1, is strictly increasing and has ≤ T_e intervals.
* The delivery half of DLV Proposition F in the restated form of `Theory_work/Wave3/API_AUDIT/pass1/R-AUD1_sol.md:32-35`
  ("Under the premises of Theorem D, P(𝒰_n) = 0 for every n ≥ 3"); its consistency sentence (`L4_delivery.md:83-84`)
  is **not** used (`Theory_work/Wave3/API_AUDIT/pass1/TRIAGE.md:23-28`).
* The extension of that delivery half to the C-GROW cap a_n = ℓ_n + |S̃₀| with total fallback and the LS0 preflight:
  FIN `s6_delivery.tex:29-46` (HQ audit A1 corrected statement, council round 3 passed; A4 preflight addition,
  OK-WITH-FIXES), as consumed by W2-UNI:F-UNI@1.1.0 ("PROVED-CHECKED"), `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:8-12, 27` (method/allocation; its Step 2, "design-free: P(no output) = 0") [LCB-3]. From these we take **the allocation 𝒜_n**: the inequalities of FIN
  `s6_delivery.tex:33-44` (A1's envelopes W_G, M_G and A4's additions P̄_LS0, P_e + A), evaluated at (n, p_raw).
* Lemma E4 (W3-RM:E4@1.0.0, "PROVED-CHECKED"; RM `STATEMENT.md:219-230`): on every accepted input `start_mode` returns a
  maximiser of γ₀, for both values of `tie_dp`.

## 1. Statement

**Lemma DLV-0.** Assume the implementation premises and configuration of STATEMENT §1 and the delivery premises (D) of
STATEMENT §2 — IDEAL-W⁺, EX-A (with its unit-cost reading), MACH(τ, τ₀, β, β₀), CONFIG at the shipped configuration
(`ls0 = TRUE`, LS0 cap ℓ_n + |S̃₀|, `grid_fallback = TRUE`, declared R′ = 4k, fixed worker count, default 𝓗), TDP-IMPL,
EX-S, SR, GUARD-W, OP-LS0, and the allocation 𝒜_n. Then for every valid non-degenerate input (n ≥ 3; X^r a finite numeric
n × p_raw matrix with at least one non-constant column; y^r a finite numeric vector of length n without dim attribute,
not constant; a scalar whole-number seed in [1, 2³¹ − 1]; an allocation list with scalar finite positive `mem_gb`,
`hours` satisfying 𝒜_n), every seed and every realisation of the method's uniform streams, `v3_fit` returns a fit with
`estimates_available = TRUE`. Without the two lifted predicates of IDEAL-W⁺ (DLV's IDEAL-W only), the same holds for
every such input in 𝔇 = {⌈log₂(n + p_raw + 1)⌉ ≤ 10⁶, ⌈log₂(n + p_raw + 1)⌉ + ⌊n/2⌋ ≤ 2³¹ − 1}.

## 2. Proof: the exit walk at the pin

We walk `v3_fit` (CORE `v3_fit.R:73-174`) and list every way it can end without estimates — every `return(finish(fit))`
before `estimates_available` is set, every `stop()`/`throw` on its call graph — and exclude each. The walk follows DLV
Theorem D's proof (`L4_delivery.md:24-42`), whose inventory (P1) and unreachable-path list (S.3) are inherited as
audits; the changes since the code C-DLV audited (39db138) are the C-ENG commits 9b9d234, 36c0cfe, bf093a8, 0638af9,
ef33f91, 98fac03, 72785fe, and their new exits are listed in (E5)–(E8).

**(E1) Input validation.** `v3_fit.R:88-89` (seed: length 1, `v3_check_seed`, `v3_preprocess.R:7-11`), `:91-94`
(allocation: list; `mem_gb`, `hours` scalar, finite, positive; missing names default to 8 / 24), `v3_preprocess.R:97-107`
(X numeric matrix; y numeric vector without dim; length(y) = nrow(X); finite entries; n ≥ 3; p_raw ≥ 1),
`:111-114` (`no_predictors` iff every column is constant), `:115` (`y_constant` iff all y entries equal). Each is
excluded by the definition of a valid non-degenerate input (this replaces DLV Lemma S.1, whose model G was used only to
show these events are null; `L2_degenerate.md:5-18`). Dropping constant columns is not an exit; the retained p ≥ 1 and
p ≤ p_raw, and every budget and allocation term is non-decreasing in p, so 𝒜_n at (n, p_raw) covers (n, p).

**(E2) Resource exits.** The preflight `v3_fit.R:116-117` (`pf$exceeds`: memory components and, on the exact branch,
the measured score time; on the SMC branch with the C-GROW cap also the LS0 archive and LS0 time, `v3_fit.R:25-70`); the escalation preflight `v3_calib.R:157`; the runtime guard (`cpp_runtime_check` in grid construction, `v3_calib.R:75-76`, tested at `:81`, `:113`;
GUARD-W checks in the final run, `cpp/v3_core.cpp:451, 459, 480`, the last one new for LS0); `resource_limit` statuses of
pilot / diagnostic / rebuild / final run. Under MACH and 𝒜_n none fires: this is Corollary R with the envelopes and
preflight bounds of FIN `s6_delivery.tex:33-44` (A1: LS0 count ≤ 1 + (ℓ_n + K + 1)q(p), q(p) = p + p²/4, from the cap
ℓ_n + |S̃₀| ≤ ℓ_n + K; A4: the LS0 preflight time 2(ℓ_n + K + 1)q(p)ŝ_K ≤ P̄_LS0 and memory P_e + A, with the strict ">"
tests so that equality passes). These are deterministic bounds for every valid input, seed and uniform realisation
(Lemma R's form). The fallback grid has ≤ T₁ intervals (E4), so the final run's bridge-stage count stays within
Lemma R's cap.

**(E3) Numerical exits.** `v3_setup` failure (`v3_fit.R:134-138`), calibration and final-run `numerical_failure`
(`v3_calib.R:57, 80, 100, 112`; `cpp/v3_core.cpp:484`), exact-branch `numerical_failure` (`cpp/v3_core.cpp:556`). All
originate in `Scorer::score` (`NumericalFailure`); by Lemma S.2 it never throws under EX-A when yᵀy > 0, and after
standardisation yᵀy = n − 1 > 0 because y^r is not constant (E1). The k > K invariant throw of the production scorer (`cpp/v3_score.h:230`; S.2's last paragraph) is unreachable [LCB-2]
(the separate throw at `cpp/v3_core.cpp:112` belongs to the auxiliary `cpp_score` entry point, not on the `v3_fit` path). So on the exact branch `e$status = "exact"` and `estimates_available = TRUE`
(`v3_fit.R:120-131`).

**(E4) Calibration without a grid.** `v3_calib.R:170`: `schedule_limit` (final tier 1, no grid) or
`grid_failure_no_escalation` (final tier 0, no grid). The latter is unreachable (S.3, D2: a tier-0 construction failure
sets `trig$grid_failure`, `v3_calib.R:82`, so `fired` is true (`:154`) and the loop escalates (`:158`), unless the escalation
preflight stops, which (E2) excludes). For the former: a tier-1 tier without a grid had some failed construction,
which set `trig$grid_failure` (`:82` for the preliminary build, `:114` for a rebuild); with `grid_fallback = TRUE`
(`v3_fit.R:150-151`, CONFIG) `v3_cal_tier` records `fallback_grid` (`v3_calib.R:122-125`): the last successful
construction `g` if `g$ok` — after a failed rebuild `g` still holds the last successful build, because `g <- gn` is
executed only after `gn$ok` (`:114-116`) — and otherwise the tier's pilot schedule `pil$schedule` (the preliminary
build failed). By DLV Lemmas 3.3, 3.4 both start at exactly 0, end at exactly 1 and are strictly increasing with
finite entries and ≥ 2 points, so `v3_check_grid` (`v3_run.R:77-82`) passes; the fallback branch `v3_calib.R:163-168`
(conditions: status "ok", no grid, e = 1, fallback on, fallback recorded, check passes) then installs it, the status
stays "ok", and `v3_frozen` (`v3_run.R:68-76`) accepts it. (The pilot itself returned status "ok": otherwise the tier
would have failed through `fail()`, `:57`, with `numerical_failure` or `resource_limit`, excluded by (E2), (E3).) So
`schedule_limit` does not occur. This is Proposition F's fallback (DLV `L4_delivery.md:79-91`; FIN `s6_delivery.tex:31`)
as implemented (C-ENG:Impl-DLV-B; checked here against the code).

**(E5) LS0 representability guards** (new since 39db138). `v3_run.R:95-97` rejects `le` unless it is a finite whole
number in [0, 1e6]; with the default `le = b$ell = ℓ_n` (`v3_run.R:95`; no option set, CONFIG) it is a non-negative
integer, so only the upper-bound predicate `le > 1e6` can fire, and it is lifted by IDEAL-W⁺ (or false on 𝔇: ℓ_n =
⌈log₂(n + p + 1)⌉ ≤ ⌈log₂(n + p_raw + 1)⌉ ≤ 10⁶). `cpp/v3_core.cpp:473-474` rejects `o.ls0_ell < 0` (false: ℓ_n ≥ 0)
or `cap_ll > INT_MAX`; cap_ll = ℓ_n + |S̃₀| ≤ ℓ_n + K ≤ ⌈log₂(n + p_raw + 1)⌉ + ⌊n/2⌋, so the second predicate is lifted by
IDEAL-W⁺ (or false on 𝔇). The `as.integer(le)` conversion (`v3_run.R:98`) is exact under IDEAL-W (unbounded integers),
and on 𝔇 because le ≤ 10⁶.

**(E6) Start-mode throws** (new since 39db138). `cpp/v3_start.h:272` (tie DP requires cap ≥ 2): the production call
passes cap 10⁶ (`cpp/v3_core.cpp:469`), so it cannot fire. The tie-DP throw "no tight path" (`cpp/v3_start.h:261`, C-ENG 9b9d234): by Lemma E4, on every accepted input (cap ≥ 2 when `tie_dp` is true) and under
EX-A for the routine's arithmetic, `start_mode` returns a maximiser of γ₀ — in particular it returns, so no throw occurs.
The enumeration cap 10⁶ (`cpp/v3_start.h:290, 303`: truncation, then `mode_tie_dp`) only switches to the DP; it is not an exit.

**(E7) Other fixed thresholds on the call graph** (not exits on valid inputs): block width 1..16 (`cpp/v3_core.cpp:146`,
called at `:274`): production B = min(⌊√n⌋, ⌊√p⌋, 16) ∈ [1, 16] for n ≥ 3, p ≥ 1 (`v3_preprocess.R:19-33`); the
supplied-block validator `cpp/v3_core.cpp:148` is not on the production setup path; snapshot thresholds
`v3_calib.R:19` affect archives only; local-search and grid-interval caps are size-dependent budgets (Lemma R.1).
The R-level helpers that `stop` on malformed internal objects (`cpp/v3_core.cpp:18-55, 212-257, 393, 425, 578`) check
invariants of objects the production path constructs itself (pointers, retained indices, block coverage, table
lengths, `|S| ≤ K`, equal-length vectors); they are part of the inherited P1/S.3 audit and are unreachable on the `v3_fit` path (each object is built by the preceding production call with the property checked). Likewise `nth_nonmember out of range`
(`cpp/v3_engine.h:143`) is excluded by DLV S.3(v) (`L2_degenerate.md:53`) [LCB-2].
**MACH exits [LCB-1].** Three kinds of call-graph exit are not mathematics and are excluded by the premise MACH
exactly as stated in DLV `STATEMENT.md:28-31` ("every heap, stack and worker allocation succeeds whenever the live bytes
stay within the declared memory …; the build, its lock/cache and runtime dependencies (Rcpp, digest) succeed; no
user/external interruption, no worker crash"), and are recorded in the inherited P1 inventory: (i) user interrupts, e.g.
`Rcpp::checkUserInterrupt()` during exact enumeration (`cpp/v3_core.cpp:552`; the catch at `:556` handles only
`NumericalFailure`) — excluded by "no user/external interruption"; (ii) runtime-dependency failures, e.g.
`digest::digest()` in `v3_frozen` (`v3_run.R:73`) and the Rcpp build/load — excluded by "runtime dependencies (Rcpp,
digest) succeed"; (iii) allocation failures anywhere (preprocessing, context construction, setup tables, calibration,
final run, serialisation of the fit) — excluded by MACH's allocation clause together with the memory envelope of 𝒜_n
in (E2) (live bytes ≤ β·(words held) + β₀ ≤ declared memory, by Lemma R's word bound).

**(E8) The final run and LS0.** `v3_final_run` (`v3_run.R:223-229`, assembling through `v3_assemble_final`, `:119-221`): its only non-"completed" statuses are
`resource_limit` (E2) and `numerical_failure` (E3) (`cpp/v3_core.cpp:413-486`); a completed LS0 that stops at its move
cap returns output (`v3_run.R:188`, "a completed LS0 capped at its move limit returns output"); GUARD-W's NA-estimate
rewrite (`v3_unavailable_estimates`) is applied only on returns without complete output (`v3_fit.R:85`, `v3_run.R:143-147`).
On "completed", `v3_assemble_final` sets `estimates_available = TRUE` (DLV `L4_delivery.md:39`; at the pin
`v3_run.R:218`), and `v3_fit` copies it (`v3_fit.R:171`) and returns.

**Conclusion.** For a valid non-degenerate input satisfying 𝒜_n, every branch of the walk either returns with
`estimates_available = TRUE` (exact branch at (E3); SMC branch at (E8)) or would pass through an exit that (E1)–(E7)
exclude, for every seed and every realisation of the uniforms (none of the exclusions depends on them: (E1) is about
the input, (E2) holds for every realisation by Lemma R / Corollary R, (E3)–(E7) are deterministic under EX-A, and the MACH exits of (E7) are excluded by premise for every run). With DLV's
IDEAL-W only, (E5) is the only place where IDEAL-W⁺ was used, and on 𝔇 it is not needed. ∎

## 3. Remarks

1. **Law-free.** No step uses a data law or a design class. Under a law for which the input is valid and non-degenerate
   a.s. (Settings F and R; `Q4_core_plus.md` (c⁺)), P(𝒰_n) = 0.
2. **v3.2.** The allocation 𝒜_n (Lemma R, Corollary R and the A1/A4 preflight terms) refers to the code as pinned; when
   v3.2 freezes, the preflight charge changes and Lemma R and 𝒜_n must be re-audited (STATEMENT (C-D) scope note).
3. **What is audited, not proved.** The completeness of the exit list rests on the inherited P1 inventory and S.3
   ("AUDITED (code reading)") plus the re-reading of the C-ENG changes in (E5)–(E8) by this seat; a code-reading claim of
   completeness, not a machine-checked one.
