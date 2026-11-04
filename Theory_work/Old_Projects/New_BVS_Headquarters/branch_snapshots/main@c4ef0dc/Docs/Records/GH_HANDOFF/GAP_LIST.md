# Handoff gap list (merged from the four thread audits)

2026-10-30. Sources: `thread_audit/SLICE_0_predecessor.md` (old HQ `<thread>`), `SLICE_1–3.md` (Headquarters `<thread>`, all 2,924 items). This list is what the new HQ's files must add or fix at cutover. Done items are marked ✔.

## A. Rules for the new AGENTS.md / CHARTER (said in chat, missing from the handoff plans)
1. Usage limits: when CP or CW hits its limit, pause and wait for the reset; never shut threads down (Felipe 10-22, 10-23).
2. Owls is a shared lab machine: "don't monopolize". Caps from H RULINGS_LEAD R-3: ≤16 cores, ≤24 GB RAM, ≤20 GB disk, nice 19; pause if load >40 or <30 GB free. Never touch Felipe's own VS Code R session. Revisit the disk cap now that bulk data lands in `BVS_GH/_data`.
3. Fable-guided deep theory audit only on Felipe's express order (10-23).
4. Briefings are "so I can make choices", not "a Bible": concrete, nothing important left out (10-28).
5. Memory safety covers RAM too: measured memory request plus margin per job, and a memory pilot before enumerations (10-29, "avoid derailment due to memory issues").
6. Running NOTS jobs are never killed on a pause; let them finish (10-23).
7. Relaunching the same work after a crash does not count as new budget.
8. Never run two copy or move commands on one tree at once. Copy → verify → delete only through tooling (`verified_delete.sh`), never ad-hoc commands (the 10-28 near-miss).
9. Launch threads inside the project ("tag with the project"), i.e. in GH-Bayesian-Variable-Selection after cutover.
10. Lean proofs are the last phase (10-29, PLAN principle 9).
11. Model accounts: Fable from Claude Work; Claude workers from Claude Personal (10-28, probably a default; confirm).
12. Felipe often decides through inline comments on quoted text (`t3-citation …&comment=`). Read and record those.
13. p≫n rerun approved "as long as we have a clear strategy to extract insight from that data into the theory building phase" (10-30; relayed to HQ to amend D23).

## B. Operational facts for OPERATIONS.md / WATCHDOG.md
1. **OAuth expiry kills HQ itself** (10-29: 3 failed watchdog runs; only Felipe's "resume" fixed it). The new HQ needs an out-of-band alert (e.g. a push notification from a non-Claude watcher on Owls) and the re-login recipe. PC recipe: `$env:CLAUDE_CONFIG_DIR="<PC_CLAUDE_CONFIG>"; claude auth login; claude auth status`. The Owls equivalent is still to be determined.
2. **Owls → NOTS SSH gets blocked after connection bursts** (10-22, ~20 min, all login nodes). One batched connection at a time, 15-min back-off; the alias is pinned to loginx2.
3. **Stalls:**
   - a broken background poll left a thread idle for 8 h;
   - a provider-error rerun sat queued for 6 h (fixed by `task_cancel` and relaunch);
   - Bash permission prompts block agents silently (D37/D38).

   Watchdog rules: hourly one-poll wake, ≤10-min foreground polls, nudge after 45 min with no file change.
4. Disk-quota truncation is silent: audit expected vs analysed counts, rerun with the same seeds.
5. `squeue` shows all fb31 jobs; throttle by job ID. Escalated fits (~8.7%) need the long limits: L500 6,300 s, L1000 24,000 s.
6. Rcpp compile-cache race: one cache per process. The NOTS default python3 is too old; use 3.13.
7. Windows tar does not recreate symlinks, so symlink "FAIL" lines in relocation checks are false alarms.
8. Transfer speed NOTS → PC is about 3–10 MB/s; long pulls must survive outages. Use one driver per disjoint unit list.
9. Slurm `long` partition: 384 CPUs, 1 TB, 3 days. There is no allocation balance, but heavy use lowers fair-share.
10. ml75 `/projects` quota (100 GB) is shared with other users.
11. Owls quota: 2,124 / 3,482 GB used (10-29), so about 1.36 TB is free, shared with Felipe's other work.
12. Rice CRC contact: <email>, https://researchcomputing.rice.edu/get-help (in `rescued_from_temp/nots_fix/INCIDENT_SUMMARY.md`).

## C. Files that must be imported, not only pointed to
- ✔ `%TEMP%` evidence rescued to `rescued_from_temp/` (nots_fix, stageC_astra; 120 files, sha256-verified 10-30).
- v3 profiling records exist only in `<PC_NB_ARCHIVE>\NOTS_projects_ml75\BVS\v3_profiling_20261020\`, not on OneDrive: BRIEF, PLAN, STATUS, REPORT_PHASE1, PROFILING_REPORT, DP2_DECISIONS, ASSUMPTIONS, RUNS, review/.
- v2.1 headline tables: `NOTS_BVS\smcbvs_v3_deploy_20261022\F_analysis\HEADLINE_TABLES.md`.
- `bench20261019/verify` snapshots: take them from NB (they were deleted on NOTS; 36 symlinks are not recreated).
- `NB\_scripts\sha\` (the durable relocation manifests; the NOTS copies are purgeable).

## D. Stale records to fix at cutover
- ✔ Memory updated 10-30: HQ identity, model roles, "no OpenAI", the 7 GB ceiling, venue, download location.
- `README.md` "Work that lives off this PC" still points to the deleted NOTS profiling folder.
- `HQ_CAMPAIGNS.md` still has the "7 GB" ceiling and "OpenAI paused".
- Theory-run provenance: the thread metadata says Opus, STATUS says Fable lead; note this in the theory record.

## E. Open decisions for Felipe (carry to the new HQ's DECISIONS "Pending")
1. Adopt the 21 locked proof entries (briefing §6.1.1): never answered.
2. c = 0.75 at p = 500 (~155–170 fit-h): never decided.
3. Benchmark freeze: `RELOCATION_OK.md` was never written, so `bench20261019/` and `Benchmarks/` stay copy-only. Who lifts the freeze? (The copy for GH is allowed; nothing is deleted.)
4. qr_data (~195 GB, non-BVS) on NOTS scratch: finish the transfer, or let the purge remove it?
5. 14 CODE_LEDGER mismatches (10-21, F2/F4_MCP_SCAD/A2_SSL mirrors): never reported to Felipe.
6. BFDR consult secondary outputs (postFDP, expected misses, ½-PFER set): never adopted or rejected.
7. Novelty check: "report the best model ever visited" vs Hans, Dobra & West (2007) shotgun stochastic search. Not done; it matters for the T21/T38 novelty claims.
8. THEORY.tex "Recommendations to the author" (10 items), the pair-addition move (LEVERS V10) and the never-firing warnings E1/E3/local_limit: deferred, not decided.
9. `cut_group`: redefine or drop (D13 demoted it to informational).
10. Wave-3 proofs: the external review is still "queued" in LOCKED_PROOFS.md. The v2.1 results never got RESULTS.md or an external review.
11. Local declutter questions: P1/P2 tar packing, L1–L8, the six REORG_PLAN questions. `.vscode-server` unused versions on NOTS (1.46 GiB).
12. Tension between "use all prior knowledge" (principle 4) and "I don't care about prior attempts" (D6) for the theory phase.
13. Public repo: which unpublished theory, manuscripts and PDFs may be pushed? (see HQ_SPINUP_PLAN).
14. **Security:** the NOTS password appears in the Headquarters transcript (10-22). Change it if not already done, and never export thread text unredacted.

## F. Threads to settle or confirm inert before cutover (Astra plan step D2)
- OpenAI A/B/C/D `<thread>`, `<thread>`, `<thread>`, `<thread>`
- Stage C Fable `<thread>`
- Campaign-2 ops `<thread>` and analysis `<thread>`
- The finished New Campaign delegates (OPS-1/2/3, CONF, CONF-2, LOWP, the paper-selection consults, briefing, inventory)
- "Plan Benchmark Deployment Specifications" `2ac75474…`, the owner of the benchmark freeze
- Older HQ-like threads, for the record: `82c98985…` (methodology lead), `89b9b8b7…` (10-01 organiser), `6418dfe6…` (10-15 proofs)
