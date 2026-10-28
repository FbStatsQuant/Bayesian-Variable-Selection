# Managing-lead rulings for the deployment (binding on A, B, C, D)

## R-1 (2026-10-22 19:25Z): study adapter mapping, which master §I.7 left OPEN

This is decided before any result is seen. It changes nothing in the method: not the HPM, the primary RB PIP, the evidence or any native diagnostic. It only maps v3 outputs onto the benchmark schema of master §IV.1.2 and the semantics of §III.3.0.

| Field | Rule |
|---|---|
| `method_id` / `rule_id` / `role` | `SMCBVS`; `hpm` → role **primary**; `pip05` → role **S0** (as stated in master line ~2690). |
| `status` | Follows §III.3.0 exactly. `ok`, or `warning` when any R warning or message was captured (stored verbatim), or `failed`. Map the Part I §I.6 statuses as follows. `exact` and `completed` give `ok`, or `warning` when an R condition was captured. `schedule_limit`, `numerical_failure`, `resource_limit` and `invalid_input` give `failed`. `y_constant` and `no_predictors` cannot occur on valid study data; if they do, they give `failed` with the native status kept. A failed rule has support = NA and k = NA. If v3 still returned an HPM or PIP-based support, keep it in `support_audit`. `timeout` and `not_run` are written only by the reconciliation step. |
| `converged` | **NA**, because SMC-BVS is a sampler with no solver convergence criterion. This is the same convention as A3 (MCMC). Schedule completion is already captured by `status`. |
| `diag_flag` | TRUE on both rule rows of a fit iff at least one pre-declared numerical-quality check failed: (a) `checks_passed_final` = FALSE (any of E1–E3 failing on the final islands); (b) `low_empirical_ESS`; (c) `grid_unconverged`; (d) `local_limit`. Nothing else sets it. It never changes `status` or a selection. |
| `diag_codes` | The flag codes of (a)–(d) that fired (`final_check_E1` / `final_check_E2` / `final_check_E3`, `low_empirical_ESS`, `grid_unconverged`, `local_limit`), plus these informational codes, which never set the flag: `escalated`, `cut_group`, `near_tie_truncated`, `forced_pilot_steps`, `exact_branch`, `local_certified_false`, `global_certified`. |
| Native fields | Keep every native v3 status and flag, the per-stage table, log Ẑ (pooled and per island), the full primary PIP vector, the bound labelled heuristic and the timings, as extra columns or in the RDS. |
| `pip_a01…pip_a14`, `max_pip_null` | Filled by the scoring step from the primary RB PIP vector, as for A1. |
| `runtime_s` | The whole fit (master §I.7). |
| `fold_seed` / `fold_sha256` | NA (not used). |

A writes this mapping into the adapter and into HANDOFF_v1.md, together with the exact CSV/RDS schema. B checks it. D scores with it.

## R-2: the root ledger and RUNS.md

- Threads never edit root files.
- Each thread stages append-only candidates in its own folder: `LEDGER_CANDIDATES.md` (CODE_LEDGER rows) and `RUNS_CANDIDATES.md`.
- The managing lead merges them at each gate.
- Individual verification jobs may run without an array; their manifests stay in the thread's folder.

## R-3: Owls resource shares

- **During the build:** A, B and D up to 4 cores each; C up to 4 for tests.
- **During C's batch run:** A, B and D drop to 2 cores each, and C may use up to 10 concurrent fits.
- **Always:** total resident memory ≤ 24 GB, everything at `nice -n 19`, and pause when the 1-minute load is above 40.

## R-4: NOTS

- **The route is repaired.** `ssh nots` goes directly from this PC to loginx3 (no Owls hop); Owls itself is still blocked by NOTS.
- **Build phase:** no NOTS use (Amendment 2).
- **Runs:** after G1, the managing lead writes "NOTS: open for runs" in STATUS.md if NOTS is the run backend. Until then, at most ONE batched read-only call by C, and only if needed.

## R-5 (2026-10-22 20:55Z): G1 CLOSED. A v1 fails B's verdict; repair it as v2

v1 stays frozen and preserved. A builds a separately frozen v2 that fixes ALL of the following (B_verify\VERDICT_v1.md), with Part I governing. No change to the method's statistics.

| ID | Required fix |
|---|---|
| B-A1 to B-A7 | Implement R-1 exactly: role hpm=primary and pip05=S0; `warning` when any R condition was captured; the y_constant/no_predictors→failed mapping, with the empty support kept in `support_audit`; `diag_flag` and `diag_codes` exactly per R-1, including on failed fits (a failure never discards quality flags); for failed fits, keep any returned support in `support_audit`; `fold_seed`/`fold_sha256` = NA; messages stored verbatim (no newline stripping). |
| B-N1 | Numerically stable centring and scaling (two-pass, or compensated) so that near-constant columns standardise correctly. The constant and duplicate tests stay exactly as in Part I. |
| B-N2 | Input validation per Part I: X must be a numeric matrix and y a numeric vector of length n; anything else gives `invalid_input`. No silent coercion. |
| B-O1 | Cache capacity = 500p, as Part I states, in both the run settings and calibration. The prototype's max(500p, 2^15) is not adopted. Cache size never changes results, so the prototype regression still holds. |
| B-O2 | The timing probe must time models of exactly size k*. Fix the stride/deduplication bug. |
| B-O5 | The exact branch records HPM provenance with phase `exact` and mechanism `enumeration`. |
| Rescoring containment | Wrap the two rescoring sites (`cpp/v3_core.cpp:406,656`) so that any scorer failure returns status `numerical_failure` through the normal handler, per Part I §I.2/§I.6. |

**Acceptance:**
- A reruns its own regression suite and the dev smoke fits on v2.
- A publishes HANDOFF_v2.md with a diff summary against v1.
- B then re-runs its full battery on v2, including every reproducer above, and writes VERDICT_v2.md.
- G1 opens only on a PASS.

**B's request 3** (the conditional rescoring gap) is resolved by the containment fix above. No contract exception is granted.
