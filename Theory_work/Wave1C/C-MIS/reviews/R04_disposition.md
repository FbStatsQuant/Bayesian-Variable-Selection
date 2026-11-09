# R04 disposition (independent mid-point, Codex gpt-6.1-sol xhigh): VERDICT CONTINUE

| # | Severity | Finding | Disposition |
|---|---|---|---|
| 1 | major | Singleton precision formula: statement's 𝒪 includes inactive omitted columns; counterexample (Θ₁₂ = 0 yet γ₁ = 1/3) | FIXED: STATEMENT §2(iii) and L2 now define 𝒪 := S₀ ∖ 𝒞 and Θ := inverse of the covariance of the *marginal* vector (x_𝒞, x_𝒪); the reviewer's example quoted in L2 |
| 2 | major | Gaussian rows give the decomposition at each n, not GR's fixed τ² | FIXED: P(a) and STATEMENT §2(iii) say "at each n"; MIS applies only when τ_n² ≡ τ² (met in GD(a), imposed in GD(b)) |
| 3 | minor | Position MIS as a transfer theorem; no-beta-min clause screens only J_n^𝒞(c); GD(a) recovers SL's full inclusion | FIXED (STATEMENT §2(iii) GD(a) sentence); positioning goes into REPORT |
| 4 | minor | L4.7 aside P(c_n < 0) for r = 0 | FIXED |
| 5 | minor | Keep F(a)/F(b)/T qualifications visible | Kept (STATEMENT §4, 00_MAIN table) |
| 6 | minor | H/D transfers correct; preserve distinctions (no P(U_n) → 0, no HPM theorem under EP alone) | Kept; REPORT will state it |
| 7 | minor | Add an analytic target-separation example; restrict Corollary N's sample-projection claim to full column rank | ADDED Example E1 (L2, STATEMENT §2) + numerics N7; Corollary N restricted |
| 8 | minor | Boundary examples beyond GR (common random slope) and EP (pre-named target) | ADDED L5 §6 Examples E2, E3 |
| 9 | minor | Null projection s₀^𝒞 = 0; O2 wording ("cannot represent the orthogonal mean r"); L5 §3(b) superseded; register T/F(b) in 00_MAIN | ADDED Lemma Z (L6, bounded p_𝒞; GR and EP) + numerics N6; O2 wording fixed in STATEMENT §5 and L5; §3(b) marked superseded; 00_MAIN rewritten with a hypothesis-to-step table |
