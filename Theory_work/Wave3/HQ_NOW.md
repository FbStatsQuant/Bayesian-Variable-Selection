# HQ now (resume card; HQ keeps this current)

## DATA OF RECORD: DESTINATION (owner 11-15)
- The laptop (Felipe_Bedoya) is often off when the owner is away. The **desktop (DESKTOP-955G53S, HQ's machine) is always on**.
- The owner gives a desktop local storage path on 11-16. Then the desktop becomes the primary destination for heavy data
  of record (NOTS → desktop; the desktop already has NOTS access), and the laptop route stays secondary/opportunistic.
  Until then, records stay on Owls NFS.

## PENDING OWLS T3 RESTART (agreed with BNP Lean HQ, peer; thread mcp:0a4bc001-e5d5-40be-b36a-3d4f45984c49)
- Purpose: set Claude Code's temp directory for the T3 server on Owls to NFS (e.g. /home/fb31/.claude_tmp/) to end the root-disk ENOSPC spikes.
- When: BNP sends a "quiet window" (expected 11-16 early afternoon CST). HQ pauses SMC departments' leads, restarts, verifies, then messages BNP back. BNP launches nothing until confirmed.
- BNP already moved its temp to /home/fb31/bnp_tmp and removed 73 stale sandboxes (11-15).

## RESUMED 11-16 16:00 CT (owner order)
- Theory and Engineering resumed on Claude Personal; Writing stays idle on Claude Work.
- **24 live SMC threads were switched from Claude Third to Claude Personal.** The 84 settled, finished threads were left as they are; they will not run again.
- POLICIES §5/§7/§8 updated: Claude Personal is the SMC default, and Claude Third is retired for SMC.

## PAUSE (owner, 11-16 ~10:40 CT): resources low
- Order: current agents finish their current task, then ALL operations cease. Resume on **Claude Personal after its weekly reset** (≈ 17:30 CT 11-16, per the owner's screenshot; Codex weekly reset ≈ 18:45 CT).
- Sent: Theory Dept, Engineering Dept and the consultant. Departments write resume cards: Theory_work/Dept/RESUME_2026-11-16.md and Docs/Experiments/P1M/RESUME_2026-11-16.md.
- Scheduled tasks disabled by HQ: Theory Dept heartbeat (45 min), Theory daily report, W3-READER S4 ping. Builders 6–7 start: disabled. Left running (no tokens): snapshot crons, desktop offload, NOTS jobs in flight. BNP's own tasks (guard 10:13 and backup 11:13 installs) are theirs; HQ only verifies the crontab diffs.
- BNP cancelled today's Owls slots (guard 10:13, backup 11:13); the SMC freezes are lifted; the crontab is verified unchanged against HQ's baseline. Both departments are STOPPED (resume cards: dept/theory db6bd259; Engineering Docs/Experiments/P1M/RESUME_2026-11-16.md). BNP is also paused; its T3-restart window comes after both resume.
- **OWNER 11-16 (during the pause): 1M fast-track APPROVED, "but I want no delays either".** First message to Engineering on resume:
  - produce, within its first working day, a fast-track plan for a **1M pilot fit before the advisor report (target Dec 1–4)**: 10⁵ and 10⁶ run side by side, the 1M pilot launches right after a short 10⁵ smoke test, and all 7 builders run at full speed from the resume;
  - the pilot is labelled "pilot", with overlap validation after;
  - **hard constraint:** the fast-track must not delay the main ladder or the January campaign. It runs as a side track; if the pilot fails, the main plan continues unchanged.
  - The plan states the Claude usage, the NOTS core-h per attempt (≈ 1k), and the gates.
- **OWNER 11-16: the Writing Department STARTS at the resume.** Assignment: Docs/Writing/ASSIGNMENT_1.md.
  - D2 (all consistency results in reader form, statuses verbatim): draft ≈ 6 h after the resume.
  - D1 (methodology as coded: priors, distributions, every parameter fixed or f(n, p), with code file:line): ≈ 24 h.
  - The Writing thread is already on Claude Personal. HQ orders one Sol read per document and shows the owner the PDFs.
- **For Engineering on resume (Writing D1 finding, 11-16):** the default v3_fit preflight is NOT memory-only. With ls0 = TRUE and cap ℓ_n+|S̃₀|, ls0_wc = TRUE (v3_fit.R:114) charges the LS0 worst-case time 2·(ℓ_n+K+1)·(p+p²/4)·(measured s per size-K score) against the allocated hours (:43-47, :65, :144-148).
  - At n = 200, p = 10⁴ that is ≈ 563 h on Owls, so a default fit returns resource_limit before setup. The README and the code comment (:25) say "memory-only".
  - Engineering: check how the overlap rung (10⁴) and the 1M plan set hours/ls0_cap, and which setting the 2,400-fit study and P6 used. Report the doc fix.
  - Theory is unaffected ((C2) assumes allocation ≥ the requirement formulas).
- **OWNER 11-16, after reading D2 v1 (binding direction):**
  - (1) A tight report and paper: the core theorems in the main text, the rest in a supplement with a one-line "why it matters", or cut. HQ's proposed core: rows 1.1/1.2, 2.1, 3.1, 3.6 (+ 3.5), and 1.3 as a remark. The owner's OK on the list is pending.
  - (2) Niche results are motivated in one sentence or cut.
  - (3) **Assumption audit.**
    - Assumptions on abstract mathematical objects (distributions, divergences, prior or kernel properties) must be proved: small checked lemmas, and Lean targets.
    - Design-matrix assumptions (and similar) get a **"why this is reasonable" dossier in the advisor report**: plain meaning, comparison with standard literature conditions, where they hold and fail, and whether our simulation designs and a typical user are plausibly inside. No empirical tracking.
    - Theory leads it; Writing presents it. The consultant stress-tests the core list and the audit plan. HQ proposes moving the freeze to include the audit (owner's OK pending).
- **HQ decision 11-16 (owner: "open for you to decide").**
  - The core list is ADOPTED.
  - The Fri 11-20 freeze STANDS for recorded statements. The audit (W3-AUDIT) is the next campaign, adding lemmas and corollaries after the freeze; a draft of its first version ≈ 3 working days after the resume, ahead of the advisor report.
  - Brief: Theory_work/Wave3/W3-AUDIT/BRIEF.md: tracks A (proved), B (reasonableness dossier, with Song–Liang as the reference point, "blank check" if same or weaker) and C (internal empirical proxies, ≤ 150 core-h).
- **OWNER 11-16: at the resume, ON THE OWNER'S ORDER (wait for his word),** the Fable consultant reviews the **sub-optimality policies** for improvements:
  - the sharpness gate, the S findings and better-theorem notes, supersession/rollback to better theorems, the optimizer, and the new W3-AUDIT track D;
  - sources: PROTOCOL_v4 (§ supersession, sharpness), memory optimality-risk-feedback, W3-AUDIT/BRIEF.md.
- **OWNER 11-16 (scope):** the theory is nearly done; the core analysis rests on what we have.
  - Improvement work covers only the core theorems and key components; track D is light, with ≤ 3 tickets and kill budgets, and no effort on niche results.
  - The Fable policy review is aimed at **the company playbook for future papers** (the owner is on board with protocol optimisation); it does not reopen this paper's theory.
- **On resume:** move the department threads to Claude Personal (t3_thread_configure), then send each manager "resume from RESUME card". Pending HQ items:
  - V (RM2-R) real-run GO after rule (b) and the dry run;
  - re-enable the 3 Theory scheduled tasks;
  - the builders 6–7 start;
  - re-plan the freeze date (was Fri 11-20).

## MORNING BRIEF 11-16 (items for the owner)
- p = 1M: re-sized (H-9, HQ overnight) to ≈ 28.3k core-h with G = 256 socket-local (≈ 1.44× plan per pair); AR-weak at 1M dropped (returns first if L5 saves); a reduced 1M self-check (N = 5,000) kept. M risk priced after T5. Schedule: with descope (c, approved) the first 1M fit is in the first week of January. Options for the owner:
  - (b) Fable 5.2 architect for WP3, ≈ 3 days (HQ recommends yes);
  - (a) 7 Opus builders, ≈ +40% Claude Third for ~3 wk (only with b, and only if the accounts allow);
  - a+b+c → ≈ Dec 21–23, but no slack.

  Card: Docs/Experiments/P1M/RECOVERY_OPTIONS.md.
- The desktop storage path (D: has ~3 TB free) and the Task Scheduler OK for hourly pulls.
- The Owls T3 restart in BNP's quiet window (early afternoon).
- The pacing plan for the day (accounts, Codex level).

## USAGE NOTE (owner, 11-15 ~21:30 CT; all times Central)
- Tonight: keep the rhythm. Tomorrow (11-16) probably pace down a bit: Claude Third is burning about a week of Ultra in
  about 2.5 days (new account, odd reset schedule). The two companies together used ~2B tokens in ~4 h; this pace is not
  the norm.
- HQ on 11-16 morning: check the account and Codex meters, then propose a pacing plan to the owner (concurrency per
  department, account split, Codex level) before the departments ramp up.

## CODEX PACING LEVEL (owner sets; POLICIES §14): **0 (normal)** since 2026-11-15

## ACCOUNT ALLOCATION (owner sets; HQ relays to all managers)
- Current (2026-11-15): department agents on **Claude Third**, except Engineering WP2 + WP5 builders/reviewers on **Claude Work** (HQ overnight 11-15 ~23:18, pending the owner's review); HQ and the Writing Department on Claude Personal.

## PRIORITY ORDER (owner 2026-11-15, evening)
1. All consistency results (selection + distribution / W3-DIST) **and their Lean parts** come first.
2. Parallel-method theory (T-MERGE, EVAR, POOL) is NOT a priority now; parked for the scaling paper.
3. **Engineering: make p = 10⁶ work** (owner 11-15: "I need the 1 mil to work out … cherry on top … impressive paper"). Plan A+D approved (≈24.6k core-h). HQ tracks: G0 kernel speed on NOTS → EXP-CP1 v2 (Sol fold-in) → 10⁴ overlap and precision → 10⁵ rung → first 1M fit. Unblock fast.

## TOP PRIORITY (owner 2026-11-15): W3-DIST — distribution consistency (Song–Liang Thm 1–2 parity)
"It needs to happen." It outranks W3-PATH, T7 and the riders in every resource conflict. Lead: Fable 5.2 on Claude Third
(Owls, thread mcp:launch:75635c1f…); team of Opus/Sonnet workers on Claude Third after CP1; parity checklist = BRIEF
addendum A1 (P1–P6). Restore points: hourly cron → branch theory/W3-DIST. Any extra resource (2nd Fable, OpenAI review
budget, CP reset use) → ask Felipe at once, framed as "needed for W3-DIST". Target: proved and in chapter v2.0 this week.

## DEPARTMENTS / ACTIVE THREADS (HQ babysits; Owls, Claude Third)
Operating model (owner, 11-15): HQ = CEO; each big effort is a top-level "department" thread (brief + branch +
restore points + checkpoints); the owner may talk to any department directly; HQ gates spend and launches.
- W3-READER (Opus): mcp:launch:2a4462b2… → CP1 (claims card by the five pillars; reader versions; notation; method intuition).
- **SMC - Theory Department** (running; Opus 5.5 high, Claude Third, Owls): mcp:launch:21e33dae…; brief `Theory_work/Dept/BRIEF.md`;
  worktree /home/fb31/BVS-wt/THEORY-DEPT, branch dept/theory. Owns: riders queue, T-PART (with Engineering OD-5),
  parallel-SMC campaign proposal by Thu. Since the 11-15 evening handover (owner) it also manages W3-DIST, W3-READER and the recorder; HQ keeps CP3 acceptance, headlines, merges, API.
- Handbook for everyone: `POLICIES.md` (repo root). Departments push their own branches and open PRs; HQ merges.
- **Owner batch (when Felipe asks):** Engineering OD-1 fixed N, OD-2 E2 escalation, OD-3 B2-3 cost column, OD-5
  partition (T-PART), OD-8(b) per-particle streams [OP-law] (dept recommendation); after ENGINEERING_SPEC v1.
- **SMC - Writing Department** (set up, idle; Opus 5.5 high, **Claude Personal**, Owls): mcp:launch:e2cf7ee6…; brief
  `Docs/Writing/BRIEF.md`; worktree /home/fb31/BVS-wt/WRITING, branch writing/main, snapshot commit-in-place :02/:17/:32/:47.
  First assignments planned: chapter v2.0 (after the freeze), advisor report (from ~11-23).
- **SMC - Lean Department** (future; owner 11-15: launch "when we have more material": i.e. once stable checked headline theorems exist, earliest after the theory freeze / W3-DIST CP3; workspace READY: Lean/BRIEF.md, Lean/BVSCert, worktree /home/fb31/BVS-wt/LEAN; thread to be launched by HQ, not yet created; GO = owner + HQ): Lean/BRIEF.md, worktree /home/fb31/BVS-wt/LEAN.
- Candidates next: Parallel-SMC theory + evidence variance (after the freeze).
- W3-DIST lead (Fable 5.2): mcp:launch:75635c1f… → CP1 pending. API attempts after CP1. Snapshot cron */15 → theory/W3-DIST.
- **SMC - Engineering Department** (was "Experiment p = 1M"; renamed by owner 11-15; Opus 5.5): mcp:launch:dac077c2… → EXP-CP1 (plan). Owls has NOTS access (since 11-15). Snapshot → exp/P1M.
- PR #10 (Actions CI): merge after the editorial-pass citecheck fixes. Protocol: PROTOCOL_v4.md (NORMAL mode).

## sharp2 riders (API sharpness batch 11-15, triage `API_AUDIT/sharp2/TRIAGE.md`; A 17 / B 11 / C 0 / D 2; ~8 real)
Run under PROTOCOL_v4 (Tier B unless a new key lemma appears), Opus, after W3-DIST in priority:
- START2 v1.5 (~8–10 h): T10 Gaussian-row rate √(log n/n) (2^{s₀} reference sets, |H_l| ≤ e^{κ√log n}) + T8
  (visibility at log n + 2 log p; keep the (V-m) negative price term, L4_VIS Step 5). T9/T11 only if time allows
  before the Wed freeze.
- T12 PSHARP Prop A: expectation lower bound for every p, constant √((a+½)/π) (~3 h), before the chapter's sharpness
  section.
- T13 MISR Cor-G(a)/Cor-H restatements (~2–3 h).
- Editorial pass: LEAK-0 "sharpens" wording (START2 STATEMENT:87-88); MISR ASSUMPTION_MAP:27 cross-cite PSHARP; do not
  present START2-P1 as a p ≫ n gain.
- From consultant cards (11-15):
  - **W2-APP:POST@1.0.1 check** (Tier B line check by Sol of `Wave2/W2-APP/lemmas/L1_POST.md`). This is the Gaussian-row
    headline's weak point (RM2-R and MISR depend on it); priority right after W3-DIST.
  - START MIS/EX/F1/F3/F4 restated under START2's hypotheses (cheap rider).
  - C-MIS → MISR supersession later, once MIS(i′) reaches c > c₀ or Remark P becomes a checked row.
- Named open problems, no tickets: RM2-R aggregated leak; START MIS with a general μ; Ex-Equi b < 3/8; the START2-O1
  count.
- For W3-DIST after CP1 (not before): MISR Cor-G(a) makes a candidate run an exact DIST (RD) instance (a Song–Liang
  Thm 4 analogue for free if β^𝒞 is strictly sparse); drop "σ*² fixed" via MISR Lemma R′; DIST-1 "sharp" needs a
  written lower bound.
- Headline statements that would change (stronger): START2 (T1⁺)/(T3⁺)(b) with IF-START⁺, PSHARP Cor A1, RM2-F
  (via T4). HQ decides under v4 §8 and informs the owner.

## ADVISOR REPORT (owner, 2026-11-15): end-of-semester progress report, due ~3 weeks (~Dec 4–6; exact date TBC)
Contents (owner):
1. the 2,400-fit study: posterior-estimation accuracy and BVS results;
2. a concrete list of the most important theorems as of then (from the headline claims card);
3. a concrete plan for the p = 1M experiment (from the Experiment department's EXP-CP1).

Also (owner): an **intuitive explanation of the whole methodology** before the formal setup: what problem each stage
solves (start tables / start mode, the tempered SMC stages, calibration, local search LS0, islands and pooling, the
reported outputs), with a pipeline figure and a small worked toy example; then the formal definitions.
Standard: thorough setup and notation section; every symbol defined before use; notation table; no internal ids;
intelligible to peers (PROGRAM "Readability" → notation).

Plan:
- start Mon 11-23, after the theory freeze;
- writer: the Owls briefing thread (it built the 11-13 status PDF);
- LaTeX PDF, ~15–20 pages;
- one fidelity check of numbers vs sources (Sol);
- draft to Felipe ~11-30, final ~12-03.

Open: does the 2,400-fit study need the v3.2 rerun (RERUN_SPEC: the published tables use pip_plain and the cost
column, which v3.1 does not emit; ~910 core-h), or can the report use the existing results with a version note?

## STRIKE PLAN week of 11-16 (owner: theory basically DONE by end of week, then p = 1M experiment)
Definition of done: 11 main results recorded PROVED-CHECKED; D1 settled (theorem or stated limit); chapter v2.0
council-passed and frozen; editorial pass merged. Anything else = named open problem in the paper.
- Mon 16:00 (furnace): D1 from P6 stage 1 (Opus) · W3-PATH scoping→CP1 (Fable, ≤ 1 day) · T7 scoping (Opus) · RM2 riders
  T2 + T4 as ONE Opus leg (T6 already in RM2 v1.4; T4 enlarged by sharp2: additive BM-W floor + Ex-Proxy with decaying θ) · chapter v2.0 assembly starts (Opus) on the recorded claims · Sun-API findings triaged.
- Tue: W3-PATH proof leg only if CP1 = GO, kill budget 2 attempts on the key lemma, hard stop Wed 23:59 · T7: 1 attempt.
- Wed: freeze theory content. Whatever is unproved → "open problem" section. Chapter v2.0 complete draft.
- Thu (full reset): chapter v2.0 council (Sol + Opus) + fixes; final API audit of the chapter.
- Fri: council pass → freeze, merge. Theory campaign closed; hand over to W3-SCALE / p = 1M.
Parallel-SMC theorems: only what the p = 1M experiment needs (output-identical engine ⇒ inherited guarantees), as a
short Opus note; the rest moves to the scaling paper.

## PLAN (owner, 2026-11-12 ~12:00 CT) — see HQ_DECISIONS same date
- Now → weekend: finish current campaign on remaining CP fuel, NO resets. ≤ 1–2 Claude threads. R06 → record W3-START,
  START2, PSHARP, MISR (per-claim seat addenda), RM2 (R1 snapshot + carrier). P6 stage 1 on NOTS (watcher every 3 h).
- Sun 11-15: $200 API credit — precision strikes only (audit + sharpness of new tickets ~$50). Owner raises Console limit.
- Mon 11-16 16:00 CT: furnace on (weekly reset): Opus volume; Fable only for W3-PATH lead + stuck key lemmas. Queue:
  D1 (P6), W3-PATH scoping→proof (brief ready, BVS-wt/W3-PATH), T7 + RM2 riders T2/T4 (Opus; T6 done in RM2 v1.4), chapter v2.0 + council,
  editorial pass (MINORs + Prop-F wording + PSHARP E1–E9 + MISR/START2 errata + C-MIS citecheck: 6 line-drifted cites into SoP 04_theory.tex, CI 11-13; W2-FAC-X reviews/citecheck.py 0→2: path prefixes miss W2-FAC-A/B REPORT cites, script fix + refresh CITECHECK.txt). Then merge PR #10 (Actions CI) once its run is green. Mid-week full reset (owner) when budget ends.
- Codex: let it recover, no reset; one reviewer per gate.
- Providers: everything on claude-personal (CP) for now; consultant = CP Fable 5.2 (operational decisions); owner = big
  picture + tokens, one daily batch. Pending owner calls: supersessions RM-F/R→RM2-F/R, C-MIS→MIS-R, 8 START claims→START2.


Mode (owner, 2026-11-11 ~18:45 CT): **continuous** — keep work running on Claude Work (effort ≤ high) until CW runs
out or a key owner decision is needed; no bursts. HQ answers checkpoints itself. HQ thread 647bfd65-83bc-403a-b3b0-0a8352044e7f. Meta-HQ watcher (Sol, every 30 min): thread 600e6dcd-e2bf-4ef8-9a4b-0e00d46a1c68.

Felipe away until ≥ 07:00 CT 11-12: implicit approval to advance checkpoint → next leg when reviews are clean (no open FATAL/MAJOR, council ≥ 8.0). Reserved items stay reserved.
CW budget: resets ~2026-11-12 13:10 CT (18 h from 19:10 CT 11-11) — use CW fully until then.

## RESTART DONE (2026-11-12 01:05 UTC): T3 restarted; all Claude sessions on .claude-work (Team); both leads resumed fresh-context; MP1 output existed (no relaunch); SC5 relaunch delegated to W3-START lead.
## (old) RESTART NOTE (2026-11-12 01:05 UTC) — read first after a T3 restart
Account fix: T3 was still launching Claude sessions with config `.claude` (Personal login). HQ copied memory, CLAUDE.md,
settings.json and skills into `.claude-work` (Team). Both leads were cancelled to stop Personal use; their files are on
disk. To resume after T3 restarts: (1) confirm new sessions write under `C:/Users/felip/.claude-work/projects`
(find -mmin -2); (2) re-send each lead its fresh-context resume message (W3-START: continue CP3 R2 plan in its LOG/
CHECKPOINT_3; W3-RM2: CP2 leg per LOG HQ CP1 decision; its MP1 Astra review was cancelled with it → relaunch if no
output in reviews/); (3) P6 smoke still on NOTS — heartbeat re-wakes the P6 lead when done.

## 2026-11-12 05:15 UTC — resumed after CW 5-h limit (02:42–~04:00 UTC). SCALE/MISR/PSHARP re-woken; RM2 CP2 accepted → Form R leg; W3-START R2 PASS → acceptance audit delegated (Opus CW). Watchdog run 03:31 failed (rate limit) — next 09:01 UTC.

## 2026-11-12 10:05 UTC (04:05 CT) — 2nd CW 5-h limit hit ~06:05–06:41 UTC (6 leads + helpers burned the window in ~1 h). Throttled: resumed R05, RM2, MISR, SCALE only; PSHARP waits for R05 to finish (then resume it). Keep ≤ 4 Claude leads per window. P6 smoke: 3/4 done, task 4 running 11 h. Watchdog 09:31 failed (rate limit).

## Running
- INFRA R05 fix (Opus CW, branch infra/R05-ckpt-status): CHECKPOINT status source + 5 safeguards + Sol review → then re-run W3-START acceptance (branch 808ddd1), merge, ingest 21; BT2 P1–P4 → W3-START2 ticket.
- W3-MISR lead (T1, Fable 5.2 CW) → CP1 → CP2.
- W3-PSHARP lead (T3, Fable 5.2 CW) → CP1 → CP2.
- W3-SCALE lead (Fable 5.2 CW, leg A → CP1; cap 150 task-h on NOTS).
- W3-RM2 lead (Fable CW, BVS-wt/W3-RM2) → CP2 (CP1 passed; v1.3, Form F key lemma).
- W3-START lead (Fable CW, BVS-wt/W3-START) → CP3 again: R1 council PASSED (9.1/8.8) but acceptance refused (wave docs in INPUTS changed on main) → v1.3.4 + Sol diff check + council R2 + reconciliation + Astra BT2. After R2: HQ acceptance audit, ingest 21 claims, merge; then blind Fable API audit of the package (credits).
- INFRA R04 fix MERGED 656982a; rule 16 lifted.
- W3-P6 smoke S1–S5 on NOTS (jobs 2689422/3); heartbeat re-wakes the P6 lead when done → CP1 (stage-1 plan).
- API audit (Console credits, not CW): pass 2 final 79 OK / 13 MINOR / 0 GAP (pass2b done); pass3 (50
  factor-design PROVED claims) done: 42 OK / 5 MINOR / 3 GAP (stopped tickets, no consumers) → R-AUD2 confirmed; SUSPECT marks applied (no checked/chapter impact). Audit plan complete.

## Next (HQ self-approves, in order as slots free)
0. W3-RM2 next leg (after CP2): add T6 (product-form localisation) next to P3. After RM2 council: T2(a–c) + T4 riders; then T7 (kill-budgeted). (sharp1/sharp1b TRIAGE)
1. Each lead's next checkpoint (CP1 → CP2 → CP3) after HQ acceptance audit.
2. P6 stage 1 release within the 1,896 core-h ceiling (approved).
3. Editorial pass: pass-1/2/3 MINORs + C-DLV:Prop-F wording (version bumps, no claim changes).
4. Chapter v2.0 once D1 (P6) and W3-START land.

## Waiting on Felipe (key decisions)
- (decided by HQ + consultant 2026-11-12, see HQ_DECISIONS) track 3 leg A launched; SAMP D/TR approved; track 1 not ready.
- For Felipe: API month spend ≈ $171 of the $195 limit — the 11-15 grant needs a higher limit to be usable before Dec 1.
- For Felipe: p = 1M fixed-N islands; primary PIP switch; TR sharpness (coded target); track 1 may shrink to a gate-0 sample.
