# HQ now (resume card; HQ keeps this current)

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
  parallel-SMC campaign proposal by Thu. HQ keeps W3-DIST, W3-READER, CP3 acceptance, headlines, merges, API.
- Handbook for everyone: `POLICIES.md` (repo root). Departments push their own branches and open PRs; HQ merges.
- **Owner batch (when Felipe asks):** Engineering OD-1 fixed N, OD-2 E2 escalation, OD-3 B2-3 cost column, OD-5
  partition (T-PART), OD-8(b) per-particle streams [OP-law] (dept recommendation); after ENGINEERING_SPEC v1.
- **SMC - Writing Department** (set up, idle; Opus 5.5 high, **Claude Personal**, Owls): mcp:launch:e2cf7ee6…; brief
  `Docs/Writing/BRIEF.md`; worktree /home/fb31/BVS-wt/WRITING, branch writing/main, snapshot commit-in-place :02/:17/:32/:47.
  First assignments planned: chapter v2.0 (after the freeze), advisor report (from ~11-23).
- Lean (READY, not started; GO = owner + HQ): Lean/BRIEF.md, worktree /home/fb31/BVS-wt/LEAN.
- Candidates next: Parallel-SMC theory + evidence variance (after the freeze).
- W3-DIST lead (Fable 5.2): mcp:launch:75635c1f… → CP1 pending. API attempts after CP1. Snapshot cron */15 → theory/W3-DIST.
- **SMC - Engineering Department** (was "Experiment p = 1M"; renamed by owner 11-15; Opus 5.5): mcp:launch:dac077c2… → EXP-CP1 (plan). REQUESTS.md = NOTS queries for HQ. Snapshot → exp/P1M.
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
