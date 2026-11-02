# Comparison with final PROD-H and pilot fixes

This is an implementation mapping for review, not an independent review verdict. Both F3 jobs use these shared scripts.

| PROD-H / pilot fix | F3 treatment |
|---|---|
| R2-1 early SMC hold; R2-10 SMC polling cadence | Not applicable as written: those are PROD-H's SMC-specific 200-unit stop rule and polling contract. OPS monitors these arrays and is responsible for stopping/escalating unexpected failures. |
| R2-4 P5 scan as compute job; Q2 P5 categories | Not applicable: F3 has no P5/resource-limit scan; its only automatic retry is the recorded TIMEOUT policy. |
| R2-5 stale locks and temporary-file cleanup | Adapted fail-closed: manifest preflight refuses lock/tmp artifacts; retries copy partial output to logs. This bundle does **not** include PROD-H's automated proof-and-archive cleaner: OPS must inspect and archive proven-stale artifacts after both scheduler checks. This is an outstanding operational limitation, not an automated equivalent. |
| R2-6 transactional/revalidated manifests | Applied: all three folders are preflighted before commits; existing manifests are compared with the entire current membership/content and never silently replaced. A retry can finish a partially committed set. |
| R2-7 post-acceptance write failure | Adapted: an exclusive, fsynced intent precedes sbatch and is retained on failure; accepted IDs go to jobs.tsv. Unlike PROD-H, the bundle does not automatically cancel accepted IDs; unresolved acceptance stops further submission for manual OPS/HQ resolution. |
| R2-8 all-array throttle | Applied: every fb31 array counts; unknown or unlimited arrays and failed scheduler queries refuse. No own-array exclusion. |
| R2-9 scratch logs/home manifest | Scratch-only logs and results applied. A home run-summary manifest is not applicable: run journals and summaries live in scratch and are downloaded there. |
| R2-10 cadence / accounting ceiling | SMC polling cadence not applicable; F3 accounting reports elapsed physical core-hours and allocated Slurm CPU-hours by cell and total. |
| Q1 QoS | Applied: nots_commons is requested. OPS must verify association before submitting. |
| R3-1 unknown scheduler state | Applied to sequencing, retry and final accounting: squeue must succeed and show job absent; complete task-level terminal sacct must succeed. Unknown state never permits another cell or cleanup. |
| R3-2 guard at direct submit | Applied: stage, every primary and every retry invoke the guard wrapper, checking both quota thresholds and probing refusal. |
| R3-3 empty result folder | Applied: a zero-file folder has a zero-byte manifest and a distinct empty check; verification recomputes exact membership without `sha256sum -c`. |
| R4-1 overlapping scan and exact-id retirement | Scan retirement is not applicable. For F3 submission, the exclusive per-cell intent prevents overlapping calls from submitting the same cell; there is no automatic retirement. |
| R5-1 atomic retirement; R5-2 signal during sbatch | Scan retirement is not applicable. F3 intent is fsynced before sbatch and remains after failure or interruption; it is never automatically removed. Manual recovery follows the R7 positive-resolution rule. |
| R6-1 any nonzero sbatch may be accepted | Applied conservatively: the intent survives **any** sbatch error and blocks relaunch, including after client death. |
| R7-1 failed diagnostic append | Adapted: submission errors write status/stdout/stderr to a scratch diagnostic file on a best-effort basis. A failure to write diagnostics cannot remove the pre-existing intent or permit a relaunch. |
| R7-2 positive-resolution recovery | Applied in JOB.md: no timeout, failed query, or unconfirmed no-match authorizes clearing an uncertain intent. |
| D43 terminal waiter | There is no background waiter. Each continuation separately proves absence from successful squeue and complete terminal sacct records; tests include absent, live and failed-query cases. |
| D44 B2 never-locked unlock | Not applicable: no truth lock or unlock operation. Intents are persistent submission evidence, not unlockable truth locks. |
| D44 B3 cleanup outside deleted tree | Applied in JOB.md: change to scratch campaign root in a separate command, invoke the home-resident OPS helper from outside each target, and ensure no open cwd/script in the target. |
| Pilot rev 7c GNU time | Applied: use the absolute time/1.9 binary, verify version and actual `-f/-o` numeric output before work, record binary SHA-256, fail closed. It is not loaded as a module so GCC/R modules are not disturbed. |
| D49/D50 CPU defaults | Applied: PROD one %30 cell at a time (60 billed), DEV %13 (26 billed); 100-task all-fb31 submit guard plus OPS 192-billed/96-task raise rule. |

The manifest wrapper proves all recorded primary/retry jobs absent from squeue and terminal in sacct, requires accounting, rejects stale artifacts, and then preflights all folders. Empty folders are verified by exact membership rather than `sha256sum -c`.
