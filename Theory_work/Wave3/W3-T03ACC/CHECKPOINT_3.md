# W3-T03ACC — CHECKPOINT 3 (council passed; 2026-11-16)

PROVED (candidate) (W1-T03R); LC-A, LC-B, LC-C VERIFIED (W3-T03ACC); council R1 PASS (astra 9.5, opus 9.4)

(Line 3 above is the per-claim status, verbatim, of `W3-T03ACC:T03S.1`–`T03S.5`; status_source of the registry block.)

## 1. Passing round (all reviews NORMAL mode, fresh, blind first read)
- **R1**, MANIFEST `9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6` (41 files + v3_score.h, v3_preprocess.R).
  Seats: **Astra** (codex gpt-6-astra, high) 9.5, gates PASS, T03S.1–.5 ACCEPT (`reviews/R1_council_astra.md`);
  **Opus** (Opus 5.5 high, Claude Third) 9.4, gates PASS, T03S.1–.5 ACCEPT (`reviews/R1_council_opus.md`).
  Findings: 0 C/S/F; 10 E (3 duplicate ERRATA E1–E3), all held for the editorial batch (`reviews/R1_disposition.md`).
  No diff round.
- `manifest.py bind`: `bind: OK, 2 review(s) give a PASS verdict (>= 8.0) on MANIFEST 9714aea4…`; council cell:
  `R1; MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6; astra=9.5 PASS(reviews/R1_council_astra.md); opus=9.4 PASS(reviews/R1_council_opus.md)`.
  `manifest.py verify`: OK.
- Chain: SL1 lock (Sol): LOCK WITH CHANGES → v1.1 (no clause WEAKER or STRONGER than the record; A ≥ 1 and p ≥ 2 not added,
  confirmed by every line check). LC-A, LC-B, LC-C (Sol): VERIFIED, 0 GAP, 0 ERROR, covering every consumed [P1]/[P3] step.
  DEPS 35/35 OK. citecheck 69 citations, 0 MISS (`reviews/CITECHECK.txt`). Holds: none on TH09/T03/TH128.
- Supporting evidence only (v4 H3): HQ's API Fable audit, both samples MINOR, 0 GAP/ERROR; its 4 slips were named points of the line
  checks: 3 confirmed editorial (ERRATA E1–E3), 1 moot (`reviews/API_dispositions.md`). Not given to the seats.

## 2. Staged ingest
- On `REPORT.md` (frozen in R1): **refused, 7 form problems**: the status is not verbatim at status_source `REPORT.md:17-23` (×5);
  `implies TH128` is not a registry id (the id is `SOP:TH128`); `kind: remark` is not an allowed kind (T03S.5).
- On the form-fixed copy `reviews/REPORT_formfix.md` (same block; only the fixes listed in its header): **5 claims, 0 problems;
  staged `check.py`: 0 ERROR (fragment 0, live 0); acceptance T03S.1–.5: PASS**. Outputs: `reviews/INGEST_STAGED.txt`.
  The live registry was not touched.

## 3. For HQ
- **Per-claim status (verbatim, all five):** `W3-T03ACC:T03S.1`–`.5`: "PROVED (candidate) (W1-T03R); LC-A, LC-B, LC-C VERIFIED
  (W3-T03ACC); council R1 PASS (astra 9.5, opus 9.4)". They imply `SOP:TH09` (the same statement) and `SOP:TH128`.
- **Record fix (v4 §7, form only):** ingest from `reviews/REPORT_formfix.md`. Alternatively, HQ can apply its three changes to
  REPORT §4 as a record edit. No council round is needed (form failure).
- **Consumers:** rows 1.1, 1.2, 3.1 may drop "conditional on SOP:TH09" (HQ/H5 call). There is no change to any headline statement or reader text (`READER_DELTA.md`).
- **Editorial batch (later, never blocking):** ERRATA E1–E4 plus R1's E items (`reviews/R1_disposition.md`), applied
  after acceptance as one "editorial only" version bump.
- **Agents:** all settled (SL1, LC-A/B/C, R1 Astra/Opus). Reviewer scratch removed.
