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
