# W3-FAMC — CHECKPOINT 3 (hard; 2026-11-17; lead Claude Opus 5.5 high, claudeAgent_personal) — recording package for the manager

Tier B assembly (no new lemma, no theorem change, not a Lean target). Codex reviews: 5 (Sol R1 line check, R2 diff, R3/R4/R5
council seats), all gpt-6.2-sol at high, run one at a time. Claude reviews: 4 (E2 check, R3/R4/R5 council seats), all
claude-opus-5-5 high on claudeAgent_personal, none an author. No Fable; no Claude Third or Work. HOLDS.md (origin/main
a1d55cef): 0 HOLD lines. All 12 external inputs are unchanged between a779c1df and origin/main a1d55cef, and every consumed
claims.tsv row is ACTIVE at the version and status quoted in STATEMENT §4. AR kill rule not triggered. Elapsed: under one
lead-day of the 3-day budget.

## Passing round
- **R5 (FORM-ONLY confirmation after R4's REPORT repair):** `reviews/R5_council_sol.md` ACCEPT, 10.0, gates PASS;
  `reviews/R5_council_opus.md` ACCEPT, 9.5, gates PASS. `reviews/R5_bind.txt`: **bind OK**. Council cell:
  `R5; MANIFEST 3305c329f1555766ac6839f98901d92cb1db61bcad41e2d27a74863af7a3f68e; sol=10.0 PASS(reviews/R5_council_sol.md); opus=9.5 PASS(reviews/R5_council_opus.md)`.
  **Binding manifest: `reviews/MANIFEST_R5.txt`** (21 files, 13 external inputs including the E2 check report; no registry
  files and no live logs). `manifest.py verify`: OK.
- History: R1 Sol line check (ACCEPT WITH CHANGES, 11/11 accepted) → R2 Sol diff (5/5 accepted) → R3 council (sol 8.8 /
  opus 9.0, both gates FAIL on provenance/registry F; no C or S; math ACCEPT by both) → R4 (opus 9.5 PASS; sol 9.0 FAIL on
  one converter defect, F-R4-1) → R5 both PASS. The registered claim §1 has been byte-identical since v1.2 (R3–R5).
  Dispositions are in `reviews/R{1..4}_disposition.md`.

## Record state
- Staged ingest `reviews/INGEST_staged.txt`: 1 claim, 2 new assumptions (A:FAMC-DESIGN, A:FAMC-COEF), **0 problems,
  0 ERROR**, acceptance (W3-FAMC:Cor-FAMC) **PASS**. The live registry was not touched.
- `ingest.py convert REPORT.md`: 0 PROBLEM lines (both new definitions convert in full; checked by both R5 seats).
- citecheck `reviews/CITECHECK.txt`: 93 checks, 0 failures. DEPS: 10 rows, recomputed by the R4/R5 seats. The checked_by
  column inside the frozen manifest is still UNCHECKED; a FORM-ONLY DEPS re-freeze can be done if the recorder wants it.

## Per-claim status (proposed; the recorder computes the final label)
- `W3-FAMC:Cor-FAMC` (STATEMENT.md:49-81; premises :25-32): "PROVED (by this seat, unchecked)" (`lemmas/A_assembly.md:3`)
  + council R5 above. Registry block: REPORT.md §6 (:39-50).
- Inputs (STATEMENT §4, D126 expansion): all PROVED-CHECKED except `W3-RM2:Ex-PolyR` (PROVED; line-checked; Opus seat not
  examined) and its conditions `W2-LOC2:Lemma-BC`, `Lemma-IR` (PROVED, unchecked). **HQ DP1: the AR half is recorded
  unconditionally** on `reviews/E2_check_opus_R1.md` (independent Opus check: PASS; bound in the manifest). Recorder:
  please confirm the status label carries no "conditional on Ex-PolyR" (HQ ruling), or tell me the form HQ wants.

## For HQ / the card
- Reader text for the H5 card and Writing: STATEMENT §1R. Writing's "any fixed AR correlation" comes after recording (HQ
  DP2). No contact with Writing.
- For W3-RM2 (via the manager): E2 PASS, plus three wording notes (`L6_poly.md:106`, `L6_examples.md:76-84`,
  `L6_examples.md:164-166`). No RM2 file was edited.
- Better-theorem proposals (Opus R3; not adopted, D107): component-wise alignment for (BLK-s), slowly growing groups, a
  logarithmic Q for AR, banded/Toeplitz designs.
- Known non-blocking: REPORT names no council in §1 beyond R3/R4 (this checkpoint is the council record).
- Errata after the freeze: none.
