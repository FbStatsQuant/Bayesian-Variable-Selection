# C1 disposition (lead) — council round R1 and diff check RC6

Manifest of the round: 00bbeab89433b2f65dbfb8eefddf5e1a88dcc5460cabe79cd7adc3c8d6515d4a. `manifest.py verify` OK
after the round and before any edit; `manifest.py bind MANIFEST_R1.txt C_R1_council_astra.md C_R1_council_opus.md`:
"bind: OK, 2 review(s) give a PASS verdict (>= 8.0)"; council cell
`R1; MANIFEST 00bbeab8…; astra=9.5 PASS(reviews/C_R1_council_astra.md); opus=8.8 PASS(reviews/C_R1_council_opus.md)`.
Both seats were blind first reads. The seven texts edited afterwards are kept as the council read them in
`as_reviewed_by_R1/` — restoring them restores the exact council tree.

## Result: **COUNCIL ROUND R1 PASSED**
| seat | model | G1–G6 | score | REQUIRED findings |
|---|---|---|---|---|
| astra | Codex gpt-6-astra, high | all PASS | **9.5** | none |
| opus | Claude Opus 5.5, high, Claude Work | all PASS | **8.8** | none |
Opus's deductions: −0.4 registry pointers (F1); −0.3 the headline still needs (W), whose primitive forms only partly
reach strongly correlated polynomial groups; −0.2 cross-record inconsistencies; −0.2 wording and NITs; −0.1 no
Form F example with p ≫ n at polynomial |Q|. Both seats: v1.4 is fit to replace the parent's Theorem 3; the most
valuable missing strengthening is O1 (path-level control, removing (W)).

## RC6 — `RC6_diffcheck_sol.md` (the seven sweep items, 24 hunks)
All RESOLVED, including the energy-constant rescaling remark [SW1-1];
"ATTESTATION: editorial/record only — the package stands as swept in round SW1"; citecheck 92 citations, 0 MISS.

## Non-required findings and what was done (markers [C1-F#], [C1-A2])
| # | seat | class | finding | action |
|---|---|---|---|---|
| F1 / A1 | both | MINOR | `status_source` line pointers in REPORT's registry block four lines off | recomputed from the §3 rows (and checked by the script that wrote them) |
| F2 | opus | MINOR | REPORT §4: a text line split the table | moved below the table |
| F3 | opus | MINOR | `better` gate cited BT1, not the review of the final statement | now `reviews/BT2_disposition.md` |
| F4 | opus | NIT | ASSUMPTION_MAP: "ladder (3.3)" does not exist | "(2.2)–(2.3)" |
| F5 | opus | NIT | "median–mean" in STATEMENT (P9) row and ASSUMPTION_MAP disagrees with the proof | "a probability-≥ ½ event plus lower-tail concentration about the mean" |
| F6 | opus | NIT | L2, L3 headers cite STATEMENT v1.3 | "written for v1.3; unchanged for Form F in v1.4" |
| F7 | opus | MINOR | SHARPNESS/REPORT: "b enters at exactly one line" ignores (S2) and P9a in Form R | reworded; registry evidence field extended |
| F10 | opus | NIT | Lemma-BC cited without version in STATEMENT | "@1.0.0" |
| A2 | astra | NIT | RESULTS opens with the historical 207-run state | a "final counts" note added at the top |
| F8 | opus | NIT | L4 reuses the symbol ϑ_n of the toolkit for √n·ζ_n | **not applied** (would touch proof text after the council); listed for revision v1.5 |
| F9 | opus | NIT | two "the right side is positive" phrasings (L1, L4) should name the whole score difference | **not applied**, same reason; v1.5 |
| F11 | opus | NIT | (C1)'s parenthetical on the old cap `ell_n` is not derived in the ticket | **not applied** (it is inside a claim; changing it is a statement change); v1.5 |
| F12 | opus | observation | Form F examples at polynomial \|Q\| all have p < n (exact-Gram designs) | recorded; p ≫ n examples are Form R |

Also written after the round: the council result in REPORT §1, §4 and in the registry block (`correct` gate and
`council` line of RM2-F and RM2-R). No hypothesis, claim, lemma statement, proof step, constant or code pin
changes. Per PROTOCOL rule 15 the diff since the council freeze is attested by an independent Sol reviewer (PC1).
