# MEET-THM · Format notes (for HQ, to reuse in later meetings)

Written by the chair, 2026-11-04.

**Format used:** four seats; a non-voting chair; three rounds plus Round 0; two check waves plus one inherited-proof check; an auditor after each synthesis.

**Seats:**
- A, B and D: Fable 5.1, on two Claude accounts.
- C: gpt-6-astra (Codex).

**Checkers:**
- PC1: gpt-6.1-sol, for the Claude seats.
- PC2: Opus 5.5, for the Codex seat.

**Support roles:** registrar and assembly clerk on Sonnet; side-by-side clerks on Haiku.

## What worked

1. **A mechanical R0 diff with a coverage script.** The registrar merged 24 + 72 + 44 (+15) + 17 items into 108 K-IDs, and a script confirmed that every source item landed somewhere. K-IDs then carried every round, check and synthesis without renumbering. Keep it.
2. **Cross-family statement-sanity checks, by cluster.** PC1 found 11 COUNTEREXAMPLEs in the Claude seats' Round 1 cards, and 9 more in their new Round 2 clauses. Every one had an explicit construction and a script. PC2 found none in Seat C in either wave (0 of 56, 0 of 29). Highlights:
   - the necessity propositions (all three refuted);
   - the stage-count sandwich order;
   - "exact/minimal" coded-grid wording;
   - the duplicate-PIP limit (2/3, not 1/2);
   - the Song–Liang covariance slip.

   Clustering the cards (20 clusters), so that shared cores were checked once, kept one Codex task per wave feasible.
3. **Moving the inherited-proof check forward.** HQ's ruling Q1(c) and every seat's rank-1 theorem depended on author-only proofs (O-WSTAB WS3/4/6d/7, N9). Running that cross-family check in parallel with Synthesis 1, instead of in wave 2, meant Q1(c) was settled before Round 2. Keep it: list the author-only results the top candidates rest on and check them as early as possible.
4. **Asking HQ early, with both readings carried.** Q1–Q4 went to HQ right after Round 1, and the meeting continued on both readings. The answers arrived before Round 2, so no round was lost. Q5 came from a check result, and was answered within the synthesis step.
5. **An auditor after every synthesis.** It caught real misrepresentations:
   - overstated agreement;
   - card-level placements reported as clause-level;
   - HQ conditions summarised too loosely;
   - family-specific scale claims written as universal;
   - missing disagreement rows.

   The rule that "PASS WITH CORRECTIONS lets the chair apply them without another audit" prevented loops.
6. **A reconciled-list proposal before the last round.** Synthesis 2 proposed a list, marked as a proposal. Round 3 then confirmed it unanimously on every main question: the 8th slot, the V/H merge, SL, the leakage placement and the Ĵ form. Only six minor placements needed a majority rule, with dissent recorded.
7. **Word caps and fixed tables.** Seat outputs stayed at 5–14k words. Verbatim extraction from session files, with a helper script, kept seat files exact and cost little chair context.

## What did not work, and fixes

1. **Synthesis 1 failed audit twice** (15 findings, then 6, then a pass with 4 corrections). The cause: the chair summarised agreement and placements by hand, from a clerk's side-by-side table.
   - *Fix:* generate the disagreement and placement tables mechanically from the side-by-side, verify every row against the seat files, and write the chair's prose only around those tables. Never write "all agree" without a per-seat cell.
2. **The clerks' side-by-side tables had placement errors** (e.g. K49, K85, K70). They took a card header as the placement, when the seat's §B/§C row said otherwise.
   - *Fix:* use a stronger clerk model for extraction that feeds a synthesis, or require the clerk to flag every header-versus-row conflict (it did so partly, with "≠").
3. **Line references drifted** because filed verdict files carry a provenance header (+2 lines).
   - *Fix:* put provenance in a separate `PROVENANCE.md` per evidence folder, and file the checker's text with no header, so that line numbers match the checker's own.
4. **New clauses in Round 2 brought new errors.** All the Round 2 COUNTEREXAMPLEs were in clauses added in Round 2 (necessity propositions, the jump corollary, run-card corollaries).
   - *Fix:* any clause added after a check wave gets the seat's own small exact-enumeration check, quoted in the answer, and is flagged "new since wave N" for the checker.
5. **IC3 exhibits at small p dispatch the exact branch.** Finite exhibits (n = 40–64, p = 8–16) recovered the groups but never ran SMC.
   - *Fix:* IC3 for a claim about the SMC path must exhibit a family on which the method actually dispatches SMC, with the method's own partition computed, not asserted.
6. **An HQ condition written for an integer quantity** ("stage count continuous in ε") needed a follow-up ruling (Q5).
   - *Fix:* when a binding condition is fixed, dry-run it on the quantity's type: integers, step functions, quantities only defined on success.
7. **Ground rule 6 against sampler moments.** Seats repeatedly made budgets conditional on M₂ = E[W²|𝒞], which is a sampler quantity.
   - *Fix:* state in the round-1 brief that budgets may depend only on (n, p) and on design-computable bounds (e.g. e^{D_*}), and give an example.

## Costs

- **Accounts:** all seats, checkers, the auditor, the registrar and the clerks ran on subscription accounts. No API credit was used. No account hit its limit.
- **Codex tasks:** 3 seat tasks, 4 checker tasks and 4 auditor tasks.
- **Compute:** no Owls jobs. All numerical checks were local Python, with ≤ 20 seeds and runs under 5 minutes.
