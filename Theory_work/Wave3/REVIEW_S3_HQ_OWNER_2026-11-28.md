# Review of Section 3 (assumptions and theorems): HQ and owner positions, 2026-11-28

Source reviewed: Writing's `sections/03_theory.tex` (writing/main 3445496d), synced to Theory's final package (dept/theory 448d236a).
HQ read it as a first human referee would. The owner then gave his take. This note records both and the resulting direction.
Status per point: **RULED** (owner decision), **AGREED** (both agree), **OPEN** (to revisit).

## Overall
- HQ verdict as referee: **major revision**. The basic assumptions are acceptable; the gap is the results, not the conditions.
- The owner agrees with the general direction. **Next: settle the assumptions, then proofs, then Lean for every theorem.**

## Points

### 1. Two of the three Song counterparts are conjectures, and proofs are not included (AGREED)
- **HQ:** selection near the detection threshold (Conj. 3.1) and misspecification under a general response law (Conj. 3.2,
  the counterpart of Song & Liang Thm 4) are conjectures. Proofs of Thms 3.1–3.3 are promised but absent. A referee would
  say the paper does not yet contain the counterparts it advertises.
- **Owner:** proofs are the next build, as soon as the assumptions are settled.
- **Direction:** settle the assumptions → write paper proofs → review (POLICIES §1b: 8.5 bar for theorems) → Lean.

### 2. Lean for every theorem (RULED)
- **Owner:** every theorem we prove gets Lean.
- **HQ (agreed, practical scope):** the deterministic and combinatorial core is fully checked. Any standard probability
  fact not yet in Mathlib (e.g. sub-Gaussian concentration on sparse sets) enters as a **named, cited axiom**, listed
  explicitly and reviewed. No hidden `sorry`. Order: paper proof → review → Lean.

### 3. Regime of the selection theorem (AGREED on fixed $s$; effect-size target to confirm)
- **HQ:** Thm 3.2 assumes fixed-size effects ($\beta_{\min}\ge\underline b$), which sit a factor of order $\sqrt n$ above
  the detection threshold, plus a fixed eigenvalue floor on sets of size about $5(A+1)(s_0+1)\log n$. A referee would call
  this the easy regime.
- **Owner:** a clear bound on the size of the true model is key in Song. The goal is to find a small true set in a vast
  ocean of predictors.
- **Reconciled:** both points stand. **Keep fixed $s$** (a small true set). HQ's concern is effect *magnitude*, not model
  size. **HQ proposal (owner to confirm):** the headline selection theorem should let effects shrink toward the
  threshold, $\beta_{\min}\gtrsim\sqrt{\log(p\sqrt n)/n}$, as in Song's Theorem 3. The fixed-effects version becomes a
  corollary.

### 4. Misspecification theorem (OPEN, owner: "go deeper later")
- **HQ:** Thm 3.3 (Gaussian predictors, Gaussian linear response on the candidate set) is correctly specified with a
  different parameter $\beta^{\mathcal C}$. It is not misspecification in Song's sense (KL projection under a wrong
  likelihood, their Thm 4). Our true counterpart is Conj. 3.2(a).
- **Direction:** revisit later. Meanwhile, label Thm 3.3 honestly ("omitted Gaussian predictors") or upgrade it once
  Conj. 3.2(a) is proved.

### 5. Selection-margin assumption (OPEN, owner: "dig into later")
- **HQ:** it uses an accounting set $Q_n$, a leakage, $h(\lambda)$, $\bar u_d$ and binomial counts, so it fails the
  naturalness and readability test. It is the data-informed assumption, and it reads that way. Proposal: state the
  beta-min sufficient condition (the current Remark) as the main assumption, and move the margin form to the supplement
  as a refinement.
- **Direction:** revisit later. It is flagged as the main readability risk in Section 3.

### 6. Dimension (RULED)
- **HQ:** we assume $p\le n^A$; Song & Liang allow $\log p=O(n^\alpha)$, and a referee will ask why.
- **Owner:** polynomial $p$ (e.g. $n^5$) is large enough for any real-life experiment.
- **Ruling:** drop the word "ultrahigh" everywhere; the setting is "high-dimensional", with $p\le n^A$. Add one sentence
  stating polynomial growth as a deliberate choice (e.g. $n=500$, $p\le n^5\approx3\times10^{13}$). Already sent to
  Writing and Theory.

### 7. Density and readability of the section (AGREED, owner: "we can correct this")
- **HQ:** notation ($\mathrm{pen}_n$, leakage, $h$, $Q_n$, $\bar u_d$) sits inside the prose; the section is further from
  Song's cadence than the rest of the paper.
- **Direction:** rewrite to Song's cadence. Definitions go in displays, each assumption gets a short intuition, and
  technical refinements go to the supplement.

## Assumptions HQ judged acceptable as they stand
- Gaussian linear model with random design; sparsity with fixed $s$; $p\le n^A$; sub-Gaussian sparse combinations
  (variance-scaled, as in Rudelson–Zhou).
- No near-exact collinearity, $n\,\lambda_{\min}\{\mathrm{Corr}(x_T)\}\ge c_\psi$ on sparse sets: milder than the usual
  fixed floor, and well argued.
- Bounded effects (upper bound): unusual direction, but the explanation (it excludes the noiseless limit, a $g$-prior
  artifact) is convincing.
- **Strength to keep:** the density-consistency theorem holds for our fixed prior with no tuning sequences, an improvement
  over Song & Liang's conditions (9)–(14).

## Related work in flight
- **CITE-AUDIT** (Theory, fresh Opus lead, double-blind Sonnet + Sol, quotes mandatory) is verifying that every cited
  paper says what the package and Section 3 claim. Its fixes feed the same rewrite.

## Requested from Theory (when the owner releases this note)
1. Confirm or counter-propose point 3 (a headline selection theorem with shrinking $\beta_{\min}$, fixed $s$).
2. A proof plan for the three Song counterparts in their final form, with a Lean plan (scope, named axioms) per theorem.
3. Hold points 4 and 5 for the owner's deeper discussion; propose options, don't decide.

## Addendum: assumptions only (HQ's referee view; numbering as in the draft at writing/main df9da1e6)

| # | Content | Used for | HQ verdict |
|---|---|---|---|
| A1 Gaussian linear model | $y=\alpha^*+x^\top\beta^*+\varepsilon$, Gaussian noise, random design, iid rows | all | standard; accept |
| A2 Sparsity | $s_0\le s$, $s$ fixed | all | Song's core setting; accept (owner: a small true set is key) |
| A3 Dimension | $2\le p\le n^A$ | all | accept (owner ruling) |
| A4 Sub-Gaussian | variance-scaled sub-Gaussian combinations of up to $c\log n$ predictors | all | standard (Rudelson–Zhou); accept |
| A5 No near-exact collinearity | $n\,\lambda_{\min}\{\mathrm{Corr}(x_T)\}\ge c_\psi$ on sparse sets | density; conjectured selection | milder than a fixed floor; accept |
| A6 Bounded effects | $\lvert\beta_j^*\rvert\,\mathrm{sd}(x_j)\le\bar b\sigma_*$ | density, selection | unusual but well argued; accept |
| A7 Selection margin | $Q_n$, leakage, $h$, $\bar u_d$, binomial terms | conjectured selection | NOT natural or readable |
| A8 Fixed candidate dimension | fixed candidate set, any response law, second moments | Conj. misspec (a) | mild; accept |
| A9 Omitted predictors | left-out signal linear in the candidates plus independent Gaussian; A3–A6 for the candidate problem | Conj. misspec (b) | acceptable but strong |
| A10 Sparse pseudo-true | $\lvert S_0^{\mathcal C}\rvert\le s_{\mathcal C}$ fixed | Conj. misspec (b) | natural; accept |

In-theorem conditions:
- **Thm 3.2:** fixed effects $\beta_{\min}\ge\underline b$ (easy regime); fixed eigenvalue floor $\varphi^2$ on sets of size $5(A+1)(s_0+1)\log n$ (large sets).
- **Thm 3.5:** Gaussian candidate predictors with a Gaussian linear response given them (strong; effectively well-specified); floor on sets of about $3(A+1)(s+1)\log n$; projected effects above the threshold by a diverging factor.

Open decisions (owner): (1) replace A7 in the main text by beta-min, moving the margin form to the supplement? (2) headline selection with $\beta_{\min}\ge C\sqrt{\log(p\sqrt n)/n}$? (3) floor on sets of size $O(s)$ instead of $O(s\log n)$? (4) misspecification: keep A9 and the Gaussian-predictor version, or target the general-law version under A8?
