# OPS-9 progress: PROD_L_BENCH (jobs/PROD_L_BENCH, HQ D67) — resume from here after any crash

Rules: one ssh at a time via ops/scaffold/sshlock; 15-min back-off after a timeout; before ANY submission check `squeue -u fb31` + `LOG_RUN/jobids.tsv`; never submit twice. Approval-safe tooling (D38).

**STAMP = 20261102T1311Z, RID = 20261102T1311Z_lowp_bench**, results `/scratch/fb31/New_Campaign/results/20261102T1311Z_lowp_benchres`, logs `/scratch/fb31/New_Campaign/logs/20261102T1311Z_lowp_bench`. Ledger BUNDLE_SHA256SUMS.txt 2a7ceba7…dfc3 (32 OK); r2 manifest 85a18248…a6b7. **No truth staged → no truth lock** (JOB.md §8/§14).

| Step | State | Notes |
|---|---|---|
| local stage | DONE 13:12Z: 1,269 files, 64.5 MB, no truth/holdout/dev; tar in NOTS Data/New_Campaign/runs/20261102T1311Z_lowp_bench/bundle | evidence/ops9_plb_20261102T1311Z_stage.txt |
| chain | QUEUED detached `ops/scaffold/plb_chain.sh` (pid ops9_plb_chain.pid; log ops9_plb_chain.txt): waits for PULL_LIST_DONE + F3 cell-1 ssh_rc; STOPs if PROD-L logs were not pulled (D58) or pulls failed; then PROD-L cleanup_prodl (dry + --yes, receipt /scratch/.../upload/cleanup_receipt_20261030T1811Z_lowp_prodL.txt), then BENCH upload + guard 75 + extract/STAGED + dry run alone + submit; then exec waiter.sh (log ops9_plb_waiter.log) | if the chain dies: check squeue + LOG_RUN/jobids.tsv BEFORE anything |
| submit | TODO | job ids -> here + message to HQ |
| reconcile / clear_stale / resubmit rounds / close / pull / accept_bench.R / cleanup | TODO | |

- 2026-11-02T22:10:46Z **SUBMITTED then FAILED at s0_verify (bundle defect):** jobs 2510090 (s0_verify FAILED), 2510091 (s1_bench CANCELLED, afterok), 2510092 (s9_collect COMPLETED). bench_env_probe.R:18 passes test_library= to lowp_load_method(id, code_dir, p, test_versions=FALSE). PROD-L cleanup VERIFIED before submission. Awaiting HQ (fixed bundle). Note: a resubmission needs a fresh STAMP (plb_submit_remote refuses an existing runs/<RID>) or HQ guidance on reusing it.
- 2026-11-02T22:14:27Z HQ D82: fix goes to PROD-L-BUILD (rev 2 READY + new ledger hash expected). On rev 2: resubmit with a FRESH STAMP (never 20261102T1311Z). Failed-run cleanup started now (does not depend on rev 2): ops/scaffold/plb_failed_cleanup_chain.sh (pid ops9_plb_failed_cleanup.pid): pull --delete scratch logs/20261102T1311Z_lowp_bench (30 files, 329 KB) -> cleanup_bench.sh dry + --yes + receipt (home runs/20261102T1311Z_lowp_bench 64 MB, scratch runs/*_tmp); status ops9_plb_failed_cleanup_chain.txt.
- 2026-11-02T22:44:13Z Failed run 20261102T1311Z fully removed (CLEANUP VERIFIED 22:43Z); nothing of it left on home or scratch; evidence logs local. Waiting for rev 2 (fresh STAMP).

## Rev 2 (HQ D85)
- 2026-11-02T23:10:07Z STAMP **20261102T2309Z** (fresh). Ledger da08f38c… (32) verified locally; NOTS-side check in plb_submit_remote_rev2.sh. Chain plb_rev2_chain.sh (pid ops9_plb_rev2.pid); status ops9_plb_rev2_chain.txt; submit output ops9_plb_rev2_submit.txt; waiter ops9_plb_rev2_waiter.log. NEVER resubmit if PLB_JOBIDS= present in ops9_plb_rev2_chain.txt. After: waiter (exit 3 = triage, then --until-terminal), reconcile_bench, clear_stale, resubmit rounds, close/manifests, pulls, accept_bench.R (local R 4.4.1), cleanup_bench with receipt.
- 2026-11-02T23:14:43Z **SUBMITTED rev 2: s0_verify 2511134, s1_bench 2511135 (0-95%32), s9_collect 2511136.** NEVER resubmit STAMP 20261102T2309Z main wave. Waiter ops9_plb_rev2_waiter.log (in chain pid ops9_plb_rev2.pid).
- 2026-11-02T23:46:37Z ALL_TERMINAL 98/98 COMPLETED. Post chain plb_post_chain.sh (pid ops9_plb_post.pid), status ops9_plb_post_chain.txt.
- 2026-11-03T12:00:59Z VPN outage 01:24Z-11:59Z. Phase A (close bench) COMPLETED on NOTS 02:13:51Z (CLEAN; 76,800 files MANIFEST 0dd8ced3…). Resumed from B with plb_post_chain_fromB.sh.
- 2026-11-03T13:23:45Z **COMPLETE**: ACCEPTED 19,200/19,200 (0 FAIL, 0 INCOMPLETE); 21.85 core-h; results+logs pulled/verified/deleted; CLEANUP VERIFIED (receipt cleanup_receipt_20261102T2309Z_lowp_bench.txt). Remaining: Sol completion review / report if HQ wants.
