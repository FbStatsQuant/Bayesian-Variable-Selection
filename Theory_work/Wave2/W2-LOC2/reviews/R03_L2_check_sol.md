VERIFIED-WITH-AMENDMENTS

1. **MAJOR — The lemma file strengthens locked (R2); remove the extra assumption by adapting the atom-tail threshold.** `L2_NAR.md:34` assumes
   \[
   L_n^2\{\log(|\mathcal A_n|+1)+\log\log n\}=o(\log n),
   \]
   whereas locked `STATEMENT.md:52–53` assumes only \(L_n^2\log(|\mathcal A_n|+1)=o(\log n)\). Consequently, lines 76–80 and 98 do not, as written, prove the entire locked claim. The additional condition is a genuine strengthening: for a fixed nonempty atom family, \(L_n^2=\log n/\log\log n\) satisfies the locked condition and fails the displayed condition. Cancelling atom representations are allowed, so the other assumptions do not exclude such coefficient norms.

   **Concrete fix, preserving the locked statement:** write \(M_n=|\mathcal A_n|\) and choose the deterministic sequence
   \[
   b_n=\sqrt{\frac{\log n}{1+L_n^2}},\qquad
   y_n^2=2\log\{2(M_n+1)\}+2b_n.
   \]
   If \(M_n\ge1\), locked (R2) implies \(L_n^2=o(\log n)\); if \(M_n=0\), then \(L_n=0\). Thus \(b_n\to\infty\), and
   \[
   \frac{L_n^2b_n}{\log n}
   =\frac{L_n^2}{\sqrt{1+L_n^2}\sqrt{\log n}}
   \le \frac{L_n}{\sqrt{\log n}}\longrightarrow0.
   \]
   The existing conditional-on-\(\varepsilon\) union bound becomes
   \[
   \Pr\!\left(\exists a:\ |(C\mathcal Wa)^\top\varepsilon|>
          y_n\|C\varepsilon\|\mid\varepsilon\right)
   \le\frac{M_n}{M_n+1}e^{-b_n}\le e^{-b_n}=o(1).
   \]
   Also \(L_n^2\log\{2(M_n+1)\}=o(\log n)\), including the empty-family case, so \(L_n^2y_n^2=o(\log n)\). Replace (R2) in the lemma file by locked (R2), make these substitutions in \(E_e\) and Step 5, and keep every other atom estimate unchanged. This supplies the missing implication without changing claim (B).

2. **MINOR — Step 5 repeatedly asserts equalities where (R1) supplies only upper bounds.** At lines 97, 99 and 100, the claims \(x'_n=2\log p+o(\log n)\), \(\zeta_n^2=2\log p+o(\log n)\), and the corresponding equality for the sample envelope are not justified. (R1) is one-sided. For example, take \(p=n\), \(Q=S_0=\{1\}\), let \(W_1\) be independent of a standard Gaussian column \(V\), and let every \(W_l\), \(l\ge2\), equal \(V\). Every required population submatrix has floor 1, all residuals equal \(V\), one singleton frame suffices, and no atoms are needed. Then \(N_n=1\) and \(x'_n=3\log\log n\), which is not \(2\log p+o(\log n)\). Global nonsingularity outside \(Q\cup\{l\}\) is not required by (B).

   **Concrete fix:** replace those equalities by upper bounds. Using either the lemma file's stronger (R2), or the repaired threshold in finding 1,
   \[
   x'_n\le2\log p+o(\log n),\quad x'_n=O(\log n),\quad
   B_n:=L_ny_n\sqrt{4/c}=o(\sqrt{\log n}).
   \]
   Since \(\eta'_n\to0\), the exact expansion of
   \(\zeta_n=\sqrt{(1+\eta'_n)x'_n}+B_n\) gives
   \[
   \zeta_n^2\le2\log p+o(\log n),\qquad \zeta_n^2=O(\log n).
   \]
   In Step 4, \(\omega'_n\to0\) and \(\epsilon_n\to0\). Therefore the exact expansion
   \[
   \{(1+\omega'_n)\zeta_n+\epsilon_n\}^2
   =\zeta_n^2+(2\omega'_n+(\omega'_n)^2)\zeta_n^2
    +2(1+\omega'_n)\zeta_n\epsilon_n+\epsilon_n^2
   \le2\log p+o(\log n)
   \]
   is a deterministic uniform upper bound on the common event. Meanwhile the threshold calculation at line 101 is correct:
   \[
   c_n-2\log p
   \ge\log n-2\log\{(\log n)^\kappa+1\}-4\kappa_E-2
   =\log n-O(\log\log n).
   \]
   The resulting gap is \(\log n-o(\log n)-O(\log\log n)>0\). Thus the needed uniform inequality really follows after the repairs; no two-sided asymptotic for the envelope or maximum is necessary.

3. **NIT — Correct the rate descriptions and constant dependencies.** Line 105's \(x\asymp\log|\mathfrak P|\) need not hold: \(x=\log|\mathfrak P|+2\log n\), even when the pair family has bounded size. Moreover, \(E_b\)'s threshold enters the additive Step 4 error, not only the relative errors claimed in lines 105–106. The condition \(\log|\mathfrak P|=o(n)\) alone would not control that additive error in a proposed extension beyond the polylogarithmic regime.

   **Concrete fix:** record
   \[
   x,v_n=O(q+\log n),\quad
   \delta_n=O\!\left(\sqrt{\frac{q+\log n}{n}}+\frac{q+\log n}{n}\right),\quad
   \omega'_n=O\!\left(\frac{q+\log n}{n}\right),\quad
   \epsilon_n=O\!\left(\frac{q+\log n}{\sqrt n}\right).
   \]
   These give the stated conclusions for every fixed polylogarithmic exponent. Either explicitly inherit \(\kappa\ge1\) from `L1_toolkit.md`, or replace the shorthand exponents in lines 59, 92 and 95 by \(\max(1,\kappa)\). Restrict the remark about harmless lattice unions to the actual polylogarithmic setting, or separately state the necessary comparison-error condition. Finally, add the fixed score constant \(\kappa_E\) to the list of dependencies of \(n_0\) at lines 47–48: the final threshold comparison necessarily depends on it. None of these corrections changes the asymptotic claim.

The remaining requested line-by-line checks yielded no additional defects:

- **Step 1, lines 51–57:** (N1) gives positive definiteness on \(T\cup\{l\}\); since \(|T|+1\le q+1=o(n)\), centering leaves enough dimensions for full column rank almost surely. The finite union over all pairs preserves this probability-one statement. The positive sample scale \(t_l\) cancels from the normalized direction. Both \(P_TC=P_T\) and \(CP_T=P_T\) hold. Therefore \(h=g-P_Te\), \(h\perp P_Te\), \(\|h\|^2=\|g\|^2-\|P_Te\|^2\), and equation (2.1), including its minus sign and denominator \(\|h\|\), are exact. Projecting the second noise factor to \(P_T\varepsilon\) is legitimate because \(P_Te\) lies in that projection's range.

- **\(E_a\), lines 60–63:** every residual and reference has iid centered Gaussian entries because its row functional and coefficients are deterministic. For positive variance, centering gives a \(\chi^2_N\) squared norm. Zero-variance references vanish almost surely. The common \(\delta_n\) covers both residual tails and the reference upper tail. There are at most \(3|\mathfrak P|\) one-sided events, so the stated \(3n^{-2}\) failure bound is valid even for a quasi-polynomial pair family. No independence between pairs is needed.

- **\(E_b\) and \(E_c\), lines 64–70:** rowwise Gaussian regression gives \(\operatorname{Cov}(e_{T,l,i},W_{iT})=0\). Joint Gaussianity and independent rows then give independence of the entire vector \(e_{T,l}\) from the entire matrix \(W_T\). Sample scaling does not spoil this: \(P_T\) is measurable with respect to \(W_T\) alone. Consequently, conditional on \(W_T\), \(\|P_Te\|^2/\tau^2\sim\chi^2_{\operatorname{rank}P_T}\). The mgf at \(1/4\) yields \(2^{d/2}e^{-v/4}\); at the displayed \(v_n\), the pair union costs at most \(n^{-2}\). Conditional on \(X\), the analogous noise law for \(P_Q\) holds, and its failure probability is at most \(2^{q/2}e^{-q}n^{-1}\le n^{-1}\). Nested projection ranges give \(\|P_T\varepsilon\|\le\|P_Q\varepsilon\|\). The proof never conditions on all of \(W\) when claiming the regression-residual chi-square law.

- **\(E_d\), lines 71–75:** the sample subspace of a frame is measurable with respect to the full extension, which is independent of \(\varepsilon\). Conditional on that extension, the projection statistic is chi-square with its actual rank, bounded by \(m_0\), even if the frame is internally dependent or degenerate. For fixed positive \(m_0\), optimizing the chi-square Chernoff bound gives \((ex/m_0)^{m_0/2}e^{-x/2}\). With \(x=x'_n\), the \(N_n\) factor cancels exactly, and \(x'_n=O(\log n)\) gives \(O((\log n)^{-1})\). The threshold diverges even if \(N_n\) is bounded. Controlling each entire subspace correctly covers every allowed linear combination; there is no missing union over directions. A dimension bound of zero is a trivial all-zero-frame case and can instead be enlarged to one.

- **\(E_e\), lines 76–80:** conditional on \(\varepsilon\), each atom inner product is Gaussian with variance \(\operatorname{Var}(a)\|C\varepsilon\|^2\). This uses independence of the entire extension from the entire noise vector, which is expressly assumed. Correlations among atoms do not affect the union bound. The original \(1/\log n\) atom-tail bound is valid under the stronger hypothesis in the lemma file; finding 1 gives the replacement for locked (B). The noise-norm tail is also correct: Laurent–Massart at \(N/8\) has threshold \(N+N/\sqrt2+N/4<2N\), hence \(\Pr(\chi^2_N>2N)\le e^{-N/8}\). No atom-norm concentration or missing factor of \(\sigma\) is involved.

- **Steps 3–4, lines 83–95:** the decomposition uses an absolute-value triangle inequality, so signs of coefficients are unrestricted. Reference membership in the sample frame subspace gives the first Cauchy–Schwarz bound. Dividing by \(\sigma\|g\|\) gives exactly the reference norm ratio and atom constant \(\sqrt{4/c}\): the atom numerator is at most \(\sigma L_ny_n\sqrt{2N}\), while \(\|g\|\ge\sqrt{cN/2}\). In Step 4 the correct multiplicative factor is \(\|g\|/\|h\|\ge1\), as written. The ratio bound follows from \(\|P_Te\|^2/\|g\|^2\le v_n/[N(1-\delta_n)]\). In the additive term, the factors \(\sigma\) and \(\tau\) cancel, leaving exactly \(2\sqrt2\sqrt{v_n(q+\log n)/N}\). This vanishes uniformly for polylogarithmic \(q\). No assumption \(\tau\le1\) is needed for this cancellation.

- **Probability mode and the NA implication:** the estimates prove the asserted joint design/noise limit. The frame tail is uniform conditional on the full extension; the atom tail is obtained by conditioning on noise and integrating. A uniform guarantee for every realized design is not established or required. Interpret Remark 3 accordingly. Intersecting with the lattice toolkit event needs no independence. In the stated setting, the inherited unit diagonal and population floor give the sample Gram floor through `L1_toolkit.md` §L1.2; fixed truth size and bounded coefficients give a deterministic \(O(n)\) signal-energy bound for the standardized design. The enlarged toolkit rates make the likelihood approximation error \(O(\log n)[O(n^{-1/3}+(\log n)^{\kappa_*}/n)+O(\log n/n)]\) vanish, with fixed \(\kappa_*\). Thus the cited GROW L2.2 reduction retains the same \(c_n\); the additional lattice union does not consume the available \(\log n\) slack.

- **Usability in the cited applications:** `L4_LOCd.md` §A.5 supplies deterministic singleton reference frames, \(\log N_n\le\log p+O((\log\log n)^d)\), coordinate atoms of variance one, bounded \(L_n\), and a variance excess tending to zero through the cited TAIL result. Section B.2 supplies deterministic two-member latent frames, \(\log N_n\le\log p+O(1)\), variance-one atoms, and \(L_n\le1/b_{\rm lo}\); its \((F_G,\xi_l)\) reference is independent of the contributing \(\xi_v\), so \(\tau^2=\varrho^2+\sum_v\lambda_v^2\) and (R3) holds with zero excess. The stated latent construction has the required joint Gaussian iid-row law and noise independence. Both applications even satisfy the stronger displayed atom condition, so finding 1 affects coverage of the locked general lemma rather than those two applications. This checks their compatibility with NA-R, without independently re-proving their population inputs.

No FATAL defect or counterexample to locked claim (B) was found. The adaptive-threshold repair in finding 1 and the one-sided Step 5 repair in finding 2 give a complete proof under the locked hypotheses.
