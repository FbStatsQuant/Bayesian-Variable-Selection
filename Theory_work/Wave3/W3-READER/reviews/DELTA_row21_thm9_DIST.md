# DELTA — card row 2.1 / READER_VERSIONS row thm9 (W3-DIST) — PROPOSAL, not applied (HQ card 13)

Written 2026-11-16 by the W3-READER lead for the manager / HQ. Nothing here is applied to `READER_VERSIONS.md` or
`CLAIMS_CARD.md`. Applicable patch (git apply --check passes on theory/W3-READER HEAD): `reviews/DELTA_row21_thm9_DIST.diff`.

**Source (read only):** `/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/` at main d2b600ba —
`STATEMENT.md` v1.4.10 (§1 masters :72-112, §1R reader versions :126-269, bridges :384-417), `CHECKPOINT_3.md` (§2, §5),
`TARGET.md` §2 (:21-35, Song–Liang parity) and §6 (:197-205, why each assumption), `REPORT.md` :11-17 (statuses).
Council R2 PASSED, MANIFEST c5cd9cdd30ecfe06a39b06ee0aa8b86f70d4b08425a98e9f4d09023de5282ddc (astra 9.3, opus 9.2).
**Rate wording:** DIST-2's "best rate ≍ (1 + s₀^r) log n·ℓ_n/n" is LOOSE (Dept RT1,
`/home/fb31/BVS-wt/THEORY-DEPT/Theory_work/Dept/research/DIST2_rate_check/RT1_sol.md`), so the proposal states **no
dependence of any rate on the sparsity**: neither DIST-2's gloss nor DIST-1 (c)'s "(1 + s₀^r) log n/n" is used. The
constants are said to depend on $(s,A,L,c_\psi,\bar b)$, as in the theorem, and nothing more.

## 1. Card row 2.1 (and the abstract-list line)
Conditions as CP3 §5: SOP:TH09 (its T01 part) on every theorem; W3-POST:Thm-1 on Theorem 9B; the W3-SAMP delivery
premises on DIST-C's delivery statements; exact arithmetic on DIST-C and Corollary 9C. **One precision against the brief:**
Corollary 9C (= W3-DIST Cor-C) is recorded "conditional on SOP:TH09 […] and EX-A" only. Its display has the list-mass
premise $\pi(\mathcal T)\ge n^{-cM/2}$ and claims no discovery, so the W3-SAMP premises attach to DIST-C's delivery
statements (C-ii)(α), (C-iv), not to Corollary 9C. The card says so.

| 2.1 (Thm 9) | **The posterior recovers the joint distribution of $(x,y)$** [H5-13]. Rows i.i.d.; Gaussian linear model, any noise level; at most $s$ nonzero coefficients, at most $n^A$ predictors; sub-Gaussian predictors on sparse directions; no near-exact collinearity (smallest eigenvalue of the correlation matrix of any $O(\log n)$ predictors $\ge c_\psi/n$); bounded signal per predictor. Then for every level $M_0\le M\le\sqrt n/\log n$, with probability $\ge1-n^{-cM}$ the posterior (prior as coded) puts mass $\le n^{-cM}$ outside the Hellinger ball of radius $\sqrt{M\log n/n}$ around the true joint law, and on models with more than $s+C_1M$ predictors. No beta-min and no fixed lower bound on eigenvalues. Without the collinearity condition: radius larger by $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$. With a fixed eigenvalue floor and detectable signals: rate $M_n/\sqrt n$ (Thm 9B). Every completed sampler run whose returned list carries posterior mass $\ge n^{-cM/2}$: the posterior restricted to the list satisfies the same bound at level $n^{-cM/2}$ (Cor 9C; exact arithmetic). | W3-DIST council R2 PASSED (MANIFEST c5cd9cdd…, astra 9.3 / opus 9.2); registry rows staged, not yet recorded. Statuses (W3-DIST REPORT.md:11-17): `W3-DIST:Thm-A`: "PROVED (by this seat), line-checked, conditional on SOP:TH09 […]" (SOP:TH09 = its T01 part); `W3-DIST:Thm-B`: "…, conditional on W3-POST:Thm-1, SOP:TH09 […]"; `W3-DIST:Cor-C`: "…, conditional on SOP:TH09 [(…) and EX-A; …]"; `W3-DIST:DIST-C` delivery statements (not used by Cor 9C): "…, conditional on SOP:TH09, W3-SAMP:D, W3-SAMP:PC, W3-SAMP:LT#, W3-SAMP:C, W3-SAMP:TR". *Note:* the SOP:TH09 condition may be discharged by the W3-T03ACC recording (task T); the registry tool recomputes it. | Song–Liang (2015) Theorems 1–2 analogue for the coded method: same distance and exponential form; rate a constant times $\sqrt{\log n/n}$ with the prior as coded and no tuning; parametric rate and the sampler's output, which they do not treat. Narrower: at most $n^A$ predictors, exact sparsity, and the sharp form uses a collinearity condition they do not need. Overall incomparable [TARGET §2]. | **clean**; bridges identity + one NEW arithmetic line (B9.5); conditional on SOP:TH09 (T01) |

- **2.1** W3-DIST council R2 passed; abstract placement and form per HQ card 13 (conditional on SOP:TH09 as row 1.1); **2.2** body remark [H5-13].

## 2. Row thm9 — proposed reader text (proved version)
Numbered primitive assumptions (A1)–(A5), plus (A6) for Theorem 9B. Displays (i), (ii) at radius $\sqrt{M\log n/n}$,
and (iii), the version without (A4), with the extra $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$. Theorem 9B (parametric
rate) and Corollary 9C (sampler output). Song–Liang comparison by item. No internal ids in the reader text; the ids sit
in the master and bridge blocks, as in every row.

Interpretive sentences (D71), each a claim with a source:
- "the posterior contracts … at the rate $\sqrt{\log n/n}$" — display (i) with $M$ fixed.
- "(ii) … does not say that they are the true ones" — W3-DIST :196.
- the Song–Liang items — TARGET §2.
- the why-lines — TARGET §6, shortened. Dropped from §6: the numerics sentences, and the necessity sentence on (A2).

````markdown
## 9. Theorem 9 — The posterior recovers the joint distribution of predictors and response
<!-- ROW thm9 BEGIN -->
**Card row** 2.1 · **Section version** 0.3 (proposal, 2026-11-16) · **Pending delta** —


### Setting and notation
The data are $n$ independent copies $(x_i,y_i)$, $i=1,\dots,n$, of a pair $(x,y)$: $x\in\mathbb R^{p_{\mathrm{raw}}}$ is the
vector of all observed predictors (a row of $X^{\mathrm r}$, §1 of the notation) and $y\in\mathbb R$ the response (an entry of
$y^{\mathrm r}$). $D_n$ denotes the data set. $p_{\mathrm{raw}}$ may grow with $n$ and may be much larger than $n$; the law of
$(x,y)$ may change with $n$. As in every theorem, $p\le p_{\mathrm{raw}}$ is the number of predictors not constant in the
sample, and the method runs on these (standardisation §2, prior $\mathrm{BB}(1,p)$ capped at $\min(p,\lfloor n/2\rfloor)$, slab
and inverse-gamma prior §3; no tuning). $\Pi(\cdot\mid D_n)$ is the resulting exact posterior of $(S,\beta,\sigma^2)$, mapped
back to the original units: $S$ is the set of included predictors, $\beta\in\mathbb R^{p_{\mathrm{raw}}}$ the coefficient vector
(zero outside $S$ and on removed predictors), $\sigma^2$ the noise variance. If fewer than two predictors remain, or the
response is constant in the sample, the posterior is not defined; under the assumptions below such data sets have
probability smaller than the exceptional probabilities in the theorems and are counted in them (and $p=p_{\mathrm{raw}}$
outside them).

*The distribution attached to a posterior draw.* A draw $(S,\beta,\sigma^2)$ defines a joint density $f$ for a new pair
$(x,y)$: $x$ has its true distribution and, given $x$, $y\sim N\big(\bar y+(x-\bar x)^\top\beta,\ \sigma^2\big)$, where $\bar y$
and $\bar x$ are the sample means. $f^*$ is the true joint density of $(x,y)$.

*Further notation.* $d_H(f,g):=\big(1-\int\sqrt{fg}\big)^{1/2}$ is the Hellinger distance. $P^*$ is the distribution of the
data. $\mathrm{sd}$, $\mathrm{Var}$, $\mathrm{Corr}$ are population standard deviations, variances and correlation matrices;
$z_j:=(x_j-Ex_j)/\mathrm{sd}(x_j)$ and $z:=(z_1,\dots,z_{p_{\mathrm{raw}}})$; $x_T$ is the sub-vector of $x$ indexed by a set $T$;
$|S|$ is the number of predictors in $S$; $a\vee b:=\max(a,b)$; $\log$ is the natural logarithm.

*Constants, level and window.* $s\ge0$ is an integer and $A\ge1$, $L\ge1$, $c_\psi>0$, $\bar b>0$ are constants; none depends
on $n$. The reader fixes a **level** $M\ge1$ (a larger $M$ gives a larger ball and a smaller exceptional probability). The
**window** is
$$
q_n:=\min\big\{p_{\mathrm{raw}},\ \lceil C_qM\log n\rceil\big\},\qquad C_q:=2\big(s(A+2)+4\big)/\log 2 ,
$$
the largest number of predictors that (A3) and (A4) constrain jointly (of order $\log n$ for a fixed level).

### Assumptions
- **(A1) Gaussian linear model.** $y=\alpha^*+x^\top\beta^*+\varepsilon$ with $\varepsilon\sim N(0,\sigma_*^2)$, $\sigma_*^2>0$,
  independent of $x$ ($\alpha^*$, $\beta^*$, $\sigma_*$ and the law of $x$ may depend on $n$).
- **(A2) Sparsity and dimension.** At most $s$ coordinates of $\beta^*$ are nonzero, and $2\le p_{\mathrm{raw}}\le n^A$.
- **(A3) Sub-Gaussian predictors on sparse directions.** Every predictor has positive variance, and for every
  $u\in\mathbb R^{p_{\mathrm{raw}}}$ with at most $q_n$ nonzero entries and every $\lambda\in\mathbb R$:
  $E\exp(\lambda u^\top z)\le\exp\big(L^2\lambda^2\,\mathrm{Var}(u^\top z)/2\big)$.
- **(A4) No near-exact collinearity.** $\lambda_{\min}(\mathrm{Corr}(x_T))\ge c_\psi/n$ for every set $T$ of at most $q_n$
  predictors.
- **(A5) Bounded signal.** $|\beta^*_j|\,\mathrm{sd}(x_j)\le\bar b\,\sigma_*$ for every $j$.

No lower bound on the nonzero coefficients (no beta-min condition) and no fixed lower bound on eigenvalues is assumed:
under (A4) predictors may be correlated up to $1-c_\psi/n$.

### Reader statement
**Theorem 9 (distribution-level consistency).** There are constants $c>0$, $C_1$, $M_0$ and $n_0$, depending only on
$(s,A,L,c_\psi,\bar b)$, such that whenever $n\ge n_0$, $M_0\le M\le\sqrt n/\log n$ and (A1)–(A5) hold with the window $q_n$
of this $M$:
$$
\text{(i)}\quad P^*\Big[\,\Pi\Big(d_H(f,f^*)>\sqrt{M\log n/n}\ \Big|\ D_n\Big)>n^{-cM}\Big]\le n^{-cM},
$$
$$
\text{(ii)}\quad P^*\Big[\,\Pi\big(|S|>s+C_1M\ \big|\ D_n\big)>n^{-cM}\Big]\le n^{-cM}.
$$
The two exceptional sets of data sets can be taken to be the same set, and the bounds are uniform over all laws of the
data that satisfy (A1)–(A5) with the given constants.

*Without (A4).* If (A4) is dropped and (A3) is required only for single predictors ($u$ with one nonzero entry), then
$$
\text{(iii)}\quad P^*\Big[\,\Pi\Big(d_H(f,f^*)>\sqrt{M\log n\cdot\log(p_{\mathrm{raw}}\vee n)/n}\ \Big|\ D_n\Big)>n^{-cM}\Big]\le n^{-cM},
$$
and (ii) holds with $s+C_1M\log n$ in place of $s+C_1M$.

*In words.* Except on data sets of probability at most $n^{-cM}$, the posterior gives probability at most $n^{-cM}$ to
joint laws of $(x,y)$ farther than $\sqrt{M\log n/n}$ from the truth in Hellinger distance, and to models with more than
$s+C_1M$ predictors: the posterior contracts around the true joint law at the rate $\sqrt{\log n/n}$. Statement (ii)
bounds the number of selected predictors; it does not say that they are the true ones.

**Theorem 9B (parametric rate when the true predictors are detectable).** Assume (A1)–(A5) with the window $q_n$ of $M=1$,
with exactly $s\ge1$ nonzero coordinates of $\beta^*$, and in addition
- **(A6) Detectable signal.** (a) $\lambda_{\min}(\mathrm{Corr}(x_T))\ge\psi$ for a constant $\psi>0$ and every set $T$ of
  at most $(2A+3)s+2$ predictors; (b) $\min\{|\beta^*_j|\,\mathrm{sd}(x_j)/\sigma_*:\beta^*_j\neq0\}\ge b_n$, where $b_n>0$ and
  $b_n^2n/\log n\to\infty$.

Then for every sequence $M_n\to\infty$: $\ \Pi\big(d_H(f,f^*)>M_n/\sqrt n\ \big|\ D_n\big)\to0$ in $P^*$-probability.

**Corollary 9C (the output of the sampler).** The method explores the models with a sequential Monte Carlo sampler; it
does not compute the full posterior (small problems that it solves by exact enumeration are not covered here). A run is
*completed* when the method reports the status "completed"; runs that stop early are not covered. The output of a
completed run contains a list $\mathcal T$ of at most $40p+1$ distinct models: the best-scoring models among those offered to
the final run of the sampler (the models scored in that run, together with models scored earlier and carried into it:
the precomputed tables for small groups of predictors and the models kept from the calibration stage). Each model in the
list comes with the logarithm of its unnormalised posterior weight, taken to be computed in exact arithmetic. The output
contains no draws of $(\beta,\sigma^2)$. Let $\pi(\mathcal T)$ be the posterior probability of the list, and let $\hat\Pi$ (not
computed by the method) be the posterior restricted to the list: the models in $\mathcal T$, weighted in proportion to the
exponentials of their returned log-weights, each with its exact conditional posterior of $(\beta,\sigma^2)$. Under the
conditions of Theorem 9, with $P^*$-probability at least $1-n^{-cM}$ over the data, **every** completed run (whatever its
random numbers) with $\pi(\mathcal T)\ge n^{-cM/2}$ satisfies
$$
\hat\Pi\Big(d_H(f,f^*)>\sqrt{M\log n/n}\Big)\le n^{-cM/2}.
$$
If a completed run scored the true model $\{j:\beta^*_j\neq0\}$ and the posterior probability of that model exceeds $\tfrac12$,
then the list contains it, it is the model the method reports as most probable, and $\pi(\mathcal T)>\tfrac12$. Whether
the list carries enough posterior probability is a property of the run: the corollary does not assert it, and the output
does not certify it.

*Example.* Jointly Gaussian predictors satisfy (A3) with $L=1$; independent predictors satisfy it when each satisfies it
with a common constant $L$. (A4) holds for all large $n$ whenever every $q_n\times q_n$ principal block of the correlation
matrix has smallest eigenvalue at least a fixed $\psi>0$, for instance correlation $\rho^{|j-k|}$ with $|\rho|<1$, or equal
correlation $\rho\in[0,1)$.

### Comparison with Song and Liang (2015), Theorems 1–2
- **Same:** the distance (Hellinger between joint densities of $(x,y)$, the law of $x$ integrated) and the exponential
  form of their display (15): $P^*[\Pi(d>\varepsilon_n\mid D_n)>e^{-c n\varepsilon_n^2}]\le e^{-cn\varepsilon_n^2}$, here with
  $n\varepsilon_n^2=M\log n$.
- **Stronger:** (1) the prior is the one the method uses, with no tuning; Song–Liang's theorems are for a family of priors
  whose conditions this prior does not meet. (2) The rate is a constant times $\sqrt{\log n/n}$; at polynomial $p$ their
  Theorem 2 gives $\varepsilon_n^2=\omega_n\log n/n$ with $\omega_n\to\infty$ tied to the prior's size cap, and their
  Corollary 1 as printed gives $n^{-(1-\alpha)}\log^kn$. (3) Theorem 9B gives the parametric rate $M_n/\sqrt n$ and
  Corollary 9C covers the sampler's output; Song–Liang have neither. (4) No lower bound on the growth of $p$ is needed.
- **Weaker:** (1) $p_{\mathrm{raw}}\le n^A$, where they allow $p$ up to $\exp(Cn^\alpha)$. (2) Exact sparsity; their
  Theorem 1 covers approximate sparsity. (3) (A4) is a condition on the design that their Theorems 1–2 do not have;
  without it, display (iii) has exponent $cM\log n=c\,n\varepsilon_n^2/\log(p_{\mathrm{raw}}\vee n)$ at radius $\varepsilon_n$,
  not $c\,n\varepsilon_n^2$.
- **Different, not ranked:** tail conditions on the predictors — (A3) and (A5) here; their Conditions 1–2 (bounded
  predictors in Theorem 1).
- **Overall: incomparable** — stronger on the prior, the rate and the coded output; weaker on the range of $p$, on
  approximate sparsity and, for display (i), by (A4).

### Why each assumption
- (A1) It is the model under which the method's likelihood is correct; it gives the posterior a closed form given the
  predictors. $\sigma_*$ is free because rescaling the response leaves the posterior over models unchanged and rescales the
  posterior of $(\beta,\sigma^2)$.
- (A2) Posterior model size is controlled relative to $s$; the constants depend on $s$ and $A$.
- (A3) Only to make the sample variances of the predictors and the sample covariances of small groups of predictors track
  their population values with probability $1-n^{-cM}$. The passage from the sample to the population distance uses no
  tail condition.
- (A4) It keeps in force the prior's penalty for each extra predictor (a factor of order $n^{-1/2}$); this gives the rate
  $\sqrt{\log n/n}$, the level $n^{-cM}$ and the bounded model size. Without it the radius gains the factor
  $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$ (display (iii)). Whether it is needed for the rate $\sqrt{\log n/n}$ is open.
- (A5) It bounds the signal in units of the noise and excludes huge coefficients that cancel.
- (A6) (Theorem 9B only) It makes the posterior select the true model, which removes the logarithm.

### Master theorem
W3-DIST reader versions (`/home/fb31/Bayesian-Variable-Selection/Theory_work/Wave3/W3-DIST/STATEMENT.md` v1.4.10, §1R
:126-269), council R2 PASSED (MANIFEST `c5cd9cdd…`, astra 9.3 PASS, opus 9.2 PASS; CHECKPOINT_3). Registry rows: staged,
ingest acceptance PASS (CHECKPOINT_3 §6), not yet recorded. Statuses verbatim from W3-DIST `REPORT.md`:11-17:
- Theorem 9 = `W3-DIST:Thm-A` (:185-207; = DIST-1 (1.1) + bridges B0, B1, B2; the sentence without (A4) = DIST-2 (1.2) + B0,
  B1): **"PROVED (by this seat), line-checked, conditional on SOP:TH09 [(SOP:TH09 = its T01 part, "T01–T03:
  PROVED-LOCKED": the coded posterior is the contrast-model posterior); …]"**.
- Theorem 9B = `W3-DIST:Thm-B` (:209-215; = DIST-3 + B0–B3 + selection consistency): **"PROVED (by this seat),
  line-checked, conditional on W3-POST:Thm-1, SOP:TH09 […]"**.
- Corollary 9C = `W3-DIST:Cor-C` (:217-238; = Theorem A + DIST-C (C-0), (C-i), (C-ii)(α)): **"PROVED (by this seat),
  line-checked, conditional on SOP:TH09 [(…) and EX-A; …]"**. The delivery statements of DIST-C (discovery of the true
  model by the sampler) are not used by Corollary 9C; they carry **"conditional on SOP:TH09, W3-SAMP:D, W3-SAMP:PC,
  W3-SAMP:LT#, W3-SAMP:C, W3-SAMP:TR"** (REPORT :14).
- The SOP:TH09 condition (its T01 part) may be discharged by the W3-T03ACC recording (task T); the registry tool
  recomputes it then.

### Bridges
| # | bridge | mark | detail |
|---|---|---|---|
| B9.0 | renaming: DIST's $p$ ↦ $p_{\mathrm{raw}}$, $r$ ↦ $p$, (A3) constant $K$ ↦ $L$, $\sigma^*$ ↦ $\sigma_*$ | identity | to match `NOTATION.md` §1, §3 (there $K$ is the size cap) |
| B9.1 | Theorem 9 (i), (ii), the "same set" and uniformity sentences, the Example = W3-DIST Theorem A | identity (text) | STATEMENT :185-207 |
| B9.2 | display (iii) = Theorem A's "Without (A4)" sentence written as a display (same level $n^{-cM}$, radius times $\sqrt{\log(p_{\mathrm{raw}}\vee n)}$) | identity (transcription) | STATEMENT :200-202 |
| B9.3 | Theorem 9B, Corollary 9C = W3-DIST Theorem B, Corollary C | identity (text; the mixture sentence of C shortened, no content dropped from the claim) | STATEMENT :209-238 |
| B9.4 | "$p=p_{\mathrm{raw}}$ outside the exceptional sets" | EXISTS-CHECKED (line-checked + council R2) | W3-DIST Setup :150-152 and bridge B1 :391-395 (on B1's event no column is dropped) |
| B9.5 | exponent in (iii): $cM\log n=c\,n\varepsilon_n^2/\log(p_{\mathrm{raw}}\vee n)$ at $\varepsilon_n^2:=M\log n\log(p_{\mathrm{raw}}\vee n)/n$ | **NEW** (one line of arithmetic) | substitute $\varepsilon_n$ |
| B9.6 | Song–Liang comparison sentences | EXISTS (W3-DIST TARGET §2, read by both council seats); reading of [SL], not a theorem | TARGET.md :21-35; "display (15)" and "Corollary 1 as printed" are TARGET's readings |

### Honest limits
Statement (ii) bounds the size of the selected models, not their identity. Corollary 9C does not assert that a run's
list carries enough posterior probability, and the output does not certify it; runs that stop early and the exact
enumeration branch are not covered. Status: the masters' statuses above, with their conditions; the registry rows are
not yet recorded.

#### Update log (thm9)
- v0.1 2026-11-15: first version (CP1).
- v0.2 2026-11-15: S1 fixes none.
- v0.3 2026-11-16 (proposal, HQ card 13): placeholder → proved version from W3-DIST §1R (council R2 passed): setting,
  numbered assumptions (A1)–(A6), displays (i)–(iii), Theorems 9B and Corollary 9C, Song–Liang comparison; no
  sparsity-dependence of the rate is stated (DIST-2's rate gloss is loose: Dept RT1) (STRONGER: placeholder → theorem).
<!-- ROW thm9 END -->
````

## 3. Row 2.2 (fallback)
**Stays, as a body remark; no longer a fallback.** Reason: it covers fixed designs and the in-sample distance, which
Theorem 9 does not state, and it is recorded PROVED-CHECKED (with its conditions). Its fallback role ends because 2.1
passed council. Card text:

| 2.2 | **Body remark (no longer a fallback):** in-sample (fixed-design) Hellinger contraction of the parameter posterior, rate $M_n/\sqrt n$ with selection, $\log n/n$ without beta-min. | `W3-POST2:D@1.1.4`: "PROVED-CHECKED, conditional on SOP:TH09, SOP:TH128, W2-APP:POST, W3-POST:Thm-1" [REG-f526]. | Fixed designs and the in-sample distance, which Theorem 9 does not state. | body remark, to write at the freeze if kept |

## 4. Bridges (reader wording ⇒ W3-DIST statement)
| # | bridge | mark |
|---|---|---|
| B9.0 | renaming ($p$ ↦ $p_{\mathrm{raw}}$, $r$ ↦ $p$, $K$ ↦ $L$, $\sigma^*$ ↦ $\sigma_*$) to match NOTATION §1, §3 | identity |
| B9.1 | Theorem 9 (i), (ii), "same set", uniformity, Example = W3-DIST Theorem A :185-207 | identity (text) |
| B9.2 | display (iii) = Theorem A's "Without (A4)" sentence :200-202 as a display | identity (transcription) |
| B9.3 | Theorem 9B, Corollary 9C = W3-DIST Theorem B, Corollary C :209-238 (C's descriptive mixture sentence dropped) | identity (text) |
| B9.4 | "$p=p_{\mathrm{raw}}$ outside the exceptional sets" = W3-DIST Setup :150-152 + bridge B1 :391-395 | EXISTS-CHECKED (line-checked; council R2) |
| B9.5 | exponent in (iii): $cM\log n=c\,n\varepsilon_n^2/\log(p_{\mathrm{raw}}\vee n)$ at $\varepsilon_n^2=M\log n\log(p_{\mathrm{raw}}\vee n)/n$ | **NEW** (one line of arithmetic) |
| B9.6 | Song–Liang comparison = TARGET §2 :21-35 (a reading of [SL], read by both seats) | EXISTS (not a theorem) |

**Checks wanted:** B9.5, and one fidelity read of the reader text against §1R (B9.0–B9.3), on the D71 list above.

## 5. Changelog tag
Row thm9: placeholder → theorem, STRONGER. Card row 2.1: "in progress" → proved (status quoted, not checked here).
Row 2.2: fallback → body remark, EQUAL in content.
