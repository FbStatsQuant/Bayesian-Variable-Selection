# BRIEF — lemma check LC1-B (seat: Codex gpt-6.1-sol, reasoningEffort high) — blind first read of L2 (key lemma) and L3

You are an independent line-by-line checker for theory ticket W3-RM2 of the SMC-BVS project (Bayesian variable
selection; this ticket proves that the coded method reports the true model when the set Q of "leaking" columns has
polynomial size n^b). The proofs were written by a Claude model; you are the cross-family check. This file is your
whole brief. Work only inside the worktree `C:/Users/felip/BVS-wt/W3-RM2` (paths below are relative to it). **Change
no git state. Write exactly one file:** `Theory_work/Wave3/W3-RM2/reviews/LC1B_L2L3_check_sol.md`. Do not edit any
other file (if you run code, write your scratch files outside the worktree). Do not start subagents. Use no effort
setting above high.

## Frozen content
The round is frozen in `Theory_work/Wave3/W3-RM2/reviews/MANIFEST_LC1.txt`; its first line is
`MANIFEST 0caea883fcf38765f1ebe5b264e8300622f80f6e444a49855ad91725e06f1558`. **Quote this digest line verbatim at the top of your review.**

## Files you may read
Only files listed in the manifest:
* the objects under review: `Theory_work/Wave3/W3-RM2/lemmas/L2_width.md` (the key lemma: Lemma 0, NA-conv, NA-W,
  W-conv and its corollary, the sufficient forms (i)–(v), Lemma d, Lemma TL-W) and
  `Theory_work/Wave3/W3-RM2/lemmas/L3_assemblyF.md` (Theorem RM2-F and the containment of RM-F);
* `Theory_work/Wave3/W3-RM2/lemmas/L0_toolkit_b.md` — the toolkit L2 uses. **Take its statements (T1)–(T5) as given**
  (another reviewer checks its proof); but check that L2 uses them within their hypotheses;
* `Theory_work/Wave3/W3-RM2/lemmas/L1_sandF_b.md` — statement only (L3 cites it; another reviewer checks its proof);
* `Theory_work/Wave3/W3-RM2/STATEMENT.md` (v1.3: §1 definitions, §3.1 conditions, claims (C1), (C3), (C4), bridges
  (P2)–(P5));
* `Theory_work/Wave3/W3-RM2/numerics/lemma_checks.R`, `lemma_checks_out.txt`, `check_identity.R`,
  `check_identity_out.txt`, `RESULTS.md` §5 (falsification numerics; blocks K3–K7 concern L2);
* the external inputs of `Theory_work/Wave3/W3-RM2/reviews/INPUTS.txt` — in particular
  `Theory_work/Wave3/W3-RM/STATEMENT.md` (RM-0 at lines 160-176; RM-F at 178-185; conditions (N-χ), (N-D) in §3.1),
  `Theory_work/Wave3/W3-RM/lemmas/L0_core.md`, `Theory_work/Wave1C/C-GROW/lemmas/L1_descent.md`,
  `Theory_work/Wave1C/C-GROW/lemmas/L2_NA_TL.md`, `Theory_work/Wave3/W3-RM/lemmas/L2_NAF.md` (templates), and the
  registry `Theory_work/INFRA/registry/claims.tsv`.
Do not read anything in `reviews/` other than the manifest and INPUTS.txt, any `LOG.md` or `CHECKPOINT*.md`.

## Task
Check every step as a referee who wants to find the error.
1. **Lemma 0.** (G1), (G2), (G3) with their constants; is the sub-Gaussian moment bound for Lipschitz functions
   quoted correctly, and are the two tail bounds used later consequences of it?
2. **NA-conv.** The exact prior ratio; the use of (T5)(b) (is x ≤ ¼ justified, is the excess really o(1) uniformly);
   the final value −½; does it prove NA(𝓛) as RM/C-GROW define it (which pairs)?
3. **NA-W.** Lipschitz property of the shifted maximum; the deterministic bound s_n ≤ a⁰_n(|T|) for every pair; the
   algebra from |Z| ≤ a − s_n/2 to Z² ≤ c_n(|T|); the size condition on s_n; the bound exp(−s_n²/8); what n₀ depends
   on; the (W-δ) corollary and the constant c* = δ₀²/(32(2A + 2)).
4. **W-conv and its corollary.** Lower tail; the lower score conversion ((T5)(c) needs Λ_T = 0 — true?; the prior
   ratio from below; feasibility of T ∪ {l}); the algebra leading to ¼as_n − 1 − log 2 − 2κ_E; the threshold
   s_n√(log(n + 1)) ≥ 8κ_E + 8; the corollary's constants. Is the "Reading" paragraph an accurate, not overstated,
   summary?
5. **Sufficient forms.** (ii) the constant "δ log n ≥ 2 log 2"; (iii) inequality (3.1) (orthogonality, the range
   inclusion, the count of directions), the Jensen step, the comparison of the two right sides; (iv) each of the
   three terms, e_n = o(√log n), the gap δ√(log n)/√(2A + 1), and that RM's (N-D)(i) is the stated special case;
   (v) the decomposition, the bound on ‖v‖, the atom coefficients L_n/φ₀, the count p·2^{ν_n}, the parenthetical
   remark.
6. **Lemma d and TL-W.** The subspace argument; identity (4.1) (signs; the swap case; why u_{A,i}ᵀμ = θ*_i‖(I − P_A)x_i‖);
   which neighbours remove a truth; pairs with |T| = K; the sizes (λ_n/4, λ_n/8); the score comparison; does 𝒟ᵀ_n
   contain every direction used; is the dependence on (W) (through 𝒵⁺_n) stated honestly?
7. **L3.** Does every hypothesis of each cited lemma follow from the hypotheses of (C1)? Is RM-0 applied within its
   statement (RM `STATEMENT.md:160-176`)? Is the conditional status (SOP:TH09) carried? Is the containment of RM-F
   correct under both branches (N-χ) and (N-D), including the choice of b and the BM chain?
8. Try to falsify: p = 1; Q = S₀; Q = [p]; |T| = K; 𝔓 = ∅; s₀ = 1; a gap s_n larger than the smallest level; a design
   where every lattice direction coincides; signs of θ*. You may run small numerical checks of your own (outside
   the worktree) and report them.

## Output format (in your one file)
```
MANIFEST <digest>
Verdict per lemma: Lemma 0 …; NA-conv …; NA-W …; W-conv (+corollary) …; sufficient forms (i)–(v) …; Lemma d …;
  TL-W …; Theorem RM2-F (assembly) …; containment of RM-F … — each VERIFIED | VERIFIED-WITH-AMENDMENTS | WRONG
Findings: numbered; each FATAL (the lemma is false or the proof has a gap that needs a new idea) / MAJOR (a step is
  wrong or missing but repairable; give the repair) / MINOR / NIT; with file:line and the exact correction.
Checks performed: step by step, what you verified and how.
Not checked: list.
```
End your reply with the verdict line(s) and the path of your file.
