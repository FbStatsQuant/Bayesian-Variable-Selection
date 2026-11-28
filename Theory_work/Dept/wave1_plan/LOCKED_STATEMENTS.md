# LOCKED STATEMENTS: final assumptions A1–A10 and final theorem list (Wave 1 Lead-A, v0.1, 2026-11-28)

**Status: DRAFT v0.2 (v0.1 + Astra adviser memo items 1–3, 6, 8) for the Plan Council (bar ≥ 8.0).** Nothing is locked until the council clears it and the Theory
Manager has ruled on every finding.
Sources: HQ curated packet `Theory_work/Wave3/HQ_ADVISORS_2026-11-28/CURATED_PACKET.md` (= "the packet"; §n = its
sections) and its five supporting files. Current draft: Writing `sections/03_theory.tex` at writing/main `df9da1e6`
(the "draft"; copy at `.rc_tmp/leadA/03_theory_df9da1e6.tex`, untracked). Proof sources: listed per theorem in
`MASTER_PROOF_PLAN.md`.
Engine locked: v3.1.1, $g=n$, truncated BB$(1,p)$, MPM. Terminology: "high-dimensional", $p\le n^A$; never "ultrahigh".

Numbering. A1–A10 keep the draft's numbers. A7 is replaced by **A7′**, A9 by **A9′**. The theorem labels below
(Thm D, Thm S, Cor S1, Thm M, Cor M1) are working labels; Writing assigns the paper numbers (3.x).

---

## 0. Setting and notation (unchanged from the draft §3.1, restated so the statements below are self-contained)

- The observations $(x_i,y_i)$, $i\le n$, are i.i.d. copies of $(x,y)$, with $x\in\mathbb R^p$ in original units.
  $p$ is the raw dimension. It and the law of $(x,y)$ may depend on $n$. A constant is **fixed** if it does not depend
  on $n$.
- Truth (when A1 holds): $y=\alpha^*+x^\top\beta^*+\varepsilon$, $\varepsilon\sim N(0,\sigma_*^2)$, $S_0=\operatorname{supp}\beta^*$,
  $s_0=|S_0|$. $\zeta_j=(x_j-Ex_j)/\operatorname{sd}(x_j)$.
- **Standardised effect** of predictor $j$: $b_j:=|\beta^*_j|\operatorname{sd}(x_j)/\sigma_*$; $b_{\min}:=\min_{j\in S_0}b_j$.
- $\Pi(\cdot\mid D_n)$: the exact posterior of $(S,\beta,\sigma^2)$ of the method as coded, mapped to original units. Its
  model marginal is $\Pi(S\mid D_n)$, with $\mathrm{PIP}_j=\Pi(j\in S\mid D_n)$, $\mathrm{HPM}=\arg\max_S\Pi(S\mid D_n)$
  (any tie rule) and $\mathrm{MPM}=\{j:\mathrm{PIP}_j>1/2\}$.
- A draw defines $f(x,y)=P_x(dx)\,\phi(y;\bar y+(x-\bar x)^\top\beta,\sigma^2)$.
  $d_H(f,g)=(1-\iint\sqrt{fg})^{1/2}$, which is Song & Liang's (SL's) distance divided by $\sqrt2$.
- $r_n:=\sqrt{\log n/n}$; $\epsilon_n:=\sqrt{M\log n/n}$ for a level $M\ge1$.
- **Sparse set:** a set of at most $c\log n$ predictors. A4 and A5 are required for every fixed $c>0$, for all large
  $n$, with constants $L$, $c_\psi$ that do not depend on $c$ (as in the draft). Each theorem uses only one window
  $c$; see `MASTER_PROOF_PLAN.md` §1, shared lemma L-DES.
- Exceptional data sets. The coded posterior is undefined if fewer than two columns are non-constant or $y$ is constant.
  Every probability statement counts such data sets as failures (the draft's convention, §3.1).

## 1. Final assumptions

Each assumption is given as **(math)**, **(plain English)** and **(change vs draft)**.

**A1 (Gaussian linear model).** The pairs $(x_i,y_i)$ are i.i.d. copies of $(x,y)$, and
$y=\alpha^*+x^\top\beta^*+\varepsilon$ with $\varepsilon\sim N(0,\sigma_*^2)$ independent of $x$ and $\sigma_*^2>0$. The
quantities $\alpha^*,\beta^*,\sigma_*$ and $P_x$ may depend on $n$.
*Plain English:* the response is a linear function of the predictors plus independent normal noise; the design is
random.
*Change:* none.

**A2 (Sparsity).** $s_0\le s$ for a fixed integer $s\ge0$.
*Plain English:* only a few predictors matter, however many there are.
*Change:* none. (The selection results add $s_0\ge1$ in their own statements.)

**A3 (Dimension).** $2\le p\le n^A$ for a fixed $A\ge1$.
*Plain English:* the number of predictors may grow like any fixed power of $n$ (the high-dimensional regime, by
deliberate choice).
*Change:* none (owner ruling, draft l.63–72).

**A4 (Sub-Gaussian predictors).** Every predictor has positive variance, and for a fixed $L\ge1$,
$E\exp(t\,w^\top\zeta)\le\exp\{L^2t^2\operatorname{Var}(w^\top\zeta)/2\}$ for every $t\in\mathbb R$ and every
$w\in\mathbb R^p$ supported on a sparse set.
*Plain English:* every combination of a few standardised predictors has tails no heavier than a Gaussian with the same
variance, up to the factor $L$.
*Change:* none.

**A5 (No near-exact collinearity).** $n\,\lambda_{\min}\{\operatorname{Corr}(x_T)\}\ge c_\psi$ for every sparse set $T$, for
a fixed $c_\psi>0$.
*Plain English:* no predictor is an almost exact linear combination of a few others; correlations may approach 1, but
no faster than $1-c_\psi/n$.
*Change:* none.

**A6 (Bounded effects).** $b_j=|\beta^*_j|\operatorname{sd}(x_j)/\sigma_*\le\bar b$ for every $j$, for a fixed $\bar b>0$.
*Plain English:* no standardised effect is more than a fixed multiple of the noise level, which excludes the noiseless
limit.
*Change:* none. The bounded-SNR variant A6′ appears at most as a supplement remark (packet §1, §5).

**A7′ (Identifiability and signal), replaces A7.** Put $j_0:=\lceil(2A+1)s_0\rceil+1$.
- **(a) Small-set floor (anchored at the true model).** $\lambda_{\min}\{\operatorname{Corr}(x_{S_0\cup J})\}\ge\varphi^2$
  for every set $J$ of at most $j_0$ predictors outside $S_0$, for a fixed $\varphi\in(0,1]$. Sets are subsets of
  $\{1,\dots,p\}$, so their size is automatically at most $\min\{p,s_0+j_0\}$.
- **(b) Beta-min.** $b_{\min}\ge C\sqrt{\log(p\sqrt n)/n}$ for a fixed constant $C$. The selection theorem states how
  large $C$ must be.

*Plain English:* (a) the true predictors, together with any small group of other predictors (about $(2A+1)$ times the
size of the true model), are not nearly collinear: none of them is strongly explained by the rest. (b) Every true effect exceeds the detection threshold
$\sqrt{\log(p\sqrt n)/n}$ by a large enough fixed factor. That threshold is the order below which no method can recover
the support; the $\sqrt n$ is the cost of the unit-information prior.
*Why (a) is needed, and why A5 alone is not enough (packet §1, Astra's example; it goes in the paper).* Take two
predictors with correlation $1-c/n$. They satisfy A5. At the threshold scale, the Kullback–Leibler divergence over $n$
observations between "the effect is on $x_1$" and "the effect is on $x_2$" is $c\,b_{\min}^2\to0$. So no posterior can
tell the two apart, and a beta-min condition with A5 alone cannot give selection.
*Two floors.* A7′(a) is a fixed floor on sets of bounded size $O(s_0)$. A5 is the weak floor $c_\psi/n$ on logarithmic
sets. Both are used, on different sets (`MASTER_PROOF_PLAN.md` L-FLOOR).
*Sufficient form (simpler to read, stronger):* A7′(a) holds if $\lambda_{\min}\{\operatorname{Corr}(x_T)\}\ge\varphi^2$ for
every set $T$ of at most $(2A+2)s+2$ predictors (since $s_0+j_0\le(2A+2)s+2$). The anchored form is the one the proof
uses (`W3-POST/STATEMENT.md:68-70`, $(F_\lambda)$). It is strictly weaker: Astra's example of $j_0+1$ equicorrelated
nulls, with correlation $(-1+1/n)/j_0$, satisfies A5 and the anchored form but fails the all-subsets form
(adviser memo, item 3). By interlacing, the anchored form still gives the floor on every set of at most $j_0$
predictors, so it excludes duplicated columns.
*Change:* the draft's selection margin A7 (accounting set $Q_n$, leakage, $h$, $\bar u_d$) and Conjecture 3.3 move to
the supplement as a conjecture. The draft's Remark `rem:th-margin` (a beta-min sufficient for A7) is deleted from the
main text, because A7 has no proof.

**A8 (Fixed candidate dimension).** The pairs $(x_{\mathcal C,i},y_i)$, $i=1,2,\dots$, form **one** i.i.d. sequence of
copies of $(x_{\mathcal C},y)$, whose joint law is fixed (it does not depend on $n$); $\mathcal C$ is a fixed set with
$2\le|\mathcal C|<\infty$; $Ey^2<\infty$, $E\|x_{\mathcal C}\|^2<\infty$,
$\operatorname{Var}(x_{\mathcal C})$ is nonsingular and $\sigma^2_{\mathcal C}>0$.
*Plain English:* a fixed set of candidate predictors is used, with any joint law of the candidates and the response
that has finite second moments. The response may be discrete, heteroscedastic or nonlinear.
*Why one fixed law:* with an $n$-dependent law, e.g. $y=n^{-1}x_1+\varepsilon$, the projected support is $\{1\}$ for
every $n$, yet the KL divergence from the null over $n$ observations is $1/(2n)$, so no rule can include $x_1$
(adviser memo, item 2). With $|\mathcal C|=1$ the coded posterior is undefined.
*Change:* wording made explicit (one sequence, finite $|\mathcal C|$); content as in the draft, l.312–316. The pseudo-true objects $(\alpha_{\mathcal C},\beta^{\mathcal C},\sigma^2_{\mathcal C},
\varepsilon_{\mathcal C},S_0^{\mathcal C},f_0)$ are those of the draft, l.263–281.

**A9′ (Gaussian residual given the candidates), replaces A9.** For a candidate set $\mathcal C=\mathcal C_n$ that is fixed
before the data are seen (or chosen on independent data), $\operatorname{Var}(x_{\mathcal C})$ is nonsingular, and the
residual $\varepsilon_{\mathcal C}=y-\alpha_{\mathcal C}-x_{\mathcal C}^\top\beta^{\mathcal C}$ is $N(0,\sigma^2_{\mathcal C})$
and independent of $x_{\mathcal C}$, with $\sigma^2_{\mathcal C}>0$.
*Plain English:* given the measured candidates, the response is still Gaussian and linear. Only the coefficients and
the noise variance change.
*Remark that replaces the old structural wording (paper).* Under A1, A9′ is equivalent to the structural form: the
left-out signal is $x_O^\top\beta^*_O=\alpha_O+x_{\mathcal C}^\top\gamma+\varepsilon_O$, with
$\varepsilon_O\sim N(0,\tau^2)$ independent of $x_{\mathcal C}$. Then $\beta^{\mathcal C}=\beta^*_{\mathcal C}+\gamma$ and
$\sigma^2_{\mathcal C}=\sigma_*^2+\tau^2$ (Cramér's decomposition theorem). This holds whenever $(x_{\mathcal C},x_O)$ is
jointly Gaussian. A9′ itself does not need A1.
*Change:* the candidate versions of A3–A7′ move out of the assumption and are listed in Cor M1.

**A10 (Sparse pseudo-true model).** $|S_0^{\mathcal C}|\le s_{\mathcal C}$ for a fixed integer $s_{\mathcal C}\ge0$.
*Plain English:* the best linear predictor from the candidates uses only a few of them.
*Change:* none. The paragraph on when A10 holds (draft l.344–352) is kept.

### 1a. Which theorem uses which assumption

| | A1 | A2 | A3 | A4 | A5 | A6 | A7′(a) | A7′(b) | A8 | A9′ | A10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Thm D (density) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | | | | |
| Thm S(a) (inclusion) | ✓ | ✓ ($s_0\ge1$) | ✓ | ✓ | ✓ | ✓ | ✓ | per strong $j$ | | | |
| Thm S(b), Cor S1 | ✓ | ✓ ($s_0\ge1$) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| Thm M (any law) | | | | | | | | | ✓ | | |
| Cor M1 (many candidates) | via A9′ | via A10 | cand. | cand. | cand. | cand. | cand. (selection) | cand. (selection) | | ✓ | ✓ |

"cand." = the assumption for the candidate problem $(x_{\mathcal C},y;\beta^{\mathcal C},\sigma^2_{\mathcal C})$.

## 2. Final theorem statements

### Thm D — Consistency of the fitted density (SL Thms 1–2, Cor 1). Statement unchanged from the draft (Thm 3.1)

**(math)** Assume A1–A6. There are fixed constants $c_H>0$ and $M_0$, depending only on $s,A,L,c_\psi,\bar b$ and the
hyperparameters $a_0,b_0$, such that, for every fixed $M\ge M_0$ and all $n\ge n_0(M)$,
$$P^*\big[\Pi\{d_H(f,f^*)>\epsilon_n\mid D_n\}>n^{-c_HM}\big]\le n^{-c_HM},\qquad \epsilon_n=\sqrt{M\log n/n}.$$
**(plain English)** Except on data sets of probability at most $n^{-c_HM}$, the posterior gives at most that much
probability to joint laws of $(x,y)$ farther than $\sqrt{M\log n/n}$ from the truth. No beta-min condition and no fixed
eigenvalue floor are needed.
**Notes.** (1) The quantifier order is "for each fixed $M\ge M_0$, for $n\ge n_0(M)$" (packet §4). The source
(W3-DIST Theorem A(i)) is stronger, with one $n_0$ for all $M\le\sqrt n/\log n$; the paper does not claim that.
(2) For level $M$ the proof uses A4–A5 on the single window $q_n=\min\{p,\lceil C_qM\log n\rceil\}$,
$C_q=2(s(A+2)+4)/\log2$, which is a sparse set with $c=C_qM+1$.
(3) Optional corollary (supplement): $\Pi\{d_H>\epsilon_n\mid D_n\}\to0$ almost surely when $c_HM>1$ (Borel–Cantelli).

### Thm S — Selection consistency, headline (SL Thm 3; SL Thm S and Cor S1)

Let $c_0(s,A):=\max_{1\le s_0\le s}\max\{4C_*,\,32[s_0(A+1)+2]\}$, with $C_*$ the T03 proof constant, and
$C_{\rm sel}(s,A,\varphi):=4\sqrt{c_0(s,A)}/\varphi$.

**(math)** Assume A1–A6 with $1\le s_0\le s$, and A7′(a). Fix a constant $C>C_{\rm sel}$.
- **(a) Inclusion of strong predictors, with no condition on the other effects.** Let
  $J_n:=\{j\in S_0:\ b_j\ge C\sqrt{\log(p\sqrt n)/n}\}$. Then
  $\Pi(S\supseteq J_n\mid D_n)=1-O_P(r_n)$. Hence $\max_{j\in J_n}(1-\mathrm{PIP}_j)=O_P(r_n)$ (vacuous if $J_n=\emptyset$).
- **(b) Exact selection.** If also A7′(b) holds with this $C$, so that $J_n=S_0$, then
  $$1-\Pi(S_0\mid D_n)=O_P(r_n),\qquad \max_{1\le j\le p}|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|\le1-\Pi(S_0\mid D_n),$$
  and $P^*(\mathrm{HPM}=\mathrm{MPM}=S_0)\to1$.

**(plain English)** (a) Every true predictor whose standardised effect clears the threshold by the factor $C$ is
included with posterior probability close to one, whatever the other effects are. (b) If every true effect clears it,
the posterior concentrates on the exact true model at the rate $\sqrt{\log n/n}$. Every inclusion probability is then
near 1 for true predictors and near 0 for the others, and the highest-probability model and the median-probability
model both equal the true model.
**Notes.** (1) $C_{\rm sel}$ is a proof constant and is labelled *not sharp*. Its value goes in the supplement.
At $s_0=5$, $A=2$, $\varphi=1$ we have $c_0=775.55$ and $C_{\rm sel}=4\sqrt{c_0}\approx111.4$, uniformly over
$2\le p\le n^A$. At $p=n^2$ the requirement is asymptotically only $\sqrt{8c_0/2.5}\approx49.8$, because
$\log(p\sqrt n)=2.5\log n$ there. The packet's "about 49.8" is this $p=n^2$ value (`ASTRA_PHASE2.md` §2). Both
are in the units of A7′(b). In the main text, write "for every fixed $C$
larger than a constant $C_{\rm sel}(s,A)/\varphi$ given in the supplement". (2) The inequality $C>C_{\rm sel}$ is strict;
the strictness is what gives a fixed $c>c_0$ uniformly in $p\ge2$ (`MASTER_PROOF_PLAN.md` S-2). (3) $J_n$ is defined
by **population** effects. The proof shows $J_n\subseteq J^{\rm sample}_n(c)$ on the design event. (4) $s_0=0$ is not
claimed (packet §5).

### Cor S1 — Fixed effects

**(math)** Assume A1–A6 with $1\le s_0\le s$, and A7′(a). If $b_{\min}\ge\underline b$ for a fixed $\underline b>0$, the
conclusions of Thm S(b) hold.
**(plain English)** Effects of fixed size are recovered exactly.
**Note (nesting).** Cor S1 replaces the draft's Thm 3.2, but its hypotheses do not contain the old ones. The old
theorem assumed a fixed floor on sets of size $5(A+1)(s_0+1)\log n$ and did not assume A5. Cor S1 assumes A5, which
is weaker on those sets, but on its own window $C_q\log n$, which is wider, plus a fixed floor on $O(s_0)$ sets only.
This is a deliberate simplification (packet §2 drops the old form); no claim is made that Cor S1 generalises the old
theorem.

### Thm M — Misspecification: fixed candidates, any response law (SL Thm 4, Cor 2)

**(math)** Assume A8. Then, $P^*$-almost surely:
- **(i) Density.** $\Pi\{d_H(f,f_0)>\epsilon\mid D_n^{\mathcal C}\}\to0$ for every fixed $\epsilon>0$.
- **(ii) Inclusion.** $\Pi(S\supseteq S_0^{\mathcal C}\mid D_n^{\mathcal C})\to1$.
- **(iii) Exact support.** If in addition $E(x_j^2\varepsilon_{\mathcal C}^2)<\infty$ for every $j\in\mathcal C$, then
  $\Pi(S_0^{\mathcal C}\mid D_n^{\mathcal C})\to1$, and $\mathrm{HPM}=\mathrm{MPM}=S_0^{\mathcal C}$ for all large $n$.

Here $f_0(x_{\mathcal C},y)=P_{x_{\mathcal C}}(dx_{\mathcal C})\,\phi(y;\alpha_{\mathcal C}+x_{\mathcal C}^\top\beta^{\mathcal C},\sigma^2_{\mathcal C})$
is **defined** as the Gaussian linear law that maximises the expected Gaussian log score
$E\log\phi(y;\alpha+x_{\mathcal C}^\top\beta,\sigma)$, uniquely by A8, and $d_H(f,f_0)$ compares two Gaussian
conditional laws of $y$ averaged over the same $P_{x_{\mathcal C}}$, whatever the law of $y$,
and $\Pi(\cdot\mid D_n^{\mathcal C})$ is the posterior computed from $(y,X_{\mathcal C})$ with $p$ replaced by $|\mathcal C|$.
All statements hold along one i.i.d. sequence from the fixed law. $S_0^{\mathcal C}=\emptyset$ is covered.
**(plain English)** Whatever the true law of the response, with a fixed set of candidates the posterior settles on the
best Gaussian linear approximation built from them. It always keeps every candidate that this approximation uses.
If the scores have finite variance, it selects exactly those candidates.
**Notes.** (1) SL Thm 4 assumes a Gaussian linear full model; A8 drops it. SL Cor 2 is inclusion in probability;
(ii) is almost sure; (iii) adds exclusion, which SL do not prove. (2) The moment condition in (iii) is used only for
exclusion, through the LIL. (3) $f_0$ is called the KL projection (SL (17); $\beta^{\mathcal C}$ is their (19)) only when some Gaussian working law
has finite KL divergence from the truth (draft l.276–280). Example where it has none: $x_{\mathcal C}$ two independent
$N(0,1)$ and $y\sim$ Bernoulli$(1/2)$ independent of them. Every Gaussian law has infinite KL divergence from the
truth, yet the log-score maximiser $N(1/2,1/4)$ is unique (adviser memo, item 1).

### Cor M1 — Many candidates (omitted predictors, high dimension)

**(math)** Let $\mathcal C=\mathcal C_n$ be fixed before the data are seen, with $2\le|\mathcal C|\le n^A$ for a fixed
$A\ge1$. Assume A9′ and A10, and assume A4–A6 for the candidate problem, i.e. with
$(x_{\mathcal C},\beta^{\mathcal C},\sigma^2_{\mathcal C})$ in place of $(x,\beta^*,\sigma_*^2)$.
- **(i)** The conclusion of Thm D holds for $\Pi(\cdot\mid D_n^{\mathcal C})$ with $f_0$ in place of $f^*$, and with
  $s_{\mathcal C}$ in place of $s$ in the constants.
- **(ii)** If also $1\le|S_0^{\mathcal C}|$ and A7′ holds for the candidate problem (with
  $b^{\mathcal C}_j=|\beta^{\mathcal C}_j|\operatorname{sd}(x_j)/\sigma_{\mathcal C}$), the conclusions of Thm S hold
  with $S_0^{\mathcal C}$ in place of $S_0$.

**(plain English)** If the measured candidates leave Gaussian noise behind, the method behaves exactly as in the
correctly specified case. It recovers the best linear predictor from the candidates, keeps candidates that stand in for
missing predictors, and drops true predictors whose effect is cancelled.
**Notes.** (1) Under A9′ the candidate data satisfy A1 with $(\alpha_{\mathcal C},\beta^{\mathcal C},\sigma_{\mathcal C})$,
and $f_0$ is their true joint density. So Cor M1 is Thm D and Thm S applied to the candidate problem (one paragraph).
(2) Optional sentence (supplement): the expectation form $E^*\{1-\Pi(S_0^{\mathcal C}\mid D_n^{\mathcal C})\}=O(r_n)$
follows from W3-POST2 Claim C case (i) (`W3-POST2/lemmas/C_expectation.md:8-16`). It is not part of Criterion 2. The rate needs the per-$n$ inequality $E\delta_n\le Cr_n+P(\mathcal A_n^c)$ with
B3's exponentially small design-failure bound, preprocessing failures included under a bounded loss convention; mere
$P(\mathcal A_n^c)=o(1)$ would lose the rate (adviser memo, item 8).
(3) The Grünwald–van Ommen sentence (why the high-dimensional result needs A9′ and Thm M does not) stays between Thm M
and A9′.

## 3. Dropped and moved (packet §2, §5)

- **Dropped from the main text:** draft Thm 3.5 (`thm:th-omitted`, Gaussian predictors; covered by Cor M1), Conjecture 3.3
  (selection under A7), Conjecture 3.6 (misspecification).
- **Moved to the supplement:** A7 (margin form) and its conjecture; A6′ (bounded SNR), at most as a remark; the
  sharpened constant $\approx5.16(1+\eta)$ (optional, separately reviewed; it gives $O_P(r_n+n^{-\gamma})$); the null
  model $s_0=0$ (optional).
- **Not targeted:** a general response law in growing dimension.

## 4. Song & Liang map (replaces draft Table 1)

| SL result | Here | Statement |
|---|---|---|
| Thms 1–2, Cor 1 (density) | Thm D | fixed prior, no tuning sequences; $p\le n^A$ |
| Thm 3 (inclusion of identifiable predictors) | Thm S(a) | each strong predictor, no condition on the others |
| Thm S, Cor S1 (MAP) | Thm S(b), Cor S1 | exact model, rate $r_n$, HPM = MPM = $S_0$ |
| Thm 4 (misspecified subset) | Thm M(i) | any response law, second moments |
| Cor 2 (pseudo-true support) | Thm M(ii)–(iii); Cor M1 | inclusion a.s.; exact support under score moments; high-dimensional under A9′ |

## 5. Open items for the council

1. A7′(a) is stated in the anchored form, which is weaker and is exactly what the proof uses. The all-subsets form on
   $(2A+2)s+2$ predictors is offered as a sufficient condition. Which should lead in the main text?
2. Cor S1 does not nest the old Thm 3.2 (see its note). Is that acceptable?
3. In Thm S, should the main text state $C_{\rm sel}$ symbolically ($4\sqrt{c_0}/\varphi$), or only "a constant given
   in the supplement"? The draft above proposes the latter.
