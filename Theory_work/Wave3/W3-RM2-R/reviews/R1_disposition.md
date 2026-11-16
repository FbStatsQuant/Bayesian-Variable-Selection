# Council R1 disposition (lead) — Opus 8.7 FAIL, Sol 8.5 FAIL; every claim ACCEPT by both; correctness gate PASS by both

| seat / # | tag | finding | disposition | where |
|---|---|---|---|---|
| opus F1 | F | REPORT/REGISTRY conditions vs STATEMENT:234 (Ex-Proxy-d lacks SOP:TH09; TL-F-c carries it and the Q3 row) | ACCEPTED. Ex-Proxy-d: status and depends_on now carry SOP:TH09 (as STATEMENT:234). TL-F-c: points at the Q2 row (STATEMENT:189) and Q2 §4 only, no TH09. POST/MODE-F (Q3 row, Q2 §6) recorded as a note under RM2-F-plus, which carries TH09. | REPORT.md §2, §5 |
| opus F2 | F | READER_DELTA R7.2: D not fixed, non-strict constant | ACCEPTED, the seat's fix verbatim (fixed D > 2 + 4A, strict margin, choice of c_TL absorbing (n − 1)/n) | READER_DELTA.md R7.2 and the note below the table |
| sol F1 | F | TARGET parity row attributes a beta-min selection result to Song–Liang (2015) Thm 1–2 (they are Hellinger contraction results) | ACCEPTED. Song–Liang and Narisetty–He (not re-verified) withdrawn from the row; YWJ (2016) kept; H5_SUMMARY likewise | TARGET.md §2; H5_SUMMARY.md |
| sol S2 | S | TARGET says the beta-min order is "necessary by numerics/heuristic" | ACCEPTED, the seat's wording ("HEURISTIC: … necessity is not proved here") | TARGET.md §1 |
| opus E3 | E | DLV-0 depends_on incomplete | applied (REPORT only): C-DLV:Prop-F@proof, P1-Inventory, L2-S3 added; note on FIN s6 allocation | REPORT.md §5 |
| opus E6 | E | REPORT row / sharpness pointers | applied (REPORT only) | REPORT.md |
| opus E8 = sol E5 | E | TARGET version, "planned" numerics, necessity wording | applied (TARGET only) | TARGET.md |
| sol E3 | E | RESULTS.md "only competitor" → "binding competitor" | applied | numerics/RESULTS.md |
| sol E4 | E | R7.2 constants | applied with opus F2 | READER_DELTA.md |
| opus E1, E2, E4, E5, E7, E9 | E | wording/notation in STATEMENT and lemma files | recorded in ERRATA.md E2–E7, **not applied** (STATEMENT and lemmas stay at their checked shas; one editorial batch later) | ERRATA.md |
No change to STATEMENT.md or any lemma file; DEPS unchanged (all OK). Changed files: TARGET.md, REPORT.md, READER_DELTA.md,
H5_SUMMARY.md, ERRATA.md, numerics/RESULTS.md (diff: `reviews/R2_diff.txt`). Next: freeze MANIFEST_R2; diff round, each
seat model in a fresh thread with its own R1 review, the diff and the DEPS dependents of every changed object.
