# W3-START2-R — CHECKPOINT 3 (council passed) — 2026-11-16 04:50 CST

Lead: Claude Opus 5.5, effort high (Claude Third). Tier B rider, NORMAL mode throughout (all OpenAI reviews Sol,
codex gpt-6.1-sol, high). No git state changed by the lead. HOLDS (`origin/main:Theory_work/Wave3/HOLDS.md`): none.

## Passing round
**R2 (diff round) on MANIFEST 90886d0690e10474a213853b690f3b1ae62ad70a3c8cdf184fe99c497d713319** (`reviews/MANIFEST_R2.txt`).
* R1 (MANIFEST 1834d1c0…): sol 7.9 gates=FAIL (one **F** in READER_DELTA reader text; every claim ACCEPT); opus 9.3
  gates=PASS (no C/S/F). Disposition `reviews/R1_disposition.md`: F repaired (READER_DELTA (A6) "why" line now states an
  upper bound on a truncated envelope + Markov); 13 E findings → `ERRATA.md` (11 rows, not applied, PROTOCOL_v4 §5.3).
* R2: sol 9.0 PASS (`reviews/R2_council_sol.md`), opus 9.3 PASS (`reviews/R2_council_opus.md`); no C/S/F; every claim ACCEPT.
`manifest.py bind` output:
```
bind: OK, 2 review(s) give a PASS verdict (>= 8.0) on MANIFEST 90886d0690e10474a213853b690f3b1ae62ad70a3c8cdf184fe99c497d713319
council cell: R2; MANIFEST 90886d0690e10474a213853b690f3b1ae62ad70a3c8cdf184fe99c497d713319; sol=9.0 PASS(reviews/R2_council_sol.md); opus=9.3 PASS(reviews/R2_council_opus.md)
```
`manifest.py verify` on MANIFEST_R2: OK (04:44 CST).

## Review chain (all files in `reviews/`; briefs saved before launch)
| step | reviewer | result |
|---|---|---|
| SL1 statement lock | Sol, blind | LOCK WITH CHANGES (2 F, 3 E, 1 optional; all applied) |
| LC1 R1_VIS, R2_NEC + statement-change check of the SL1 rows | Sol, new agent | PASS, no findings; STRONGER/EQUAL tags confirmed |
| LC2 R3_RATE, R4_TRANSFER_COR, R5_EX | Sol, new agent | PASS WITH FIXES (1 S, 2 E; repaired) |
| RC1 (stalled on sandbox approval, completed late; `RC1_recheck_sol_late.md`) / RC1b (relaunch, of record) | Sol, new agents | LC2 repairs resolved; R5 FAIL on one E (four mis-continued short citations; repaired) |
| RC2 R5 citation repair | Sol, new agent | PASS |
| Council R1 / R2 | Sol + Opus 5.5 high, fresh, blind (R1); fresh threads (R2) | see above |
OpenAI reviews used: 8 Sol sessions (SL1, LC1, LC2, RC1, RC1b, RC2, R1, R2) — above the Tier B band 3–6 because of the
stalled RC1 relaunch and one editorial re-check.

## Record
* **DEPS.tsv:** every row under a claim OK (statement rows: SL1 + LC1; R1, R2: LC1; R3, R4: LC2 + RC1b; R5: LC2 + RC1b +
  RC2). The REPORT row reads "UNCHECKED (council)" in the frozen file; it was checked by council R1/R2.
* **Citation check:** `reviews/CITECHECK.txt` — 438 citations (332 with line ranges, 106 path-only); MISSING/OUT-OF-RANGE: 0.
* **Staged ingest** (`python Theory_work/INFRA/tools/ingest.py claims Theory_work/Wave3/W3-START2-R/REPORT.md --staged`; full
  output `reviews/STAGED_INGEST_CP3.txt`): "14 claim(s) to add; 0 problem(s) … ERROR introduced by this claims fragment: 0;
  ERROR already in the live registry: 0"; acceptance REFUSED with 162 acceptance ERROR, **all A5-accepted** (stale accept
  records of the consumed W3-START / W3-START2 claims — the registry issue the manager flagged at CP1; recorder fixing; not
  this ticket's). The REPORT `council:` field and `correct:` gates are to be filled by HQ from the council cell above.

## Per-claim statuses (verbatim author status; council decision)
| claim | author status (status_source) | council R2 |
|---|---|---|
| W3-START2-R:START-F, VIS-c, VIS-m | "PROVED (by this seat)" (`lemmas/R1_VIS.md:3`) | ACCEPT, ACCEPT |
| W3-START2-R:F4, NEC-b, NEC | "PROVED (by this seat)" (`lemmas/R2_NEC.md:3`) | ACCEPT, ACCEPT |
| W3-START2-R:BR, START-R, IF-START | "PROVED (by this seat)" (`lemmas/R3_RATE.md:3`) | ACCEPT, ACCEPT |
| W3-START2-R:F1 (F1–F3), TRANSFER, MIS, OVL | "PROVED (by this seat)" (`lemmas/R4_TRANSFER_COR.md:3`) | ACCEPT, ACCEPT |
| W3-START2-R:EX | "PROVED (by this seat)" (`lemmas/R5_EX.md:3`) | ACCEPT, ACCEPT |

## For HQ
* **Headline changes (H5 card):** START2 (T3⁺)(b) START-R and IF-START⁺ → with uncorrelated nulls, o₀ = O_P(√(log n/n))
  (optimal up to √log n against the floor); START2 (T1⁺) START-F → visibility at c·log n + 2 log p of the actual p, sharp at
  c = 1 for every p_n. Reader text: `READER_DELTA.md` (row "thm5").
* **Better-theorem proposals** (council; not findings): sol — keep the truncation level ⇒ o₀ = O_P(√((log 2p + log log n)/n));
  opus — interpolation b_n in (D5); separate the second-order hypothesis of (b)(iii); lower the F-2 threshold below A = 3/4.
* **Errata:** `ERRATA.md` (11 rows) for the editorial batch. **Open items:** REPORT §7 (W3-START2R-O1 MIS with general μ; T9, T11).
* Numerics (observations): G-1 rate consistent; (V-cp) switch not resolved at n ≤ 3200 (`numerics/RESULTS.md`).
