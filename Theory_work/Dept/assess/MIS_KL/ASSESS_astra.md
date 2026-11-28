# Assessment: a KL-projection extension of MIS-R

## 1. Value

Pursue a small robustness result for the supplement, with a short main-text summary; it is useful thesis material, not yet a headline. A referee comparing our “misspecification” claim with Song–Liang will reasonably ask about nonlinear omitted effects and non-Gaussian errors. Our present reduction makes the candidate contrast model Gaussian and correctly specified; a population KL projection can remain meaningful when that reduction fails. This is a substantive gap, not merely a weaker rate.

Song–Liang §2.3, Theorem 4 (p. 957), gives qualitative Hellinger consistency at the KL projection; Corollary 2 gives inclusion, not exact selection. Condition 4 is a predictor second-moment condition. However, §2.3 starts from their full linear model (1), and its displayed projection is of the full linear signal. The main paper alone does not justify calling this a theorem for literally every joint law without existence, integrability and identifiability qualifications. The missing supplement prevents checking its De Blasi–Walker application and hidden regularity requirements. Their Discussion (§7) also distinguishes subset posterior inference from full-data inference. Neither result establishes sampler accuracy. The earlier `C-PACK/SONG_LIANG_MAP.md`, rows 10–11, makes the fixed-subset and screening distinctions; `H3_songliang_notes.md`, F9, reports the fixed-size qualification, but is not a substitute for inspecting the supplement.

## 2. Target statement

**Candidate only, not an established claim.** Start with a fixed candidate dimension and iid rows. Define
\[
(a_0,b_0)=\arg\min_{a,b}E_*(Y-a-X^Tb)^2,\quad
v_0=E_*(Y-a_0-X^Tb_0)^2>0,\quad S_0=\operatorname{supp}(b_0),
\]
\[
f_0(dx,dy)=P_X(dx)\,\phi(y;a_0+x^Tb_0,v_0)\,dy.
\]
Assume a unique projection, a positive-definite covariance of the retained predictors, finite joint fourth moments, and finite \(\mathrm{KL}(P_*\Vert f_0)\) for the literal KL interpretation. Otherwise describe the target as the Gaussian expected-log-score projection. Nonlinear conditional means and heteroscedastic, non-Gaussian residuals are allowed; conditional mean-zero residuals are not required.

For the unchanged coded posterior, with raw coefficients and the plug-in intercept of `W3-DIST/STATEMENT.md` §0, target
\[
\Pi\{H(f,f_0)>\epsilon\mid D_n\}\to_{P_*}0\quad(\epsilon>0),
\qquad \pi(S_0\mid D_n)\to_{P_*}1.
\]
Allow the empty support by a direct finite-dimensional argument. For fixed nonzero coefficients, separation from underfitted models follows from identifiability; density consistency alone requires no beta-min.

At our interface level: retain bounded signal-to-residual energy, an eventual (F₀) floor, and determinant control (OS), anchored at \(b_0\); require positive population prediction loss for underfits. A fixed positive-definite covariance supplies these design properties. New score and residual-square laws of large numbers, with tight score fluctuations, replace (GRᶜ). These are additional stochastic assumptions, not consequences of (OS)/(ID).

Keep the coded model prior, slab, response standardisation and variance prior; the cap is eventually inactive. Give up growing \(p\), uniform expectation rates and arbitrary dependent designs initially. Exactness is plausible and worth targeting; inclusion plus Hellinger consistency is a fallback. Do not promise \(\sqrt{\log n/n}\) expectation error, almost-sure convergence, or KL-to-truth convergence. A later growing-dimensional target would retain bounded support, \(p\le n^A\), strengthened residual-score concentration, and a quantitative population analogue of (ID), but needs a separate feasibility gate.

## 3. Feasibility given the existing theory

**Reusable algebra.** `W3-MISR/lemmas/R_reduction.md`, R′(a),(a′), gives pathwise invariance/equivariance regardless of the data law. R′(b) does not transfer; R′(c)'s directional total variation need not vanish. `W3-POST2/lemmas/A_occam.md`, A0, retains determinant/prior bounds. The Gaussian marginal-likelihood formula and conditional Gaussian/inverse-gamma posterior remain exact integrations of the *working* model under non-Gaussian data. What breaks is their sampling-law analysis, not the integration.

**Selection bottleneck.** `C_expectation.md`, C2, uses the true-density identity \(E_*[m/f_*]=1\); substituting a pseudo-true Gaussian density loses that identity. Its assembly also consumes `A_occam.md` (G3′),(C5′), including exact chi-square truncated exponential moments. (OS) alone no longer bounds those expectations. `E_visibility.md`, E1(a), needs replacement for its Gaussian cross-term bound. Its deterministic comparison and the (ID) loss geometry remain useful. Thus POST2 Claim C and the parent POST size-tail theorem are not black-box inputs.

Under nonlinear misspecification the residual is orthogonal to predictors in population, but generally has nonzero conditional mean given the design. Heteroscedasticity changes directional score variances relative to \(v_0\). Conditioning on the design therefore cannot recover the existing argument. Independent sub-Gaussian errors permit quadratic-form concentration, applied in raw coordinates before centring; general nonlinear residuals instead need joint empirical-score control. Even strong tails do not automatically recover the Gaussian critical exponential moments or the same expectation rate.

**Contraction and intercept.** POST2 `D_hellinger.md`'s conjugate algebra survives; its sampling bounds need replacement. `W3-DIST/STATEMENT.md` §3, Lemmas H and T, retain Gaussian-to-Gaussian distance reduction and distribution-free sparse sample-to-population transfer. Lemmas X/S and V's Gaussian moment bound require new proofs. `W3-MISR-R/lemmas/H1_plus.md` H1.3 retains its Gaussian KL inequality; H1.0's Gaussian transfer and `H2_uniform.md`'s uniform conclusion do not. CorG-min(c), `STATEMENT.md` §2, explains why the existing reduction cannot simply be relaxed.

A common random intercept cancels for model selection, but can destroy iid rows and a deterministic population density target; fix it initially. The rider's §4 KL-reading restriction is essential. De Blasi–Walker and Kleijn–van der Vaart supply misspecified-consistency routes; the latter's 2012 local theory also warns that posterior and sampling covariance differ. None automatically handles our response-dependent prior. For fixed dimension, direct quadratic likelihood comparison and prior bracketing look cheaper. These literature routes are recalled, not supplement-verified. The supplied registry's `theory_loop.tsv`, C-MIS row, expressly leaves “outside GR” open; its older labels do not certify this extension.

## 4. Cost and risk

Estimate: a medium/T2 ticket, three key lemmas (projection and empirical moments; coded-prior likelihood comparison; density/intercept transfer), about 2–4 lead-weeks including checks. Fixed-dimension consistency has low-to-moderate mathematical risk; novelty is modest. Retaining polynomial dimension and expectation rates is a high/T3 project: roughly 5–7 key lemmas and 6–10+ lead-weeks, with substantial risk that tail/variance restrictions make the result weak. The critical issue is controlling accumulated overfit mass, not identifying the projection.

## 5. Recommendation

Commission only the fixed-dimensional result first, retaining the actual coded prior and covering nonlinear means and heteroscedastic non-Gaussian residuals. Require an example outside (OVᶜ), and an explicit audit of standardisation and the variance prior. Stop before a growing-dimensional promise unless the overfit-mass argument closes. Preserve the existing MIS-R rates as a separate stronger conclusion on its narrower law class.

VERDICT: pursue a narrow version — Fixed-dimensional KL-projection consistency fills a real robustness gap at manageable cost, while preserving polynomial-dimensional expectation rates requires a substantially new argument.
