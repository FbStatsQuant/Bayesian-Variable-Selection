# PROTOCOL — SMC - Engineering Department (v1.0, approved by HQ 2026-11-15; HQ approves every change)

Aligned with company handbook v2.0 (main 8a14bff2); the handbook wins on any conflict.
Tailored as a department protocol variant (POLICIES.md §9). Engineering's checks are code tests, gates, overlap validation and benchmarks, not proof
councils.
**Company minimums kept in full:**
- independent review before "validated" or "done";
- restore points and a rollback path;
- a decision log;
- honest labels;
- escalation;
- compute discipline (POLICIES §6).

## 1. Work units and where work lives
| unit | example | where | record |
|---|---|---|---|
| plan / spec document | EXPERIMENT_PLAN, ENGINEERING_SPEC | `Docs/Experiments/P1M/` (repo) | LOG.md; version line in the file |
| code work package | WP1–WP7 of ENGINEERING_SPEC | git worktree `/home/fb31/BVS-wt/eng-<wp>` on branch `exp/P1M-<wp>` | PR to `main` |
| NOTS batch | G0, an exploratory probe, a ladder stage | scripts in NOTS `~/SMC_Engineering_Department/scripts/<batch>/`; heavy data in `scratch/runs/<batch>/<run_id>/` | LEDGER.md row + run manifest |
| local benchmark | kernel micro-benchmark | Owls `/home/fb31/SMC_Engineering_Department/bench/<name>/` | its README + LOG.md |
| decision | D-n | `DECISIONS.md` | HQ confirms |

## 2. Review: how work becomes "done" or "validated"
**Code (every PR to `main`).**
1. Tests in the same PR:
   - unit tests;
   - **golden bit tests** for every kernel claimed bit-identical (T1/T2);
   - **invariance tests** for threads, groups and tiles (T3);
   - CI green.
2. **Independent code review** by a reviewer who did not write the code: an Opus 5.5 helper (a child of the task lead) with a written brief for
   routine PRs; a Sol review via HQ for the engine core (scorer, kernels, streams, merge, calibration), subject to the
   Codex pacing level (POLICIES §2). At level ≥ 1, engine-core PR reviews stay on Sol, but routine PR reviews are
   Opus-only. The verdict and the disposition of each finding are filed in `reviews/`.
3. HQ merges. No self-merge.

**Plan and spec.** The Sol feasibility and budget review at each EXP-CP (commissioned by HQ). Independent expert reviews
(Fable only with approval up the chain, or Opus) for design questions, each with a written disposition (adopt / reject with reason /
defer).

**Experiments, through the gates G0 → G-A → G-B → G-C → G-C2 (ENGINEERING_SPEC §0-v2.6).**
- **Pre-registration:** thresholds, tolerances, seeds, designs, configuration and evaluator are written down and
  hash-frozen **before** the runs they judge. A change after a run is a logged deviation, and the gate is re-run or
  labelled.
- A gate passes only on its declared numbers, read back from the records (sacct + output files), not from logs or memory.
- Every analysis script that turns records into a published table gets an independent review before its numbers are
  quoted as results (as in P6, rule 15).

**Overlap validation (POLICIES §4).** V against the theory's method on the same datasets, with the tolerances of
ENGINEERING_SPEC §0-v2.7. The verdict "validated" also needs an independent review of the comparison (code and tables).

**Benchmarks.** Each number carries: machine, node type, threads, command, date, job id. A measurement replaces a
planning value only after it has been read back and logged.

## 3. Labels (honest, everywhere: docs, reports, tables)
| label | meaning |
|---|---|
| **MEASURED** | read from a record; cite job id or file |
| **ESTIMATE / (guess)** | derived from a model or extrapolated; state the basis |
| **PLANNING VALUE** | an estimate adopted for budgeting; replaced at a named gate |
| **PROVISIONAL** | produced, but not yet independently reviewed |
| **VALIDATED** | passed its pre-registered gate **and** an independent review |
| **DONE** | merged to `main` (code) or accepted by HQ (document or stage) |
| **FAILED / NOT RUN / CENSORED** | stated, never dropped; every submitted fit stays in the denominator |
| output class | [OP-bit] / class A / [OP-law] / [Δ𝒞] / [Δlaw] / "V-1M variant" for every engine change |

1M results are always labelled "engineered variant V-1M, validated against the theorem-covered method on the overlap
rung" (POLICIES §4).

## 4. Rollback and provenance
**Git.**
- Work on department branches only.
- No force-push, no history rewrite.
- A bad change is undone by `git revert` on the branch, or by closing the PR.
- **Tags** at each gate pass: `eng-G0`, `eng-GA`, ….
- `main` changes only by HQ merge, so it can always be rolled back to the last tag.

**Restore points.**
- HQ's 15-minute snapshot of `Docs/Experiments/P1M/`.
- A department commit at every meaningful state: a checkpoint, a gate, a plan version.
- Frozen copies of the code used by each NOTS batch: `scratch/runs/<batch>/code/` holds a `git archive` of the exact commit,
  with its hash in the manifest.

**Run provenance (every NOTS run).** A `manifest.json` written before the first output, containing:
- code commit and binary hash;
- compiler and flags;
- input data hash, or the generator id + seed;
- configuration hash;
- node type;
- Slurm job id;
- the time limit.

Outputs are immutable once published (write to a temporary name, then rename). A re-run gets a new `run_id`, never an
overwrite. A failed or cancelled run keeps its directory and its ledger row.

**Data lifecycle.** Generated data are regenerable from (generator, seed) and checked by hash. Results of record go off
NOTS by the **continuous offload** (POLICIES §6, Storage; `machines/OFFLOAD.md`):
1. checksummed (SHA-256 computed on NOTS) to Owls, then to the **owner's desktop (primary; path from the owner on 11-16)**;
2. mirrored to the laptop when it is online;
3. NOTS scratch is freed only after the Owls and desktop copies are verified.

Nothing of record stays idle in scratch for more than **7 days** (POLICIES §6, Storage; the CRC purge is 14 days on atime).
Nothing of record is deleted without a verified copy, and nothing at a final destination is deleted without the owner's
request.

**Errors found later.** An error in a result already reported gets:
1. a correction entry in LOG.md;
2. a re-run with a new run_id;
3. the affected tables relabelled;
4. a note to HQ the same day.

## 5. Records
- `LOG.md`: heartbeat and every action, with real time.
- `DECISIONS.md`: technical decisions, with HQ confirmation.
- `LEDGER.md`: NOTS core-h per batch (ids, worst case, actual).
- `REQUESTS.md`: the interface to HQ and the Theory Department.
- `reviews/`: review briefs, verdicts, dispositions.
- On each machine, `INDEX.md` in the department folder.

## 6. Escalation (to HQ at once)
- A plan becomes infeasible, or a gate fails.
- A budget overrun, or a re-size beyond the approved envelope; a number moving > 15% after a review (H-1).
- A blocked dependency.
- Anything touching a paper claim (e.g. an overlap tolerance missed).
- A machine incident: Owls root above 95%, or a ±3-point change above 85%; NOTS home above 8 GB; anything that might
  look odd to Rice IT.
- A stray file found outside the department folders.

## 7. Compute discipline (POLICIES §6, summary; the policy text wins)
- Work only inside the department folders.
- SSH multiplexed, sequential.
- Polling ≤ 1 squeue/sacct per 5 minutes.
- Job arrays only; at most 468 concurrent NOTS jobs in total (company-wide).
- `--constraint=sapphirerapids`; Slurm output under `scratch/slurm_out/`; TMPDIR under `scratch/tmp/$SLURM_JOB_ID`.
- Owls: small-scale work only, `nice`, gradual ramp-up; nothing large or multi-day on Owls without HQ's go.
- Exploratory batches ≤ ~200 core-h on HQ's standing authorisation (logged); gated stages and larger batches only with
  HQ's go.
- **Cost honesty (HQ, 11-16).** Before submitting, compare the batch's realistic cost with the figure already given to
  HQ. If the actual may exceed it by more than 50%, tell HQ before submitting, even under the ~200 core-h authority.
  Size every estimate from the slowest measured point, not the builder's guess.
- Daily machines line in the report.


**Owner priority on NOTS (owner, 2026-11-15).** NOTS limits are per *user*: 1,536 CPUs and 2,304 GB for the whole
`fb31` account. Every Engineering job therefore competes with the owner's other projects. When the owner says he needs
NOTS ("clear the way", with how much and how soon):
1. **At once:** no new submissions; pending tasks of ours are held (`scontrol hold`). Reply with what is running: job ids,
   CPUs, memory, expected end, and whether each job is checkpointed.
2. **If he needs the capacity now:** cancel our running jobs that block it, longest-remaining first (`scancel`, owner's
   explicit request). Checkpointed jobs resume later from their last stage. Others are re-run from their manifests under
   new run_ids.
3. **Labels:** these stops are logged as "owner preemption" (LOG, LEDGER), never as failures. The lost core-h are counted
   in the ledger.
4. **Resume** only when the owner says the way is clear: release the holds, resubmit, and report.

Design consequence: Engineering jobs stay short (≤ 6 h where possible), checkpoint at stage boundaries, and keep a
headroom of CPUs under the cap whenever the owner has other NOTS work announced.

## 8. Changes to this protocol
Proposed by the Engineering manager, approved by HQ, recorded in the changelog below.

## Changelog
- v1.0 (2026-11-15) — first version; submitted to HQ with EXP-CP1 v2. Includes the owner-priority rule for NOTS (owner, 11-15).
- v1.0 approved by HQ 11-15, with two edits folded in: §4 data lifecycle → continuous offload (desktop primary, laptop mirror, NOTS freed after verification, 7-day rule); §2 Sol reviews subject to the Codex pacing level (POLICIES §2; at level ≥ 1 routine PR reviews are Opus-only).
- v1.1 (2026-11-16) — §7: cost-honesty rule (HQ, after the WP3 SPR sweep cost 77.4 core-h against the stated ≈ 40).
- v1.2 (2026-11-16) — old POLICIES §14, now §7 (HQ): Codex/sandboxed agents never set TMPDIR or write outside their own worktree (scratch in a git-ignored `.rc_tmp/`); runs over 2 h get a pending-request check. Folded into briefs/BUILD_COMMON.md.
- v1.3 (2026-11-28) — aligned with company handbook v2.0 (main 8a14bff2): POLICIES section references re-pointed; NOTS cap now 468 concurrent jobs in total; Owls rule now "nothing large or multi-day without HQ's go".
