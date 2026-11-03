# SMC-BVS: master plan from here to a proved, Lean-checked paper

**As of 2026-11-03.** The empirical phase is **DONE** (HQ D94), and this repo has been refreshed with the final results (`Docs/SYNC_LATER.md`, done). Per Felipe (D77), "the theory campaign is being executed elsewhere", so the old HQ stopped after the empirical work. §3 onwards is the plan for whoever runs the theory phase.

## Read with
- `Docs/HQ/BOOTSTRAP.md`: how the new HQ takes over.
- `Docs/HQ/RULES.md`: Felipe's standing rules.
- `Docs/HQ/DECISIONS.md`: decision log D1–D94 (final).
- `Docs/HQ/STATUS.md`: the results on one screen.
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

## 2. Experimental phase: DONE (2026-11-03, D94)

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

**Results:** `Docs/HQ/STATUS.md` has a one-screen summary. Full reports:

| Regime | Headline | Theory evidence |
|---|---|---|
| Low p | `Results/2026-10-28_New_Campaign/L_20261102/HEADLINE_L.md` | `EVIDENCE_L.md` |
| High p | `Results/2026-10-28_New_Campaign/H2_20261102/HEADLINE_H.md` | `EVIDENCE_H.md` |

The 2026-10-23 fits' tables are in `Results/2026-10-28_New_Campaign/H_existing_20261030/`. Every final report has an independent tie-out (Terra) and a Sol acceptance next to it (`review/`, `tieout/`).

| Run or analysis | Final state |
|---|---|
| PROD-H, run `20261030T0934Z_prodH` (2,400 SMC fits, p ∈ {500, 1000}) | Closed. 2,394 ok + 6 `resource_limit`, counted as misses; P5 not run (D62). Reproduces the 2026-10-23 fits exactly. The F1 procedural deviation was accepted and disclosed (D92) |
| PROD-L, run `20261030T1811Z_lowp_prodL` (enumeration + SMC + 100×5 repeats, p ∈ {20, 30}) | Closed. 14,400 units completed natively; P5 not needed (D63) |
| BENCH_F3_DEV and BENCH_F3_PROD (aLasso with the lasso pilot, 2,400 fits) | Closed. 2,400 valid, 71.98 core-h; Sol ACCEPT WITH FIXES (D86, D87, D93) |
| PROD_L_BENCH rev 2, run `20261102T2309Z_lowp_bench` (8 benchmarks at low p) | Closed. `accept_bench` ACCEPTED 19,200/19,200. Rev 1 failed on a bundle probe defect, fixed in rev 2 (D82, D85, D92) |
| ANALYSIS-H2 (p ≫ n headline, aLasso rows, EVIDENCE_H) | DONE (D78, D87) |
| ANALYSIS-L (low-p headline Q1–Q4, stability, benchmark rows, EVIDENCE_L, ABESS exact-size check) | DONE (D75, D94) |
| NOTS | OPS CLOSED (D93). No jobs of ours; scratch `New_Campaign` removed; campaign home 2.4 MB of frozen code. Record: `Scripts/Campaigns/2026-10-28_New_Campaign/ops/FINAL_NOTS_STATE.md` |

**Disclosures carried into the paper:**
- PROD-H P5 not run (6 stops are misses);
- lasso-family headline `ebic1_K37`, with CV as a sensitivity (D42);
- EN α at the grid edge; aLasso `cv_min` last grid point;
- the post-hoc aLasso pilot change (the ridge rows are kept as a labelled sensitivity);
- ABESS is a heuristic: RSS-optimal in 2,375/2,400 low-p fits, +7 recoveries if corrected (D54.3, D94);
- low-p flags with no audit (D94): SSL exceeds the exact HPM, which is organic since the exact posterior is our own model's; the horseshoe `ci95` drop at p = 30, c = 0.5.

**Data** (bulk, not in Git): see `Docs/Records/DATA_INDEX.md`. The data mirror is on Felipe's PC ("NOTS Data/New_Campaign"). Moving it to the git-ignored `_data/` on Owls is Felipe's call.

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
| **P4 Let the data talk** | `EVIDENCE_H.md` + `EVIDENCE_L.md`, read together, give per target (THEORY_EXTRACTION_STRATEGY mapping): which premises hold, where and why the method fails, and a support / contradict / silent verdict per conjecture. **Inputs DONE:** both reports are final and accepted (D78, D87, D94), and their verdicts are summarised in `Docs/THEORY_PRIORITIES.md` §5. Still to do: the joint synthesis that turns the verdicts into the P6 cards | Analysis threads (Opus), Terra tie-out, Sol review | Reports accepted (done); synthesis by whoever runs the theory phase |
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
6. Old VS Code server versions on NOTS (1.46 GiB) and old Codex releases: deferred.
7. qr_data (~195 GB, non-BVS) on NOTS scratch: finish the transfer, or let the purge remove it.

Already resolved; only check the implementation:
- **Lasso-family headline (D42.6):** `ebic1_K37` is the headline at both scales, with CV disclosed as a sensitivity. Verify that the final tables implement it.

Resolved at the campaign's close: the PROD-H finding F1 was accepted as a disclosed procedural deviation, with no data loss (D92).

Carried forward (the old HQ stopped under D77, so these pass to whoever runs the theory phase or a new HQ):
8. The ABESS low-p exact-size result (2,375/2,400 RSS-optimal) and the horseshoe `ci95` drop at p = 30, c = 0.5 are disclosed, not audited (D94). Decide whether the paper needs more.
9. 14 old CODE_LEDGER mismatches (F2/F4_MCP_SCAD/A2_SSL mirrors, 2026-10-21), never reported to Felipe.
10. BFDR consult secondary outputs (postFDP, expected misses, ½-PFER set): adopt or reject.
11. Novelty check: "report the best model ever visited" vs Hans, Dobra & West (2007) shotgun stochastic search. Matters for the T21/T38 novelty claims.
12. THEORY.tex "Recommendations to the author" (10 items), the pair-addition move (LEVERS V10), the never-firing warnings E1/E3/local_limit: deferred.
13. `cut_group`: redefine or drop (D13 made it informational; it fires in 2,398/2,400 fits).
14. Wave-3 proofs' external review (queued). The v2.1 results never got a RESULTS.md or an external review (superseded by the v2.2.1 rerun reports).
15. Tension between "use all prior knowledge" (principle 4) and "I don't care about prior attempts" (D6) in the theory phase.
16. Local declutter questions on the old PC folder (P1/P2 tar packing, L1–L8, REORG questions).
17. **Security:** a NOTS password appeared in an old HQ transcript (2026-10-22). Change it if not done; never export thread text unredacted.

---

## 5. Cutover to this repo (after the experiments)

Full design: `Docs/Records/GH_HANDOFF/ASTRA_HANDOFF_PLAN.md` §D, steps D1–D10, and `HQ_SPINUP_PLAN.md`. In short:
1. Old HQ certifies the experimental phase complete (§2). **Done, D94.** Step 3 (the refresh) was done on 2026-11-03. What remains is Felipe's push (`Docs/PUSH_CHECKLIST.md`) and, if he wants a repo-based HQ, steps 7–9.
2. Quiesce the old watchdog. Freeze the source.
3. Refresh this repo per `Docs/SYNC_LATER.md`.
4. Verify (`Scripts/Campaigns/2026-10-28_New_Campaign/verify_manifests.sh` + PUSH_CHECKLIST).
5. **Felipe pushes.**
6. PCs sync via GitHub Desktop.
7. Bootstrap the new HQ on Owls (`Docs/HQ/BOOTSTRAP.md` §3): a capability rehearsal plus the activation evidence of BOOTSTRAP §4. That evidence is a Sol capability audit against the old HQ's responsibility table, a tested PC-independent archive and transfer receipt, persistent-job and log inspection, and the Owls re-login and out-of-band alert procedure. Felipe then accepts readiness.
8. Transfer authority once: one HQ, one watchdog. Exercise one harmless watchdog recovery with Terra observing the saved cycle, then get Astra's final handoff review and Felipe's acceptance (BOOTSTRAP §5).
9. Archive the old folder read-only only after step 8 is accepted. Any failed or unavailable capability leaves the dependent work inactive, and the old HQ stays authoritative.

Bulk data never enters Git. It lands in the git-ignored `_data/` on Owls.
