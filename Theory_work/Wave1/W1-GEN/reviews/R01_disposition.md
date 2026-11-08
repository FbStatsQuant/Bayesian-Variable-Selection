# R01 (statement lock, Codex gpt-6.1-sol high) — disposition by the lead

Verdict received: LOCK-WITH-CHANGES. All nine required changes accepted and applied in STATEMENT.md v2.

| # | Required change | Disposition |
|---|---|---|
| 1 | H0 explicit; empty-family conventions; residual directions only where SE gives them | Applied: H0 written out (j₀, m♯_n, R_m, normalized vs unnormalized eigenvalues); ζ_n := 0 if 𝒱 = [p]; NL_avg omitted if p = s*; ε₀, E-convention stated; u_{T,l}, δ_{T,l} defined only on named families. |
| 2 | Exact Λ-minimiser is not a valid canonical S* (W counter-instance) | Accepted (the W instance is correct: ε_n-leakage makes the exact minimiser include nulls with o(log n) gain). S* is now an existential certificate; the "canonical" sentence removed. |
| 3 | State the generalized T22 lemma precisely | Applied in (C1) and to be written in L2 with each substitution recorded (reference S*, NL_C + NL_avg replacing NL_η, EXP′ from L1). |
| 4 | L3 must cover swaps, supersets, (L), and the whole BM-∞ range with contrast-level bounds | Accepted. (C2) now states the TD′_∞-type conclusion on 2^𝒱 incl. (L); L3 will use contrast-level Gaussian bounds (error O(σh_n‖r_A − r_P‖) + O(log n)), not E5's absolute n^{2/3} error nor U3's fixed margin. SEP restated relative to the guaranteed decrement: ζ_n ≤ c_S(n−1)φ₀⁴θ*²_min, c_S < 1 (more general than v1's o(·)). |
| 5 | Cap/operational quantifiers | Applied: τ(C) defined for the uncapped path; capped scoring/certification as implications; "centres" vs scanned neighbours distinguished; C3 for n with |𝒱| ≤ K and ℓ_n ≥ 2^{v̄} − 1; C3-fav uses D_n ≤ P(S̃₀ ≠ S₀) only; R′ > 4 premises (IND-T, extra search from c₄) listed. |
| 6 | C4 uniform quantifiers; measurability | Applied: every deterministic sequence in 𝒜_n satisfies the hypotheses with the same constants and the same deterministic envelopes; 𝒱, S*, β X-measurable; diagonal argument to be proved in L5. |
| 7 | Precise instance obligations | Applied: LH defined as in T38_PROOF.md:217-235 (rank-one hub links, unit structure); LH-iid hypotheses to be verified directly on 𝒜_n; W's (H0) to be verified directly; candidate inputs labelled. |
| 8 | Define the study asymptotic sequence | Applied: sequence defined (groups of 5, fixed signal groups, β pattern, c, p_n → ∞, β X-measurable); per-scenario claims S1/S3/S4/S6 covered, S2/S5 not, to be proved; actual partition checked; nothing at n = 200. |
| 9 | C6: reformulate conclusion and isolate hypotheses | Applied: new construction with weak nearly-orthogonal proxies (a/√d_n loading) so that SE on 𝒱 holds with a fixed φ₀ and SEP holds; all hypotheses except |𝒱| ≤ v̄ retained; failure stated on a high-probability event via the 2(ℓ+1) distance bound; conclusion = no universal LS0-discovery guarantee; full-method D_n not claimed. |

Optional suggestions: separation of core vs instances adopted (L1–L5 core; L6, L7 separate); look-alike detour test is
in numerics E4(i); p ≤ 10 exact enumeration where used.

STATEMENT.md v2 is LOCKED (2026-11-08).
