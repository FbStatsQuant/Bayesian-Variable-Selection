# BRIEF — statement diff check SC4 (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read

You are an independent reviewer for theory ticket W3-START of the SMC-BVS project. This file is your whole brief.
Work only inside the worktree `C:/Users/felip/BVS-wt/W3-START` (paths below are relative to it). **Change no git
state** (read-only git commands such as `git show`, `git diff` are allowed). **Write exactly one file:**
`Theory_work/Wave3/W3-START/reviews/SC4_diff_check_sol.md`. Do not edit any other file. Do not start subagents. Use no
effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-START/reviews/MANIFEST_SC4.txt`. Its first line is
`MANIFEST 26e9e50976f67a4f31e94498395a339d158cf569bb4334b4485666c13cd69734`. **Quote this digest line verbatim at the
top of your review.** You may run `python -B Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-START
Theory_work/Wave3/W3-START/reviews/MANIFEST_SC4.txt`.

## Files you may read
Only files listed in that manifest: the ticket's `STATEMENT.md` (v1.3.1, the object under review), `PLAN.md`,
`BRIEF.md`, `ASSUMPTION_MAP.md`, the `lemmas/` folder (proofs of the fixed-design part: L1–L5), the `numerics/` folder,
and the external inputs in `Theory_work/Wave3/W3-START/reviews/INPUTS.txt`. In addition you may read the previous
locked version with `git show HEAD:Theory_work/Wave3/W3-START/STATEMENT.md` (v1.3) and compare
(`git diff HEAD -- Theory_work/Wave3/W3-START/STATEMENT.md`). Do not read any other file in any `reviews/` folder
(except the manifest and INPUTS.txt), any `LOG.md`, or any `CHECKPOINT*.md`.

## What this review is
Version 1.3 was the locked target; the fixed-design part ((C0), (T0), (C1), (T1), the bridges (B-TK), (B-L), (B-V1),
(B-V2)) has proofs in `lemmas/`. Version 1.3.1 makes four changes, none of which is meant to touch a proved claim:
1. **Scope of the leaking-null limit.** (N2) of (T4) gets a scope paragraph: its premise cannot hold when s₀ ≤ 15
   (the set V = S₀ is included and every null gain given all truths is zero), so the partition-free limit is
   non-vacuous only for s₀ ≥ 16; for s₀ ≤ 15 the one-column failure threshold is claimed on the actual partition by
   (C2)(i). The overview §0 (iv) and the remark in Corollary F4 now refer to (C2)(i).
2. **Quantitative form of [TK].** A paragraph at the end of §4 says which form of the toolkit the bridges use.
3. **(B-R), clause C_L = 0.** The bridge row now states 𝔏_n(Q) = O_P((log n)^{15κ_Q+1/2}) (tightness) instead of a bound
   with a fixed constant holding with probability → 1; the proof-structure sentence of (T3)(b) is adjusted.
4. **Examples table (T7).** Verified families are separated from expected ones; the fixed-design examples are
   restricted to p ≤ n − 1 and described more precisely.

Check, with file:line evidence:
A. **Completeness.** List every difference between v1.3 and v1.3.1. Is there any change outside the four items and
   the header?
B. **Correctness of each change.**
   * Item 1: verify that δ_{S₀,l} = 0 for every null l (so the premise of (N2) is empty for s₀ ≤ 15, including
     s₀ = 0), and that for s₀ ≥ 16 the premise is satisfiable in principle. Is (C2)(i) correctly described (which
     conditioning set, which threshold)? Does the sentence "(N2), (N3) follow from (C2)" remain true? Is any other
     sentence of the statement, of `ASSUMPTION_MAP.md` or of `PLAN.md` now inconsistent with the scope paragraph (for
     example a claim that the leakage level is necessary in partition-free form)? Is (N3) affected by a similar
     vacuity?
   * Item 2: is the paragraph an accurate description of what `lemmas/L2_TK.md` delivers and of what
     `lemmas/L3_LEAK.md`, `lemmas/L4_VIS.md` use? Does it add or remove a hypothesis of any claim?
   * Item 3: with the bridge clause weakened to tightness, does the last sentence of (T3)(b) (the O_P rate for
     C_L = 0) still follow from a uniform conditional bound of the form (T1)(d)? Is the main display of (T3)(b)
     (probability → 1 with the factor exp(C_R√log n)) still supported by the first part of the bridge row? Is the
     interface corollary (T5) under (T3)(b) affected?
   * Item 4: is anything that v1.3 claimed about examples now silently dropped rather than labelled? Is the new
     description consistent with the hypotheses of F1, F2, F4, (GF-16), (V-m), (T3)(b) (for instance: can a fixed
     design with p ≤ n − 1 retained columns have exactly orthogonal centred columns; is "at most one truth per group"
     a sensible restriction for population visibility in a block-diagonal covariance)?
C. **Effect on proved claims and on consumers.** Confirm that no hypothesis or conclusion of (C0), (T0), (C1), (T1) and
   of the bridges proved in `lemmas/` changed, and that (T5) still delivers what `Theory_work/Wave3/W3-SAMP/STATEMENT.md`
   asks (P-START at its line 76; P-OVL at its line 82).
D. **Classification.** For each of the four items say whether it is editorial, a narrowing of a claim, or a
   strengthening.

## Output format (in your one file)
```
MANIFEST <digest>            (verbatim first line of the manifest)
Verdict: ACCEPT | ACCEPT WITH CHANGES | REJECT
Required changes: numbered; each with class (CRITICAL / MAJOR / MINOR), location (file:line), the problem, and the
                  exact change you require.
Optional suggestions: numbered.
Checks performed. Not checked.
```
End your reply with the verdict line and the path of your file.
