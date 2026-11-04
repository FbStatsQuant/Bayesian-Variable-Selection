# PLAN: method-fidelity audit, then c = 0.5 production (2026-10-21)

Protocol: Miscellaneous operations (`misc.md`). The task reruns existing, verified pipelines with one setting changed (scale c050), after an audit; no new method is designed.

## Goal (from the person, 2026-10-21)

1. Before any new production: agents check that each benchmark's code holds and reflects the actual published method.
2. Once confirmed: rerun all eight benchmarks (F1–F5, A1–A3, with their variants F4_SCAD, SuSiE-L100, SSL-RS) at c = 0.5 only: 1,200 datasets per method (600 at p = 500, 600 at p = 1000), same sealed inputs (`Y[, "c050"]`), same X, ε, folds, seeds and truth as the c = 1 runs.
3. At most three methods in flight at once, about 400 concurrent NOTS tasks in total.

## Phase 1: audit (in parallel)

| Piece | Who | Machine | Output | Acceptance |
|---|---|---|---|---|
| P0 Exact package sources | lead (one scp; hashes match `environment_manifest.txt`) | local | `C:/Users/felip/Documents/bench_refs_20261021/pkgs/` | 7 sha256 match (done) |
| P1 Method papers | Sonnet agent | local | `bench_refs_20261021/papers/` + `INDEX.md` | each PDF opens, first-page title matches |
| P2 Fidelity audit, one per method (8) | Opus 5.5 high, F1–F5 on CW, A1–A3 on CP (other account than the code's author) | local only, no NOTS | `verify/fidelity_c050/<method>/REPORT.md` | verdict + findings with file:line, paper section, package source line evidence |
| P3 c050 infrastructure + pilot, F1–F5 | Opus 5.5 high thread (CP) | NOTS | new code copies `/home/fb31/projects/BVS/Benchmarks/<method>/c050/`; report | infra-only diff; c100 rerun bit-identical to production on 3 datasets; 12-dataset c050 pilot: 0 failures, diagnostics, runtime, memory |
| P4 same for A1–A3 | Opus 5.5 high thread (CW) | NOTS | same | same |
| P5 Judge | Fable 5.1 (Plan type, read-only, condensed dossier) | — | `verify/fidelity_c050/FABLE_JUDGE.md` | ruling per finding: fix before c050 / document / ignore |

- P3/P4 change infrastructure only: the scale key passed to `run_case` and the chunking (400 tasks × 3 datasets per method, `%133`). Fit functions, hyperparameters, rules and diagnostics are untouched; the diff against the c = 1 production snapshot is in the report.
- The engineers prepare the pilot and reproduction submissions; **the lead submits them** (STANDING RULES). The pilot reports diagnostics only; nobody computes recovery from the pilot, and no setting is changed on the basis of recovery.
- A confirmed BLOCKING fidelity finding means a core-code fix, re-verification, and a rerun of that method at c = 1 as well; the person is told before production.

## Phase 2: c050 production

- Rolling pool of three methods: start A3, F3, A1 (longest); as each one finishes, start the next of A2, F4, F5, F1, F2.
- Each run: frozen snapshot + `manifest.json`, `RUNS.md` row, run id `<stamp>_bench20261019_prodc050_<method>`.
- After each run: post-run audit by its engineer; scoring by S (thread mcp:234128fe…); independent recount G9 by R (Sol, mcp:72dd7e8d…); reproduction G5 on 12 datasets per method by VF (Sol) / VB (Opus CW). Post-hoc K37 rows derived for F4/F5 as at c = 1, labelled post hoc.
- Final: table like the c = 1 one (exact recoveries by scenario × p), plus paired c = 1 vs c = 0.5.

## NOTS discipline

One SSH connection per agent at a time, `timeout 90` on every SSH call, commands batched, job checks at most every 10 minutes, no watch loops. Concurrency limit per user on commons: cpu=1536, mem=2304G (checked 2026-10-21); 400 × 3 GB = 1.2 TB.

## Data and outputs

Inputs, truth, results, scoring: `$STUDY=/projects/ml75/fb31/BVS/bench20261019` on NOTS. Local references: `C:/Users/felip/Documents/bench_refs_20261021/`. Reports: `verify/fidelity_c050/`, `thread_briefs/`.

## Agents (budget)

Sonnet 1 (P1); Opus 8 (P2) + 2 threads (P3, P4); Fable 1–2 (P5). Phase 2 reuses S, R, VF, VB threads.

## Pre-declared decisions (recorded before any c050 output is seen)

- **D-c050-1 (A3 MCMC budget, 2026-10-21, after FA-A3 finding A3-1).** The A3 budget stays as at c = 1 (10,000 burn-in + 15,000 kept, thin 5) for every scale, so c = 1 and c = 0.5 stay paired. Any budget change would apply to all scales and re-run c = 1 too. ESS flags (`ess_tau`, `ess_ci95`) are reported per scenario × p in production, with results on all fits and on passing fits. If flagged fits are concentrated in some cell, a longer-chain sensitivity rerun of the flagged fits (both scales) is reported beside the main result, never substituted for it. Rejected: per-scenario O10 rule on the 12-dataset pilot (one fit per cell cannot estimate a per-scenario rate).
- **D-c050-2 (fidelity findings).** Findings that change no selection (runtime settings, documentation) are recorded and fixed in the master text, not in code. Code changes only for BLOCKING findings, or MATERIAL ones the lead accepts after the Fable ruling.
