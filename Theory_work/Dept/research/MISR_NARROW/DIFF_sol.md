# Statement diff review — Sol

Reviewed the authoritative patch against `origin/main`, the specified original statement/proof spans, L1-1 and K1-1, the BASE_KL_VERDICT, and the rider wording at lines 123–131. The patch was reconstructed and checked in memory only; no source file was patched and no scratch files were created.

**(a) PASS — the restricted reading is true.** For each n, take α and the example's parameters deterministic, with σ²_𝒞 > 0 as in Corollary G's applicable regime. Set γ = Σ_𝒞𝒞⁻¹Σ_𝒞𝓜β_𝓜 and a = m_𝓜ᵀβ_𝓜 − m_𝒞ᵀγ. Gaussian conditioning gives

    X^r_𝓜,iᵀβ_𝓜 = a + x_𝒞,iᵀγ + ζ_i,
    ζ_i | x_𝒞,i ~ N(0, τ²).

The residual is independent of the candidate row, and the independent noise adds variance σ²; thus y_i | x_𝒞,i ~ N(α′ + x_𝒞,iᵀβ^𝒞, σ²_𝒞), with α′ = α + a. This is a member of the candidate linear-Gaussian family, so the minimum KL divergence from the true conditional law is zero. For centred population rows (m = 0), a = 0, giving the stated SL f₀ reading. Conditional on the entire candidate design, subtracting the sample average of the conditional mean gives marginal N((CX^r_𝒞β^𝒞)_i, σ²_𝒞); this preserves the distinction from the actual centred response Cy^r, whose marginal variance is σ²_𝒞(1 − 1/n). Deterministic parameters may still depend on n.

The standing allowance for random α remains valid for the contrast/contraction statements, but cannot justify an unrestricted row-wise Gaussian claim: the supplied α = (X^r_𝒞)²_{2,1} counterexample adds an independent χ²₁ shift to row 1. The added disclaimer accurately withdraws that interpretation for random intercepts; it does not assert that every random-intercept model lacks some possible KL interpretation.

**(b) PASS — scope is confined to the reading and its changelog.** Exact hunk/context verification against `origin/main` succeeds. Both versions have 272 lines; the complete set of changed line numbers is {1, 191, 192, 193, 194, 195}. Cor-H's hypotheses and displays at lines 178–186, the reference-law paragraph at lines 187–190 and the initial “interpretation.” on line 191, and lines 196–197 are unchanged. All other body lines are identical. The substantive edits at 191–195 add the deterministic-intercept/parameter restriction, its provenance tag, and the matching random-intercept disclaimer; the remaining changes there are wrapping. Line 1 only updates the version/date and appends the described changelog entry.

**(c) PASS — WEAKER is the correct tag.** The old interpretive assertion covered random intercepts allowed by the standing convention; the replacement claims less by adding a used deterministic-intercept hypothesis. Unchanged contraction displays do not make this interpretive restriction EQUAL. This agrees with K1-1's classification.

**(d) PASS — no concrete application defect found.** The qualifier clearly attaches to the KL reading alone and matches the rider's accepted deterministic-intercept wording. The tag [W3-MISR-R L1-1] identifies the rider and the finding in [L1_statement_lock_sol.md](/home/fb31/BVS-wt/W3-MISR-R/Theory_work/Wave3/W3-MISR-R/reviews/L1_statement_lock_sol.md:7), so its provenance is resolvable. The wrap keeps the bold qualifier balanced, preserves paragraph structure and the 272-line count, and introduces no mathematical ambiguity. The unchanged proof's Gaussian-conditioning argument supports the narrowed statement when read under its new deterministic-intercept restriction; this statement-only patch need not change the proof file.

DIFF: PASS
