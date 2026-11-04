# MEET-THM · Round 2 brief (identical for Seats A, B, C, D)

Chair (non-voting), 2026-11-04. The agenda is frozen at dispatch.

You are **Seat {SEAT}** of MEET-THM (the paper-1 theorem list). Round 2 is the **rebuttal and final-statement round**. You now see everything: the other seats' Round 1 answers, both check verdicts, HQ's rulings and the chair's synthesis.

You are **read-only**: do not edit, commit or push. Your **final message is your full answer**, which the chair files verbatim as `R2_{SEAT}.md`. Small local checks are allowed: Python, under a minute each, ≤ 20 seeds, in a scratch directory outside the repository. Quote the script and its output compactly.

Working directory: `/home/fb31/.t3/worktrees/Bayesian-Variable-Selection/theory-MEET-THM`. Run `git fetch origin`.

## Read
1. `theory_campaign/MEET-THM/SYNTH_R1.md`: the v2 (corrected after the auditor's report `SYNTH_R1_AUDIT.md`; re-audit `SYNTH_R1_REAUDIT.md`): HQ's rulings as applied (§0.1), the §5.3 facts (§0.4), the disagreement table D1–D18 (§2), the repairs required by the checks (§3), the agenda (§4).
2. `theory_campaign/MEET-THM/evidence/2026-11-04_HQ_RULINGS_Q1-Q4.md`, HQ's binding rulings on §5.3, §5.4 and the run card.
3. The check verdicts: `evidence/W1_PC1/VERDICTS.md` (Seats A, B, D) and `evidence/W1_PC2/VERDICTS.md` (Seat C). Also `evidence/CHK_INHERITED/REPORT.md` if present (cross-family check of OWS-WS3/4/6d/7 and N9).
4. All four Round 1 answers: `R1_A.md`–`R1_D.md`. Your own is `R1_{SEAT}.md`.
5. As needed: `DOSSIER.md`, `R0_DIFF.md`, the registrar's index, `ROUND1_BRIEF.md` (the reading list there still applies).

## Rules (unchanged from Round 1, plus three)
- The method is fixed, except that growth rates of (R, L, ℓ, N) may be set as explicit functions of (n, p). Depth is claimed at the island level only. Binding goals escalate; they are never silently dropped. Hypotheses are model/design conditions (ground rule 6).
- Status words are never upgraded. Your own argument is at most "PROVED (by this seat, unchecked)". Copy registry statuses **with their qualifiers** (AUTHOR-ONLY, SAME-FAMILY-ONLY, "external review queued").
- **Do not re-derive** a result that has a filed check. Cite the verdict row (e.g. "PC2 §0 item 1").
- **A checker's COUNTEREXAMPLE stands** unless you show the checker misread the statement (quote both). Otherwise repair the clause or concede it.
- **An OPEN conjecture is not a list theorem.** It goes to future work, or appears only inside a fallback statement that is itself provable.

## Answer in these sections. Tables only; ≤ 80 words per rebuttal row; ≤ 250 words of free text per card; whole answer ≤ 12,000 words

**§R1 Rebuttal**, one row per disagreement D1–D18 of SYNTH_R1 §2 (for D17 and D18, one row per K-ID or group): `row | concede / hold / amend | your position now | evidence that would change it`.

**§R2 Final statements.** One card for every theorem you keep (main or supplement). Fields:
- ID (K-IDs);
- final statement with every hypothesis named;
- the §3 repairs applied (cite the verdict row), or "none needed";
- status verbatim, with qualifiers;
- placement (main / supplement);
- proof route and key lemma;
- Lean core;
- fallback + stop rule;
- IC3 design: if it changed, explain why the new one satisfies every hypothesis, including the method's own partition where the theorem is about blocks.

For cards unchanged in substance, give the final statement and write "unchanged from R1 §D <card>" for the rest.

**§R3 The §5.3 package** (HQ Q1). One card with three named parts:
- **(a) Discrepancy half:** the π₀-vs-π divergence is controlled by the cross-block terms plus the explicit σ²-coupling term.
- **(b) Bridge-form stability:** per-stage χ²/weights, stage count and constants, continuous in ε around the block-orthogonal baseline.
- **(c) Refutation of the one-shot form:** OWS-WS6(d), WS7. It ships only if the cross-family check passes.

Also give:
- the honest ε-scale of (a) and (b) (see SYNTH_R1 §0 item 4: perturbative, ε ≲ n^{−1/2}/p);
- whether a matching **necessity** proposition is provable (at fixed ε, osc d ≳ √n·ε, or weights unbounded), with its route;
- one IC3 exhibit on which **the method's own partition** recovers the blocks and every hypothesis holds. Give the parameters, and say where it was checked.

**§R4 Masked-regime accuracy statement** (HQ Q3 requirement). Name the one statement paper 1 proves in the masked regime (K-ID and card), and why it is non-vacuous on a masked family.

**§R5 Run-card definitions** (HQ Q4). Give exact definitions, computed only from the run's existing quantities, with no random numbers and no feedback, of:
- (i) the Jeffreys estimate Ĵ;
- (ii) the cross-block leakage proxy.

For each give the estimator, its numerical label, and the theorem that is stated about it.

**§R6 Agenda items 6, 7, 9, 10, 11 and item 1 closure.**
- **6:** the thesis theorem's exact formal scope: fixed data vs asymptotic; favourable vs masked; the sentence that is not a corollary of other cards (or "remark only").
- **7:** for each theorem that needs R, L, ℓ or N to grow, the explicit rate as a function of (n, p), and the method edit to record. Settle D11, R_n in Theorem H.
- **9:** scope. p ≤ n^A in; any exponential-p statement → in reach, or FUTURE_WORK with a reason.
- **10:** novelty risks. Each overlap (e.g. Hou–Wang–Atchadé; YWJ/ZYVR; Del Moral; Chatterjee–Diaconis), with the citation you checked and the theorem it touches.
- **11:** your final **main list of ≤ 8** (ranked) and the supplement list.
- **Item 1:** your final list of THM-INV §1 cells marked "nothing provable", each with a reason.

**§R7 Questions for HQ.** Only decisions outside the meeting's authority. "None" is valid.
