# LC-A — line check of Q1, Q2, Q7 (Sol: codex gpt-6.1-sol, reasoningEffort high; new agent, blind; brief BRIEF_LCA_sol.md). Files checked at the shas in LCA_shas_at_launch.txt. Reply verbatim below (link targets shortened).

**Q1_sandF_c.md: VERIFIED-WITH-AMENDMENTS**

1. **[E] [Q1_sandF_c.md:171]** — The inherited source-comparison paragraph says the proof differs from its sources only in Step 2(b)’s last line and the toolkit input. Step 2(a) now also differs: those sources assume \(M_n\to\infty\), whereas this file supplies a new constant-level argument. **Fix:** explicitly include Step 2(a)’s constant-visibility change in the comparison and mark the amendment [R-#].

The mathematical changes check out. In [R-3], the lower bound is squared only after establishing \(\sqrt{M_V\log n}>\sigma\bar z_n\). Its error is \(o(\log n)\), and the remaining coefficient is strictly positive exactly under the stated \(M_V>M_V^0\). The bounds hold simultaneously for every maximiser. No other proof step needs diverging visibility.

The parent diff confirms that the remaining proof text is unchanged apart from the marked hypothesis, interface, reference and remark changes; the introductory metadata is rewritten.

**Q2_TL_c.md: VERIFIED**

No findings requiring amendment.

All [R-#] changes and §6 check out:

- The implications from (BM-W), (BM-Q♭), and \(d_n^2\le D\log n\) use valid constants.
- The exact deletion/swap identity retains the swap’s subtraction term. (BM-W⁺)(i) gives the first-square bound \(\sigma^2\lambda_n/4\); (ii) makes the residual contrast positive and closes the score margin:
  \[
  \gamma=\frac{\sigma^2(c_{\rm TL}/4-2A-2)}{2C_R}-A-\frac12>0
  \quad\Longleftrightarrow\quad c_{\rm TL}>c_{\rm TL}^0.
  \]
- Toolkit (T4)(b) applies to the resulting positive RSS contrast, including nonnested swap pairs. No use remains of \(\lambda_n/\log n\to\infty\).
- The onset dependencies are permitted by the hypotheses. The lattice toolkit’s growth condition is supplied by the stated (F0)/(P0) assumptions.
- §6 faithfully consumes TH09’s BM(c) branch. Boundedness justifies convergence in expectation; the posterior-majority inclusion and Markov bound prove [MODE]. Conditionality on SOP:TH09 is retained.

The copied §0 and §4 passages agree with the parent outside the identified changes.

**Q7_proxy_d.md: VERIFIED**

No findings requiring amendment.

The residual formula is correct:
\[
(I-P_P)e_1
=\frac{s}{s^2+r^2|P|}
\left(se_1-r\sum_{j\in P}e_j\right).
\]
An outside-\(Q\) swap column is orthogonal to this calculation, so every truth-removal direction has the asserted form.

The pointwise Gaussian bound gives exactly
\[
d_n\le\sqrt{2/\pi}\,\frac{1+r(q-1)}{\sqrt{1-r^2}},
\]
whose right-hand side tends to \(\sqrt{2/\pi}\), since \(rq\to0\).

Part (b) covers every statistical hypothesis of parent RM2-F: energy and beta-min are rechecked; the global Gram floor, feasibility, zero outside leakage and exact localisation remain valid for varying \(\theta_n\). The equivalence for (BM-Q) and the \((\log n)^2/n\) witness are correct.

Part (c)’s strict liminf margin permits fixed \(c>c_0\), \(M_V>M_V^0\), and \(c_{\rm TL}>c_{\rm TL}^0\). Bounded \(d_n\) also supplies (BM-W⁺)(i). No additional signal hypothesis is needed.

Q1 — **VERIFIED-WITH-AMENDMENTS:** one editorial source-comparison correction; proof valid.  
Q2 — **VERIFIED:** constant-level truth removal and posterior/mode bridge valid.  
Q7 — **VERIFIED:** residual formula, width bound, separation witness and both hypothesis checks valid.
