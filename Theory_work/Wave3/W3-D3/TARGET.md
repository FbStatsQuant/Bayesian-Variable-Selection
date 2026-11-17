# W3-D3 — TARGET (one page; RIDER_RULES §2)

**Target clause TC1 = Theorem 2SG** (`STATEMENT.md` §1); companions B3w (§2) and ExSG (§3). Coexisting with row 1.2.

## Assumption map of the changed hypothesis

| hypothesis | row 1.2 (recorded) | Theorem 2SG | used where | class (D109) |
|---|---|---|---|---|
| row law | i.i.d. N_p(m_n, Σ_n), Σ_n a correlation matrix | i.i.d., mean m_n, covariance Σ_n a correlation matrix, and (A4) | B3w: sample SDs ([EB]`B1.md`), sparse sample Gram floors ([EB]`B2core.md`, `B2.md` (a)) | 1 (proposed; STATEMENT §5: between NH14 Lemma 6.1 and SL Condition 1) |
| (A4) constant L | — (L = 1) | fixed L | B1, B2core exponents c₁n/L⁴, c₂n/L⁴; threshold n₁(s₀, A, L) | as above |
| (A1)–(A3) | as recorded | verbatim | as in row 1.2 | as recorded (ASSUMPTION_COMPLIANCE.md lines 27–29, branch theory/W3-AUDIT) |

No hypothesis is weakened below the recorded reader statement except the row law, so no boundary numerics are owed; a
sanity run with non-Gaussian rows (Rademacher, uniform, and a correlated Rademacher mixture) is in `numerics/`.

## Parity rows

| clause | vs row 1.2 (reader Thm 2) | vs closest published result |
|---|---|---|
| hypotheses | STRONGER theorem (row law widened; rest verbatim) | Song & Liang (2015) Thm 2 (p. 953): random design under their Condition 1 (weaker than (A4)), their prior with tuning (not the coded prior), conclusion = Hellinger contraction of the joint density, not model selection. NH14 Lemma 6.1 (p. 16): independent isotropic sub-Gaussian rows (identity covariance) give the sparse minimum-eigenvalue part of their Condition 4.5 with high probability (pp. 16–17); their prior is a spike-and-slab prior with shrinking and diffusing variances. Ours: coded prior, no tuning, exact selection at rate √(log n/n) under any correlation with a sparse floor. |
| conclusions | EQUAL (verbatim) | different in kind from SL's (exact selection with a rate, against contraction of the joint density); no comparison with NH14's conclusions is made here |

## Why each assumption (one line each; for the reader version)
- (A4) Only to make the sample standard deviations of the predictors and the sample correlation matrices of small groups
  of predictors track their population values; the fixed-design posterior theorem uses only the observed design.
- (A1)–(A3) as row 1.2 ([RV] `:280-289`).

## Necessity (not claimed)
Some tail condition is needed by this route (the sample floor of a set of predictors can fail with non-vanishing
probability for heavy-tailed or very sparse binary predictors). Whether posterior concentration itself needs it is open;
nothing is claimed.
