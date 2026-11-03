# LIT-PAR — REPORT: is there already a parallel, correlation-robust BVS with strong guarantees?

Run of 2026-11-03, branch `theory/LIT-PAR`. Literature task: no new theorem is claimed. Status words follow
`theory_campaign/PROTOCOL.md`; a "PROVED" attributed to a paper means that the paper states it as a theorem. All our
own items are **candidates**. Source notes with verbatim quotes are in `notes/01–07`. Every entry below names the file or URL
actually read. **UNVERIFIED** marks anything seen only second-hand.

(DRAFT v0. Sections 1–3 will be completed once the two sub-sweeps, notes/03 and notes/04, land.)

## 1. Headline

1. **Verdict on the gap claim: TRUE WITH QUALIFICATIONS.** Feature-splitting and data-splitting BVS with theorems all need
   design conditions that strongly correlated or masked designs violate. Song–Liang needs a nonzero within-split projection
   coefficient for every true variable. DECO needs a well-conditioned Σ and s² log p/n small. BB-SSL needs low mutual
   coherence. DFP needs consistent plug-in estimates. Or else they do not target the model-space posterior. We found **no**
   published method that combines (i) the exact model posterior with an unbiased Ẑ, (ii) communication-free width, and
   (iii) a proved bound on the sequential depth under a correlated design.
2. **The literal claim "methods with guarantees are sequential" is FALSE in the work/depth sense.** It must not appear in
   the paper. ZYVR's informed chain (JRSSB 2022) has a proved p-free iteration bound, T_mix ≤ 800·max(nκ₁/c₁, 3s₀). Each
   iteration scores O(p·s₀) neighbours, and the authors note these scores "can be easily parallelized". That gives
   depth O(n log p) under Condition 1, which API-POS found to hold on our LH family with ZYVR's own priors (PROOF SKETCH).
   This is the strongest counterexample candidate.
3. **Two of our ingredients are standard and must be cited as such.** Ẑ-weighted pooling of R independent SMC runs,
   consistent as R → ∞ at fixed N (our T31(i)), is eq. (4.8) of Dai–Heng–Jacob–Whiteley (2022). It traces back to
   Andrieu–Doucet–Holenstein (2010). "Parallel strong scaling" of non-communicating Ẑ-weighted islands has a published
   generic theorem (Liang et al. 2024, MSE ≤ C/(NP)), proved under global Doeblin mixing. Parallel tempered SMC for BVS on
   {0,1}^p is Schäfer–Chopin (2013). Exact per-block enumeration on correlation-clustered blocks, parallel over blocks, is
   Papaspiliopoulos–Rossell (2017); it is exact only for a block-diagonal Gram matrix.
4. **Self-critique: our own depth is Θ(p) per move round, not O(1).** The v3 round runs p + B + 2 elementary steps one
   after another within each particle. So "depth = stage count T" holds only if a round counts as one unit. Counted in
   score evaluations, the depth is T·L·(p + B + 2). That is worse in p than a parallelised informed chain. Either state the
   depth honestly or change the move kernel (§3).
5. **What survives (our candidates; no literature equivalent found).**
   - O-STAGES' stage-count laws: T* = O(1) favourable, log₂A₀ + O(1) masked.
   - The masked-start regime: generic SMC complexity theory (Mathews–Schmidler 2024) degrades exponentially there through
     μ⋆, and our LH results (T38 (b1-LH)/(b2-LH)) address it.
   - The exact block start used as the SMC initial law with a bridge to the exact posterior.

## 2. Annotated table
(see §2 below; filled from notes)

## 3. Gaps, threats, phrasing
(pending)

## 4. Sources actually read
(pending; see notes/*.md)
