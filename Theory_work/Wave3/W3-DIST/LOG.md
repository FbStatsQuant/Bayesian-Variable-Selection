# W3-DIST — LOG (heartbeat; local time = America/Chicago, CST)

Agents so far (model, provider, role):
- Lead: Claude Fable 5.2, Claude Third (`claudeAgent_claude_third`), effort high.
- Helper H1 "prior probe": Claude Opus 5.5, Claude Third, high — brief `briefs/BRIEF_prior_probe.md`, output `work/prior_probe/`.
- Helper H2 "numerics harness": Claude Sonnet 5.5, Claude Third, high — brief `briefs/BRIEF_numerics.md`, output `work/numerics/`.
- Reviewer S1 (blind read; statement lock + better-theorem): gpt-6-astra, codex, reasoningEffort high — `reviews/`.
Claude inference tally: all on Claude Third (lead + 2 helpers). OpenAI: 1 Astra read.

## Entries
- 2026-11-15 15:32 CST — `git pull --ff-only` (1610990 → 9f45132). HOLDS.md read: no holds. Read BRIEF, PROGRAM, PROTOCOL.
- 15:34 — HQ steer: second `git pull --ff-only` (→ 4d7826b, ADDENDUM A1; working tree later at cef2c32 by HQ's own
  commit). HOLDS: none. Read SONG_LIANG_MAP, W3-POST2 STATEMENT + D_hellinger, T04 STATEMENT/STATUS/FINAL_REPORT,
  I4_SL_corollaries, Song–Liang pp. 949–956 (PDF pages 3–10), W3-POST STATEMENT, registry statuses.
- 15:40 — HQ steers A2 (DEPS.md, STATEMENT changelog, sharpness gate) and A3 (team) received and adopted.
- 15:47 — Code read for P6 (core = 4676af6; `git diff --stat 4676af6 HEAD -- Scripts/SMC_BVS/core` empty at cef2c32):
  `v3_run.R:141-163, 170-173, 210`, `cpp/v3_ledger.h:43-56, 78`, `cpp/v3_core.cpp:358-366`; W3-SAMP STATEMENT + CC.
  Finding: the run returns HPM, island and pooled RB PIPs, MPM, log Ẑ and the scored top store (40p + 1 models with F);
  **no particles, no coefficient or variance draws, no predictive**.
- 15:50 — `orchestrator_capabilities` called; codex (gpt-6-astra) and Claude Third available. H1 and H2 launched (async).
- 15:52 — HOLDS read: none. Writing PLAN, STATEMENT v1.0, ROUTES, DEPS, ASSUMPTION_MAP.
- 15:58 — Read W3-POST2 Claim B's proof and A_occam's (C5′): the size tail's weak failure probability comes only from
  Markov/Chebyshev steps that have χ²/Gaussian replacements; Lemma S re-rated low–medium. STATEMENT v1.0.1 (t-range
  n^{1−κ₀}; s₀ ≤ s₀^r), tagged EQUAL. HOLDS read: none.
- 16:09 — H2 (numerics) completed: R = 40 per cell, exact enumeration p = 12, restricted family for p ≫ n. Nothing
  contradicts a candidate statement; readings in ASSUMPTION_MAP §3. Added `work/numerics/.gitignore` (68 MB of
  regenerable arrays; note for HQ's snapshot cron).
- 16:15 — H1 (prior probe) completed: [SL] (9), (10), (11), "r_n ≻ 1" fail for the coded prior ((11) corrects the lead);
  (14) holds; sieve route incompatible when log p → ∞; direct conjugate route supported, with a new Lemma V; an
  exponential size tail at s₀ + O(u) without a floor refuted by duplicates. STATEMENT v1.0.2, DEPS v1.1 (EQUAL edits).
  HOLDS read: none.
- 16:16 — Manifest S1 frozen: fb6d0dab98b8083273c1df73693af90831329776915737bda397c39ec024b62e (106 files, 18 extra
  inputs). Blind read S1 launched (gpt-6-astra, codex, reasoningEffort high; brief `reviews/BRIEF_S1_astra.md`).
  No manifest-covered file is edited while it runs.
- 16:58 — HQ steer A4 (protocol v4; Tier A, NORMAL). `git pull --ff-only` (→ fe9a1d7); PROTOCOL_v4.md not yet on main.
- 17:45 — HQ note on W3-POST2 Claim D (D(b) repaired after council; diff round in progress): recorded in the consumes
  table. `git pull --ff-only`: PROTOCOL_v4.md on main; read §3, §4, §6 and H1–H5. HOLDS read: none.
  Blind read S1 back (`reviews/S1_astra.md`, written 17:41): GO-WITH-REPAIRS; 5 MAJOR, 5 MINOR, 1 NIT; Lemma T
  FALSE-AS-STATED on part of its range (DEPS: T REFUTED in its v1.0.2 form; dependents DIST-1, DIST-2 — repaired range
  used, no target clause weakened); bridge B1 exponential clause refuted (no dependents among target clauses).
- 17:48 — STATEMENT v1.1 (all S1 findings and the four better-theorem proposals adopted; changelog table at the foot,
  v4 §4.2 form); ROUTES v1.1; ASSUMPTION_MAP v1.1; `reviews/S1_disposition.md`.
- 17:51 — TARGET.md (v4 §3.2), API_CARDS.md (steer A4 item 6), DEPS.tsv (v4 §4.1 form, by hand with sha256; all rows
  UNCHECKED). HOLDS read: none.
- 17:55 — CHECKPOINT_1.md written. Run ends with CP1 as the final message. No work past CP1 without HQ's go.
  Agents this leg: lead Fable 5.2 (Claude Third); H1 Opus 5.5 (Claude Third); H2 Sonnet 5.5 (Claude Third);
  S1 gpt-6-astra (codex, high). No other agents. No git command beyond `git pull --ff-only` (4 times) and read-only
  `git log`/`rev-parse`/`diff --stat`/`branch --show-current`.
- 17:53 — Completion notice of the S1 Astra task received; its summary matches the report file already dispositioned (5 MAJOR, 5 MINOR, 1 NIT; GO-WITH-REPAIRS). No change to CHECKPOINT_1.md or any statement. HOLDS read: none.
- 18:10 — HQ steer A5 (owner: readability; reader versions; bridges on the critical path) and its correction (clarity,
  not a copy of Song–Liang's form). `git pull --ff-only` twice (→ aa79ecd): PROGRAM "Readability" and PROTOCOL_v4 H6
  read. HOLDS read: none.
- 18:15 — STATEMENT v1.2: §1R reader versions (Theorem A, Theorem B, Corollary C; assumptions (A1)–(A6)); bridges B0,
  B1 (primitive form), B2-core, B2, B3 stated; W3-MISR:R′@1.0.0 consumed for B0 (σ* arbitrary). TARGET §6 (reader
  versions, one line per assumption, TC9/TC10); ROUTES §2b; API_CARDS card B; ASSUMPTION_MAP §4; DEPS.tsv rows and sha
  refreshed (DEPS.md v1.3). Changelog rows tagged NEW-CLAIM / STRONGER / EQUAL; no target clause weakened.
- 18:16 — Same-family pre-check P1 launched: Claude Opus 5.5, Claude Third, high (brief
  `briefs/BRIEF_P1_reader_precheck.md`; output `reviews/P1_opus_precheck.md`). It is a filter, not a review layer; the
  cross-family check of the reader versions and of the v1.1/v1.2 tags stays with HQ to order. CHECKPOINT_1.md will be
  revised after P1 returns.
- 18:17–18:20 — HQ notes on presentation (house style; then "nothing taken from other papers"; then the settled
  note: the two papers mark the level of clarity only, the form is the lead's choice). Pulls → 965af2a. A draft
  modelled on the owner's paper was written in the scratchpad only and deleted; nothing from it entered the ticket.
- 18:28 — P1 back (`reviews/P1_opus_precheck.md`): REPAIRABLE; 3 MAJOR (wording), 6 MINOR, 7 NIT; no reader clause
  false under its faithful reading. DEPS: B2's v1.2 determinant formula wrong (same conclusion by interlacing) —
  repaired, dependents unchanged. STATEMENT v1.3 (final reader form: setup, (A1)–(A5), Theorem A with displays (i),
  (ii), statement without (A4), example, Theorem B with (A6), Corollary C, notation table; bridges repaired);
  TARGET §6 rewritten; ROUTES §2b, API_CARDS card B, DEPS.tsv sha refreshed (DEPS.md v1.4); `reviews/P1_disposition.md`.
- 18:35 — CHECKPOINT_1.md revised (reader theorem first; bridges in kill budgets and plan; TC9/TC10). HOLDS read: none.
  Run ends with the revised CP1 as the final message. Agents this leg: lead Fable 5.2; H1 Opus 5.5; H2 Sonnet 5.5;
  P1 Opus 5.5 (all Claude Third); S1 gpt-6-astra (codex, high).

## Proof leg (HQ GO at CP1, restore point RP W3-DIST CHECKPOINT_1, branch theory/W3-DIST @ 8eec1b5)
HQ decisions recorded: TC1–TC9 fixed (TC10 = companion results); kill budgets of CHECKPOINT_1 §5 approved; early
checkpoint on WEAKER TC1–TC9, X exhausted, B2-core → Gaussian only, B0 → fixed σ*; CP2 soft; API attempts incoming under
`work/api_attempts/`; second Fable decided after S-FIT attempts.
- 2026-11-15 18:45 CST — `git pull --ff-only`; HOLDS read: none. STATEMENT v1.3.1 (editorial: earlier review verdicts
  removed from the body for blind-read hygiene); DEPS.tsv sha refreshed (f8ff769760f69064).
- 18:46 — Manifest S2 frozen: 54cf9123be0545bfba5228560af875214bfade4d4ca2c402780a082beae4206f (105 files, 7 extra
  inputs; state at freeze — workers add files under `work/` only; STATEMENT, TARGET, ROUTES are not edited while S2 runs).
- 18:47 — Launched (all async): S2 blind read — gpt-6.1-sol, codex, high (`reviews/BRIEF_S2_sol.md`; reader versions,
  bridges, changelog tags). Stream B — Opus 5.5, Claude Third (`briefs/BRIEF_B_transfer.md`: H, T, DIST-3). Stream C —
  Opus 5.5 (`BRIEF_C_size.md`: S, V, X1–X2). Stream D — Opus 5.5 (`BRIEF_D_output.md`: P6, DIST-C, Corollary C).
  Stream E — Opus 5.5 (`BRIEF_E_bridges.md`: B0–B3, assembly; critical path). Stream F — Sonnet 5.5
  (`BRIEF_F_numerics.md`). Common rules: `briefs/COMMON.md`. Stream A (lead, Fable): Lemma X steps X3–X4, in `lemmas/X.md`.
  Agent tally this leg: 5 Claude workers (Claude Third) + 1 codex Sol.
- 18:51 — Stream A: `lemmas/X.md` v0.1 written (steps X1, X3, X4 and the assembly of Lemma X with explicit constants: C_A = 3A + 5, C′ = 12A + 68, c = 1/2; Lemma X′ in §5). Inputs from stream C fixed in the exact forms (I-X2), (I-S), (I-V). DEPS.tsv rows X, X′ updated (UNCHECKED). Proof attempt 1 of 3 on X (kill budget). HOLDS read: none.
- 19:05 — HQ delivered API attempts (`work/api_attempts/dist1/`, 21 files; H3: proof material only). Read X-d-1
  (adversarial: no counterexample; (C) cannot be dropped) and X-b-1 in full; skimmed X-a-1, X-a-2, X-b-2, T-a/b/c.
  Decision (lead): main proof of Lemma X := the fractional-moment route of X-b-1 (`lemmas/X.md` v0.2, §0–§8 reproduced,
  §9 Lemma X′ and §10 check notes by the lead); the lead's truncated-moment proof kept as `lemmas/X_route_a.md`
  (independent derivation). Lemma X is now self-contained modulo locked [P1]; it no longer consumes stream C's S, V,
  X12 (which stay as independent versions and as the proofs of the stated Lemmas S and V). [P1] citations verified
  to exist; five items flagged for the line check (X.md §10). DEPS.tsv rows X, X′ updated. HOLDS read: none.
  API files for stream owners (C: S-*, V-*; B: T-*; E: B-*) will be attached to each lemma's pre-check as comparison
  material, since the streams are mid-run.
- 18:56 — Pre-check P2 launched on `lemmas/X.md` v0.2 (Lemma X, Lemma X′): Claude Opus 5.5, Claude Third, high; brief `briefs/BRIEF_P2_X_precheck.md`; comparison material X_route_a.md and API attempts X-a-1, X-a-2, X-b-2, X-d-1. Filter only; the Astra line check of X follows its disposition. Agent tally this leg: 6 Claude (Claude Third) + 1 codex Sol. HOLDS read: none.
- 19:15 — Stream D completed (`work/D_output/P6_DISTC.md`, `COR_C.md`; DRAFT): P6, DIST-C (C-0)–(C-iv), Corollary C
  proved taking DIST-1/2/3 as given; retention proved from the store rule; 33 code pins re-verified. Statement-change
  requests queued (STATEMENT is not edited while S2 runs): SCR-1 (C-iii) needs e^{−ct} ≤ ¼; SCR-2 (C-i)'s "λ = 0, π(𝒯) ≥ η"
  parenthesis is not an instance of the display (replace by the threshold form for a ∈ (0, 1]); SCR-3..5 editorial;
  Corollary C reader text: the returned list is the best of the final-run ledger, which also holds block-table and
  calibration-inherited models; stopped runs return a partial store; weights are returned as logs. None touches
  TC1–TC9 (DIST-C deterministic transfers unchanged; Corollary C is TC10).
  Pre-check P3 launched (Opus 5.5, Claude Third; `briefs/BRIEF_P3_D_precheck.md`). HOLDS read: none.
- 19:25 — Stream B completed (`work/B_transfer/H.md`, `T.md`, `DIST3.md`; DRAFT): Lemma H proved; Lemma T proved **as
  stated** (same range of d, same η²_n) by a self-contained one-sided inequality (ghost sample + Cantelli, random swaps
  + Hoeffding; Sauer–Shelah and the half-space VC bound proved in the file) — no external inequality cited, which
  settles the open citation of the VC inequality if the proof survives checking; DIST-3 proved with c = 1 and explicit
  constants. No statement-change request; wording clarifications queued (rename (TR₀)'s direction u → w; record c = 1
  and n₀'s dependence; route text of Lemma T to point at the proved inequality). Pre-check P4 launched (Opus 5.5,
  Claude Third; `briefs/BRIEF_P4_B_precheck.md`; comparison material API T-a-1, T-b-1, T-c-1). HOLDS read: none.
- 19:35 — Stream E completed (`work/E_bridges/B0.md`, `B1.md`, `B2core.md`, `B2.md`, `B3.md`, `ASSEMBLY.md`; DRAFT): all
  bridges proved with explicit absolute constants (c₁ = 1/576, c₂ = 10⁻⁵); B0 pathwise with σ* free (no fallback to
  fixed σ*); B2-core in the stated generality (no fallback to Gaussian rows); Theorem A (i), (ii) and its sentence
  without (A4) assembled from (1.1), (1.2), Lemma X′ and the bridges with one n₀ and constants depending only on
  (s, A, K, c_ψ, b̄); Theorem B from DIST-3, B0–B3 and W3-POST Theorem 1 (hypothesis); Example verified. One editorial
  change request queued: STATEMENT's phrase "q_n ≥ m_n(M log n) + s" is false for small p; what holds and is needed is
  ⌈C_qM log n⌉ ≥ m_n + s, i.e. min{p, m_n + s₀} ≤ q_n (no target clause changes). No early-checkpoint trigger.
  Pre-check P5 launched (Opus 5.5, Claude Third; `briefs/BRIEF_P5_E_precheck.md`; comparison API B-a-1, B-b-1, B-c-1).
  HOLDS read: none.
- 19:50 — Pre-check P2 back (`reviews/P2_opus_precheck_X.md`): VERIFIED-WITH-AMENDMENTS, 0 CRITICAL / 0 MAJOR / 2 MINOR /
  4 NIT; every section of Lemma X VERIFIED, §7 and §9 with amendments (definition of n₀ "for every n ≥ n₀"; §9's
  constants and a c_D-free n₀′). All applied: `lemmas/X.md` v0.3 (sha 4c3a657742455bef); `reviews/P2_disposition.md`;
  DEPS.tsv rows X, X′ refreshed (still UNCHECKED: a pre-check is not a review layer). Earlier verdicts removed from the
  file header before the blind line check.
- 19:52 — Cross-family line check L1 launched on `lemmas/X.md` v0.3: gpt-6-astra, codex, high (`reviews/BRIEF_L1_astra_X.md`).
  HOLDS read: none. Agent tally this leg: 10 Claude (Claude Third: 5 workers, 5 pre-checks incl. P1) + 2 codex (Sol S2, Astra L1).
- 20:05 — Stream C completed (`work/C_size/S.md`, `V.md`, `X12.md`; DRAFT; no statement-change request): Lemma S proved in a
  stronger form (every n ≥ 3, every t > 0; constants free of κ₀; P(𝓑_nᶜ) ≤ 4e^{−c_Bn}); Lemma V (a), (b), (c) proved,
  including singular and duplicated designs; X1–X2 as an independent version with facts F1–F7. C notes that the
  variance surcharge cannot go inside V(b)'s first moment (λ_max(D′) can approach 1) — consistent with `lemmas/X.md`,
  which uses the fractional moment λ₁ < 1 − 1/(8A + 4). Pre-check P6 launched (Opus 5.5, Claude Third;
  `briefs/BRIEF_P6_C_precheck.md`; comparison API S-a-1, S-b-1, S-c-1, V-a-1, V-b-1, V-c-1).
- 20:05 — Stream F completed (`work/F_numerics/RESULTS.md`; DRAFT). Nothing contradicts a statement. (1) Nested tails at
  p = 12 (200 data sets, 10⁶ draws each): at t ≈ log n the median over data sets of Π(n·d² > t | D) is 1.2·10⁻³ (n = 100)
  and 2.6·10⁻⁵ (n = 400), worst data set 0.54 and 0.029; with c = 1 the display needs C² ≥ 2 at these n. (2) Dangerous
  collinearity scale τ² ∈ {log n/n², 4 log n/n², n^{−1.5}}: the distance clause does not deteriorate; the size clause
  fails with (ND) (P(|S| ≥ 6) ≈ 0.03–0.06, flat in n) — as predicted; supports S-FIT. (3) (A5) violated: B = √n keeps
  (E), (C) and n·d² = O(1); B = n breaks them and n·d² ≈ 0.14n — the coefficient-cost interface is really needed.
  (4) Lemma T: no violation found (margin ≥ 60 at n = 1000; heuristic search, 10 data sets per cell). (5) B2-core:
  minima ≥ 0.79 at n = 2000; at n = 200, q = 4 the factor ½ fails in 35% (AR 0.9) of samples — consistent with the
  lemma's requirement q log(ep/q) ≤ c₂n/K⁴ and a large onset n₀ (to be stated honestly). (6) Lemma V: 0 violations in
  1500 adversarial designs; Lemma S's cutoff is vacuous at p = 12 (clamps to K). (7) Citecheck of STATEMENT pins: MISS = 0.
  HOLDS read: none.
- 20:20 — Pre-check P3 back (`reviews/P3_opus_precheck_D.md`): VERIFIED-WITH-AMENDMENTS, 0 CRITICAL / 0 MAJOR / 3 MINOR /
  7 NIT; P6 VERIFIED; all 33 code pins and the retention induction re-checked; SCR-1..5 judged justified and
  non-weakening. Amendments appended to `work/D_output/P6_DISTC.md` and `COR_C.md`; `reviews/P3_disposition.md`; DEPS.tsv
  rows P6, TC/DIST-C, R/Corollary-C refreshed (UNCHECKED until the cross-family line check).
  Line check L2 launched: gpt-6.1-sol, codex, high (`reviews/BRIEF_L2_sol_D.md`). Grouping note: cross-family line
  checks are run one call per stream, with a separate verdict for each lemma or bridge in the report.
  HOLDS read: none. Agent tally this leg: 11 Claude (Claude Third) + 3 codex (Sol S2, Astra L1, Sol L2).
- 20:30 — Pre-check P4 back (`reviews/P4_opus_precheck_B.md`): VERIFIED-WITH-AMENDMENTS, 0 CRITICAL / 0 MAJOR / 2 MINOR /
  2 NIT. Lemma H VERIFIED; Lemma T VERIFIED exactly as stated (constants recomputed: swap exponent 48/169 ≥ 1/4, nη² > 36.64
  on the whole range, failure probability δ/2; no external result) — the kill-budget risk "constant/reference of the
  VC inequality" is closed pending the cross-family check; DIST-3 VERIFIED-WITH-AMENDMENTS (statement must say that C
  depends on C_T and quantify n₀; queued, EQUAL). `reviews/P4_disposition.md`; DEPS.tsv rows H, T, TC/DIST-3 refreshed.
  Line check L3 launched: gpt-6.1-sol, codex, high (`reviews/BRIEF_L3_sol_B.md`). HOLDS read: none.
  Agent tally this leg: 11 Claude (Claude Third) + 4 codex (Sol S2, Astra L1, Sol L2, Sol L3).
- 20:45 — Pre-check P5 back (`reviews/P5_opus_precheck_E.md`): VERIFIED-WITH-AMENDMENTS, 0 CRITICAL / 0 MAJOR / 4 MINOR /
  4 NIT. B0, B1, B2-core, B2, B3 VERIFIED; ASSEMBLY VERIFIED-WITH-AMENDMENTS (wording only). Noted for honesty: with the
  proved absolute constant c₂ = 10⁻⁵ the reader theorem's n₀ is of order 10¹⁵–10¹⁸ — the changelog's phrase "realistic n₀"
  is withdrawn (queued STATEMENT edit); Theorem A is asymptotic. Amendments appended to `work/E_bridges/B1.md`,
  `ASSEMBLY.md`; `reviews/P5_disposition.md`; DEPS.tsv bridge and reader rows refreshed.
  Line check L4 launched: gpt-6.1-sol, codex, high (`reviews/BRIEF_L4_sol_E.md`). HOLDS read: none.
  Agent tally this leg: 11 Claude (Claude Third) + 5 codex (Sol S2, Astra L1, Sol L2, L3, L4).
- 21:00 — Pre-check P6 back (`reviews/P6_opus_precheck_C.md`): VERIFIED-WITH-AMENDMENTS, no mathematical error, 2 MINOR /
  5 NIT. Lemma V, X1, X2, facts F1–F7 VERIFIED; Lemma S VERIFIED-WITH-AMENDMENTS (range statement of Corollary S.1).
  C-7 (queued STATEMENT edit): §0's sentence "(C) is used only through (L₀)" is false for Lemma V(a) and step X4, which
  use ρ′ — to be restricted to Lemma S and DIST-3 (no lemma statement is affected: Lemma X keeps (C)). Amendments
  appended to `work/C_size/S.md`; `reviews/P6_disposition.md`; DEPS.tsv rows S, V refreshed, row X12 added (not on the
  path). Line check L5 launched: gpt-6-astra, codex, high (`reviews/BRIEF_L5_astra_SV.md`; Lemma S and Lemma V).
  All five streams now have proofs written and pre-checked; cross-family line checks running: L1 (Astra, X/X′),
  L2 (Sol, D), L3 (Sol, B), L4 (Sol, E), L5 (Astra, S/V); blind read S2 (Sol) running. HOLDS read: none.
  Agent tally this leg: 11 Claude (Claude Third) + 6 codex.
- 19:21 — HQ notes: organization (W3-DIST directly under HQ until CP3; lead = manager of the ticket and its team) and `POLICIES.md` (main dfbdf2c) read in full: access (may read everything, run tools, commit/push own branch theory/W3-DIST; shared root clone must not switch branch — the snapshot cron stays the restore mechanism for this folder, so no git by the lead beyond pulls), resources (Claude Third default; Codex shared, NORMAL mode), reporting (≤ 10 lines to HQ at checkpoints via t3_thread_send; escalate at once on a counterexample to a target, a WEAKER change to a target clause, a hold on a consumed claim, a budget overrun). HOLDS read: none.
- 19:43 (from `date`) — **Clock correction (flagged, not rewritten).** The proof-leg entries above stamped 19:05, 19:15,
  19:25, 19:35, 19:50, 19:52, 20:05 (×2), 20:20, 20:30, 20:45 and 21:00 are **mis-stamped**: the lead typed estimated times
  instead of reading `date`. They were actually written between 18:55 and 19:21 CST, in the order listed (the entries
  stamped 18:51, 18:56, 19:21 and this one are from `date`). In the scoping leg, the entries stamped 17:55 and 18:35
  (CHECKPOINT_1 and its revision) were likewise typed by hand and are a few minutes late (`date` read 17:52 and 18:30).
  From here on every stamp is taken from `date`.
- 19:43 — Message received in this thread from the Theory Dept manager: W3-DIST moved under the SMC - Theory Department
  (reporting to thread mcp:launch:21e33dae…, API cards via the department). **Not yet reflected in the records on main**
  (34ce461): POLICIES.md §1 "Tickets directly under HQ: W3-DIST, W3-READER"; HQ_NOW.md "HQ keeps W3-DIST"; Dept/BRIEF.md
  "Not yours (HQ keeps until done): W3-DIST"; HQ's own note of this evening said W3-DIST stays under HQ until CP3.
  Action: the clock correction (above) is done; the reporting change is held until HQ confirms it; a one-line
  confirmation request is sent to the HQ thread. Work continues unchanged. HOLDS read: none.
- 19:45 — HQ confirmed the move (records on main updated: POLICIES.md §1, Dept/BRIEF.md "Handover", HQ_NOW): W3-DIST now reports to the SMC - Theory Department manager (thread mcp:launch:21e33dae…; ≤ 10 lines at checkpoints and daily; API cards routed through the department). HQ keeps CP3 acceptance and headline cards. Owner memo (POLICIES §4): a new Fable expert needs approval via HQ and the owner; the lead continues as is. HOLDS read: none.
- 19:45 — Line check L1 back (`reviews/L1_astra_X.md`; gpt-6-astra, codex, high; on lemmas/X.md sha 4c3a657742455bef):
  **Lemma X VERIFIED; Lemma X′ VERIFIED; no finding at any severity**; every section §1–§7, §9 VERIFIED; all [P1]
  citations audited; null truth, p = 2, singular true blocks, duplicates, unions outside Ω and the top of the t range
  checked analytically; no counterexample found (algebraic verification, no numerical search). DEPS.tsv: rows X, X′
  → **OK** (checked_sha = sha, checked_by L1). Kill budget on X: 1 of 3 attempts used, passed.
- 19:45 — CP2 break review BR1 prepared (`reviews/BRIEF_BR1_astra_break.md`): Astra, on STATEMENT + lemmas/X.md + [P1];
  asks to break Lemma X and the passage to (1.1)/(1.2), then CONTINUE / REDIRECT / STOP. Launched now (Lemma X no longer
  consumes S or V; their line check L5 runs in parallel). HOLDS read: none.
- 19:47 — Owner memo (via the Theory Dept manager; POLICIES.md §4) received and adopted: technical problems are solved inside the ticket; Opus/Sonnet helpers within the brief; a new Fable expert (including the possible second Fable for S-FIT) needs permission requested through the department manager; big problems reported to the manager at once. One-line confirmation with the L1 result sent to the department thread. HOLDS read: none.
- 19:52 — Owner's final rule on helpers noted (POLICIES §4, §8): Opus/Sonnet/Haiku helpers free within the brief; a new Fable needs the owner's green light, requested through the department manager (problem, why Opus is not enough, how many, size/duration, account). No change to the plan. HOLDS read: none.
- 20:00 — POLICIES §9 noted (requests for expensive resources go to the department manager in ≤ 10 lines; nothing expensive starts before the answer). No request made now: the main line needs none; S-FIT is decided after the resubmitted API attempts (dist1b) are read. HOLDS read: none.
- 20:03 — Owner rule (POLICIES §10) noted: never settle, archive, cancel, interrupt or delete any thread or agent; unneeded
  results are ignored and logged. (None has been cancelled on this ticket.)
- 20:03 — Blind read S2 back (`reviews/S2_sol.md`): REPAIR REQUIRED; 3 MAJOR / 4 MINOR. Theorem B and bridge B3
  FALSE-AS-STATED (b_n > 0 missing; counterexample with b_n = −1) — repaired; B2/B3 window inequalities false for small p —
  repaired (same as stream E's request); reader Setup wrote the prior with p instead of the retained count — repaired
  (r). No counterexample to Theorem A's displays; B1, B2-core SOUND. Part 2: changelog tags checked (several pre-CP1
  EQUAL tags contested as literal tags). **STATEMENT v1.4** written (S2 dispositions + all queued edits from streams B,
  D, E and pre-checks P3–P6): sha f4087ea62b6ea654; TARGET §6 synced; `reviews/S2_disposition.md`; DEPS.tsv sha of
  STATEMENT-based rows refreshed. DEPS note: STATEMENT changed after L1 — rows X, X′ keep OK (their object is
  lemmas/X.md, unchanged; the statements of Lemma X, X′ in STATEMENT §3 are unchanged in v1.4).
  No WEAKER change to the mathematics of TC1–TC9 relative to the CP1 baseline; S2-03 edits the Setup of the headline
  reader theorem (description of the prior) → reported to the department manager now. HOLDS read: none.
- 20:04 — Owner rule (POLICIES §10, final) noted: never cancel or interrupt running work; finished own helpers may be
  settled (not archived or deleted). None cancelled on this ticket.
- 20:04 — Resubmitted API attempts read (`work/api_attempts/dist1b/`; H3: proof material, unchecked). **F-b-r2 claims a
  counterexample to stretch item S-FIT in its exponential form**: explicit design (anchor + ⌊√n⌋ near-copies at
  τ² ≍ log n/n², s₀ = 0, μ = 0) on which, w.p. ≥ 0.6, Π(‖μ̂ − μ‖² ≥ (k/24) log n | y) ≥ c(k)/n — so the distance clause of Lemma X
  cannot hold under (E), (C) alone: (ND) or a substitute is needed for the exponential form at the sharp rate, not only
  for the size clause. It does **not** contradict any target (TC2–TC4 assume (ND); TC6's radius is tℓ_n) and does not
  break the in-probability form. F-a-r2: in-probability sharp-rate bound proved for supersets without (ND) (complete for
  s₀ = 0); F-c-r2 and X-c-r2: partial (non-supersets open; a weaker "fit–Occam" interface in place of (ND)).
  Lead's reading: S-FIT (exponential) is dead if F-b-r2 survives checking — which turns the "short of Song–Liang" row
  for (ND) into a proved limitation of the coded prior; S-FIT (in probability) stays open. Pre-check P7 on F-b-r2
  launched (Opus 5.5, Claude Third; `briefs/BRIEF_P7_NEC_precheck.md`). No second-Fable request for now. HOLDS read: none.
- 20:05 — Line check L3 back (`reviews/L3_sol_B.md`; gpt-6.1-sol, codex, high; sha H 1ca0d39c24eebd49, T 193cdc8145e724e8,
  DIST3 4240189593efcb4d): **Lemma H VERIFIED; Lemma T VERIFIED; Theorem DIST-3 VERIFIED; no finding at any severity.**
  Lemma T: exact range and remainder of the statement, success probability 1 − δ/2, self-contained (no external
  inequality) — the open citation question is closed. The wording requests of T.md and DIST3.md judged EQUAL (already
  applied in STATEMENT v1.4). Not verified by L3 (outside its packet): the locked identification of the coded
  posterior (P-T01) and the external selection theorems. DEPS.tsv: H, T, TC/DIST-3 → OK. Kill budgets H, T: 1 attempt
  each, passed. The L1 completion notice (Astra, Lemma X) also arrived; already processed. HOLDS read: none.
- 20:10 — Manager's reading of the S2 tags applied to the changelog (STATEMENT v1.4, tags only): Theorem B "b_n > 0" →
  WEAKER on a companion, non-target clause (reported at the next checkpoint; no early checkpoint); bridge remarks
  (B2/B3 windows, B3 positivity, B0 domain) → WEAKER, non-target, split from the EQUAL row for Lemmas T and V. TC9: EQUAL
  for the mathematics (manager's view; HQ decides on an H5 card). The Sol diff check v1.3.1 → v1.4 will confirm or
  correct every tag. S2's completion notice also arrived (already processed). HOLDS read: none.
- 20:21 — POLICIES §12 (compute discipline) noted and added to `briefs/COMMON.md` and `briefs/PRECHECK_COMMON.md` for future
  helpers. Check done: the lead's scratchpad is empty (one temp script removed); this ticket's helpers left only small
  scripts in their own scratchpads (≤ 44 KB each); `work/numerics/arrays/` (68 MB, git-ignored) and
  `work/F_numerics/out/` (1.2 MB, arrays ignored) stay in the ticket folder, no copies elsewhere. The large folders
  under /tmp/claude-71711 (≈ 2 GB) belong to other projects' and other departments' sessions; not touched. No job of this
  ticket is running on Owls CPUs now. HOLDS read: none.
- 20:22 — Line checks L5 and L4 back. **L5** (`reviews/L5_astra_SV.md`, Astra): Lemma S, Corollaries S.1, S.2 and Lemma V
  (a), (b), (c) all VERIFIED; 2 MINOR + 1 NIT (a wrong simulation in the check script — its validation claim withdrawn;
  R^T_m's upper limit K made explicit in STATEMENT v1.4.1; toolbox s > 0). **L4** (`reviews/L4_sol_E.md`, Sol): B0, B1,
  B2-core VERIFIED; B2, B3, ASSEMBLY (Theorems A, B) VERIFIED-WITH-AMENDMENTS, 5 MINOR (capped-window chain in B3; common
  exceptional set without (A4); c₃ > 0; p_ret = p qualification) — amendments appended to S.md, B3.md, ASSEMBLY.md.
  `reviews/L4_L5_disposition.md`. DEPS.tsv: V, B0, B1, B2-core, B2 → OK; S, B3, R/Theorem-A, R/Theorem-B → STALE
  (verified, then amended as prescribed; one Sol diff check will confirm, batched with the STATEMENT diff check).
  **CP2 gate: X, X′ (L1), S and V (L5) are line-checked; the Astra break review BR1 is still running.** HOLDS read: none.
- 20:24 — POLICIES §12 rule 7 (calm usage) noted: no NOTS access from this ticket (none was ever used); no bursts of parallel jobs; Owls jobs ramp up within 16 cores; helpers kept to the brief and staggered. Currently running for this ticket: 3 agents (BR1 Astra, L2 Sol, P7 Opus with a small numerical check); the remaining launches (one Sol diff check, later the sweep) will be sequential. L3 and L4 completion notices arrived (already processed). HOLDS read: none.
- 20:27 — Temp convention noted (HQ + Engineering): temp work under /home/fb31/bvs_tmp/W3-DIST/, never /tmp; TMPDIR exported in commands that write temp files; added to briefs/COMMON.md and briefs/PRECHECK_COMMON.md for future helpers. Directory created (empty). HOLDS read: none.
- 20:33 — Temp path refined (Engineering's README): /home/fb31/bvs_tmp/theory/<YYYYMMDD>-W3-DIST-<what>, removed when the job ends. The empty top-level /home/fb31/bvs_tmp/W3-DIST created 6 minutes earlier was removed (nothing was in it); briefs/COMMON.md and briefs/PRECHECK_COMMON.md updated. HOLDS read: none.
- 20:37 — FINAL temp location (POLICIES §12 rules 8–9): /home/fb31/SMC_Theory_Department/tmp/<YYYYMMDD>-W3-DIST-<what>; briefs updated. This ticket has nothing under /home/fb31/bvs_tmp and no temp folder at present. HOLDS read: none.
- 20:38 — Line check L2 back (`reviews/L2_sol_D.md`, Sol): Lemma P6 (a), (b), (c), DIST-C (C-0), (C-iv) VERIFIED; (C-i), (C-ii),
  (C-iii) and Corollary C VERIFIED-WITH-AMENDMENTS; 4 MINOR + 1 NIT, none against a completed-run statement. Amendments
  appended to `work/D_output/P6_DISTC.md` (A-8..A-10) and `COR_C.md` (A-3, A-4); STATEMENT v1.4.2 and TARGET §6: Corollary C's
  opening sentence corrected (the method does not compute the full posterior). Disposition appended to
  `reviews/L4_L5_disposition.md`. DEPS.tsv: P6, TC/DIST-C, R/Corollary-C → STALE (verified, then amended; diff check pending).
  **All five cross-family line checks are back (L1–L5): no CRITICAL or MAJOR finding in any proof.** Outstanding: BR1
  (Astra break review), P7 (Opus pre-check of the necessity counterexample), then one Sol diff check of the statement
  changes and post-check amendments. HOLDS read: none.
- 21:05 — **Break review BR1 back** (`reviews/BR1_astra_break.md`, Astra): Lemma X NOT BROKEN; passage X → (1.1) NOT BROKEN;
  Lemma X′ NOT BROKEN; passage X′ → (1.2) NOT BROKEN; 3 MINOR assembly omissions with full repairs (deterministic
  sparsity level for Lemma T; the intercept-noise event; C′ = 33 for the size clause); **CP2: CONTINUE.**
  `reviews/BR1_disposition.md`. Master assembly written: `lemmas/DIST12.md` v0.1 (DIST-1, DIST-2 from H, T, X, X′, with the
  three repairs). STATEMENT v1.4.3 (the applications sentence of Lemma T; EQUAL). DEPS.tsv: TC/DIST-1, TC/DIST-2 →
  lemmas/DIST12.md, UNCHECKED. `reviews/DIFF_STATEMENT_v131_to_v143.patch` generated (read-only `git diff` against the
  snapshot commit f54bd6f = v1.3.1) for the coming diff check.
- 21:05 — **CHECKPOINT_2.md written (soft CP2): gate met** — X, X′, S, V line-checked; break review CONTINUE; no open blocking
  finding; no kill budget spent. The lead continues. Line check L6 (Sol) of `lemmas/DIST12.md` launched
  (`reviews/BRIEF_L6_sol_DIST12.md`); the diff check follows it (sequential, calm usage). Running for this ticket: L6 (Sol),
  P7 (Opus). HOLDS read: none.
- 21:06 — Manager/HQ: CP2 CONTINUE approved. Owner's standing rule applied: asymptotics are never framed as a limitation — the remark on the numerical size of n₀ removed from STATEMENT (v1.4.4, EQUAL) and kept only as an internal REPORT line ("explicit constants, not optimised"); no such figure in any reader-facing text (TARGET §6 never had it). To be confirmed in the Sol diff check batch. Council-freeze target re-sent: Mon 2026-11-16 09:00 CT. HOLDS read: none.
- 21:08 — Manager: I freeze the R1 manifest and launch both council seats myself (Astra seat; Opus 5.5 seat on Claude
  Third), fresh and blind, briefs from INFRA/templates/COUNCIL_BRIEF.md saved before launch, each with the "must give
  gates=FAIL on its own C/S/F" sentence; same for the sweep; digest sent to the manager right after the freeze; HOLDS
  read just before the freeze. n₀ line: "explicit constants, not optimised", internal REPORT only (leftover phrase
  removed from the changelog too).
- 21:08 — Pre-check P7 back (`reviews/P7_opus_precheck_NEC.md`): the counterexample is correct as a **fixed-design,
  in-sample** statement (Lemma X without (ND) is false, also with an outer probability only tending to 0); numerics on
  the exact posterior confirm the n⁻¹ scaling; the attempt's commentary overclaimed (S-FIT at theorem level, Lemma X′'s
  logarithm) — corrected. Written as `lemmas/NEC.md` (Proposition NEC + Corollary; non-target sharpness result);
  `reviews/P7_disposition.md`; STATEMENT v1.4.5 (Proposition NEC in §3; S-FIT text; NEW-CLAIM non-target); DEPS rows NEC,
  S-FIT. Line check L7 (Sol) launched (`reviews/BRIEF_L7_sol_NEC.md`). Running: L6 (Sol), L7 (Sol). HOLDS read: none.
- 21:11 — REPORT.md generated (`mkreport.py` + `REPORT_extra.md`: §1 table pointing to STATEMENT lines, review trail, numerics, relations and sharpness, inputs and assurance with the three reviewer-unverified premises as "conditional on …", 20 registry blocks; internal line "Explicit constants, not optimised"). It is regenerated after any STATEMENT edit. Running: L6, L7 (Sol). HOLDS read: none.
- 21:57 — Cross-department finding (Engineering via HQ and the manager; `Docs/Experiments/P1M/DECISIONS.md` D-17,
  `reviews/PR12_review.md`, `PR12_disposition.md`, read only): at the planned (n, p) the posterior is spread over S₀ and
  about p one-null supersets (π(S₀) ≈ 0.45–0.65 at n = 200). Search of STATEMENT, TARGET, REPORT, ROUTES, ASSUMPTION_MAP: **no
  statement-level text relied on a point-mass posterior**; two conditional sentences use π(S₀) > ½ only as a sufficient
  condition (DIST-C (C-ii)(α); Corollary C's retention sentence). Wording made explicit (STATEMENT v1.4.6, EQUAL): the
  store law is in general a mixture over many models; the condition of Corollary C concerns the list as a whole;
  (C-ii)(γ) added as a description; TARGET §6 synced; REPORT regenerated. Goes into the Sol diff check batch.
  P7's completion notice arrived (already processed). HOLDS read: none. X.md sha re-verified (4c3a657742455bef).
- 22:04 — **L6 landed** (`reviews/L6_sol_DIST12.md`, Sol): displays (1.1), (1.2), D.1–D.3, consequences (a), (b), (d), (e)
  VERIFIED; one finding, **L6-01 (MAJOR)**: the sparsity dependence claimed in DIST-1 (c) / TC3 (M₀ = O((1 + s₀^r)(A + 1))) was
  not established (K_s gave M₀ ≳ s log s; C grew with s; raw/retained sparsity mixed). **Repaired by constants, TC3 kept
  as fixed**: `lemmas/X.md` v0.4 (K_s → 2; C_d := 34), `lemmas/DIST12.md` v0.2 (C_T free of s; dependence paragraph),
  STATEMENT v1.4.7 (c) with the explicit bound M₀ ≤ 16 + 4(1 + s₀^r)(A + 1) + 3(M + M′)/(2σ*²), tag EQUAL; TARGET P3 synced;
  DEPS: X, X′, TC/DIST-1, TC/DIST-2 → STALE (re-check inside the Sol diff check D1); REPORT regenerated;
  `reviews/L6_disposition.md`. Fallback if the re-check fails: reviewer's minimal repair = WEAKER on TC3 = early
  checkpoint. Manager told. L7 (Sol, NEC) still running (launched about 21:05). HOLDS read: none.
- 22:06 — Diff check **D1 (Sol, new agent)** launched (`reviews/BRIEF_D1_sol_diff.md`): Part A re-check of the L6-01 repair
  (X.md v0.4, DIST12.md v0.2); Part B the post-check amendments (S, P6_DISTC, COR_C, B3, ASSEMBLY); Part C STATEMENT
  v1.3.1 → v1.4.7 and every changelog tag from 1.4 on. Diffs: `reviews/DIFFS_D1.patch` (each file against its
  line-checked version, taken from the snapshot branch, read-only git) and `reviews/DIFF_STATEMENT_v131_to_v147.patch`.
  Running: L7 (Sol), D1 (Sol). HOLDS read: none.
- 22:09 — **L7 landed** (`reviews/L7_sol_NEC.md`, Sol): **Proposition NEC and Corollary NEC VERIFIED**; file
  VERIFIED-WITH-AMENDMENTS: L7-01 (MINOR: the radius attributed to (1.2) in "what this does not say"), L7-02 (NIT: 0.0705
  rounded down), L7-03 (MINOR: the numerical check is the posterior restricted to sizes ≤ 4, not the full posterior). All
  three applied (`lemmas/NEC.md` v0.2; nothing in the Proposition, Corollary, constants or proofs changes). DEPS row NEC:
  STALE until the three hunks are re-checked (D2, a short Sol diff check, `reviews/BRIEF_D2_sol_NEC_diff.md`).
  Citation check: 9 pins, 0 MISS (the script's own spot check looks for `pip_r` on v3_run.R:160; it is on :161, inside
  the cited range 159–162: no error in STATEMENT). Staged registry ingest of REPORT.md: first run 14 form problems
  (statuses not verbatim on their source line; "bridge none"; a "|" inside an assumption text): fixed in
  `mkreport.py` / `REPORT_extra.md` (table status and block status now come from one string); second run 20 claims,
  **0 problems, 0 ERROR introduced**; acceptance on the staged copy REFUSED with 4 ERROR, all the same cause outside this
  ticket: the accept record of the consumed claim **W3-MISR:R′** is stale in the live registry (B0 → Theorem A,
  Theorem B, Corollary C). To the manager. HOLDS read: none.
- 22:13 — Manager's conditions on L6-01 received (reviewer confirms the EQUAL tag; no new condition may be hidden in
  the repair; fresh Sol agent on the exact diffs and every STALE row; no second break review for a constant repair) and
  answered: all three are in D1's brief; "e^{s₀}q ≤ n^{−1/8} ≤ ½" is an unchanged, line-checked line of X.md v0.3 (threshold
  condition (d) of n₀). D2 (Sol, three NEC hunks) launched. Prepared while D1, D2 run: `reviews/INPUTS_R1.txt` (tracked
  external inputs), `reviews/BRIEF_SW1_astra.md` (sweep, two passes: blind, then records), `reviews/BRIEF_R1_TEMPLATE.md`
  (council seats; C/S/F/E tags; the gates=FAIL sentence; verdict-line block), REPORT §2 rows for L6, L7, D1, D2.
  Running: D1 (Sol), D2 (Sol). HOLDS read: none.
- 22:27 — Manager: the W3-MISR:R′ accept record is fixed on main (b69476e). `git pull --ff-only` done (main only). The
  consumed text of W3-MISR STATEMENT (lines 70–72, 75–77) is unchanged. Staged ingest rerun: 20 claims, 0 problems,
  0 ERROR introduced, **acceptance PASS, 0 acceptance ERROR**. L6's late completion notice arrived (already processed;
  thread settled). Running: D1 (Sol), D2 (Sol). HOLDS read: none.
- 22:39 — L7's completion notice arrived. The reviewer was still in its final verification when I read its file at
  22:07 and amended `lemmas/NEC.md` (I took the written file for a finished review; from now on I act on a review only
  after its completion notice). It noticed the change, re-read v0.2 (sha 54340e87b89336a1 = current) and rewrote its
  report: three findings RESOLVED, **overall VERIFIED, no outstanding finding**. DEPS row NEC → **OK**. D2 (new Sol agent
  on the same three hunks) is left to finish as a second reading; it is not cancelled. L7 thread settled.
  Running: D1 (Sol), D2 (Sol). HOLDS read: none.
- 23:20 — **D2 landed** (`reviews/D2_sol_NEC_diff.md`, Sol, second reading of NEC.md v0.2): hunks for the version line,
  L7-01, L7-02 RESOLVED; L7-03 NOT RESOLVED: **D2-01 (MINOR)**, the numerical remark still asserted "slightly smaller"
  full-posterior masses and the full-posterior event, which a calculation restricted to |S| ≤ 4 does not give.
  Proposition and Corollary unaffected. Accepted; the reviewer's wording applied (`lemmas/NEC.md` v0.3, §8(d) only).
  DEPS row NEC: STALE until that sentence is re-read; batched with whatever D1 returns into one short Sol check (D3).
  D2 thread settled. Running: D1 (Sol). HOLDS read: none.
- 00:11 — **D1's report** (`reviews/D1_sol_diff.md`, written 23:51; completion notice not yet received at 00:10; manager told at
  00:07 under the 2-hour rule, answered "fine, proceed"): overall VERIFIED-WITH-AMENDMENTS. **Part A: the L6-01 repair
  VERIFIED (items 1–7); Lemma X, X′, DIST-1, DIST-2 VERIFIED as they stand; "EQUAL on TC3" CONFIRMED**; no new condition
  (e^{s₀}q ≤ n^{−1/8} < ½ from the existing (a), (d)). Part B: S, COR_C, B3, ASSEMBLY VERIFIED; P6_DISTC
  VERIFIED-WITH-AMENDMENTS (D1-01: A-10 mixed the N-dimensional likelihood with shape 0.01). Part C: 15 changelog rows
  CONFIRMED, 3 CONTESTED on tags (D1-04: Corollary C has a STRONGER part; Remarks a WEAKER part; bridges mixed), D1-02
  ((C-i) wording, SCR-4 not yet applied), D1-03 (an unrecorded range change in the last bridge bullet), D1-05 (my
  statement patch was a deletion snapshot: regenerated with diff -u). No CRITICAL, no MAJOR.
  **HQ go (via manager, 11-16): the STRONGER HPM conclusion of Corollary C stays in**; the sweep brief and both council
  briefs must name it as a point to check; recorded in the changelog row.
  Applied: STATEMENT **v1.4.8** ((C-i) event written out, tag EQUAL on TC8 pending the reviewer; three v1.4 rows
  re-tagged; check column filled from D1); `work/D_output/P6_DISTC.md` A-10 corrected (contrast model, shape 0.51).
  DEPS: X, X′, TC/DIST-1, TC/DIST-2, TC/DIST-3, S, B3, R/Theorem-A, R/Theorem-B, R/Corollary-C → **OK**; P6, TC/DIST-C, NEC
  STALE until D3. D3 (Sol, new agent, about sixty changed lines, `reviews/BRIEF_D3_sol_diff.md`, `reviews/DIFFS_D3.patch`)
  launched. Running: D1 (final pass), D3. HOLDS read: none.
- 00:12 — D1's completion notice arrived; verdicts identical to the report I acted on (file checked again: same first and
  last lines). D1 thread settled. Running: D3 (Sol). HOLDS read: none.
