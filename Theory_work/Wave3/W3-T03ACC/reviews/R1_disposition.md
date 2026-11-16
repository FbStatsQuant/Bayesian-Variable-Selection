# Council R1 disposition (lead) — MANIFEST 9714aea441df09c3caedff6179232fd84cce9e6aa631050ddfeb9c1cec86b3c6

`ERRATA.md` is inside the frozen manifest, so v4 §5.9 forbids editing it now. E findings are therefore collected
here and appended to `ERRATA.md` in the one editorial batch after acceptance (v4 §5.3). They never block.

## Opus seat (`reviews/R1_council_opus.md`): T03S.1–.5 ACCEPT; G1–G6 PASS; score 9.4; findings E only
| # | finding (E) | disposition |
|---|---|---|
| O-E1 | den′ (`PROOF.md:91`) cites "the first two sentences" of [P1] lem:den "Assembling"; only half of the second sentence is used | accepted, editorial batch |
| O-E2 | STATEMENT §5 consumed-label list omits [P3] `eq:ratio`, `eq:supsum`, `eq:assemble`, the Step 1 paragraph, and the opening facts of §`sec:main` (all inside checked DEPS blocks) | accepted, editorial batch (record only; DEPS blocks already cover them) |
| O-E3 | "deterministic M_n" not listed among the §4 readings | accepted, editorial batch |
| O-E4 | DEPS bookkeeping: no row for `PROOF.md:9-17` (notation, R_m definition); STMT row ends at line 132 of 141 (changelog excluded on purpose); one `checked_by` cell carries a `#` annotation | accepted, editorial batch (add row PROOF notation; STMT range note) |
| O-E5 | agrees with ERRATA E1–E3 (p = 1 wording) | noted |
| O-E6 | REPORT "PROVED (W1-T03R …)" vs the NBH TH128 wording "PROVED (candidate) (W1-T03R)" | accepted, editorial: use "PROVED (candidate) (W1-T03R)" in the registry status at CP3 |

## Astra seat (`reviews/R1_council_astra.md`): T03S.1–.5 ACCEPT; G1–G6 PASS; score 9.5; findings E only
| # | finding (E) | disposition |
|---|---|---|
| A-E1 | `PROOF.md:9` p = 1 wording (= ERRATA E2) | already in ERRATA (E2) |
| A-E2 | `PROOF.md:16` negative-m sum notation (= ERRATA E3) | already in ERRATA (E3) |
| A-E3 | `STATEMENT.md:73`, `PROOF.md:168`: write "j ∈ S₀" in J_n^∞ (= ERRATA E1) | already in ERRATA (E1) |
| A-E4 | `TARGET.md:3` says v1.0 (reviewed statement is v1.1); `TARGET.md:12` points bounded energy to [P3] `lem:ongood`(b), its direct use is (a) | accepted, editorial batch |

## Outcome
Both seats on MANIFEST 9714aea4…: every claim ACCEPT, all gates PASS, scores 9.5 / 9.4 (≥ 8.0). No C, S or F finding
from either seat → no diff round (v4 §5.5). `manifest.py bind`: OK. Ten E items (O-E1–O-E6, A-E1–A-E4; three of them
duplicate ERRATA E1–E3) go to the one editorial batch.
