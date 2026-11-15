# BRIEF — statement-lock review SL1 (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole brief.
Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START` (all paths below are relative to it). **Change no git
state. Write exactly one file:** `Theory_work/Wave3/W3-START/reviews/SL1_statement_lock_sol.md`. Do not edit any other
file. Do not start subagents. Use no effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START/reviews/MANIFEST_SL1.txt`. Its first line is
`MANIFEST 53849ef3dc7dfbcd353bc880e2cf0f7604208f4818ab1fdf1b4a8a7e76e6fed1`. **Quote this digest line verbatim at the
top of your review.** You may run `python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START
Theory_work/Wave3/W3-START/reviews/MANIFEST_SL1.txt` and report its result.

## Files you may read
Only the files listed in the manifest: `Theory_work/Wave3/W3-START/STATEMENT.md` (the object under review),
`Theory_work/Wave3/W3-START/PLAN.md`, `Theory_work/Wave3/W3-START/BRIEF.md` (HQ's ticket brief), and the 23 external
inputs listed in `Theory_work/Wave3/W3-START/reviews/INPUTS.txt` (pinned code, wave documents, premise sources and
consumers). Do not read any other file in any `reviews/` folder, any `LOG.md`, or any `CHECKPOINT*.md`.

## What a statement-lock review is
Nothing in STATEMENT.md is proved yet. You decide whether the **target statement** is fit to be locked before proof
work starts. You are briefed to break it. Check, with file:line evidence:
1. **Well-posedness.** Every object, quantifier, constant and probability space is defined; no circular or ambiguous
   definition; each claim is a definite mathematical statement (what is random, what is fixed, which limit).
2. **Fidelity to the code.** "π₀" must be the start distribution exactly as the pinned code computes it (score, prior,
   cap K, partition, block tables, normaliser). Check each pin in STATEMENT §1 against the code lines.
3. **Fidelity to cited sources.** Every imported definition or status (C-GROW, W3-RM, W3-SAMP, C-MIS, W1-PXN, T22)
   is quoted correctly; consumed claims are ACTIVE in `Theory_work/INFRA/registry/claims.tsv` at the stated version
   with the stated status; nothing below PROVED-CHECKED is consumed silently (PROTOCOL rule 11).
4. **Design-agnostic form.** No design family or block appears in a hypothesis of a theorem (PROGRAM presentation
   rule); hypotheses are conditions on (X, θ*) (or (Σ_n, θ*)) only; interface properties are used as PROTOCOL item 5
   requires.
5. **Plausibility / quick falsification.** Try to refute each claim (S0)–(S6) by a small example, a limiting case
   (s₀ = 0, s₀ ≥ 16, p < n, p ≫ n, Q = S₀, Q = [p], all truths in one block, exact collinearity, K boundary), a
   dimensional or constant check, or an inconsistency between clauses. Check the deterministic claims (S0) by hand
   algebra where you can (prior ratios of w(k) = ½/C(2p − 1, k); the table ratio bound (n + 1)^{−1/2}; the bounds
   (J0)–(J3)). Say explicitly which claims you checked and how, and which you could not check.
6. **Consumers.** Does (S5) deliver exactly W3-SAMP's P-START and P-OVL as they are stated there?
7. **Honesty of scope.** Does §6 "Not claimed" and (S4)(N4) say clearly where the result fails (masked truths,
   strong-factor designs)? Is anything claimed that the plan cannot plausibly prove?

## Output format (in your one file)
```
MANIFEST <digest>            (verbatim first line of the manifest)
Verdict: LOCK | LOCK WITH CHANGES | DO NOT LOCK
Required changes: numbered; each with location (file:line), the problem, and the exact change you require.
Optional suggestions: numbered.
Checks performed: what you verified and how (algebra, code reading, counterexample attempts), per claim.
Not checked: list.
```
Classify each required change as CRITICAL (a claim is false or ill-defined), MAJOR (a hypothesis or scope must
change) or MINOR (wording, citation, missing definition). Be concrete; do not propose a different theorem (a separate
review does that). End your reply with the verdict line and the path of your file.
