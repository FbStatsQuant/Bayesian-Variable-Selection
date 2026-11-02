# Headquarters: campaign tracker

HQ thread: "Headquarters", <thread>, Claude Opus 5.5. Last updated 2026-10-23 ~01:00Z.

## Mandate (Felipe, 2026-10-23 ~01:20Z)

HQ is in charge, outside the usual protocols.

**Final goals:**
1. Empirical data on SMC-BVS v3 effectiveness against the benchmarks.
2. Lock in all current proofs that hold.

**Next theory step:** a Fable-guided deep audit of the theory, ONLY on Felipe's express order.

**For now:** audit what we have, and test the actual working of the method. No new proof waves; wave 3 finishes.

## Standing decisions (Felipe)

- **2026-10-23 00:50Z:** OpenAI is paused. All work moves to Claude: Claude Personal (CP) and Claude Work (CW), at about 60% / 40%. Anything the OpenAI threads already ran is kept if it passes audit.
- **Goals:**
  1. SMC-BVS v3 on 100 seeds per scenario per p (S1–S6 × p ∈ {500, 1000} × r = 1..100), at c = 1 and c = 0.5: 2,400 fits on the benchmark datasets. Report how often each method recovers the true model, against the benchmarks.
  2. Prove as many v3 theorems as possible.
- **Usage limits:** pause and resume after the reset. Never cancel or move work.
- **Infrastructure:**
  - NOTS: `ssh nots` goes direct to loginx3. Use batched commands, never connection bursts.
  - Owls is a shared lab machine: nice 19, small footprints.

## Campaign 1: Claude audit of the OpenAI work (running)

Folder: 02_Experiments/H_2026-10-22_smcbvs_v3_deploy/AUDIT_CLAUDE/ (AUDIT_CONTEXT.md).

| Auditor | Model and account | Scope |
|---|---|---|
| A-CODE | Opus, CP | Production code v2 against Part I and the prototype; regression rerun on Owls |
| B-VERIFY | Opus, CP | B's oracles, independence and claims against logs; R-6 |
| C-OPS | Sonnet, CP | The 120-dataset selection, seeds and hashes; pilot; runner; why NOTS N0 failed |
| D-ANALYSIS | Sonnet, CP | Scoring reuse, benchmark reproduction, join, Monte Carlo SEs |
| INVENTORY | Haiku, CP | Ledger and snapshot hashes, with canaries |
| PROOFS T22(iii) + T27(i) | Opus, CW (delegated) | Writes proofs/WAVE2_CLAUDE_AUDIT/ |
| PROOFS T21 + T25(iv) | Opus, CW (delegated) | Writes proofs/WAVE2_CLAUDE_AUDIT/ |

## Campaign 2: deployment of 2,400 fits (after the audit)

Plan, to be confirmed by the audit results:
1. One Claude Opus ops thread (CP) takes over C's role:
   - fix the NOTS N0 infrastructure problems (module initialisation, /usr/bin/time);
   - build v2 (or a v3 fix if the audit requires one) on NOTS;
   - run the regression and the battery;
   - run the smokes;
   - produce the full array of 2,400 units (cost ≈ 1,120 core-hours, extrapolated from the pilot).
2. An independent Opus reviewer (CW) checks any code fix and the NOTS readiness.
3. One Claude Opus analysis thread (CW) scores the runs with the benchmark scoring code: exact recovery and errors, against the 8 benchmark methods (+ SuSiE-refine at c = 0.5).
4. HQ gates every step.

## Campaign 3: proofs, wave 3 (running; brief: Theory_architecture_v3/proofs/WAVE3_BRIEF.md)

| Theorem(s) | Thread | Account |
|---|---|---|
| T01 + T02 | <thread> | CP |
| T03 | <thread> | CP |
| T06 + T07 | <thread> | CP |
| T04 | <thread> | CW |
| T10 | <thread> | CW |

**Next waves (candidates):** T17, T28, T32, T34 (core), the remaining parts of T11/T14/T20/T23/T31, then T26 and the secondary items. Proved so far: 14 (wave 1: 10; wave 2: 4, audit pending). One Fable 5.1 campaign review is planned per wave.

## Campaign 4: Owls to NOTS migration (running; Felipe, 2026-10-23 ~01:05Z)

**Owner:** OWLS-MIGRATE (Sonnet, CP).

**Phase 1:**
- inventory ~/smcbvs_v3_deploy_20261022, ~/BVS and ~/_reloc on Owls;
- copy the infrastructure (code and scripts, ≤ 50 MB) to NOTS /projects/ml75/fb31/BVS/smcbvs_v3_deploy_20261022/;
- copy EVERYTHING to the laptop, <PC_NB_ARCHIVE>\Owls_home\;
- verify by sha256;
- write 00_Admin/OWLS_MIGRATION.md.

**Phase 2: deletion on Owls.** Only after HQ writes 00_Admin/OWLS_DELETE_OK.md. HQ writes it when:
- (1) the audit agents A-CODE and B-VERIFY, which use Owls, have finished;
- (2) an independent Haiku checker has re-verified the copies.

**Scope update (Felipe, ~01:10Z):**
- The NOTS infrastructure destination is now /home/fb31/projects/BVS/SMC_BVS_v3_deploy/.
- Phase 3: reorganise ALL BVS code on NOTS into organised folders under /home/fb31/projects/BVS/. Plan first, in 00_Admin/NOTS_CODE_REORG_PLAN.md; execute only after HQ writes 00_Admin/NOTS_REORG_OK.md.
- Benchmark freeze: copy-only for bench20261019/ and Benchmarks/ until RELOCATION_OK.md exists.

**Scope.** Other projects in Owls ~ (ANN_GH, Deep_Learning, Pandas, R, envs, Misc, Bayesian_Lin_Reg_GH_Owls) are NOT touched; they are not BVS.

## Campaign 5: local folder declutter (planning)

**Owner:** LOCAL-REORG (Sonnet, CP). It writes the plan only, 00_Admin/REORG_PLAN_20261023.md, with no moves.

**Then:**
- HQ reviews the plan;
- a Sonnet executor applies the approved moves;
- a Haiku verifies them;
- README.md and PATH_MAP.md are updated.

Active campaign folders are untouched until those campaigns end.

## Audit results so far

**INVENTORY (Haiku): done.**
- v2 archive, snapshot and Owls copy: all byte-identical.
- Root ledger: 159/171 rows OK. The 12 stale rows are working-tree A_build/code paths edited after the ledger was written; the frozen v2 snapshot rows are OK.
- Two ledger notes to fix: line 284 cites the v1 archive hash as "frozen archive", and line 500 has an unpaired hash.
- Both canaries behaved correctly.

**Proof audit T21 + T25(iv) (Opus, CW): done.**
- Both are correct; small wording fixes are listed in proofs/WAVE2_CLAUDE_AUDIT/AUDIT_T21_T25iv.md.
- E2: H10 may follow from the addition floor in wave-1 T22 Lemma 2. Relayed to the T10 thread.
- E5: T25(iv) is a direct unrolling of PW2, so it adds nothing without PW2.

**Proof audit T22(iii) + T27(i) (Opus, CW): done.**
- Both are correct, with one optional wording fix each (AUDIT_T22iii_T27i.md). It agrees with all the OpenAI reviews.
- New candidate: EXP′ itself looks provable from G, R and within-block SE (sketch; one check bounded the remainder at about 15–17). Added to the next-wave queue as "Lemma EXP′".

**Wave-2 Claude audit: ALL 4 PROOFS CONFIRMED CORRECT.**
- Pending: one Sonnet pass to apply the wording fixes E1, E3 and E5 (T21/T25) and the optional fixes (T22iii, T27i), as new proof versions.

**Next-wave queue (updated):** T17, T28, T32, T34, Lemma EXP′, then the remaining parts.

**C-OPS audit (Sonnet): SOUND WITH FIXES.**
- Data: 120/120 datasets and 240 units match an independent recomputation (seeds, hashes, manifest).
- Pilot facts confirmed, including the p1000 E2 flag (SD 1.24).
- Runner: dataset-keyed and rerun-safe, BUT no real fit has gone through it yet (synthetic fixtures only).
- NOTS N0 failures are all infrastructure, never the SMC code: no lmod profile on compute nodes, no /usr/bin/time, and a self-built GNU time that fails make check.
- Fixes for Campaign 2:
  - drop or replace the GNU-time dependency, e.g. /proc VmHWM plus wall clock, or `sacct MaxRSS`;
  - initialise modules explicitly;
  - re-derive the unit time limits from NOTS timings;
  - do not commit resource kills as permanent failures;
  - fix the NOTS status-line string;
  - run one REAL fit end to end through the runner before the array.

**A-CODE audit (Opus): SOUND WITH FIXES, deployable.**
- Every v2 diff against the prototype is justified and correct.
- Regression 32/32 rerun on Owls.
- End to end at production budgets: v2 is bit-identical to the prototype on 3 cases.
- Study layer correct. Minor items F1–F5 go into the Campaign 2 brief:
  - F1: locale-independent source hash;
  - F2: exact-branch label;
  - F3: R OOM should record failed;
  - F5: --hours must match the external unit limit.

This upgrades the Astra build grade to roughly B+.

**B-VERIFY audit (Opus): SOUND WITH FIXES.**
- The oracles are correct, independent and backed by logs.
- F1 (major): 77 of about 90 orchestration clauses were checked by source review only.
  - Mitigated by A-CODE: v2 is bit-identical to the verified prototype at production budgets.
  - Campaign 2 readiness must add a tiny-p SMC-versus-exact check.
- G1_PASSED wording corrected; R-6 relabelled as a waiver.

## OpenAI external-audit queue

These run in bulk when Felipe announces an OpenAI usage reset ("turn the furnace on"). Nothing is spent piecemeal.
- Wave-3 proofs (T01+T02, T03, T04, T06+T07, T10): one external review each, Astra or Sol, after the Claude reviews.
- Any code fix made for Campaign 2: an external Sol review.
- The 2,400-fit results and tables (Campaign 2): an external Astra review before the final report.

**Authority (Felipe, 2026-10-23 ~01:40Z):**
- HQ is in charge overnight and uses its own judgement.
- Claude usage limits pause work; nothing is shut down.
- HQ may spawn Astra reviewers for anything it judges critical. Everything else waits in the OpenAI queue for the next reset.
- Felipe checks in tomorrow.

## Status at ~02:15Z

**Campaign 1 (audit) DONE.** All 7 audits are sound or sound with fixes (AUDIT_CLAUDE/AUDIT_SUMMARY.md).

**Campaign 2 LAUNCHED** (BRIEF_CLAUDE.md):
- ops thread <thread> (CP);
- analysis thread <thread> (CW).

Gates: NOTS_READINESS.md → independent review (CW) → GO_2400.md (HQ) → array → OUTPUTS.md → RESULTS.md → external Astra review (critical).

**Campaign 4:**
- phase 3 (the NOTS code reorganisation) is done: /home/fb31/projects/BVS/SMC_BVS_v3/{deploy,core,prototype_profiling} plus READMEs; the old /projects deploy folder is superseded, archived and removed; item 5 waits for RELOCATION_OK.
- Owls re-check PASS; OWLS_DELETE_OK written; phase 2 deletion running.
- The 202 extra files on NOTS are the verified item-3 nots_side_code copy plus the README; they are known.

**Campaign 4 DONE (~02:30Z).**
- Owls: 213,220/213,220 files (21.5 GB) and 250 symlinks deleted, each re-hashed against the verified copy just before deletion. 32 read-only snapshot directories inside ~/BVS were given owner write to allow deletion.
- ~/OWLS_BVS_MOVED.md left in place.
- Copies: laptop NOTS_BVS/Owls_home (all) and NOTS SMC_BVS_v3/deploy (infrastructure).
- Item 5 (bench code copy) waits for RELOCATION_OK.

**Campaign 5 (~02:40Z).**
- Plan written (REORG_PLAN_20261023.md): 204,549 files and 27.1 GiB in the project, about 80% of it large data that belongs outside.
- HQ approved R1–R8, Q1–Q5, X1–X2 and the README/PATH_MAP edits (REORG_OK_20261023.md): about 21.2 GiB out of the project, a few archive moves, and only regenerable deletes.
- Executor REORG-EXEC (Sonnet) running; a Haiku re-verification follows.
- **For Felipe (tomorrow):**
  - P1/P2: pack the old archives into tars?
  - L1–L8: tidy-ups after the campaigns.
  - The plan's six questions, including whether to archive the Unified report.

## Check at ~02:50Z

**Wave 3 DONE.** All 5 proved (T01+T02, T03, T04, T06+T07, T10), each verified by 2 independent Opus xhigh reviewers with no judge needed; threads settled.
- T03 and T04 used H-T02, which is now proved by T01_T02.
- External OpenAI review of wave 3 is queued.
- PROOF-LOCK (Sonnet) is applying the wave-2 wording fixes and writing proofs/LOCKED_PROOFS.md with dependency closure.

**Campaign 2:**
- ops is in readiness (one job per check on NOTS);
- analysis Phase 1 is complete (D-F1 fixed, D-F2 closed on real v2 dev fits) and waits for OUTPUTS.

**LOCKED_PROOFS.md written (~03:00Z).**
- 19 rows (21 theorem entries), with all 38 path and SHA-256 pairs verified. The wave-2 wording fixes are applied as new versions (T21 v3, T25iv v2, T22iii v2, T27i v3).
- Closed hypotheses: START, H-T12, H03, H-T02, H-T03, H10, and the premises of T22(iv-c).
- Open: H24, PW2, EXP′, VIS, NL_η, NL_avg, T27 H2/H3, BASIN, T21 occurrence and exposure, T13 COVER, and the regime assumptions.
- Caveat: dropping H-T02 from T03/T04 was matched by wording only.

**Campaign 5 DONE (~03:30Z).**
- About 21 GiB of data left the project; 51,823 files verified after the move.
- Independent Haiku re-check PASS: 1,631 files hashed, all 11 pointers resolve, no sources remain, both canaries behaved correctly, backups present.
- Open for Felipe: P1/P2 (tar packing), L1–L8 (after the campaigns), the plan's six questions.

## Check at 10:35Z

- **Stall found:** the ops thread was idle from 02:29Z to 10:33Z (its background poll broke and it was never woken). It resumed by itself at 10:33Z. The HQ check now detects stalls and nudges.
- **Readiness (from NOTS_READINESS.md):**
  - build plus 32/32 regression: PASS;
  - v2.1 contract test, 77 checks: PASS;
  - B battery on NOTS: PASS;
  - pending: tiny-p versus exact, smokes, unit limits, the e2e fit.

## Check at 11:35Z

**NOTS readiness COMPLETE, all PASS:**
- build plus 32/32 regression;
- B battery;
- tiny-p versus exact, 40 fits: |dlogZ| <= 0.027, PIP error <= 0.0051, HPM 40/40;
- smokes bit-identical to Owls;
- e2e fit plus transfer OK;
- unit limits L500 = 1500 s and L1000 = 5400 s.

The independent gate reviewer (Opus xhigh, CW) is running and will write E_ops_claude/GATE_REVIEW_GO2400.md. GO_2400 follows.

**GATE (~12:40Z): GO WITH CONDITIONS** (GATE_REVIEW_GO2400.md; GO_2400.md written).
- Key catch: the old limits would have truncated every escalated fit (the hardest datasets) and biased the results. Limits raised to L500 = 6300 s and L1000 = 24000 s.
- Sapphire Rapids nodes pinned.
- Stop rule in the first 200 finished units.
- Rerun machinery to be fixed, with --no-requeue.
- Timeouts reported as their own category.
- The ops thread was told to launch once C1, C2 and C4 are done.

## PRODUCTION LAUNCHED 12:27Z (2026-10-23)

| Array | Job | Tasks / units | Throttle | Limit L |
|---|---|---|---|---|
| p1000 | 2365494 | 600 / 1,200 | %60 | 24,000 s |
| p500 | 2365495 | 600 / 1,200 | %40 | 6,300 s |

- Both arrays: sapphirerapids nodes, --no-requeue, code v2.1 908a70ca.
- C1–C5 met before submission.
- Expected wall time: about 10–14 h.
- The HQ hourly check wakes the ops thread to poll, so it cannot stall again.

**13:10Z poll:** 243/2400 finished (p1000 76, p500 167), all ok. 0 method_failed, 0 resource_limit, 0 timeout, 0 infra; 3 escalated. C3 window (first 200) PASSED, so the run continues. 99 tasks running.

**13:34Z poll:** 392/2400 finished, all ok; 18 escalated; 0 failures, timeouts or infra.

**Incident:** the 14:55Z wake failed on a network/DNS outage (ENOTFOUND) around 15:00Z. The ops thread was resumed at 16:10Z. The NOTS arrays were unaffected.

**16:12Z poll:** 1,359/2,400 finished (p1000 462, p500 897), all ok; 99 escalated; 0 failures, timeouts or infra. 100 tasks running.

**17:11Z poll:** 1,731/2,400 finished (p1000 587, p500 1,144), all ok; 124 escalated; 0 failures, timeouts or infra.
- The poll's "running tasks 491" counts every fb31 job. At 18:10Z, HQ's direct check showed only 61 of ours running (p1000 60 at %60; p500 1 left), so the throttle is respected.
- The p1000 throttle goes to %100 once p500 ends (instructed in this wake).

**18:11Z poll:** 1,909/2,400 finished (p1000 711, p500 1,198). 1,908 ok and 1 infra (0.05%, below the 2% rule; it gets an infrastructure-only rerun at the end with the same seed). 0 timeouts, 0 resource_limit; 142 escalated.

**19:09Z–20:15Z: VPN DOWN on the PC.** owls does not resolve, and all NOTS nodes time out, so polls are skipped. The NOTS arrays are unaffected. Felipe must reconnect the Rice VPN (AnyConnect); HQ retries each hour.

**23:53Z:** the VPN is still down (NOTS unreachable). Polls stay skipped; the arrays keep running on NOTS. Waiting for Felipe to reconnect.

## 2026-10-24 ~23:50Z: STOP ordered by Felipe ("stop everything for now")
- HQ hourly schedule (<scheduled-task>…) PAUSED (enabled=false; not deleted).
- No T3 threads were running besides HQ: ops (<thread>) and analysis (<thread>) are idle. Nothing was sent to them.
- NOTS arrays 2365494 / 2365495 were NOT cancelled. NOTS is unreachable (PC off the Rice VPN since ~19:09Z), and cancelling would throw away finished work. Last known: 1,909/2,400 finished (18:11Z poll).
- Resume point: re-enable the schedule; once the VPN is back, run one poll from the ops thread, then rerun the infra failures, reconcile, pull, and write OUTPUTS.md.

## 2026-10-26 17:00Z: production FINISHED (one read-only check by HQ; nothing restarted)
- VPN back. sacct: 2365494 600/600 COMPLETED and 2365495 600/600 COMPLETED.
- poll.py --no-hold: 2,400/2,400 units finished; 2,394 ok; 6 resource_limit (p1000 5, p500 1); 0 method_failed; 0 timeout; 0 infra (the 18:10Z infra flag no longer appears; ever_infra = 0); 208 escalated (p1000 145, p500 63). Nothing is pending in the queue.
- Still to do (on Felipe's go): reconcile --full-verify, pull to the laptop and delete on NOTS, OUTPUTS.md, analysis Phase 2 (recovery rates), review, external Astra review. The schedule stays PAUSED.

## 2026-10-28 ~14:30Z: results scored (on Felipe's request for the tables)
- Pulled both runs to the laptop: tar sha256 c6dcfeb7…2d91. NOTS full-verify passed, and on the laptop 2,400/2,400 bundles pass sha256. E_ops_claude/OUTPUTS.md written. The NOTS originals are NOT deleted (that waits for Felipe).
- Scored with F_analysis_claude/pipeline/score_campaign2.py, one pass per run: NOTS_BVS/.../F_analysis/score_p0500_20261028T1404Z and score_p1000_20261028T1404Z. Both exit 0. The 1,400 benchmark cells are identical across the two passes.
- Independent recount (F_analysis/independent_recount/, stdlib Python, raw CSV vs truth_manifest 'active'): 48/48 SMC cells match the pipeline.
- Headline tables: F_analysis/HEADLINE_TABLES.md. SMC-BVS HPM exact /600: c=1 p500 559, p1000 560; c=0.5 p500 370, p1000 340.
- Still pending: the plain-language RESULTS.md, a critical review, the external Astra review, and the NOTS deletion.

## 2026-10-28: theory inventory and alignment audit (Felipe's request) DONE
- Report: 01_Methodology_and_Theory/Theory_architecture_v3/INVENTORY_20261028/THEORY_INVENTORY.md.
- Team: Astra high ×2 (plan + final consult); Sol 6.1 high ×4 (alignment groups A/B/C + regime); Sonnet ×2 (intuition, citation check 396/396 OK, 3/3 canaries caught); Haiku ×1 (inventory, 38/38 hashes, 2/2 canaries caught). Fable 0.
- Code provenance: the local v2_1 is byte-identical to the NOTS production code (verify/HQ_PROVENANCE.md).
- Key findings:
  - the target and algorithm match under EX-A/EX-S;
  - escalation is calibration-only;
  - material: resource-limit stops versus the theorems' complete-run assumption; global versus reported HPM;
  - SE is impossible at n=200, and BM-C fails by about 100×, so the statistical theorems are asymptotic only here;
  - cut_group fires in 2,398/2,400 fits.

## 2026-10-28: status briefing for Felipe (DONE)

- **Briefing:** `04_Reports_and_Presentations/STATUS_BRIEFING_20261028/BRIEFING.md`. Sections: data, method, benchmarks, results, ranked theorems (36), recommendations.
- **Team:**
  - Sonnet x2: method and benchmark fact sheets;
  - Haiku: merged tables, 0 mismatches;
  - Fable (CW, high) and Astra (high): independent advice, then sign-offs (both endorse with changes);
  - Sol 6.1: numbers review, certified with corrections;
  - Terra 6.1: method/theory review (not certified); its re-check had 9 replacements, all applied.
- **New facts surfaced by the review:**
  - F5 ABESS also fails G5 check 4 at c=1 (2,560/4,848 path supports beaten).
  - 3 of the 4 c=1 SMC stopped fits had the exact truth in their audit-only output.
  - Benchmarks had one doubled-time retry on timeout; SMC had none.
- **Awaiting Felipe:** decisions in section 6.1 (adopt locked theory; venue/ambition; stage-1 runs).

## 2026-10-28: paper theorem selection FROZEN

- **Frozen list:** `01_Methodology_and_Theory/Theory_architecture_v3/PAPER_SELECTION_20261028/FROZEN_LIST.md`; hashes in `FROZEN.sha256`.
- **Reviews:** Fable (CW, high) and Astra (high), independent; both "endorse with changes".
- **JRSS-B main text (8):**
  - T03 (+T01, T02);
  - T07;
  - T22+T27;
  - T37 (NEW; T24 as alternative);
  - T21;
  - T38 (NEW main theorem: two-regime HPM consistency, with delivery);
  - T26(i)-(ii) (favourable regime);
  - T12 (+T31(i)).
- **Biometrika (5):** T03, T22, T37/T24, T21, T38.
- **Contingency:** T39 (Astra's repair tracks; a method extension).
- **Next:** Felipe plans a multi-thread proof campaign, deployed from HQ.

## 2026-10-28: NEW CAMPAIGN (experimental phase) LAUNCHED

- **Felipe's mandate:** run or rerun all simulations and benchmarks for the shipped method, in both regimes, and process the results. HQ orchestrates; threads do the work. The theory discussion comes after.
- **Charter:** `02_Experiments/I_2026-10-28_New_Campaign/CHARTER.md`, with `STATUS.md` and `DECISIONS.md` beside it.
- **Rules:**
  - NOTS: 10 GB quota with a 7 GB campaign ceiling.
  - Layout: `BVS/New_Campaign` on NOTS, `/scratch` for transient data, downloads to OneDrive `NOTS Data/New_Campaign`.
  - Continuous clean-up; reviewers on every deliverable; no scanning of caches.
- **Wave 1 threads (Opus 5.5 high managers):** OPS-1 (NOTS clean-up and scaffold), CONF (conformance and code v2.2), LOWP (low-p build).
- **Next:** pilot, then production for regimes L and H, then analysis, then a benchmark audit if needed.
