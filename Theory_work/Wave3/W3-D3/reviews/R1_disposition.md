# W3-D3 — council R1 disposition (lead, 2026-11-17)

Round R1, MANIFEST de19cf54f91f81defa8bc75a5b174e01a697ea75c3984f70106efaa23a39b768.
- Sol seat (`reviews/R1_council_sol.md`): ACCEPT Thm2SG, B3w, ExSG; score 8.5, gates=FAIL on S1 (with F).
- Opus seat (`reviews/R1_council_opus.md`): ACCEPT all three; score 8.8, gates=FAIL on S1; E1–E6.
R1 not passed. Both seats' S1 is the same defect in prose outside the registered spans (card text, REPORT, READER_DELTA): the
centring and common-constant qualifiers of STATEMENT §§4–5 were dropped. No finding touches a registered claim span except two
editorial clarifications (E4, E5), tagged EQUAL. All findings accepted.

| finding | disposition | where |
|---|---|---|
| sol S1 [S/F] "implies Song and Liang's Condition 1" without "for z = x − m_n" (counterexample: mean (n, n)) | ACCEPTED: qualifier restored everywhere it was dropped | REPORT §2, §3 card; READER_DELTA class paragraph; PLAN, TARGET (same omission) |
| opus S1 [S] card: "each sub-Gaussian" drops the common constant L; NH14 "centred"; SL "x − m_n" | ACCEPTED: card rewritten — mixtures of independent mean-zero, unit-variance features sub-Gaussian with one common L (bounded: one common K, L = K); NH14 for centred rows, Σ_n = I; SL for x − m_n | REPORT §3 |
| opus E1 changelog check cell "pending" for ExSG (b) | ACCEPTED: cites K1 (CONFIRMED STRONGER on ExSG) | STATEMENT §9 |
| opus E2 TARGET "proposed" | ACCEPTED: HQ ruling D114 | TARGET |
| opus E3 TARGET "correlated Rademacher mixture" run; N2 docstring K | ACCEPTED | TARGET; numerics/N2 docstring (output unchanged) |
| opus E4 ExSG (b) common K | ACCEPTED: "every ξ_k …, the same K > 0 for all k" (EQUAL) | STATEMENT §3 (b); ASSEMBLY ExSG claim |
| opus E5 𝒜′_n for n < n₁ | ACCEPTED: "put 𝒜′_n := ∅" (EQUAL) | STATEMENT §2 (c); B3w (c) |
| opus E6 citecheck docstring §5 → §6 | ACCEPTED | citecheck.py |

STATEMENT v1.3 (changelog rows 1.3). Diff round R2 (Opus only, per the ticket): `reviews/BRIEF_R2_opus.md`; it judges both
seats' R1 findings and the STALE DEPS rows.
