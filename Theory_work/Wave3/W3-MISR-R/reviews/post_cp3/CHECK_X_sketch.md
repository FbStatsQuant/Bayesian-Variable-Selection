# CHECK X — unchecked sketch, input for check X (post-freeze)

Status: **unchecked sketch**; not reader text, not a claim. Moved verbatim from the v0.4 draft of `READER_DELTA_v0.4.md`
(manager instruction, 2026-11-16) as input for the consultant's check X (alignment of card rows 1.2 and 1.4), which HQ parked
for after the freeze: a read-only alignment note first, then an HQ decision.

## Remark text (as drafted, withdrawn from the reader delta)

*Relation to Theorem 2 [P4].* With no omitted predictors ($\beta^{\mathcal C}=\beta$, $\sigma^2_{\mathcal C}=\sigma^2$), the
assumptions of Theorem 2 imply (A0)–(A3): Theorem 2's floor is on larger sets, and a correlation-matrix covariance, a fixed
$s$, coefficients $b_{\mathrm{lo}}\le|\beta_j|\le b_{\mathrm{hi}}$ and a fixed $\sigma^2$ give the energy bound and a diverging
beta-min. So in that case Theorem 4 gives Theorem 2's conclusions for $1-\pi(S_0\mid y)$ and the HPM in the stronger
expectation form, and also when $\Sigma$, $\beta$, $\sigma^2$ vary with $n$; Theorem 2's PIP and MPM clauses then follow from
the deterministic bounds $\max_j|\mathrm{PIP}_j-\mathbf 1\{j\in S_0\}|\le1-\pi(S_0\mid y)$ and
$\{\mathrm{MPM}\neq S_0\}\subseteq\{1-\pi(S_0\mid y)\ge\tfrac12\}$. Theorem 2 does not give Theorem 4 (it fixes $\sigma^2$ and has
no omitted predictors). The two theorems rest on different masters with their own conditions, and this comparison is a
bridge (B4.5), not a separate claim.

## Bridge row B4.5 (as drafted, withdrawn from the bridge table)

| # | bridge | mark | detail |
|---|---|---|---|
| B4.5 | Relation to Theorem 2 (remark) ⇒ masters | NEW (comparison; for W3-READER's fidelity read) [P4] | Theorem 2 (row thm2: (A1)–(A3), `READER_VERSIONS.md:255-262` at W3-READER 45d39fb4) with no omitted predictors ⇒ CorGb-plus hypotheses: floor on \|S\| ≤ 5(A+1)(s₀+1)log n ⊇ the sets of (A2) here; energy β'Σβ ≤ λ_max(Σ_SS)‖β_S‖² ≤ s²b_hi² (correlation entries ≤ 1), so M₀ = s²b_hi²/σ²; beta-min n b_lo²/(σ² log n) → ∞; (S1) gives (A0) with constant α′. Conclusions: CorGb-plus display; PIP/MPM by the deterministic consequences of W3-MISR STATEMENT.md:119-120 (MIS-R (i), items 1–2, "for every data set"). Not implied: Theorem 4 by Theorem 2. Masters differ: W3-MISR-R:CorGb-plus vs W3-POST:Thm-1 item 6 + W2-APP:POST |
