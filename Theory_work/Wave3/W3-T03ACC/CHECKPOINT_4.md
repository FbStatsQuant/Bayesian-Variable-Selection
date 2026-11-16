# CHECKPOINT_4 — W3-T03ACC statuses after council R1 (HQ-written carrier, PROTOCOL_v4 §7; NOT a lead checkpoint)

Per-claim statuses (status_source = the line below each id):

W3-T03ACC:T03S.1
PROVED-CHECKED; council R1, MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6, astra=9.5 PASS, opus=9.4 PASS

W3-T03ACC:T03S.2
PROVED-CHECKED; council R1, MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6, astra=9.5 PASS, opus=9.4 PASS

W3-T03ACC:T03S.3
PROVED-CHECKED; council R1, MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6, astra=9.5 PASS, opus=9.4 PASS

W3-T03ACC:T03S.4
PROVED-CHECKED; council R1, MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6, astra=9.5 PASS, opus=9.4 PASS

W3-T03ACC:T03S.5
PROVED-CHECKED; council R1, MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6, astra=9.5 PASS, opus=9.4 PASS

SOP:TH09
PROVED-CHECKED (T03♯ only: the conjunction of W3-T03ACC:T03S.1–T03S.4, clause map CHECKPOINT_4.md §2; council R1, MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6, astra=9.5 PASS, opus=9.4 PASS; LC-A, LC-B, LC-C VERIFIED). Not upgraded (their statuses stay as at theory_main.tsv:68): T02(i♯) and T02(ii♯) PROVED, SF/XF VERIFIED; T01–T03 PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY

SOP:TH128
PROVED-CHECKED (the conjunction of W3-T03ACC:T03S.1–T03S.5 = record clauses 1–5, clause map CHECKPOINT_4.md §2; council R1, MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6, astra=9.5 PASS, opus=9.4 PASS; LC-A, LC-B, LC-C VERIFIED)

## 1. Record (HQ recorder, H5 card 12, consultant AGREE with four conditions; HQ GO real run (task T, H5 card 12, 2026-11-16))
- Council R1 PASS on `reviews/MANIFEST_R1.txt` (MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6): astra 9.5, opus 9.4, both ACCEPT on T03S.1–.5 (`reviews/R1_council_astra.md`, `reviews/R1_council_opus.md`); lead checkpoint `CHECKPOINT_3.md`. Acceptance binds to this manifest (no re-freeze). HQ seat carriers `reviews/R1_record_astra.md`, `reviews/R1_record_opus.md` (CITATION-ONLY: seat table verbatim + two HQ-derived rows SOP:TH09, SOP:TH128), bound with `manifest.py bind`.
- **Ingest is from the form-fixed copy `reviews/REPORT_formfix.md`** (REPORT.md stays frozen in R1). Its three form changes against REPORT.md §4: (1) status verbatim at its source (CHECKPOINT_3.md:3; REPORT.md:17-23 did not carry it verbatim); (2) `implies TH128` -> `SOP:TH128`; (3) T03S.5 kind `remark` -> `proposition`. Also repo-relative paths.
- Post-council fields (this carrier): status = the PROVED-CHECKED line above each id (council R1 passed); council cell of all seven rows = the carrier cell `R1; MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6; astra=9.5 PASS(reviews/R1_record_astra.md); opus=9.4 PASS(reviews/R1_record_opus.md)` (the R1 bind cell `R1; MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6; astra=9.5 PASS(reviews/R1_council_astra.md); opus=9.4 PASS(reviews/R1_council_opus.md)` names the seat reviews, whose tables carry only T03S.1–.5); correct: evidence = the R1 seat reviews. `implies` dropped (no T03S claim gives a whole statement of TH09/TH128; card 12 item 2): the per-clause relations are the clause map (§2), also in each claim's notes.
- Not applied (editorial batch, later): ERRATA E1–E4, the 10 E findings of R1 (`reviews/R1_disposition.md`), the API audit's 2 MINOR (`reviews/API_dispositions.md`).

## 2. Clause maps (coverage)
SOP:TH09 as registered (`Theory_work/State_of_Project/registry/theory_main.tsv:68`, statement column): "Posterior concentration 1 − π(S₀) = O_P(√(log n/n)) under R1, G, R, SE_λ, SE_w, BM; exact HPM and MPM consistent; large-signal inclusion without beta-min".
| TH09 clause | T03S claim | STATEMENT line |
|---|---|---|
| posterior concentration 1 − π(S₀) = O_P(√(log n/n)) under R1, G, R, SE_λ, SE_w, BM | W3-T03ACC:T03S.1 | `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:64` |
| MPM consistent | W3-T03ACC:T03S.2 | `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:65` |
| exact HPM consistent | W3-T03ACC:T03S.3 | `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:66-69` |
| large-signal inclusion without beta-min | W3-T03ACC:T03S.4 | `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:70-73` |
| hypotheses R1, G, R, SE_λ(j₀), SE_w(m♯_n; g₀), BM-∞ or BM(c > c₀) = Theory_work/Wave3/W3-T03ACC/STATEMENT.md:43-60 (SL1 lock: no clause WEAKER or STRONGER than the record, Theory_work/Wave3/W3-T03ACC/reviews/SL1_statement_lock_sol.md) | all | `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:43-60` |

Coverage of SOP:TH09: **complete** (4 of 4 clauses; T03S.5, scale invariance, is record clause 5, not in TH09's registered text). The TH09 row's status also names T01–T03 and T02(i♯)/(ii♯): **not upgraded** (scope T03♯ only).

SOP:TH128 as registered (`Theory_work/State_of_Project/registry/history.tsv:94`): "Posterior target consistency (statement of record W6-FIXREV2 section 1.2)" = `Theory_work/Wave3/W3-T03ACC/sources/statement/W6-FIXREV2_STATEMENTS.md:51-61`, clauses 1–5.
| TH128 clause | T03S claim | STATEMENT line |
|---|---|---|
| record clause 1 (Theory_work/Wave3/W3-T03ACC/sources/statement/W6-FIXREV2_STATEMENTS.md:53) | W3-T03ACC:T03S.1 | `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:64` |
| record clause 2 (Theory_work/Wave3/W3-T03ACC/sources/statement/W6-FIXREV2_STATEMENTS.md:54) | W3-T03ACC:T03S.2 | `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:65` |
| record clause 3 (Theory_work/Wave3/W3-T03ACC/sources/statement/W6-FIXREV2_STATEMENTS.md:55-57) | W3-T03ACC:T03S.3 | `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:66-69` |
| record clause 4 (Theory_work/Wave3/W3-T03ACC/sources/statement/W6-FIXREV2_STATEMENTS.md:58-60) | W3-T03ACC:T03S.4 | `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:70-73` |
| record clause 5 (Theory_work/Wave3/W3-T03ACC/sources/statement/W6-FIXREV2_STATEMENTS.md:61) | W3-T03ACC:T03S.5 | `Theory_work/Wave3/W3-T03ACC/STATEMENT.md:74-77` |

Coverage of SOP:TH128: **complete** (5 of 5).

## 3. The record's Scope paragraph (verbatim, `Theory_work/Wave3/W3-T03ACC/sources/statement/W6-FIXREV2_STATEMENTS.md:63-81`; it accompanies T03♯ and is not part of the claim)

**Scope (must accompany the theorem).**
- This is posterior / global-HPM theory. It says nothing about the reported HPM Ŝ (discovery by the sampler).
- Prop. E3 (S03, PROVED): for this route — a Markov numerator over an S₀-denominator with the exact-tail cutoff — the
  cutoff cannot be s₀ + O(s₀ log n/log p). It is a barrier for this proof route only, not a lower bound for the posterior.
- Prop. D (S03, COUNTEREXAMPLE): under G and R alone (duplicate columns), Π(|S| > m | y) ≥ 2^{−(m+4)}e^{−m(m−1)/(4(p−m))}
  on an event of probability → 1, so some growth m_n ≳ ½ log₂ n is needed in general. It violates size-2 SE and does not
  contradict T03♯ (under T03♯, Π(|S| > s₀ | y) ≤ 1 − π(S₀) = O_P(r_n), V03 Prop. D′).
- **Finite-n disclosure (corrected; replaces S03's "≈ 1.2·10⁵").** With s₀ = 14, p = round(n^A), 1/g₀ → 0 (most
  favourable) and exact m♯_n, the proof as written needs δ_n ≤ ½ (first n = 115,150 / 130,328 for A = log 500/log 200 /
  log 1000/log 200), the geometric-series condition q_n ≤ ½ (first n = **2,116,048 / 2,457,025**), and, only to fix the
  displayed constant c_q, e^{2ε_n} ≤ 4 (first n = 25,571,897 / 29,755,302). At S03's n = 130,328, q_n ≈ 5.53·10²² (A = 1.17)
  and 7.86·10²⁸ (A = 1.30). These are checks of named conditions, **not a universal n₀**: other thresholds involve the signal,
  variance and eigenvalue constants and the BM sequence. At (n, p) = (200, 500) and (200, 1000), m♯_n = K = 100 (the cap
  binds; uncapped m♯_n would be 146 and 168, locked m_n = 201 and 215); the cap removes the dimension-tail term there but
  does not verify SE_λ, SE_w or BM, and the O_P rate is not numerically informative.
  Replacement sentence for the disclosure: "…and the proof's own deterministic thresholds (as written) hold only from
  n ≈ 2×10⁶ (p = n^{1.17}) to 2.5×10⁶ (p = n^{1.30}); the O_P constants are unspecified."
  (Independent recomputation: `scripts/t03_thresholds.py`, `results/t03_thresholds.txt`; it agrees with V03 R1 and A-REV2 §3.5
  to the integer.)

## 4. Consumers
Edges into SOP:TH09/TH128 are discharged by edge type (card 12 item 1); the edge table and the status changes are in the task T record (registry events, reason `task T`). Other conditions stay.
