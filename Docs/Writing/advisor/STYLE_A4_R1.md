# STYLE_A4_R1: advisor note on the outline of the unified manuscript (2026-11-17)

Read: `manuscript/OUTLINE.md`; page maps and notation of D1 v1 (19 pp), D2 v2.1 (main text 11.5 pp), A2 v2.1 (6 pp).

## (a) One paper, or three stapled? Six seams, each with its bridge
1. **§3 → §4.** §3 ends on a parameter table; §4 opens on a results table. Bridge: close §3 with "What the results
   need from the method", five lines naming the start law, the reported model and its certification, the pooled
   estimates, the returned list and the conventions, each with its stage. That is D2 §2.2, which then disappears.
2. **§4 → §5.** A2 names the theorems ("the reported-model theorem"); D2 numbers them (Results 1–5). Use "Result 3
   (the reported model)" at first use in §5, then one form throughout.
3. **"Our designs" in §5** come from simulation studies that this manuscript does not present. A referee will ask
   where they are. One sentence in §1 and one in §5.2: what the studies are, and where they are reported.
4. **Notation, once D1 and D2 share a page.** $L$ is the burn-in count (D1) and the sub-Gaussian constant (D2), next
   to $L_n$. $T$, $T_i$ are stages (D1) and sets, with the list $\mathcal T$ (D2). $\phi$ sits beside $\varphi$,
   $\varphi_0$; $r_b(U)$ beside $r_n$, $r^\circ_n$; $d(S)$ beside $d_n$, $d_H$. Rename on the D1 side.
5. **Vocabulary.** D1 says "reports", D2 and A2 "printed estimates"; "the method", "the software" and "the code"
   alternate. One glossary pass before drafting.
6. **§2 against §3.1.** Keep §2 statistical (data, model (1), designs, standardisation). D1 §1's code-level notes
   (two-pass centring, the $10^{-10}$ duplicate rule, input validity) belong in §3 or Appendix B.

Mechanical: "the companion section", "Assumptions §x" and "methodology section, eq. (6)" all become `\ref`.

## (b) The four questions
1. **Results before assumptions, as planned.** The assumptions argument is comparative: one table, three design
   classes, shared assumptions. Splitting it by theorem scatters all three. Put only one thing next to each theorem:
   a one-line "Scope" (which design classes are inside), pointing to §5.4.
2. **In §4, as its first subsection.** §2 also serves §3, which needs no statistical assumption. (FS$_\theta$), (V)
   and (NL) stay with Results 3 and 4.
3. **No: move Algorithm 1 to the supplement.** Every theorem holds for every outcome of the calibration. The main
   text needs three facts: it is frozen before the final run; it is a function of the data and its own random
   numbers; and what "succeeds" means. That is five lines, and it is the main lever on §3's budget.
4. **Title.** The current one has 20 words, and "as coded" reads oddly in a title. Suggest "Consistency of a
   sequential Monte Carlo method for Bayesian variable selection, as implemented". Keep "as coded" for §3's heading.

## (c) Budget: my estimate is about 27 pp against 25
- **Overruns:** §3 at 8–8.5 pp against 6.5 (D1 §2–§5 is 12 pp and its table 3 pp; the sampler and the calibration
  alone are 4 pp); §4 at 9.3 against 9; §2 at 1.7 against 1.5.
- **Decide first** whether the 25 pages are counted with the status boxes on; off, §4 is about 0.8 page shorter.
- **Cuts, in order:**
  1. D1 §5.5 (calibration): Algorithm 1 and the tier and trigger detail to the supplement (−0.8).
  2. D1 §5.4: the three moves in four lines; acceptance rules to the supplement (−0.4).
  3. D1 §5.7: diagnostics, the evidence lower bound, the near-tie window and the list of stops to Appendix B (−0.5).
  4. D1 §5.1 and the compact table: keep only the parameters a theorem uses or a reader must know, about 12 rows.
  5. A2 §3 restates (V), (NL) and the leakage set inside its "Evidence" lines; §4 now defines them (−0.3).
  6. D1's $p=3$ prior example in two lines.
- **Do not cut** D1's six-predictor leakage example: it is the most concrete thing in the paper (see (d)3).

## (d) Repetition the outline does not mark
1. **Scope of Results 3 and 4** (which designs are inside, what still holds) appears in D2 Table 1, D2 §6.2, D2
   Remark 5.4(iv), A2 §1 ¶2, A2 §3.3, A2 §3.4, and the planned §6. One home, §5.4; two lines and a pointer elsewhere.
   §6 then holds only what does not depend on the design.
2. **The mechanism** (the start mode holds the true predictors and some leaks; the search deletes them) is told in
   D1 §4, D1's example, D2 Result 3 "In words" and the "why" of D2 Theorem A.9. Tell it once, in §3.3.
3. **Two leakage examples:** D1's six predictors (numbers) and D2's three predictors (covariances). Keep D1's in
   §3 and name its leakage set $Q$ there; in §4.4 keep one sentence on masking. The word "leakage" must mean the
   same in both (my D1 flag of round 3).
4. **Unbiasedness:** D1 §5.7 uses it for the lower bound ("since $\hat Z$ is unbiased") before §4.5 proves it.
   Define the estimator in §3 and state the property in §4.5 only.
5. **Statuses.** They are in the boxes, the table, A2 §4 and the ledger. The outline's §6 adds "the Prop-LB check, the
   T11 premise": internal names, and status content outside the toggle. Keep §6 free of statuses.
6. **Smaller, each to be said once:**
   - the run description (D2 §2.2 and D1 §5.7);
   - valid input and seed (D1 §1.2, the D1 table, (C1), D2 Appendix C);
   - the domain $\mathfrak D$ and the two integer limits (D1 §6, D2 Appendix C, the Result 3 status);
   - Result 5(a), restated as the evidence for sparsity in A2 §3.1;
   - the primitive form of the random-design theorem (D2 after Theorem 3.1, A2 §2);
   - the block cap of 16 (D1, D2 and A2's visibility evidence).

## (e) What the introduction must say in 1.5 pages
1. **The gap, in two sentences.** Theory for Bayesian variable selection covers an exact posterior under priors
   the analyst tunes; users run software with fixed defaults and read its output.
2. **The method, in five lines:** fixed prior, closed-form posterior up to the evidence, a start law from blocks, a
   tempered sampler on four islands, local searches, a reported model; nothing tuned.
3. **The five results as a numbered list,** one sentence each, with its scope in the same sentence: Result 3
   excludes pervasive factors with $p\gg\sqrt n$; Result 4 is unbiased everywhere, consistent only without leakage.
4. **Position against earlier work,** one paragraph. Follow TRACK_B v1.4 on Song and Liang: their statements about
   sampler output are limits in the number of iterations at fixed data; ours hold at the coded budget. The outline's
   "theory usually covers an idealised posterior, not the software" must not say more than that.
5. **The assumptions headline,** one sentence, pointing to §5.
6. **What the paper is not:** no simulation study here (say where it is); no theorem for the parallel engine.
7. **Organisation,** three lines. Leave out statuses, symbols beyond $n$, $p$, $s_0$ and the rate, and "seed-free"
   (write "for every seed").

One gap to raise with HQ: the three sources cite five works in all. A referee will expect the literature on selection
consistency, on MCMC for variable selection, and on sequential Monte Carlo over binary spaces. That paragraph needs a
reference list from the owner; I have not drafted claims about those papers.
