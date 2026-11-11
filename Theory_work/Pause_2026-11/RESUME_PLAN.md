# Theory Wave 3 — RESUME PLAN (written 2026-11-10 21:20 CST, read-only analysis; research sub-agent, Opus 5.5 high)

Sources read: `Theory_work/Wave3/{PROGRAM,PROTOCOL,HQ_DECISIONS}.md`; `git log -1 9d86c01`; every ticket's LOG, REPORT,
review dispositions; NOTS `/scratch/fb31/theory_w3/*` and `/home/fb31/projects/BVS/theory_w3/runs/*` (read-only: `ls`,
`tail`, `grep`, `scp` *from* NOTS; no job submitted, nothing written there). P6 numbers below were re-derived locally
with the repo's own `Theory_work/Wave3/W3-P6/scripts/rederive.R` on copies of the RDS files (output kept in my scratchpad,
not in the repo). UNVERIFIED = I could not check it.

## 0. Headline: the commit message is stale — three "council pending" tickets have already PASSED on disk

`9d86c01` says "W3-RM council pending, W3-SAMP sweep/council pending, W3-POST2 council pending". The working tree says
otherwise (all of these files are **untracked**, see `git status`):

| ticket | council result on disk | evidence |
|---|---|---|
| W3-RM | **PASSED round 2**: Astra 9.8 / Opus 9.1, all six gates (round 1: 8.8 with G6 FAIL / 8.9) | `W3-RM/reviews/C2_disposition.md`, `C1_disposition.md`, `W3-RM/LOG.md` (19:15) |
| W3-SAMP | **sweep SW1 done (28 items, all fixed); PASSED round 1**: Astra 9.1 / Opus 8.8, all gates | `W3-SAMP/reviews/SW1_disposition.md`, `C1_disposition.md`; committed `W3-SAMP/REPORT.md` §1 already says so |
| W3-POST2 | **PASSED round C1**: Astra 8.6 / Opus 8.6, all gates | `W3-POST2/reviews/C1_disposition.md`, `W3-POST2/LOG.md` step 16–17 |

So the three proof tickets need **HQ decisions + labels + a commit**, not more review. Only W3-P6 needs compute.

## 1. HQ housekeeping before any launch (≈ 15 min, HQ alone, no agents)

1. **Provider rule conflict.** `Wave3/PROTOCOL.md` item 2 still says "Claude Personal runs only Fable 5.2; every Opus …
   runs on Claude Work". The current allocation (owner, 2026-11-10; HQ memory) is Opus ≈ 2/3 Claude Personal / ≈ 1/3
   Claude Work, Fable only on Claude Personal. Add one line to `HQ_DECISIONS.md` amending item 2 before relaunch, or agents
   will follow the file.
2. **HQ decisions owed** (each one line in `HQ_DECISIONS.md`):
   - W3-RM flag 3: keep STATEMENT v1.2 (weaker hypotheses adopted post-lock from R02 P1/P2/P3a) or revert to v1.1
     wording (`W3-RM/REPORT.md` flags 3, §6 item 4). Recommendation: keep v1.2 (both council rounds reviewed v1.2.x).
   - W3-RM flag 1: accept that the result is "(V)+(L)+lattice condition (N)/(D-R)", not "(V)+(L)" (`REPORT.md` flag 1).
   - W3-POST2 flags 1–2: approve the post-lock strengthenings (items 3, 4, and 5 via (ID^M)) and rule the E1 v2
     restatement within the kill budget (`W3-POST2/REPORT.md` flags 1–2). Recommendation: approve (K2 line check,
     mid-point, sweep and council all reviewed the adopted versions).
   - W3-SAMP: v3 already accepted by HQ 2026-11-09 17:26 (`W3-SAMP/LOG.md`); nothing owed.
3. **Labels:** apply PROVED-CHECKED per clause to W3-RM (RM-0, RM-F, RM-R, Lemma E4, examples), W3-SAMP (CC, PC, MR, ST,
   D, LT♯, C, TR; NC_r necessity stays OPEN), W3-POST2 (claims A–E). W3-POST2 REPORT explicitly leaves the label to HQ.
4. **Registry blocks (PROTOCOL rule 8, from 2026-11-10):** W3-POST2 has them (`REPORT.md` §8). W3-RM has a "Registry items"
   section in the older rule-7 form (`REPORT.md` §5); W3-SAMP has §5 "Assumptions … for INFRA" but no template block.
   INFRA already ingested W3-POST and W3-SAMP (commit `8596a60` on `theory/infra`); W3-RM, W3-SCR, W3-POST2 not yet.
   Rule 8 is dated after these tickets closed → **ingest via `tools/ingest.py` after PR #6 merges** rather than re-opening
   reports.
5. **Commit the paused state (owner approval needed for the commit):** `Theory_work/Wave3/W3-RM/`, `W3-POST2/`, `W3-P6/`,
   the five untracked W3-SAMP files, the HQ_DECISIONS lines. **Exclude** `*.exe` (Wave1 harness binaries) and
   `__pycache__/`. The bibliography change (`Papers/Core_bibliography/INDEX.txt` + Song–Liang 2015 PDF) is a separate
   commit. W3-P6 `results/` is empty locally — results live only on NOTS (§2.4).

## 2. Per-ticket state and next action

### 2.1 W3-RM (PROGRAM item 3: reported model under (V), (L)) — DONE, awaiting HQ
* **State:** STATEMENT v1.2.1 locked (R01 LOCK-WITH-CHANGES → v1.1; post-lock weakenings → v1.2; wording-only v1.2.1)
  (`W3-RM/LOG.md`). Every lemma cross-family checked: R03 (L0/L1/L2), R04 Opus (SAND-R), R05 (E4 vs code; 84,000 calls, 0
  failures), R06 (batch 2; examples file had 4 MAJOR, fixed). Mid-point R07 CONTINUE. Sweep R08: 0 FATAL / 6 MAJOR (all
  in sharpness/necessity wording, fixed). Council C2 PASSED 9.8 / 9.1. CITECHECK 280 ranges / 0 failures.
  (`W3-RM/reviews/*_disposition.md`, `REPORT.md` §1.)
* **Open objections:** none blocking. Scientific gaps recorded in `REPORT.md` flags 1–2 and §6: (N)/(D-R) lattice
  condition remains; Form R needs a localisation clause; sharpness gate flagged every probed assumption `improvable`
  (`SHARPNESS.md` §6: V1 296/300, L1 138/140 vs old cap 89/140, N1 whole-lattice NA violated 90/180 while LS0 reaches S₀
  178/180).
* **Next action:** HQ decisions §1.2, label, commit. Follow-ups → §3.2.
* **Cost:** HQ time only.

### 2.2 W3-SAMP (PROGRAM item 4: sampler outputs as coded) — DONE, committed report, review files untracked
* **State:** STATEMENT v3 (locked v2 + BT1 strengthenings, accepted by HQ). SL1 lock; BT1 better-theorem; LC1, LC2 (Sol)
  lemma checks; MP1 mid-point CONTINUE; SW1 rerun 0 CRITICAL / 4 MAJOR / 16 MINOR / 8 EXPO, all fixed; council C1 9.1 /
  8.8, all gates PASS; 11 non-blocking items applied (`W3-SAMP/LOG.md` 18:12–18:45, `reviews/C1_disposition.md`).
* **Open:** NC_r necessity OPEN (labelled); P-START is a named input awaiting the item-2 ticket (`REPORT.md` flag 3, §6).
  Code finding for the paper: main reports only Rao–Blackwell PIPs (`REPORT.md` flag 2).
* **Next action:** commit the 5 untracked files (`reviews/C1_*`, `reviews/SW1_*`, `numerics/run_checks_v4.py`,
  `numerics/RESULTS_v4.txt`); label. **Cost:** none.

### 2.3 W3-POST2 (improvements to W3-POST posterior theorem) — DONE, awaiting HQ
* **State:** STATEMENT v1.2.1 (L01 lock → v1.1; R03b adoptions → v1.2). Line checks K-AE, K-BC, K-D, K2 (all VERIFIED or
  VERIFIED-WITH-AMENDMENTS); M01 mid-point CONTINUE; S01 sweep 0 FATAL / 2 MAJOR (numerics), fixed; council C1 8.6 / 8.6,
  all gates; citecheck 136 / 0 failures (`W3-POST2/LOG.md`, `reviews/C1_disposition.md`).
* **Open:** HQ approval of post-lock strengthenings and kill-budget ruling (§1.2). Item 2 of the original brief ("stretch
  with a kill budget", `HQ_DECISIONS.md`) — REPORT says all five brief items closed, none stopped; UNVERIFIED whether
  "item 2" here maps to claim E (REPORT header maps claims to W3-POST §4 numbering).
* **Next action:** HQ decision, label, commit. **Cost:** none.

### 2.4 W3-P6 (experiment for Decision D1) — PAUSED mid-grid; the only ticket that needs compute
* **State:** DESIGN v2 after R01 NO-GO (9 findings, all accepted; `W3-P6/reviews/R01_disposition.md`). Code: archive of
  main 2252d57, core unchanged vs 11dc9b7 (`W3-P6/LOG.md`). NOTS queue is **empty**; every running task was **cancelled
  2026-11-09 20:57:50** (Slurm `.err` lines in `/scratch/fb31/theory_w3/b2/slurm/`, 56 files with CANCELLED).
  On NOTS (`/scratch/fb31/theory_w3/`):
  - b1 (job 2651495, 320 tasks, n = 50): **298 RDS** (all `completed`, 0 `hpm_incomplete`); 22 missing:
    cs ρ=.5 s₀=8 p=250 (11), cs ρ=.5 s₀=4 p=500 (6), s5 p=250 (5).
  - b2 (job 2652199, 240 tasks, n ∈ {75, 100, 150}): **0 RDS**; 35 tasks had started (logs) and were cancelled.
  - probe01 (25 tasks): 10 result RDS (+2 FULL copies); the long probes (n = 100 p ≥ 250 except s5, n = 150, 200,
    (50, 2500), (100, 5000)) never finished.
  - `analysis/b1_summary.md` is stale (127 records at 19:32). Its Group A header is mislabelled: the columns headed
    "s0 | n | p | p/n" hold n, p, s₀, s₀/p — fix `summarize.py` before the final table.
* **Preliminary D1 reading — PRELIMINARY, n = 50 ONLY, NOT A D1 VERDICT.** K = ⌊n/2⌋ = 25, so every cell has p > K;
  p/n ∈ {1, 2.5, 5, 10}. "As coded" = reported HPM with the shipped cap ℓ_n + |S̃₀| (MR1; derived from the wide arm).
  Classes per DESIGN §3: posterior = F(HPM) > F(S₀) (S₀ not the posterior mode at this n), search = S₀ never scored.

  | design (factor strength) | s₀ | p=50 | p=125 | p=250 | p=500 |
  |---|---|---|---|---|---|
  | cs ρ=.3 (corr .3) | 4 | 19/20 (1 post) | – | 18/20 (2 post) | – |
  | cs ρ=.5 (corr .5) | 4 | 19/20 (1 post) | 19/20 (1 post) | 10/20 (10 post) | 8/14 (6 post; 6 not run) |
  | cs ρ=.7 (corr .7) | 4 | 11/20 (9 post) | – | 4/20 (16 post) | – |
  | cs ρ=.5 | 8 | 2/20 (18 post) | – | 0/9 (9 post; 11 not run) | – |
  | fac2 (2 factors, corr .60/.10) | 4 | 18/20 (2 post) | – | 16/20 (4 post) | – |
  | s5 (factor + groups of 5, corr .7/.3) | 4 | 20/20 | – | 15/15 (5 not run) | – |

  Facts across all 258 wide-arm fits (+ 40 mr1 validation fits):
  - **0 search failures.** Every miss is a posterior-mode failure (F(HPM) > F(S₀)). max |F_direct − F_ledger| = 0.
  - **cap ℓ_n + 2|S̃₀| changed the HPM in 0/258 fits** (MR1 HPM = cap2 HPM everywhere).
  - In all 179 successes S₀ was already the running HPM **before LS0** and after the SMC islands; provenance =
    calibration pilot (`pilot/gibbs_flip` 178, `pilot/nswap` 1). LS0 never supplied S₀.
  - For p ≥ 125 the start mode has size exactly K in 135/138 wide-arm fits and contains S₀ rarely (cs ρ=.5 p=500: 1/14;
    fac2 p=250: 1/20) — the regime of Theorem NEG; the method recovers S₀ through SMC, not through π₀/LS0.
  - Validation pairs (mr1 vs wide, same seeds, (50,50) and (50,125)): 40/40 identical on HPM, pre-LS0 HPM, start mode,
    seed, calibration tier.
  - Cost: median 0.6–1.25 h per fit at n = 50, p = 250–500 (tier 1 in every p ≥ 250 fit); (100,100) 1.8 h;
    s5 (100, 250) 3.85 h (probe01).

  Reading under DESIGN §6: **search component: no failure seen; cap question: no effect at n = 50; D1 overall:
  "insufficient evidence"** — one n only, so no n-trend; as-coded rates at n = 50 are driven by posterior failures that
  grow with ρ, s₀ and p (expected at s₀/n = 0.16 or corr .7) and fall under posterior concentration, not search.
  Implication worth HQ's attention (my reading, unreviewed): if the pattern holds at n = 75–150, a D1 proof would go through
  calibration/SMC discovery (W3-SAMP Theorem D style), not through LS0, and no LS0-cap change would be requested.
* **What remains:**
  1. b1 remainder: 22 tasks, same seeds, b1's frozen scripts (`runs/b1/scripts`, v2 driver; the v2 parity bug affects
     only fac2 with odd step — none of the 22). ≈ 20 core-h.
  2. b2 in full: 240 tasks (main sequence n ∈ {75,100,150} at p/n ∈ {1, 2.5, 10}; breadth at (100, 250)), frozen
     scripts_v3. DESIGN estimate ≈ 740 + 500 ≈ 1,240 core-h; wall ≈ 1–2 days at ≤ 150 concurrent (n = 100, p = 1000 cost
     is UNVERIFIED: no probe finished, > 3.3 h).
  3. Re-probe for the conditional cells: (50, 2500) for p/n = 50 and n = 200 p ∈ {200, 500} for group B (DESIGN §5:
     submit B only if a 22.5-h allocation passes the calibration pilot). ≈ 5 tasks, ≤ 115 core-h.
  4. Log the cancellation as a Slurm interruption (DESIGN §5 policy: rerun once with the same seeds, new RUN_ID).
  5. After completion: rederive + `summarize.py` (header fix), copy `analysis/` back to `W3-P6/results/`, REPORT.md,
     then a council on the REPORT (it is a D1 decision input).
* **Exact next action (needs owner greenlight — NOTS compute):** resubmit b1-remainder and b2 from
  `/home/fb31/projects/BVS/theory_w3/runs/{b1,b2}` with the same task tables (filter b1 to the 22 missing keys), new
  RUN_IDs, job prefix `w3p6_`, throttle ≤ 150; then the 5 probes.
* **Agents:** lead Opus 5.5 high (Claude Personal); council on the final REPORT: Astra high + Opus high (Claude Work).
  **Cost:** ≈ 1,250–1,400 core-h NOTS; 1 lead session + 2 council runs (+1 round if needed).

## 3. Other queued items (one-line plans)

1. **Start-mass rate (PROGRAM item 2; new ticket W3-START).** Prove π₀(S₀) ≥ 1 − n^{−c} under no leakage, and the
   primitive conditions behind W3-SAMP's P-START (`W3-SAMP/STATEMENT.md` l.76, l.184); deliverable consumed by SAMP C/TR
   and RM. Note from P6: on strong-factor designs at p > K the start mode excludes S₀ (above), so state it as
   "no-leakage designs" and do not expect it to cover D1. Full pipeline. Lead Fable 5.2 high (Claude Personal); lock and
   line checks Sol high; mid-point and better-theorem Astra high; council Astra + Opus (Claude Work). ≈ 12 agent runs,
   ≈ 4 h wall (W3-RM took 16:00–19:15 with this shape).
2. **W3-RM follow-up A — polynomial leakage |Q| ≤ n^b, b < ¼, design-agnostic (R02 P5; `W3-RM/REPORT.md` §6.1, MEDIUM,
   "3–5 proof days").** New ticket W3-RM2 reusing RM-0 and SAND-R; lead Opus high (Claude Personal), checks Sol, council
   Astra + Opus. ≈ 12–15 runs.
3. **W3-RM follow-up B — path-level "no-addition" condition replacing (N)/(D-R) (R02 P6; HIGH, open).** Exploration only,
   with an explicit kill budget (e.g. one Fable attempt + one Astra break review); escalate to a ticket only on a proof
   sketch that survives. ≈ 2–3 runs. Also queued, lower value: Form R leakage at √(log n/n) (P3b), joint block visibility
   (P4) (`REPORT.md` §6.3).
4. **Can W3-SCR's SCR-C + "certified & sparse w.p. → 1" supersede W3-RM's leakage condition?** My reading (unreviewed):
   not as stated. SCR-C needs s₀ = O(1) and a near-orthogonality floor φ_n(q_n) ≥ 2 log p/(2 log p + log n) + ε
   (`W3-SCR/STATEMENT.md` l.171–178), which strong-factor/correlated designs violate (CS ρ gives φ ≈ 1 − ρ), and it is
   conditional on {certified, |Ŝ| ≤ q_n}, whose probability → 1 is exactly the search claim RM supplies under (V)+(L)+(N).
   So it supersedes RM only where both hold and someone proves P(certified & sparse) → 1 without (L). Plan: one scoping
   memo (Fable 5.2 high, Claude Personal) + one Astra "break it" review comparing the hypothesis sets; HQ then decides
   between "SCR-C as a corollary/examples row" and a W3-RM2 merge. ≈ 2 runs, < 1 h.
5. **Merge PR #6 (theory/infra), then tag `theory-v2.0-pre`.** Local facts: `theory/infra` (worktree
   `C:/Users/felip/BVS-infra`) is 10 ahead / 2 behind main, pushed (`origin/theory/infra` = 35b5b36); its diff vs main is
   117 added files under `Theory_work/INFRA/` only, so conflicts are unlikely. PR #6 state/mergeability UNVERIFIED (`gh`
   not available in this shell). Order: commit the paused Wave 3 state (§1.5) → merge PR #6 (owner approval) → run
   `ingest.py` for W3-RM, W3-SCR, W3-POST2 → tag `theory-v2.0-pre` on that main commit and push the tag. ≈ 30 min HQ.
6. **Chapter v2.0 restructure.** Rebuild the theory chapter (`Theory_work/State_of_Project/` main.tex/sections; chapter
   v1.0 location UNVERIFIED) to PROGRAM's presentation rule: design-agnostic theorems in package order 1–6, families only
   in an examples table, statuses from the registry. Start after the tag and after the P6 reading (D1 decides whether the
   strong-factor row says "recovery" or "screening + limits"). Lead Fable 5.2 high (Claude Personal); council Astra +
   Opus. ≈ 6–8 runs.

## 4. Recommended relaunch order

1. **HQ housekeeping (§1):** amend the provider rule, record decisions for W3-RM / W3-POST2, apply labels, commit the
   paused state (owner approves the commit). Minutes.
2. **W3-P6 resubmission** (owner greenlight for NOTS): b1 remainder + b2 + 5 probes. Starts the longest clock first;
   runs unattended 1–2 days.
3. **PR #6 merge → ingest → tag `theory-v2.0-pre`** while NOTS runs.
4. **W3-START** (item 2) and the **SCR-vs-RM scoping memo** in parallel (independent).
5. **W3-RM2** (polynomial leakage), scoped by the memo's outcome.
6. **W3-P6 REPORT + council** when b2 lands → HQ records Decision D1 (proof ticket via SMC discovery, or "screening +
   limits").
7. **Chapter v2.0** after D1 and W3-START.
8. Path-level (N) exploration last, kill-budgeted.
