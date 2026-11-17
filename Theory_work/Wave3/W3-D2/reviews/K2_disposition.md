# W3-D2 — K2 disposition (lead, 2026-11-17)

Reply: `reviews/K2_recheck_opus.md` (Opus 5.5 high, new agent): RESOLVED-WITH-AMENDMENTS; K1-1..K1-4 resolved, PROOF diff
breaks nothing; C 0, S 0, F 5, E 6. All accepted (diff `reviews/K2_repair.diff`). No claim span and no proof step changed.

| finding | tag | disposition |
|---|---|---|
| F-1 §0 gloss: σ² and X_S clash with §0's symbols | F | ACCEPT: working variance v, "X the standardised design", IG(0.01, 0.01) (STATEMENT v1.3 §0) |
| F-2 caveat (b) changes subject; Theorem 2X's own (A2) range contains k̄_n | F | ACCEPT: caveat (b) rewritten (masters incomparable; Thm2X's (A2) stronger than LSF on the floor; "smaller sets" measured against the reader statement's 5(…)); same in REPORT §2(b). Substantive for the recording package |
| F-3 REPORT assumption line refs one line early | F | ACCEPT: `:35-36`, `:37` |
| F-4 Cor2X tagged A:LSF | F | ACCEPT: A:CORR-FLOOR-LOG, with the correlation-matrix reading in `notes` |
| F-5 `implies: W3-POST:Cor-1R` false as an edge | F | ACCEPT: `implies:` empty; conclusion-level note in `notes` |
| E-1 PROOF :50 reading → the master's usage | E | ACCEPT (reviewer's wording) |
| E-2 PROOF :4 version; STATEMENT :1 note | E | ACCEPT |
| E-3 premise span :76-84 → :77-84 | E | ACCEPT |
| E-4 "explicit bound" → b_n and 2b_n, n ≥ n* | E | ACCEPT |
| E-5 card "of size at most" | E | ACCEPT |
| E-6 changelog check cell | E | ACCEPT |

Also (lead, for the ingest tool): PROOF.md:3 now carries the full conditional status verbatim (status_source); REPORT
assumption text avoids "|" inside fields; `note:` → `notes:`. Staged ingest: 0 problems; acceptance PASS (both ids).
Re-check: K3, new Opus agent, on `reviews/K2_repair.diff`.
