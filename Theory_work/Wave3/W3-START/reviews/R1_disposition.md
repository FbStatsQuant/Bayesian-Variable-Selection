# Council round R1 — disposition (lead, 2026-11-11)

Frozen content: `reviews/MANIFEST_R1.txt`, digest `0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97`
(57 files). Blind first reads (briefs `BRIEF_R1_sol.md`, `BRIEF_R1_opus.md`); six gates G1–G6.

| seat | model, provider, effort | score | gates | file |
|---|---|---|---|---|
| sol | Codex gpt-6.1-sol, codex, reasoningEffort high | 9.1 | PASS (G1–G6) | `reviews/R1_council_sol.md` |
| opus | Claude Opus 5.5, Claude Work, effort high | 8.8 | PASS (G1–G6) | `reviews/R1_council_opus.md` |

**Council PASSED in round 1**: both seats ≥ 8.0, all six gates PASS, same manifest. `manifest.py bind` (current main's
tool): "bind: OK, 2 review(s) give a PASS verdict (>= 8.0)"; council cell:
`R1; MANIFEST 0a6daa2cabc89d3124a7ee133e69e593f8b65f605c05cedec19d2f537687de97; sol=9.1 PASS(reviews/R1_council_sol.md); opus=8.8 PASS(reviews/R1_council_opus.md)`.
`manifest.py verify` passes on the current tree. Every id of `REPORT.md` §3 is "accepted" by both seats (sol: NEC with
a non-blocking remark; opus: LEAK, F4, EX with non-blocking remarks).

## Non-blocking issues — NOT applied
The acceptance tool requires the frozen content to be unchanged after the passing round (LIFECYCLE §4.1 A4), so none
of the ten non-blocking issues is applied. Each is recorded here with the lead's reading, for a later version
(v1.3.4) if HQ orders one; applying them needs a new council round.

| # | seat | issue | lead's reading |
|---|---|---|---|
| S1 / O3 | both | `ASSUMPTION_MAP.md` keeps its v1.2 body and corrects it in appended sections §3–§5 | correct; regenerate §1–§2 for the final statement and keep §3–§5 as history |
| S2 | sol | `numerics/RESULTS.md:94, :129`: phrases stronger than a finite simulation supports ("tracks the truth", "the mass converges") | correct; replace by finite-n observational wording |
| S3 | sol | `STATEMENT.md:316`: (N1) abbreviates the exact-order consequence without repeating κ_V > ½ | correct; add "and κ_V > ½" (the F2 clause and the proof state it) |
| O1 | opus | Setting F is said to equal C-GROW's setting "with s₀ ≥ 0 allowed", but it also allows any A > 0 where C-GROW has A ≥ 1 | correct; write "with s₀ ≥ 0 and any fixed A > 0 allowed". The proofs never use A ≥ 1 |
| O2 | opus | F4 and example F-2 are meaningful only for astronomically large n (tail budget below 1 only for log n > 256); said in the numerics report, not in the statement or `REPORT.md` | correct as a remark on presentation; the results are asymptotic by design. Add one scope sentence to F4 and to the F-2 entry |
| O4 | opus | the (B-L) row has e^{2κ_E+o(1)} while Lemma L3.3 displays e^{2κ_E+1} (its proof gives e^{2κ_E+ς_n}, ς_n → 0) | correct; state L3.3 with e^{2κ_E+ς_n} |
| O5 | opus | the code pin names `main` = fe9a066, and `main` has advanced; CORE is unchanged since 72785fe | correct; phrase the pin as "CORE tree as of 72785fe" |
| O6 | opus | summaries write the Gaussian-row rate without the factor (s₀ + 1) (absorbed by the constant) | optional: write "for some C" |
| O7 | opus | `citecheck.py` writes into the repository | add an output-path argument |

No finding of either seat concerns a proof step, a hypothesis or a constant of a claim.
