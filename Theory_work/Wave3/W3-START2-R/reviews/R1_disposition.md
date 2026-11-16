# Council R1 — disposition (lead, 2026-11-16)

Round R1 on MANIFEST 1834d1c0941f297eef629337b02361097a0d2f02ae1596afeaa4bf322ebbab19.
* seat sol (`reviews/R1_council_sol.md`): every claim ACCEPT; G6 FAIL on one **F** finding; score 7.9; gates=FAIL.
* seat opus (`reviews/R1_council_opus.md`): every claim ACCEPT; all gates PASS; no C/S/F finding; score 9.3.
R1 does not pass (sol gates=FAIL). One accepted F finding ⇒ diff round R2 (PROTOCOL_v4 §5.5).

| finding | tag | disposition |
|---|---|---|
| sol #1: READER_DELTA (A6) "why" line says uncorrelated nulls make "each expected factor of order √log n"; the proof gives an upper bound on a truncated envelope's expectation plus Markov | F | **Accepted.** `READER_DELTA.md:50-55` reworded: the proof bounds the expectation of a truncated envelope by O(√log n) (an upper bound), and averaging and Markov's inequality give the displayed rate; the (A5)-only sentence likewise says "the same upper bound then carries a factor e^{O(√log n)}". The displayed reader conclusions are unchanged. |
| sol #2–#4; opus #1–#10 | E | Accepted as errata; recorded in `ERRATA.md` (11 rows), not applied in the frozen content (§5.3). |
| sol better-theorem: keep the truncation level ⇒ o₀ = O_P(√((log 2p + log log n)/n)) | — | logged as a better-theorem proposal for HQ (not a finding) |
| opus better-theorem (3): interpolation b_n in (D5); separate second-order hypothesis in (b)(iii); F-2 threshold below 3/4 | — | logged as better-theorem proposals for HQ |

Diff round R2: the diff since MANIFEST_R1 is `READER_DELTA.md` (the F repair) and the new file `ERRATA.md`; DEPS has no
row for READER_DELTA (reader text; covered by gate F/G6), so no DEPS row is edited. Each seat gets, in a fresh thread, its
own R1 review, the diff and the dependents.
