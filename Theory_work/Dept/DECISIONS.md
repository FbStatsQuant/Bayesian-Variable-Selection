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
