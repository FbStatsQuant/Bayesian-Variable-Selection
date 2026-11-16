# T10 · Re-audit P1/S.3 — PROOF v1 (second-seat code reading at pin 4676af6; paths relative to `Scripts/SMC_BVS/core/`)

Method: (1) list every `stop`, `stopifnot`, `throw`, `checkUserInterrupt` in `cpp/` and `*.R` (grep, 2026-11-16) and
every assignment of a non-success status reaching `v3_fit`; (2) keep those on the `v3_fit` call graph; (3) map each to an
INVENTORY row and re-locate its lines; (4) re-check each S.3 invariant against the code at the pin.

## 1. Exit map (INVENTORY row → pin lines)
| row | exit | pin lines | note |
|---|---|---|---|
| A1 | `invalid_input` (seed) | `v3_fit.R:88-89`; `v3_preprocess.R:7-11` | excluded by the declared seed |
| A2 | R error (allocation) | `v3_fit.R:91-94` | excluded by the declared allocation |
| A3 | `invalid_input` (data; incl. n < 3, p < 1) | `v3_preprocess.R:99-107`; return `v3_fit.R:99-103` | A6 (`degenerate_n`) is not coded; n < 3 is here |
| A4 | `no_predictors` | `v3_preprocess.R:111-114`; `v3_fit.R:99-103` | |
| A5 | `y_constant` | `v3_preprocess.R:115`; `v3_fit.R:99-103` | |
| A7 | `unsupported_size` | not coded (spec only) | premise IDEAL-W |
| B1, B2 | preflight `resource_limit` | `v3_fit.R:26-68, 115-117` | with `ls0_worst_case` on by default (`v3_fit.R:114`) |
| B3 | escalation re-preflight | `v3_calib.R:157`; `v3_fit.R:144-148, 154-159` | |
| C1 | exact-branch `numerical_failure` | `cpp/v3_core.cpp:556`; `v3_fit.R:122-130` | |
| C2 | setup tables | `cpp/v3_core.cpp:284-297`; `v3_setup.R:71-72`; `v3_fit.R:134-138` | |
| C3 | pilot, diagnostics, V | `cpp/v3_core.cpp:649-650, 695-696, 717-721`; `v3_calib.R:57, 67, 80, 100, 112` | |
| C4 | final run (islands, final search, LS0) | `cpp/v3_core.cpp:483-484`; `v3_run.R:143-148` | LS0 is inside the same `try` (`cpp/v3_core.cpp:417-482`) |
| C5 | scorer throw rule | `cpp/v3_score.h:226-238` | EX-A: never (L2 S.2) |
| D1 | `schedule_limit` | `v3_calib.R:163-170`; `v3_fit.R:154-159` | see §3 |
| D2 | `grid_failure_no_escalation` | `v3_calib.R:170` | unreachable, §2 |
| E1 | bridge-stage guard | `cpp/v3_engine.h:335-338`; `cpp/v3_core.cpp:637, 673-680, 451` | T1 GW |
| E2 | local-search guard | `cpp/v3_core.cpp:645, 692, 459` | T1 GW |
| E3 | grid-construction guard | `v3_calib.R:75-81, 113` | T1 GW |
| E4 | guard rule (sticky) | `cpp/v3_runtime.h:21-27` | |
| E5 / X10 | LS0 guard stop (now coded) | `cpp/v3_core.cpp:480` (gate `cpp/v3_core.cpp:465`) | T1 GW; no-output by `v3_run.R:143-148` |
| X1, X3, X5 | OOM kill, environment, allocation exceptions | — | MACH |
| X2 | internal invariants | §2 | unreachable |
| X4 | user interrupt | `cpp/v3_core.cpp:552` | MACH |
| X6 | build lock / cache / `digest` | `v3.R:55, 64`; `v3_run.R:73` | MACH |
| X7 | LS0 base-cap validator | `v3_run.R:95-97` | A:IDEAL-W⁺ or 𝔇 (erratum) |
| X8 | LS0 cap-range guard | `cpp/v3_core.cpp:473-474` | A:IDEAL-W⁺ or 𝔇 (erratum) |
| X9 | `start_mode` exceptions (new) | `cpp/v3_start.h:261, 272`, via `cpp/v3_core.cpp:469` | unreachable, §2 |

Every other `stop`/`throw` in the core is off the `v3_fit` call graph: `cpp/v3_core.cpp:112` (`cpp_score`),
`cpp/v3_core.cpp:148, 212-219` (`cpp_start`), `cpp/v3_core.cpp:233-257` (start inspection helpers),
`v3_setup.R:18, 49, 81` (inspection wrappers). Non-success statuses reaching `v3_fit`: `invalid_input`,
`no_predictors`, `y_constant`, `resource_limit`, `numerical_failure`, `schedule_limit`, `grid_failure_no_escalation`
(the statuses set at the lines above; `v3_fit.R:89, 100, 117, 122, 135, 155`; `fr$status` copied at `v3_fit.R:171`). Each
row above is one of them or an error without a fit object. So (P1′) holds.

## 2. S.3 invariants at the pin
- **D2** (`v3_calib.R:170`): needs status "ok", the last tier without a grid, and e = 0. A tier has no grid iff a
  construction failed (`out$grid` NULL iff `trig$grid_failure`, `v3_calib.R:126`; set at `v3_calib.R:82, 114`); then
  `fired` is TRUE (`v3_calib.R:154`) and with e = 0 the loop either escalates (`v3_calib.R:158`) or stops with
  `resource_limit` (`v3_calib.R:157`). So with status "ok" the final tier is 1: unreachable.
- **(i)** `check_B` (`cpp/v3_core.cpp:146`, called at `cpp/v3_core.cpp:274`): B ∈ [1, 16] by T2 (BLK-a).
  (`check_blocks` is called only in `cpp_start`.)
- **(ii)** `setup required` (`cpp/v3_core.cpp:393`): `has_graph` is set by `cpp_setup` (`cpp/v3_core.cpp:304`), and
  `v3_final_run` runs only after a successful `v3_setup` (`v3_fit.R:133-138, 162`).
- **(iii)** `to_internal` validation (`cpp/v3_core.cpp:24-36`) on inherited models (`cpp/v3_core.cpp:422`) and the
  inherited HPM (`cpp/v3_core.cpp:434, 493`): they were exported by `models_to_list` / `to_orig` from internal models of
  the same context (`cpp/v3_core.cpp:735`, `hpm_now` `cpp/v3_core.cpp:616-619`), i.e. sorted distinct retained indices; the
  size check (`cpp/v3_core.cpp:425`) passes since calibration models lie in Ω (W3-SAMP CC5).
- **(iv)** `phase_index` / `mech_index` (`cpp/v3_core.cpp:54-55`, reached at `cpp/v3_core.cpp:436, 439, 499, 502, 503`):
  the provenance strings were produced by `event_to_list` from the same enums, so the lookup succeeds.
- **(v)** `nth_nonmember` (`cpp/v3_engine.h:143`): called with ⌊u(p − k)⌋ < p − k = the number of non-members
  (`cpp/v3_engine.h:151`), and `set_model`/`add_var`/`del_var` keep `bits` consistent with `S` (`cpp/v3_engine.h:80-85`).
- **(vi)** scorer k > K (`cpp/v3_score.h:230`): every caller passes |S| ≤ K (Gibbs `add_ok`, swaps preserve size, π₀
  draws, tables |U| ≤ B ≤ K, local search skips additions at K `cpp/v3_engine.h:397`, inherited size check).
- **(vi″)** `cpp_build_grid` equal length (`cpp/v3_core.cpp:578`): `cpp_cal_V` fills `lg0`, `d` with one entry per model
  of V (`cpp/v3_core.cpp:711-716`) or returns a failure status that `v3_calib.R:67, 80, 112` intercepts first. Seed
  re-checks `v3_calib.R:146`, `v3_run.R:225` pass by A1.
- **(vi′)** `v3_context` assertions (`v3_setup.R:8`), from `v3_fit.R:118` and the timing context (`v3_fit.R:12`):
  `kept` is increasing (`which`, `v3_preprocess.R:112`), lengths match, the timing submatrix keeps these properties.
- **(vii)** grid checks (`v3_run.R:78-80`), reached from `v3_frozen` (`v3_calib.R:186`) and `v3_final_run`
  (`v3_run.R:225`): the frozen grid is a successful construction (C-DLV L3 Lemma 3.4: starts at 0, strictly increasing,
  ends at 1) or a fallback that passed `v3_check_grid` (`v3_calib.R:164`); class assertions `v3_run.R:224` hold for
  objects built by `v3_setup` / `v3_frozen`.
- **X9 (new).** `cpp/v3_start.h:272` needs cap < 2; the only call passes 10⁶ (`cpp/v3_core.cpp:469`).
  `cpp/v3_start.h:261` needs k̂ < 0 or no tight path from (J, k̂): impossible by T9 (TDP-b) "E ≠ ∅" under T4 (ENC).
- **X7, X8** are reachable on very large inputs and excluded only by A:IDEAL-W⁺ or 𝔇, as the erratum says
  (`Theory_work/Wave1C/C-DLV/INVENTORY.md:83-93`); confirmed at `v3_run.R:95-97` and `cpp/v3_core.cpp:473-474`.

## 3. D1 at the pin
`v3_cal_tier` records a fallback only when `grid_fallback` and `trig$grid_failure` and tier = 1 (`v3_calib.R:122-125`):
the last successful construction g (if `g$ok`) or the tier's pilot schedule. `v3_calibrate` uses it when status is "ok",
the last tier has no grid, e = 1, and `v3_check_grid` passes (`v3_calib.R:163-169`); only otherwise does
`schedule_limit` follow (`v3_calib.R:170`). A successful construction starts at 0, increases strictly and ends at 1
(C-DLV L3 Lemma 3.4). The pilot schedule is {0} followed by the pilot's φ values (`cpp/v3_core.cpp:636`): each step of
`pilot_next_phi` (`cpp/v3_calib.h:30-46`) returns 1.0, or lo with lo − φ ≥ 1/T_e > 0, or min(1, φ + 1/T_e) snapped to 1
within 10⁻¹², so the values increase strictly; the adaptive loop stops exactly when φ = 1.0 (`cpp/v3_engine.h:310`).
So `v3_check_grid` passes and D1 does not occur on the shipped path (EX-A; the pilot schedule's monotonicity also holds in
binary64 by the same three cases). ∎

## Re-audit verdict
P1 and S.3 hold for the code of record after re-location, with two additions (X9 unreachable; X10 = the coded LS0 guard,
a resource path covered by T1) and one correction of emphasis (D1 is unreachable on the shipped path with the tier-1
fallback; the INVENTORY summary predates the fallback).
