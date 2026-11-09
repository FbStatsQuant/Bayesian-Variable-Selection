# Final council (updated Wave-2 protocol), round 1 — disposition

Seats:
- R19: gpt-6-astra (reasoningEffort high, codex). File: reviews/R19_council_astra.md. Score 9.2. G1–G6 all PASS. No REQUIRED items.
- R20: Claude Opus 5.5 (effort high, claude-personal). File: reviews/R20_council_opus.md. Score 8.9. G1–G6 all PASS. No REQUIRED items.

Both seats were independent: neither was shown the earlier council seats (brief reviews/COUNCIL_BRIEF_FINAL.md).

**Result: PASS in round 1.** Both seats are ≥ 8.0 with all six gates PASS in the same round, so Theorem FAC-CS-iid is
**PROVED-CHECKED**.

The recommended (non-blocking) items were applied after the pass. None changes a claim of STATEMENT v3.

## R19 items
- **R19-1 (MINOR).** REPORT §6, Ψ row: "breaks the rank-one structure" was imprecise. It is replaced by: the identity-plus-rank-one
  reference and the iid-coordinate argument do not cover block-local Ψ.
- **R19-2 (EDITORIAL).** REPORT §4 trail refreshed: all council rounds, models and scores are listed, and the sentence
  "Astra / Fable: not used" is removed.

## R20 items
- **R20-1 (MINOR, accepted; analytic and numeric check in reviews/R20_scratch/r20_addmargin_out.txt).** The ½ frontier has a
  third cause: beyond ½, the uniform-in-𝔫 form of (C2)(ii) is false. The adversarial 𝔫 is the 15 largest positive null ξ;
  re-adding one of them gains ≈ log p − ½ log n → +∞. Changes:
  - STATEMENT §5, first bullet: remark added ("no claim changed").
  - REPORT flag 4 and the §6 growth row: three causes listed (band; second-order resolvent term; uniform-in-𝔫 bulk
    addition margin). Going beyond ½ needs both a band decoupling and a replacement for the uniformity over 𝔫.
- **R20-2 (MINOR).** REPORT §1/§4 now list every council round: R08/R09; R13/R14; R19/R20, with seats, scores, gates and
  disposition files. The reviewer-family sentence is corrected.
- **R20-3 (EDITORIAL).** X4.5: "after m_{i_e} (≤ m₁ − 1) further moves (total exactly m₀(𝔫))".
- **R20-4 (EDITORIAL).** STATEMENT §7: the FAC-A status is now quoted in full, "PROVED-CHECKED (for the narrowed, flagged target
  STATEMENT.md v1.2)" (W2-FAC-A/REPORT.md:20). Only L5.1's de-randomisation pattern is used.
- **R20-5 (EDITORIAL).** X4.5 Entry: one sentence added, "B1 also holds at i = i* by the same wide-phase argument (N₊ ≥ m₁ − 1)".
