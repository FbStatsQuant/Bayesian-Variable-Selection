# BRIEF — statement-change check SC1 (seat: Codex gpt-6.1-sol, reasoningEffort high) — fresh review of a post-lock change

You are an independent reviewer for theory ticket W3-RM2 of the SMC-BVS project. This file is your whole brief. Work
only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (all paths below are relative to it). **Change no git state**
(read-only git commands such as `git diff --no-index` or `git show` are allowed). **Write exactly one file:**
`Theory_work/Wave3/W3-RM2/reviews/SC1_statement_change_sol.md`. Do not edit any other file. Do not start subagents.
Use no effort setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_SC1.txt`. Its first line is
`MANIFEST 9af7889ee7da1292df93b4e802ce07e440a12e18c115428c33749bfd9fdae3dc`. **Quote this digest line verbatim at the
top of your review.** You may run `python Theory_work/Wave3/tools/manifest.py verify Theory_work/Wave3/W3-RM2
Theory_work/Wave3/W3-RM2/reviews/MANIFEST_SC1.txt` (from the worktree root) and report its result.

## Files you may read
* the files listed in the manifest — in particular `Theory_work/Wave3/W3-RM2/STATEMENT.md` (now **v1.3**, the
  object under review), `ASSUMPTION_MAP.md`, `PLAN.md`, `BRIEF.md`, `numerics/RESULTS.md`, and the 31 external inputs
  of `reviews/INPUTS.txt` (the parent result W3-RM, the engines C-GROW / W1-GEN / W2-LOC2, the pinned code);
* `Theory_work/Wave3/W3-RM2/reviews/STATEMENT_v1.2_LOCKED.md` — the locked text before the change (identical to the
  file committed at `81ff7d6`);
* `Theory_work/Wave3/W3-RM2/reviews/BT1_better_theorem_astra.md` (the review that proposed the two changes, P1 and
  P2) and `reviews/BT1_disposition.md` (the lead's disposition, including the constant-free form "G1" of P2);
* `Theory_work/Wave3/W3-RM2/reviews/post_BT1_addendum/README.md` (source of the limits remark).
Do not read any `LOG.md`, any `CHECKPOINT*.md`, the other files in `reviews/`, or anything under
`C:/Users/felip/BVS-wt/W3-MEMO-SCR-RM`.

## Background
STATEMENT v1.2 was locked after three statement-lock rounds. HQ then adopted two improvements proposed by the
better-theorem review, to be written into v1.3 and checked by one fresh reviewer before any proof work
(PROTOCOL rule 15: a change to a statement needs a fresh review of the change and of what depends on it):
* **[CP1-P1]** the signal floor (BM-Q) is replaced by (BM-W), a floor at the Gaussian width d_n of the
  truth-removal directions;
* **[CP1-P2]** the lattice-width condition (W) is stated as a diverging gap (𝔴⁰_n → −∞, constant-free level
  a⁰_n(k)), the converse as 𝔴⁰_n → +∞, and an explicit failure rate for no-addition is added; the v1.2
  fixed-fraction condition becomes the named sufficient form (W-δ).
Nothing in the statement is proved yet; this is still a target. You are briefed to break the change.

## Task
1. **Diff.** Compare v1.2 and v1.3 and list every changed hunk. Classify each as (a) part of [CP1-P1], (b) part of
   [CP1-P2], (c) the limits remark / registry state note / header (record), or (d) anything else — any (d) hunk
   that alters a hypothesis, claim, bridge statement, constant or code pin is a defect.
2. **Is each v1.2 hypothesis sufficient for its v1.3 replacement?** Check by hand, constants included:
   * (BM-Q) ⇒ (BM-W): is d_n ≤ √(|Q| + 1) + √(2 log(2p)) correct for the family 𝒟ᵀ_n as defined in §1 (which
     subspace contains u_{A,i}; are the directions defined under (FL-Q))? Is "BM-∞ suffices when d_n² = O(log n)"
     right?
   * (W-δ) ⇒ (W): the bound a⁰_n(k) − a_{n,δ}(k) ≥ δ√(log n)/(2√(2A + 2)) for n ≥ 3, p ≤ n^A, k < p; hence
     𝔴⁰_n ≤ 𝔴_n(δ) − δ√(log n)/(2√(2A + 2)).
   * the chains in (C3)(c) and (C4) (containment of RM-F and RM-R, including the BM chain).
3. **Are the new claims plausible as stated?** Try to refute them.
   * (C3)(a): from 𝔴⁰_n → −∞ and Gaussian concentration of a 1-Lipschitz functional, does
     P(some (T, l) ∈ 𝔓 has Z²_{T,l} > c_n(|T|)) ≤ exp(−(𝔴⁰_n)²/8) hold for n ≥ n₀? (Note c_n(k) = a⁰_n(k)² − 4κ_E − 2;
     check what n₀ must depend on, and the edge case of a gap larger than the smallest level.) Is
     c* = δ₀²/(32(2A + 2)) right under (W-δ)?
   * (C3)(b): from 𝔴⁰_n → +∞, does P(NA(𝓛)) → 0 follow with the stated bound? Check the lower score conversion for
     an addition at a lattice set of size k < K: prior ratio (k + 1)/(2p − 1 − k) ≥ (k + 1)/(2p),
     ν log(RSS_T/RSS_{T∪{l}}) ≥ νσ²Z²/RSS_T, RSS_T ≤ ‖Cε‖², bounded remainders 2κ_E. Is the parenthetical claim about
     the v1.2 converse right?
   * bridge (P2): the identity RSS_A − RSS_T = (θ*_i‖(I − P_A)x_i‖ + σZ_{A,i})² − σ²Z²_{T,l} for A = (T ∖ {i}) ∪ {l},
     T ⊇ S₀ (last term absent for a deletion); does (BM-W) plus a uniform bound Z²_{T,l} ≤ (2A + 2) log n give
     RSS_A − RSS_T ≥ c·nφ₀²θ*²_min and then F(A) < F(T) through C-GROW L2.1's comparison? Is the treatment of pairs
     with |T| = K (not in 𝔓) adequate? Does 𝒟ᵀ_n contain every direction the argument needs?
   * (W-R) in its new form and bridge (P9): consistent with (C2) and with the F→R bridge (P8)?
4. **Records.** Registry block §7: A:BM-W and A:W rows, the alternatives row of W-suff, the sharpness/binding
   entries, the CANDIDATE note — do they state exactly what the statement claims? Is the limits remark in (C6) an
   accurate summary of `numerics/RESULTS.md` B4 and the addendum, and clearly labelled an observation?
   Is `ASSUMPTION_MAP.md` (two rows marked [v1.3]) consistent with v1.3?
5. **Verdict.** `ACCEPT v1.3` / `ACCEPT WITH CHANGES` (list each required change exactly, classified CRITICAL / MAJOR
   / MINOR) / `REJECT` (the change makes a claim false or ill-defined and cannot be repaired by wording).

## Output format (in your one file)
```
MANIFEST <digest>
Hunks: numbered, classified (a)/(b)/(c)/(d).
Checks: per item of the task, what you verified and how (algebra, counterexample attempts).
Required changes: numbered, classified, with location and exact text (or "none").
Verdict: ACCEPT v1.3 | ACCEPT WITH CHANGES | REJECT
Not checked: list.
```
End your reply with the verdict line and the path of your file.
