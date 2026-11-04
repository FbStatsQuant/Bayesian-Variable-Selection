# MEET-THM · Check wave 2 brief: revised statements (identical for both proof checkers)

Chair, 2026-11-04. You are **Proof checker {PC}** of MEET-THM, the meeting that fixes paper 1's theorem list.

Working directory: `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/theory-MEET-THM`. Run `git fetch origin`.

**Your seats:** {ASSIGNMENT}. The cross-family rule applies: Claude seats are checked by Codex and the Codex seat by Claude.

## Read
- Your seats' Round 2 answers `theory_campaign/MEET-THM/R2_{X}.md`, all sections.
- Their Round 1 answers `R1_{X}.md`, for "unchanged from R1" references.
- Wave 1 verdicts: `evidence/W1_PC1/VERDICTS.md` (Seats A, B, D) and `evidence/W1_PC2/VERDICTS.md` (Seat C).
- The inherited-proof check `evidence/CHK_INHERITED/REPORT.md` (OWS-WS3/4/6d/7 and N9).
- `SYNTH_R1.md` §0.1: HQ's rulings as the meeting applies them. §3 lists the required repairs.
- `evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`.
- The method: `git show origin/theory/MEET-v31:theory_campaign/MEET-v31/METHOD_v3.1_FINAL.md` (with `AMENDMENT_HQ_01.md`). Code: `Scripts/SMC_BVS/core/`.

## What to check (in this order)

1. **The §5.3 package (§R3) of each seat, deepest look.** For each of parts (a), (b), (c), the necessity proposition if one is given, and the IC3 exhibit, give three verdicts:
   - **True as written?** One of: TRUE-AS-WRITTEN (say how you searched) / COUNTEREXAMPLE (construction + script) / NEEDS-HYPOTHESIS / AMBIGUOUS.
   - **Non-vacuous?** One of: DESIGN-VERIFIED / DESIGN-ASSERTED / DESIGN-FAILS. Verify that **the method's own partition** recovers the blocks in the exhibit, and that ε > 0.
   - **Route plausible?** One of: PLAUSIBLE / GAP / IMPLAUSIBLE.

   Also:
   - Reproduce every local script the seat quotes.
   - Check the stated ε-scale against your own computation.
   - Check that (c) uses the inherited check's amendments (bounded-block setting for the TV clause).
   - Check that HQ's conditions for (a) and (b) are met: constants, the σ²-coupling term, stage count, continuity in ε, and a correlated family with ε > 0.
2. **Every main-list card** (each seat's §R6 item 11 ranked main list, with its §R2 statement):
   - **Repairs:** was every wave-1 adverse verdict on that card (wave-1 file, and SYNTH_R1 §3) actually repaired? Answer per repair: REPAIRED / NOT REPAIRED / REPAIRED DIFFERENTLY (then judge the new wording).
   - **New or changed clauses:** the three verdicts as in item 1.
3. **§R4 masked-regime accuracy statement:** true as written, and non-vacuous on a **masked** family, exhibited?
4. **§R5 run-card definitions** (Ĵ, the leakage proxy):
   - Is each computed only from existing run quantities, with no random numbers and no feedback?
   - Is the theorem stated about each true as written?
5. **Supplement cards:** only those whose statement changed in Round 2. Repairs and new clauses, briefly.
6. **Growth rates** (§R6 item 7): is each rate an explicit function of (n, p) and of design-computable quantities (ground rule 6)? Does the theorem hold with it?

Flags, as in wave 1:
- (a) reliance on index-§4 known-false claims;
- (b) any status stronger than the registry's (copy verbatim, with qualifiers);
- (c) any hypothesis that is not a model/design condition;
- (d) a variant presented as v3.1.

## Rules
- **Never upgrade.** TRUE-AS-WRITTEN means no counterexample was found. Do not re-check results with a filed cross-family check: cite the wave-1 row or the CHK_INHERITED item.
- **Scripts:** Python 3, fixed seeds, ≤ 20 seeds, each under about 5 minutes, local only. Put them under `theory_campaign/MEET-THM/evidence/W2_PC{PC}/scripts/`.
- **Verdict file:** write it progressively to `theory_campaign/MEET-THM/evidence/W2_PC{PC}/VERDICTS.md`. Do not edit any other file; do not commit or push.
- **Output format:**
  - At the top, a summary: counts per verdict, then every COUNTEREXAMPLE / NEEDS-HYPOTHESIS / DESIGN-FAILS / IMPLAUSIBLE / NOT REPAIRED, one line each.
  - Then one table per seat per item: `card · clause | claim (≤ 25 words) | true | non-vacuous | route | repair status | flags | evidence`. ≤ 60 words per cell.
- **Your final message** is the full verdict file content.
