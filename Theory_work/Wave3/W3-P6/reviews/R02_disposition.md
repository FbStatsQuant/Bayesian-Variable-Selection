# R02 disposition (lead, 2026-11-12) — Sol review of summarize.py v2 → v3

Verdict received: **ACCEPT-WITH-FIXES** (`R02_summarize_v3_sol.md`). No silent mis-count on valid, distinct-tag inputs;
supplied data reconcile (b1 + smk1_v2: 320 / 299 / 21; b2 + smk1_v3: 240 / 4 / 236). All four findings accepted.

| # | sev | finding | disposition |
|---|---|---|---|
| 1 | MAJOR | reused TAG across `--run`/`--rerun` bypasses per-input table membership; origin = rerun tag accepted | fix in v4: reject any repeated TAG; keep per-input table-membership check in addition to owner check |
| 2 | MAJOR | record `run` field not checked against its CLI tag | fix in v4: require `r["run"] == TAG`, else fail closed |
| 3 | MAJOR | one transfer per key: a release of a never-run b2 key uses the only slot, so a later Slurm-kill retry fails closed | fix in v4: explicit attempt chain (`--release` for first execution of never-run / cancelled-before-writing keys; `--rerun` for one retry after a failed attempt); every superseded attempt must have no record; same group and seeds |
| 4 | MINOR | seeds of accepted records not validated | fix in v4: check `data_seed`, `method_seed` against the DESIGN §1 formula for every accepted record |

Timing: v4 is written locally during stage 1 (rule 15: fresh Sol review of the v4 diff) and must pass before any
analysis and before any retry of a stage-1 task is summarized. No run on NOTS depends on summarize.py.
