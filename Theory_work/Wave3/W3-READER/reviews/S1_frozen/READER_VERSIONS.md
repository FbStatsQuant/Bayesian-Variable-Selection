# Reader versions of the headline theorems — draft v0.1 (W3-READER, CP1, 2026-11-15)

**How to read this file.** Each section has: the **reader statement** (numbered assumptions in standard terms, a
conclusion in 1–3 displays, notation from `NOTATION.md` only); **one line per assumption** (why it is there, whether it
is known to be necessary); the **master theorem** it follows from (registry id@version, file:lines, status verbatim);
the **bridges** from the reader assumptions to the master's hypotheses, each marked **EXISTS-CHECKED** (registry status
"PROVED-CHECKED"), **EXISTS-UNCHECKED** (exists, status below PROVED-CHECKED, quoted) or **NEW** (stated precisely
here, with an effort estimate); and **honest limits**. Reader statements are deliberately *stronger in hypotheses*
than the masters where that buys clarity; nothing in a conclusion goes beyond the master.

Status conventions (binding): statuses are quoted verbatim from `Theory_work/INFRA/registry/claims.tsv` (as of this
branch, base c04db8b); long council suffixes are cut after the first clause and marked "…". Nothing below
PROVED-CHECKED is called checked; "conditional on …" is carried.

**Standing assumptions and conventions** (used by every theorem below; stated once in the paper's setup section).
(S1) Model of §1 of the notation: Gaussian errors with fixed variance $\sigma_*^2>0$, independent of the design.
(S2) Asymptotics: $n\to\infty$, $p=p_n$ with $2\le p\le n^A$ for a fixed $A\ge1$ ($p\gg n$ allowed).
(S3) "The method" means the method as coded, under the standing conventions of `NOTATION.md` §5 (exact arithmetic,
shipped configuration, sufficient allocation). (S3) matters only for Theorems 5–8.

Numbering of the headline theorems (proposal; see `CLAIMS_CARD.md`):
1. Posterior concentration, fixed design — §1
2. Posterior concentration, random Gaussian design — §2
3. The rate cannot be improved — §3
4. Omitted variables (misspecification) — §4
5. The start law already concentrates — §5
6. The reported model, random Gaussian design (main theorem) — §6
7. The reported model, fixed design — §7 (honest limits: sample-level conditions)
8. Certified screening — §8
9. Distribution-level consistency — §9 (placeholder; ticket in progress)

---

## 1. Theorem 1 — Posterior concentration (fixed design)

### Reader statement
**Theorem 1.** Let the design be fixed. Assume
- **(A1) Model.** (S1) and (S2).
- **(A2) Sparsity.** $s_0\ge1$ is fixed.
- **(A3) Bounded coefficients.** $\max_{j}|\theta^*_j|\le\bar\theta$ for a fixed $\bar\theta<\infty$.
- **(A4) Sparse eigenvalue floor.** $\lambda_{\min}(\hat R_S)\ge\varphi_0^2$ for every $S\subseteq[p]$ with
  $|S|\le 2(A+1)s_0+2$, for a fixed $\varphi_0\in(0,1]$.
- **(A5) No near-collinearity among $O(\log n)$ columns.** $\lambda_{\min}(X_S^\top X_S)\ge g_0$ for every $S$ with
  $|S|\le 3(A+1)(s_0+1)\log n$, for a fixed $g_0>0$.
- **(A6) Beta-min.** $\theta^*_{\min}\ge C_\beta\,\sigma_*\sqrt{\log n/n}$ with a fixed $C_\beta$ such that
  $C_\beta^2\varphi_0^2>c_0(s_0,A)$; or $\theta^*_{\min}\sqrt{n/\log n}\to\infty$.

Then
$$
1-\pi(S_0\mid y)=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big),\qquad
P\big(\mathrm{HPM}=\mathrm{MPM}=S_0\big)\to1,\qquad
\max_{j\le p}\big|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}\big|\le 1-\pi(S_0\mid y).
$$

*Remarks (go to the paper's remarks, not the statement).* (i) The last inequality holds for every data set; with the
first display it gives sensitivity and specificity of all PIPs at rate $\sqrt{\log n/n}$, uniformly in $j$.
(ii) Without (A6): $\pi(S\supsetneq S_0\mid y)=O_P(\sqrt{\log n/n})$ (no over-fitting mass) and every truth with
$\theta_j^{*2}\ge c\,\sigma_*^2\log n/(n\varphi_0^2)$, $c>c_0$, has $1-\mathrm{PIP}_j=O_P(\sqrt{\log n/n})$; specificity can
fail without beta-min (numerical counterexample). (iii) $c_0(s_0,A)=\max\{4C_*,32[s_0(A+1)+2]\}$ is a proof constant
(not sharp). (iv) (A3) is used only through the energy bound $\|X\theta^*\|^2\le n s_0^2\bar\theta^2$; any bound
$\|X\theta^*\|^2\le nM$ suffices. (v) Models of size $\ge 3(A+1)(s_0+1)\log n$ carry posterior mass $O_P(n^{-1/2})$ with
no eigenvalue condition at all (size-tail lemma; separate statement).

### Why each assumption, and is it necessary
- (A1) Gaussian errors give exact $\chi^2$ laws for the score differences. Necessity open; every comparable Bayesian
  selection theorem assumes it. $p\le n^A$ enters through union bounds over models of size $O(\log n)$; open.
- (A2) Fixed $s_0$ keeps combinatorial constants bounded. Close to necessary for this rate: on *every* design the rate
  $\sqrt{\log n/n}$ forces $s_0=O(\sqrt{\log n})$, and $\pi(S_0\mid y)\to1$ forces $s_0=o(\sqrt n)$ (Theorem 3).
- (A3) Bounded signal energy keeps the posterior of the noise variance on scale. Believed improvable (sub-linear growth);
  some control of the coefficients is necessary for the size-tail step (explicit counterexample).
- (A4) Lets the posterior separate $S_0$ from under-fitted models of bounded size. The part *anchored at $S_0$* is
  needed at the beta-min scale (numerics); the floor on null-only directions looks removable (numerics; an unchecked
  strengthening replaces it by an identifiability margin).
- (A5) Excludes exact (or near-exact, $\lambda_{\min}<g_0$ unnormalised) linear dependence among $O(\log n)$ columns, so
  over-fitted models pay their full Occam factor. Note the floor is $g_0/(n-1)$ on the correlation scale: it vanishes.
  Looks improvable (numerics); an unchecked strengthening replaces it by a weaker Occam-sum condition.
- (A6) The signal must beat the prior cost of one variable plus a $\chi^2$ fluctuation, both of order $\log n$. The
  order $\sqrt{\log n/n}$ is necessary by numerics and a leading-order heuristic (not proved); the constant $c_0$ is a
  proof artefact.

### Master theorem
`W3-POST:Thm-1@1.0.0` (= `SOP:TH09@1.0.0`, T03♯ with the SL0/SL1 consequences), `Theory_work/Wave3/W3-POST/STATEMENT.md:61-100`
(hypotheses :63-75; conclusions 1–3 at :80-85).
Registry status, verbatim: **"T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"**. Council W3-POST C3 passed
(Astra 8.8 / Opus 8.7; briefing 11-13), but the registry label is **not** PROVED-CHECKED. Theorem 1 is therefore
"proved, verified same-family and cross-family, council-passed; registry label pending".

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B1.1 | (A3) ⇒ (E) $\|\mu\|^2\le nM$, $M=s_0^2\bar\theta^2$ | NEW (one line) | $\|X\theta^*\|\le\sum_{j\in S_0}|\theta^*_j|\,\|x_j\|\le s_0\bar\theta\sqrt{n-1}$. Same remark at W3-POST STATEMENT.md:57. |
| B1.2 | (A4) ⇒ (F_λ) = SE_λ(j₀) | NEW (one line) | Every $S_0\cup J$ with $|J|\le j_0=\lceil(2A+1)s_0\rceil+1$ has $|S_0\cup J|\le(2A+2)s_0+2$. |
| B1.3 | (A5) ⇒ (F_w) = SE_w(m♯_n; g₀) | EXISTS-UNCHECKED + NEW arithmetic | $m^\sharp_n\le s_0+\lceil(\log\binom{p}{s_0}+\tfrac{s_0+1}2\log n+\tfrac12\log n)/\log2\rceil$ ([T03R] E2(ii), stated at W3-POST STATEMENT.md:38-39; inside SOP:TH09, status above). With $\binom{p}{s_0}\le n^{As_0}$ and $n\ge3$: $s_0+m^\sharp_n\le(2s_0+1)\log n+1.45(As_0+\tfrac{s_0}2+1)\log n\le3(A+1)(s_0+1)\log n$. Checked numerically on $A\in[1,20]$, $s_0\le39$, $n\in[3,10^{15}]$ (LOG 2026-11-15). |
| B1.4 | (A6) ⇔ (BM) | identity | (A6) is BM($c$) with $c=C_\beta^2\varphi_0^2$, or BM-∞. |
| B1.5 | δ_n rate ⇒ HPM/MPM/PIP clauses | inside the master | SL0/SL1, deterministic (W3-POST STATEMENT.md:121). |

**Effort:** B1.1–B1.4 are a half page; one Sol line check.

### Honest limits
None for the statement: every assumption is primitive. The beta-min constant is not explicit in a friendly form
($c_0\ge128$ at $s_0=A=1$); the paper should say "a sufficiently large constant depending only on $(s_0,A,\varphi_0)$"
in the statement and give $c_0$ in a remark.

---

## 2. Theorem 2 — Posterior concentration (random Gaussian design)

### Reader statement
**Theorem 2.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a correlation matrix, and
assume
- **(A1) Model.** (S1) and (S2).
- **(A2) Sparsity and fixed signals.** $s_0\ge1$ is fixed and $b_{\mathrm{lo}}\le|\beta^*_j|\le b_{\mathrm{hi}}$ for
  $j\in S_0$, with fixed $0<b_{\mathrm{lo}}\le b_{\mathrm{hi}}<\infty$.
- **(A3) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge\varphi^2$ for every $S$ with
  $|S|\le 5(A+1)(s_0+1)\log n$, for a fixed $\varphi\in(0,1]$ (for instance, $\lambda_{\min}(\Sigma_n)\ge\varphi^2$).

Then, under the joint law of design and noise, the three conclusions of Theorem 1 hold:
$$
1-\pi(S_0\mid y)=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big),\qquad P(\mathrm{HPM}=\mathrm{MPM}=S_0)\to1,\qquad
\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|=O_P\Big(\sqrt{\tfrac{\log n}{n}}\Big).
$$

*Remarks.* No upper eigenvalue bound on $\Sigma_n$ and no beta-min beyond (A2) are needed; $p\gg n$ is allowed. The
master allows the floor on sets of size $O(\log n)$ to vanish slowly ($\psi_n\gg(\log n)^{3/2}/\sqrt n$); the reader
version uses a constant for simplicity.

### Why each assumption
- (A1) as Theorem 1.
- (A2) Fixed nonzero coefficients sit far above the $\sqrt{\log n/n}$ detection level, so no separate beta-min is
  needed; fixed $s_0$ as in Theorem 1. Without the lower bound $b_{\mathrm{lo}}$, the no-over-fitting and strong-signal
  clauses still hold (remark (ii) of Theorem 1).
- (A3) Transfers to the sample floors (A4)–(A5) of Theorem 1 with probability $\to1$ (entrywise Gram concentration).
  The small-set part is needed (anchored floors); the $O(\log n)$ part is improvable (the entrywise transfer is crude).
  Gaussian rows are used only for the entrywise concentration step; sub-Gaussian rows are expected to work (not
  claimed).

### Master theorem
`W3-POST:Thm-1@1.0.0` item 6 (random-design interface), `Theory_work/Wave3/W3-POST/STATEMENT.md:95-100`, status as in §1;
with `W2-APP:POST@1.0.1`, `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:27-33`, status verbatim **"PROVED (by this seat,
unchecked); R02 VERIFIED-WITH-AMENDMENTS, applied"**, and its restatement `W3-POST:Cor-1R@1.0.0`
(`W3-POST/STATEMENT.md:106-118`), status **"PROVED (by this seat, unchecked)"**.

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B2.1 | (A3) ⇒ LSF (i) and (ii) with $\psi_n=\varphi^2$ | NEW arithmetic | LSF asks the floor on $|S|\le\min(p,s_0+j_0)$ and on $|S|\le\bar k_n=\min\{p,s_0+\max(j_0,\bar m_n)\}$, $\bar m_n=\lceil[s_0(A\log n+\log2)+\log2+\tfrac{s_0+2}2\log n]/\log\tfrac32\rceil$ (L1_POST.md:20-25). For $n\ge3$: $\bar k_n\le(2.47As_0+3.7s_0+5.9)\log n\le5(A+1)(s_0+1)\log n$, and $s_0+j_0\le(2A+2)s_0+2$ is smaller. Checked numerically (LOG). |
| B2.2 | LSF + Gaussian rows + fixed coefficients ⇒ events $\mathcal A_n$, $P(\mathcal A_n)\to1$, carrying (E), (F_λ), (F_w), BM-∞ with common constants | **EXISTS-UNCHECKED** | `W2-APP:POST@1.0.1` part (a). Raw-scale coefficients are covered (L1_POST.md:12-15, event $\mathcal H_n$). **The weak point of every random-design headline** (Theorems 2, 4b, 6 depend on it). Already queued by HQ: Tier-B Sol line check of `L1_POST.md`. |
| B2.3 | events ⇒ conclusions under the joint law | inside the master | Theorem 1 item 6 (diagonal transfer). |

**Effort:** B2.1 half a page; B2.2 one Sol line check (~84-line lemma), HQ-scheduled.

### Honest limits
None for the statement. Its status is the weakest link: until `W2-APP:POST` is line-checked, Theorem 2 must be
presented as "proved; one input lemma not yet independently checked".

---

## 3. Theorem 3 — The rate cannot be improved

### Reader statement
**Theorem 3.** (a) *(Every design.)* For every $n\ge3$, every standardised design with $p\ge2$, every response and every
model $S$ with $|S|\le\min(K-1,p/2)$,
$$
\pi(S\mid y)\ \le\ \Big(1+\frac{|S|+1}{3\sqrt n}\Big)^{-1}.
$$
(b) *(Orthogonal or Gaussian null columns.)* Assume (S1), $s_0$ fixed, $p\to\infty$, $\|X\theta^*\|^2\le nM$ and
$\|\theta^*\|^2\le nM'$ with fixed $M,M'$, and either
- **(N-orth)** the columns outside $S_0$ are mutually orthogonal and orthogonal to the columns in $S_0$; or
- **(N-gauss)** the raw columns outside $S_0$ have i.i.d. $N(0,1)$ entries, independent of $X^{\mathrm r}_{S_0}$ and
  $\varepsilon$, and $p\le n^A$.

Then
$$
1-\pi(S_0\mid y)\ \ge\ (1-o_P(1))\,(s_0+1)\sqrt{\frac{\log p}{\pi n}}.
$$

*Consequences (remarks).* By (a), no design gives a rate faster than $n^{-1/2}$; $\pi(S_0\mid y)\to1$ requires
$s_0=o(\sqrt n)$; the rate $\sqrt{\log n/n}$ requires $s_0=O(\sqrt{\log n})$. By (b) with $p=n^a$, the factor
$\sqrt{\log n}$ is attained: on these designs, which satisfy the assumptions of Theorems 1–2, the rate
$\sqrt{\log n/n}$ is exact whenever $\log p\asymp\log n$ (this last sentence is conditional on Theorems 1 and 2).

### Why each assumption
(a) has none: it is a deterministic property of the prior and the Occam factor (each of the $p-s_0$ one-variable
supersets keeps posterior odds at least of order $n^{-1/2}/p$). (b): the witness conditions make the $p$ one-variable
supersets behave as nearly independent $\chi^2_1$ competitors, whose maximum gives the $\sqrt{\log p}$; energy and
coefficient bounds keep the variance posterior on scale. These are witnesses, not claimed necessary.

### Master theorems
`W3-PSHARP:B@1.0.0`, `Theory_work/Wave3/W3-PSHARP/STATEMENT.md:90-114` (display at :94-96, consequence (B1) at :99), and
`W3-PSHARP:A@1.0.0`, same file :46-77 (Corollary A1 at :71-73; (N-gauss) is the example at :59-60 of (W-sph)). Status of
both, verbatim: **"PROVED-CHECKED; council R2, MANIFEST 4513e05a…, sol=9.2 PASS, opus=9.3 PASS; …"**.

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B3.1 | (a) from Corollary B: $c(p,s_0)\ge(s_0+1)/3$ for $s_0\le p/2$ | EXISTS-CHECKED | Inside `W3-PSHARP:B` (:95, :99). Reader version renames $S_0$ to any $S$ (Corollary B holds for every subset, :92-93). |
| B3.2 | (N-gauss) ⇒ (W-sph) | EXISTS-CHECKED (example in the claim text) + NEW one line | (W-sph) asks $(\log N_n)^2=o(n)$ and $(r_0+1)\log N_n=o(n)$; with $N_n\le p\le n^A$ and $s_0$ fixed both hold. |

### Honest limits
None. Note for the text: the expectation form of (b) for every $p$ (sharp2 rider T12) is not yet proved.

---

## 4. Theorem 4 — Omitted variables (misspecification)

### Reader statement
**Theorem 4** (candidate-only fit with omitted predictors). Let the rows $(x_{\mathcal C,i},x_{\mathcal M,i})$ be i.i.d.
$N(m,\Sigma)$ with $\Sigma_{\mathcal C\mathcal C}\succ0$, and let
$y^{\mathrm r}_i=\alpha+x_{\mathcal C,i}^\top\beta_{\mathcal C}+x_{\mathcal M,i}^\top\beta_{\mathcal M}+\varepsilon_i$
with $\varepsilon\sim N_n(0,\sigma^2I)$ independent of the rows. The method is run on $(x_{\mathcal C},y^{\mathrm r})$
only ($p$ = number of candidates). Define the **projected coefficient** and **residual variance**
$$
\beta^{\mathcal C}:=\beta_{\mathcal C}+\Sigma_{\mathcal C\mathcal C}^{-1}\Sigma_{\mathcal C\mathcal M}\beta_{\mathcal M},\qquad
\sigma^2_{\mathcal C}:=\sigma^2+\beta_{\mathcal M}^\top\big(\Sigma_{\mathcal M\mathcal M}-\Sigma_{\mathcal M\mathcal C}\Sigma_{\mathcal C\mathcal C}^{-1}\Sigma_{\mathcal C\mathcal M}\big)\beta_{\mathcal M}>0,
$$
and $S_0^{\mathcal C}:=\operatorname{supp}\beta^{\mathcal C}$, $s:=|S_0^{\mathcal C}|$. Assume
- **(A1) Dimension and sparsity.** $2\le p\le n^A$; $s\ge1$ fixed.
- **(A2) Floor.** $\lambda_{\min}(\Sigma_{TT})\ge c$ for every $T\subseteq\mathcal C$ with $|T|\le3(A+1)(s+1)\log n$, and
  $\max_j\Sigma_{jj}\le C_0$, with fixed $c,C_0>0$.
- **(A3) Signal relative to the residual variance.**
  $\beta^{\mathcal C\top}\Sigma_{\mathcal C\mathcal C}\beta^{\mathcal C}\le M_0\,\sigma^2_{\mathcal C}$ and
  $n\min_{j\in S_0^{\mathcal C}}\Sigma_{jj}(\beta^{\mathcal C}_j)^2/(\sigma^2_{\mathcal C}\log n)\to\infty$.

No condition is placed on how $\sigma^2$ or the omitted part vary with $n$. Then
$$
E\big[1-\pi(S_0^{\mathcal C}\mid y)\big]=O\Big(\sqrt{\tfrac{\log n}{n}}\Big),\qquad
P\big(\mathrm{HPM}\neq S_0^{\mathcal C}\big)=O\Big(\sqrt{\tfrac{\log n}{n}}\Big).
$$
*Remark.* $N(\alpha'+x_{\mathcal C}^\top\beta^{\mathcal C},\sigma^2_{\mathcal C})$ is the conditional law of $y$ given the
candidates, hence the Kullback–Leibler projection of the truth onto the candidate linear models: the posterior
concentrates on the support of the best candidate predictor. A fixed-design version (uniform over the residual
variance) and a Hellinger version exist (remarks in the paper; same status).

### Why each assumption
- (A1) as Theorem 1.
- (A2) Population floors transferred to the sample (as Theorem 2), on the candidates only.
- (A3) Everything is measured relative to the residual variance $\sigma^2_{\mathcal C}$, because the method is exactly
  invariant to shifts and rescaling of $y$. The energy bound cannot be dropped (numerical witness); the beta-min order is
  that of Theorem 1.
- Gaussian rows: they make the omitted part Gaussian given the candidates. Arbitrary non-Gaussian residual laws are
  outside this result.

### Master theorem
`W3-MISR:Cor-G(b)@1.0.0`, `Theory_work/Wave3/W3-MISR/STATEMENT.md:171-174` (with (a) at :164-170), status verbatim:
**"PROVED-CHECKED, conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0, C-MIS:Prop-P, SOP:TH09, SOP:TH128,
C-MIS:GDb; input versions …; council R2, MANIFEST 217d6708…, sol=9.2 PASS, opus=8.9 PASS; …"**.
Inputs below PROVED-CHECKED, verbatim: `W3-POST2:C@1.0.0`, `W3-POST2:E@1.0.0`, `W3-POST2:A1@1.0.0`,
`W3-POST2:A0@1.0.0`: **"PROVED (by this seat, unchecked)"** (council C1 8.6/8.6, but acceptance STOPPED 11-15: no
frozen C1 manifest, and the repaired D(b) post-dates C1 — HQ_DECISIONS 2026-11-15); `C-MIS:Prop-P@1.0.0`: **"R02
VERIFIED; R04 wording fixes checked in R05; council PASS"**; `C-MIS:GD(b)@1.0.0`: **"R02 VERIFIED-WITH-AMENDMENTS
(applied); council PASS"**; `SOP:TH09`, `SOP:TH128` as in §1.
Fixed-design form: `W3-MISR:MIS(i)@1.0.0` (:110-123), **"PROVED-CHECKED, conditional on W3-POST2:C; …"**.

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B4.1 | (A2) size $3(A+1)(s+1)\log n$ ⇒ Cor-G(b)'s $|T|\le s+\max(j_0,m^\sharp_n)$ | NEW arithmetic | As B1.3 with $s_0:=s$ (and $s+j_0\le(2A+2)s+2$). $m^\sharp_n$ here is computed with $p=|\mathcal C|$. |
| B4.2 | (A3) = Cor-G(b)'s signal conditions | identity | :172-173. |
| B4.3 | POST2 C, E, A1, A0 | **EXISTS-UNCHECKED** | Needs the council diff round HQ already identified (frozen manifest + per-claim tables, v4 §5.5). Highest-value bookkeeping item for the card. |

### Honest limits
The statement is primitive. The status is not: Theorem 4 is "proved and council-passed, conditional on four
council-passed but not accepted posterior refinements". The card must say so until the POST2 diff round passes.

---

## 5. Theorem 5 — The start law already concentrates

### Reader statement
**Theorem 5.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$, $\Sigma_n$ a correlation matrix, and let
$y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with a deterministic $\theta^*$ (signal fixed on the standardised
scale). Assume
- **(A1) Model.** (S1), (S2), and $p>s_0$.
- **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  $S_0$.
- **(A3) Small-set floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c$ for every $|S|\le16+s_0$.
- **(A4) Visibility.** For every $j\in S_0$ and every $U\not\ni j$ with $|U|\le15$:
  $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a$, for a fixed $a>0$.
- **(A5) No leakage.** For every $l\notin S_0$ there is a set $H_l\supseteq\{l\}\cup S_0$ with
  $|H_l|\le(\log n)^{\kappa}$ such that, for every $U\not\ni l$ with $|U|\le15$ and $U_0:=U\cap H_l$:
  $|\operatorname{Cov}(W_l,W_j\mid W_{U_0})|\le Cn^{-1/2}$ for $j\in S_0\setminus U_0$, and
  $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|,|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\le r_n$ for $v\in U\setminus H_l$,
  $j\in S_0\setminus U_0$, where $r_n(n\log n)^{1/4}\to0$.

Then for every $c<\tfrac12$,
$$
P\big(\pi_0(S_0)\ge1-n^{-c}\big)\to1,
$$
and the exponent $\tfrac12$ cannot be improved: $1-\pi_0(S_0)\ge\tfrac13(n+1)^{-1/2}$ for every data set.

*With leakage (remark or second display).* If (A5) holds with $S_0$ replaced by a deterministic $Q\supseteq S_0$,
$|Q|\le K$ (columns outside $Q$ do not leak), then
$P\big(\pi_0(\mathcal L(Q))\ge1-(|Q|+1)n^{-1/2}e^{C\sqrt{\log n}}\big)\to1$; for $|Q|\le n^{1/2-\epsilon}$ this is
$\ge1-n^{-c}$ for every $c<\epsilon$.

### Why each assumption
- (A3) Block regressions of at most 16 columns are well posed. Necessity open.
- (A4) Each truth, alone, improves the fit of every small model it is missing from: then the start law, which only sees
  within-block interactions, still ranks $S_0$ first. The level is sharp in the fixed-design analogue (threshold
  $1+2A$); masked truths violate it and are treated separately.
- (A5) Nulls must not imitate truths within the start law's block view; the partial-covariance level $n^{-1/2}$ is a
  proof threshold (numerics show no cliff there); localisation is needed because the blocks are data-dependent.
- The exponent $\tfrac12$ is optimal (deterministic floor).

### Master theorem
`W3-START2:START-R@1.0.0`, `Theory_work/Wave3/W3-START2/STATEMENT.md:134-145` ((L-R⁺) at :63-73; (FL-R16), (V-R) at
`W3-START/STATEMENT.md:160-162`), status **"PROVED-CHECKED"** (unconditional). Floor: `W3-START:FLOOR@1.0.0`
(`W3-START/STATEMENT.md:241-243`), **"PROVED-CHECKED"**. Bridge (B-R⁺): `W3-START2:BR@1.0.0`, **"PROVED-CHECKED"**.

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B5.1 | (A3)–(A5) = (FL-R16), (V-R), (L-R⁺) with $Q=S_0$ | identity | word for word. |
| B5.2 | floor $\tfrac13(n+1)^{-1/2}$ | EXISTS-CHECKED | (T0) holds when $s_0<K$, i.e. for all large $n$ since $p>s_0$. |

### Honest limits
The statement is in population terms but (A5) is long. Two presentation options for HQ: (i) state the theorem with
$Q=S_0$ only (as above) and move the leakage form to a remark; (ii) a shorter sufficient condition (e.g. exact conditional uncorrelatedness of nulls and truths) does **not**
immediately give the localisation clause, because that clause also constrains columns outside $H_l$; no such
simplification is proposed without a proof. Recommendation: option (i).
Also: this theorem is about an internal object of the method; it belongs in the paper's method section, not in the
abstract.

---

## 6. Theorem 6 — The reported model equals the truth (random Gaussian design; main theorem)

### Reader statement
**Theorem 6.** Let the rows of $X^{\mathrm r}$ be i.i.d. $N_p(m_n,\Sigma_n)$ with $\Sigma_n$ a positive definite
correlation matrix, and $y^{\mathrm r}=\alpha\mathbf 1+X\theta^*+\varepsilon$ with deterministic $\theta^*$. Fix
$b\in(0,\tfrac12)$ and $\rho>0$ with $15\rho+b<\tfrac12$. Assume
- **(A1) Model.** (S1), (S2) ($p\gg n$ allowed), (S3).
- **(A2) Sparsity and fixed signals.** $s_0\ge1$ fixed; $\theta_{\mathrm{lo}}\le|\theta^*_j|\le\theta_{\mathrm{hi}}$ on
  $S_0$.
- **(A3) Visibility.** $|\operatorname{Cov}(W_j,\,W^\top\theta^*\mid W_U)|\ge a>0$ for every $j\in S_0$ and every
  $U\not\ni j$ with $|U|\le15$.
- **(A4) Polynomial leakage set.** There is a deterministic $Q\supseteq S_0$ with $|Q|\le n^b$ and, for large $n$,
  $|Q|\le K$ and ($Q=[p]$ or $K\ge2|Q|+32s_0+1$), such that:
  (i) *(no leak outside $Q$)* $|\operatorname{Cov}(W_l,W_j\mid W_U)|=o\big(\sqrt{\log n/n}\big)$ uniformly over
  $l\notin Q$, $j\in S_0\setminus U$, $|U|\le15$;
  (ii) *(locality)* every $l\notin Q$ has a deterministic $H_l\supseteq\{l\}\cup S_0$, $|H_l|\le n^{\rho}$, such that
  for every $U\not\ni l$ with $|U|\le15$ and $U_0:=U\cap H_l$: $|\operatorname{Cov}(W_l,W_v\mid W_{U_0})|\to0$ and
  $|\operatorname{Cov}(W_j,W_v\mid W_{U_0})|\to0$ uniformly over $v\in U\setminus H_l$, $j\in S_0\setminus U_0$.
- **(A5) Population sparse eigenvalue floor.** $\lambda_{\min}(\Sigma_{n,S})\ge c>0$ for every $S$ with
  $|S|\le5(A+1)(s_0+1)\log n$ and for every $S=Q\cup\{l\}$, $l\in[p]$.
- **(A6) Local regressions within $Q$.** For every $l\in[p]$ there is $N_l\subseteq Q\setminus\{l\}$ with
  $|N_l|=o(\log n)$ such that
  $\|\bar\beta_{T,l}-\bar\beta_{T\cap N_l,l}\|_1\le L_n$ for every $T$ with $S_0\subseteq T\subseteq Q$, $l\notin T$,
  where $L_n\to0$ and $L_n^2\log(|Q|+1)=o(\log n)$ (bars: population regression coefficients, zero-padded).

Then, under the joint law of design and noise and for every seed,
$$
P(\text{the run produces output})=1\ \ \text{for every }n,\qquad P(\hat S=S_0)\to1 ,
$$
and more strongly there are data events $\mathcal G_n$ with $P(\mathcal G_n)\to1$ on which **every** run that produces
output reports $\hat S=S_0$, whatever its seed and the outcome of its internal calibration.

*Remarks.* (i) On $\mathcal G_n$ the local search from the start mode only deletes the spurious members of the start
mode, one per move, at most $n^b$ moves, and certifies $S_0$; its move cap never binds. (ii) The polylogarithmic case
$|Q|\le(\log n)^{\kappa}$ is a special case (the earlier version of the theorem). (iii) Examples (never hypotheses):
metric-local correlation, polynomial correlation decay of exponent $\alpha>2$ (example status unchecked), one-factor
blocks.

### Why each assumption
- (A2) Fixed signals give the posterior input (Theorem 2) and the truth-removal margin.
- (A3) No truth can be explained away by at most 15 others: every truth enters the start mode. Needed in this form for
  the start; masked designs violate it and are separate examples (the method still works there, by other theorems).
- (A4) Columns outside $Q$ never enter the start mode; columns inside $Q$ may, and the search removes them. $b<\tfrac12$
  is where the prior-plus-Occam penalty of one more variable ($\approx\log p+\tfrac12\log n$) stops dominating the best
  of $p$ noise gains ($\approx\log p$) at model size $\approx\sqrt n$; beyond it the route's key events are expected to
  fail (heuristic; whether the conclusion fails is open). Locality (ii) is needed because the method's blocks are
  data-dependent.
- (A5) Floors make block regressions and the lattice directions well defined; the floor on $Q\cup\{l\}$ is a floor on
  sets of polynomial size; necessity not asserted.
- (A6) Guarantees that no addition improves the score anywhere on the lattice of $Q$, so the search goes straight down
  to $S_0$. It is a sufficient form of a width condition that is *forced* by this route (if the width gap diverges the
  other way, no-addition fails w.p. $\to1$). Not known to be necessary for the conclusion.

### Master theorems
1. `W3-RM2:RM2-R@1.0.0`, `Theory_work/Wave3/W3-RM2/STATEMENT.md:216-218` (assumptions :172-202), status verbatim
   **"PROVED-CHECKED, conditional on W2-APP:POST; input versions W2-APP:POST@1.0.1; council R1, MANIFEST 00bbeab8…,
   astra=9.5 PASS, opus=8.8 PASS; …"**.
2. `W3-RM:RM-0@1.0.0`, `Theory_work/Wave3/W3-RM/STATEMENT.md:160-176` (pathwise reduction; common good event
   :173-175), **"PROVED-CHECKED"**; `W3-RM:E4@1.0.0` (:219-230), **"PROVED-CHECKED"**.
3. `W2-UNI:F-UNI@1.1.0`, `Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:15-21` (delivery), **"PROVED-CHECKED"**
   (registry; the lemma file's own header still says "PROVED (by this seat, unchecked)" — bookkeeping note for HQ).

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B6.1 | (A5) ⇒ (T1-R) (= LSF with $\psi_n=c$) and (FL-R) | NEW arithmetic | As B2.1; and $16+s_0\le5(A+1)(s_0+1)\log n$ for $n\ge3$, $s_0\ge1$. |
| B6.2 | (A4)(i),(ii) = (L-R^b) | identity | (L-gain-R) with $\varpi_n=o(\sqrt{\log n/n})$; (L-loc-R) with $r_n\to0$ (RM2 STATEMENT.md:176-189). (L-feas) carried in (A4). |
| B6.3 | (A6) + (A5) ⇒ (D-loc^b) incl. its variance clause | **NEW** (one paragraph; proof below) | (D-loc^b) = RM (D-loc) (RM STATEMENT.md:154-156) with $L_n^2\log(|Q|+1)=o(\log n)$; its second clause $\operatorname{Var}(W_l\mid W_{T\cap N_l})\le(1+\eta_n)\operatorname{Var}(W_l\mid W_T)$, $\eta_n\to0$, follows from (A6) and (A5): see proof. |
| B6.4 | (D-loc^b) ⇒ (D-R^b) ⇒ (W-R) | EXISTS-CHECKED | `W3-RM2:D-to-W@1.0.0`, "PROVED-CHECKED; council R1, …" (STATEMENT.md:256, (C3)/(P9)). |
| B6.5 | (T1-R) ⇒ posterior input [POST] | EXISTS-CHECKED, conditional | `W3-RM2:POST-R@1.0.0`, "PROVED-CHECKED, conditional on W2-APP:POST; …" ⇐ B2.2 (**EXISTS-UNCHECKED**). |
| B6.6 | RM2-R conclusions ⇒ F-UNI premises (S), (P); (V) input validity from "$\Sigma_n$ positive definite" | **NEW** (assembly, one paragraph) | (S): $P(\mathrm{Sand}\cap\mathrm{NA}\cap\mathrm{TL})\ge1-\sum P(\cdot^c)\to1$ from [SAND(Q)], [NA(Q)], [TL(Q)]; (P) = [POST]; (V) = "(R) with $\lambda_{\min}(\Sigma_n)>0$". Must also check that F-UNI's method premises (tier-1 fallback freezing, LS0 cap $\ell_n+|\tilde S_0|$, allocation inequalities) match (S3) and RM2's configuration; the fallback is the shipped default (`v3_calib.R:141-144`). |
| B6.7 | standardised-signal convention | limit | The masters take $\theta^*$ deterministic (Setting R). A raw-scale version (fixed $\beta^*$) would need a **NEW** bridge (medium; the population conditions involve $\theta^*$). Not proposed for CP1. |

**Proof of B6.3.** Fix $l$ and $T$ in the lattice with $l\notin T$, put $A:=T\cap N_l\subseteq T$ and
$d:=\bar\beta_{T,l}-\bar\beta_{A,l}$ (supported in $T$, $\|d\|_1\le L_n$). Since $W_l-W_T^\top\beta_{T,l}$ is
uncorrelated with $W_T$,
$\operatorname{Var}(W_l-W_A^\top\beta_{A,l})=\operatorname{Var}(W_l\mid W_T)+d^\top\Sigma_{n,TT}d$. Unit diagonal gives
$|\Sigma_{ik}|\le1$, so $d^\top\Sigma_{n,TT}d\le\|d\|_1^2\le L_n^2$; and
$\operatorname{Var}(W_l\mid W_T)\ge\lambda_{\min}(\Sigma_{n,T\cup\{l\}})\ge c$ by (A5) (interlacing, $T\cup\{l\}\subseteq Q\cup\{l\}$).
Hence $\operatorname{Var}(W_l\mid W_A)\le(1+L_n^2/c)\operatorname{Var}(W_l\mid W_T)$ with $\eta_n:=L_n^2/c\to0$ by
(A6). (This is why (A6) asks $L_n\to0$ besides $L_n^2\log(|Q|+1)=o(\log n)$; the two coincide when $|Q|\ge n^{b'}$ for a
fixed $b'>0$. When $|Q|$ is only polylogarithmic the master allows a bounded $L_n$ with the variance clause assumed
separately; the reader version gives that case up for a shorter statement.) ∎

**Effort:** B6.1, B6.3 half a page; B6.6 one page with a premise-by-premise table; all three need one Sol line check.

### Honest limits
All assumptions are on the population law, but (A4) and (A6) are long and specific (15 = block size − 1; partial
covariances; local regressions). They are the natural price of a statement about a *search* algorithm: they say that
the signal is not masked, that what can imitate it is confined to a set of size $n^b$, and that within that set
regressions are local. HQ choices: keep them as stated (faithful), or state Theorem 6 in words in the abstract
("under visibility, polynomially bounded leakage and local dependence") with the full list in the theorem.

---

## 7. Theorem 7 — The reported model equals the truth (fixed design)

### Reader statement (two sufficient versions)
**Theorem 7.** Let the design be fixed. Assume
- **(A1) Model and posterior conditions.** (S1), (S2), (S3); (A2)–(A5) of Theorem 1; and strong signals
  $\theta^*_{\min}\sqrt{n/\log n}\to\infty$.
- **(A2) Floors.** $\lambda_{\min}(\hat R_T)\ge\varphi_0^2$ for every $T$ with $|T|\le16$ and for every
  $T=Q\cup\{l\}$, $l\in[p]$ ($Q$ as in (A4)).
- **(A3) Visibility.** There is a deterministic $M_n\to\infty$ such that $\delta^2_{U,j}\ge M_n\log n$ for every
  $j\in S_0$ and every $U\not\ni j$ with $|U|\le15$.
- **(A4) Bounded leakage.** There are a deterministic $Q\supseteq S_0$ (with $|Q|\le K$ and ($Q=[p]$ or
  $K\ge2|Q|+32s_0+1$) for large $n$) and a fixed $\eta\in[0,\eta_A)$, $\eta_A:=(\sqrt{2A+1}-\sqrt{2A})^2$, such that
  $\delta^2_{U,l}\le\eta\,\tau^2_U\log n$ for every $l\notin Q$ and every $U\not\ni l$ with $|U|\le15$.
- **(A5) Size of the leakage set**, one of:
  (a) $|Q\setminus S_0|\le(1-\delta)\log n$ for a fixed $\delta\in(0,1)$; or
  (b) $|Q|\le n^b$ with $b<\tfrac12-\tfrac\eta2-\sqrt{2A\eta}$; $\theta^{*2}_{\min}\,n/(|Q|+\log n)\to\infty$; and *local
  regressions*: for every $l$ a set $N_l\subseteq Q\setminus\{l\}$ with $|N_l|\le h\log_2n$, $h+b<\tfrac12$, and
  $L_n\to0$ with $L_n^2\log(|Q|+1)=o(\log n)$, such that
  $\|\hat\beta_{T,l}-\hat\beta_{T\cap N_l,l}\|_1\le L_n$ for every $T$ with $S_0\subseteq T\subseteq Q$, $|T|<K$,
  $l\notin T$.

Then there are data events $\mathcal G_n$, $P(\mathcal G_n)\to1$, on which every run that produces output reports
$\hat S=S_0$, for every seed and calibration outcome; and
$$
P(\text{the run produces output})=1,\qquad P(\hat S=S_0)\to1 .
$$

### Intuition for each condition (for the paper's text)
- *Visibility (A3).* Each truth, added alone to any small model that misses it, explains $\gg\log n$ more signal —
  more than the prior charges for one variable. So the start law, which judges variables block by block, never leaves a
  truth out.
- *Bounded leakage (A4).* Outside $Q$, no column, added to any small model, explains more than a fraction $\eta$ of
  $\log n$ residual-variance units; such columns never look like signal and stay out of the start mode.
- *Size of $Q$ (A5).* Columns of $Q$ may enter the start mode. The local search then removes them one at a time; for that
  the score must not reward *adding* any column at any model between $S_0$ and $Q$. This holds automatically when $Q$
  has fewer than $\log n$ extra columns (a), or when every column's regression on such models is carried by a few
  ($O(\log n)$) members of $Q$ (b).
- *Floors (A2).* Regressions on blocks and on $Q\cup\{l\}$ are well posed.

### Master theorem
`W3-RM2:RM2-F@1.0.0`, `Theory_work/Wave3/W3-RM2/STATEMENT.md:206-214` (assumptions :126-170), status verbatim
**"PROVED-CHECKED, conditional on SOP:TH09; input versions SOP:TH09@1.0.0; council R1, MANIFEST 00bbeab8…, astra=9.5
PASS, opus=8.8 PASS; …"**; with `W3-RM:RM-0@1.0.0` and `W2-UNI:F-UNI@1.1.0` as in §6 (input validity "(E) with
nonconstant raw columns").

### Bridges
| # | Bridge | Mark | Detail |
|---|---|---|---|
| B7.1 | (A1) ⇒ (T1-F) | as B1.1–B1.4 (with BM-∞) | (T1-F) uses BM-∞ (RM STATEMENT.md:91-92). |
| B7.2 | (A5)(a) ⇒ (L-size^b) for every small $b>0$, (W) via (W-χ), (BM-W) = BM-∞ | EXISTS-CHECKED | `W3-RM2:W-suff@1.0.0` (C3)(c) "(W-χ) ⇒ (W-δ)"; (BM-W) reduces to BM-∞ when $d_n^2=O(\log n)$ (STATEMENT.md:137-139). $b<\beta(\eta,A)$ is possible because $\eta<\eta_A$. |
| B7.3 | (A5)(b) ⇒ (W) via (W-loc) ⇒ (W-ref) ⇒ (W-unif) ⇒ (W-δ) | EXISTS-CHECKED | `W3-RM2:W-suff@1.0.0`; the variance clause of (W-loc) follows from $L_n\to0$ under the floor on $Q\cup\{l\}$ (STATEMENT.md:164). $\theta^{*2}_{\min}n/(|Q|+\log n)\to\infty$ is (BM-Q) ⇒ (BM-W) (:138-139). |
| B7.4 | RM2-F conclusions ⇒ F-UNI premises | **NEW** (assembly) | as B6.6, fixed-design input validity. |

### Honest limits (the case the brief names)
(A3)–(A5) are **sample-level conditions on $(X,\theta^*)$**: partial signal gains $\delta^2_{U,j}$ and sample regressions.
They are interpretable but not reducible to eigenvalue floors and beta-min: visibility fails on well-conditioned designs
where truths cancel (masking), and the lattice condition (A5) is a condition on the *search route*, not on the
posterior. What exists instead: (i) the intuition paragraphs above, one per condition; (ii) Theorem 6, which shows the
same conditions hold with probability $\to1$ under population analogues; (iii) the examples table (polylog: every
example of the earlier version; polynomial: one truth with $n^b$ weak proxies — checked, conditional on the posterior
theorem; one equicorrelated group, $b<3/10$ — checked, conditional; polynomial decay $\alpha>2$ — unchecked).
**Not available:** the theorem without any lattice condition (open problem: control of the actual search path), and
any $b\ge\tfrac12$. Recommendation: present (A5)(a) in the main text (fully explicit) and (b) as the strengthening.

---

## 8. Theorem 8 — Certified screening

### Reader statement
**Theorem 8.** Let the design be fixed and assume (S1), (S3) and
- **(A1) Sparse eigenvalue floor.** $\lambda_{\min}(\hat R_S)\ge\kappa$ for every $S$ with $|S|\le q_n+s_0$;
- **(A2) Fixed signals.** $\theta^*_{\min}\ge b_0>0$ and $\|\theta^*\|_1\le M$ (fixed $\kappa,b_0,M,\sigma_*$);
- **(A3) Size budget.** $(q_n+1)\log p+\log n\le c_1n$, $c_1:=\kappa^2b_0^2/(200(M^2+\sigma_*^2))$, with
  $q_n\le K-1$.

Then
$$
P\big(\text{output},\ \hat S\text{ certified},\ |\hat S|\le q_n,\ S_0\not\subseteq\hat S\big)\to0 .
$$
In particular this holds for $p\le n^A$ and every $q_n=o(n/\log n)$. No condition on the start, leakage, blocks,
visibility, or on correlations among null columns is used; $p\le n^A$ is not needed.

### Why each assumption
(A1) only the realised combination of missing truths must keep a fraction of its energy outside any small model (the
master uses a weaker directional floor); the full floor is not needed (numerics with highly correlated nulls).
(A2) fixed signals; a version with beta-min at rate $\sigma\sqrt{((q_n+1)\log p+\log n)/n}$ exists (remark).
(A3) a union bound over models of size $\le q_n$.

### Master theorem
`W3-SCR:A1@1.0.0`, `Theory_work/Wave3/W3-SCR/STATEMENT.md:158-163`, status **"PROVED-CHECKED"**.

### Bridges
None: the statement is the master's, with the floor named in standard terms (the master already lists the sparse
eigenvalue floor as the sufficient case, :158-159). "Certified" must be explained in words (NOTATION §5).

### Honest limits
None. It is a one-sided guarantee (no false negatives among small certified models); exact recovery from the
certificate needs a near-orthogonality floor (`W3-SCR:SCR-C`, PROVED-CHECKED), which is not reader-friendly
($\varphi_n(q_n)\ge2A/(2A+1)+\epsilon$) — keep it as a remark.

---

## 9. Theorem 9 — Distribution-level consistency (placeholder)

Ticket W3-DIST is at its CP1 (read-only here; not touched). Candidate master: "Theorem DIST-1" in
`/home/fb31/BVS-wt/W3-DIST/Theory_work/Wave3/W3-DIST/STATEMENT.md:67-87` — joint Hellinger contraction of the
$(x,y)$ density at rate $\sqrt{\log n/n}$ in exponential form, with design interfaces (E), (C), (ND). **Status: candidate
statement at a scoping checkpoint; not proved; no registry row.** Its CP1 already proposes "Reader version = master
theorem + bridges B0, B1, B2" (:119). W3-READER will take that proposal over at W3-DIST's CP2/CP3; no reader version
is written here.

---

## Summary of bridges (feeds CHECKPOINT_1)

| Bridge | Theorem | Mark | Importance | Cost |
|---|---|---|---|---|
| B2.2 `W2-APP:POST` line check | 2, 4, 6 | EXISTS-UNCHECKED | **critical** (every random-design headline) | 1 Sol line check, HQ-queued |
| B4.3 POST2 C/E/A1/A0 council diff round | 4 | EXISTS-UNCHECKED | high (misspecification headline) | council diff round (HQ identified) |
| B6.6 / B7.4 RM2 ⇒ delivery assembly | 6, 7 | NEW | high (turns "if output, then $S_0$" into "$P(\hat S=S_0)\to1$") | ~1 page + Sol line check |
| B6.3 local regressions ⇒ variance clause (+ "$L_n\to0$") | 6 | NEW | medium | ½ page + Sol |
| B1.1–B1.3, B2.1, B4.1, B6.1 arithmetic of set sizes | 1, 2, 4, 6 | NEW (arithmetic) | medium (they make the statements explicit) | 1 page total + Sol |
| B3.2 Gaussian nulls ⇒ (W-sph) | 3 | NEW (one line) | low | trivial |
| B6.7 raw-scale coefficients in Theorems 5–6 | 5, 6 | NEW (optional) | low–medium | medium; not proposed |
