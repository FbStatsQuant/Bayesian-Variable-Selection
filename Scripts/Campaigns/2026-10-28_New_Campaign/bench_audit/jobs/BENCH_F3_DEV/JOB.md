# BENCH F3 v2: dev timing pilot — DRAFT, DO NOT SUBMIT

This is a hand-off to OPS. Submission requires the manager's frozen manifest and source hashes, a successful integration check against that freeze, and independent Sol review under D36. No SSH was opened by the author. The shared runner is in sibling `BENCH_F3_PROD/runner/`.

`BUNDLE_SHA256SUMS_FINAL` (authoritative; rewritten 2026-11-02 after the HQ D64 production resource fill changed the shared `runner/resources.json`) includes this folder and relative references to the shared production runner (including its filled freeze.json) and prepare.py. Earlier ledgers are historical only, in `archive_ledgers/`. This dev run (`20261030T1855Z_bench_f3v2_dev`) is complete and accepted (HQ D64); its upload digest b43fa799… is unaffected.

## Work and allocation

Twenty-four dev datasets/scales (p=500,1000, S1–S6, r001, c100/c050) plus production p1000 S4 and S6 r001 at c050: **26 one-CPU tasks**, one array `1-26%13` (26 billed CPUs), Sapphire Rapids, commons/nots_commons, 4 GiB and 75 minutes per task provisionally. The launcher counts all fb31 arrays against a combined 100-task ceiling; OPS can set `--throttle N` and must coordinate concurrent launches because the check is a snapshot. Any increase must respect 192 billed CPUs and 96 total campaign tasks (D47/D49/D50), including PROD-H and PROD-L. Historical F1 cost suggests total actual work below 2 core-hours; this is an unverified estimate, and requested wall is a ceiling of 32.5 core-hours. Pause and report if actual work threatens the pilot budget. No fit accesses truth.

Forecast: DEV <2 physical core-hours ≈ <4 billed core-hours; requested wall permits 32.5 physical / 65 billed, so that forecast is not enforced. PROD ≈75–90 physical / 150–180 billed core-hours, before retry and overhead. Production resources must come from the inspected NOTS pilot, never laptop timings.

Inputs are read-only `/projects/ml75/fb31/BVS/bench20261019/dev/inputs/p{0500,1000}/<dev_dataset_id>.rds` and `dev/manifests/dev_inputs_manifest.csv`; the two production timing inputs use `inputs/p1000/<dataset_id>.rds` and `manifests/inputs_manifest.csv`. Study library: `/projects/ml75/fb31/BVS/bench20261019/lib/R452`. One numerical thread; GCC/14.3.0, R/4.5.2, glmnet 5.1, and the verified absolute binary `/opt/apps/software/time/1.9-GCCcore-13.3.0/bin/time` from time/1.9. Its version, format/output behavior and SHA-256 are checked; loading its module is avoided to preserve the compiler/R modules, as in pilot rev 7c.

Run ID: `YYYYMMDDTHHMMZ_bench_f3v2_dev` (seconds are also accepted). Code only in `/home/fb31/projects/BVS/New_Campaign/code/bench_v2/F3_AdaptiveLasso/`; output root `/scratch/fb31/New_Campaign`, results `results/<run_id>/p{0500,1000}/<case_id>/F3.{rds,csv,sha256,done}`, logs `logs/<run_id>/`; staging is `/scratch/fb31/New_Campaign/upload/<run_id>/`. GNU time records wall seconds and max RSS KiB per attempt in `logs/<run_id>/timing/`.

## Freeze, prepare and stage

1. Manager freezes `code/bench_v2/MANIFEST_SHA256.txt` and sets its **own file SHA-256** as `<<BENCH_V2_MANIFEST_SHA256>>` and the distinct run_case.R source-tree SHA-256 as `<<BENCH_V2_F3_SOURCE_SHA256>>` in `BENCH_F3_PROD/runner/freeze.json`. Manifest entries must use `F3_AdaptiveLasso/<relative-path>`. The verifier rejects an unlisted, missing, altered or symlinked F3 file, and checks the runner tree hash. Source-tree membership/order must match `CODE_FILES` in the frozen `run_case.R`.
   This is the sole bundle edit at freeze. The PROD bundle ledger records the placeholder file before this edit; prepare creates a fresh upload manifest after the values are filled.
2. On the laptop run the command below, substituting the run ID. It creates `C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/staging/<run_id>`, prints the upload manifest digest, and refuses an existing destination.

```text
py -3 -B "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/prepare.py" dev <run_id> "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/code/bench_v2"
```

3. OPS creates `/scratch/fb31/New_Campaign/upload/` and uses `scp -r "<full staging directory>" nots:/scratch/fb31/New_Campaign/upload/` to upload that folder. Compare the upload-manifest digest printed by prepare with the value passed below. This is an OPS-only transfer. Do not write to the frozen study or old benchmark home paths.
4. On NOTS, as OPS, run `bash /scratch/fb31/New_Campaign/upload/<run_id>/runner/stage.sh /scratch/fb31/New_Campaign/upload/<run_id> <upload_manifest_sha256>`. It verifies the upload, runs the disk guard with 30 MiB planned home growth, stages or verifies the code without overwriting, verifies the frozen manifest, then reports `STAGED_OK`.

On a stage failure, retain the upload unchanged, resolve the fault, then repeat the same stage command with the original upload digest; it repeats upload and installed-code verification. The OPS transfer helper's own manifest and VERIFIED receipt are authoritative for later download of the upload folder; results-folder `manifests.py --verify` does not apply to the upload folder.

An incomplete or mismatched installed tree is never overwritten by staging: OPS reports it to HQ, checks whether jobs use it, and follows the charter's reviewed archive/verification procedure before any authorized repair. A mismatched upload is kept for diagnosis and replaced by preparing a fresh run ID and fresh upload, never by bypassing checks.

## Submit and collect

The following are individual NOTS commands. Replace `<run_id>` and `<source_sha256>` with frozen values; use the exact paths, no changes to the study. Enable `set -o pipefail` before commands using `tee`. Monitor recorded IDs with `squeue -u fb31` and `sacct -j <job_id> --format=JobID%40,State%30,Elapsed,ExitCode`.

```text
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/launch.py dev <run_id> --resources /scratch/fb31/New_Campaign/upload/<run_id>/runner/resources.json --dry-run
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/launch.py dev <run_id> --resources /scratch/fb31/New_Campaign/upload/<run_id>/runner/resources.json
source /scratch/fb31/New_Campaign/upload/<run_id>/runner/env.sh
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/retry.py dev <run_id> --dry-run
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/retry.py dev <run_id>
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/reconcile.py --root /scratch/fb31/New_Campaign/results/<run_id> --kind dev --run-id <run_id> --source-sha256 <source_sha256> 2>&1 | tee /scratch/fb31/New_Campaign/logs/<run_id>/reconcile.txt
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/accounting.py /scratch/fb31/New_Campaign/logs/<run_id> 2>&1 | tee /scratch/fb31/New_Campaign/logs/<run_id>/accounting.tsv
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/collect_timing.py dev /scratch/fb31/New_Campaign/logs/<run_id>/timing | tee /scratch/fb31/New_Campaign/logs/<run_id>/timing.tsv
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/sizing.py /scratch/fb31/New_Campaign/logs/<run_id>/timing.tsv | tee /scratch/fb31/New_Campaign/logs/<run_id>/sizing.tsv
```

Run retry only after all primary tasks are terminal and sacct has all task records. It reports every state, selects only TIMEOUT tasks lacking a valid result, and allows one retry at twice the original time; FAILED/OOM are reported, not retried. An intent without job id means submission outcome is uncertain: inspect the scheduler and escalate, do not delete the marker. The historical policy appears in `NOTS_home/projects/BVS/Benchmarks/F3_AdaptiveLasso/slurm/submit_prod.sh` and its c050 counterpart (comments: one retry, double time for TIMEOUT); D11 cites the same policy. OPS records scheduler IDs, status, command, reconciliation, accounting and stdout/stderr in scratch logs. The initial and per-submission gates run the campaign guard, probe its ceiling, verify source, check GNU time and glmnet, and create scratch directories. A guard refusal or any gate failure means no submission.

The submission intent is permanent evidence, not an unlockable truth lock. If submission or a journal write fails, keep it. Resolve acceptance by the job name and run comment recorded in the intent: the submitting process and sbatch client must have finished; all matching candidates must be absent from squeue and terminal in sacct; and acceptance or rejection must be positively established. A failed query, elapsed time or an unconfirmed no-match is not proof. Escalate unresolved outcomes to HQ. This bundle does not create or unlock a truth lock.

Sizing uses nearest-rank p95 per p×scale, **time = max(10, ceil(3×p95 seconds/60)) minutes**; **memory = max(2, ceil(1.5×max RSS KiB/1048576)) GiB**. The eight p1000/c050 observations include the two production cases; other cells have six. Estimated production core-hours = 600 times mean wall seconds per cell / 3600, summed across cells; it excludes retries and scheduler overhead. Sample is small; review long tails and failures before using the recommendation.

## Acceptance and cleanup

Acceptance: 26 unique expected units, no unexpected cases, matching rds/csv hashes and frozen source on all six rows, v2 schema, six rule IDs, valid coefficient evidence, status tallies visible, no missing units; accounting covers every primary and retry task; sizing has all four cells and all 26 timings. A structurally valid `failed` row is reported, not relabeled successful. Preserve reconciliation and accounting output in logs using `tee`, with shell pipefail enabled; check both command exit statuses. Independent Sol review is required.

A zero-runtime whole-fit failure is refused with `runtime_s not one positive value per fit`; OPS retains or quarantines its four files and logs, records the refusal and escalates it under the failed-unit policy, never counting it as accepted or silently omitting it.

After all jobs are terminal and logs have stopped changing, run:

```text
python3 /scratch/fb31/New_Campaign/upload/<run_id>/runner/manifests.py --run-log /scratch/fb31/New_Campaign/logs/<run_id> /scratch/fb31/New_Campaign/results/<run_id>/p0500 /scratch/fb31/New_Campaign/results/<run_id>/p1000 /scratch/fb31/New_Campaign/logs/<run_id>
```

OPS downloads each folder with `py -3 "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/ops/transfer/nots_pull.py" <absolute remote folder>` to the matching path under `C:\Users\felip\OneDrive - Rice University\NOTS Data\New_Campaign\`; the helper verifies SHA-256 and writes a receipt. Independently run `py -3 -B "C:/Users/felip/OneDrive/Documents/Local_to_global_Bayesian/02_Experiments/I_2026-10-28_New_Campaign/bench_audit/jobs/BENCH_F3_PROD/runner/manifests.py" "<absolute downloaded folder>" --verify` on each. Pull and verify the upload folder too, to retain scripts and source snapshots. Sol reviews the exact deletion list and receipts after download. **D44 B3:** issue `cd /scratch/fb31/New_Campaign` as a separate command before cleanup; launch the helper from outside every tree being deleted, and ensure no process has a working directory or script open inside it. Only then may OPS invoke `bash /home/fb31/projects/BVS/New_Campaign/code/ops/remote_pack.sh delete <exact remote folder> <manifest_sha256 from that folder's VERIFIED transfer receipt>`; it rechecks the folder and refuses while jobs are active. Delete each reviewed scratch folder separately, record cleanup, and retain the tiny frozen code in campaign home. No deletion by this bundle.
