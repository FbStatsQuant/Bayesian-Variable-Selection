# W3-MISR-R — READER_DELTA (draft v0.3, 2026-11-16; v0.3 = council R1 faithfulness fixes [R1]; v0.2 = manager's CP1 wording rules applied; for W3-READER `READER_VERSIONS.md` row "thm4", card row 1.4)

Source read (read only): `/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/READER_VERSIONS.md`, row thm4 (between
`<!-- ROW thm4 BEGIN -->` and `END`), section version 0.2 / update log v0.3 (2026-11-16). This draft proposes the delta;
the manager passes it to HQ for W3-READER. Nothing here is written in W3-READER's folder. Status of every new master:
**not yet checked** (this ticket is at CP1); the row must keep the current masters until W3-MISR-R passes CP3 and HQ
(with the consultant, v4 H5) adopts the change.

## 1. What changes, in plain words

| item | current (thm4 v0.3) | proposed | master |
|---|---|---|---|
| model | rows (x_𝒞, x_𝓜) jointly Gaussian; y = α + x_𝒞ᵀβ_𝒞 + x_𝓜ᵀβ_𝓜 + ε | candidate rows Gaussian; **given the candidates, the responses are independent normal with mean linear in the candidates and constant variance**. Jointly Gaussian omitted predictors become the leading example | `W3-MISR-R:CorGb-plus` (case with no explicit omitted columns) + `W3-MISR-R:CorG-min` (E1), (E2) |
| (A2) floor | λ_min(Σ_TT) ≥ c and max_j Σ_jj ≤ C₀ | λ_min(R_TT) ≥ c for the **correlation** matrix R; no variance bound | `CorGb-plus` |
| (A3) beta-min | → ∞ | unchanged in the reader text (the liminf form goes to a remark) | `CorGb-plus` |
| conclusion | E[1 − π] = O(√(log n/n)), P(HPM ≠ S₀^𝒞) = O(√(log n/n)) | unchanged | — |
| remark | "a Hellinger version exists" | Hellinger and Kullback–Leibler in-sample versions whenever the posterior selects the support with probability → 1; uniform over configurations; random designs by conditioning | `CorH-plus`, `CorH-U` |

Classification: STRONGER (weaker hypotheses, same conclusion). The headline masters MIS(i), (i′), (ii) are unchanged.

## 2. Proposed reader statement (replaces "### Reader statement" of row thm4)

**Theorem 4** (fitting the candidates only, with predictors missing). The method is run on the candidate predictors
$x_{\mathcal C}$ and the response $y^{\mathrm r}$ only ($p$ = number of candidates). Assume:
- **(A0) Model.** The candidate rows $x_{\mathcal C,1},\dots,x_{\mathcal C,n}$ are i.i.d. $N_p(m,\Sigma)$, and, given the
  candidate design, the responses are independent with
  $y^{\mathrm r}_i\mid x_{\mathcal C}\sim N\big(\alpha'+x_{\mathcal C,i}^\top\beta^{\mathcal C},\ \sigma^2_{\mathcal C}\big)$, $\sigma^2_{\mathcal C}>0$.
  Write $S_0^{\mathcal C}:=\operatorname{supp}\beta^{\mathcal C}$ and $s:=|S_0^{\mathcal C}|$.
- **(A1) Dimension and sparsity.** $2\le p\le n^A$; $s\ge1$ fixed.
- **(A2) Floor.** With $R$ the correlation matrix of a candidate row, $\lambda_{\min}(R_{TT})\ge c$ for every
  $T\subseteq\mathcal C$ with $|T|\le 3(A+1)(s+1)\log n$, for a fixed $c>0$.
- **(A3) Signal relative to the residual variance.**
  $\beta^{\mathcal C\top}\Sigma\beta^{\mathcal C}\le M_0\,\sigma^2_{\mathcal C}$ and
  $n\min_{j\in S_0^{\mathcal C}}\Sigma_{jj}(\beta^{\mathcal C}_j)^2/(\sigma^2_{\mathcal C}\log n)\to\infty$.

No condition is placed on how $m$, $\Sigma$, $\beta^{\mathcal C}$ or $\sigma^2_{\mathcal C}$ vary with $n$. Then
$$
E\big[1-\pi(S_0^{\mathcal C}\mid y)\big]=O\Big(\sqrt{\tfrac{\log n}{n}}\Big),\qquad
P\big(\mathrm{HPM}\neq S_0^{\mathcal C}\big)=O\Big(\sqrt{\tfrac{\log n}{n}}\Big).
$$
*Example (omitted predictors).* If the rows $(x_{\mathcal C,i},x_{\mathcal M,i})$ are i.i.d. Gaussian with
$\Sigma_{\mathcal C\mathcal C}$ invertible and
$y^{\mathrm r}_i=\alpha+x_{\mathcal C,i}^\top\beta_{\mathcal C}+x_{\mathcal M,i}^\top\beta_{\mathcal M}+\varepsilon_i$ with
$\varepsilon\sim N_n(0,\sigma^2I)$ independent of the rows, then (A0) holds with
$\beta^{\mathcal C}=\beta_{\mathcal C}+\Sigma_{\mathcal C\mathcal C}^{-1}\Sigma_{\mathcal C\mathcal M}\beta_{\mathcal M}$ and
$\sigma^2_{\mathcal C}=\sigma^2+\beta_{\mathcal M}^\top(\Sigma_{\mathcal M\mathcal M}-\Sigma_{\mathcal M\mathcal C}\Sigma_{\mathcal C\mathcal C}^{-1}\Sigma_{\mathcal C\mathcal M})\beta_{\mathcal M}$.
(If $\Sigma_{\mathcal C\mathcal C}$ is singular, the same holds with its Moore–Penrose inverse in place of the inverse.)
The same holds when the omitted predictors are a linear function of the candidates plus Gaussian noise whose rows are
i.i.d. and independent of the candidates.
*Remark.* The law in (A0) is the conditional law of $y$ given the candidates, hence the Kullback–Leibler projection of
the truth onto the candidate linear models: the posterior concentrates on the support of the best candidate
predictor. Under the same assumptions the posterior's fitted mean and variance also contract around this law, with its
mean centred over the sample (the fitted mean carries no intercept), in the in-sample average Hellinger and
Kullback–Leibler distances, at rate $M_n/\sqrt n$ in Hellinger and $M_n/n$ in Kullback–Leibler (any $M_n\to\infty$).
For a fixed design the contraction needs only that the posterior mass of $S_0^{\mathcal C}$ tends to one in probability
(with the energy bound and a floor on $S_0^{\mathcal C}$); it holds uniformly over any class of fixed-design configurations with
common constants and bounded support size on which this convergence is uniform. A fixed-design version of the theorem, uniform
over the residual variance, also holds (remarks in the paper; same status).

## 3. "Why each assumption" (replaces the row's list)
- (A0) is a convenient sufficient form. The proof uses only a weaker condition: given the candidates, the coordinates of
  the residual vector $y^{\mathrm r}-\alpha'1-x_{\mathcal C}\beta^{\mathcal C}$ in an orthonormal basis of the vectors
  orthogonal to the constant vector are i.i.d. Gaussian with a common variance (nothing is required of the residual's
  sample mean). When the noise is Gaussian and independent of all predictors, this holds if and only if the omitted part
  has the same property given the candidates. (A0) covers omitted Gaussian predictors and omitted predictors that are
  linear in the candidates plus Gaussian noise. The Gaussian law of the candidate rows is an assumption on how the data
  are generated (not a choice of design); it is used only to transfer the population floor (A2) and (A3) to the sample.
- (A1) as Theorem 1.
- (A2) The method standardises each column, so only correlations matter; the floor is on the candidates only.
- (A3) Everything is measured relative to $\sigma^2_{\mathcal C}$ because the method is invariant to shifts and rescaling of
  $y$. The energy bound cannot simply be dropped (numerical evidence); the beta-min order is that of Theorem 1
  (a liminf condition at a fixed constant suffices; remark).

## 4. Bridges (replace the row's table)

| # | bridge | mark | detail |
|---|---|---|---|
| B4.0 | (A0) ⇒ CorGb-plus setting | NEW (one line) | take no explicit omitted columns, ε := y^r − α′1 − X_𝒞β^𝒞: given X_𝒞 it is N_n(0, σ²_𝒞I), hence independent of X_𝒞 ((N) with q = 0; (OV) with γ = 0, τ² = 0). The Example is `CorG-min` (E1) (and (E2) for the linear-plus-noise sentence) |
| B4.1 | (A2) size 3(A+1)(s+1)log n ⇒ CorGb-plus's \|T\| ≤ s + max(j₀, m♯_n), for all large n | NEW arithmetic (as current B4.1) | unchanged arithmetic; the floor is now on R; sufficient for the O(·) conclusions |
| B4.2 | (A3) = CorGb-plus's signal conditions (→ ∞ branch of its liminf condition) | identity | `STATEMENT.md` §3 |
| B4.3 | POST2 C, E, A1, A0 (and D for the remark) | EXISTS-UNCHECKED (unchanged) | as the current row |
| B4.4 | Remark ⇒ CorH-U (RD) with 𝒦^♭_n := 𝒦^λ_n(s, A, 2M₀+1, (c_R/8)^{1/2}, C_OS, c) ((UP) by MIS(i) + Markov) and the events 𝒜_n of CorGb-plus's proof (P(𝒜_n) → 1); contraction sentence for a fixed design ⇒ CorH-plus (a′), (KL), with the premise δ_n → 0 in probability; uniform sentence ⇒ CorH-U (U-a), with its premise (UP); "fixed-design version of the theorem, uniform over the residual variance" ⇒ W3-MISR:MIS(i)@1.0.0 (BASE `STATEMENT.md:110-114`, constants free of v) | NEW (composition; the random-design part is `CorH-U` clause (G), STATEMENT §5) | the Hellinger rate M_n/√n and KL rate M_n/n are the sets H^a, K^a; the reference is centred (STATEMENT §1: μ(κ) = Cxβ) [R1] |

## 5. Master-theorem paragraph (delta)
Replace "`W3-MISR:Cor-G(b)@1.0.0` … status verbatim" by `W3-MISR-R:CorGb-plus` (with `W3-MISR-R:CorG-min` for the
Example) once registered, with their CP3 statuses verbatim, and add `W3-MISR-R:CorH-plus`, `W3-MISR-R:CorH-U` for the
remark. Until then the row keeps its current masters and statuses; this delta is a proposal.

## 6. Errata absorbed
W3-EDIT LEDGER I4-F2 (full status quotes of SOP:TH09, SOP:TH128) is absorbed in this ticket's `STATEMENT.md` §7. No
other routed erratum is restated by this delta (I4-F1, I4-F4 concern BASE §3(a) and the BASE changelog).

## 7. Wording rules applied (manager, CP1 answer)
Asymptotics are stated as what is proved, never as a limitation; no displayed numerical constant beyond the theorem's own
(the liminf constant of the master stays in the master); the Gaussian law of the candidate rows is stated as an assumption
on the data's law, not as a design family. The parity line "short vs SL Thm 4 in metric and mode" stays in TARGET/REPORT only.
