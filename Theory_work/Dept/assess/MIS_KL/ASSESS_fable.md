# ASSESS (Fable 5.2) — Song–Liang-type misspecification (KL projection): should we pursue it, and is it feasible?

Assessment only. The targets in item 2 are unproved candidates, and everything marked *heuristic* is my own unchecked derivation. Literature beyond the local files is cited from memory and needs a citation check. Page 957 was also read as an image (scratch file `out_fable/scratch_p957-11.png`). The snapshot's registry files carry no W3 rows; statuses were read from the STATEMENT files.

## 1. Value

**What SL's Theorem 4 says on the page.** Their truth is still their model (2), $f^*(y,x)=\phi(y;x^\top\beta^*,\sigma^*)\,\nu_x(dx)$: Gaussian noise, linear in all $P_n$ predictors, covariates of any law. The misspecification is omitted predictors only. Condition 4 is finite second moments of $x_s$. The subset size is fixed, the conclusion is almost-sure Hellinger consistency at $f_0$ with no rate, and Corollary 2 gives inclusion $\tilde s\subset\xi$ only. So "arbitrary $f^*$" in the brief is more than the main text states. But since $\nu_x$ is arbitrary, the residual given $x_s$ can be non-Gaussian, heteroscedastic and non-linear in mean.
**Limit.** Without the supplement I cannot check whether the proof uses the Gaussian $\varepsilon$, nor which De Blasi–Walker conditions it verifies (`H3_songliang_notes.md` G1, H5 record only that it uses them and that $s$ is fixed).

**Does it say more than ours?** In one respect, yes, and a reader will care: it does not need (OV^c). (OV^c) asks that the omitted part, given the candidates, be linear plus Gaussian with scalar covariance. This fails for binary or heavy-tailed omitted covariates, the usual case. CorG-min (c) proves (OV^c) necessary only for our exact law reduction, not for the conclusion (`W3-MISR-R/TARGET.md:38-39`). In every other respect ours is stronger: exact support, rate, $p\le n^A$, uniform classes, the shipped prior.

**Level: a supplement result, not a headline.** At fixed $p$ the statement is classical in kind (Berk 1966; Sin–White 1996; Kleijn–van der Vaart 2012; Rossell–Rubio 2018), so it carries no novelty claim. Its use is to close `SONG_LIANG_MAP.md` rows 10–11 ("compared not exceeded"). A referee who knows SL, or Rossell (2022), which I recall treats misspecified truths at growing $p$, will ask whether Gaussianity of the omitted part is needed. Item 3 gives a two-part answer worth printing.

## 2. Target statement

Setting **(P)**: rows $(x_i,y_i)$ iid from a fixed law $P^*$ on $\mathbb R^p\times\mathbb R$, $\Sigma=\mathrm{Var}(x)\succ0$, $\beta^0=\Sigma^{-1}\mathrm{Cov}(x,y)$, $\alpha^0=Ey-Ex^\top\beta^0$, $r=y-\alpha^0-x^\top\beta^0$, $v=Er^2>0$, $S_0=\operatorname{supp}\beta^0$ (SL's $\tilde s$), $f_0=\nu_x(dx)\,\phi(y;\alpha^0+x^\top\beta^0,v)$.

**Target A (fixed $p$; recommended).** Under (P) with $p$ fixed, $E[\|x\|^2r^2]<\infty$ and $Er^4<\infty$, for the coded posterior:
$$1-\pi(S_0\mid D_n)=O_P(n^{-1/2}),\qquad P(\mathrm{HPM}=\mathrm{MPM}=S_0)\to1,\qquad \max_j|\mathrm{PIP}_j-1\{j\in S_0\}|=O_P(n^{-1/2}),$$
$$\Pi\big(d_H(f_{S,\theta,v'},f_0)>M_nn^{-1/2}\ \text{or}\ \mathrm{KL}(f_0\,\|\,f_{S,\theta,v'})>M_n/n\ \big|\ D_n\big)\to0\ \text{in probability, for every }M_n\to\infty,$$
and $f_0$ is the Kullback–Leibler projection of $P^*$ whenever that divergence is finite for some member of the family. No Gaussianity, no linear conditional mean, no homoscedasticity.

**Target N (boundary at growing $p$; recommended).** Fixed design, $y^r=\alpha1+x\beta+\varepsilon$, $\varepsilon\sim N_n(0,\mathrm{diag}(v_i))$, all design hypotheses of MIS-R (i) in force. For a null column put $\rho_j=\sum_i\tilde x_{ij}^2v_i\big/\big(\bar v\sum_i\tilde x_{ij}^2\big)$, with $\tilde x_j$ the part of $x_j$ orthogonal to $x_{S_0}$ and $\bar v$ the mean variance. If $p=n^{A'}$ and $p^{1-o(1)}$ mutually orthogonal null columns have $\rho_j\ge\rho>1+1/(2A')$, then $\pi(S_0\mid x,y^r)\to0$ in probability. So the scalar covariance in (GR^c) cannot be dropped at polynomial $p$.

**Target B (growing $p$, non-Gaussian residual; not recommended).** MIS-R (i) with independent residuals of variance $v$ and sub-Gaussian proxy $K^2v$: $1-\pi(S_0)\to0$ in probability when $K^2<1+1/(2A)$, at a slower rate.

**What we give up.** A gives up $p\le n^A$, the expectation rate and the uniform class (since $E\,e^{\rho\chi^2_1/2}=\infty$ for $\rho\ge1$); it keeps exactness, the coded prior and a rate. B would give up arbitrary $A$ or the coded prior (a stronger size penalty or a size cap), and the expectation rate.

## 3. Feasibility, given the theory we have

**Carries over unchanged (deterministic or law-free).**
- Lemma R′(a), (a′), (a″) and the projective form in (c) (`W3-MISR/lemmas/R_reduction.md` R.0–R.3, R.5): the posterior depends on $y^r$ only through two quadratic forms of the standardised response, so a random intercept and an unknown scale are harmless for selection.
- `M_misr.md` M.1 consequences (1a)–(2c) and input (I6); [POST2] Claim A2; `D_hellinger.md` D0, D1; the (KL) identity (`H1_plus.md` H1.3).
- W3-DIST Lemma H and Lemma T (distribution-free transfer to the joint distance). They compare a posterior draw with $f_0$, both in the Gaussian family, so $f^*$ never enters.
- The pattern of D(a) and CorH-plus (a′): once $\delta_n\to0$, it uses only $O_P$ bounds on $\|P_{S_0}e\|^2$, $\|e\|^2$ and one cross term, which Chebyshev gives under moments.

**Breaks.**
- R′(b), hence display (M0) in `M_misr.md` and (T1), (T2) in `H1_plus.md`. The total-variation term of R′(c) does not vanish for iid non-Gaussian residuals (`W3-MISR/STATEMENT.md:105-106`).
- The size tail: [P1] `thm:Ta`, `lem:num` use $E[m(S)/f_0]=1$ under the true Gaussian density (`C_expectation.md` Lemmas C1–C2, Claim B, W3-DIST Lemma S). For $f^*$ outside the family this expectation can grow exponentially in $n$. This is the non-convexity problem of Kleijn–van der Vaart (2006).
- Exact $\chi^2$ laws: (G3′) (`A_occam.md:46-50`), the truncated moments behind the weights $a_J$ in (OS), and the Gaussian linear forms of `E_visibility.md` Lemma E1(a).
- The conditioning of MIS-R (ii) and CorH-U (RD) needs a mean-zero residual given $\mathcal F_n$. A non-linear $E[y\mid x_{\mathcal C}]$ breaks it; one must then work with the joint law of rows.
- The row-wise KL reading stays restricted to a deterministic intercept ([L1-1]).

**Main obstacle (*heuristic*): the coded prior has no slack.** Adding one null column $j$ to $S_0$ multiplies the posterior odds by about $\frac{s+1}{2p}(n+1)^{-1/2}\exp(\rho_jZ_j^2/2)$, $Z_j\approx N(0,1)$, where $\rho_j=E[\tilde x_j^2r^2]/(E\tilde x_j^2\,Er^2)$ is the sandwich ratio, equal to 1 under (GR^c). Summed over $p$ nulls this is of order $p^{\bar\rho-1}n^{-1/2}=n^{A(\bar\rho-1)-1/2}$. At fixed $p$ it always vanishes. At $p=n^A$ it vanishes only if $\bar\rho<1+1/(2A)$. Example: elliptical (multivariate-$t_\nu$) rows keep the conditional mean linear but give $\bar\rho$ up to $(\nu-2)/(\nu-4)$. Our numerics agree: heteroscedastic residual, $\delta/r_n$ = 1.46, 1.71, 2.04, 2.59, "the rate looks lost" (`W3-MISR/ASSUMPTION_MAP.md:15`, N3(ii)); at fixed $p$ a non-linear conditional mean still converges to the best-linear-predictor support (`W3-MISR-R/TARGET.md:34-39`). So at growing $p$ the phenomenon changes, not only the proof.

**Known routes.** De Blasi–Walker (as I recall it: iid data, a fixed data-free prior, consistency only) and Kleijn–van der Vaart do not fit the coded prior: it depends on the data, and `W3-DIST/ROUTES.md` §1 shows the sieve route fails for it. Target A needs neither: closed-form marginal likelihoods over $2^p$ models, the law of large numbers and the central limit theorem. For Target B, the Hsu–Kakade–Zhang quadratic-form inequality gives every $\chi^2$ tail with the proxy in place of $v$, which loses the factor $p^{K^2-1}$, and the size tail still needs a new argument.

## 4. Cost and risk

- **A + N:** one Tier B rider on W3-MISR-R, NORMAL mode. Three key lemmas: (1) Bayes factors over a finite model set under moments; (2) contraction given selection plus the joint-distance transfer; (3) the heteroscedastic counterexample. About 1.5–2 lead-weeks including statement lock and council. Risk: low for (1)–(2); medium for (3), which needs a design that meets (F₀), (OS) and the margin while violating only scalar covariance. Cheapest version worth doing: A alone, about 1 lead-week.
- **B or a full growing-$p$ KL theorem:** Tier A. It replaces A:GAUSS-NOISE along the whole chain ([P1] size tail, [P3] `lem:chi`, (G3′), Lemma E1, Claims B and C, Lemma S): at least 6–8 key lemmas, 6–10 lead-weeks. High risk of a weak result, because the honest statement restricts $A$ or changes the prior.

## 5. Recommendation

Pursue a narrow version: Targets A and N as one rider after the break. A covers SL's own regime (fixed subset size, iid rows) with weaker assumptions on the truth and stronger conclusions, except the almost-sure mode. N turns the non-claim of `W3-MISR/STATEMENT.md:259` into a stated boundary. Do not pursue Target B or a growing-$p$ KL theorem for the coded prior: the obstacle is the prior's calibration to Gaussian tails, and the cost is that of a new main theorem.

VERDICT: pursue a narrow version — a fixed-p theorem for arbitrary truths plus a heteroscedastic counterexample at growing p closes the gap with Song–Liang's Theorem 4 in about two lead-weeks, while a growing-p version is expected (heuristic, backed by our N3 numerics) to fail for the coded prior once the sandwich ratio exceeds 1 + 1/(2A).
