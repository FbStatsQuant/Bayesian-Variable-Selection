# W3-D2 — READER_DELTA (draft v0.1, 2026-11-17; for the manager → HQ → W3-READER; read-only source [RV] row thm2)

**Current reader version:** `READER_VERSIONS.md:263-282` (Theorem 2, row 1.2, section v0.4 + FRZ-B).

**What changes (as an added statement; see the HQ decision at the foot).** (A3) is asked on sets of size 3(A+1)(s₀+1) log n (was 5(A+1)(s₀+1) log n); Σ_n need not be a
correlation matrix (floor on its correlation matrix); σ², Σ, β may vary with n, measured relative to σ²; the
conclusions are in expectation. Tag: STRONGER (statement); status becomes conditional (see STATEMENT §7).

**New text (proposal).**
> **Theorem 2.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m,\Sigma)$ with $\Sigma_{jj}>0$, and let $R$ be the
> correlation matrix of a row. Assume (S1) with $\sigma^2>0$ allowed to depend on $n$ [R1-opus-E6] and
> - **(A1) Dimension and sparsity.** $2\le p\le n^A$; $s_0\ge1$ fixed.
> - **(A2) Sparse eigenvalue floor.** $\lambda_{\min}(R_{TT})\ge c$ for every $T$ with $1\le|T|\le3(A+1)(s_0+1)\log n$, for a fixed $c>0$.
> - **(A3) Signal relative to the noise.** $\beta^\top\Sigma\beta\le M_0\sigma^2$ and $n\min_{j\in S_0}\Sigma_{jj}\beta_j^2/(\sigma^2\log n)\to\infty$.
>
> No condition is placed on how $m$, $\Sigma$, $\beta$ or $\sigma^2$ vary with $n$. Then
> $$E\big[1-\pi(S_0\mid y)\big]=O\Big(\sqrt{\tfrac{\log n}{n}}\Big),\quad P(\mathrm{HPM}\neq S_0)+P(\mathrm{MPM}\neq S_0)=O\Big(\sqrt{\tfrac{\log n}{n}}\Big),\quad E\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|=O\Big(\sqrt{\tfrac{\log n}{n}}\Big).$$
> *Remarks.* Fixed $\sigma^2$, a correlation matrix $\Sigma$ and $b_{\mathrm{lo}}\le|\beta_j|\le b_{\mathrm{hi}}$ on $S_0$ give (A3)
> with $M_0=s_0^2b_{\mathrm{hi}}^2/\sigma^2$. This is Theorem 4 with no omitted predictors, plus the deterministic PIP/MPM consequences [R1-opus-E7].

**Bridges.** B2.1′ := `W3-D2:Thm2X` (STATEMENT §1; PROOF P1–P2: CorGb-plus with q = 0 + `W3-READER:R1` B4.1);
B2.1″ := `W3-D2:Cor2X` (old hypotheses ⇒ new; PROOF P3). The old B2.1–B2.3 stay for the coexisting O_P master.
**HQ decision (2026-11-17): COEXIST.** Row 1.2's reader statement stays as it is; the text above is not swapped in. It goes
into the paper as an added statement (a corollary or remark under Theorem 2, with its conditional status), card text in
`REPORT.md` §3. The old B2.1–B2.3 stay unchanged.
