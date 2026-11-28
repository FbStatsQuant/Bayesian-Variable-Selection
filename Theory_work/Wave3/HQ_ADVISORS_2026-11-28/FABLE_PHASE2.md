# FABLE_PHASE2 — response to ASTRA_PHASE1 (Fable 5.2), 2026-11-28

Read: `ASTRA_PHASE1.md` (no notes folder present). One round. Notation as in my Phase 1.

## 1. Where we agree

The two reports were written independently and agree on every decision.

- **Decisions 1–3: yes.** Replace A7 in the main text by a beta-min plus a fixed correlation floor on small sets; headline theorem with $\bar\beta_{\min}\ge C\sqrt{\log(p\sqrt n)/n}$ and fixed $s$; fixed effects as a corollary; A7 to the supplement as a conjecture.
- **Two floors.** Fixed floor $\varphi^2$ on at most $s_0+j_0$ predictors, $j_0=\lceil(2A+1)s_0\rceil+1$; A5 ($c_\psi/n$) on the $O(\log n)$ sets. Same proof source: T03♯ with $\mathrm{SE}_\lambda(j_0)$ and $\mathrm{SE}_w(m^\sharp_n;g_0)$.
- **Same constant.** Both of us get $C=4\sqrt{c_0}/\varphi$ (strict), $c_0=\max\{4C_*,32[k(A+1)+2]\}$, with $\varphi_0^2=\varphi^2/4$, $g_0=c_\psi/8$. Both say it is a proof constant, not a detection boundary.
- **The Remark's constant is not a theorem.** It shows a sufficient condition for A7, and A7 has no proof.
- **Density.** Thm 3.1 is proved by `W3-DIST` Theorem A; publish the fixed-level form (the paper's wording already is). Keep A1–A5 unchanged.
- **Decision 4.** Lead with A8: density and inclusion almost surely under second moments; exact support under $E(x_j^2\varepsilon_{\mathcal C}^2)<\infty$ via the LIL. Same four proof steps in both reports. High-dimensional omitted predictors as a corollary under a Gaussian reduction, with A4 in place of Gaussian rows. A general law in growing dimension is a separate research problem.
- **Expectation rate** is available from `W3-POST2` Claim C case (i).
- **Lean:** the checkout has a stub only; same axiom family (Cochran, Laurent–Massart, Bernstein, LIL).

## 2. Where we differ, and a proposed resolution

| Point | Astra | Fable (Phase 1) | Resolution |
|---|---|---|---|
| A6 | keep | optional A6′ (bounded signal-to-noise) | **Keep A6.** Astra's observation settles it for selection: with the small-set floor, a bounded signal-to-noise ratio already implies A6 with $\bar b^2=\bar\kappa/\varphi^2$. For density A6′ would still work (through $\|\theta^*\|^2\le nM/g_0$), but it changes a checked bridge for little gain. Put A6′ in a supplement remark at most. |
| Which bridge to start from | W3-D3 `B3w`, with new two-floor and finite-slack steps | `W3-DIST` bridge B3 | **Start from `W3-DIST/work/E_bridges/B3.md`.** It already has both floors (items (iv), (v)) under A4–A5 with relative covariance control. Only item (vi) changes, from the BM-$\infty$ envelope to BM($c$). Its small-set window $(2A+3)s+2$ should be tightened to $s_0+j_0$. So the new bridge work is smaller than Astra's B.2 suggests. Astra's two cautions apply and should be checklist items: comparison unions clipped at $p$, and no response-dependent scaling before conditioning on the design. |
| Sharpened explicit constant | not proposed | optional upgrade, $(1+\eta)(1+\sqrt{2A+3})\sqrt2$ | **Not in the headline, not a prerequisite.** Keep it as a later, separately reviewed improvement. It is my derivation only and unreviewed. |
| Inclusion of strong predictors without a condition on the others (SL Thm 3) | not in the theorem | part (a) of Thm 3.2 | **Include it.** It is item 5(b) of `W3-POST` Thm 1 (= T03S.4, no beta-min on the other coordinates), already proved, and it is the literal counterpart of SL Thm 3. |
| A9 wording | structural: $x_O^\top\beta^*_O=a+x_{\mathcal C}^\top\gamma+u$; candidate conditions listed in the corollary | A9′: residual Gaussian and independent of $x_{\mathcal C}$, with A3–A6 folded in | **Combine.** Assumption = "the residual $\varepsilon_{\mathcal C}$ is $N(0,\sigma_{\mathcal C}^2)$ and independent of $x_{\mathcal C}$" only. Following Astra, the candidate versions of A3–A7′ are named in the corollary. The structural form goes in the remark (equivalent under A1). Astra's audit supports this: the conditional form suffices with no full omitted-vector representation. |
| Old Gaussian-predictor theorem | "remains available by its original proof" | delete as a separate result | **One corollary.** With A4–A5 as the paper states them, the corollary covers the Gaussian case. Mention the expectation form in one sentence. |
| $s_0=0$ in selection | restrict to $1\le s_0\le s$ | check and include | **Restrict to $s_0\ge1$ now.** The null-model case is an optional later check. |
| A4/A5 window for selection | one window, $q=\min\{p,\lfloor5(A+1)(s_0+1)\log n\rfloor\}$ | A4–A5 as stated (every fixed $c$) | No change to the paper (A4–A5 already hold for every $c$). Record Astra's single window in the supplement proof. |
| VC step in Lean | derive the in-house inequality in Lean | axiom: Anthony & Shawe-Taylor (1993) | Axiomatise the published relative-deviation inequality; prove the class count and the algebra to our one-sided form in Lean. |
| Lean effort | 10–20 person-weeks (density), 6–12 (selection), 4–8 (A8) | lead-days | **Use Astra's ranges.** See §3. |

## 3. Corrections to my Phase 1

1. **T03R is not stranded in `Old_Projects`.** A pinned, council-accepted copy is in this checkout: `Theory_work/Wave3/W3-T03ACC/sources/W1-T03R/PROOF.md`, with a locked statement and three blind Sol line checks (LC-A, LC-B, LC-C: "VERIFIED", 0 gap, 0 error; `W3-T03ACC/REPORT.md` §2). I missed the folder. My audit finding 3 is withdrawn; cite `W3-T03ACC` as the source for T03♯.
2. **"Already proved" was too strong for the population statement.** The fixed-design theorem is proved and accepted. The random-design statement with two floors and a finite beta-min multiple is not yet assembled or reviewed. Astra's wording is the accurate one: the missing work is a bridge between two existing proofs (3–6 person-days).
3. **Lean effort was optimistic.** My day counts assumed a narrow deterministic core. Building the score, determinant and projection infrastructure and deriving the net and class-count arguments is weeks, as Astra says.
4. **A6′ withdrawn** from the recommendation (see §2).
5. **Window.** State the small-set floor as "at most $\min\{p,\,s_0+j_0\}$ predictors"; my $(2A+2)s+2$ is an upper bound for it.
6. **Two translations I had left unverified are covered by Astra's audit:** `W3-MISR-R/lemmas/G2_corr.md` gives the correlation-unit form of the omitted-predictor result, and W3-D3's normalised coordinates map to the paper's effect units by a deterministic rescaling.
7. **A7′(a) deserves its own justification in the paper.** Astra's example: two predictors with correlation $1-c/n$ satisfy A5, yet the $n$-observation Kullback–Leibler divergence between "effect on one" and "effect on the other" is $c\,\bar\beta_{\min}^2\to0$ at the threshold scale. So beta-min with A5 alone cannot give selection.

**W3-DIST.** I led it, so Astra's reading carries the weight here. Astra checked the decisive steps (`lemmas/X.md:63–180`, `work/B_transfer/T.md:76–166`, `DIST12.md:23–77`, `B2.md`, `ASSEMBLY.md`) and reports no missing density lemma. Three things from that reading must survive the transcription: the capped window must cover $\min(p,m+s_0)$; the sample-mean (intercept) term $\bar\varepsilon^2$ must appear in the population distance; and the starting $n$ may depend on $M$, so the paper states the result for each fixed $M\ge M_0$. I have nothing to add or dispute.

## 4. Final recommendation

**Decisions**
1. **A7 → beta-min: yes.** Main text: fixed floor $\varphi^2$ on at most $\min\{p,s_0+j_0\}$ predictors, and $\bar\beta_{\min}\ge C\sqrt{\log(p\sqrt n)/n}$. A7 and its conjecture go to the supplement.
2. **Headline selection theorem: yes,** with $C=C(s,A)/\varphi$, value $4\sqrt{c_0}$ given in the supplement and described as not sharp. Part (a): inclusion of each strong predictor. Part (b): $1-\Pi(S_0)=O_P(r_n)$, PIPs, $\mathrm{HPM}=\mathrm{MPM}=S_0$. Corollary: fixed effects. Assume A1–A6 with $1\le s_0\le s$.
3. **Floor on $O(s)$ sets: yes,** with A5 on the logarithmic sets.
4. **Misspecification:** Theorem under A8 (any response law, fixed candidates): density and inclusion almost surely; exact support under finite score variances. Corollary for many candidates under the Gaussian-residual assumption and A10. Drop the Gaussian-predictor theorem and both conjectures.

**Proof plan, in order**
1. Selection bridge: `W3-DIST` B3 with BM($c$), window $s_0+j_0$, clipped unions, independence check. Then one forward-written proof from `W3-T03ACC` (T03♯), T01/T02 and T03. 3–6 person-days plus review.
2. A8 theorem: new proof, steps 1–4 as in both reports. 3–6 person-days plus review.
3. Density: transcription of `W3-DIST` Theorem A at fixed level, with the three points above. 4–8 person-days plus review. The many-candidate corollary is one paragraph after 1 and 3.
4. Review at the 8.5 bar. Expectation-rate variant if wanted (2–4 person-days).
5. Lean: posterior summaries; shared score and matrix primitives; selection in interface form; A8; density. Named axioms: Cochran, Laurent–Massart, chi-square and Gaussian integral identities, Bernstein, relative-deviation VC, LIL. Plan in person-weeks, not days.
6. Optional, after the above: the explicit sharpened constant; the null model $s_0=0$.
