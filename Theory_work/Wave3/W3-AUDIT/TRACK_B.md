# W3-AUDIT — track B: are the design and data assumptions reasonable? (v1.4, conditional-comparison format, 2026-11-16)

Author: audit Fable. Each dossier: **verdict** against Song and Liang (2015) → **strongest evidence** → **holds / fails**
→ **our designs** → **candidate corollary** in primitive terms (Σ, β, σ², n, p). Nothing here is a registered result.
My own short computations on which a verdict depends were checked by an independent reviewer and are marked
"checked (AUDITCALC_check_opus.md §k)" (`reviews/AUDITCALC_check_opus.md`, 2d7c2b90: none refuted, four corrected). Lines still marked
[audit calc] or [audit reading] carry no verdict and are unchecked. Track C (internal proxy computations,
`track_C/RESULTS.md` @ 4f0f9a82, Owls part; NOTS cells pending) is cited in the design lines; it tests 19 designs that
include ours or close relatives. Citations of `W3-READER` files are **(READER pre-freeze)**: read at 7eb818e6, to be
re-pinned to the READER commit of the CP3 freeze.

## Answer (for the owner's question)

**Format rule (HQ, v1.4).** A comparison with Song–Liang is written as one conditional sentence that names the regime,
with their page and equation. One-word labels are used only where they are true in every regime of both papers, and the
text says so. No overall "stronger" or "weaker" is claimed.

1. **Same kinds of assumptions.** Our theorems and Song–Liang's rest on the same kinds of conditions: a Gaussian linear
   model, exact sparsity, a bound on the dimension, a law for the predictors, eigenvalue floors on small sets of
   columns, and nonzero coefficients that are not too small.
2. **On the designs we study, ours hold.** The assumptions of the two posterior theorems (core 1: the true model;
   core 2: the true distribution) hold on every design of the 2,400-fit study, of P6 (strong factors included) and of
   the 1M plan. The reported-model theorem (core 3) holds on S1–S4, S6, IND, AR, BLK and not on pervasive factors at
   p ≫ √n (S5, P6, FAC). The printed-estimates theorem (row 3.6) is correct as stated and reaches S1 and IND only;
   outside it, Theorem 6 (reported model) and row 3.5 (unbiased evidence) still hold.
3. **Where the papers differ, the direction depends on the regime** — chiefly on their model-size cap r̄_n, on whether
   predictors are centred, on how their β* is read, and on which of their theorems is the comparator. The summary table
   gives the comparison assumption by assumption.
4. **Conclusions are compared per theorem** (§S), not globally: against their Theorem 3 ours add specificity and exact
   selection at a polynomial rate while theirs gives sensitivity with an exponentially small error; against their
   Theorem S the two statements concern different posteriors; for the distribution theorem the distance is the same.

| Core theorem | Our designs inside |
|---|---|
| 1 and 2 (posterior) | **all** |
| 3 (reported model) | S1–S4, S6, IND, AR, BLK; not S5, P6, FAC |
| 4 (printed estimates, row 3.6) | S1, IND only |
| 5 (rate lower bound) | — (witness designs) |

**Song–Liang source.** Every "SL" reference is to the paper itself, read first-hand: Q. Song and F. Liang (2015),
J. R. Statist. Soc. B 77(5), 947–972, local file `/home/fb31/SMC_Theory_Department/refs/Song_Liang_2015.pdf` (sha256
`315c247c236b5f33…`; not in git). Page numbers are journal pages. Their supplement (20 pages; `/home/fb31/SMC_Theory_Department/refs/Song_Liang_2015_supplement.pdf`, sha256
`a584b328c859c087…`, not in git) was read for v1.3: pp. 13–16 as page images (Theorem S, its proof and remarks, Corollary
S₁), pp. 1, 4, 5, 6, 12, 17 as text (divergences d_t, proofs of their Theorems 2.2–2.4, the sampler estimates, Lemma S₂);
the other pages (SAMC details, extra simulations) were not read. "supp p." below means a page of the supplement. Their theorems are for a random design; x has law ν_x.

**Our theorems** (reader versions, `W3-READER/READER_VERSIONS.md` §1, §2, §3, §6, §9, §10): Thm 1/1′ and Thm 2 (posterior
finds the model), Thm 9 (posterior finds the distribution), Thm 6 (reported model), Thm 10 (printed estimates), Thm 3
(rate lower bound).

**Our designs** (all have i.i.d. Gaussian rows, σ = 1, fixed nonzero coefficients):
- **Study** = the 2,400-fit study: n = 200, p ∈ {500, 1000}, s₀ = 14 (one truth per group of 5, coefficients ±0.8…1.8
  times c ∈ {1, 0.5}); S1 identity; S2 AR(1) 0.5; S3 / S4 blocks of 5 with correlation 0.7 / 0.85; S5 = blocks of 5 at 0.7
  **plus a global factor** (0.3 between all columns); S6 blocks of 5 with correlation 0.4–0.9
  (`Scripts/Data_generators/gen_dev_data.R:18-41`; `Theory_work/Pause_2026-11/RERUN_SPEC.md:41-42`).
- **P6** = strong factors, n ∈ {50,…,150}, p up to 10n, s₀ ∈ {4, 8}: `cs(ρ)` one factor, ρ ∈ {0.3, 0.5, 0.7}; `fac2` two
  pervasive factors; `s5` (= S5) (`Theory_work/Wave3/W3-P6/DESIGN.md:13-17`).
- **1M** = the p = 10⁶ plan: IND; AR Toeplitz 0.6 (primary); BLK blocks of 20 at 0.5; FAC `cs(0.3)` (contingent, 10⁴
  only); s₀ = 5 (`/home/fb31/Bayesian-Variable-Selection/Docs/Experiments/P1M/EXPERIMENT_PLAN.md:87-92`, untracked).

**Track C, one caution (internal).** At (n, p) = (200, 2000) the sample proxies of visibility and of the floor on
O(log n)-sets are near 0 in most designs; single pilot cells suggest that they recover as n grows, except for a
pervasive factor with mixed-sign truths. The p = 10n trend is pending (NOTS). No inside/outside verdict below is
contradicted by track C.

"Inside / outside" means: the design, continued as a sequence in n with its structure and s₀ fixed, satisfies the
assumption. The dossiers judge the qualitative conditions (a floor bounded below, a signal on the √(log n/n) scale, a
leakage set of size n^b). The explicit constants in the proofs are conservative and are not part of the judgement
(HQ ruling, 11-16). Track C results (internal) will be cited in the "Designs" lines when they land.

---

## B1. Gaussian linear model with independent Gaussian errors (all theorems)
**Comparison: the same, in every regime** (a one-word label is kept because it holds uniformly). Their model (1) and
density (2), p. 950; ours adds an intercept.
**Evidence.** SL (2): f*(y, x) = φ(y; xᵀβ*, σ*) ν_x(dx). Ours: the same model with an intercept; Thm 9 lets σ* depend on n.
**Holds / fails.** Fails for heavy-tailed or heteroscedastic errors; no theorem of ours or of SL covers them.
**Designs.** All inside (Gaussian noise generated). **Corollary.** None needed.

## B2. Dimension p ≤ n^A (all theorems except Thm 3(a))
**Comparison (two ranges, two comparators).** *Upper range.* Their Hellinger results allow P_n < exp(Cn^α), α ∈ (0, 1)
(Corollary 1, p. 954). Their selection result, Theorem S, needs log(√n/r_n) ≻ √(log P_n) (supp p. 13, condition 2),
hence log P_n ≺ (log n)²/4; Corollary S₁ states P_n < n^{κ log n}, κ ∈ (0, ¼) (supp p. 16). Ours needs log p ≤ A log n.
So ours admits fewer dimensions in both comparisons: far fewer than Corollary 1, slightly fewer than Theorem S.
*Lower range.* They assume P_n ≻ n^θ (p. 950) and r_n ≺ P_n ((13), p. 952), so P_n → ∞; ours admits bounded p. Neither
range contains the other.
**Evidence.** The registry records it as a consequence of the prior and the proof technique, with exponential p "OPEN"
(`assumptions.tsv` A:P-POLY). It enters through union bounds over models of O(log n) variables.
**Holds / fails.** Holds for every polynomial regime, p ≫ n included. Fails only for log p of polynomial order in n.
**Designs.** All inside: the largest exponent is 1M at n = 200, A = log 10⁶ / log 200 ≈ 2.6.
**Corollary.** None; the constant A enters the other assumptions only through set sizes of order (A + 1)s₀ log n.

## B3. Exact sparsity with s₀ fixed (Thm 1, 2, 6, 10; Thm 9 with "at most s")
**Comparison: the same as their strict sparsity (4), p. 950, which their Theorems 2, 3 and S use** (uniformly true for
those theorems; label kept). Their Theorem 1 alone also allows (3), p. 950, under which the number of nonzero
coefficients may grow; ours does not cover that case.
**Evidence: it cannot be dropped.** Theorem 3(a) (`W3-PSHARP:B@1.0.0`, "PROVED-CHECKED; council R2, …"): on every design
π(S₀ | y) ≤ (1 + (s₀ + 1)/(3√n))⁻¹, so π(S₀ | y) → 1 forces s₀ = o(√n), and the rate √(log n/n) forces s₀ = O(√log n).
**Designs.** Inside as sequences with s₀ fixed. At the simulated sizes the same bound is informative [audit calc]:
Study (s₀ = 14, n = 200) π(S₀ | y) ≤ 0.74 for every data set; P6 (4, 50) ≤ 0.81; 1M (5, 200) ≤ 0.88. At these sizes the
posterior is a mixture over S₀ and its neighbours; that is its shape, not a failure (card note ENG-D17).
**Corollary.** None. A generator rule s₀ = ⌊√n⌋ would be outside (`Docs/THEORY.md:325`).

## B4. Signal size: bounded above, and fixed nonzero or beta-min at √(log n/n) below
(Thm 1 (A3), (A6); Thm 2 (A2); Thm 6 / 10 (A2); Thm 9 (A5); none below in Thm 9.)
**Comparison (depends on how their β* is read).** Their theorems state no lower bound on the nonzero coefficients; their
Theorem 1 bounds the coefficients above through (3) and (8) (pp. 950, 952). *(i) If β* is one fixed sequence* — the
natural reading: every n-dependent quantity of theirs carries a subscript and β*, σ* carry none, and (3)–(4) are limits
of partial sums (p. 950) — the nonzero coefficients are constants by their statement; then the fixed signals of our
Theorems 2, 6, 10 ask the same, and Theorems 1 and 9, whose coefficients may vary with n, admit more. *(ii) If β* may
vary with n*, their statements set no size condition, and their proof steps need rates: β*_t²δ_n ≥ 20σ*²ε_n² for Theorem
3 (from d² ≥ min{δ_n, β*_t²δ_n/(20σ*²), 1 − √0.8}, supp p. 6) and n·l_n·c² ≻ r̄_n log P_n with c = min_{i∈t}|β*_i| for
Theorem S (supp p. 15); then our fixed signals ask more than those steps use, and Theorem 1's beta-min,
θ*²_min φ₀² n ≥ c₀σ*² log n, has the same form as their rates, at a fixed multiple of log n where theirs is a diverging
multiple of r̄_n log P_n. **Does it matter for our designs? No:** all have fixed nonzero coefficients.
**Evidence.** Thm 2, 6, 10 assume only fixed nonzero coefficients. The explicit beta-min is used
only in the fixed-design Thm 1, at the usual order σ√(log n/n); Thm 1′ and Thm 9 have none. Without any lower bound
specificity can fail (numerical counterexample, Thm 1 remark (ii)).
**Designs.** All inside (fixed nonzero coefficients, far above the √(log n/n) scale as n grows). Track C: the beta-min
rate and the identifiability margin grow like n^0.7–1.15 in all 19 designs (P7).
**Corollary.** Thm 2 is already in primitive terms: b_lo ≤ |β*_j| ≤ b_hi on S₀.

## B5. Eigenvalue floor on small sets (Thm 1 (A4) / (A4′); Thm 2 (A3); Thm 6 / 10 floors; Thm 9B (A6a))
**Comparison (depends on r̄_n and on the theorem).** *Counterparts.* Condition 3 (p. 955), for their Theorem 3: on
r̄_n + 1 columns that contain a true predictor, at a vanishing level δ_n ≻ ε_n². Conditions (22)–(23) (supp p. 13), for
Theorem S: on models of |t| + r̄_n columns, n·l_n < ch′₁(X_ζᵀX_ζ) ≤ ch₁(X_ζᵀX_ζ) < n·l′_n with r̄_n log P_n ≺ n·l_n.
Theorem S assumes only (12), 1 ≤ r_n ≤ r̄_n < P_n, so r̄_n may be bounded; Theorem 3 inherits r_n ≻ 1 from Theorem 2
(p. 953). *(i) Where their sets are no larger than ours* (|t| + r̄_n ≤ 2(A + 1)s₀ + 2 against Theorem 1 (A4);
r̄_n + 1 ≤ 5(A + 1)(s₀ + 1) log n against Theorem 2 (A3)): our fixed floor implies their condition (for (22)–(23), with
standardised columns, take l_n = φ₀²/2 and l′_n = |ζ|; for Condition 3, with Gaussian predictors), and we also ask a
floor on sets where they ask nothing. *(ii) Where their sets are larger than ours* (r̄_n ≻ log n): they constrain sets
on which we ask nothing, at a vanishing level, and we ask a fixed level on our smaller sets; neither condition implies
the other. *Upper half of (22):* no restriction for standardised columns (l′_n = |t| + r̄_n always works, and
n·l_n ≻ l′_n then follows from (23)); it binds only for raw columns whose scale grows with n. In every regime both
conditions follow from λ_min(Σ_n) ≥ c. **Does it matter for our designs? No:** all 13 have λ_min(Σ) ≥ 0.1.
**Evidence.** SL Condition 3 (p. 955): E exp{−(x_k + Σ_{i ≤ r̄_n} b_i x_{j_i})²} ≤ 1 − δ_n with δ_n ≻ ε_n². Their own
sufficient forms: for standard normal predictors var(x_k + Σ b_i x_{j_i}) ≻ ε_n², implied by ch′₁{var(x)} ≻ ε_n²
(pp. 955–956); for bounded predictors ch′₁{var(x̃)} ≻ r̄_n ε_n² (p. 955). So SL ask a **vanishing** eigenvalue level on
sets of r̄_n + 1 predictors, r̄_n → ∞ (Theorem 2 needs r_n ≻ 1 and (12) r_n ≤ r̄_n, pp. 952–953), anchored at each true
predictor, and conclude **sure screening** only (p. 956: "the specificity is not controlled"). We ask a **fixed** level
φ² on sets of O(log n) predictors (Thm 2; the master needs it fixed only on sets of (2A + 2)s₀ + 2 predictors) and
conclude exact selection with a rate. (Their Theorem S: §S.) Both are implied by λ_min(Σ_n) ≥ c, the form a reader will check first. **No upper
eigenvalue bound is used**, so pervasive factors are allowed. Thm 1′ replaces the floor off S₀ by a residual-signal
margin c σ*² log n; per observation this is c σ*² log n / n, below SL's level ε_n² ≻ r̄_n log P_n / n (their (10)) [audit
reading; sample level against population level].
**Holds / fails.** Holds: every Σ with λ_min ≥ c (W2-APP family map, `W2-APP/lemmas/L4_families.md:159-168`: "POST holds"
for iid, bounded spectrum, AR(1), Toeplitz, banded, blocks, fixed equicorrelation, factor with a floor). Fails: exact
or asymptotic duplicates of a true predictor; correlations → 1 with a truth.
**Designs.** All inside. λ_min(Σ): S1 1; S2 1/3; S3 0.3; S4 0.15; S5 0.3; S6 0.1; cs(ρ) 1 − ρ; fac2 0.40; s5 0.3; IND 1;
AR(0.6) 0.25; BLK 0.5; FAC 0.7 — checked (AUDITCALC_check_opus.md §3). **Strong factors (S5, all of P6) are inside the
posterior theorems.** Track C confirms: sample floors on sets of 16 and at the O(log n) size cutoff are positive and
rise with n in all 19 designs along p = n (P1–P3).
**Corollary (Thm 2, primitive).** Rows i.i.d. N_p(m, Σ), λ_min(Corr) ≥ φ² > 0 (largest eigenvalue free), s₀ and the
nonzero β fixed, p ≤ n^A: 1 − π(S₀ | y) = O_P(√(log n/n)) and HPM = MPM = S₀ w.p. → 1. This is Thm 2 with its "for
instance"; no new proof.

## B6. No near-exact collinearity among O(log n) columns
(Thm 1 (A5): λ_min(X_SᵀX_S) ≥ g₀; Thm 9 (A4): λ_min(Corr(x_T)) ≥ c_ψ/n.)
**Comparison (depends on the comparator and on r̄_n).** *(a) Their Theorems 1–2 (Hellinger)* have no eigenvalue condition
on the design — (11) and (14), p. 952, are on the prior covariance V_ξ — so Thm 9 (A4) is a condition they do not have,
in every regime. *(b) Condition 3 (their Theorem 3):* since e^{−u} ≥ 1 − u it gives E(x_t + Σ b_i x_{j_i})² ≥ δ_n ≻ ε_n²
on r̄_n + 1 columns that contain a true predictor (p. 955), a level above our g₀/n; on sets of null columns only they
ask nothing. *(c) Condition (22) (Theorem S)* asks the level l_n ≻ r̄_n log P_n / n on models of |t| + r̄_n columns,
null-only ones included (supp p. 13). In (b) and (c): if their sets are at least as large as ours
(r̄_n ≥ 3(A + 1)(s₀ + 1) log n), theirs gives ours on the sets they cover and ours asks less there; if their sets are
smaller (r̄_n ≺ log n, allowed by (12) and by Corollary S₁ with k₁ < 1), ours constrains sets that theirs does not, and
neither implies the other (log n null columns, one of them the normalised sum of the others, satisfy (22) with a
constant l_n and violate (A5)). Thm 1 (A5) is on the sample Gram matrix, Thm 9 (A4) on the population correlation
matrix. **Does it matter for our designs? No.**
**Evidence.** SL's eigenvalue conditions (11) and (14) (p. 952) are on the prior covariance V_ξ. With their own "ridge"
choice V_ξ⁻¹ = E(x_ξᵀx_ξ) + c_n I, c_n ∝ 1/n (p. 953), B̃_n ≤ c_n⁻¹ ∝ n and no design condition is left; the price
is the rate, ε_n² ≻ r̄_n log P_n / n with r̄_n → ∞ (their (10)). Our floor c_ψ/n (correlation scale; g₀ unnormalised) is
of the same order as that ridge, on O(log n) sets only, and buys the radius √(M log n/n) with no diverging factor.
Without it Thm 9 still holds with radius √(M log n · log(p ∨ n)/n) (display (iii)): the assumption costs one log factor.
**Holds / fails.** Holds for any Σ with λ_min ≥ c on O(log n) sets and for correlations up to 1 − c_ψ/n. Fails for
duplicated columns (null duplicates included) and one-hot or compositional coding with exact dependence.
**Designs.** All inside. Track C: the Occam term is bounded and decreasing in every design (P8). **Typical user:** inside
after removing exact duplicates and exact linear dependences.
**Corollary (Thm 9, primitive).** Gaussian rows with any correlation matrix whose q_n × q_n principal blocks have
λ_min ≥ c_ψ/n, at most s nonzero β_j with |β_j| sd(x_j) ≤ b̄σ, p ≤ n^A: display (i). This is the Example of Thm 9.

## B7. Law of the rows: i.i.d. Gaussian (Thm 2, 6, 10); sub-Gaussian on sparse directions (Thm 9 (A3))
**Comparison (depends on centring and on which of their theorems).** *Counterparts:* |x_i| ≤ 1 (their Theorem 1, p. 952);
Condition 1 (their Theorem 2, p. 953), a raw exponential-moment bound with constants fixed in n, which they verify for
bounded predictors and for a Gaussian process "with zero mean and var(x_i) = 1"; Condition 2 (second moments, p. 954)
for their limit form (16). *(i) On centred, unit-variance predictors* Gaussian rows and Thm 9 (A3) each imply
Condition 1 (for every r; checked, AUDITCALC_check_opus.md §4); the converse fails (bounded, strongly dependent
predictors). *(ii) On raw predictors* neither implies the other: we allow any means m_n (Gaussian rows with mean n
satisfy Theorems 2 and 6 and violate Condition 1); bounded non-Gaussian predictors satisfy Condition 1 and not our
row law. *(iii) Against |x_i| ≤ 1* neither implies the other: Gaussian predictors are unbounded; a bounded binary
predictor with P(x = 1) → 0 violates (A3) for every fixed L. *Roles differ:* Condition 1 enters their proof in the
prior-mass condition in the divergence d₁, for perturbations of order ε_n/r_n on one model that contains the true
predictors (supp p. 4); ours enters the passage from sample to population covariances. Theorem 1 (fixed design) needs
no row law. **Does it matter for our designs? No:** every generator draws centred Gaussian rows with unit variances,
which satisfy Condition 1 itself.
**Evidence.** SL Condition 1 (p. 953): E exp{(Σ_{i ≤ r} a_i x_{j_i}/r)²} ≤ exp(M) for r ≤ r̄_n, |a_i| ≤ δ; SL verify it
for bounded predictors and for Gaussian ones with unit variance (p. 953). Our (A3) is E exp(λuᵀz) ≤ exp(L²λ²Var(uᵀz)/2)
for q_n-sparse u. (A3) ⇒ Condition 1 for standardised predictors, **for every r** (no link between r̄_n and q_n is
needed), with δ = √(3/8)/L and M = log 2: (Σ a_i z_{j_i}/r)² ≤ r⁻¹Σ a_i² z_{j_i}², and each single predictor has
E exp(a_i² z²) ≤ (1 − 2L²δ²)^{−1/2} = 2 — checked (AUDITCALC_check_opus.md §4). Only (A3) for single predictors is used.
The converse fails (bounded, strongly dependent predictors). Thm 1 (fixed design) needs no row law at all.
**Holds / fails.** (A3): Gaussian rows (L = 1), independent sub-Gaussian coordinates. Fails for heavy tails, and for
bounded predictors whose sparse combinations are not sub-Gaussian at their own scale. Gaussian rows are used "only for
the entrywise concentration step" (Thm 2, why-line); the sub-Gaussian extension is expected, not claimed.
**Designs.** All inside (Gaussian generators). **Typical user:** genotype or other bounded data are outside Thm 2, 6, 10
as stated and inside SL's Condition 1; they are covered by the fixed-design Thm 1 when its sample conditions hold.
**Corollary.** Candidate, not proved: Thm 2 for rows with independent sub-Gaussian coordinates after a linear map.

## B8. Visibility (Thm 6 (A3); Thm 10 (A4)): |Cov(W_j, Wᵀθ* | W_U)| ≥ a for every true j and every |U| ≤ 15
**Comparison: ours implies their Condition 5, in every regime** (p. 958: |cov(x_t, y)| > 0 for every true predictor; it
is our case U = ∅ without the margin). We ask more: a fixed margin, and up to 15 conditioning columns. Same role: the
cheap first stage must see every true predictor.
**Evidence.** U = ∅ in (A3) gives |Cov(W_j, y)| ≥ a [one line]. SL need Condition 5 so that their iterative subset
screening "ensures that all true predictors that are contained in X_s will be selected" (p. 958). Ours conditions on up
to 15 other columns because the method's blocks have at most 16 columns.
**Holds / fails.** Holds when no truth is cancelled by ≤ 15 others: bounded blocks with one truth each, AR and banded with the truths spread apart (study gaps 31–37, ≈ p/5; adjacent mixed-sign AR truths can cancel: ρ = 0.5, θ = (1, −2) lies on B, Lemma VIS),
(W2-APP family map, "PTV automatic if ≤ 1 truth/block", `L4_families.md:165`). Fails for masked truths (zero marginal or
partial covariance with y); those designs are treated by a separate theorem (W1-PXN), not by Thm 6. Track C gives two
concrete failures at the population level: a pervasive factor with **mixed-sign** truths (its D14, D15: a set of ≤ 15
columns cancels the truth's covariance with the signal) and the **clustered** placement of the riboflavin-like design (D18; effectively on the bad set B, not certifiably on it: a 15-column U gives |Cov| ≤ 6.9 × 10⁻⁹, exact recomputation). **Update (track V, Lemma VIS v1.5, W3-AUDIT-V:VIS, 11-17):** D18's **spread** placement is inside with a certified margin a ≥ 0.1·min_k|θ_k| (up to 5 × 10⁻¹⁴) for p ≥ 16352 (truths in four different tiles, so every visibility direction is a coordinate vector; `Theory_work/Wave3/W3-AUDIT/track_V/reviews/D18/D18_VERDICT.md`), and D18/D19, being built from one fixed matrix, have finitely many local patterns (VIS-d)(i).
**Designs** — checked (AUDITCALC_check_opus.md §5). Inside: S1–S4, S6, IND, AR, BLK (block or Markov structure: the
covariance is θ_j Var(W_j | W_U) plus geometrically small terms, ≥ |θ_j| λ_min/2). cs(ρ) of P6: inside (aligned signs,
positive partial covariances). **fac2 and s5 of P6: inside** (moved from "unclear" in v1.2). P6's truths have aligned
signs (`W3-P6/DESIGN.md:16-17`), so it suffices that every conditional covariance between columns outside U is ≥ 0;
then Cov(W_j, Wᵀθ* | W_U) ≥ θ_j Var(W_j | W_U) ≥ θ_j λ_min(Σ). *s5:* Σ⁻¹ = A⁻¹ − κJ with A = 0.3I + 0.4H, κ > 0, has all
off-diagonal entries negative (an M-matrix), and so has every principal submatrix, hence all conditional covariances
are ≥ 0; margin ≥ 0.3·θ_j. *fac2:* given any U with m₁ even and m₂ odd columns, the conditional covariance of two columns
is 0.10/det (opposite parity) or (0.6 + 0.875·m_opp)/det (same parity), det > 0; margin ≥ 0.40·θ_j. (The reviewer's
argument, API triage T8; I re-derived both computations; they agree with the checker's search values 0.364 and 0.431.)
**Unclear, not upgraded:** S5 of the study (mixed signs; near-cancellation, worst ratio 0.0056) and FAC of 1M (0.16 in
the checker's search, below the aligned-sign bound 0.7, so its signs are mixed). Track C agrees on all counts: visibility inside and rising with n for IND, AR(0.5), fixed
blocks and S6; factor designs inside with aligned truths and outside with mixed-sign truths (its D14, D15); small for
S5 (population 0.06). **Typical user (updated by Lemma VIS):** the riboflavin-like design is inside for the spread placement (p ≥ 16352, a ≥ 0.1·min_k|θ_k| up to 5 × 10⁻¹⁴) and outside in practice for the clustered placement (four highly correlated truths in one tile; no usable margin certifiable);
the FRED-QD-like tiles are inside whenever ϑ is off one fixed closed null set B (generic position; not certified for track C's placements, whose population margins 0.08–0.30 are consistent).
**Corollary (primitive).** Block-diagonal Σ with λ_min ≥ c and at most one truth per block ⇒ (A3) with a = c·min|θ*_j|.

## B9. Polynomial leakage set with locality (Thm 6 (A4)): Q ⊇ S₀, |Q| ≤ n^b, b < ½
**Comparison.** Song–Liang have no hypothesis of this kind. The nearest text is their informal remark (a), p. 958, which
is not a condition of any of their theorems. Ours is a hypothesis with a rate (|Q| ≤ n^b). No ordering is claimed.
**Evidence.** SL p. 958, remark (a): "all the predictors that are correlated with X_t will be selected … if all the
predictors are linearly correlated, it is futile to apply this iterative procedure"; and "if there are p_n predictors
correlated with the true predictors X_t, p_n ≺ P_n, then there are at most cp_n predictors to be selected". Ours states
it as a hypothesis with a rate: nulls whose conditional covariance with a truth is above o(√(log n/n)) must lie in a set
of at most n^b columns; correlations below that level do not count. SL's statements on their sampler's output are limits in the number of iterations at fixed data (supp pp. 9–10,
12–13, 16–17; §S), with no design condition of this kind
(§3.2, p. 959, cites the SAMC algorithm), so there is no formal counterpart to compare levels with.
**Holds / fails.** Holds: metric-local correlation and bounded blocks (`W3-RM2:Cont-R@1.0.4`, "PROVED-CHECKED, conditional
on W2-APP:POST, SOP:TH05.0; …"); one truth with n^b weak proxies and one equicorrelated group of size n^b, b < 3/10
(`W3-RM2:Ex-Proxy`, `Ex-Equi`, "PROVED-CHECKED; council R1, …"). **Fails for pervasive factors when p ≫ √n:** already at
U = ∅ every null has a fixed covariance with every truth (cs(ρ): ρ; fac2: 0.10 or 0.60; s5 and S5: 0.3 or 0.7), so
Q = [p] and |Q| ≤ n^b forces p ≤ n^b — checked (AUDITCALC_check_opus.md §6). This matches the record: `W2-FAC-X:Thm-FAC-CS-iid` needs limsup log p/log n < ½, and `W2-FAC-PK:Thm-NEG`
("PROVED-CHECKED") shows the start-mode search alone fails for K < p ≤ n − 1.
**Designs.** Inside: S1 (Q = S₀); S2, AR (Q = a C log n neighbourhood of S₀); S3, S4, S6, BLK (Q = the truths' blocks,
|Q| = 5s₀ or 20s₀). **Outside: S5, all of P6 (cs, fac2, s5), FAC.** Track C confirms each entry it tests: leak set bounded
for IND, AR(0.5), AR(0.8), fixed blocks and S6; the whole design for S5 and for factors with a fixed or slowly decaying
common correlation. It adds: the leak set grows slowly for AR(0.95) (≈ n^0.1 at p = 10n; corrected by the NOTS cells, C-NOTS) and like n^0.4 for
Toeplitz decay α = 1 (inside only for b close to ½), and a factor whose common correlation decays like p^{-1/2} comes inside from n = 800.
**Corollary (Thm 6, primitive; candidate, short proof expected).** Rows i.i.d. N(m, Σ), Σ block-diagonal with blocks of at
most g columns (g fixed), λ_min(Σ) ≥ c, at most one truth per block, fixed nonzero θ* on S₀, p ≤ n^A: every admissible
run that produces output reports S₀, on one data event of probability → 1. Route: Q = the truths' blocks, H_l = Q ∪
block(l), N_l = block(l) ∩ Q, L_n = 0, ϖ_n = r_n = 0; then B8's corollary and Thm 6.

## B10. Floor on Q ∪ {l} and local regressions inside Q (Thm 6 (A5) second part, (A6))
**Comparison.** *Floor on Q ∪ {l}:* an eigenvalue floor of the kind of Condition 3 (p. 955) and (22) (supp p. 13), at a
fixed level, on the family Q ∪ {l} (up to n^b + 1 columns, for every column l). As in B5: where their sets are subsets
of ours it implies their condition; otherwise the two constrain different sets. Their stage 2 applies their theory to
the merged set (p. 959, step (c)), their analogue of Q. *Local regressions (A6):* Song–Liang have no condition of this
kind (it serves the search, which they do not analyse). Both of ours follow from B5's global floor plus a locality
property of Σ. **Does it matter for our designs? No.**
**Evidence.** (A6) is a sufficient form of the lattice-width condition (W), and (W) is forced by this proof route (Thm 6
why-line: if the width gap diverges the other way, the no-addition event fails w.p. → 1). The fixed-design master needs
nothing of the kind when |Q ∖ S₀| ≤ (1 − δ) log n (`W3-RM2/STATEMENT.md:148`).
**Holds / fails.** Holds with N_l = the block-mates or the nearest Q-neighbours of l for block, banded and AR
structures; polynomial decay with exponent α > 2 (`W3-RM2:Ex-PolyR`: "PROVED; line-checked LC2-C; Astra seat ACCEPT; not
examined by the Opus seat …"). Not verified for an equicorrelated group of size n^b with b ≥ 3/10 (`W3-RM2/STATEMENT.md:268`).
**Designs.** As B9: inside S1–S4, S6, IND, AR, BLK; not applicable where B9 fails. Track C: the local-regression tail
and the width proxy are inside for IND, AR(0.5), fixed blocks and S6, and unclear but improving with n for AR(0.8)
with spread truths. **Corollary.** Included in B9's.

## B11. No leakage (Thm 10 (A5) = Thm 5 (A5)): every null is conditionally uncorrelated with every truth, up to C n^{-1/2}
**Comparison: Song–Liang have no condition of this kind** (uniformly: none of their theorems concerns a start law).
Its reach is narrow: it is the one assumption of the core theorems that most of our own designs violate.
**Evidence (counterexample to membership).** With U = ∅, (A5) asks |Cov(W_l, W_j)| ≤ C n^{-1/2} for every null l and truth
j. In AR(1) with ρ = 0.5 the neighbour of a truth has covariance 0.5; in a block design every block-mate of a truth has
covariance ≥ 0.4. For such designs the proved start result is concentration on the lattice of Q, not on S₀
(`W3-START2-R:EX`, example G-2: "1 − π₀(𝓛(Q)) = O_P(√(log n/n))"), and Thm 10's route needs π₀(S₀) → 1 (P-START). The
alternative route (`W3-SAMP:TR`) needs a global-overlap premise that the record says is not derived from conditions on
(X, θ*) (`W3-SAMP/STATEMENT.md:183`).
**Holds / fails.** Holds: Σ = I (`W3-START2-R:EX` G-1); truths uncorrelated with all nulls and nulls locally correlated
among themselves. Fails: any null correlated with a truth at a fixed level.
**Designs.** **Inside: S1, IND only. Outside: S2–S6, all of P6, AR (the primary 1M design), BLK, FAC** — the covariances
are read off Σ (0.5, 0.6, ≥ 0.4), checked (AUDITCALC_check_opus.md, summary table). Track C: the leak set equals S₀ for
IND only.
**What is still true there.** Thm 6 (reported model = S₀) covers S2–S4, S6, AR, BLK; row 3.5 (unbiased evidence) needs
no design condition. Not covered there: consistency of the printed PIPs, MPM and Ẑ.
**Corollary (Thm 10, primitive).** Σ = diag(Σ_{S₀}, Σ_N) with λ_min ≥ c and Σ_N block-diagonal with bounded blocks.
**Candidate repair (track D #1, scoped in `TRACK_D.md` §0, not proved):** ask no leakage only given the truths of the
column's own group. It would bring S3, S4, S6 inside. It would not bring AR or BLK (groups of 20 exceed the block cap
16): there, **as n → ∞**, the start mass on S₀ falls below every power of n (`W3-START:NEC-b`, "PROVED-CHECKED") —
checked (AUDITCALC_check_opus.md §1). At the 1M plan's sizes (n ≤ 400, p = 10⁶) that result's threshold is not met, so
nothing recorded bounds the start mass there in either direction.

## B12. Witness designs of Thm 3(b): orthogonal, or i.i.d. N(0, 1), null columns
**Comparison: not an assumption to defend** (a lower bound needs one design; Song–Liang state no lower bound). Part (a) has no
assumption. **Designs.** S1 and IND are of type (N-gauss) only if the truths are independent of the nulls (they are).

---

## Summary table (assumption × Song–Liang counterpart × comparison by regime × our designs)

The design columns are unchanged from v1.3. "supp" = their supplement.

| # | Assumption (theorems) | Song–Liang counterpart (page / eq) | Comparison, by regime | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
|---|---|---|---|---|---|---|
| B1 | Gaussian linear model (all) | model (1), density (2), p. 950 | the same in every regime | in / in / in / in | in | in / in / in / in |
| B2 | p ≤ n^A (all) | Hellinger: P_n < exp(Cn^α), Cor 1, p. 954. Selection: log(√n/r_n) ≻ √(log P_n), supp p. 13; Cor S₁, supp p. 16. Lower: P_n ≻ n^θ, p. 950 | above, ours admits fewer dimensions (far fewer than Cor 1, slightly fewer than Theorem S); below, ours admits bounded p and theirs does not | in | in | in (A ≈ 2.6) |
| B3 | s₀ fixed (all) | strict sparsity (4), p. 950; (3), p. 950, in their Thm 1 | the same as (4) (their Thms 2, 3, S); their Thm 1 also admits growing supports under (3), ours does not | in (as a sequence) | in | in |
| B4 | signal bounded; fixed nonzero or beta-min (1, 2, 6, 10; 9 above only) | no lower bound stated; (3), (8) above in Thm 1, pp. 950, 952; proof rates supp pp. 6, 15 | if their β* is one fixed sequence (natural reading, p. 950): our Thms 2, 6, 10 ask the same, Thms 1 and 9 admit more; if β* may vary with n: their statements ask nothing, their proof steps need rates, and our fixed signals ask more than those steps | in | in | in |
| B5 | eigenvalue floor on small sets (1, 2, 6, 10, 9B) | Condition 3, p. 955 (r̄_n + 1 columns with a true predictor, level ≻ ε_n²); (22)–(23), supp p. 13 (\|t\| + r̄_n columns, level l_n) | where their sets are no larger than ours (bounded r̄_n against Thm 1; r̄_n ≲ log n against Thm 2): ours implies theirs and asks more; where theirs are larger (r̄_n ≻ log n): different sets, neither implies the other; upper half of (22) is free for standardised columns | in | **in** | in |
| B6 | no near-exact collinearity on O(log n) sets (1, 9) | none in Thms 1–2 ((11), (14), p. 952, are on V_ξ); Condition 3, p. 955; (22), supp p. 13 | against Thms 1–2: a condition they do not have. Against Condition 3 and (22): if r̄_n ≥ 3(A + 1)(s₀ + 1) log n theirs gives ours on the sets they cover; if r̄_n ≺ log n ours constrains sets theirs does not | in | in | in |
| B7 | Gaussian rows (2, 6, 10); sub-Gaussian sparse directions (9) | \|x_i\| ≤ 1, Thm 1, p. 952; Condition 1, p. 953; Condition 2, p. 954 | on centred unit-variance predictors ours implies Condition 1; on raw predictors, and against \|x_i\| ≤ 1, neither implies the other | in | in | in |
| B8 | visibility, ≤ 15 conditioning columns (6, 10) | Condition 5, p. 958 | ours implies theirs in every regime (theirs is our case U = ∅ without the margin) | in / in / in / unclear | **in** (cs, fac2, s5: aligned signs) | in / in / in / unclear |
| B9 | leakage set \|Q\| ≤ n^b with locality (6) | no hypothesis; informal remark (a), p. 958 | no ordering claimed | in / in / in / **out** | **out** | in / in / in / **out** |
| B10 | floor on Q ∪ {l}, local regressions in Q (6) | floor: Condition 3, p. 955; (22), supp p. 13. Local regressions: none | floor: as B5, on a different family of sets; local regressions: they have no such condition | in / in / in / n.a. | n.a. | in / in / in / n.a. |
| B11 | no leakage (10) | none | they have no such condition (no start law in their theorems) | in / **out** / **out** / **out** | **out** | in / **out** / **out** / **out** |
| B12 | witness designs (3(b)) | none (no lower bound stated) | — | — | — | — |

**Reading.** The two posterior theorems (core 1, core 2) hold on every one of our designs, strong factors included. The
assumptions are of the same kinds as Song–Liang's; where the papers differ, the direction depends on the regime, as the
table shows, and nothing in the differences excludes a design of ours. The reported-model theorem (core 3) adds two
method-specific conditions (B8, B9) whose Song–Liang counterparts are Condition 5 and remark (a); it excludes pervasive
factors at p ≫ √n, which is where P6 sits. The printed-estimates theorem (core 4) rests on B11, which only the
independent designs satisfy.

---

## T. API triage 1 (blind second opinion `Theory_work/Wave3/API_AUDIT/audit1_results/` on main 0eb08a4b; v1.2; kept as a record — its one-word labels are superseded by v1.4)

Each finding was read against the paper (journal pages) and our statements. Accepted findings changed labels only; no
inside/outside verdict for cores 1–2 was challenged (all NO-FINDING), and core 2 had no finding.

| # | Finding (samples) | Decision | Reason and citation | Change made |
|---|---|---|---|---|
| T1 | core1 B5.SL (1/2): "smaller sets" fails for Thm 2's floor when r̄_n ≺ log n | **ACCEPT** | SL need only r_n ≻ 1 (Thm 2, p. 953) and r_n ≤ r̄_n ((12), p. 952); Cor 1 (p. 954) admits r̄_n ≺ log^k n. Condition 3's sets have r̄_n + 1 columns (p. 955) | B5 verdict: stronger in level, set size not ordered; summary row; AUDIT rows |
| T2 | core1 B6.SL (2/2): Condition 3 is a counterpart of (A5) | **ACCEPT** | Condition 3 (p. 955) with e^{−u} ≥ 1 − u gives E(x_t + Σ b_i x_{j_i})² ≥ δ_n ≻ ε_n², a collinearity bound on r̄_n + 1 columns containing a true predictor; nothing for null-only sets (p. 956: specificity not controlled) | B6 verdict split by comparator (Thm 1–2 against Thm 3); "population twin" corrected; AUDIT row |
| T3 | core1 B7.SL and core3 B7.SL (2/2 each): "implies Condition 1" fails with unbounded means | **ACCEPT** | Theorems 2 and 6 take rows N_p(m_n, Σ_n) with m_n free; Condition 1 (p. 953) is a raw-moment bound; SL's Gaussian case is "zero mean and var(x_i) = 1" (p. 953). The implication holds for centred, unit-variance predictors (checker §4) | B7 verdict: stronger on centred predictors, not ordered on raw ones; summary row; AUDIT rows |
| T4 | core3 A2.SL (2/2): (A2) is not "same as (4)" | **ACCEPT** | (4), p. 950, bounds the number of nonzero coefficients only; (A2) also fixes their size | AUDIT core 3 and core 4 rows split (sparsity: same; signal: stronger as stated); B4 verdict made plain |
| T5 | core3 B10-FL.SL (1/2): the floor on Q ∪ {l} has a counterpart | **ACCEPT** | it is an eigenvalue floor of the same kind as Condition 3 and its sufficient forms (pp. 955–956); SL apply their theory to the merged set (p. 959, step (c)) | B10 verdict split (floor: same kind; local regressions: none); summary row; AUDIT row |
| T6 | core3 B2.SL (unclear): Cor 1 not among the reviewer's excerpts | **REBUT** | the passage reads as cited: "Suppose that P_n < exp(Cn^α) for some α ∈ (0, 1)" (Cor 1, p. 954) | none |
| T7 | core3 B5.SL (unclear): set sizes; "stronger conclusion" against Theorem S | **ACCEPT in part** | set sizes: as T1. Theorem S was not inspected at v1.2; it is compared in §S (v1.3) | as T1; one sentence in B5 limiting the comparison to Theorem 3 |
| T8 | core3 B8.IO (2/2, in our favour): P6 fac2 and s5 are inside visibility | **ACCEPT** | aligned signs (`W3-P6/DESIGN.md:16-17`) + nonnegative conditional covariances: s5 by the M-matrix form of Σ⁻¹, fac2 by the explicit two-factor posterior; both re-derived here | B8: fac2, s5 moved to inside; summary row; reconciled with track C (aligned inside, mixed-sign outside) |

Counts, by finding (9: core 1 B5, B6, B7; core 3 A2, B7, B10-FL, B2, B5, B8): 8 accepted (one in part), 1 rebutted. Label changes: B4, B5, B6, B7, B10 (and the AUDIT rows that quote them);
one design entry (P6 fac2, s5: unclear → inside).

---

## S. Song–Liang's Theorem S (MAP consistency) against core 1 and core 3 (v1.4)

**Theorem S, hypotheses and conclusion as printed (supp p. 13).** "Let D_n be a dataset generated from model (1) of the
main text with a sparse true model t. Assume condition (12) of the main text and the following eigen-structure
conditions hold: For any model ζ with size |ζ| = min{|t| + r̄_n, n}, there exist a non-increasing sequence {l_n} and a
non-decreasing sequence {l′_n} such that
  n·l_n < ch′₁(X_ζᵀX_ζ) ≤ ch₁(X_ζᵀX_ζ) < n·l′_n, (22)   r̄_n log P_n ≺ n·l_n. (23)
If, further, one of the following two condition holds: 1. n·l_n ≻ log l′_n, log(√(n·l_n)/r_n) ≻ √(log P_n), and we set
V_ξ⁻¹ = I for any ξ; or 2. n·l_n ≻ l′_n, log(√n/r_n) ≻ √(log P_n), and we set V_ξ⁻¹ = X_ξᵀX_ξ/n for any ξ, then, for any
model k, the posterior probability (7) of the main text satisfies: max_{k≠t} π(k | D_n)/π(t | D_n) →_p 0. (24)"
Relation signs checked on the page image. Remarks (supp pp. 15–16): (22) "is hardly satisfied"; it may be replaced by
the probabilistic (26), Pr{n·l_n > ch′₁(X_ζᵀX_ζ) or ch₁(X_ζᵀX_ζ) > n·l′_n} < e^{−nC} for |ζ| = r̄_n + |t|, which holds for a
Gaussian process whose Var(x) has eigenvalues between l_n and l′_n. Corollary S₁ (supp p. 16): P_n < n^{κ log n},
κ ∈ (0, ¼), r̄_n ≺ log^{k₁}(n) or r̄_n ≺ n^q with q ≤ ½ − √κ, l′_n = l_n⁻¹ = √n/log^{k₂}(n). The cap r̄_n is free subject
to (12), 1 ≤ r_n ≤ r̄_n < P_n: it may be bounded.

**Against core 1** (Theorem 1 is the nearest: fixed design, sample conditions; Theorem 2 corresponds to (26)).

| Item | Theorem S | Ours | Comparison, by regime |
|---|---|---|---|
| Model, sparsity | model (1), "sparse true model t" | Gaussian linear model, s₀ fixed | the same in every regime |
| Prior | (12); V_ξ⁻¹ = I or X_ξᵀX_ξ/n; r_n tied to n and P_n by condition 1 or 2 | the coded prior, no tuning | different posteriors: theirs is (7) under prior (6), ours the coded one; ours has no condition on hyperparameters |
| Dimension | log(√n/r_n) ≻ √(log P_n); Cor S₁: P_n < n^{κ log n}; P_n → ∞ | p ≤ n^A, bounded p allowed | above, ours admits slightly fewer dimensions; below, ours admits bounded p |
| Lower eigenvalue bound | (22)–(23): above n·l_n, r̄_n log P_n ≺ n·l_n, on models of \|t\| + r̄_n columns | fixed φ₀² on sets of ≤ 2(A + 1)s₀ + 2 columns; g₀ (unnormalised) on O(log n) columns | if \|t\| + r̄_n ≤ 2(A + 1)s₀ + 2: ours implies (22)–(23) (standardised columns, l_n = φ₀²/2) and asks a floor on larger sets where they ask nothing; if \|t\| + r̄_n exceeds our O(log n) sets: they constrain sets we do not, at a vanishing level; neither implies the other |
| Upper eigenvalue bound | (22): below n·l′_n; n·l_n ≻ l′_n (condition 2) | none | no difference for standardised columns (l′_n = \|t\| + r̄_n works, and the l′ clauses follow from (23)); it binds only for raw columns whose scale grows with n |
| Signal size | none stated; the proof step needs n·l_n·c² ≻ r̄_n log P_n, c = min_{i∈t}\|β*_i\| (supp p. 15) | Thm 1: θ*²_min φ₀² n ≥ c₀σ*² log n; Thms 2, 6: fixed signals | against the statement: ours asks a condition theirs does not state; against the proof step: the same form, ours at a fixed multiple of log n; if their β* is a fixed sequence, the same as our fixed signals |
| Conclusion | (24): the mode of their posterior (7) is t, in probability; no rate; no claim that π(t \| D_n) → 1 | 1 − π(S₀ \| y) = O_P(√(log n/n)) for the coded posterior; HPM = MPM = S₀; PIPs | different posteriors, so neither statement implies the other; within one posterior, mass on the truth with a rate is a stronger form of statement than (24) |

**Against core 3** (the reported model). Song–Liang's statements about what their sampler reports hold for every fixed
data set, with no design condition, as the number of iterations N → ∞: the weighted averages converge almost surely to
posterior expectations (supp pp. 9–10, (13)–(15)); "q̂_j → q_j almost surely as N → ∞" (supp pp. 12–13, after (21)); and
the sampled highest-probability model is a consistent estimate of the MAP model (supp p. 16, with Lemma S₂(ii),
pp. 16–17). Ours (Theorem 6) says that the coded run, at its actual budget, reports S₀ on a data event of probability
→ 1 under design conditions; it has no statement as iterations grow and none on convergence of sampler estimates to
posterior quantities (Theorem 10 has, on S1 and IND only). **Neither implies the other:** theirs needs an infinite
budget and covers every data set; ours holds at a finite budget, jointly with n, on designs that satisfy (A3)–(A6).
So they do have statements about the sampler's output, and the earlier sentence "they prove nothing about its selection
output" is replaced by this paragraph. Theorem S adds no condition of the visibility or leakage kind (B8, B9).

**Conclusions, per theorem (only what survived both blind audits).**
- *Against their Theorem 3 (p. 956).* Theirs: each true predictor has posterior inclusion probability ≥ 1 − exp(−c₁nε_n²)
  outside a data event of probability < exp(−c₁nε_n²); sensitivity only ("the specificity is not controlled"). Ours:
  max_j|PIP_j − 1{j ∈ S₀}| ≤ 1 − π(S₀ | y) = O_P(√(log n/n)) and HPM = MPM = S₀. Ours adds specificity and exact
  selection; theirs has the smaller error for sensitivity. Neither implies the other.
- *Against their Theorems 1–2, (15) (pp. 952–953).* The same distance. Ours holds at radius √(M log n/n) for every level
  M₀ ≤ M ≤ √n/log n with exceptional mass and probability n^{−cM} = exp(−c·nε²) at ε² = M log n/n: the same exponential
  form as (15) inside that window. Their radius must satisfy nε_n² ≻ r̄_n log P_n ((10), with r_n ≻ 1 in Theorem 2), so
  a constant multiple of √(log n/n) is outside their statement at polynomial p; radii with nε² > √n, and exponential p,
  are outside ours.
- *Against Theorem S, (24).* See the last row of the table.

## T2. Supplement: what the proofs add (v1.4; replaces the v1.3 label table)

| Item | Statement in v1.4 | Source (page / equation) |
|---|---|---|
| B2 range of p | the selection theorem itself needs log P_n ≺ (log n)²/4 | condition 2, supp p. 13; Cor S₁, supp p. 16 |
| B4 signal size | their proof steps need rates, not constants: β*_t²δ_n ≥ 20σ*²ε_n² (Thm 3) and n·l_n·c² ≻ r̄_n log P_n (Theorem S); the wording of the proofs treats the coefficients as constants | supp p. 6 (display d² ≥ min{δ_n, β*_t²δ_n/(20σ*²), 1 − √0.8}); supp p. 15 |
| B5, B6 eigenvalues | (22)–(23) concern models of \|t\| + r̄_n columns with r̄_n free under (12); the comparison with ours depends on r̄_n (dossiers B5, B6) | supp p. 13 |
| B7 row law | Condition 1 is used once, for the prior mass in d₁ | supp p. 4 |
| Core 2 distance | the same Hellinger distance; d₀ (Kullback–Leibler) and d_t(f, f*) = t⁻¹(∫f*(f*/f)^t − 1) appear only in the prior-mass hypotheses of their Lemma 1.1 | supp p. 1 |
| Sampler output | they state limits as N → ∞ at fixed data; neither their statements nor ours imply the other | supp pp. 9–10, 12–13, 16–17 |
| Misspecification (not core) | not revisited; their Lemma 1.2 is de Blasi–Walker's Corollary 1 | supp p. 6 |

## T3. API triage 2 (`Theory_work/Wave3/API_AUDIT/audit2_results/` on main 0be3c352; v1.4)

Each finding was read against the supplement (pp. 13–16 as page images; p. 6 and p. 10 as text) and our statements.

| # | Finding (samples) | Decision | Reason and citation | Change made |
|---|---|---|---|---|
| U1 | B5.S (2/2): "not ordered" fails when r̄_n is small | **ACCEPT** | Theorem S assumes only (12) (supp p. 13), so r̄_n may be bounded (e.g. s₀ + 1); then Thm 1 (A4) implies (22)–(23) and asks more | B5 rewritten by regime; §S lower-bound row |
| U2 | B6.S (2/2): "weaker" needs \|t\| + r̄_n ≥ our set size | **ACCEPT** | for r̄_n ≺ log n (allowed by (12), Cor S₁ with k₁ < 1, supp p. 16) a set of log n null columns can satisfy (22) and violate (A5) | B6 rewritten by regime |
| U3 | SAMP.LABEL (2/2): "weaker counterpart" fails; "not none" stands | **ACCEPT** | theirs: N → ∞, every data set, convergence to posterior quantities (supp pp. 9–10, 12–13, 16–17); ours: finite budget, design conditions, a different object | §S core 3 paragraph; AUDIT rows |
| U4 | HEAD.S (2/2), HEAD.H (1/2): the headline's "we ask less / we add" clauses | **ACCEPT** | they depend on r̄_n, on the reading of β*, on centring; their Hellinger theorems do carry a law for x (\|x_i\| ≤ 1, p. 952; Condition 1, p. 953) and a range for P_n | headline replaced by the HQ form; B2, B7 rewritten |
| U5 | HEAD.CONC (2/2): "our conclusions are stronger" | **ACCEPT**; one clause rebutted | Thm 3's error exp(−c₁nε_n²) is below every power of n (p. 956): not implied by ours. Rebutted in part: Theorem 9's level-M form does give the exponential form up to M ≤ √n/log n (`W3-DIST:Thm-A`), so the Hellinger tails match inside that window | blanket claim dropped; per-theorem list in §S |
| U6 | S.LOWER (2/2) | **ACCEPT** | as U1 | §S row |
| U7 | S.UPPER (1/2): the upper half of (22) is not a real difference | **ACCEPT** | (22) is existential in l′_n; for columns of squared norm n − 1, l′_n = \|t\| + r̄_n works and n·l_n ≻ l′_n follows from (23) | §S row; B5 |
| U8 | S.CONC (1/2): "ours implies (24)" compares two posteriors | **ACCEPT** | (24) is about their posterior (7) under prior (6) (p. 951; supp p. 13); ours about the coded posterior | §S conclusion row; AUDIT row |
| U9 | B4.PROOFS (1/2): "needs β*_t bounded away from zero" | **ACCEPT** | the printed bound is on supp p. 6 and needs only a rate; likewise supp p. 15 | B4 rewritten; §T2 |
| U10 | B4.STATED (unclear): may their β* vary with n? | **ACCEPT as open** | the texts read as one fixed sequence (p. 950) but do not say so | B4 states both readings; the "1/n" example is dropped |

## C-NOTS. Track C cross-check with the NOTS cells (track C lead, 2026-11-16; B9 correction folded into the B9 dossier by the manager, v1.4.1; details `track_C/RESULTS.md`, final)
- B5: confirms "all inside": sample floors (sets of 16 and the m♯ cutoff) rise with n at p = 10n and at p = 2·10⁴ in all 19 designs.
- B6: confirms "all inside": Occam term bounded and decreasing at p = 10n in every design.
- B8: confirms inside (IND, AR, blocks, S6, aligned factors) and outside (mixed-sign strong factor D14/D15, riboflavin-like); refines the two "unclear": S5-type (4 mixed-sign truths) has a small positive population margin (0.06) and rising sample visibility; FRED-like is inside when tiled (population 0.08–0.30, sample rising).
- B9: confirms every listed in/out; **corrects the Track-C sentence on AR(0.95)**: at p = 10n its leak set grows ≈ n^0.1 (466 → 585), not n^0.4–0.5 (that was capped by p = n = 200); Toeplitz α = 1 (n^0.4) and growing blocks (n^0.5) stand.
- B10: confirms inside for IND, AR(0.5), blocks, S6; AR(0.8) spread unclear and improving.
- B11: confirms; **corrects "leak set = S₀ for IND only"**: also for weak factors (common correlation 0.5 p^{-1/2}) once below √(log n/n); no study/P6/1M design is of that kind, so no design verdict changes.
