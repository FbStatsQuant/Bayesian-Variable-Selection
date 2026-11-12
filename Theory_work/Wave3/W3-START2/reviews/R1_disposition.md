# R1 disposition (lead) — council round R1

Manifest 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f (STATEMENT v1.4.1, `lemmas/P1`–`P4`, `REPORT.md`,
`numerics/`, `citecheck.py`, external inputs).

| seat | model, provider, effort | score | gates | review file |
|---|---|---|---|---|
| sol | gpt-6.1-sol, Codex, reasoningEffort high | 9.1 | PASS (G1–G6) | `reviews/R1_council_sol.md` |
| opus | Claude Opus 5.5, Claude Personal, effort high | 9.1 | PASS (G1–G6) | `reviews/R1_council_opus.md` |

`manifest.py bind`: `bind: OK, 2 review(s) give a PASS verdict (>= 8.0)`; council cell
`R1; MANIFEST 29e07311fc662cb546de2ee5ea090828669c4bc1034e0d5323c0184d9708117f; sol=9.1 PASS(reviews/R1_council_sol.md); opus=9.1 PASS(reviews/R1_council_opus.md)`.
`manifest.py verify`: OK after the round. **The council passed in round 1.** Every claim of `REPORT.md` §3 was accepted
by both seats; neither seat raised a BLOCKING issue.

## Remarks (all NON-BLOCKING) and what is done with each

The frozen content is not edited (PROTOCOL rule 15: an edit after the round needs a new round). Each remark is
accepted as correct and recorded as an erratum for the next version in `CHECKPOINT_2.md` §3 (rows E1–E8).

| remark | seat | disposition |
|---|---|---|
| `REPORT.md:23`: "exact order for bounded p" lacks the conditions η′ = 0, κ_V > ½ | sol 1 | erratum E1; the statement (`STATEMENT.md:115-117`) carries the conditions |
| `REPORT.md:89`: sharpness row — leading term versus exact order of o₀ | sol 2, opus 7 | erratum E2 |
| `lemmas/P1_LEADING.md:16-17`: "BASE" twice | opus 1 | erratum E3 (introduced by the lead's own prefix repair before LC1; the citation resolves) |
| `STATEMENT.md:108`: "word for word" for clause (c) | opus 2 | erratum E4 |
| `STATEMENT.md:205-206`: citation of BASE `CHECKPOINT_3.md:241`, outside the frozen content | opus 3 | erratum E5; the status it supports is also in `BRIEF.md:3-4`, and acceptance is conditional on the base in any case |
| `REPORT.md:27-28`: informal wording of the (N2⁺) threshold | opus 4 | erratum E6 |
| `STATEMENT.md:82`, `lemmas/P1_LEADING.md:38`: "(E)" in a fixed-n lemma | opus 5 | erratum E7; the proof uses only the inequalities of (E) at n, as the seat verified |
| dependency list should name the reused base proof steps | opus 6 | applied where it can be without touching frozen content: the registry blocks of `CHECKPOINT_2.md` §6 carry `@proof:<step>` edges |

No statement, hypothesis, constant or proof step is affected by any remark.
