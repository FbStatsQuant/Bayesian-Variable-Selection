# BRIEF — statement-lock review SL1 (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent reviewer for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable selection by
sequential Monte Carlo; this ticket is about when the coded method **reports the true model** when the set of columns
that "leak" signal has polynomial size n^b). This file is your whole brief. Work only inside the worktree
`C:/Users/felip/BVS-wt/W3-RM2` (all paths below are relative to it). **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/SL1_statement_lock_sol.md`. Do not edit any other file. Do not start subagents. Use
no effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_SL1.txt`. Its first line is
`MANIFEST 1397b036a1eff57d1f6f281c196a9deee176d8da23bab07f86876e8e1e249066`. **Quote this digest line verbatim at the
top of your review.** You may run `python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2
Theory_work/Wave3/W3-RM2/reviews/MANIFEST_SL1.txt` (from the worktree root) and report its result.

## Files you may read
Only the files listed in the manifest: `Theory_work/Wave3/W3-RM2/STATEMENT.md` (the object under review),
`Theory_work/Wave3/W3-RM2/PLAN.md`, `Theory_work/Wave3/W3-RM2/BRIEF.md` (HQ's ticket brief), and the 31 external inputs
listed in `Theory_work/Wave3/W3-RM2/reviews/INPUTS.txt` (pinned code, wave documents, the parent result W3-RM, the
engines whose proofs will be re-run, the polynomial-decay precedent). Do not read any other file in any `reviews/`
folder, any `LOG.md`, any `CHECKPOINT*.md`, or anything under `C:/Users/felip/BVS-wt/W3-MEMO-SCR-RM`.

## What a statement-lock review is
Nothing in STATEMENT.md is proved yet. You decide whether the **target statement** is fit to be locked before proof
work starts. You are briefed to break it. Check, with file:line evidence:
1. **Well-posedness.** Every object, quantifier, constant and probability space is defined; no circular or ambiguous
   definition; each claim is a definite mathematical statement (what is random, what is fixed, which limit). In
   particular the lattice-width functionals 𝔴_n(δ), 𝔴⁺_n(δ) (§1), the set 𝔓, the levels a_{n,δ}(k) (is p/(k + 1) ≥ 1
   on 𝔓?), the order of the constants (η, b, δ₀, h, ρ), and conditions (W), (W-unif), (W-χ), (W-ref), (W-loc), (W-R),
   (D-R^b).
2. **Fidelity to the code.** The three code pins of §1 against `Scripts/SMC_BVS/core/cpp/v3_core.cpp` and
   `v3_engine.h` (neighbourhood of one LS0 scan, strict improvement, tie rule, cap).
3. **Fidelity to cited sources.** Every imported definition, line range and status (W3-RM, C-GROW, W2-LOC2, W2-APP,
   SOP:TH09, W1-GEN) is quoted correctly; consumed claims are ACTIVE in `Theory_work/INFRA/registry/claims.tsv` at the
   stated version with the stated status; nothing below PROVED-CHECKED is consumed silently (PROTOCOL rule 11).
   Does RM-0 (W3-RM `STATEMENT.md:160-176`, `lemmas/L0_core.md`) really have no size restriction on Q?
4. **Design-agnostic form.** No design family and no block of the method's partition appears in a hypothesis of
   (C1)–(C4) (PROGRAM presentation rule; the labelled block-relative variant is allowed as in W3-RM); hypotheses are
   conditions on (X, θ*) (or (Σ_n, θ*)) and the deterministic set Q; interface properties as PROTOCOL item 5.
5. **Plausibility / quick falsification.** Try to refute each claim by a small example, a limiting case, or a
   constant check. Suggested targets:
   * (C1): is b < β(η, A) what the junk-exclusion step of C-GROW L3 / RM Lemma B2τ gives when log k̃ ≤ b log n + O(1)?
     Does the size ladder of C-GROW L3 survive |Q| = n^b? Does anything else in the fixed-design sandwich use
     log|Q| = o(log n)?
   * (C3)(a): with the size-dependent level c_n(k), does the score conversion of C-GROW L2.2 go through (prior ratio
     log[(k + 1)/(2p − 1 − k)]), and does (W) plus Gaussian concentration of a 1-Lipschitz functional give
     max over 𝔓 of [Z²_{T,l} − c_n(|T|)] ≤ 0 with probability → 1?
   * (C3)(b): is the converse correctly stated (direction of the inequalities, the factor 2p, feasibility of T ∪ {l})?
   * (C3)(c): check the three implications by hand, constants included: (W-χ) ⇒ (W); (W-ref) ⇒ (W-unif) ⇒ (W) with
     δ₀ = (1 − 2b − 2h)/4; (W-loc) ⇒ (W-ref). Is the variance-ratio clause of (W-loc) needed, and is its
     parenthetical remark right?
   * (C4): do RM-F's and RM-R's hypotheses (W3-RM `STATEMENT.md` §3–§4) imply those of (C1), (C2) as claimed?
   * (C2) and bridges (P7)–(P9): are the budgets 15ρ + b < ½ and b < ½ what W2-LOC2 `lemmas/L6_poly.md` (P6), (P11)–(P15),
     (P18)–(P19) give when the design family is replaced by the abstract conditions? Is (W-R) well-posed, and can a
     joint-law bound on max|Z_{T,l}| be turned into the conditional-mean statement in (W-R)?
   * the toolkit (P0) at polynomial size: which conditions on (|Q|, n) do the GEN-L1 / C-GROW L0 proofs need?
   Say explicitly which claims you checked and how, and which you could not check.
6. **Honesty of scope.** Does §6 "Not claimed" say clearly what is missing (no theorem without a lattice condition;
   b ≥ ½)? Is anything claimed that the plan cannot plausibly prove? Is the dependency section (§5) accurate about
   what is consumed as proved, what is conditional, and what is only a template?

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
