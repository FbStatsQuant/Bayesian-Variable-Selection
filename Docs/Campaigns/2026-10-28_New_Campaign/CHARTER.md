# New Campaign: charter (read this first; binding for every thread)

Owner: HQ (thread "Headquarters", <thread>). Approved by Felipe on 2026-10-28. Under the Miscellaneous protocol: no protocol machinery, HQ's own plan. Big picture: `ROOT/00_Admin/CAMPAIGN_PLAN_20261028.md`.

ROOT = `<OLD_ROOT>`.

## 1. Goal of this campaign (the experimental phase only)

Run, or rerun, every simulation and benchmark needed for the method we ship (SMC-BVS v3), in both regimes, and process the results.

**Regime H (p ≫ n).** n = 200; p ∈ {500, 1000}; S1–S6; c ∈ {1, 0.5}; 100 replicates.
- **SMC-BVS:** rerun with the patched and instrumented code, so that both regimes run one code version.
- **Benchmarks:** the existing results stand (same datasets), unless the benchmark audit finds a fault.

**Regime L (p ≪ n).** n = 200; p ∈ {20, 30}; S1–S6; c ∈ {1, 0.5}; 100 replicates.
- **Data generation:** exactly as in master Part II (§II.2–II.9). The only changes are p, and the truth size implied by one signal per block of 5:
  - s₀ = 4 at p = 20 (blocks 1–4);
  - s₀ = 5 at p = 30 (blocks 1–5, as in master §II.3).
- **Coefficients:** the first s₀ values of the pattern (1.4, −1.0, 1.8, −1.2, 0.8, −1.6).
- **Placement:** within-block positions cycle (3, 2, 4, 1, 5).
- **Exact reference:** full enumeration of all 2^p models gives the exact posterior (exact Z, PIPs, HPM, MPM, mass on the truth).
- **Comparisons:** SMC-BVS against the exact posterior and against the truth. The 8 primary benchmark methods with their primary rules, adapted to p ≤ 30 only where infeasible, by a written, committed rule.

**Headline questions** (the only things Felipe wants reported):
1. Is Ẑ accurate?
2. Is the HPM accurate: equal to the exact HPM, and equal to the truth?
3. Are the PIPs accurate, both RB and plain?
4. Exact recovery per scenario /100 and pooled /600, for every method.

**Scope of the questions by regime (Felipe, 2026-10-29).**
- **Low p (p ≤ 30):** we track the performance of both the SMC and the BVS. Questions 1–3 are answered against the exact posterior; question 4 against the truth.
- **High p (p ≫ n, i.e. p > 30):** the model space is infeasible to enumerate, so there is no true Z, exact HPM or exact PIP. Only the BVS is assessed, against the truth:
  - recovery /100 and /600 for every method;
  - HPM = truth;
  - PIP-based selection (MPM) = truth, for both RB and plain.
- **Never** present an "Ẑ accuracy" or "PIP error vs exact" result for p ≫ n.

Everything else is collected and stored, not reported.

**Benchmark audit.** If a benchmark performs poorly, a small team checks whether it was our implementation or the method itself.

## 2. Felipe's rules (non-negotiable)

1. **Order, no clutter.** One folder per location, with the same subfolder names everywhere:
   - **Local, non-data** (code, specs, reports): `ROOT/02_Experiments/I_2026-10-28_New_Campaign/`.
   - **Local data** (downloads): `<PC_NOTS_DATA>\New_Campaign\`, downloaded folder by folder as data accumulate.
   - **NOTS home** (10 GB quota, shared with Felipe's other work): `/home/fb31/projects/BVS/New_Campaign/`.
     - Holds code, inputs, manifests, logs and small summaries only.
     - Never create anything else under `/home/fb31/projects/BVS/`.
   - **NOTS bulky transient outputs:** `/scratch/fb31/New_Campaign/` only. Download them, sha256-verify, then delete. Scratch is purged, so never keep the only copy there.
2. **Disk ceiling.** The home quota is nearly full with Felipe's other material (8.85 of 10 GiB after the pre-campaign clean-up, 2026-10-29). So the campaign keeps its home footprint tiny: at most **0.5 GiB** in `New_Campaign`, for code, manifests and small inputs only. Home usage must stay under **9.6 GiB** in total. Everything else, including logs, goes to `/scratch/fb31/New_Campaign`.
   - Every submission is preceded by a usage check, and a run that would cross the ceiling is refused.
   - Felipe must never have to come back and clean NOTS.
   - **Archive-then-erase (D31, Felipe, 2026-10-30).** HQ owns every NOTS storage decision; Felipe is not asked. When space is needed, or heavy data must go, OPS:
     1. downloads the data to `<PC_NOTS_DATA>\NOTS_home_archive\<what>_<date>\`;
     2. sha256-verifies the copy;
     3. has Sol review the deletion list;
     4. erases it on NOTS;
     5. logs it in `ops/CLEANUP_LOG.md`.
     - **Excluded:** program installs in use, credentials, config, and open files.
     - **Telling Felipe:** HQ mentions what was archived in its next milestone report.
3. **Continuous clean-up.** A run is done only when its outputs are downloaded, verified and removed from NOTS, and its temporary files pruned.
4. **Thorough clean-up before the campaign** (the OPS thread does it first).
5. **No scanning of caches or wasteful folders.** Agents read only the paths their brief names: no R libraries, build caches, `.git`, old experiment folders, or whole-disk searches.
6. **Big runs need evidence.** No large runs on gambles: pilot first, then size the run. More than 10 seeds goes to NOTS.
7. **Felipe sees only results.** Reports are plain and short; details stay in files.

## 3. Standing safety rules

- **Credentials.** Never repeat, store or put in a prompt any password. NOTS key auth works through `~/.ssh/id_rice`.
- **SSH:**
  - **Only the OPS thread opens SSH to NOTS**, with batched commands. At most **two** concurrent connections (D76): one bulk lane for long transfers, one control lane for short commands (each ≤ 5 min, serialised).
  - Use only the configured alias `ssh nots`. It is pinned to the login node that hosts Felipe's live T3 server (loginx2 since 2026-10-28). Never connect to another login node directly, and never touch `~/.claude/remote` or `.t3-recovery`.
  - After a timeout or a reset, back off 15 minutes.
  - Never hold an ssh session open for more than about 1 hour.
- **Truth separation.** Never read sealed truth or holdout folders from fitting code. Truth is used only by scoring, after the fits.
- **Benchmark freeze.** Do not delete, move or chmod anything under `/projects/ml75/fb31/BVS/bench20261019/` or `/home/fb31/projects/BVS/Benchmarks/` until `RELOCATION_OK.md` exists. Reading and copying are fine.
- **Jobs and other users.** Cancel jobs only by explicit ID, and only our own. Never touch other users' files. Never edit T3 databases.
- **Hardware.** Use Sapphire Rapids nodes (`CONSTRAINT=sapphirerapids`) for timing-comparable runs.
- **Local tools.** Python is `py -3`; R 4.4.1 is at `C:/Program Files/R/R-4.4.1`.

## 4. People (model hierarchy)

| Role | Models | Use |
|---|---|---|
| Managers (thread leads) | Opus 5.5 high | Plan, delegate, integrate, decide routine questions |
| Consultants (expensive; hire only for a scoped hard question, with HQ's agreement) | Fable 5.1, Astra (gpt-6-astra) | Delicate judgment or a hard question |
| Reviewer | Sol 6.1 (gpt-6.1-sol, high) | Default independent reviewer. Worker only with a tight brief |
| Workers (cheap labour; most of the volume) | Sonnet 5.5, Terra 6.1, Haiku 5.5, Luna (gpt-6-luna) | Haiku and Luna do clerical work |

- **Spawning workers.** Managers spawn Claude workers with the native Agent tool (Claude Personal), and OpenAI workers or reviewers with `delegate_task`.
- **Briefs.** Every brief names exact paths, inputs, the expected output and an acceptance check.
- **Separation.** Workers never verify their own work.
- **Reviewers on every relevant task (Felipe).**
  - **What needs review:** every deliverable that matters gets an independent review before it counts as done. That covers code, specs, the conformance verdict, cleanup deletion lists, job bundles before submission, scoring outputs and result tables.
  - **Who reviews:** Sol 6.1 is the default reviewer. For numbers-only tie-outs, Terra or Sonnet may review instead.
  - **Record:** the review's verdict and fixes are saved next to the deliverable, in a `review/` subfolder of the thread's area.
  - **Not reviewed:** purely clerical steps (moving a file, listing a folder).

## 5. Shared layout

`ROOT/02_Experiments/I_2026-10-28_New_Campaign/`:

```
CHARTER.md        this file (HQ)
STATUS.md         campaign board (HQ only)
DECISIONS.md      every decision with its reason (HQ only)
conformance/      thread CONF: audit, patch specs, regression evidence
code/             core/ (CONF owns), lowp/, bench_lowp/, scoring/ (LOWP owns); one tree, ledgered in CODE_LEDGER.md
ops/              thread OPS: OPS_LOG.md, NOTS_INVENTORY.md, CLEANUP_LOG.md, DISK_LOG.md, transfer/
analysis/         later: tables and headline answers
bench_audit/      later, only if needed
```

**Data mirror** (local data and NOTS use the same names): `inputs/`, `manifests/`, `results/<run_id>/`, `logs/<run_id>/`.

## 6. Hand-offs

- **Reporting.** Each thread reports to HQ by finishing its task with a compact summary: what was done, file paths, evidence, and open issues.
- **Through HQ only.** Threads do not message each other. Anything that needs NOTS goes through HQ to the OPS thread, as a job bundle: a folder plus a `JOB.md` giving the command, inputs, expected outputs, memory and time requests, and an acceptance check.
