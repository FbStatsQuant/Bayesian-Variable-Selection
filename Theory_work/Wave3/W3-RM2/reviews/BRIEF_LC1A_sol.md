# BRIEF — lemma check LC1-A (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read of L0 and L1

You are an independent line-by-line checker for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable
selection; this ticket proves that the coded method reports the true model when the set Q of "leaking" columns has
polynomial size n^b). The proofs were written by a Claude model; you are the cross-family check. This file is your
whole brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change
no git state. Write exactly one file:** `Theory_work/Wave3/W3-RM2/reviews/LC1A_L0L1_check_sol.md`. Do not edit any
other file (if you run code, write your scratch files outside the worktree). Do not start subagents. Use no effort
setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_LC1.txt`; its first line is
`MANIFEST 0caea883fcf38765f1ebe5b264e8300622f80f6e444a49855ad91725e06f1558`. **Quote this digest line verbatim at the top of your review.**

## Files you may read
Only files listed in the manifest:
* the objects under review: `Theory_work/Wave3/W3-RM2/lemmas/L0_toolkit_b.md` (Lemma Toolkit-b) and
  `Theory_work/Wave3/W3-RM2/lemmas/L1_sandF_b.md` (Lemma SAND-F^b, Lemma B1);
* `Theory_work/Wave3/W3-RM2/STATEMENT.md` (v1.3: what the lemmas must deliver — bridges (P0), (P1), and the
  [SAND(Q)] part of claim (C1));
* `Theory_work/Wave3/W3-RM2/numerics/lemma_checks.R`, `lemma_checks_out.txt`, `RESULTS.md` §5 (falsification
  numerics, blocks K1, K2 concern these lemmas);
* the external inputs of `Theory_work/Wave3/W3-RM2/reviews/INPUTS.txt` — in particular the templates the proofs
  follow: `Theory_work/Wave1/W1-GEN/lemmas/L1_lemmaE.md`, `Theory_work/Wave1C/C-GROW/lemmas/L0_toolkit.md`,
  `Theory_work/Wave1C/C-GROW/lemmas/L3_sandwich.md`, `Theory_work/Wave3/W3-RM/lemmas/L1b_rss.md`,
  `Theory_work/Wave3/W3-RM/lemmas/L1_fixed.md`, and the pinned code if you need the prior or the score.
Do not read `lemmas/L2_width.md`, `lemmas/L3_assemblyF.md`, anything in `reviews/` other than the manifest and
INPUTS.txt, any `LOG.md` or `CHECKPOINT*.md`.

## Task
Check every step of both files as a referee who wants to find the error. For each numbered claim ((T1)–(T5) and the
two families of L0; Lemma B1, Facts 1–2, Step 1, Step 2(a), Step 2(b) and the remarks of L1):
1. Is the statement well-posed and does it deliver what STATEMENT.md's (P0) / (P1) say (hypotheses not stronger,
   conclusion not weaker)? Is L0 really self-contained (no conclusion of a source used as an input)?
2. Is each inequality correct **with its constants** — in particular: the three probability bounds of (T1) with
   t_n, h_n defined from the actual cardinalities; the constants 1.01/1.03/0.52 in (E2)/(E4); n₀'s list; (T5)(a)–(c);
   the τ-form floor (Fact 2) and the factor (1 − ζ_n); display (2.2) (division by d/2); the choice of ε₁ and the
   exponent ξ in the ladder; the Markov step and the geometric sum; the feasibility cases in Step 2(a); the final
   margin [β(η, A) − b] log n − o(log n) in Step 2(b), including every term hidden in the o(log n)?
3. Quantifiers: "for every maximiser"; events that must not depend on the maximiser; what n₀ depends on; the role
   of (L-feas) and of Q = [p].
4. Hidden uses of the size of Q: does anything besides Step 2(b) need |Q| small? Does anything need b < ½ beyond
   b < β(η, A)?
5. Try to falsify: boundary cases (η = 0; s₀ ≥ 17 so that truths fill a block; a block of size 1; k̃ = K; p < n;
   p ≫ n; |Q| = 1 + s₀), sign errors, a constant that should be 16 or 32, the direction of each monotonicity.
   You may run small numerical checks of your own (outside the worktree) and report them.

## Output format (in your one file)
```
MANIFEST <digest>
Verdict per lemma: Toolkit-b …; SAND-F^b …; B1 … — each VERIFIED | VERIFIED-WITH-AMENDMENTS | WRONG
Findings: numbered; each FATAL (the lemma is false or the proof has a gap that needs a new idea) / MAJOR (a step is
  wrong or missing but repairable; give the repair) / MINOR / NIT; with file:line and the exact correction.
Checks performed: step by step, what you verified and how.
Not checked: list.
```
End your reply with the verdict line(s) and the path of your file.
