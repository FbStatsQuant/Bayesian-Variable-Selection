# W3-MISR-R — CHECKPOINT 3 (hard; 2026-11-16; lead Claude Opus 5.5 high, Claude Third)

Tier B rider (T13), NORMAL mode throughout. HOLDS.md (origin/main): no holds. Branch merged with origin/main before the
R1 freeze; external inputs = main at both freezes.

## Council outcome: cap reached, no passing round — only a reader-text sentence blocks
| round | manifest | Sol (OpenAI seat) | Opus (Claude seat) |
|---|---|---|---|
| R1 (blind) | fadb67e8cceacbceaf7b226925155c5817aa5915b4f333542e3aef7bfba8a994 | 4/4 ACCEPT, 7.8, gates=FAIL | 4/4 ACCEPT, 8.5, gates=FAIL |
| R2 (diff) | 227720d3d5b3ef95adbc1e91f7835058d7858986ef4b173a4044f65ad49879ea | 4/4 ACCEPT, 8.6, gates=FAIL | 4/4 ACCEPT, 9.2, gates=FAIL |
No C finding in either round; `correct` PASS from both seats in both rounds; STATEMENT and lemmas unchanged since K2.
R1's blocking items (F, in READER_DELTA and REPORT registry lists) are all RESOLVED in R2. Both R2 seats raise one new F on
the **same sentence** introduced by the R1 fix (`READER_DELTA.md:61-65`, the (A0) "why" line: the contrast condition must
be centred with the (A0) variance, and necessity must be for the omitted part minus its linear candidate component).
Fix drafted in `reviews/R2_disposition.md`, **not applied** (MANIFEST_R2 kept intact). `manifest.py bind` R2: REFUSED
(gates=FAIL); `manifest.py verify` R2: OK.

## HQ decision needed (v4 §5.6–5.8)
(a) Order one more round (diff-only, both seats, the one-sentence fix + §1 table alignment); est. 1 h, 2 Codex-equivalent
reviews (1 Sol). Recommended. Or (b) treat READER_DELTA as a proposal outside the claim manifest (claims all ACCEPT, no
C/S/F names a claim clause) and label on the R2 evidence — HQ's call on form; the bind tool will not bind gates=FAIL.

## Records
- DEPS.tsv: 10/10 OK (K1 + K2). Citecheck: 152 checks, 0 failures (`reviews/CITECHECK.txt`).
- Staged ingest `REPORT.md --staged`: 4 claims, 0 problems; check.py 0 ERROR introduced; acceptance 0 ERROR (the stale
  W3-MISR parent accept records seen on 11-15 no longer appear on current main — recorder task J apparently done).
- Statuses (verbatim, lemma line 4): CorG-min "PROVED (by this seat, unchecked)"; CorGb-plus "PROVED (by this seat,
  unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, SOP:TH09, SOP:TH128, C-MIS:GDb"; CorH-plus
  "PROVED (by this seat, unchecked), conditional on W3-POST2:D"; CorH-U "PROVED (by this seat, unchecked), conditional on
  W3-POST2:D, W3-POST2:C, W3-POST2:A0; clause (G) also conditional on W3-POST2:E, W3-POST2:A1, SOP:TH09, SOP:TH128, C-MIS:GDb".
- Changelog: v1.1a WEAKER (an interpretive KL sentence restricted to a deterministic intercept; no display changed; tag
  set by K1, reported here per v4 §4.2), v1.1b EQUAL, v1.2 NEW-CLAIM (CorH-U (G), CP1-approved; K1 change check).
- Reviews (all Sol = gpt-6.1-sol high): L1 lock, K1 line check + change check, K2 re-check, R1/R2 Sol seats (5 Codex);
  Opus R1/R2 seats. ERRATA.md: E1–E6 (editorial batch). Better-theorem proposals (Opus R1) for HQ: `reviews/R1_disposition.md`.
- W3-DIST pointer: `REPORT.md` §3, HEURISTIC/OPEN only.
