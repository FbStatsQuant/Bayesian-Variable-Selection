# BENCH F3 v2: production rerun — READY for OPS (resources set, HQ D64, 2026-11-02)

OPS hand-off. Frozen code and freeze values filled; Sol review (R1, R2, narrow check: READY FOR OPS after the dev pilot); dev pilot accepted and resources set by HQ D64 (below). Satisfies D36. This bundle does not authorize SSH by the author. Never write to the frozen study or `/home/fb31/projects/BVS/Benchmarks/`.

## Work, input and allocation

F3 only on the original 1,200 frozen datasets, p=500/1000 × S1–S6 × r001–r100, each at c100 and c050: **2,400 one-CPU fits**. Read only `/projects/ml75/fb31/BVS/bench20261019/inputs/p{0500,1000}/<dataset_id>.rds` and `/projects/ml75/fb31/BVS/bench20261019/manifests/inputs_manifest.csv`; R library `/projects/ml75/fb31/BVS/bench20261019/lib/R452`. Code: `/home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso/`; scratch output root: `/scratch/fb31/New_Campaign`. Run ID: `YYYYMMDDTHHMMZ_bench_f3v2_prod` (seconds also accepted).

Four arrays of 600 tasks each, `1-1199:2%30`, `2-1200:2%30`, `1201-2399:2%30`, `1202-2400:2%30`. One array is submitted at a time; repeat the launcher after the preceding cell is absent from squeue and all 600 task records are terminal in sacct. One CPU bills as two: %30 is 60 billed CPUs. The guard counts **all** fb31 arrays, including this campaign's, and refuses if existing pending/running array concurrency plus the requested throttle exceeds 100 tasks; no recorded arrays are excluded. Count is a snapshot, so OPS coordinates launches. OPS may choose `--throttle N`; any increase must keep all campaign work within 192 billed CPUs and 96 tasks (D47/D49/D50), including PROD-H at 120 billed and PROD-L's applicable ceiling of 68 while PROD-H runs. All use Sapphire Rapids, commons/nots_commons, one CPU, single-thread numerical libraries, GCC/14.3.0, R/4.5.2, glmnet 5.1 and verified absolute-path GNU time.

**Production resources (HQ D64, from the accepted NOTS dev pilot).** These are the values in `runner/resources.json`:

| Cell | Wall per fit | Memory |
|---|---:|---:|
| p500 c100 | 00:30:00 | 2G |
| p500 c050 | 00:30:00 | 2G |
| p1000 c100 | 00:30:00 | 2G |
| p1000 c050 | 00:30:00 | 2G |

Dev pilot evidence (OPS-4; `ops/OPS_LOG.md` 2026-11-02 entries, `ops/evidence/ops_finish_h_f3_20261102.txt`): run `20261030T1855Z_bench_f3v2_dev`, job 2496644, 26/26 COMPLETED, reconcile 26/26 valid, 0 timeouts; 0.757 core-h (1.514 billed); 37–192 s wall per fit; peak RSS ≤ 291 MiB. The pilot sizing rule below gave 10 min / 2 GiB in every cell and ≈ 66.6 physical core-h for production. HQ D64 set the wall to 30 min in every cell (about 9× the slowest observed fit), memory 2 GiB, with the bundle's single doubled-time (60 min) timeout retry as backstop; one array of 600 at `%30` at a time, as designed. Updated forecast: ≈ 66.6 physical ≈ 133 billed core-h, plus retries/overhead; the requested walls permit at most 1,200 physical core-h.

Historical (superseded for this run by D64): the pilot rule for `fill_resources.py` from `sizing.tsv` was: nearest-rank p95 in each cell; time in minutes = max(10, ceil(3×p95 seconds/60)); memory in GiB = max(2, ceil(1.5×max RSS KiB/1048576)). Production resources must come from the inspected NOTS pilot, never laptop timings. The pilot estimates production core-hours as 600 × cell mean seconds / 3600, summed over cells, excluding retry and scheduler overhead. The forecast is 75–90 physical core-hours, approximately 150–180 billed core-hours; dev is forecast under 2 physical / 4 billed core-hours. Dev requested wall permits 32.5 physical / 65 billed core-hours, so the forecast is not an enforced ceiling.

## Prepare and stage

**Single freeze edit:** manager replaces `<<BENCH_V2_MANIFEST_SHA256>>` and `<<BENCH_V2_F3_SOURCE_SHA256>>` in `runner/freeze.json` with the digest of `code/bench_v2/MANIFEST_SHA256.txt` and the distinct runner tree hash. No other bundle file is edited for freeze. Manifest entries use `F3_AdaptiveLasso/<relative-path>`; the verifier checks exact membership, every SHA-256 and the tree digest. Confirm its listed code-file order matches frozen `run_case.R`'s `CODE_FILES`.

**Authoritative bundle ledger: `BUNDLE_SHA256SUMS_FINAL` (this folder, written 2026-11-02 after the HQ D64 resource fill).** Earlier ledgers (pre-freeze draft, R2-reviewed, narrow-checked) are historical only and live in `archive_ledgers/`; do not verify current files against them. The prepare step makes and verifies a fresh `UPLOAD_SHA256.txt` containing the filled files.

On the laptop, substitute the chosen run ID in this single PowerShell command:

```text
py -3 -B "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/prepare.py" prod <run_id> "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
```

It produces `C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/staging/<run_id>/` and prints the upload manifest digest. OPS creates `/scratch/fb31/New_Campaign/upload/`, copies the staging directory with `scp -r "<full staging directory>" nots:/scratch/fb31/New_Campaign/upload/`, then on NOTS runs:

```text
bash /scratch/fb31/New_Campaign/upload/<run_id>/runner/stage.sh /scratch/fb31/New_Campaign/upload/<run_id> <upload_manifest_sha256>
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/launch.py prod <run_id> --resources /scratch/fb31/New_Campaign/upload/<run_id>/runner/resources.json --dry-run
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/launch.py prod <run_id> --resources /scratch/fb31/New_Campaign/upload/<run_id>/runner/resources.json
```

Stage verifies upload bytes and frozen code, and checks the disk guard with 30 MiB planned home growth. Every array and retry submission checks the guard again and validates GNU time, library/version, thread settings, and frozen source; scratch directories are created under `/scratch/fb31/New_Campaign`. Guard refusal means stop. Repeat the launch command after each terminal cell; each call submits at most one. Production logs record resource config, gate receipts, commands, IDs, and per-fit GNU-time wall/RSS in `logs/<run_id>/`. Results are `results/<run_id>/p{0500,1000}/<dataset_id>_<scale>/F3.{rds,csv,sha256,done}`. A `primary_<cell>.intent` without its corresponding jobs.tsv entry means acceptance is unknown: retain it and resolve with OPS/HQ using squeue and sacct; never assume rejection from a failed client. Never reuse a run ID.

If staging fails, retain the upload unchanged and rerun the same stage command with the same upload digest after resolving the fault. The upload membership is reverified and the installed code is rechecked against the frozen manifest; mismatches stop staging. Resources for this run are the HQ D64 values in `runner/resources.json` inside the immutable upload; no `config/<run_id>` folder is needed. The OPS transfer helper's own manifest and VERIFIED receipt are the verification authority for the upload folder; do not use the results-folder `manifests.py --verify` command for it.

If the installed tree is incomplete or differs, the stage command refuses rather than replacing it. OPS must report the mismatch to HQ, establish whether any job uses the tree, and use the charter's reviewed archive/verification procedure before any authorized repair. If the upload itself differs, retain it for diagnosis and prepare a fresh run ID and upload; do not edit the failed snapshot or skip checks.

## Terminal accounting, retry and acceptance

After all primary arrays terminate and accounting has settled, OPS runs the commands below. Monitor recorded IDs with `squeue -u fb31` and `sacct -j <job_id> --format=JobID%40,State%30,Elapsed,ExitCode`. Save each command's stdout and stderr in scratch logs and check exit status. Enable `set -o pipefail` before commands using `tee`. Source the environment before invoking the R validator.

```text
source /scratch/fb31/New_Campaign/upload/<run_id>/runner/env.sh
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/retry.py prod <run_id> --dry-run
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/retry.py prod <run_id>
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/reconcile.py --root /scratch/fb31/New_Campaign/results/<run_id> --kind prod --run-id <run_id> --source-sha256 <source_sha256> 2>&1 | tee /scratch/fb31/New_Campaign/logs/<run_id>/reconcile.txt
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/accounting.py /scratch/fb31/New_Campaign/logs/<run_id> 2>&1 | tee /scratch/fb31/New_Campaign/logs/<run_id>/accounting.tsv
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/collect_timing.py prod /scratch/fb31/New_Campaign/logs/<run_id>/timing | tee /scratch/fb31/New_Campaign/logs/<run_id>/timing.tsv
```

Retry requires complete terminal `sacct` records and absence from squeue, lists all states and selects only TIMEOUT units lacking valid outputs. It archives any partial files to scratch logs, then submits **at most once** with doubled original wall and the same memory, run ID, inputs and seeds. It submits one retry cell per invocation; repeat only after it is terminal for remaining cells. FAILED, OOM and all other states are reported for manager disposition. Existing retry intent prevents resubmission; if no job ID appears in an intent, inspect Slurm and escalate. Historical policy: original `F3_AdaptiveLasso/slurm/submit_prod.sh` and `F3_AdaptiveLasso/c050/slurm/submit_prod.sh` document one retry with double wall on timeout; campaign D11 also records it.

Submission intents are permanent evidence, not truth locks. If submission or a journal write fails, keep the intent. Resolve acceptance by the job name and run comment in it: the submitting process and sbatch client must have finished; all matching candidates must be absent from squeue and terminal in sacct; and acceptance or rejection must be positively established. A failed query, elapsed time or an unconfirmed no-match is not proof. Escalate unresolved outcomes to HQ. This bundle never creates or unlocks a truth lock.

Acceptance requires **2,400 expected = 2,400 observed**, no extras or duplicate rules; each file set includes `.done`, SHA-256 verified RDS/CSV, correct run/case/source on every row, loadable schema-version-2 RDS with six specified rules, allowed statuses and consistent coefficient supports. The reconciliation tallies rule statuses, including failures, and returns nonzero on structural failures. Accounting must cover every primary and retry task and reports elapsed core-hours by cell plus allocated CPU-hours. Review every failed or missing unit; no silent drop. Produce timing/cost reports and preserve raw `sacct` and logs. Sol review of the bundle and independent table tie-out precede release.

A zero-runtime whole-fit failure is refused with `runtime_s not one positive value per fit`; OPS retains or quarantines its four files and logs, records the refusal and escalates it under the failed-unit policy, never counting it as accepted or silently omitting it.

## Download, verify, clean

When all output is terminal and stable, execute these separately:

```text
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/manifests.py --run-log /scratch/fb31/New_Campaign/logs/<run_id> /scratch/fb31/New_Campaign/results/<run_id>/p0500 /scratch/fb31/New_Campaign/results/<run_id>/p1000 /scratch/fb31/New_Campaign/logs/<run_id>
```

OPS uses `py -3 "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/transfer/nots_pull.py" <absolute remote folder>` once per folder; it downloads into `C:\Users\felip\OneDrive - Rice University\NOTS Data\New_Campaign\` and verifies hashes. Run `py -3 -B "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/manifests.py" "<absolute downloaded folder>" --verify` on each. Also pull and verify the upload folder to preserve the exact code and launch scripts. After all downloads verify, Sol reviews the exact deletion list and receipts. **D44 B3:** first issue the separate command `cd /scratch/fb31/New_Campaign`; launch the cleanup helper from that directory, outside every tree being deleted, and ensure no process has a working directory or script open inside it. OPS then uses `bash /home/fb31/projects/BVS/New_Campaign/code/ops/remote_pack.sh delete <exact remote folder> <manifest_sha256 from that folder's VERIFIED transfer receipt>` for each reviewed folder. The helper re-hashes and refuses if jobs are active or bytes changed. Record deletion in `ops/CLEANUP_LOG.md`; retain frozen campaign code, never alter the original study.

No `config/<run_id>` folder is created for this run (HQ D64); the resource settings used are recorded in `logs/<run_id>/resources_used.json`. If one exists anyway, pull it with the OPS helper, keep its VERIFIED receipt, and include it in the reviewed deletion list.
