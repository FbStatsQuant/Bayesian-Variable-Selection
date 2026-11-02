# SMC-BVS: master plan from here to a proved, Lean-checked paper

**As of 2026-11-02 ~15:30Z** (snapshot taken during the GH packaging). The experimental phase is still finishing on the old HQ. Refresh §2 from the final campaign `STATUS.md`/`DECISIONS.md` at cutover (`Docs/SYNC_LATER.md`).

## Read with
- `Docs/HQ/BOOTSTRAP.md`: how the new HQ takes over.
- `Docs/HQ/RULES.md`: Felipe's standing rules.
- `Docs/HQ/DECISIONS.md`: decision log D1–D70.
- `Docs/HQ/OPS_FACTS.md`: NOTS facts.
- `Docs/THEORY.md`: every result and its status.
- `Docs/THEORY_PRIORITIES.md`: the frozen paper targets and their order.

Origin: the campaign plan of 2026-10-28 (`Docs/Campaigns/2026-10-28_New_Campaign/CAMPAIGN_PLAN_20261028.md`), phases P0–P9, approved by Felipe; the New Campaign charter (`…/CHARTER.md`) covers P1–P4.

---

## 1. Principles (Felipe)

1. **Unify first.** Stop adding pieces; one body of work.
2. **Paper = execution before theory.** The executed method must match the written methodology; otherwise fix and redeploy.
3. **Patch everything possible before the hard theory.**
4. **Let the data talk.** The simulations are instruments for the theory.
5. **Each hard theorem ends in one of two outcomes:** it holds (or a comparably strong version does under reasonable assumptions), or it hits a fundamental obstruction and the method must change.
6. **Investment rule for a method change plus a full rerun.** Do it ONLY if **both** hold:
   - with the change, all or most key results are provable;
   - a pilot gives strong evidence that the method still performs well.

   No large runs on gambles. Benchmarks need no rerun while the datasets are unchanged.
7. **Committed rules.** Low-p settings may differ, but only as one committed rule for every p ≪ n case. No arbitrary constants: every setting is tied to n, p or a stated principle.
8. **Believed versions before the swarm.** Fable leads statement refinement; Felipe green-lights; only then is the proof swarm released.
9. **Lean last.**

---

## 2. Remaining experimental work (state as of 2026-11-02 ~15:30Z)

The shipped code is **SMC-BVS v2.2.1**, FROZEN (manifest `d880afdb…13e1`, 27 files, `Scripts/Campaigns/2026-10-28_New_Campaign/code/core/v2_2_1/`).

**Regime scope (D22, Felipe):**
- **Low p (p ≤ 30)** assesses both the SMC (Ẑ, HPM, RB and plain PIPs against exact enumeration) and the BVS (against the truth).
- **High p (p > 30)** assesses only the BVS against the truth: recovery /100 and /600, HPM = truth, MPM (RB and plain) = truth.
- **Never report** Ẑ accuracy or PIP error against an exact reference for p ≫ n. SMC-internal quantities there are stored, not reported.

**Headline questions** (the only things reported to Felipe):
1. Is Ẑ accurate?
2. Is the HPM accurate (equal to the exact HPM, and to the truth)?
3. Are the PIPs (RB and plain) accurate?
4. Exact recovery per scenario /100 and pooled /600, for every method.

| Item | State | Next step | Owner (old HQ) |
|---|---|---|---|
| PROD-H: 2,400 SMC fits, p ∈ {500, 1000}, c ∈ {1, 0.5} | DONE. 2,394 ok + 6 `resource_limit` (P5 retries **not run**, D62; counted as non-recoveries). Pulled, verified and deleted on NOTS. Reproduction of the 2026-10-23 fits: 2,400/2,400 identical. Sol ACCEPT WITH FIXES. One deviation (per-folder delete before the home summary was verified) awaits HQ disposition | HQ disposition of finding F1 | OPS-4 thread |
| PROD-L: enumeration + SMC + 100×5 repeats, p ∈ {20, 30} | DONE on NOTS. enum20, enum30, smc (9,600 files) and smcrep (48,000) pulled, VERIFIED and deleted. P5 not needed (D63) | PROD-L clean-up on NOTS (`cleanup_prodl.sh`, queued in the PLB chain) | OPS-4 |
| BENCH_F3_DEV: adaptive-lasso dev pilot | DONE, 26/26 (D64) | — | OPS-4 |
| BENCH_F3_PROD: aLasso lasso-pilot rerun, p ≫ n, 2,400 fits (D42) | READY (D65). Run `20261102T1252Z_bench_f3v2_prod`; 4 arrays of 600 at %30, one at a time; chain queued | Launch cells 1–4, then retry (TIMEOUT only, once, 2× wall), reconcile, pull, Sol deletion review, delete | OPS-4 (`ops/OPS8_F3PROD_PROGRESS.md`) |
| PROD_L_BENCH: 8 benchmark methods at low p (bench_lowp r2) | READY (D67). Run `20261102T1311Z_lowp_bench`; chain queued after the pulls and F3 cell 1 | Submit `--profile alone`, reconcile, close, pull, `accept_bench.R`, clean-up | OPS-4 (`ops/OPS9_PLB_PROGRESS.md`) |
| ANALYSIS-H2: p ≫ n reproduction, plain-PIP row, lasso-family `ebic1_K37` headline, theory evidence | RUNNING. Headline draft done; reproduction done; TD d = 0 sample (196 cases) running; EVIDENCE_H to write; Terra tie-out running; Sol review after (D53: at most 2 rounds) | Finish; aLasso rows after F3 PROD lands | ANALYSIS-H2 thread |
| ANALYSIS-L: low-p headline Q1–Q4, repeat-seed stability, theory evidence | RUNNING. Pass A (theory + TD) done; pass B running | Tables → HEADLINE_L, EVIDENCE_L → Terra tie-out → Sol; benchmark rows after PROD_L_BENCH | ANALYSIS-L thread |
| Benchmark freeze (`bench20261019/`, `Benchmarks/` on NOTS) | Copy-only until `RELOCATION_OK.md` exists (never written) | Decide who lifts it (open decision) | HQ |
| Final NOTS clean-up | Continuous rule: a run is done only when its outputs are downloaded, verified and removed | Verify that scratch is empty of campaign data and that the campaign home footprint is ≤ 0.5 GiB | OPS |

**Experimental phase complete when:**
- every row above is DONE, with Sol-accepted final reports (`HEADLINE_H`, `HEADLINE_L`, `EVIDENCE_H`, `EVIDENCE_L`, benchmark rows including aLasso v2);
- downloads are verified;
- NOTS is clean;
- no job or writer is live.

Then the GitHub cutover (§5) runs, and the theory phase starts in the new HQ.

**Redeployment standard (D36), if any rerun becomes necessary:**
- one fix, applied in both regimes;
- a test that would have caught it;
- a Sol ACCEPT;
- frozen code with a manifest;
- local tests including negative controls;
- a pilot before scale;
- an independent tie-out;
- full reconciliation, with no silent drops.

---

## 3. After the experiments: analysis, then theory (P4–P9)

| Phase | What | Lead / staff | Gate |
|---|---|---|---|
| **P4 Let the data talk** | `EVIDENCE_H.md` + `EVIDENCE_L.md`, read together, give per target (THEORY_EXTRACTION_STRATEGY mapping): which premises hold, where and why the method fails, and a support / contradict / silent verdict per conjecture. Preliminary signals are in `Docs/THEORY_PRIORITIES.md` §5 | Analysis threads (Opus), Terra tie-out, Sol review | Report accepted by HQ |
| **P5 Theory layer 1 (bookkeeping)** | Restatements with no new mathematics: potential-uninterrupted-run + output-available event for T11(iii), T12, T14, T15, T23, T25, T27(i), T31; write T34; T13 snapping wording; drop T12's secondary-PIP clause; T12 islandwise wording; T21 route wiring; T07 + T06(i) sentence; T26 scope; T02(i) exact BB(1,p) tail and T03 restatement; T05 remark | Opus lead, Sonnet workers, Sol review; Fable only on a stuck step | HQ accepts; Felipe informed |
| **P6 Vetting the hard targets** | **Fable 5.1 leads statement refinement** ("believed versions") of T37, T22 + T27 on one compatible family, T38, T26(i)–(ii); T24 and T39 as fallbacks. One **confidence card** per target: refined statement; data evidence; exact small-case tests (p ≤ 30); proof skeleton with the crux isolated; Astra's attack; Sol's review; risk; method change needed? | Fable lead; Astra adversary; Sol review; Opus manager | **G3: Felipe green-lights each card.** No swarm without it |
| (if a card fails) | Method-change proposal under the **investment rule** (§1.6), with a proof sketch and a pilot. If approved, loop back: one redeploy carries every change (P2–P3 again, D36 standard) | Opus + Fable; Sol; pilot via OPS | Felipe |
| **P7 Proof swarm** | Proofs of the green-lit targets, in the order of THEORY_PRIORITIES §4 (T37 first) | Opus-managed, worker-heavy; Sol + Astra reviews (cross-family); Fable only on cruxes | Proof accepted only after independent reviews, never self-verified |
| **P8 Lean** | Formalise every accepted proof (`lean.md`), then merge (`lean-merge.md`). Scope and cost each theorem first: the exact finite results (T07, T21, T11(iii), T12, T37(i)) are mechanical; the probabilistic and asymptotic ones need Mathlib groundwork | Opus-led | — |
| **P9 Assembly** | One consistent theory section plus the empirical package, ready for the paper protocol | — | Felipe |

**Pursuit order for the proofs** (`Docs/THEORY_PRIORITIES.md` §4):
1. T37 (needs restating first; the literal TD fails generically in the data);
2. T02(i) tail + T03 restatement;
3. T22(i)/(iii) + T27 on one compatible family;
4. T38 (composition + eligibility, LS0 tweak if needed);
5. T24 only if T37 fails, T39 only if T38(b) fails;
6. bookkeeping (T12, T21, T26(i)–(ii), T07, T05 remark).

**Adoption.** The 21 locked proof entries are not adopted until Felipe says so. Never present a locked result as adopted.

---

## 4. Open decisions (carry to the new HQ's "Pending")

Felipe's:
1. Adopt the 21 locked proof entries (briefing §6.1.1); never answered.
2. Paper ambition / venue (JCGS or Bayesian Analysis soon, vs JRSS-B/Biometrika with the frozen targets). The frozen list targets JRSS-B / Biometrika.
3. c = 0.75 at p = 500 (≈ 155–170 fit-h); never decided.
4. Benchmark freeze: who lifts it (`RELOCATION_OK.md` never written). Copying is allowed; nothing is deleted.
5. Public repo: which unpublished theory, manuscripts, reviews and PDFs may be pushed, or make the repo private (`Docs/PUSH_CHECKLIST.md`).
6. Lasso-family headline rule: D42.6 made `ebic1_K37` the headline at both scales, with CV disclosed. Confirm when the tables land.
7. Old VS Code server versions on NOTS (1.46 GiB) and old Codex releases: deferred.
8. qr_data (~195 GB, non-BVS) on NOTS scratch: finish the transfer, or let the purge remove it.

HQ's (decide or carry):
9. PROD-H completion finding F1 (delete before the home summary was verified; no data loss).
10. 14 old CODE_LEDGER mismatches (F2/F4_MCP_SCAD/A2_SSL mirrors, 2026-10-21), never reported to Felipe.
11. BFDR consult secondary outputs (postFDP, expected misses, ½-PFER set): adopt or reject.
12. Novelty check: "report the best model ever visited" vs Hans, Dobra & West (2007) shotgun stochastic search. Matters for the T21/T38 novelty claims.
13. THEORY.tex "Recommendations to the author" (10 items), the pair-addition move (LEVERS V10), the never-firing warnings E1/E3/local_limit: deferred.
14. `cut_group`: redefine or drop (D13 made it informational; it fires in 2,398/2,400 fits).
15. Wave-3 proofs' external review (queued). The v2.1 results never got a RESULTS.md or an external review (superseded by the v2.2.1 rerun reports).
16. Tension between "use all prior knowledge" (principle 4) and "I don't care about prior attempts" (D6) in the theory phase.
17. Local declutter questions on the old PC folder (P1/P2 tar packing, L1–L8, REORG questions).
18. **Security:** a NOTS password appeared in an old HQ transcript (2026-10-22). Change it if not done; never export thread text unredacted.

---

## 5. Cutover to this repo (after the experiments)

Full design: `Docs/Records/GH_HANDOFF/ASTRA_HANDOFF_PLAN.md` §D, steps D1–D10, and `HQ_SPINUP_PLAN.md`. In short:
1. Old HQ certifies the experimental phase complete (§2).
2. Quiesce the old watchdog. Freeze the source.
3. Refresh this repo per `Docs/SYNC_LATER.md`.
4. Verify (`Scripts/Campaigns/2026-10-28_New_Campaign/verify_manifests.sh` + PUSH_CHECKLIST).
5. **Felipe pushes.**
6. PCs sync via GitHub Desktop.
7. Bootstrap the new HQ on Owls (`Docs/HQ/BOOTSTRAP.md`), with a capability rehearsal and Felipe's readiness check.
8. Transfer authority once (one HQ, one watchdog).
9. Archive the old folder read-only.

Bulk data never enters Git. It lands in the git-ignored `_data/` on Owls.
