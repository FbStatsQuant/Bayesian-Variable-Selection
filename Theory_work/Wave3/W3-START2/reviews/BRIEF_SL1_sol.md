# BRIEF — statement-lock review SL1 (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent reviewer for theory ticket W3-START2 of the SMC-BVS project. This file is your whole brief.
Work only inside the worktree `C:/Users/felip/.t3/worktrees/Bayesian-Variable-Selection/t3-0d1ae879-e1e1cd03cea23a59`
(all paths below are relative to it). **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-START2/reviews/SL1_statement_lock_sol.md`. Do not edit any other file. Do not start subagents.
Use no effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START2/reviews/MANIFEST_SL1.txt`. **Quote its first line (`MANIFEST
<digest>`) verbatim at the top of your review.** You may run `python -B Theory_work/Wave3/tools/manifest.py verify
Theory_work/Wave3/W3-START2 Theory_work/Wave3/W3-START2/reviews/MANIFEST_SL1.txt` and report its result.

## Files you may read
Only the files listed in that manifest: `Theory_work/Wave3/W3-START2/STATEMENT.md` (the object under review),
`Theory_work/Wave3/W3-START2/PLAN.md` (the lead's proof sketches), `Theory_work/Wave3/W3-START2/BRIEF.md` (HQ's
ticket brief), and the external inputs listed in `Theory_work/Wave3/W3-START2/reviews/INPUTS.txt`: the pinned code,
the base statement `Theory_work/Wave3/W3-START/STATEMENT.md` (version 1.3.4), the base proof files
`Theory_work/Wave3/W3-START/lemmas/L1…L11`, and three source statements. Do not read any file in any `reviews/`
folder other than the manifest and INPUTS.txt (in particular nothing in `Theory_work/Wave3/W3-START/reviews/`), any
`LOG.md`, any `CHECKPOINT*.md`, or any `REPORT.md`.

## What is under review
`STATEMENT.md` is a **delta statement**: version 1.4 of the start-mass statement = the base statement v1.3.4 with
two amended definitions (§2: the sharp leading functional 𝔏^♯_n(h); assumption (L-R⁺)) and nine claims (§3: Lemma
LEAK-0, (T1⁺), F2⁺, (T3⁺)(a), (T3⁺)(b), (B-R⁺), (T4⁺), IF-START⁺, OVL⁺). The base statement and its proof files are
council-passed and are **not** under review; treat their claims and proof steps as given, and check that the delta
uses them correctly. The proofs of the changed steps are not written yet; `PLAN.md` §3 has the sketches.

## What a statement-lock review is
You decide whether the **target statement** is fit to be locked before proof work starts. You are briefed to break
it. Check, with file:line evidence:
1. **Well-posedness.** Every object, quantifier and constant of §2–§3 is defined (here or at the cited base lines);
   each claim is a definite mathematical statement (what is random, what is fixed, which limit). Check every base
   line reference in §1–§5 of the delta: does the cited span contain what the delta says it contains?
2. **Each claim is true as stated — try to refute it.** For each of the nine claims, use the sketch in `PLAN.md` §3
   and the cited base proof lines, and look for a counterexample, a limiting case or a gap:
   * Lemma LEAK-0 and (T1⁺)(b),(d): the split of the null columns, the count |𝒩_exc| ≤ 16 − s₀, the facts
     (p − s₀)/(4p) ≤ 𝔏^♯_n(h) ≤ 𝔏_n(S₀; h), the admissible range of λ, the constants 5, 15, 451, the claim that the
     constants c₀, n₀ of the base Proposition L5.2 can be kept; the cases s₀ = 0, s₀ ≥ 16, p = s₀ + 1, bounded p, all
     columns in one block, p ≫ n. Is the small-gain premise of the base step bound L3.3 available for every column
     where it is used?
   * F2⁺: does any step of the base proof L6.2 still need p/√log n → ∞? Is "exact order n^{−1/2}" right for fixed p?
   * (T3⁺)(a), IF-START⁺: do they follow from (T1⁺)(d) exactly as their base versions follow from (T1)(d)?
   * OVL⁺: the identity, the product inequality (check it by hand or by enumeration on small positive tables with
     the prior w(k) = ½/C(2p − 1, k)), and whether any use of (V-c) or of e_n survives; is (V-m) "with this Q"
     enough for (T1⁺)(a)?
   * (N2⁺): the counting argument, the role of the uniqueness of the block containing S₀, the exclusion of s₀ = 0,
     equality with the base (N2) for s₀ ≥ 16, and non-vacuity of the premise together with (E) and (GF-16).
   * (L-R⁺), (B-R⁺), (T3⁺)(b): find every place in the base proof `lemmas/L9_BR.md` (and in what it uses from L5,
     L6, L8) where the size of Q is used; is the uniform bound (T1)(d) really uniform in Q with |Q| ≤ K; is the
     "trivially true when the right side is ≥ 1" argument sound for a deterministic sequence Q_n, for the
     probability-to-one display and for the O_P display of the clause C_L = 0?
3. **Supersession.** §5 claims that each new claim implies the base claim it replaces. Check each row.
4. **Design-agnostic form.** No design family in any statement; theorem hypotheses are partition-free conditions on
   (X, θ*) or (Σ_n, θ*).
5. **Honesty of scope.** Does §4 say clearly what is not claimed? Is anything claimed that the sketches cannot
   plausibly prove? Is the dependence on the base ticket's status stated correctly (§5)?

## Output format (in your one file)
```
MANIFEST <digest>            (verbatim first line of the manifest)
Verdict: LOCK | LOCK WITH CHANGES | DO NOT LOCK
Required changes: numbered; each with location (file:line), the problem, and the exact change you require.
Optional suggestions: numbered.
Checks performed: what you verified and how (algebra, enumeration, counterexample attempts), per claim.
Not checked: list.
```
Classify each required change as CRITICAL (a claim is false or ill-defined), MAJOR (a hypothesis or scope must
change) or MINOR (wording, citation, missing definition). Use DO NOT LOCK only if a CRITICAL change cannot be made by
a local edit of the statement; otherwise use LOCK WITH CHANGES and give the exact edits. Do not propose a different
theorem. End your reply with the verdict line and the path of your file.
