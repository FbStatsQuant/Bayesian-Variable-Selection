# VLC1 brief — blind line check of track-V item V1 (Lemma VIS: visibility with a margin uniform in n) (Claude Opus 5.5, high; fresh agent)

You are an independent line checker and have never seen this work. Read only the files below; do not open any LOG,
CHECKPOINT, INDEX, CHECK or `reviews/` file. Write no files; change no git state; start no subagents. Your job is to
**break** this lemma.

Workspace: `/home/fb31/BVS-wt/W3-AUDIT`.
- The item: `Theory_work/Wave3/W3-AUDIT/track_V/V1_VIS/{STATEMENT,PROOF}.md`.
- Context (to see what the lemma is for; do not review): the visibility hypotheses of Theorems 5, 6, 10 —
  `git -C /home/fb31/BVS-wt/W3-AUDIT show origin/main:Theory_work/Wave3/W3-READER/READER_VERSIONS.md` lines 575-590,
  660-700, 1287-1295; the partial-covariance notation `git ... show origin/main:Theory_work/Wave3/W3-READER/NOTATION.md`
  lines 155-175; the design dossier `Theory_work/Wave3/W3-AUDIT/TRACK_B.md:209-233` and `Theory_work/Wave3/W3-AUDIT/track_C/RESULTS.md:60-70`.

The requirement the lemma must meet (binding): a lower bound a > 0 on |Cov(W_j, Wᵀθ* | W_U)| that is **uniform in n** and
over all U with |U| ≤ 15, for designs with finitely (or countably) many local patterns, under a stated sign condition or
for θ in a stated open set — **not** merely "nonzero for almost every θ".

Check:
1. **Correctness** of every step: F1, F2 (Stieltjes inverse ≥ 0 via Perron–Frobenius and the Neumann series), (VIS-0)
   reduction and the lower bound on Var(W_j | W_U), (VIS-a) incl. the component argument and the sign bookkeeping, (VIS-b)
   closedness of B and the distance bound, (VIS-c), (VIS-d) (locality of γ, continuity, compactness, the one-point
   compactification for stationary designs, the finite-pattern examples), (VIS-e) (the inverse formulas and floors for
   AR(ρ) incl. ρ < 0, equicorrelation, one factor, blocks). Try counterexamples (small matrices) to any inequality.
2. **Strength**: does the lemma really give a margin uniform in n (is B independent of n; is δ > 0 a sensible, checkable
   condition; is the "almost every" trap avoided)? Is any clause stronger than proved? Every hypothesis stated?
3. **Faithfulness**: is the target condition quoted correctly (Theorem 6 (A3), Theorem 5 (A4), Theorem 10 (A4))?
If a clause is false, say so first and tag it **C**.

Reply (plain markdown, as your final message): verdict `VERIFIED` / `VERIFIED WITH AMENDMENTS` / `NOT VERIFIED`, then
numbered findings tagged **C**, **S**, **F** or **E** with file:line, what fails, and the fix. Last line:
`VLC1-VERDICT: V1=<…>`.
