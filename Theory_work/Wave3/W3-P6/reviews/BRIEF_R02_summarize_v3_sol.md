# R02 — rule-15 review of the summarize.py v2 → v3 change (W3-P6; reviewer: Codex gpt-6.1-sol, high)

You are an independent reviewer. This is a **blind first read** of a code change to an analysis script. Do not edit any
file except your report. Change no git state. Do not use NOTS or any network resource.

## Context (facts only)
W3-P6 is a simulation study. Each Slurm run (RUN_ID / "tag") has a frozen task table (`TASKS_TSV`, one task per line:
`<id>\t<command with key=value args>`); `rederive.R` writes one JSON line per fit RDS (`DERIVED_JSONL`).
`summarize.py` reconciles scheduled tasks with records and tabulates per-cell outcomes. Policy (DESIGN §5): every
scheduled seed stays in the denominator; Slurm failures are rerun once with the same seeds under a new RUN_ID.
v2 (frozen, sha256 `8011253e…`) aborts when a task key is scheduled in two runs, so a rerun cannot be summarized.
v3 adds `--rerun TAG DERIVED_JSONL TASKS_TSV`: a key in a rerun table moves its schedule from its origin `--run` to the
rerun tag and is then counted once, from the rerun only.

Intended uses (the reviewer should check whether v3 handles them correctly or fails closed):
1. b1 (v2 driver, 320 keys, 298 records) + smk1_v2 (1 key from b1, rerun, 1 record).
2. b2 (240 keys, 0 records) + smk1_v3 (4 keys from b2) + later release runs that take further b2 keys (keys never run
   or cancelled before writing), each key released at most once; a later Slurm-killed release task may need a second
   rerun of the same key.
3. Keys of b2 never released (dropped / deferred cells, budget-cut seeds) stay scheduled under b2 without a record.

## Files (read these; paths absolute)
- v3 (under review): `C:/Users/felip/BVS-wt/W3-P6/Theory_work/Wave3/W3-P6/scripts/summarize.py` (CRLF on disk;
  LF sha256 `ae47e03204741617610b69f992197cd7936d0abf32f192db951dc275539e79ed`)
- v2 frozen: `C:/Users/felip/BVS-wt/W3-P6/Theory_work/Wave3/W3-P6/reviews/R02_inputs/summarize_v2_frozen.py`
- unified diff v2 → v3: `.../reviews/R02_inputs/summarize_v2_v3.diff`
- test data in `.../reviews/R02_inputs/`: `b1_derived.jsonl` (298 lines), `smk1_v2_derived.jsonl` (1),
  `smk1_v3_derived.jsonl` (4), `smk1_v2_tasks.tsv`, `smk1_v3_tasks.tsv`
- frozen task tables: `C:/Users/felip/BVS-wt/W3-P6/Theory_work/Wave3/W3-P6/configs/b1_tasks.tsv`, `.../configs/b2_tasks.tsv`
- `C:/Users/felip/BVS-wt/W3-P6/Theory_work/Wave3/W3-P6/DESIGN.md` (§5 policy) for the estimand/denominator rules

You may run the scripts (python) on copies in your own temporary directory, including synthetic fault cases.

## Questions
1. Is the change correct: each scheduled key counted exactly once; a record accepted only from the run that currently
   owns the key; all misuse (unscheduled rerun key, record in the origin of a rerun key, duplicate, group change,
   table/record order) fails closed? Is v3 output identical to v2 when no `--rerun` is given?
2. Can any input make v3 silently mis-count (a record dropped, double-counted, or attributed to the wrong run/group)?
3. Does it support intended uses 1–3? Where it does not (e.g. a second rerun of one key), does it fail closed, and is
   that acceptable or a required fix before analysis?
4. Anything else in the diff that affects reported numbers.

## Output
Write `C:/Users/felip/BVS-wt/W3-P6/Theory_work/Wave3/W3-P6/reviews/R02_summarize_v3_sol.md`: findings numbered, each
with severity (CRITICAL / MAJOR / MINOR), evidence (line refs, a reproducing input if any), and a suggested fix; then a
final line `R02-VERDICT: ACCEPT | ACCEPT-WITH-FIXES | REJECT`. Reply with the verdict line and a ≤ 10-line summary.
