# HQ curated packet: assumptions, theorems and proof plan (2026-11-28)

Curated by HQ from two independent advisers, Fable 5.2 (Claude Third) and Astra 6.2: Phase 1 (independent) and Phase 2 (each read the other).
Sources in this folder: `FABLE_PHASE1.md`, `ASTRA_PHASE1.md`, `FABLE_PHASE2.md`, `ASTRA_PHASE2.md`, `REVIEW_S3_HQ_OWNER_2026-11-28.md`.
**HQ check:** the two advisers reached all 4 decisions independently and agree on them. Their remaining differences are
resolved below. Every "already proved" claim is narrowed to what was actually checked.

Owner rules that bind this work: fixed $s$; $p\le n^A$ (never "ultrahigh"); assumptions natural and general (Song &
Liang's style); every proved theorem gets Lean (deterministic core checked, named and cited probability axioms, no hidden
`sorry`); councils are Opus + Sol + Opus with the same agents across rounds; plan bar 8, proof bar 8.5; Fable arbiter
after 3 rounds.
**Definition of done:** every assumption accepted company-wide, AND every targeted theorem has at least a partial,
promising, reviewed proof.

## 1. Final assumption set (proposed for company acceptance)

| # | Status | Final form |
|---|---|---|
| A1 Gaussian linear model | keep | as in the draft |
| A2 Sparsity | keep | $s_0\le s$, $s$ fixed. Selection results assume $1\le s_0\le s$ |
| A3 Dimension | keep | $2\le p\le n^A$ |
| A4 Sub-Gaussian | keep | as in the draft (every fixed $c$) |
| A5 No near-exact collinearity | keep | $n\lambda_{\min}\{\mathrm{Corr}(x_T)\}\ge c_\psi$ on sparse ($O(\log n)$) sets |
| A6 Bounded effects | keep | as in the draft. A bounded-SNR alternative (A6′) may appear only as a supplement remark |
| **A7 → A7′ Identifiability and signal** | **replace** | (a) fixed floor $\lambda_{\min}\{\mathrm{Corr}(x_T)\}\ge\varphi^2$ for all $T$ with $\lvert T\rvert\le\min\{p,\,s_0+j_0\}$, $j_0=\lceil(2A+1)s_0\rceil+1$; (b) standardised beta-min $b_{\min}=\min_{j\in S_0}\lvert\beta_j^*\rvert\,\mathrm{sd}(x_j)/\sigma_*\ \ge\ C\sqrt{\log(p\sqrt n)/n}$ with $C$ a sufficiently large fixed constant. The old margin A7 and its conjecture move to the supplement |
| A8 Fixed candidate dimension | keep | fixed candidate set, any response law, finite second moments, $\mathrm{Var}(x_{\mathcal C})$ nonsingular, $\sigma^2_{\mathcal C}>0$ |
| **A9 → A9′ Omitted predictors** | **simplify** | the candidate residual $\varepsilon_{\mathcal C}$ is $N(0,\sigma^2_{\mathcal C})$ and independent of $x_{\mathcal C}$. The structural form (left-out signal linear plus Gaussian) goes into a remark, equivalent under A1. The candidate versions of A3–A7′ are listed in the corollary |
| A10 Sparse pseudo-true model | keep | as in the draft |

**The paper must justify A7′(a)** with Astra's example: two predictors with correlation $1-c/n$ satisfy A5, yet the
KL divergence between "the effect is on one" and "the effect is on the other" is $c\,b_{\min}^2\to0$ at the threshold
scale. So a beta-min with A5 alone cannot give selection, and a fixed floor on small sets is needed.

## 2. Final theorem list (one-to-one Song & Liang counterparts)

1. **Density consistency** (SL Thms 1–2). As in the draft (Thm 3.1), under A1–A6, at a fixed level $M\ge M_0$.
   **Status:** proved (`W3-DIST` Theorem A); needs transcription.
2. **Selection consistency, headline** (SL Thm 3, Thm S). Under A1–A6 and A7′, with $1\le s_0\le s$:
   - (a) every strong predictor is included, with no condition on the others;
   - (b) $1-\Pi(S_0\mid D_n)=O_P(r_n)$, uniform PIP convergence, and $\mathrm{HPM}=\mathrm{MPM}=S_0$ with probability tending to 1.

   **Corollary:** fixed effects. The sufficient constant goes in the supplement: $C=4\sqrt{c_0}/\varphi$,
   $c_0=\max\{4C_*,32[k(A+1)+2]\}$, about 49.8 at $s_0=5$, $A=2$, $p=n^2$. It is labelled not sharp.
   **Status:** the fixed-design proof is proved and council-accepted (`W3-T03ACC` T03♯; `W3-POST` Thm 1). The
   random-design bridge exists (`W3-DIST/work/E_bridges/B3.md`) and needs a small modification: replace the divergence
   in step 5 (item (vi)) by a fixed $c>c_0$, tighten the window to $s_0+j_0$, and use the fixed-$c$ design event in
   step 6.
3. **Misspecification, fixed candidates, any response law** (SL Thm 4, Cor 2). Under A8:
   - density consistency to the KL projection $f_0$, and inclusion of $S_0^{\mathcal C}$, almost surely, via the
     finite-model SLLN;
   - exact support almost surely if $E(x_j^2\varepsilon^2_{\mathcal C})<\infty$, via the LIL.

   **Status:** NEW proof, elementary, low risk.
4. **Corollary: many candidates** under A9′, A10 and the candidate versions of A3–A7′. Density and selection follow from
   items 1–2 applied to the candidate problem. Expectation rate from `W3-POST2/lemmas/C_expectation.md`.
   **Dropped:** the separate Gaussian-predictor theorem (old Thm 3.5) and both conjectures (selection margin;
   misspecification). A general response law in growing dimension is out of scope.

## 3. Proof plan, in order (Wave 2 leads)
1. **Selection (Lead-S).** The B3 bridge modification above, then one forward-written proof from `W3-T03ACC` (T03♯),
   T01/T02 and T03, including part (a) (`W3-POST` Thm 1 item 5(b) = T03S.4). About 3–6 person-days plus review.
2. **Misspecification under A8 (Lead-M).** New proof in 4 steps, as in both reports. About 3–6 person-days plus review.
   Then the many-candidate corollary, one paragraph.
3. **Density (Lead-D).** Transcription of `W3-DIST` Theorem A at a fixed level. About 4–8 person-days plus review.
4. **Review** at the 8.5 bar (Opus + Sol + Opus, same council across rounds; the manager rules on findings).
5. **Lean (Lead-L), after each paper proof passes.**
   - Formalise the deterministic cores, posterior summaries, shared score and matrix primitives, and selection in
     interface form; then A8; then density.
   - Named, cited axioms: Cochran; Laurent–Massart; chi-square and Gaussian integral identities; Bernstein; the
     relative-deviation VC inequality (Anthony & Shawe-Taylor 1993); the LIL.
   - Reuse the archived L-LEAN finite-posterior results (e.g. `T21HPM.lean`). The active `Lean/BVSCert` is a stub.
   - Effort: density 10–20 person-weeks, selection 6–12, A8 4–8.

## 4. Checklist that must survive transcription
- The capped comparison window covers $\min(p,m+s_0)$; comparison unions are clipped at $p$.
- The sample-mean (intercept) term $\bar\varepsilon^2$ appears in the population distance.
- The starting $n$ may depend on $M$, so the density result is stated for each fixed $M\ge M_0$.
- No response-dependent scaling before conditioning on the design.
- Selection assumes $s_0\ge1$.

## 5. Optional, later (not needed for "done")
- A sharpened constant, about $5.16(1+\eta)$. It needs one extra design estimate (Astra's repair, `ASTRA_PHASE2.md` §2),
  separate review, and gives the rate $O_P(r_n+n^{-\gamma})$.
- The null model $s_0=0$.
- A6′ (bounded SNR) as a supplement remark.

## 6. Organisational notes from the audit
- The selection proof is a diff chain across several files; Lead-S should write it forward as one proof.
- Several proof headers say "unchecked" while the registry says checked; Lead-A reconciles them.
- `W3-D2` and `W3-D3` and the manuscript sections live on main; work from main plus dept/theory.
