# MEET-THM · Check wave 1 brief: statement sanity (identical for both proof checkers)

Chair, 2026-11-04. You are **Proof checker {PC}** of MEET-THM, the meeting that fixes the theorem list of paper 1 of the SMC-BVS project. Four seats wrote Round 1 theorem cards. Your job is **statement sanity** for the cards assigned to you below, not full proofs.

Working directory: `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/theory-MEET-THM`. Run `git fetch origin`; read other branches with `git show origin/<branch>:<path>`.

**Your cards:** {ASSIGNMENT}. (Cross-family rule: Claude-written cards are checked by a Codex model and Codex-written cards by a Claude model.)

## Read
- The seat files `theory_campaign/MEET-THM/R1_{A,B,C,D}.md`, §D (cards), §E (proposal §5.3), §F (proposal §5.4). Only your seats' cards are yours; read the others only to recognise a shared core.
- The method (fixed): `git show origin/theory/MEET-v31:theory_campaign/MEET-v31/AMENDMENT_HQ_01.md`, `…/METHOD_v3.1_FINAL.md`; base `Docs/Methodology/METHODOLOGY_v3.md`; code under `Scripts/SMC_BVS/core/` if a statement depends on what the code does.
- What exists: `origin/theory/MEET-THM-REG:theory_campaign/MEET-THM/evidence/REGISTRY_INDEX.md` (statuses, check history, **§4 known-false list**); `theory_campaign/MEET-THM/R0_DIFF.md` (K-IDs; §3 known-false hits).
- `theory_campaign/MEET-THM/DOSSIER.md` §4 (inclusion criteria IC1–IC7), §5 (the card).

## For every card, and every clause of it that makes a mathematical claim, give three verdicts

1. **True as written?** `TRUE-AS-WRITTEN (no counterexample found: say how you searched)` / `COUNTEREXAMPLE (explicit construction + script)` / `NEEDS-HYPOTHESIS (name the missing one and show why)` / `AMBIGUOUS (the readings, and which is true)`. Search for counterexamples on small cases: exact enumeration at p ≤ 12, small n, the method's actual rules (coded grid, LS0, Ẑ-weighted pooling) where the statement is about the shipped method.
2. **Non-vacuous?** `DESIGN-VERIFIED (you checked a concrete design satisfies every hypothesis; for a correlation theorem the design is genuinely correlated)` / `DESIGN-ASSERTED (the card names one but you could not verify it)` / `DESIGN-FAILS (it violates hypothesis X)` / `NONE-GIVEN`.
3. **Route plausible?** `PLAUSIBLE (the key lemma is right and the steps fit)` / `GAP (name the step)` / `IMPLAUSIBLE (why)`.

Also flag: (a) any clause that restates or relies on an index-§4 known-false claim (e.g. C3-PGD, CEX-localmax(A2), VPGD-PropG, OPW2-cex, FD-NM, SHARE-M(b), general LH locking per A-REV7) without addressing the refutation; (b) any status word stronger than the registry's (copy the registry status verbatim); (c) any hypothesis that is a condition on the study rather than on the model and design (ground rule 6); (d) any statement about "v3.1" that actually holds only for a variant (v3 without LS0, an ideal grid, equal-weight pooling).

**Never upgrade.** Your verdicts are about statement sanity; a TRUE-AS-WRITTEN is not a proof. A seat's own argument stays "PROVED (by this seat, unchecked)" unless you check it line by line, and then you say "argument checked line by line by PC{PC}: no error found", nothing stronger.

**Cards on proposal §5.3 (the seats' §E) get priority and a deeper look:** reproduce any local script the seat ran (its text is in the seat file), and test the statement on at least one genuinely correlated design of your own (weak, non-zero cross-block correlation) with the method's coded grid where feasible.

## Work rules
- Shared cores: many cards across seats state the same result (clusters below). Check a shared core once, then each card's differing clauses. Do not re-derive a result that has a filed cross-family check in the index; cite it.
- Scripts: Python 3 (`pip install numpy scipy sympy mpmath` if needed), fixed seeds, ≤ 20 seeds, each under ~5 minutes, local only (no Owls, no cluster jobs). Put them under `theory_campaign/MEET-THM/evidence/W1_PC{PC}/scripts/`, and write your verdict file progressively to `theory_campaign/MEET-THM/evidence/W1_PC{PC}/VERDICTS.md` (so nothing is lost if the session ends). Do not edit any other file; do not commit or push (the chair does).
- Order: main-list clusters first (1–16 below), then the rest.
- Output: one table per cluster: `card · clause | claim (≤ 25 words) | true as written | non-vacuous | route | flags | evidence (script / construction / line)`. ≤ 60 words per cell. At the top, a summary table: counts per verdict, and every COUNTEREXAMPLE / NEEDS-HYPOTHESIS / DESIGN-FAILS / IMPLAUSIBLE in one line each.
- Your **final message** is the full verdict file content (the chair files it verbatim).

## Clusters (card IDs per seat; A = R1_A, B = R1_B, C = R1_C, D = R1_D)

| # | Cluster | A | B | C | D |
|---|---|---|---|---|---|
| 1 | Validity, general-h identity (N1, N9) | C2 | D1 | — | M1 |
| 2 | Theorem H (bounded functionals, finite R) | C5 | D2 | D1 | M2 |
| 3 | Output events, Z𝒯, certificate card | C3, C7 | D3 | D5, D12 | M3 |
| 4 | Weight stability §5.3 (**priority**) | C9 (§E) | D6 (§E) | D14 (§E) | M10 (§E) |
| 5 | The start (Theorem 2) | C8 | D4 | D2 | M6 |
| 6 | Reported-HPM consistency, LS0, Theorem A | C18 | D8 | D4 | M5 |
| 7 | Composition at every n | C17 | D8 (part) | D4 (part) | M4 |
| 8 | SEP + Lemma KL | C10 | D5 | D3 | M7 |
| 9 | Stage laws, restricted-ESS geometry | C11 | D7, D19 | D7, D13 | M9, S10 |
| 10 | Theorem SL (vs split-and-merge) | C14 | D9 | — | M8 |
| 11 | Theorem CD (thesis) | C13 | D10 | — | M11 |
| 12 | Target consistency; finite-n | C15 | D13, D20 | D8 | M12 |
| 13 | Work, depth, width (island level) | C12 | D11 | D6 | M13 |
| 14 | Pooling rules, equal-weight PIP, R_eff | C4, S2 | D14 | — | S5, S7 |
| 15 | Evidence Ẑ: variance, masked tails, bounds | C6 | D12 | — | S6 |
| 16 | Approximation error §5.4: TV, KL, coverage | S4 (§F) | (§F) | D15-TV, D15-KL, D15-CI (§F) | S8 (§F) |
| 17 | Repair, local search, certificates, numerics, tie DP | C16 | D18 | D9 | S9 |
| 18 | Limitations | S3 | D15 | — | S11 |
| 19 | Kernel, blocks, start machinery | S1, S6 | D16, D21 | D10 | S2, S4 |
| 20 | Target lemmas, decision rules, fixed p | C1, S5 | D17 | D11 | S1, S3, S12 |
