# BRIEF — independent mid-point review MP1 (seat: Codex gpt-6-astra, reasoningEffort high) — blind first read

You are an independent senior reviewer for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable selection
by sequential Monte Carlo; this ticket is about when the coded method **reports the true model S₀** when the set Q of
columns that may "leak" signal has polynomial size n^b). This file is your whole brief. Work only inside the worktree
`C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change no git state. Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/MP1_midpoint_astra.md`. Do not edit any other file (scratch files for your own
checks go outside the worktree). Do not start subagents. Use no effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_MP1.txt`. Its first line is
`MANIFEST 960c9069b362a251403f6aed9cd804c96870fd63775a72ebf307588b45a10730`. **Quote this digest line verbatim at the top of your review.**

## Files you may read
Only the files listed in that manifest:
* `Theory_work/Wave3/W3-RM2/STATEMENT.md` — the target statement (v1.3);
* `Theory_work/Wave3/W3-RM2/lemmas/L0_toolkit_b.md`, `L1_sandF_b.md`, `L2_width.md` (the **key lemma**),
  `L3_assemblyF.md` — the proofs written so far (fixed-design form only);
* `Theory_work/Wave3/W3-RM2/PLAN.md`, `ASSUMPTION_MAP.md`, `BRIEF.md` (HQ's ticket brief);
* `Theory_work/Wave3/W3-RM2/numerics/` (RESULTS.md, SPEC.md, scripts and outputs — observations, not proofs);
* the external inputs listed in `Theory_work/Wave3/W3-RM2/reviews/INPUTS.txt` (pinned code; the wave PROGRAM and
  PROTOCOL; the parent result W3-RM with its lemmas; the engines C-GROW / W1-GEN / W2-LOC2; the registry).
Do not read any other file in any `reviews/` folder (except the manifest and INPUTS.txt), any `LOG.md`, any
`CHECKPOINT*.md`, or anything under `C:/Users/felip/BVS-wt/W3-MEMO-SCR-RM`. Markers such as [SL1-#], [CP1-P#],
[LC1A-#] in the files point to earlier internal rounds whose reports you are not given; judge the text as it stands.

## Where the ticket is
The fixed-design theorem (C1) "RM2-F" is claimed proved by the four lemma files: toolkit (L0), fixed-design
sandwich (L1), the key lemma (L2: whole-lattice no-addition from the width gap, with a rate; its converse; the
sufficient forms; truth removal under (BM-W)), and the assembly with the containment of the parent theorem RM-F
(L3). The Gaussian-row theorem (C2), the examples (C5) and the sharpness record (C6) are **not yet written**.

## Your task — an independent mid-point judgement
1. **Is the key lemma proved?** Read `L2_width.md` as a referee. Verify, with your own derivations, the steps you
   consider most likely to hide an error; at least: the concentration step and the algebra giving
   P(𝒵_nᶜ) ≤ exp(−(𝔴⁰_n)²/8) (Lemma NA-W); the size-dependent score conversion (Lemma NA-conv) and its use of the
   toolkit; the converse (Lemma W-conv); the chain (W-loc) ⇒ (W-ref) ⇒ (W-unif) ⇒ (W-δ) ⇒ (W) and (W-χ) ⇒ (W-δ);
   the truth-removal identity (4.1) and Lemma TL-W, including its dependence on the addition bound 𝒵⁺_n.
2. **Does the chain L0 → L1 → L2 → L3 prove (C1) exactly as stated in STATEMENT.md?** Look for: a hypothesis used in
   a proof but missing from (C1); a conclusion of (C1) not delivered; a quantifier or uniformity gap ("for every
   maximiser", "for every admissible run", n₀'s dependence); a consumed result used outside its statement or its
   recorded status (STATEMENT §5; `Theory_work/INFRA/registry/claims.tsv`); an inconsistency between the statement's
   definitions (§1, §3.1) and the objects the proofs use; a mis-applied import of the parent's core RM-0
   (`Theory_work/Wave3/W3-RM/STATEMENT.md:160-176`, `lemmas/L0_core.md`).
3. **Is the statement itself sound at this stage?** In particular: is (W) (width gap → −∞) a genuine condition on
   (X, θ*, Q) with a non-empty set of natural examples at polynomial |Q| (check the sufficient forms against what
   polynomially large leak sets can satisfy), or is it close to vacuous or to a restatement of the conclusion? Is
   (BM-W) well-posed? Are the "not claimed" items and the limits remark honest about what the numerics show?
4. **Is the remaining plan sound?** (PLAN.md §3 and §5; STATEMENT bridges (P7)–(P10) for Gaussian rows.) Name the
   step of the Gaussian-row form you consider most at risk and why.
5. **Verdict:** `CONTINUE` (the key lemma stands; proceed), `CONTINUE WITH CHANGES` (list the required changes), or
   `STOP` (a FATAL gap: say which claim falls and what would be needed).

## Output format (in your one file)
```
MANIFEST <digest>
Verdict: CONTINUE | CONTINUE WITH CHANGES | STOP
Findings: numbered; each FATAL / MAJOR / MINOR / NIT, with file:line, the problem, and the exact correction or the
  missing argument.
Independent derivations: what you re-derived yourself, step by step, and the outcome.
Assessment of the statement (item 3) and of the remaining plan (item 4).
Not checked: list.
```
End your reply with the verdict line and the path of your file.
