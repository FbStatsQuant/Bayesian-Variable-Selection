# Theory Department — decisions log

## 2026-11-15 19:35 CT — riders queue set up
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
