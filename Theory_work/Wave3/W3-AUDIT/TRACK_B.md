# W3-AUDIT — track B: are the design and data assumptions reasonable? (v1.1, revision round, 2026-11-16)

Author: audit Fable. Each dossier: **verdict** against Song and Liang (2015) → **strongest evidence** → **holds / fails**
→ **our designs** → **candidate corollary** in primitive terms (Σ, β, σ², n, p). Nothing here is a registered result.
My own short computations on which a verdict depends were checked by an independent reviewer and are marked
"checked (AUDITCALC_check_opus.md §k)" (`reviews/AUDITCALC_check_opus.md`, 2d7c2b90: none refuted, four corrected). Lines still marked
[audit calc] or [audit reading] carry no verdict and are unchecked. Track C (internal proxy computations,
`track_C/RESULTS.md` @ 4f0f9a82, Owls part; NOTS cells pending) is cited in the design lines; it tests 19 designs that
include ours or close relatives. Citations of `W3-READER` files are **(READER pre-freeze)**: read at 7eb818e6, to be
re-pinned to the READER commit of the CP3 freeze.

## Answer (for the owner's question)

1. **The posterior theorems (core 1: the true model; core 2: the true distribution) hold on all our designs** — the
   2,400-fit study, P6 with its strong factors, and the 1M plan — **under assumptions that are the same as, or comparable
   to, Song–Liang's.** Three items are stronger than theirs: the range of p (p ≤ n^A, B2), a collinearity floor of order
   c/n on O(log n) columns (B6), and the law of the rows (Gaussian or sub-Gaussian, B7).
2. **The reported-model theorem (core 3)** adds two method-specific conditions with Song–Liang counterparts: visibility
   (stronger than their Condition 5, B8) and a leakage set (their remark (a), p. 958, B9). Inside: S1–S4, S6, IND, AR,
   BLK. Outside: pervasive factors at p ≫ √n (S5, P6, FAC).
3. **The printed-estimates theorem (row 3.6)** is correct as stated and has a narrow reach: its "no leakage" condition
   (B11) holds on S1 and IND only. Outside it, Theorem 6 (reported model) and row 3.5 (unbiased evidence) still hold.

| Core theorem | Assumptions against Song–Liang | Our designs inside |
|---|---|---|
| 1 and 2 (posterior) | same or comparable; stronger: B2, B6, B7 | **all** |
| 3 (reported model) | + B8 (stronger than Condition 5), B9 (comparable to remark (a)), B10 (no counterpart) | S1–S4, S6, IND, AR, BLK; not S5, P6, FAC |
| 4 (printed estimates, row 3.6) | + B11 (no counterpart) | S1, IND only |
| 5 (rate lower bound) | witnesses only | — |

**Song–Liang source.** Every "SL" reference is to the paper itself, read first-hand: Q. Song and F. Liang (2015),
J. R. Statist. Soc. B 77(5), 947–972, local file `/home/fb31/SMC_Theory_Department/refs/Song_Liang_2015.pdf` (sha256
`315c247c236b5f33…`; not in git). Page numbers are journal pages. Their supplement (proofs; Theorem S on MAP
consistency) is **not inspected**: no comparison below relies on it. Their theorems are for a random design; x has law ν_x.

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
**Verdict: same as Song–Liang** (their model (1) and density (2), p. 950).
**Evidence.** SL (2): f*(y, x) = φ(y; xᵀβ*, σ*) ν_x(dx). Ours: the same model with an intercept; Thm 9 lets σ* depend on n.
**Holds / fails.** Fails for heavy-tailed or heteroscedastic errors; no theorem of ours or of SL covers them.
**Designs.** All inside (Gaussian noise generated). **Corollary.** None needed.

## B2. Dimension p ≤ n^A (all theorems except Thm 3(a))
**Verdict: stronger than Song–Liang on the upper range** (their Corollary 1, p. 954, allows P_n < exp(Cn^α), α ∈ (0, 1));
**weaker on the lower range** (they assume P_n ≻ n^θ for some θ > 0, p. 950; we need no growth of p).
**Evidence.** The registry records it as a consequence of the prior and the proof technique, with exponential p "OPEN"
(`assumptions.tsv` A:P-POLY). It enters through union bounds over models of O(log n) variables.
**Holds / fails.** Holds for every polynomial regime, p ≫ n included. Fails only for log p of polynomial order in n.
**Designs.** All inside: the largest exponent is 1M at n = 200, A = log 10⁶ / log 200 ≈ 2.6.
**Corollary.** None; the constant A enters the other assumptions only through set sizes of order (A + 1)s₀ log n.

## B3. Exact sparsity with s₀ fixed (Thm 1, 2, 6, 10; Thm 9 with "at most s")
**Verdict: same as Song–Liang** (their strict sparsity (4), p. 950, used by Theorems 2–3; their Theorem 1 alone allows
the weaker (3)).
**Evidence: it cannot be dropped.** Theorem 3(a) (`W3-PSHARP:B@1.0.0`, "PROVED-CHECKED; council R2, …"): on every design
π(S₀ | y) ≤ (1 + (s₀ + 1)/(3√n))⁻¹, so π(S₀ | y) → 1 forces s₀ = o(√n), and the rate √(log n/n) forces s₀ = O(√log n).
**Designs.** Inside as sequences with s₀ fixed. At the simulated sizes the same bound is informative [audit calc]:
Study (s₀ = 14, n = 200) π(S₀ | y) ≤ 0.74 for every data set; P6 (4, 50) ≤ 0.81; 1M (5, 200) ≤ 0.88. At these sizes the
posterior is a mixture over S₀ and its neighbours; that is its shape, not a failure (card note ENG-D17).
**Corollary.** None. A generator rule s₀ = ⌊√n⌋ would be outside (`Docs/THEORY.md:325`).

## B4. Signal size: bounded above, and fixed nonzero or beta-min at √(log n/n) below
(Thm 1 (A3), (A6); Thm 2 (A2); Thm 6 / 10 (A2); Thm 9 (A5); none below in Thm 9.)
**Verdict: comparable to Song–Liang.** Above: their (3) with |x_i| ≤ 1 (Theorem 1, p. 952) bounds the signal; under (4)
alone their main text states no bound. Below: their Theorem 3 (p. 956) states **no** beta-min; a true predictor needs
only to be "identifiable" (Condition 3, p. 955), and the step "d(f*, f) ≥ ε_n for any density f that does not select x_t"
is in their supplement (not inspected).
**Evidence.** Thm 2, 6, 10 assume only fixed nonzero coefficients, as SL's setting does. The explicit beta-min is used
only in the fixed-design Thm 1, at the usual order σ√(log n/n); Thm 1′ and Thm 9 have none. Without any lower bound
specificity can fail (numerical counterexample, Thm 1 remark (ii)).
**Designs.** All inside (fixed nonzero coefficients, far above the √(log n/n) scale as n grows). Track C: the beta-min
rate and the identifiability margin grow like n^0.7–1.15 in all 19 designs (P7).
**Corollary.** Thm 2 is already in primitive terms: b_lo ≤ |β*_j| ≤ b_hi on S₀.

## B5. Eigenvalue floor on small sets (Thm 1 (A4) / (A4′); Thm 2 (A3); Thm 6 / 10 floors; Thm 9B (A6a))
**Verdict: comparable to Song–Liang's Condition 3** — stronger in level, on smaller sets, and for a stronger conclusion.
**Evidence.** SL Condition 3 (p. 955): E exp{−(x_k + Σ_{i ≤ r̄_n} b_i x_{j_i})²} ≤ 1 − δ_n with δ_n ≻ ε_n². Their own
sufficient forms: for standard normal predictors var(x_k + Σ b_i x_{j_i}) ≻ ε_n², implied by ch′₁{var(x)} ≻ ε_n²
(pp. 955–956); for bounded predictors ch′₁{var(x̃)} ≻ r̄_n ε_n² (p. 955). So SL ask a **vanishing** eigenvalue level on
sets of r̄_n + 1 predictors, r̄_n → ∞ (Theorem 2 needs r_n ≻ 1 and (12) r_n ≤ r̄_n, pp. 952–953), anchored at each true
predictor, and conclude **sure screening** only (p. 956: "the specificity is not controlled"). We ask a **fixed** level
φ² on sets of O(log n) predictors (Thm 2; the master needs it fixed only on sets of (2A + 2)s₀ + 2 predictors) and
conclude exact selection with a rate. Both are implied by λ_min(Σ_n) ≥ c, the form a reader will check first. **No upper
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
**Verdict: stronger than Song–Liang's Theorems 1–2, which have no design eigenvalue condition;** very weak in absolute
terms, and it is the population twin of a term SL put in their prior.
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
**Verdict: Thm 9 (A3) is stronger than Song–Liang's Condition 1 and implies it; Gaussian rows are stronger still.**
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
**Verdict: stronger than Song–Liang's Condition 5** (p. 958: |cov(x_t, y)| > 0 for every true predictor), which is its
case U = ∅ without the margin; same role (the cheap first stage must see every true predictor).
**Evidence.** U = ∅ in (A3) gives |Cov(W_j, y)| ≥ a [one line]. SL need Condition 5 so that their iterative subset
screening "ensures that all true predictors that are contained in X_s will be selected" (p. 958). Ours conditions on up
to 15 other columns because the method's blocks have at most 16 columns.
**Holds / fails.** Holds when no truth is cancelled by ≤ 15 others: bounded blocks with one truth each, AR, banded
(W2-APP family map, "PTV automatic if ≤ 1 truth/block", `L4_families.md:165`). Fails for masked truths (zero marginal or
partial covariance with y); those designs are treated by a separate theorem (W1-PXN), not by Thm 6. Track C gives two
concrete failures at the population level: a pervasive factor with **mixed-sign** truths (its D14, D15: a set of ≤ 15
columns cancels the truth's covariance with the signal) and a riboflavin-like real-data design (D18).
**Designs** — checked (AUDITCALC_check_opus.md §5). Inside: S1–S4, S6, IND, AR, BLK (block or Markov structure: the
covariance is θ_j Var(W_j | W_U) plus geometrically small terms, ≥ |θ_j| λ_min/2). cs(ρ) of P6: inside (aligned signs,
positive partial covariances). **Unclear, not upgraded:** S5 (mixed signs; the checker's search finds a near-cancellation,
worst ratio 0.0056), s5 and fac2 of P6 (no cancellation found, 0.364 and 0.431; a search, not a proof), FAC of 1M
(0.16). Track C agrees: visibility inside and rising with n for IND, AR(0.5), fixed blocks and S6; small for S5
(population 0.06). **Typical user:** the two real-data-like designs of track C are outside (riboflavin-like) or unclear
(FRED-QD-like).
**Corollary (primitive).** Block-diagonal Σ with λ_min ≥ c and at most one truth per block ⇒ (A3) with a = c·min|θ*_j|.

## B9. Polynomial leakage set with locality (Thm 6 (A4)): Q ⊇ S₀, |Q| ≤ n^b, b < ½
**Verdict: comparable to Song–Liang, where the same requirement is an informal remark, not a condition.**
**Evidence.** SL p. 958, remark (a): "all the predictors that are correlated with X_t will be selected … if all the
predictors are linearly correlated, it is futile to apply this iterative procedure"; and "if there are p_n predictors
correlated with the true predictors X_t, p_n ≺ P_n, then there are at most cp_n predictors to be selected". Ours states
it as a hypothesis with a rate: nulls whose conditional covariance with a truth is above o(√(log n/n)) must lie in a set
of at most n^b columns; correlations below that level do not count. SL prove no theorem on their sampler's output
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
common correlation. It adds: the leak set grows like n^0.4–0.5 for AR(0.95) and Toeplitz decay α = 1 (inside only for
b close to ½), and a factor whose common correlation decays like p^{-1/2} comes inside from n = 800.
**Corollary (Thm 6, primitive; candidate, short proof expected).** Rows i.i.d. N(m, Σ), Σ block-diagonal with blocks of at
most g columns (g fixed), λ_min(Σ) ≥ c, at most one truth per block, fixed nonzero θ* on S₀, p ≤ n^A: every admissible
run that produces output reports S₀, on one data event of probability → 1. Route: Q = the truths' blocks, H_l = Q ∪
block(l), N_l = block(l) ∩ Q, L_n = 0, ϖ_n = r_n = 0; then B8's corollary and Thm 6.

## B10. Floor on Q ∪ {l} and local regressions inside Q (Thm 6 (A5) second part, (A6))
**Verdict: no Song–Liang counterpart** (it serves the search, which they do not analyse); implied by B5's global floor
plus a locality property of Σ.
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
**Verdict: no Song–Liang counterpart; narrow.** It is the one assumption of the core theorems that most of our own
designs violate.
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
**Verdict: not an assumption to defend** (a lower bound needs one design; SL have no lower bound). Part (a) has no
assumption. **Designs.** S1 and IND are of type (N-gauss) only if the truths are independent of the nulls (they are).

---

## Summary table (assumption × Song–Liang × our designs)

| # | Assumption (theorems) | Against Song–Liang (2015) | Study S1 / S2 / S3,4,6 / S5 | P6 | 1M IND / AR / BLK / FAC |
|---|---|---|---|---|---|
| B1 | Gaussian linear model (all) | same: (1)–(2), p. 950 | in / in / in / in | in | in / in / in / in |
| B2 | p ≤ n^A (all) | stronger above (Cor 1, p. 954); weaker below (P_n ≻ n^θ, p. 950) | in | in | in (A ≈ 2.6) |
| B3 | s₀ fixed (all) | same: (4), p. 950 | in (as a sequence) | in | in |
| B4 | signal bounded; fixed nonzero or beta-min (1, 2, 6, 10; 9 above only) | comparable: (3), p. 950; no beta-min stated in Thm 3, p. 956 | in | in | in |
| B5 | eigenvalue floor on small sets (1, 2, 6, 10, 9B) | comparable to Condition 3, p. 955: fixed level against vanishing, smaller sets, stronger conclusion | in | **in** | in |
| B6 | no near-exact collinearity on O(log n) sets (1, 9) | stronger: none in Thm 1–2 ((11), (14) are on the prior, p. 952); same order as their ridge c_n ∝ 1/n, p. 953 | in | in | in |
| B7 | Gaussian rows (2, 6, 10); sub-Gaussian sparse directions (9) | stronger than Condition 1, p. 953 (implies it) | in | in | in |
| B8 | visibility, ≤ 15 conditioning columns (6, 10) | stronger than Condition 5, p. 958 (its case U = ∅) | in / in / in / unclear | cs in; fac2, s5 unclear | in / in / in / unclear |
| B9 | leakage set \|Q\| ≤ n^b with locality (6) | comparable: informal remark (a), p. 958 | in / in / in / **out** | **out** | in / in / in / **out** |
| B10 | floor on Q ∪ {l}, local regressions in Q (6) | no counterpart | in / in / in / n.a. | n.a. | in / in / in / n.a. |
| B11 | no leakage (10) | no counterpart | in / **out** / **out** / **out** | **out** | in / **out** / **out** / **out** |
| B12 | witness designs (3(b)) | no counterpart (no lower bound in SL) | — | — | — |

**Reading.** The two posterior theorems (core 1, core 2) hold on every one of our designs, strong factors included, under
assumptions that are the same as, or comparable to, Song–Liang's; the only items stronger than theirs are the range of p
(B2), a 1/n-level collinearity floor (B6) and the row law (B7). The reported-model theorem (core 3) adds two
method-specific conditions (B8, B9) whose Song–Liang counterparts are Condition 5 and remark (a); it excludes pervasive
factors at p ≫ √n, which is where P6 sits. The printed-estimates theorem (core 4) rests on B11, which only the
independent designs satisfy.
