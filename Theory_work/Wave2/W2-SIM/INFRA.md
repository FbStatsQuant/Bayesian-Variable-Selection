# W2-SIM — NOTS infrastructure and rules (binding for every W2-SIM family lead)

Lead: W2-SIM (Claude Opus 5.5, Claude Work). Set 2026-11-09.

## Protocol
`Theory_work/Wave2/PROTOCOL.md` (extends Wave1C and Wave1 PROTOCOL.md) applies: no claim without a file; every number
traces to a script + output file; statuses copied verbatim (never upgraded); reviewers briefed to break, never given
our conclusion; every review is a fresh `delegate_task` (Codex `gpt-6.1-sol`, reasoningEffort high) recorded verbatim
in `reviews/`. Empirical trends are evidence, never limit proofs. No git state changes (HQ commits). Write only inside
`Theory_work/Wave2/W2-SIM/` (your family folder + `results/<family>/` + `reviews/`).

## NOTS (binding)
* `ssh nots` (BatchMode, user fb31, Slurm). Workspace ONLY `/home/fb31/projects/BVS/theory_w2/` and
  `/scratch/fb31/theory_w2/`. **Never touch** `/home/fb31/projects/BVS/SMC_BVS_v3/deploy/`, `/projects/ml75`, or any
  other existing run/file.
* Code deployed (read-only except the core's `.cpp_cache`):
  - `/home/fb31/projects/BVS/theory_w2/code/main_11dc9b7/repo/` = `git archive` of main @ 11dc9b73416dacb9f159846d39902d4b57b49a57
    (production core `Scripts/SMC_BVS/core` identical to the v3.1 merge 4676af6; plus W2-FAC-A/B, W2-APP/data_diag,
    W2-LOC2 numerics). sha256 list: `code/main_11dc9b7.SHA256SUMS`.
  - `/home/fb31/projects/BVS/theory_w2/code/tickets_20261109T0943/Theory_work/Wave2/<TICKET>/numerics/` = snapshot of
    the (untracked) numerics scripts of W2-FAC-PK, -PKA, -S5, -X, -XA taken 2026-11-09 09:43 (no data files).
    sha256 list: `code/tickets_20261109T0943.SHA256SUMS`. If you need a newer ticket script, upload a new snapshot dir
    `code/tickets_<timestamp>_<family>/` with its own SHA256SUMS and cite it in your manifest.
* Environment: every job sources `sim/env_sim.sh` (= production `env.sh`: GCC 14.3.0, R 4.5.2, one thread, module R
  library; plus `SciPy-bundle/2025.07`: Python 3.13.5, numpy 2.3.2, scipy 1.16.1; PYTHONDONTWRITEBYTECODE=1).
* Submission: `sim/submit_table.sh RUN_ID TASKS_TSV SCRIPTS_DIR PARTITION TIME MEM THROTTLE` (run on the login node
  from `/home/fb31/projects/BVS/theory_w2/sim`). TASKS_TSV lines: `task_id<TAB>shell command`; the command runs from the
  frozen `runs/RUN_ID/scripts/` copy of SCRIPTS_DIR with env vars `$OUT` (= `/scratch/fb31/theory_w2/RUN_ID`),
  `$CODE` (main archive repo root), `$TICKETS` (ticket snapshot root), `$RUN_DIR`. Write raw output to `$OUT/raw/`.
  Per-task logs: `$OUT/log/task_<id>.log`, `starts.jsonl`, `ends.jsonl` (rc, wall). The script writes
  `runs/RUN_ID/manifest.json` (commit, sha256 of every frozen file, sbatch args, job id). Never reuse a RUN_ID.
  Prefix your RUN_IDs with your family tag (e.g. `s5cc_...`).
* Partitions: `commons` (≤ 24 h) or `scavenge` (≤ 1 h, preemptible: use for short tasks only, and rerun preempted
  units). 1 CPU per task. Sensible `--time`/`--mem`. **Throttle: your family's concurrent tasks must stay within your
  allotment** (given in your brief; W2-SIM total ≤ 150). Check `squeue -u fb31` / `sacct -j JOB` for failures; rerun only
  failed units (new RUN_ID with only those tasks, or same scripts with a filtered TASKS_TSV).
* Python scripts that import ticket modules: put `sys.path.insert(0, os.environ["TICKETS"] + "/Theory_work/Wave2/<T>/numerics")`
  (or copy the module into your scripts dir and record its sha256 against the snapshot). Never modify ticket sources;
  if a fix/optimisation is needed, write a new module in your scripts dir and **validate it against the original on
  small cases** (save the validation output).
* Pull back only summaries (+ compact per-seed raw JSONL/CSV if small, ≲ 20 MB per family) to
  `Theory_work/Wave2/W2-SIM/results/<family>/`. Record NOTS job ids in your family REPORT.

## Production core (v3.1) — driver `scripts/prod_fit.R` (W2-SIM lead)
`Rscript --vanilla prod_fit.R $CODE/Scripts/SMC_BVS/core OUT.jsonl RDS_DIR key=value...` — designs `excs` (exact-Gram
CS), `iidcs`, `iidfac`; `arm=mr1` (merged cap ℓ_n + |S̃₀|) or `arm=dbl` (testing option `v3.ls0_ell = ℓ_n + K` ⇒ cap
ℓ_n + K + |S̃₀|); `hours` = allocation (preflight / runtime guard). Records status, HPM, hpm_before_ls0, LS0 path
decomposition, first LS0 scan that scores S₀, preflight estimates, timings. Production fits are run by the W2-SIM lead
unless your brief says otherwise; ask the lead for designs you need.
