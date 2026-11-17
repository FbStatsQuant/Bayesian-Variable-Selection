# C1 · Check of C-DLV:P1-Inventory and C-DLV:L2-S3 — PROOF v1 (code reading at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

Reuse. T10 (`Theory_work/Wave3/W3-AUDIT/track_A/T10_P1S3/`, STATEMENT v2.2 / PROOF v2.1, council-bound R2:
`Theory_work/Wave3/W3-AUDIT/track_A/reviews/MANIFEST_R2.txt`) re-audited P1/S.3 at this pin as a new claim (P1′, S.3′).
This item turns that work into a verdict on the two **registered** claims, re-verifies T10's map independently
(grep of 2026-11-16 20:00 CST, below) and adds the call-graph nodes T10 did not name. Where a step is T10's, it is cited
as "T10 §k" (`Theory_work/Wave3/W3-AUDIT/track_A/T10_P1S3/PROOF.md`).

## 1. P1: every exit without estimates is a listed site
**1.1 Returns of `v3_fit`.** `fit` starts with `estimates_available = FALSE` (`v3_fit.R:76-78`). It becomes TRUE only at
`v3_fit.R:129` (exact branch, `e$status == "exact"`) or by copying `fr` from `v3_final_run` (`v3_fit.R:171`), whose
`estimates_available` is TRUE only at `v3_run.R:218`, reached only when `raw$status == "completed"` (`v3_run.R:143-148`
return FALSE otherwise). `finish` (`v3_fit.R:79-87`) never sets it TRUE (`v3_fit.R:85` only blanks estimate fields via
`v3_unavailable_estimates`, `v3_run.R:110-114`). So the returns without estimates are exactly:
| return | status source | row |
|---|---|---|
| `v3_fit.R:89` | seed check `v3_fit.R:88` (its `stop` is caught by `tryCatch`) | A1 |
| `v3_fit.R:99-103` | `v3_preprocess` (`v3_preprocess.R:98-107`, `:114`, `:115`) | A3, A4, A5 |
| `v3_fit.R:117` | preflight `v3_fit.R:114-117` | B1, B2 |
| `v3_fit.R:131` with `e$status != "exact"` | `cpp/v3_core.cpp:536, 556` (only "exact" or "numerical_failure") | C1 |
| `v3_fit.R:134-138` | `cpp_setup` failure (`cpp/v3_core.cpp:284-297`; `v3_setup.R:71-72`) | C2 |
| `v3_fit.R:154-159` | `v3_calibrate`: `resource_limit` (`v3_calib.R:81, 113, 157`), `numerical_failure` (C3 sites), `schedule_limit` / `grid_failure_no_escalation` (`v3_calib.R:163-170`) | E3, B3, C3, D1, D2 |
| `v3_fit.R:173` via `v3_run.R:143-148` | final run status ≠ "completed": `numerical_failure` (`cpp/v3_core.cpp:483-484`) or `resource_limit` (guard: `cpp/v3_engine.h:335-338`, `cpp/v3_core.cpp:451, 459`; LS0 guard `cpp/v3_core.cpp:480`) | C4, E1, E2, E5 |
The pilot/diagnostic guard stops (`cpp/v3_core.cpp:637, 645, 673-680, 692`) reach `v3_fit` through the calibration
status (`v3_calib.R:57, 67, 100`), rows E1, E2 (T10 §1). The sticky guard rule is E4 (`cpp/v3_runtime.h:21-27`).

**1.2 Errors.** Every explicit `stop`, `stopifnot`, `throw`, `checkUserInterrupt` in `*.R` and `cpp/` at the pin
(grep, 2026-11-16 20:00): `v3_run.R:78, 79, 80, 97, 224`; `v3_setup.R:8, 18, 49, 81`; `v3_preprocess.R:9`;
`v3_fit.R:88, 91, 94`; `v3.R:55, 64`; `cpp/v3_score.h:230, 237`; `cpp/v3_start.h:261, 272`; `cpp/v3_engine.h:143`;
`cpp/v3_core.cpp:18, 29, 31, 35, 54, 55, 112, 146, 148, 212, 213, 218, 219, 233, 240, 254, 257, 393, 425, 474, 552,
578`. This is T10 §1's list. Map: `v3_fit.R:88` caught (A1); `v3_preprocess.R:9` the seed check (A1, declared seed);
`v3_fit.R:91, 94` A2; `v3.R:55, 64` X6; `cpp/v3_score.h:237` the `NumericalFailure` (C5, caught into C1–C4);
`cpp/v3_core.cpp:552` X4; `v3_run.R:97` X7; `cpp/v3_core.cpp:474` X8; `cpp/v3_core.cpp:112, 148, 212-219, 233-257` and
`v3_setup.R:18, 49, 81` off the `v3_fit` call graph (T10 §1); all others are internal-invariant sites, X2 (§2).
Implicit errors (Rcpp conversions, `XPtr`, name lookups, base-R shape errors) are the X2-imp class (T10 §2); allocation
failures are X5; process-level events X1, X3, X4, X6 (MACH).

**1.3 Call-graph nodes not named by T10.** `v3_fit` also calls, on every non-early-exit run:
`cpp_runtime_new` (`v3_fit.R:96`; `cpp/v3_core.cpp:764-768`: no stop; an `XPtr` construction), `cpp_dup_components`
(`v3_fit.R:119`; `cpp/v3_core.cpp:746-760`: `get_holder` then O(p²) reads of the Gram `D.G`, which `data_init` always
allocates and fills, `cpp/v3_score.h:44-52`; no stop), `cpp_cut_group` (`v3_fit.R:141`; `cpp/v3_core.cpp:794-818`: `get_holder`, reads of
`D.G` and `st.blk`; no stop), and in `finish` `cpp_runtime_report` (`cpp/v3_core.cpp:777-789`; `runtime_ptr` returns
NULL-safe, `cpp/v3_core.cpp:780`), `cpp_numerical_routes` (`cpp/v3_core.cpp:822-827`) and `v3_peak_memory_kb`
(`v3_fit.R:2-7`, its read wrapped in `tryCatch`). Their only possible errors are `get_holder`'s stop (X2, §2),
implicit conversions (X2-imp) and allocation (X5). None is a new row. (E-note for `C-DLV:L1-R`: the two O(p²) passes
are deterministic work outside any guard checkpoint; their time counts toward the next checkpoint's elapsed time.)

**1.4 Conclusion.** Every return without estimates (1.1) and every error (1.2, 1.3) is in A1–A5, A7, B1–B3, C1–C5, D1,
D2, E1–E5, X1–X8. A6 is not coded (n < 3 is an A3 case, `v3_preprocess.R:99-107`); A7 is spec-only (premise IDEAL-W).
So the P1 claim holds at the pin; its line numbers are re-located by the tables above and T10 §1 (amendment A-1). ∎(C1-a)

## 2. S.3: D2 and the X2 sites are unreachable
Each of S.3's steps (`Theory_work/Wave1C/C-DLV/lemmas/L2_degenerate.md:38-66`) at the pin:
| S.3 step | recorded lines | pin lines | verdict |
|---|---|---|---|
| D2 | `v3_calib.R:153`, `:82, :114`, `:145`, `:148-149` | `v3_calib.R:170`; trigger `v3_calib.R:82, 114`; `fired` `v3_calib.R:154`; stop `v3_calib.R:157`; escalate `v3_calib.R:158` | holds (T10 §2): with status "ok" a tier-0 grid failure escalates, so the final tier is 1 |
| (i) block size | `cpp/v3_core.cpp:143-145` | `check_B` `cpp/v3_core.cpp:146` at `cpp/v3_core.cpp:274`; `check_blocks` (`:148`) off the graph | holds; reason: B ∈ [1, 16] by the code (T2 BLK-a, `track_A/T2_BLK`), not the SoP text (A-5) |
| (ii) setup required | `:390` | `cpp/v3_core.cpp:393`; `has_graph` set `cpp/v3_core.cpp:304` | holds |
| (iii) model validation | `cpp/v3_core.cpp:24-35`, `:413, :425`, size `:416` | `cpp/v3_core.cpp:24-36`; `cpp/v3_core.cpp:422, 434, 493`; size `cpp/v3_core.cpp:425` | holds |
| (iv) provenance enums | `:54-55`, `:427-430` | `cpp/v3_core.cpp:54-55`, reached `cpp/v3_core.cpp:436, 439, 499, 502, 503` | holds |
| (v) `nth_nonmember` | `cpp/v3_engine.h:143`, `:151` | same | holds |
| (vi) scorer k > K | `cpp/v3_score.h:230` | same; local search skip `cpp/v3_engine.h:397` | holds; callers at the pin incl. LS0's local search from S̃₀ ∈ Ω (T10 §2 (vi)) |
| (vi″) grid length, seed re-checks | `cpp/v3_core.cpp:546`, `:679-683`; `v3_calib.R:137`, `v3_run.R:173` | `cpp/v3_core.cpp:578`, `cpp/v3_core.cpp:711-716`; `v3_calib.R:146`, `v3_run.R:225` | holds |
| (vi′) context assertions | `v3_setup.R:8`, `v3_fit.R:91`, `:12` | `v3_setup.R:8`; `v3_fit.R:118`, `v3_fit.R:12` | holds |
| (vii) grid checks, classes | `v3_run.R:78-80`, `:172` | `v3_run.R:78-80`, `v3_run.R:224` | holds; the frozen grid may also be the tier-1 fallback, which passed `v3_check_grid` (`v3_calib.R:164`) |
**New X2-class sites at the pin (amendment A-2), each unreachable:** `get_holder` (`cpp/v3_core.cpp:18`; every fit-path
call passes `ctx` or `setup$ptr`; T10 §2); the `start_mode` exceptions (`cpp/v3_start.h:261, 272`, via
`cpp/v3_core.cpp:469`): `:272` needs cap < 2 and the only call passes 10⁶; `:261` needs k̂ < 0 or a failed root
feasibility check, excluded by T9 (TDP-e) under T4 (ENC) (T10 §2, X9); the implicit-error class X2-imp (T10 §2).
**Erratum sites (viii)–(ix)** (= X7, X8): stops no invariant excludes; excluded by A:IDEAL-W⁺ or 𝔇 as recorded, and
false for every input R can represent: n, p ≤ 2³¹ − 1 (`cpp/v3_core.cpp:92`), so `le` ≤ 32 < 10⁶ and `cap_ll` ≤
32 + 2³⁰ − 1 < 2³¹ − 1 (T10 §2; `Theory_work/Wave3/W3-AUDIT/track_A_X/T14_REP/PROOF.md`). ∎(C1-b)

## 3. Consequence (C1-c)
§1 gives the coverage; §2 gives D2 and the X2 class unreachable. Of the remaining rows, A1, A2 are excluded by the
declared inputs, A3–A5 by DLV-0's non-degeneracy (or by S.1 a.s. on the classes), C1–C5 by EX-A (S.2, whose (vi) caller
list holds at the pin, §2), A7 and X1, X3–X6 by IDEAL-W and MACH, X7–X8 by A:IDEAL-W⁺ or 𝔇 (or R representability),
and B1–B3, D1, E1–E5 are the resource and schedule rows that DLV-0 handles by its own walk (Theorem D, Lemma R,
Prop F; outside this item). D1 is unreachable on the shipped path under EX-A (T10 §3, amendment A-4). So the audits
supply DLV-0's premise at the pin. ∎
