# C-DLV — inventory of every no-output path (v2 after R01, 2026-11-08 ~21:55)

Scope: sites on the `v3_fit` call graph (`core/v3_fit.R:49-144`) whose firing ends the fit without estimates. Rows
D3–D5 and G1, G3, G4 are listed because they are capped or non-stopping, not because they are exits.

Code = production core `Scripts/SMC_BVS/core/` (abbreviated `core/`), cited by path:line. Spec additions (v3.1 + LS0,
not in the code) cited from the State-of-Project document (`SoP/` = `Theory_work/State_of_Project/sections/`).
"No output" (event 𝒰 = 𝒪ᶜ) = the fit returns with `estimates_available = FALSE` (estimate fields unavailable), or the
process ends without a fit object. A returned "best scored model so far" labelled `hpm_incomplete` is NOT output
(SoP/02_method.tex:585-590, #15).

Classes: (a) deterministic resource use, polynomially bounded; (b) random resource use; (c) statistical / degenerate
event needing a probability bound; (d) excluded by an assumption (named).

## A. Entry, input and preprocessing
| # | path | trigger | code | class |
|---|---|---|---|---|
| A1 | `invalid_input` (seed) | seed not a single integer in [1, 2³¹−1] | core/v3_fit.R:63-64; core/v3_preprocess.R:7-11 | (d) valid seed declared |
| A2 | R error (allocation) | allocation not a list / not finite positive (error thrown, no fit object) | core/v3_fit.R:66-69 | (d) valid allocation declared |
| A3 | `invalid_input` (data) | X not numeric matrix, y not numeric vector, length mismatch, non-finite entry, n < 3, p < 1 | core/v3_preprocess.R:97-107 | (c)/(d): P = 0 under model G (Gaussian, finite) for n ≥ 3, p ≥ 1 |
| A4 | `no_predictors` | every column exactly constant (returns ĥ = ∅ but `estimates_available = FALSE`) | core/v3_preprocess.R:111-114; core/v3_fit.R:74-77 | (c): P = 0 on the classes (columns nonconstant: exact Gram (n−1)Σ, or continuous iid rows) |
| A5 | `y_constant` | all y exactly equal | core/v3_preprocess.R:115; core/v3_fit.R:74-77 | (c): P = 0 (σ² > 0 Gaussian noise) |
| A6 | `degenerate_n` (v3.1 e3, spec only) | n = 1 | SoP/02_method.tex:59-63 | (d) n ≥ 3 |
| A7 | `unsupported_size` (v3.1 e7, spec only) | integer / stream-id / allocation arithmetic overflow | SoP/02_method.tex:59-60, :659 (row 45) | (d) **IDEAL-W** (new premise: no overflow). For any fixed word size it fires for all large n: a fixed machine cannot support growth (same status as EX-A) |

## B. Preflight (deterministic functions of (n, p, allocation))
| # | path | trigger | code | class |
|---|---|---|---|---|
| B1 | `resource_limit` (preflight, SMC) | est. bytes 8(3np+3p²) + tables + convolution + cache + stores + populations > mem | core/v3_fit.R:17-46, :88-90 | (a) |
| B2 | `resource_limit` (preflight, exact) | est. bytes > mem, or (exact count) × (measured s/score) > time | core/v3_fit.R:21-25, :45, :88-90 | (a) for bytes; the time estimate uses a measured s/score: (b)-like, bounded under MACH |
| B3 | `resource_limit` (escalation re-preflight) | tier-1 memory estimate > mem (escalation blocked) | core/v3_fit.R:117-121; core/v3_calib.R:147-148 | (a) |

## C. Numerical failures (scorer)
| # | path | trigger | code | class |
|---|---|---|---|---|
| C1 | `numerical_failure` (exact branch) | NumericalFailure in enumeration | core/cpp/v3_core.cpp:504-524; core/v3_fit.R:95-103 | (d) EX-A |
| C2 | `numerical_failure` (setup / block tables) | NumericalFailure while scoring tables | core/cpp/v3_core.cpp:281-291; core/v3_setup.R:71-72; core/v3_fit.R:107-111 | (d) EX-A |
| C3 | `numerical_failure` (pilot, diagnostics, V rescoring) | NumericalFailure | core/cpp/v3_core.cpp:617-618, :663-664, :685-688; core/v3_calib.R:57, :67, :80, :100, :112 | (d) EX-A |
| C4 | `numerical_failure` (final run) | NumericalFailure | core/cpp/v3_core.cpp:452-453; core/v3_run.R:111-116 | (d) EX-A |
| C5 | scorer throw rule | Cholesky, refactor, augmented QR all fail, or log m non-finite | core/cpp/v3_score.h:226-238 | (d) EX-A: H_S=(n+1)G_S+I and A_S=G_S+I are positive definite and Q_S ≥ yᵀy/(n+1) > 0, so the first route succeeds in exact arithmetic |

## D. Calibration schedule (statistical/algorithmic, random)
| # | path | trigger | code | class |
|---|---|---|---|---|
| D1 | `schedule_limit` | at tier 1, a grid construction (preliminary or any rebuild) fails; tier 1 reached after a tier-0 trigger | core/v3_calib.R:79-82, :111-114, :120, :141-153; core/v3_fit.R:126-132 | **(c)** — the main random path |
| D1a | construction failure reasons | `no_target_above_u`, `non_progress` (two sites), `validation_failed`, `too_many_intervals` (> T_e) | core/cpp/v3_calib.h:68-98 (:76, :86, :90, :92, :94) | (c); under EX-A `no_target_above_u` is unreachable (1 is a target); `too_many_intervals`, `non_progress` (60 halvings) and `validation_failed` at a point snapped to 1 (:89 then :92; counterexample in reviews/R01) are reachable (L3 Lemma 3.4, L4 Theorem D (α)–(γ)) |
| D2 | `grid_failure_no_escalation` | final tier 0 with no grid | core/v3_calib.R:153 | unreachable: a tier-0 grid failure sets a trigger (:82, :114) ⇒ escalation (:145-149) unless B3 fires |
| D3 | grid_unconverged / forced pilot steps / E1–E3 / local_limit | triggers only (escalation); at tier 1 the last grid is used | core/v3_calib.R:59-61, :101-118, :145-146 | not no-output |
| D4 | adaptive pilot stage count | ≤ T_e stages by the floor 1/T_e (deterministic cap) | core/cpp/v3_calib.h:30-46; core/cpp/v3_engine.h:303-341 | (a) count capped; never a stop |
| D5 | rebuild count | ≤ ℓ per tier, ≤ 2 tiers | core/v3_calib.R:85, :141-150 | (a) |

## E. Runtime (wall-clock) guard — stop-only, `resource_limit`, estimates unavailable
| # | checkpoint | code | class |
|---|---|---|---|
| E1 | after every bridge stage (pilot, diagnostic, final islands) | core/cpp/v3_engine.h:335-338; core/cpp/v3_core.cpp:605, :646, :442 | (b): wall time of a run whose operation count is deterministically bounded (Lemma R) ⇒ (a) under MACH |
| E2 | after every local search (pilot, diagnostic, final) | core/cpp/v3_core.cpp:613, :660, :450 | as E1 |
| E3 | after every grid construction | core/v3_calib.R:75-81, :113 | as E1 |
| E4 | guard rule: stop iff elapsed + just-completed operation > allocation (sticky) | core/cpp/v3_runtime.h:21-27 | — |
| E5 | (spec) worker stop, merge stop, LS0 stop (GUARD-W, #6) | SoP/02_method.tex:403-406 | (a)/(b) under MACH; worker crash = (d) MACH |

## X. Process-level and internal (no fit object)
| # | path | class |
|---|---|---|
| X1 | out-of-memory kill (actual peak memory > physical allocation; the code has no mid-run memory check, preflight is an estimate) | (a) with an explicit memory bound (Lemma R) under MACH |
| X2 | internal-invariant `stop()` / `runtime_error` on the `v3_fit` call graph (incl. the equal-length check of `cpp_build_grid`, core/cpp/v3_core.cpp:546, reached via core/v3_calib.R:6, :68 — unreachable since `cpp_cal_V` returns lg0 and d of equal length, :679-683; seed re-checks core/v3_calib.R:137, core/v3_run.R:173 are covered by A1's declared seed; setup `cpp_setup` core/cpp/v3_core.cpp:269-311 incl. block-size check :143-145; inherited-model size :416; frozen-grid check core/v3_run.R:78-80; scorer k > K core/cpp/v3_score.h:230) | unreachable on valid internal state (L2 S.3: call-graph invariant argument); the auxiliary entry points (e.g. core/cpp/v3_core.cpp:109, :209-216) are not on the call graph |
| X3 | compile / environment failure | (d) MACH (binary builds) |
| X4 | user / process interruption: `Rcpp::checkUserInterrupt()` in exact enumeration (core/cpp/v3_core.cpp:520; its catch at :524 handles only NumericalFailure), signals, worker crash | (d) MACH (no external interruption) |
| X5 | allocation exceptions: R allocation errors, C++ `std::bad_alloc` / length errors (preprocessing core/v3_fit.R:72, timing context :12, context/Gram allocation, serialisation of the fit) | (a) under MACH with mem_n ≥ the byte envelope of Corollary R (L1), which counts these objects |
| X6 | build and dependency failures: compile-lock timeout (core/v3.R:55), cache copy failure (:64), missing runtime package `digest` (core/v3_run.R:73) | (d) MACH (build, lock/cache and dependencies succeed) |

## G. Spec-only components (v3.1 + LS0)
| # | path | spec | class |
|---|---|---|---|
| G1 | LS0 move cap reached (`local_limit`) | SoP/02_method.tex:404-405, :497-498 | NOT no-output |
| G2 | LS0 operational interruption | SoP/02_method.tex:497 | as E (guard) |
| G3 | start-mode tie enumeration cap 10⁶ → tie-aware DP (e4) | SoP/02_method.tex:499-500, :655 | deterministic, terminates; (a) |
| G4 | stacking R′ = 4k, extra c₄ search, workers/merge | SoP/02_method.tex:365-385, :392-401 | (a) per R′ declared |

## Summary
Under (d)-premises EX-A, IDEAL-W, MACH and valid declared inputs, every path except D1 is either impossible
(P = 0 or unreachable) or deterministic resource use; D1 (`schedule_limit`) is the only random no-output path.
