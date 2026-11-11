# Theory Wave 3 — HQ decisions log

- 2026-11-09 W3-POST: the protocol's mid-point + sweep layers are replaced, for this re-check ticket, by the two
  independent whole-chain adversarial re-checks R01 (gpt-6-astra high) and R02 (Opus high), followed by a passed council
  (C3: 8.8/8.7). Reason: the object was an existing proof chain, and two whole-chain adversarial reviews cover more than a
  mid-point + sweep. Labels: Theorem 1 chain "PROVED-CHECKED (W3-POST re-check)"; Lemma 1a′ and Proposition LB
  "PROVED-CHECKED (W3-POST: R01/R02 + council C2/C3 line checks)".
- 2026-11-09 W3-POST follow-up: launch W3-POST2 (improvements 1, 3, 4, 1b; 2 as stretch with a kill budget).
- 2026-11-11 (resume, owner go for launch 13:00 CT): providers per PROTOCOL item 2 amendment of 2026-11-11 (CP = Fable 5.2
  only; all other Claude on CW).
- 2026-11-11 W3-RM: keep STATEMENT v1.2.1 (both council rounds reviewed v1.2.x). Result stated as (V)+(L)+lattice
  condition (N)/(D-R); replacing (N) is the kill-budgeted path-level follow-up. Labels per clause: RM-0, RM-F, RM-R,
  Lemma E4, examples PROVED-CHECKED (council C2 Astra 9.8 / Opus 9.1).
- 2026-11-11 W3-SAMP: labels per clause CC, PC, MR, ST, D, LT#, C, TR PROVED-CHECKED (SW1 + council C1 9.1 / 8.8);
  NC_r necessity OPEN; P-START remains a named input (W3-START).
- 2026-11-11 W3-POST2: post-lock strengthenings (items 3, 4, 5 via (ID^M)) approved; E1 v2 restatement ruled within the
  kill budget. Claims A-E PROVED-CHECKED (council C1 8.6 / 8.6).
- 2026-11-11 W3-RM2 lead upgraded to Fable 5.2 (hardest open proof; sub-par theorem risk).
- 2026-11-11 registry ingest of W3-RM, W3-SCR, W3-POST2 via tools/ingest.py after PR #6 merges (rule 8 post-dates them).
- 2026-11-11 CORRECTION to this morning's labels (following pipeline review R01, rule 15): W3-SAMP:CC keeps its
  REPORT status (CODE-CHECKED); HQ does not upgrade it. The PROVED-CHECKED labels for W3-RM, W3-SAMP and W3-POST2 are
  **on hold** until a Sol diff check confirms that the edits made after each council (RM C2_disposition, SAMP C1 "11
  items applied", POST2 C1 disposition) are editorial or correct. Until then, registry statuses stay verbatim from
  each REPORT. W3-POST2 strength stays `better:PENDING` (four R03b proposals open).
- 2026-11-11 Headline flags: all 43 `headline=yes` rows were set by tools (ingest.py marks any claim with strength
  fields); none is an owner decision. They are treated as headline (changes need Felipe) until Felipe confirms the
  headline set at chapter v2.0. W3-SAMP:D and W3-SAMP:TR were registered from a mid-ticket draft; their final, council-
  reviewed statements are narrower (D: KERNEL hypothesis added; TR: the non-nesting label holds only for abstract
  targets). Recorded as NARROW+CLEAR, no dependent became SUSPECT. **Awaiting Felipe's approval.**
