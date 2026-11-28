# FABLE_PHASE1 — HQ adviser report (Fable 5.2), 2026-11-28

Scope: the three Song–Liang (2015) counterparts only (density, selection, misspecification). Checkout `dept/theory @ 40febfb6`.
Notation as in `paper_03_theory.tex`: $\bar\beta_{\min}=\min_{j\in S_0}|\beta^*_j|\,\mathrm{sd}(x_j)/\sigma_*$, $r_n=\sqrt{\log n/n}$.

## Executive summary (10 lines)

1. **The headline selection theorem HQ asks for is already proved in the repository.** `W3-POST` Theorem 1 gives $1-\Pi(S_0)=O_P(r_n)$ under a beta-min at the threshold scale, $\bar\beta_{\min}\ge C\sqrt{\log n/n}/\varphi$, with fixed $s$; the paper's Thm 3.2 states a strictly weaker result than its own proof chain delivers.
2. **Decision (3): yes, and it is free.** The fixed floor $\varphi^2$ is needed only on sets of at most $(2A+2)s+2$ predictors; sets of size $O(\log n)$ need only A5 (the $c_\psi/n$ floor). This is exactly the $(F_\lambda)/(F_w)$ split of `W3-POST` Thm 1 and bridge B3 of `W3-DIST`.
3. **Decisions (1) and (2): yes.** Replace A7 in the main text by a beta-min assumption; make the shrinking-effect theorem the headline and fixed effects a corollary. Move A7 and Conj. 3.3 to the supplement as an unproved sharp-constant refinement.
4. **Honest cost: the constant.** What is proved today has $C=\sqrt{8c_0(s,A)}\approx 79$ (at $s=5$, $A=2$, in $\sqrt{\log n/n}$ units). I give a route to the explicit, $s$-free constant $(1+\eta)(1+\sqrt{2A+3})\sqrt2\approx5.2$; that is new work, low–medium risk, about 3 lead-days.
5. **Decision (4): prove Conj. 3.6(a) and demote Thm 3.5 to a corollary.** The general-law, fixed-dimension result under A8 is the true counterpart of SL Thm 4/Cor 2; its proof is elementary (SLLN, plus the LIL for exclusion), low risk, 2–3 lead-days. It has no written proof yet.
6. **The high-dimensional omitted-predictor result needs no new proof.** Under A9 the candidate data satisfy A1, so Conj. 3.6(b) is Thm 3.1 plus the selection theorem applied to the candidates. Gaussian predictors are not needed; state it as a corollary and say so.
7. **Density theorem (Thm 3.1): keep as is.** The proof (`W3-DIST`) is complete and cross-family line-checked; without A5 its fixed-design core fails at the stated radius (Prop. NEC). Optional: A6 can be weakened to a bounded signal-to-noise ratio with a half-page bridge.
8. **Audit:** I found no mathematical gap in the parts I read line by line (T03, T02(i), T03R, W3-POST Thm 1). The risks are organisational: the selection proof is spread over five files written as diffs, one under `Old_Projects`, and two proof folders plus the manuscript exist only on `main`.
9. **Lean:** `Lean/BVSCert` is a 10-line stub. Plan per theorem: a deterministic "on the good event" inequality with no axioms, then the probability of the event from about eight named, cited axioms (list in §B.5).
10. **Not targeted, with reasons:** a general response law in growing dimension, and the sharp constant 2 of A7. Both are high risk and neither is a Song–Liang counterpart.

What I read line by line: T03 `PROOF_v2.tex` (all), T01/T02 `PROOF_v3.tex` l.253–383, T03R `PROOF.md` l.1–60 and l.125–215, `W3-POST/STATEMENT.md` (all), `L1a_size_tail.md` l.1–40, the statements and bridges of `W3-DIST/STATEMENT.md` (§0–1, §1R to Theorem A, §3), `M_misr.md` l.1–75, `R_reduction.md` R.0–R.4. For the rest (bodies of `W3-DIST` Lemma X and bridges, `W3-POST2`, C-MIS L2–L6, `W3-MISR-R`) I rely on the recorded checks in `DEPS.tsv` and the file headers. I led W3-DIST in an earlier session, so Astra's independent reading of that proof is worth more than mine.

---

## A. Assumptions

### A.1 Verdict per assumption

| # | Verdict | Reason |
|---|---|---|
| A1 Gaussian linear model | **keep** | Needed for the exact $\chi^2$ laws and for the identity $E^*[m_b(S)/f_0]=1$ behind the size tail (T01/T02 `lem:num`). |
| A2 Sparsity, $s_0\le s$ fixed | **keep** | Owner position. Every constant is a maximum over $s_0\le s$. |
| A3 $2\le p\le n^A$ | **keep** | Used in all union bounds and in $j_0=\lceil(2A+1)s\rceil+1$. |
| A4 Sub-Gaussian sparse combinations | **keep** | Gives the multiplicative sample isometry (bridge B2-core) that makes a $c_\psi/n$ population floor usable. |
| A5 No near-exact collinearity | **keep** | Without it the fixed-design core of Thm 3.1 fails at the stated radius (Prop. NEC, `W3-DIST/lemmas/NEC.md`; a random-design counterexample is not written). In the selection theorem it replaces the fixed floor on $O(\log n)$ sets. |
| A6 Bounded effects | **keep, or change (optional)** | The proofs use only $\|\mu\|^2\le nM$ and $\|\theta^*\|^2\le nM'$ (`W3-DIST` interfaces (E), (C)). A bounded signal-to-noise ratio suffices; wording in A.3. |
| A7 Selection margin | **move to the supplement** | Not natural, and no proof exists (only the path in `ASSUMPTIONS_AND_PROOF_PATHS.md` §3.3). Replace in the main text by A7′ (A.3). |
| A8 Fixed candidate dimension | **keep, add one clause** | Add the score moments $E(x_j^2\varepsilon_{\mathcal C}^2)<\infty$ as a named part (b), used only for exclusion. |
| A9 Omitted predictors | **change the wording** | State it as "the candidate model is itself Gaussian linear"; the present form (with $x_O$, $\gamma$, $\tau$, $\varepsilon_O$) is equivalent under A1 by Cramér's theorem and goes into the remark. |
| A10 Sparse pseudo-true model | **keep** | Counterpart of A2 for the candidates; require $s_{\mathcal C}\ge1$ for selection. |

### A.2 Conditions written inside the theorems

| Where | Condition | Verdict | Reason |
|---|---|---|---|
| Thm 3.2 | $\bar\beta_{\min}\ge\underline b$ fixed | **drop from the headline; corollary** | Fixed effects imply A7′ for large $n$. |
| Thm 3.2 | floor $\varphi^2$ on sets of size $5(A+1)(s_0+1)\log n$ | **change** to sets of size $\le(2A+2)s+2$, and add A5 | The large sets need only the Occam factor, which A5 gives (T03R §7 remark 1, l.213). |
| Thm 3.2 | "assume A1–A4 and A6" (no A5) | **change** to A1–A6 | Follows from the previous line. |
| Thm 3.5 | Gaussian rows $x_{\mathcal C,i}$ | **drop** | Only the design events used Gaussianity; bridges B1–B3 of `W3-DIST` give them from A4–A5. |
| Thm 3.5 | Gaussian linear response given $x_{\mathcal C}$ | **keep, as A9′** | This is what makes the candidate problem an instance of A1. |
| Thm 3.5 | $\mathrm{Var}(x_{\mathcal C})$ nonsingular | **keep** | Uniqueness of $\beta^{\mathcal C}$. |
| Thm 3.5 (i) | floor on $3(A+1)(|S_0^{\mathcal C}|+1)\log n$ sets | **change** as in Thm 3.2 | Same proof. |
| Thm 3.5 (ii) | $\mathrm{Var}(x_{\mathcal C}^\top\beta^{\mathcal C})\le\bar\kappa\sigma_{\mathcal C}^2$ | **keep** | It is A6′ for the candidate problem. |
| Thm 3.5 (ii) | $n\min_j(\beta_j^{\mathcal C})^2\mathrm{Var}(x_j)/(\sigma_{\mathcal C}^2\log n)\to\infty$ | **change** to a fixed multiple | `W3-POST` Thm 1 allows BM($c$) with a fixed $c>c_0$ (l.74–75). |

### A.3 The four open decisions

**(1) Replace A7 in the main text by beta-min? Yes.** A7 is the only assumption a referee cannot check by eye, and Conj. 3.3 is the only place it is used. Proposed main-text assumption:

> **Assumption 7′ (Identifiable effects).** $s_0\ge1$, and there are fixed $\varphi\in(0,1]$ and $C_\beta$ such that
> (a) $\lambda_{\min}\{\mathrm{Corr}(x_T)\}\ge\varphi^2$ for every set $T$ of at most $(2A+2)s+2$ predictors;
> (b) $\displaystyle\min_{j\in S_0}\frac{|\beta^*_j|\,\mathrm{sd}(x_j)}{\sigma_*}\ \ge\ \frac{C_\beta}{\varphi}\Big\{\frac{\log(p\sqrt n)}{n}\Big\}^{1/2}.$

Intuition sentence for the paper: "(a) says that no true predictor is nearly a combination of a few others; it concerns sets of fixed size only. (b) asks each true effect to exceed a multiple of $\{\log(p\sqrt n)/n\}^{1/2}$, the price $\log p+\tfrac12\log n$ that the prior and the marginal likelihood charge one predictor." Condition (a) is the fixed-size analogue of SL Condition 3 and of SL's (26). SL's proofs of Thm 3 and Thm S treat $\beta_t^{*2}/\sigma^{*2}$ as fixed and positive, which is the fixed-effects case of (b).

**(2) Headline selection theorem with $\bar\beta_{\min}\ge C\sqrt{\log(p\sqrt n)/n}$ and fixed $s$? Yes.**

> **Theorem 3.2 (Selection of the true model).** Assume A1–A6.
> (a) *Inclusion of strong predictors.* Suppose A7′(a) holds, and let $J_n$ be the set of $j\in S_0$ that satisfy the inequality in A7′(b). There is a constant $C_0(s,A)$ such that, if $C_\beta>C_0(s,A)$, then $\max_{j\in J_n}(1-\mathrm{PIP}_j)=O_P(r_n)$, whatever the other effects are.
> (b) *Exact selection.* Under A7′ with $C_\beta>C_0(s,A)$,
> $$1-\Pi(S_0\mid D_n)=O_P(r_n),\qquad \max_{1\le j\le p}\big|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}\big|\le1-\Pi(S_0\mid D_n),\qquad P^*(\mathrm{HPM}=\mathrm{MPM}=S_0)\to1 .$$
>
> **Corollary 3.3 (Fixed effects).** Assume A1–A6 and A7′(a). If $\bar\beta_{\min}\ge\underline b$ for a fixed $\underline b>0$, the conclusions of Theorem 3.2(b) hold.

Part (a) is the counterpart of SL Thm 3 (stated there per identifiable predictor); part (b) is the counterpart of Thm S and Cor S1, with a rate and with the whole posterior mass, not pairwise odds. Both parts are items 1–3, 5(b) and 6 of `W3-POST` Thm 1. An expectation form, $E^*\{1-\Pi(S_0)\}=O(r_n)$, is also available (`W3-POST2` Claim C case (i), `STATEMENT.md` l.85–94).

*The constant, honestly.* The proved value is $c_0(s,A)=\max\{4C_*,\,32[s(A+1)+2]\}$ with $C_*=2s+3[Aj_0+s+\log(j_0+1)+1]$, in the sample form $\theta^{*2}_{\min}\ge c\,\sigma_*^2\log n/(n\varphi_0^2)$. Passing to population quantities costs a factor 8 ($\varphi_0^2=\varphi^2/4$, $\hat s_j^2\ge\mathrm{Var}(x_j)/2$), so

| $(s,A)$ | $c_0$ | $\bar\beta_{\min}\varphi/\sqrt{\log n/n}\ \ge$ | sharpened target, in $\sqrt{\log(2p\sqrt{n+1})/n}$ units |
|---|---|---|---|
| $(1,1)$ | 128 | 32 | 4.6 |
| $(5,2)$ | 776 | 79 | 5.2 |
| $(10,1.5)$ | 995 | 89 | 4.9 |

In $\sqrt{\log(p\sqrt n)/n}$ units the proved constant is $C_0=4\sqrt{c_0}$ in the worst case (bounded $p$) and $\sqrt{8c_0/(A+\tfrac12)}$ at $p=n^A$. For scale: on the S1 design ($n=500$, $p=5000$, $s_0=10$, $\varphi^2=0.25$), exact recovery appears between ratio 2 and 4 in $\sigma_*\sqrt{\log p/n}$ units. The proved threshold is about 145 in those units (35–70 times the observed transition) and the sharpened one about 11.5 (3–6 times). I recommend printing the theorem with "a constant $C_0(s,A)$", giving its value in the supplement, and saying in one sentence that it is not sharp. This is Song–Liang's own practice (no constants).

*Sharpened constant (new work).* With $\bar u_d=\lceil(2A+1)d\rceil+1$ and any fixed $\eta>0$, the route in §B.2 gives the theorem under

$$\bar\beta_{\min}\ \ge\ \frac{(1+\eta)\big(1+\sqrt{2A+3}\big)}{\varphi}\Big\{\frac{2\log\big(2p\sqrt{n+1}\big)}{n}\Big\}^{1/2},$$

with rate $O_P(r_n+n^{-\gamma})$, $\gamma=\gamma(\eta)>0$. It improves the Remark's factor $1+\sqrt{\bar u_{s_0}}$ to $1+\sqrt{2A+3}$, because a rival missing $d$ true predictors has residual signal at least $n\varphi^2d\,\bar\beta_{\min}^2\sigma_*^2$, and $\bar u_d/d\le2A+3$.

**(3) Floor on sets of size $O(s)$ instead of $O(s\log n)$? Yes: at most $(2A+2)s+2$ predictors.** The fixed floor enters the proof in two places only (T03R §7 remark 1): the signal bound $\|(I-P_S)\mu\|^2\ge(n-1)\varphi_0^2\|\theta^*_{S_0\setminus S}\|^2$ on $S\cup S_0$ for rivals with at most $j_0$ nulls (T03 `lem:signal`, l.146–152), and the ridge correction on those same sets. Rivals with more than $j_0=\lceil(2A+1)s\rceil+1$ nulls need no signal: their prior-plus-Occam odds sum to $O_P((\log n)^{(j_0+1)/2}/n)$ (T03 `lem:assemble`, l.314–330; T03R (C8)). Sets of size up to $m^\sharp_n=O(\log n)$ need only $\lambda_{\min}(X_T^\top X_T)\ge g_0$, which is A5 after the transfer of bridge B2 ($g_0=c_\psi/8$). So A5 is not an extra price: it is already assumed for Thm 3.1.

**(4) Misspecification:** see §D. Recommendation: prove the general-law version under A8 as a theorem; restate the high-dimensional version under A9′ and A10 as a corollary; drop the Gaussian-predictor theorem as a separate result.

### A.4 Replacement wording for the other changes

**A6′ (optional; weaker and more standard than A6).**

> **Assumption 6′ (Bounded signal-to-noise ratio).** $\mathrm{Var}(x^\top\beta^*)\le\bar\kappa\,\sigma_*^2$ for a fixed $\bar\kappa>0$.

"The population $R^2$ stays below $\bar\kappa/(1+\bar\kappa)<1$; this excludes the noiseless limit. A6 with A2 implies it with $\bar\kappa=s^2\bar b^2$." Why it suffices: (E) follows by Bernstein's inequality on the fixed-size set $S_0$ (A4), and on the event of bridge B2, $\|\theta^*\|^2\le\|\mu\|^2/\lambda_{\min}(G_{S_0})\le 8nM/c_\psi$, which is interface (C; $M'$) of `W3-DIST`. The constants of Thm 3.1 then depend on $(s,A,L,c_\psi,\bar\kappa)$. Caveat: `ASSUMPTIONS_AND_PROOF_PATHS.md` (A-BS′, l.118–129) records this as "not adopted until the size lemma is re-proved". My reading of the `W3-DIST` statement is that Lemma X is already stated under (E) and (C) with arbitrary fixed $M'$ (l.55–59, 354–365), so only bridge B1 changes. This needs one line check before adoption. If HQ prefers no risk, keep A6.

**A8 (add part (b)).**

> **Assumption 8 (Fixed candidate set).** The pairs $(x_{\mathcal C,i},y_i)$ are independent copies of $(x_{\mathcal C},y)$, whose law does not depend on $n$; $|\mathcal C|\ge2$ is fixed; (a) $E y^2<\infty$, $E\|x_{\mathcal C}\|^2<\infty$, $\mathrm{Var}(x_{\mathcal C})$ is nonsingular and $\sigma^2_{\mathcal C}>0$; (b) $E(x_j^2\varepsilon_{\mathcal C}^2)<\infty$ for every $j\in\mathcal C$.

**A9′ (simpler statement of A9).**

> **Assumption 9′ (Gaussian linear candidate model).** $\mathrm{Var}(x_{\mathcal C})$ is nonsingular, and the residual $\varepsilon_{\mathcal C}=y-\alpha_{\mathcal C}-x_{\mathcal C}^\top\beta^{\mathcal C}$ is $N(0,\sigma^2_{\mathcal C})$ and independent of $x_{\mathcal C}$. Assumptions A3–A6 hold with $(x_{\mathcal C},\beta^{\mathcal C},\sigma^2_{\mathcal C})$ in place of $(x,\beta^*,\sigma_*^2)$.

Remark for the paper: "Under A1 this holds when $(x_{\mathcal C},x_O)$ is jointly Gaussian; by Cramér's theorem it is equivalent to $x_O^\top\beta^*_O=\alpha_O+x_{\mathcal C}^\top\gamma+\varepsilon_O$ with $\varepsilon_O$ Gaussian and independent of $x_{\mathcal C}$."

**A7 and Conj. 3.3 → supplement,** under a heading such as "A sharper signal condition (conjecture)". Keep the heuristic and the constant 2; delete $Q_n$, $h$, leakage and $\bar u_d$ from the main text. The Remark's comparison with Narisetty–He, Luo–Chen and the lower bounds of Wainwright and Fletcher et al. moves next to A7′.

One further low-cost item to verify: the case $s_0=0$. T03 covers it ((v), l.380: the beta-min conditions hold vacuously), which would give $1-\Pi(\emptyset)=O_P(r_n)$ when $\beta^*=0$; `W3-POST` restricts to $s_0\ge1$. A referee will ask about the null model; it is worth one line check to include it.

---

## B. Proof plans

### B.0 Final list of targets

| Target | SL counterpart | Status today |
|---|---|---|
| **D** Thm 3.1, density | Thms 1–2, Cor 1 | proved, checked; needs transcription |
| **S** Thm 3.2 (a), (b) + Cor 3.3 | Thm 3, Thm S, Cor S1 | proved in interface form; needs assembly and one self-contained write-up |
| **M1** Thm 3.4, any response law, fixed candidate set | Thm 4, Cor 2 | proof path only; **to be proved** |
| **M2** Cor 3.5, omitted predictors in high dimension | (beyond SL) | corollary of D and S; a previously delivered analogue exists |

### B.1 Target D — density consistency (Thm 3.1, statement unchanged)

Route (existing; `Theory_work/Wave3/W3-DIST`):

1. **Scale.** Reduce to $\sigma_*=1$, $\alpha^*=0$ by the exact scale covariance of the coded posterior (bridge B0; `W3-MISR/lemmas/R_reduction.md` R.1–R.2).
2. **Design event.** From A4–A6: sample standard deviations within a factor 2, no dropped column, $\|\mu\|^2\le nM$, $\|\theta^*\|^2\le nM'$ (B1); multiplicative lower isometry with an intercept on $q_n$-sparse vectors (B2-core, net plus Bernstein); hence $\lambda_{\min}(X_T^\top X_T)\ge c_\psi/8$ on the window and the Occam condition (ND) (B2). Failure probability $\le5p\,e^{-cn/L^4}\le n^{-cM}$.
3. **Fixed-design core (Lemma X).** Conditionally on the design: (X1) a noise event; (X2) for models of size $\le d_t$ with small ridge loss, the conditional normal–inverse-gamma posterior puts mass $\le e^{-ct}$ outside $\{\|\hat\mu-\mu\|^2\le C\sigma_*^2t,\ |v/\sigma_*^2-1|\le C\sqrt{t/n}\}$; (X3) small models with large ridge loss have mass $\le e^{-ct}\pi(S_0)$; (X4) models larger than $d_t=s_0+\lceil C't/\log n\rceil$: a moment of order $\lambda=(4A+1)/(4A+2)$ of the Bayes factors of the supersets of $S_0$ under (ND) for sizes up to $m_n(t)$, and the BB$(1,p)$ tail $2^{-m}$ above.
4. **Lemma H.** $d_H^2(f,f^*)\le(v/\sigma_*^2-1)^2+E_x\min\{1,\Delta(x)^2/(4\sigma_*^2)\}$.
5. **Lemma T.** Distribution-free transfer from the in-sample truncated loss to its population value, uniformly over $d$-sparse directions (a one-sided VC bound for unions of two half-spaces on $d$ coordinates).
6. **Assemble** DIST-1, then Theorem A with $t=M\log n$.

- Key lemmas: X, T, H, B0–B2 (`STATEMENT.md` §3; proofs in `lemmas/X.md`, `work/B_transfer/`, `work/E_bridges/`).
- Reuse: everything. `DEPS.tsv` records each item as OK after cross-family line checks.
- New pieces: none mathematically. A single self-contained supplement proof; the half-page bridge if A6′ is adopted.
- Main risk: transcription. The source has about ten files and a reader version that differs in notation ($K$ for the sub-Gaussian constant, $r$ for retained columns). Low mathematical risk.
- Effort: 4–6 lead-days to write, plus two review rounds.
- Worth adding to the paper as one sentence: without A5 the same statement holds at radius $\sqrt{M\log n\,\log(p\vee n)/n}$ (DIST-2, proved). It answers "why A5?" before the referee asks.

### B.2 Target S — selection (Thm 3.2 and Cor 3.3)

Route:

1. **Reduction.** Contrast coordinates: $y_c=\mu_c+e$, $e\sim N_{n-1}(0,\sigma_*^2I)$; exact score formula; $\pi(S)\le\ell(S)/\ell(S_0)$ (T03 `lem:red`, l.64–83).
2. **Deterministic facts.** Ridge smoother, determinant ratio $1\le D_T/D_S\le(n+1)^{|T|-|S|}$ and its lower bound under a floor $g$, prior ratios with the multiplicity cancellation $\binom{p-s_0}{j}w(s_0+j)/w(s_0)\le2(j+1)^{s_0}2^{-j}$ (T03 l.94–144).
3. **Design event $\mathcal A_n$.** From A4–A6 and A7′: (E); $(F_\lambda)$ with $\varphi_0^2=\varphi^2/4$ on $S_0\cup J$, $|J|\le j_0$; $(F_w)$ with $g_0=c_\psi/8$ on $S_0\cup J$, $|J|\le m^\sharp_n$; BM($c$) with $c=C_\beta^2/16>c_0$ (bridges B1, B2-core, B2, B3).
4. **Size tail.** $\Pi(|S|>m^\sharp_n)=O_P(n^{-1/2})$ from $E^*[m_b(S)/f_0]=1$ at a data-free rate, the mixed-endpoint transfer, and a lower bound on $m(S_0)/f_0$ (T01/T02 `thm:Ta`, `lem:num`, `lem:den`, `thm:T02i`, l.255–379; design-free form `W3-POST/lemmas/L1a_size_tail.md`).
5. **Supersets.** $\sum_j\Xi_j\le e^{\rho_n}\Upsilon_n$ with $E\Upsilon_n\le Cq_n$, $q_n\le c_q r_n$, from the truncated moment $E[e^{\chi_j^2/2}\mathbf 1\{\chi^2_j\le\tau_j\}]\le(e\tau_j/j)^{j/2}$ and step 2 (T03 `prop:sup`, l.256–278; T03R (C4)–(C5)).
6. **Underfitting rivals with at most $j_0$ nulls.** Compare $S$ with $S'=S\cup S_0$: $\ell(S)/\ell(S')\le(2p)^{d}(n+1)^{d/2}\exp\{-\nu\tfrac n{n+1}V_S/(E_n+V_S)+\rho_n\}$; signal $V_S\ge\tfrac14\Delta_S$; beta-min gives $\le n^{-2}$ (T03 `lem:SvsSp`, `lem:signalgain`, l.284–312).
7. **Underfitting rivals with more than $j_0$ nulls.** Crude bound $(2p)^{s_0}(n+1)^{s_0/2}$ times $\Upsilon_n^{>j_0}$; no signal needed (T03R (C6)(a), (C8)).
8. **Assemble and summarise.** $\delta_n=O_P(r_n)$; PIP, MPM and HPM by the deterministic summaries; part (a) by restricting step 6 to rivals that miss $j\in J_n$ (T03 (iv), l.366–378).
9. **Random design.** Apply the fixed-design statement on $\mathcal A_n$ and add $P(\mathcal A_n^c)\to0$ (`W3-POST` Thm 1 item 6; `W2-APP/lemmas/L1_POST.md` step (5)).

- Reuse: steps 1–2, 5–8 from `Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex` with the modifications of T03R §4–6; step 4 from `T01_T02_contrast_dimension/PROOF_v3.tex`; steps 3 and 9 from `W3-DIST` bridges and `W3-POST`.
- New pieces: (i) bridge B3 with BM($c$) in place of BM-$\infty$ (three lines: $\theta^{*2}_j=\hat s_j^2\beta_j^{*2}\ge\tfrac12\mathrm{Var}(x_j)\beta_j^{*2}$); (ii) one consolidated proof, written forward, not as a diff; (iii) the corollary (immediate).
- Main risk: none mathematical for the baseline. The practical risk is that the proof is a chain T01/T02 → T03 → T03R (diff) → W3-POST (statement) → bridges, and T03R lives in `Theory_work/Old_Projects/.../W1-T03R/`. A consolidated write-up removes it.
- Effort: 3–4 lead-days to write, plus two review rounds.

*Optional upgrade: the explicit constant.* Replace step 6 by a direction bound. For a rival $S$ with $d$ missing true predictors and $u\le\bar u_d$ nulls, let $v_S=(I-P_S)\mu_c/\sqrt{\Delta_S}$. Then $v_S$ lies in $\mathrm{col}(S')\ominus\mathrm{col}(S)$, so

$$\sqrt{V_S}\ \ge\ \langle v_S,y_c\rangle=\sqrt{\Delta_S}+\langle v_S,e\rangle,\qquad \langle v_S,e\rangle\sim N(0,\sigma_*^2).$$

A union bound over the at most $2^{s_0}\binom{p-s_0}{u}$ rivals with $u$ nulls gives $\langle v_S,e\rangle\ge-\sigma_*\{2\log\binom{p-s_0}{u}+2s_0\log2+2t_n\}^{1/2}$ simultaneously, with $t_n=\log\log n$. Since $x\mapsto x/(1+x)$ increases, the exponent may be evaluated at $V_S=2(1+\eta')\sigma_*^2[d\log(2p\sqrt{n+1})+\gamma\log n]=O(\log n)$, where $\nu\tfrac n{n+1}V/(E_n+V)=(1-o(1))V/(2\sigma_*^2)$. With $\Delta_S\ge(n-1)\varphi_0^2d\,\theta^{*2}_{\min}$ the requirement becomes, after dividing by $\sqrt d$,

$$\sqrt{n}\,\varphi\,\bar\beta_{\min}\ \ge\ (1+\eta)\Big(1+\sqrt{\bar u_d/d}\Big)\sqrt{2\log(2p\sqrt{n+1})},\qquad \bar u_d/d\le2A+3 .$$

The split in step 7 is then made at $\bar u_d$ for each $d$: $(2p)^d(n+1)^{d/2}E\Upsilon_n^{>\bar u_d}\le C(\log n)^{(\bar u_d+1)/2}/n$. This is the "structure-free" case $\bar a\equiv1$ of the council's Lemma W, and nothing else from A7 is needed.
Risk: low–medium (the uniform width must be combined with the superset sum without double counting; the accounting above pays the nulls once in the width and once in $\Upsilon_n$, which is conservative and safe). Effort: about 3 lead-days plus review. Fallback: the baseline constant.

### B.3 Target M1 — any response law, fixed candidate set (new)

> **Theorem 3.4 (Misspecified model, fixed candidate set).** Assume A8(a). Then, almost surely,
> (i) $\Pi\{d_H(f,f_0)>\epsilon\mid D_n^{\mathcal C}\}\to0$ for every $\epsilon>0$;
> (ii) $\Pi(S\supseteq S_0^{\mathcal C}\mid D_n^{\mathcal C})\to1$.
> (iii) If A8(b) also holds, $\Pi(S_0^{\mathcal C}\mid D_n^{\mathcal C})\to1$ almost surely, and $P(\mathrm{HPM}=\mathrm{MPM}=S_0^{\mathcal C}\ \text{eventually})=1$.

(i) is SL Thm 4, (ii) is SL Cor 2 (almost surely, where SL have "in probability"), (iii) goes beyond SL. The case $S_0^{\mathcal C}=\emptyset$ is covered.

Route (finitely many models; $K=|\mathcal C|$ once $n\ge2|\mathcal C|$):

1. **Sample moments.** By the SLLN the sample means, variances and covariances of $(x_{\mathcal C},y)$ converge almost surely. Hence, on the standardised scale, $\mathrm{SS}_S/(n-1)\to1-\rho_S^2$ for every $S$, where $\rho_S^2$ is the population $R^2$ of the best linear predictor from $x_S$; the ridge terms change $\mathrm{SS}_S$ by $O(1)$ because $G_S/n\to\mathrm{Corr}(x_S)\succ0$; and $1\le D_S\le(n+1)^{|S|}$.
2. **Risk gap.** If $S\not\supseteq S_0^{\mathcal C}$ then $\rho_S^2<\rho_{\mathcal C}^2$, by uniqueness of $\beta^{\mathcal C}$. So
$$\log\frac{\pi(S)m(S)}{\pi(\mathcal C)m(\mathcal C)}\le C+\frac{|\mathcal C|}2\log(n+1)-\frac n2\log\frac{1-\rho_S^2}{1-\rho^2_{\mathcal C}}\,(1+o(1))\to-\infty\quad\text{a.s.}$$
This proves (ii).
3. **Density.** For each $S\supseteq S_0^{\mathcal C}$ the conditional posterior is normal–inverse-gamma with mean converging to the pseudo-true parameters (the best linear predictor from $x_S$ is the one from $x_{\mathcal C}$) and covariance $O(1/n)$; the map back to the original units and the plug-in intercept are continuous. Lemma H with $E\|x_{\mathcal C}\|^2<\infty$ gives $d_H(f,f_0)\to0$ in conditional posterior probability. With (ii) this proves (i). No score moment is used.
4. **Exclusion.** For $S\supsetneq S_0^{\mathcal C}$ the extra fitted sum of squares is $u^\top\tilde X(\tilde X^\top\tilde X)^{-1}\tilde X^\top u$, with $u_i=\varepsilon_{\mathcal C,i}$ and $\tilde X$ the columns of $S\setminus S_0^{\mathcal C}$ residualised on $S_0^{\mathcal C}$ and the intercept. $E(Zu)=0$ and A8(b) give $\|\sum_iZ_iu_i\|=O(\sqrt{n\log\log n})$ a.s. (Hartman–Wintner), and $(\tilde X^\top\tilde X/n)^{-1}=O(1)$ a.s. So the gain is $O(\log\log n)$, against an Occam cost $\tfrac12|S\setminus S_0^{\mathcal C}|\log n$. This proves (iii).

- Reuse: Lemma H (`W3-DIST`); the score formula; the path in `THEOREM_DEFINITIONS.md` l.215–219 and `ASSUMPTIONS_AND_PROOF_PATHS.md` §3.4.
- New pieces: the whole proof, about 3–5 pages. No existing file proves it.
- Main risk: low. Two places need care: the map from the standardised draw to original units when sample moments are random, and the statement of step 4 for the intercept direction ($Z=(1,x_{\mathcal C}^\top)^\top$, so $E u^2<\infty$ is also used; it holds).
- A8(b) is close to necessary for (iii): with scores in the domain of attraction of an $\alpha$-stable law, $\alpha<2$, the gain is of order $n^{2/\alpha-1}\gg\log n$. This is a heuristic remark, not a proved converse.
- Effort: 2–3 lead-days plus review.

### B.4 Target M2 — omitted predictors in high dimension (corollary)

> **Corollary 3.5 (Omitted predictors, many candidates).** Assume A9′ and A10. Then the conclusion of Theorem 3.1 holds for $\Pi(\cdot\mid D_n^{\mathcal C})$ with $f_0$ in place of $f^*$. If also $S_0^{\mathcal C}\ne\emptyset$ and A7′ holds for the candidate problem, the conclusions of Theorem 3.2 hold with $S_0^{\mathcal C}$ in place of $S_0$.

Route: under A9′ the pairs $(x_{\mathcal C,i},y_i)$ satisfy A1 with parameters $(\alpha_{\mathcal C},\beta^{\mathcal C},\sigma^2_{\mathcal C})$, the posterior is by definition the one computed from $(y,X_{\mathcal C})$ with $p$ replaced by $|\mathcal C|$, and $f_0$ is the true joint density of $(x_{\mathcal C},y)$. Apply D and S. One line.

- Reuse: D and S. The earlier route (`W3-MISR` Lemma R′ and Theorem MIS-R (ii), `STATEMENT.md` §4 l.142–160; C-MIS L1–L2) reaches the same statement through the scale reduction and gives the expectation form $E^*\{1-\Pi(S_0^{\mathcal C})\}=O(r_n)$.
- New pieces: none.
- Risk: none beyond D and S. The requirement that $\mathcal C$ is fixed before the data are seen must stay in the text.
- Effort: half a day.

### B.5 Lean plan

`Lean/BVSCert` contains only `Basic.lean` (10 lines; toolchain `v4.35.0-rc2`). A sorry-free snapshot with the posterior summaries exists in `Theory_work/Old_Projects/.../L-LEAN/` (`hpm_eq_truth`, `markov_half`, `T07Bayes`). All Mathlib claims below are from memory and must be verified.

**Architecture (the same for every theorem).** Two layers.
- *Layer 1, no axioms.* A theorem of the form: for every real design matrix, response and constants such that the listed inequalities hold (the good event, written as explicit inequalities on $e=y_c-\mu_c$ and on the design), the posterior over models, defined by the closed-form score of eq. (marglik), satisfies the conclusion. This is finite-dimensional real linear algebra and finite sums.
- *Layer 2, named axioms.* The probability of the good event under A1–A7′, from the axioms below. The certificate then reads "Theorem X holds given axioms AX1–AXk", and `#print axioms` lists exactly those.

| Axiom | Statement | Source | Used by |
|---|---|---|---|
| AX1 `gaussian_proj_chisq` | for $e\sim N(0,\sigma^2I_N)$ and an orthogonal projection $P$ of rank $d$, $\|Pe\|^2/\sigma^2\sim\chi^2_d$ | Cochran (1934) | S, D |
| AX2 `chisq_tail` | $P(\chi^2_d\ge d+2\sqrt{dx}+2x)\le e^{-x}$, $P(\chi^2_d\le d-2\sqrt{dx})\le e^{-x}$ | Laurent & Massart (2000), Lemma 1 | S, D |
| AX3 `chisq_density` | density of $\chi^2_d$ (then the truncated moment of T03 `lem:chi`(b) is a Gamma integral, provable) | standard | S |
| AX4 `gauss_integral_mv` | $\int_{\mathbb R^k}e^{-x^\top Ax/2}dx=(2\pi)^{k/2}\det(A)^{-1/2}$ for $A\succ0$ | standard (e.g. Anderson 2003) | S (the identity $\int m_b(S)=1$), D |
| AX5 `bernstein_subexp` | Bernstein's inequality for sums of independent sub-exponential variables | Vershynin (2018), Thm 2.8.1 | bridges B1, B2-core |
| AX6 `vc_relative_deviation` | $P(\exists A\in\mathcal A:\ P(A)-P_n(A)>\epsilon\sqrt{P(A)})\le4S_{\mathcal A}(2n)e^{-n\epsilon^2/4}$ | Anthony & Shawe-Taylor (1993), Thm 2.1 | D (Lemma T) |
| AX7 `gamma_tail` | Chernoff bounds for a Gamma variable (posterior of $1/v$) | standard; possibly provable from Mathlib's mgf | D |
| AX8 `lil` | Hartman–Wintner law of the iterated logarithm | Hartman & Wintner (1941) | M1 (iii) only |

Expected to be available in Mathlib, so not axioms: Markov's inequality, the strong law (`ProbabilityTheory.strong_law_ae`), the Gaussian mgf and Chernoff bound, Sauer–Shelah, the Schur-complement determinant formula. To verify: Cauchy interlacing (probably absent; it can be avoided, since $D_{S\cup\{j\}}/D_S=(1+(n+1)a_H)/(1+a_A)$ with $0\le a_H\le a_A$ gives $D_T/D_S\le(n+1)^{|T|-|S|}$ by Schur complements alone), and the VC dimension of half-spaces (via Radon's theorem, which Mathlib has).

Per target:

| Target | Layer 1 (fully formal) | Layer 2 axioms | Effort (lead-days) |
|---|---|---|---|
| S | score formula and $\pi(S)\le\ell(S)/\ell(S_0)$; ridge-smoother and determinant inequalities; prior ratios; the bounds of T03 `lem:onesup`, `lem:SvsSp`, `lem:signalgain`, `lem:assemble` as inequalities on a fixed data set; summaries (PIP, MPM, HPM) | AX1–AX5 | 8–12 for layer 1; 4–6 for layer 2; 1 for the summaries (port from L-LEAN) |
| D | Lemma H as a real inequality given the closed-form Gaussian affinity; the model-mass part of Lemma X (X3, X4) on a fixed data set; the assembly | AX1–AX7; the conditional normal–inverse-gamma tails of X2 enter through AX2 and AX7 | 6–10 and 5–8 |
| M1 | the finite-model argument: if every score gap tends to $-\infty$ the posterior mass tends to 0; continuity of the unit map | Mathlib SLLN; AX8 for (iii) | 5–8 |
| M2 | instantiation of D and S | none new | 1 |

Two honest limits. (a) For D, the posterior of $(\theta,v)$ given $S$ is a measure, so "deterministic core" there means the model-level bounds and Lemma H; the parameter-level concentration is layer 2. (b) Bridge B2-core (net plus Bernstein) is in-house; under the owner's rule it must be proved in Lean from AX5, not assumed. If that is too costly in the first pass, certify the *interface form* first (item 6 of `W3-POST` Thm 1: the theorem on any design event $\mathcal A_n$ on which the sample conditions hold), which needs AX1–AX4 only, and add the bridge later. Every formal statement needs the fidelity check of `Lean/BRIEF.md`.

### B.6 Suggested order

1. Owner settles A7′, the statements of Thms 3.2 and 3.4, and whether to adopt A6′.
2. S: consolidated proof (baseline constant). In parallel M1: new proof.
3. D: transcription. M2: one paragraph.
4. Review at the 8.5 bar; then the optional sharpened constant for S.
5. Lean: summaries, then S layer 1, then S layer 2 in interface form, then M1, then D.

---

## C. Audit of existing proofs

Legend: **A** = reusable as is; **R** = reusable after repair or rewriting; **O** = obsolete for these targets.

| Proof | Where | Correct? | Matches the current statements? | Use |
|---|---|---|---|---|
| T01/T02: contrast identity, envelope, transfer, size tail, strict supersets | `Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`; read l.253–383 | Yes for the part read. `lem:num` (l.317–322) uses a data-free rate, and `thm:Ta` (l.255–265) handles the data-dependent rate $b_0s_y^2$ correctly; the remark at l.381–383 states exactly what is and is not claimed. | Fixed design; hypotheses R (floor on $S_0$, $\|\mu\|^2\le nM$). Consistent with A1–A6 through the bridges. | **A** (base of S, step 4) |
| T03: selection, PIPs, HPM | `Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex`; read in full | Yes. No gap found. Lossy constants at l.194 (G4), l.311 ($V_S\ge\Delta_S/4$) and l.287–300 ($\min(V/8\sigma^2,n/5)$) explain the size of $c_0$. | Stronger assumption than needed (SE: fixed floor on sets of size $m_n+s_0=O(\log n)$, l.171) and conditional on H-T02. Superseded in hypotheses by T03R. Already a threshold-scale beta-min theorem (BM-C, l.342–349). | **R** (rewrite with the T03R changes merged) |
| T03R: exact BB tail, T02(i♯), T02(ii♯), T03♯ | `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md`; read l.1–60, 125–215 | Yes for the part read. Lemma B (l.137–142) and (C1)–(C10) (l.161–209) are correct modifications of T03. | This is the proof of the proposed Thm 3.2 in fixed-design form: $\mathrm{SE}_\lambda(j_0)$, $\mathrm{SE}_w(m^\sharp_n;g_0)$, BM($c$) with fixed $c>c_0$ (l.129–134, 163–167). | **R**: written as a diff against two other files, and stored under `Old_Projects`. Must be promoted and consolidated. |
| W3-POST Theorem 1 and Lemma 1a′ | `Theory_work/Wave3/W3-POST/STATEMENT.md` l.41–127; `lemmas/L1a_size_tail.md` | Statement consistent with T03R; Lemma 1a′ proof correct for the part read (l.1–40). Council-passed (C3). | Yes: items 1–3, 5(b), 6 are the proposed Thm 3.2(a), (b) in interface form. Restricts to $s_0\ge1$. | **A** |
| W3-DIST: DIST-1, Lemmas X, T, H, S, V; bridges B0–B3; Theorem A; Prop. NEC | `Theory_work/Wave3/W3-DIST/STATEMENT.md` §1 l.74–98, §1R, §3 l.320–417; `lemmas/`, `work/` | Not re-derived by me in this pass. `DEPS.tsv`: every item on the path is OK after cross-family line checks; `ERRATA.md` E1–E8 are editorial. | Thm 3.1 of the paper = Theorem A(i). Notation differs ($K$ vs $L$; $r$ vs $p$). B3 already contains the floor split with BM-$\infty$ (l.409–414). | **A** for D; **R** for S (B3 needs the BM($c$) variant) |
| W2-APP L1_POST: Gaussian rows | `Theory_work/Wave2/W2-APP/lemmas/L1_POST.md` | Not read; used here only for the diagonal transfer of step (5), restated as item 6 of W3-POST. | Gaussian rows only; needs $\psi_n\sqrt n/(\log n)^{3/2}\to\infty$ (W3-POST Cor 1R, l.106–118), which is stronger than A5. | **O** except step (5) |
| W3-D3: sub-Gaussian rows, Theorem 2SG (the delivered `thm:post-random`) | **only on `main`**: `Theory_work/Wave3/W3-D3/lemmas/ASSEMBLY.md`, `B3w.md` | Skimmed the assembly: it applies W3-POST item 6 with a BM-$\infty$ envelope. Header: "PROVED (by this seat, unchecked)". | It is the proof of the paper's present Thm 3.2 (floor on $5(A+1)(s_0+1)\log n$ sets, fixed effects). Not needed for the proposed form. | **O** for the new statement |
| W3-POST2: Claim C (expectation rate), A (Occam), E | `Theory_work/Wave3/W3-POST2/STATEMENT.md` l.85–94; `lemmas/` | Not read. Header statuses "PROVED (by this seat, unchecked)", with later Sol line checks. | Gives $E\delta_n\le Cr_n$ under the Thm 1 conditions (case (i)). | **A** if the expectation form is wanted |
| C-MIS: Lemma R, Theorem MIS, Prop. P, Lemma GD | `Theory_work/Wave1C/C-MIS/lemmas/00_MAIN.md`, L1–L6 | Map read; bodies not read. | Gaussian rows; first version of the omitted-predictor result. | **O** (superseded by W3-MISR and by Cor 3.5) |
| W3-MISR: Lemma R′, Theorem MIS-R (i), (i′), (ii), Cor G | `Theory_work/Wave3/W3-MISR/lemmas/R_reduction.md` (R.0–R.4 read), `M_misr.md` (l.1–75 read), `STATEMENT.md` §4–5 | R′(a), (b) correct as read: the posterior depends on the response only through the direction of the contrast vector. MIS-R (i) is a correct reduction to W3-POST2 Claim C. | The paper's Thm 3.5 is Cor G(b) (Gaussian rows; covariance-scale floor and $\max_j\Sigma_{jj}\le C_0$; diverging signal). MIS-R (ii) (l.142–160) already allows general designs on interface events. | **A** for M2 (alternative route); Cor G(b) **O** |
| Paper path for the sharp margin (A7, Conj. 3.3) | `Theory_work/Dept/song_assumptions/ASSUMPTIONS_AND_PROOF_PATHS.md` §3.3, l.279–322; obligations l.405 | Not a proof. Four obligations are listed as unwritten (truncated superset sum, per-base mixed odds, $k>\bar m_d$ step, size lemma). | Matches A7. | **R**: only the $\bar a\equiv1$ case is recommended (§B.2 upgrade) |
| Paper path for the fixed-dimension general law | `THEOREM_DEFINITIONS.md` l.215–219; `ASSUMPTIONS_AND_PROOF_PATHS.md` §3.4 | A sound sketch; no proof file. | Matches Conj. 3.6(a). | to be written (M1) |
| T04: contraction without beta-min | `Docs/Theory/proofs/T04_A3_contraction/PROOF_v2.tex` | Not read. Recorded as proved, two reviewers. | Fixed design, in-sample prediction and parameter error, floor SE; not the joint Hellinger statement. | **O** (superseded by W3-DIST) |
| T06/T07: ties, ranking ceiling | `Docs/Theory/proofs/T06_T07_identifiability_size_prior/PROOF_v2.tex` | Not read. | Not a Song counterpart. Only "HPM $=S_0$ when $\pi(S_0)>\tfrac12$" is used, and T03 (ii)–(iii) proves it directly (l.362–364). | **O** |
| `COLLECTED/`, T09–T31 | `Docs/Theory/proofs/COLLECTED_PROOFS_v2.tex` | Sampler results. | Deferred by the owner's scope ruling. | **O** for these targets |
| Lean | `Lean/BVSCert/BVSCert/Basic.lean` | Stub. | — | start from L-LEAN snapshot |

Findings that need action:

1. **The paper understates its own selection theorem.** Thm 3.2 asks for a floor on $O(s\log n)$ sets and fixed effects; the chain T03R → W3-POST Thm 1 → B3 proves it with a floor on $(2A+2)s+2$ predictors and threshold-scale effects.
2. **Files missing from this branch.** `Theory_work/Wave3/W3-D2`, `W3-D3` and `Docs/Writing/manuscript/sections/or5_assumptions.tex`, `or6_theorems.tex`, `supplement_or.tex` are on `main` but not on `dept/theory @ 40febfb6`, although `TH_PREP.md` and `THEOREM_DEFINITIONS.md` cite them. Whoever writes the proofs needs them in one tree.
3. **A load-bearing proof lives under `Old_Projects`.** T03R is the only place where the floor split is proved.
4. **Status strings disagree.** Several proof files still carry "PROVED (by this seat, unchecked)" in the header (`L1a_size_tail.md`, `M_misr.md`, `R_reduction.md`, W3-D3 `ASSEMBLY.md`) while the registry and `TH_PREP.md` say "proved and independently checked". The check records exist; the headers should be reconciled before the paper cites the supplement.
5. **Two statement translations I did not verify:** the paper's Thm 3.5 (correlation-scale floor) against Cor G(b) (covariance-scale floor with $\max_j\Sigma_{jj}\le C_0$), and the paper's Thm 3.2 (standardised effects with A6) against W3-D3's raw-scale $b_{lo}\le|\beta^*_j|\le b_{hi}$. Both become moot if the proposed statements are adopted.
6. **No gap found** in T03, in T02(i), or in the T03R modifications.

---

## D. Misspecification plan

### D.1 What Song and Liang prove

SL Thm 4: the full model is Gaussian linear, the predictors have finite second moments, and the method is run on a *fixed* subset that omits true predictors. Given the subset, the response is then in general neither Gaussian nor linear, and the posterior concentrates almost surely at the Kullback–Leibler projection $f_0$. Cor 2 adds inclusion of the pseudo-true support, in probability. So their result is a fixed-dimension statement under a genuinely wrong likelihood. HQ's point 4 is correct: the paper's Thm 3.5 assumes the conditional law of the response given the candidates is exactly Gaussian linear, so it is a correctly specified problem with a different parameter.

### D.2 Options

| Option | Content | Feasibility | Risk | Effort |
|---|---|---|---|---|
| 1. Keep as is | Thm 3.5 (Gaussian predictors) proved; Conj. 3.6(a), (b) | no work | referee objection stands; two conjectures remain | 0 |
| 2. **Recommended** | **Thm 3.4** under A8: any response law, fixed candidate set; density (a.s.), inclusion (a.s.), exact selection under A8(b). **Cor 3.5** under A9′, A10: high-dimensional candidates, as a corollary of Thms 3.1–3.2. Thm 3.5 disappears. | Thm 3.4: new, elementary. Cor 3.5: immediate. | low | 2–3 lead-days plus review; half a day |
| 3. General law, growing candidate dimension | density and selection for any second-moment law with $|\mathcal C|\to\infty$ | not with the present method of proof | high | open-ended |
| 4. Extension of option 2 | Thm 3.4 for a law that changes with $n$, in probability, with a risk gap $\min_{S\not\supseteq S_0^{\mathcal C}}(\sigma_S^2-\sigma_{\mathcal C}^2)/\sigma_{\mathcal C}^2\ge C\log n/n$ and uniformly bounded score variances | feasible (Chebyshev replaces the LIL) | low–medium | 2 lead-days; optional remark |

### D.3 Routes

- **Option 2, Thm 3.4:** §B.3. The tools are the SLLN, the closed-form score, Lemma H and, for exclusion, the law of the iterated logarithm. Nothing from the high-dimensional machinery is used, and the De Blasi–Walker result that SL rely on is not needed.
- **Option 2, Cor 3.5:** §B.4. Under A9′ the candidate data satisfy A1.
- **Option 3, why it fails now.** Three steps of the selection and density proofs use the Gaussian likelihood exactly: the identity $E^*[m_b(S)/f_0]=1$ that gives the size tail without any eigenvalue condition (T01/T02 `lem:num`, l.317–322); the exact $\chi^2$ laws of the fitted noise (T03 l.171); and the truncated moment of T03 `lem:chi`(b). Under a wrong error law a null predictor gains $\varrho\,\chi^2_1$ with a variance-inflation factor $\varrho$, and with $p_{\mathcal C}$ nulls the best of them gains about $2\varrho\log p_{\mathcal C}$ against a price $\log p_{\mathcal C}+\tfrac12\log n$. Selection then needs a condition of the type $(\varrho-1)\log p_{\mathcal C}<\tfrac12\log n$; this budget is heuristic, not proved. It is the mechanism behind the failures that Grünwald and van Ommen report, and it is not a Song–Liang counterpart, since their Thm 4 is for a fixed subset.

### D.4 Risks of the recommendation

- The reader may ask why the high-dimensional result needs A9′ while the fixed-dimension one does not. The paper already answers this with the Grünwald–van Ommen sentence; keep it, placed between Thm 3.4 and A9′.
- A8(b) is an extra moment condition relative to SL. It is used only for exclusion, which SL do not prove.
- A fixed law in A8 excludes effects that shrink with $n$. That is SL's setting too; option 4 removes the restriction if a referee asks.
- Calling Cor 3.5 a corollary gives up a "theorem" in the count. It is the honest label, and Table 1 then reads: Thm 4 ↔ Thm 3.4(i); Cor 2 ↔ Thm 3.4(ii), with exact selection in (iii); many candidates ↔ Cor 3.5.

### D.5 Recommendation

Adopt option 2. Keep A8 (with part (b)), restate A9 as A9′, keep A10. Prove Thm 3.4, state Cor 3.5, delete the Gaussian-predictor theorem and Conj. 3.6. Do not target option 3. Resulting map:

| Song & Liang | Here | Status after the plan |
|---|---|---|
| Thms 1–2, Cor 1 | Thm 3.1 | proved |
| Thm 3 | Thm 3.2(a) | proved |
| Thm S, Cor S1 | Thm 3.2(b), Cor 3.3 | proved |
| Thm 4 | Thm 3.4(i) | to be proved (low risk) |
| Cor 2 | Thm 3.4(ii), (iii) | to be proved (low risk) |
| — | Cor 3.5 | corollary |

No conjecture remains in the main text.
