# gpt-6.2-sol quality log (owner, HQ 11-17)

One line per gpt-6.2-sol review. Verdict vs what we'd expect from the 6.1 family on four points:
**F** = real findings caught · **N** = false positives / nitpicks (BETTER = fewer) · **B** = fidelity to the brief (scope, format) · **S** = speed / cost.
Each point is BETTER / SAME / WORSE, plus one short reason. Alarm rule: two WORSE in a row on substance (F or N) → tell HQ at once.
Leads append their own lines (manager checks); the daily report gives the running tally.

| date | ticket | review type | F | N | B | S | reason |
|---|---|---|---|---|---|---|---|
| 2026-11-17 | SOL62 A/B case1 (W3-MISR-R L1) | statement lock, replay vs 6.1 same inputs | BETTER | SAME | BETTER | WORSE | both caught KL + 3/3; 6.2 +1 verified +2 plausible, verdict = stored; 0 false each; ≈5 vs ≈2–3 min |
| 2026-11-17 | SOL62 A/B case2 (W3-D2 R1) | council seat, replay vs 6.1 same inputs | SAME | WORSE | SAME | SAME | both caught lgamma F1 + "P=0" point; 6.2 false REJECT of Thm2X on a null-event caveat + 1 nit; 6.1 gave no decisions |
| 2026-11-17 | SOL62 A/B case3 (W3-MISR-R K2) | clean-control re-check, replay vs 6.1 same inputs | SAME | SAME | SAME | SAME | both exact (2 RESOLVED, 0 new, 2 VERIFIED); ≈2 vs ≈3 min |
| 2026-11-17 | W3-FAMC (R1) | line check (statement + assembly) | BETTER | BETTER | SAME | SAME | 11 points, all genuine (0 false, 0 nit); MAJOR §1R overclaim caught with a concrete case; S not timed |
| 2026-11-17 | W3-FAMC (R2) | diff round | BETTER | SAME | SAME | SAME | 5 points, all genuine; caught a MAJOR introduced by the R1 fix (group signs, θ=(1,−2)) |
| 2026-11-17 | W3-FAMC (R3) | council seat | BETTER | SAME | SAME | SAME | 4 F + 3 E, all genuine; per-claim REJECT on provenance/registry only (math PASS), warranted |
| 2026-11-17 | W3-FAMC (R4) | council diff check | BETTER | SAME | BETTER | SAME | 1 F genuine: ran the ingest converter and caught the `|x|` registry-block parse defect the Opus seat missed |
| 2026-11-17 | W3-FAMC (R5) | council confirmation | SAME | SAME | SAME | SAME | clean confirm, ran converter + verify, 0 findings (lead) |
| 2026-11-18 | pre-Lean Sol-1 (C1 audits) | final-text confirmation | SAME | SAME | SAME | — | ACCEPT ×2; 1 observation, agreed by the Fable |
| 2026-11-18 | pre-Lean Sol-2 (READER R4/R5) | final-text confirmation | BETTER | SAME | SAME | — | caught a real card overclaim (6L↔9C, S2-1; consultant AGREE) + 2 status quotes |
| 2026-11-18 | pre-Lean Sol-3 (W3-D2 + D3) | final-text confirmation | SAME | SAME | SAME | — | ACCEPT ×5; 3 local stale-wording points |
| 2026-11-18 | pre-Lean Sol-4 (track V R4) | final-text confirmation | BETTER | SAME | SAME | — | 2 real dossier overreaches in the unreviewed B8 edit |
| 2026-11-18 | pre-Lean T4 Sol adversarial | blind adversarial | SAME | WORSE | SAME | — | 3 Lean points; 1 (p = 1) already ruled at W3-T03ACC (Fable OBJECT) |
| 2026-11-18 | pre-Lean T5 Sol adversarial | blind adversarial | SAME | SAME | SAME | — | corroborated Astra's 'equivalent' overclaim independently + 1 new Lean point |

| 2026-11-18 | pre-Lean Sol-5 (D5P landed, NA_DROP v1.2, MEAS-D MEASD7) | final-text confirmation | BETTER | SAME | SAME | — | caught LIST-CODE (v) 'exact-branch run' vs status exact (resource_limit before enumeration), missed by earlier D5P rounds; independently re-found T6 F3 (b-1); MEAS-D PASS with 3 wording items; 0 false |
| 2026-11-18 | pre-Lean Sol-5b (D5Pa + NA_DROP v1.3 deltas) | delta read | BETTER | SAME | SAME | — | all 7 Sol-5 fixes verified; caught b′-1, an overreach the Opus R2 seat's C-1 sentence had introduced (tail allocation vs (D)), = T6-1; 2 wording points, 0 false |
## Running tally
F: BETTER 9 / SAME 7 / WORSE 0 · N: 1/13/2 · B: 2/14/0 · S: 0/7/1 (16 gpt-6.2-sol reviews: 3 A/B + 5 W3-FAMC + 8 pre-Lean; pre-Lean S not timed). The pre-Lean Astra (gpt-6.2-astra) lines are in PRE_LEAN_PASS/SOL62_LINES.md. Alarm rule (two WORSE in a row on F or N): not triggered.
