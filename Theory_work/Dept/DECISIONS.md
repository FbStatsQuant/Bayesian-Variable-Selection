# Theory Department — decisions log

## 2026-11-15 19:28 CT — riders queue set up
- **D1. Rider tickets are new folders `<PARENT>-R` with delta statements.** Parent folders stay read-only: their
  STATEMENT/lemma lines and CHECKPOINT_<k>.md files are hashed in the registry (sha256, status_sha256, check.py C12),
  so in-place edits would break recorded claims and v4 principle 2. Pattern = START2 v1.4 over START v1.3.4. New claim
  ids get `implies` edges; headline supersession goes HQ → consultant (H5). Common rules: `RIDER_RULES.md`.
- **D2. Grouping.** W3-START2-R = T10 + T8 + START restatements (MIS/EX/F1/F3/F4) + LEAK-0 wording (one lead; T8 and
  T10 touch different lemma files, helpers allowed); W3-RM2-R = T4 + T2(a–c) (T6 already in RM2 v1.4, not redone);
  W3-PSHARP-R = T12; W3-MISR-R = T13; W3-EDIT = the HQ_NOW editorial pass (later slot; it edits recorded files, so it
  needs the recorder's rehash path — brief with HQ).
- **D3. Tier B, NORMAL mode, no Astra better-theorem review at CP1**: the targets come from the blind sharp2 audit,
  which served as the better-theorem input. Sol: lock, line checks, council OpenAI seat; Opus Claude seat.
- **D4. Launch order** START2-R, RM2-R, PSHARP-R now (3 = cap); MISR-R at the first free slot; W3-EDIT after.
  Optional items (T9, T11, Ex-Equi 3/8, quantile (W)) decided at each CP1 against the Wed 18:00 CT cut-off.
- **D5. Snapshot cron** commit-in-place (SNAP_WT=1) for the 4 rider worktrees at :01/:03/:06/:08 +15.
- **D6. Not taken:** W2-APP:POST@1.0.1 line check (HQ_NOW lists it; HQ's recorder already handles W2-APP PC1) — asked HQ.

## 2026-11-15 19:36 CT — HQ answers; premise tickets; early scoping leg
- HQ approved D1, the Wed 18:00 CT rider cut-off (freeze Fri 11-20; a late rider ships at its last checked state),
  the W3-EDIT recording path (HQ merges + recorder rehash), H5 cards + READER_DELTA at each CP1. W2-APP PC1 is the
  recorder's (not ours). D6 closed.
- **D7. Premise tickets** (ENGINEERING_SPEC §4.2: T-N, T-PART, T-STREAM, T-CAL, T-MERGE) go into the parallel-SMC
  campaign proposal (Thu). Blocking analysis (to confirm with Engineering): T-PART blocks OD-5 and WP2 setup (11-23);
  T-N de-risks OD-1 (owner, ~11-20); T-STREAM/T-CAL needed before G-A (~12-07); T-MERGE's pooling rule before WP4's
  merge is final (~11-30). Interface file `ENG_INTERFACE.md`.
- **D8. Early scoping leg PSMC-S0 = T-PART + T-N premise audits to CP1 by Thu 11-19 12:00 CT** (brief
  `drafts/PSMC-S0_BRIEF.md`; ~5–7 Opus h; 1 Sol fidelity read). Asked HQ for a temporary 4th/5th slot so that
  PSMC-S0 and W3-EDIT do not wait behind the riders; default order if refused: MISR-R → W3-EDIT → PSMC-S0.
- **D9. W3-EDIT brief final** (`drafts/W3-EDIT_BRIEF.md`): citation fixes first (unblock PR #10); rehash table for the recorder.

## 2026-11-15 19:38 CT — Engineering dates (REQUESTS THEORY-1..3)
- **D10. PSMC-S0 re-scoped:** Part 1 = T-N audit + T-CAL preliminary → CP1 Thu 11-19 12:00 CT (owner OD-1/OD-2 batch,
  soft 11-20); Part 2 = T-PART audit over Engineering's full consumer list (THEORY-1) → CP2 Tue 11-24 (soft 11-25).
  T-STREAM (soft 11-27) is the campaign's first ticket after the freeze; T-MERGE (soft 11-30, hard 12-18) its main one.

## 2026-11-15 19:41 CT — HQ: slots and launches
- **D11.** HQ granted 2 temporary slots (≤ 5 running until Wed 18:00 CT). Launched PSMC-S0 (brief rev. 1: Part 1 T-N +
  T-CAL prelim → CP1 Thu 12:00; Part 2 T-PART → CP2 Tue 11-24; HQ's "T-PART + T-N" approval predates D10, both are in
  scope) and W3-EDIT (citation fixes first → ping HQ for PR #10). W3-MISR-R takes the next free slot.
  Codex order: W3-DIST > riders > PSMC-S0 / W3-EDIT; > ~2 h queue → tell HQ.

## 2026-11-15 19:43 CT — handover from HQ (owner's decision)
- **D12.** W3-DIST (Fable lead, mcp:launch:75635c1f…; root-clone folder, snapshot → theory/W3-DIST), W3-READER (Opus,
  mcp:launch:2a4462b2…, worktree BVS-wt/W3-READER) and the recorder (mcp:launch:563aa9b9…) now report to the Theory
  Department. HQ keeps CP3 acceptance, H5 headline cards, merges, API submission. DIST and READER sit outside the lead
  cap. Codex: W3-DIST > riders > PSMC-S0/W3-EDIT/READER.
- Leads told: report to this thread; DIST told to take timestamps from `date` (its LOG has 20:30–21:00 entries before
  a 19:21 one); READER told about the incoming READER_DELTAs and the equal-weight pooling fact (v3_run.R:154,162).
- Recorder: task C continues (PC1 Sol); task D on hold. Two decisions go to HQ with a recommendation: (a) clear the
  tool-set headline flags (v4 §8) by consultant card until the strength gates run; (b) inputs below PROVED-CHECKED →
  "conditional on …" with @hyp (W3-11). No real run without HQ.

## 2026-11-15 19:45 CT — HQ items: pooled-PIP fix, Engineering D-3/D-7/D-8, OD-4, self-sufficiency
- **D13. Pooled-PIP faithfulness fix routed in-department:** W3-READER states the coded equal-weight PIP (told);
  W3-EDIT item 7 adds a "what the code does" sentence after the quoted v3.1 text in 02_method.tex:440-451 (steered);
  `Docs/Writing/QUEUE.md` created in the WRITING worktree (HQ-authorised) with the row for the Writing Department.
- **D14. Engineering D-7 (final-run leader stores)** assigned to PSMC-S0 Part 1 (inside AUDIT_CAL; verdict SAFE TO DROP
  / NOT SAFE at CP1). D-3 (`logical` cost column) and D-8 (PIP_𝒯, log Z_𝒯, law.bin) registry staging: recorder task
  when Engineering sends the specifics; dry runs only, HQ approves real runs.
- OD-4 confirmed (dept + HQ): equal-weight primary; T-MERGE's convex-pooling theorem is the target.
- Owner's standing rule: departments self-sufficient; HQ only for gates, budget, merges, API, cross-department. EVAR
  Fable decided in-department (reported to HQ).
- Lesson: send to a *running* lead with mode steer (queue waits for the run to end).

## 2026-11-15 19:48 CT — owner memo (POLICIES 34ce461a) relayed
- **D15.** Memo passed to all 8 leads (DIST, READER, recorder; START2-R, RM2-R, PSHARP-R, PSMC-S0, W3-EDIT), with the
  reporting line restated to DIST/READER/recorder and the pooled-PIP code fix to READER. A Fable expert now needs
  owner permission via HQ (reason + size): EVAR in NEXT_CAMPAIGN updated; DIST's "second Fable" needs it too.
- Check after relay: the three riders had ended their turns while waiting on async Sol statement locks (not at CP1);
  the memo turn only logged it. No checkpoint was skipped.

## 2026-11-15 19:49 CT — operating rhythm (POLICIES §7–§8)
- **D16.** Daily report to HQ by 09:00 CT (done / in progress / blocked / needs / budget used), scheduled 08:30 CT
  daily (first 11-16), plus a report at every checkpoint; heartbeat every 45 min stays. Charter (§8) adds **strength
  gates for headline candidates** (lit / necessity / better) to our remit: queued below, planned with the recorder's
  task D blocker (POST2 / W2-APP headline rows lack lit/necessity/better PASS).

## 2026-11-15 19:49 CT — HQ on recorder decisions
- 4(b) approved (conditional-on + @hyp). 4(a) with HQ's consultant (H5), condition: W3-READER candidate rows keep flags
  until the claims card is decided. Recorder told: dry runs for C and D, two variants for 4(a) (flags kept / cleared off
  the candidate list); no real run until HQ. Forward W3-READER CP1 claims card to HQ as soon as Sol S1 lands.

## 2026-11-15 19:52 CT — HQ verdict 4(a): clear all 44 headline flags; strength gates scheduled
- Recorder task F (dry runs): clear all 44 tool-set flags; HEADLINE_CANDIDATES.md (cleared ids, why candidate,
  pending gates, citation rule); staged acceptance POST2 + W2-APP with 4(b); find Ex-STAR/ENUM real block. Real runs: HQ.
- **D17. Strength gates for the five-pillar rows = W3-READER leg 2** (draft `drafts/W3-READER_LEG2_GATES.md`):
  outside the lead cap, same lead that already owns the card and the per-assumption necessity lines. better: gates
  cite the blind API sharpness audits (sharp1/1b/2 + triage dispositions) where they cover a row; fresh Opus reviews for
  uncovered rows; Codex kept for DIST and riders. Deadline Thu 11-19 18:00 CT → recorder enters gates before the Fri freeze.
  W3-DIST gates in its own chain; rider rows at their CP1.

## 2026-11-15 19:56 CT — owner scope clarification (POLICIES end of §8)
- **D18.** Theory stays about the method as coded at 10⁴; Engineering may modify the algorithm for 1M (documented,
  validated on an overlap rung). Premise tickets T-N, T-PART, T-STREAM, T-CAL are **downgraded to Engineering's choice**
  (no theory ticket). PSMC-S0: Part 1 finishes (Sol FR1 already running; useful to Engineering: D-7, OD-1 correction,
  calibration questions), reframed as Engineering-facing notes; **Part 2 (T-PART) cancelled**. Its slot goes to
  W3-MISR-R as soon as PSMC-S0 writes CHECKPOINT_1.
- **Kept, pending the owner's answer** on whether islands + merge are part of the theorem-covered method: T-MERGE's
  "any convex pooling inherits PIP/MPM consistency" (cheap assembly; also makes OD-4 a theorem for the coded 4-island
  equal-weight pooling). EVAR / POOL (evidence variance) move to the scaling paper; re-planned in the Thu proposal.

## 2026-11-15 19:57 CT — W3-EDIT vs riders
- **D19.** Errata in parent files consumed by running riders (STATEMENT.md, lemmas/ of PSHARP, START2, START, MISR,
  RM2, RM) are CHAPTER-ONLY now (no in-place edit while riders hash them in DEPS); W3-EDIT CP1 groups them by parent;
  each rider absorbs the ones its delta restates; the rest go to a post-freeze in-place batch after the riders' CP3.
  In-place edits only in files no rider consumes. W3-EDIT told to take timestamps from `date` (stamped 20:45 at 19:57).

## 2026-11-15 20:02 CT — POLICIES §10: leads as child agents
- **D20.** From now on leads, helpers, reviewers and experts start as this thread's child agents (`delegate_task`,
  provider claudeAgent_claude_third, Opus 5.5 high; the child works in its ticket worktree by absolute path; the task text
  authorises it to start its own Sol/Astra reviewers and ≤ 2 helpers). Top-level only for a large independent theorem,
  with the reason stated. Running top-level leads (DIST, READER, START2-R, RM2-R, PSHARP-R, PSMC-S0, W3-EDIT, recorder)
  finish in place; each is settled when finished. dept/theory merged with origin/main (brief update). Research helper
  (PSMC digest) settled.
- W3-MISR-R launches as a child when PSMC-S0 writes CHECKPOINT_1 (cap 5 until Wed 18:00).

## 2026-11-15 20:03 CT — correction to D20 (owner, POLICIES §10)
- **D21.** Never settle, archive, cancel, interrupt or delete any thread or agent unless the owner asks; finished leads
  stay idle. The PSMC digest helper settled under D20 was **unsettled**. Heartbeat prompt updated. Relayed to all leads.

## 2026-11-15 20:04 CT — final owner rule (POLICIES §10), replaces D21
- **D22.** Let work run, then clean up: never cancel or interrupt; when a non-department thread we manage has finished
  for good (ticket done, recorder tasks done, helper/reviewer done) the manager settles it; never settle department
  threads; never archive or delete. A lead waiting at a checkpoint is not finished. Digest helper re-settled. Leads may
  settle their own finished reviewers/helpers (settle only); they must not cancel or interrupt anything.

## 2026-11-15 20:07 CT — recorder package C/D/E/F
- F clean (44 cleared) but empties paper/generated (blocks only for headline rows): asked HQ for (a) assemble.py blocks
  for HEADLINE_CANDIDATES rows (recommended) vs (b) Writing from READER_VERSIONS; F real run held until decided.
- D clean (POST2 10/10) with two record fixes needing HQ OK; E clean (B(ii) CODE-CHECKED; D-7 placeholder).
- C (W2-APP): PC1 Sol gates=FAIL 8.4 (Family-map REJECT; F1–F4 on post-C3 edits only; POST ACCEPT). Proposal to HQ:
  record the 10 ACCEPT rows on the C3 snapshot (RM2 precedent), Family-map excluded; F1–F4 later diff round.
- **D23.** A3 cascade (Ex-STAR/ENUM + 10 consumers): fix the root — recorder task H dry-runs W3-POST:Thm-1 (=SOP:TH09)
  acceptance on its C3 council and checks C-PACK:SL0, SOP:TH05.0; fallback honest re-status. No "checked-class by fiat".

## 2026-11-15 20:08 CT — owner priority: consistency results + their Lean parts
- **D24.** Campaign re-planned (NEXT_CAMPAIGN v1): (a) finish all consistency results (DIST CP3, riders, strength
  gates, reader versions, acceptance backlog); (b) Lean readiness list (child helper → research/LEAN_READINESS.md:
  Level-1 deterministic cores, stability vs this week's tickets, ready dates; Level-2 targets). T-MERGE parked;
  EVAR/POOL scaling paper. D18 approved by HQ.

## 2026-11-15 20:10 CT — W3-DIST S2 (Sol read of reader versions)
- **D25.** Tags: TC9 Theorem A EQUAL (Setup faithfulness: prior BB(1, r), r = non-constant predictors, cap min(r, n/2);
  "no identifiability condition" withdrawn → "no beta-min and no fixed lower bound on eigenvalues"); my view to HQ:
  no H5 card needed, HQ decides. Theorem B: "b_n > 0" added = WEAKER on a non-target companion (changelog row, reported
  at next CP). Sol diff check v1.3.1 → v1.4 owed before the next freeze. READER synced (prior as coded for all theorems).

## 2026-11-15 20:11 CT — W3-READER CP1 answered
- **D26.** Thm 6: full list + one-line abstract summary. Thm 7: version (a) main, (b) strengthening. Row 3.6 reader
  version in the bridge leg (consistency of printed outputs = owner priority); 3.5 one-line remark. Bridge leg GO
  (Tier B), one Sol review for bridges + v0.1→v0.2 diff. MISR → pillar 1 (row 1.4), recommended to HQ. Leg 2 (gates)
  brief placed in READER's folder (BRIEF_LEG2_GATES.md). Card v0.3 forwarded to HQ for H5. CP3 council target Fri a.m.

## 2026-11-15 20:12 CT — HQ approves recorder real runs
- Order: (G citefix branch) → D (POST2, two record fixes) → E (D-3/D-8; D-7 placeholder) → F + assemble.py tool fix
  (candidate blocks labelled "headline admission pending (strength gates)", regression test) → C dry run (10 ACCEPT
  rows bound to MANIFEST_PC1; Family-map excluded) → HQ → C real → H root-fix dry run (TH09/SL0/TH05.0; else honest
  re-status of 10 consumers). Commit hash + check totals after each, relayed to HQ.

## 2026-11-15 20:15 CT — 20 class-(iii) audit MINORs (W3-EDIT TRIAGE_MINORS, fd0dd92)
- **D27.** Escalated to HQ (6 ★ headline candidates incl. two W2-APP:POST sub-clauses). Fresh Opus adjudicator (child)
  gives E / PATCH / NARROW / REFUTED per row with consumers (propagate --dry-run) → research/ADJ_MINORS_iii.md.
  NARROW → LIFECYCLE §3 priced; headline main clause → H5 via HQ. C (W2-APP) real run held pending M57/M58; D/E/F go on.
  The 30 class-(ii) slips and 9 class-(i) wording items: routed after the adjudication (post-freeze editorial/patch batch).

## 2026-11-15 20:17 CT — H5 card 5 (headline split) folded in
- **D28.** READER told: 1.1 re-base on POST2 A1 + C (E variant) or explicit better-gate dispositions; 3.1 delivery
  clause out of the abstract until F-UNI's correct: gate is fixed (recorder task I); 1.4 flag on MIS(i)/(ii); Gaussian-row
  setting line; 3.7 into the abstract, 3.6 candidate, 2.2 fallback; condition (i): FAITHFUL fidelity read via the CP3
  council Sol seat (explicit FIDELITY line; Codex economy, told HQ), no unstated conditional inputs in the abstract,
  pooled-Ẑ corollary registered as a W3-READER claim and line-checked. CP3 Fri morning.

## 2026-11-15 20:22 CT — POLICIES §12 compute discipline
- **D29.** Relayed to all 8 leads. Correction to my disk note: no /home/fb31/scratch_recorder (never created); recorder
  clones go in an ignored `_scratch/` inside its own worktree (record-1115), one at a time, removed when done; its /tmp
  clones removed when no task needs them. W3-DIST arrays (~70 MB .npz) already git-ignored in work/numerics/arrays/;
  stay there. My own scratchpad temp files removed.

## 2026-11-15 20:26 CT — HQ: 6th slot; Lean launch Thu 11-19
- **D30.** W3-MISR-R launched as a child agent (6th lead until PSMC-S0 closes; then cap 5, 3 after Wed 18:00).
- Lean department launches Thu 11-19 (HQ): inventory + Level-1 batch (SL0, LT♯ core, T01 prior counting, DIST Lemma H),
  then the score base; Level 2 Mon 11-23 (DIST-1 if CP3 landed, else W3-POST:Thm-1). LEAN_READINESS.md stays current
  (refresh after Wed rider CP3s and DIST CP2/CP3). Old sorry-free snapshot:
  Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/L-LEAN/ (STATUS.md, REPORT.md).

## 2026-11-15 20:32 CT — adjudication of the 20 class-(iii) audit items
- **D31.** E 2, PATCH 6, NARROW 12, REFUTED 0; no headline-candidate main clause affected. W2-APP:POST M57/M58 PATCH
  (sub-clause / parenthetical): C real run proposed to HQ on MANIFEST_PC1; the patches join F1–F4 in the post-freeze
  Family-map diff round. F-UNI M27 PATCH: gate record fix now (task I), text after RM2-R CP3 + H5 card. 12 NARROW →
  one post-freeze LIFECYCLE §3 batch (priced), H5 card for GEN (C4), FAC-CS (C1), SAMP:Pkg. Narrowed wordings added to
  Docs/Writing/QUEUE.md for the chapter; READER told. Open checks M69, M05 go into the batch prep.

## 2026-11-15 20:39 CT — POLICIES §12 rules 8–9: department folders
- **D32.** Owls: /home/fb31/SMC_Theory_Department/ laid out (tmp/, ci/, recorder/, logs/, helpers/, INDEX.md). All new
  temp/CI/clones go there (all 9 leads told; RIDER_RULES updated). Idle bvs_tmp/{theory,ci} + top-level department
  folders migrate there at a quiet moment (after the running G clone and W3-EDIT CI finish); bvs_tmp then retired for us.
  NOTS: migration of theory_w2/w3, /scratch/fb31/theory_w2|3, P6 outputs into /home/fb31/SMC_Theory_Department (+ scratch
  link) is planned after the Wed freezes, calm and idle-only, with INDEX.md; first a single read-only check that Owls
  can reach NOTS (HQ_NOW said it could not: host key) — if not, the migration runs via HQ/Engineering.

## 2026-11-15 20:41 CT — HQ on D31
- C (W2-APP) real run approved (10 rows on MANIFEST_PC1, Family-map excluded); F-UNI stale gate = record fix now; M27
  text after RM2-R CP3 as H5; 12 NARROW = one post-freeze batch with one H5 card for M61/M35/M30; chapter guard confirmed
  (Writing QUEUE + READER already done). Real-run order D → E → F → C → F-UNI gate. Recorder told.

## 2026-11-15 20:41 CT — NOTS scratch purge risk (14 days without access)
- **D33.** Engineering copies /scratch/fb31/theory_w2 and theory_w3 (P6) today, checksum-verified, into
  /home/fb31/SMC_Theory_Department/records/ (created + indexed in INDEX.md). On arrival: I verify the checksums against
  Engineering's manifest and index each dataset (source, size, files, check result). Rule: data of record lives on Owls
  NFS (later the owner's laptop), never only in NOTS scratch for more than 7 days; the NOTS move (D32) keeps that.

## 2026-11-15 20:42 CT — SHARP3 triage (W3-READER, f7d2ad8)
- No correctness problem. NC_r every island = restatement (islands i.d. given 𝒞; class C). P-MAP localisable to 𝒜 =
  trivial restatement (W3-SAMP errata). Gate record: P-START NECESSARY-FOR-ROUTE in Thm C's any-parameter scope,
  ARTEFACT at production budgets (E|W−1| ≤ 2·TV attained at N_e = T = 1).
- **D34.** Two post-freeze riders queued: **SAMP-R1** (truth-free D, TV re-centring of C, hybrid TR bound, LT rate
  under NC_r; READER thm10) and **SCR-R1** (drop "fixed" signals, ℓ¹ → total signal, exponential rate; READER thm8).
- Gates PASS on all five-pillar rows except 1.1 (POST2 C/E: PENDING-DISPOSITION of 4 R03b proposals; SHARP3 addendum
  g05–g06 with HQ).

## 2026-11-15 20:43 CT — HQ: D32 approved; NOTS access exists
- Owls → NOTS works (`ssh nots`, key ~/.ssh/id_ed25519_nots; POLICIES §5). The department runs its own NOTS move after
  the Wed freezes under §12: one multiplexed session, idle data only, INDEX.md on NOTS, no deletion without a verified
  copy on Owls (records/ copy by Engineering today; verify + index on arrival). Plan: Thu 11-19 or later, one session.

## 2026-11-15 20:50 CT — row 1.1 card (R03b + SHARP3b)
- **D35.** Card forwarded to HQ (consultant): A+, E+, E-floor+ DEFER as POST2-O1..O3; B+ REJECT (no bearing); gate PASS
  with named open items. New expectation lower bound on every design → **post-freeze rider POST2-R1** (not a widening of
  T12: W3-PSHARP-R is in its statement lock; one step unverified). Queued.

## 2026-11-15 20:52 CT — H5 card 6 (row 1.1) agreed
- **D36.** Row 1.1 better = PASS with named open items O1–O3 (B+ rejected; N1 → POST2-R1). Conditions to READER: floor
  "sufficient; not known to be necessary (O3)"; Thm 1′ "no eigenvalue condition off S₀"; improvable + open necessity kept
  on POST2:C/E; "sharp" only on witness designs (1/√n on every design) until N1; no displayed margin value. Gate set after
  1–4 are in the files.
- Post-freeze order (owner tie-break): **POST2-O3 (E-floor+) first**, then **POST2-R1 (N1) with POST2-O2 (E+)**, each
  kill-budgeted. O2 rider must price the MISR rebuild: if c₁ < c₀ (258.9 vs 192 at s = 2, A = 1) MIS(i′) covers C-MIS's
  whole inclusion range → C-MIS → MISR supersession possible (H5).

## 2026-11-15 21:03 CT — W3-PSHARP-R CP1: GO
- **D37.** Target clauses fixed (Prop A-E, Cor A1-E STRONGER/headline, Cor A2-E, A2C → open item if not a restatement,
  readings A3′/B3′); hypothesis moves approved. Conditions: witness-only "sharp" scope (card 6), no extra displayed
  constants. H5 input sent to HQ; READER_DELTA staged in READER row thm3 as pending until CP3. CP3 target Tue, latest Wed.
- W3-DIST: BR1 (Astra break review) NOT BROKEN, 3 MINOR; L2 back — CP2 report expected from the lead.

## 2026-11-15 21:05 CT — W3-DIST CP2 (soft): CONTINUE
- **D38.** BR1 NOT BROKEN (3 MINOR repaired); all line checks VERIFIED first attempt; DIST12.md in L6. TC9 EQUAL (HQ);
  WEAKER non-target rows to CP3; n₀ remark in REPORT only; unverified premises carried as "conditional on …". Next: L6 →
  Sol diff check → REPORT → Astra sweep → citecheck → council → CP3; council-freeze date requested from the lead.

## 2026-11-15 21:34 CT — recorder real runs on main
- E 68d48f4 (Engineering D-3/D-8), F 70644a2 + cec478b (assemble.py candidate blocks + 44 flags cleared +
  HEADLINE_CANDIDATES.md), D 8efc627 (W3-POST2 10 rows PROVED-CHECKED conditional). check.py 468 / 0 ERROR; tl 174/0.
  Next: C dry run (cascade until H; H may precede C's real run), F-UNI gate, CI venv, I, J.

## 2026-11-15 21:41 CT — task J findings (escalated)
- Platform bug: _pcase lower-cases accept artifact paths on Windows → 57 stale 11-12 records (49 match after folding).
  Proposed: one-line tool fix (case-preserving _pkey) + regression test + narrow Opus code review + one Linux re-record.
- **My miss:** the citefix merge (66b67f7) changed C-MIS files that W3-START and W3-MISR council manifests list as EXT
  inputs → manifest verify fails (A4 START 21, MISR 7; A5 START2). W3-EDIT had flagged the drift; I judged it harmless
  because the tickets were accepted, without checking the EXT-input consequence for re-record and downstream CP3s.
  Lesson: before merging an edit to any file, grep **all** MANIFEST_* (accepted ones too) for it, not only running riders.
  Proposed (a) PC-style diff check + re-frozen manifests with seat carriers now; (b) EXT-at-freeze-commit tool change post-freeze.
- 8 genuinely stale rows re-record after (2); Cont-F/R re-point is HQ's call.

## 2026-11-15 21:43 CT — HQ on task J
- **D39.** Case-folding tool fix approved (case-preserving _pkey + regression test + narrow Opus code review), then one
  Linux re-record of the 49, PSHARP first. Manifest drift: (a) now — Opus diff check (running: research/PC_CMIS_CITEFIX_opus.md)
  then re-frozen START/MISR manifests with seat carriers; (b) EXT-at-freeze-commit tool change after Friday. Cont-F/R recorded
  as-is (implication lemmas; by design). PROTOCOL.md: manifest-impact check before any merge (§C) + B11 (Opus diff checks
  for citation-only changes). CP3-blocking status report from the recorder by Tue 12:00.

## 2026-11-15 21:48 CT — W3-START2-R CP1: GO
- **D40.** Target approved (16 claims; (iii) under (L-gain-0); F2⁺⁺/OVL⁺⁺ restated). T9/T11 not adopted (open items).
  Helpers A (Opus, T8) and B (Sonnet, numerics) approved. Priority: headline clauses (T3⁺⁺)(b), IF-START⁺⁺, (T1⁺⁺) first;
  restatements drop to a post-freeze rider if Wed 18:00 is tight. H5 input to HQ. READER row thm5.
- PSMC-S0 FR1 (Sol) > 2 h — flagged to HQ (low priority, off the critical path).

## 2026-11-15 21:55 CT — W3-EDIT CP1 (final): manifest-impact check applied
- **D41.** First use of the manifest-impact rule: W3-EDIT's in-place diff touches files listed in 4 accepted council
  manifests (W2-APP MANIFEST_PC1 ← C run!; MISR R1/R2; PSHARP R1/R2; START2 R1). Merge now only the unlisted subset
  (02_method.tex, W1-N3 LFP, W1-PXN CR + W1-PXN:CR.R-prime patch rehash) via branch theory/W3-EDIT-now; the rest
  POST-FREEZE with the manifest re-freeze / EXT tool change. Lead asked to build the branch; recorder adds the rehash.

## 2026-11-15 22:12 CT — W3-DIST L6-01 (MAJOR on TC3 sentence)
- **D42.** Lead repaired constants (X.md v0.4, DIST12 v0.2) to keep TC3 as fixed: M₀ ≤ 16 + 4(1+s₀^r)(A+1) +
  3(M+M′)/(2σ*²), C = C(A, σ*², M, M′). Conditions: fresh Sol re-check of exact diffs + all STALE rows (combined with
  D1 diff check); reviewer confirms EQUAL tag and that "e^{s₀}q ≤ ½" needs no new hypothesis; else WEAKER on TC3 =
  early checkpoint to HQ. No second break review for a constants-only repair. HQ informed.

## 2026-11-15 22:15 CT — W3-MISR-R CP1: GO
- **D43.** Lock LOCK-WITH-AMENDMENTS (1 MAJOR, 3 MINOR applied). Targets fixed: CorG-min, CorGb-plus (extension
  approved), CorH-plus (+ KL), CorH-U ([LA-1] approved; its statement-change check folded into the Sol line-check agent).
  MIS(i)/(i′)/(ii) unchanged; reader row thm4 weaker hypotheses / same displays (STRONGER) → H5 at CP3. CP3 target Tue 11-17.
