# R02 disposition (fresh statement lock, Codex gpt-6.1-sol high — verdict LOCK-WITH-CHANGES)

1. **X3 prefix form; off-by-one; B1 crossing case.** X3 now states every claim for a given prefix (any length I);
   (vii) is in prefix form (M := min(i₀, I) ≤ Q; the contradiction uses only the centres x_0, …, x_Q and the Q + 1
   deleted points; no bound on x_{Q+1} is asserted); (iii) gives the general-|K| crossing bound ω < c(κ′)ϖ besides
   ω < 4ϖ for |K| ≥ 3; (ix) uses it. X4.4 applies X3 to the established prefix of length i (no future step), and B1 is
   split into the narrow phase (deletions confined near x_0; far kept points of both signs) and the wide phase
   (no crossing, so only the last-point deletion can empty a side). Order B1(i) → B2(i) → B3(i) → B4(i) kept.
2. **X2 constants for bounded p.** Accepted (R02's p = 2 counterexample is valid for the v2 event). D3/D4 now bound
   |η| and the truth coordinates by √(2L_n) ≤ H̄ (probability cost ≤ (s₀ + 1)/log n); one definition
   H̄² = 2 log(2(p − s₀) + 2) + 2L_n in X2–X4 and STATEMENT; |x_T| ≤ H̄ + ℓ√(2L_n) ≤ (1 + ℓ)H̄; Proposition X2's
   right side uses H̄ + |x_T| ≤ (2 + ℓ)H̄; regime (S) uses the sharper H̄ + ℓ√(2L_n).
3. **Binding in (C2).** STATEMENT §3/§4 define S*(N), 𝒩*(N), m₀(N) and edges for each N; the LS0/cap consequence is
   restricted to N = N₀.
4. **Gain-error conversion; E-add factor; end phase.** X4.1 keeps E = C/n + C|τ̂_{j′}|⁴/n and uses
   √(x + y) ≤ √x + y/(2√x), giving slack C n^{−1/2} + C H̄³/n. E-add uses |δ|/(1 − γ_{k+1}) ≤ 2ϖ. The end-phase
   structure is re-proved for the approximate rule (no crossing via ω ≥ 2(H − δ_e) > c(κ′)ϖ or an empty side; the
   deleted null is the edge point by D8; exact top sets propagate), instead of importing FACB L4.1.
5. **Frontier wording.** "iff"/"i.e." removed in STATEMENT §5 and X2's remark; the criterion is stated as sufficient;
   the additive (log n)^{3/2} term is shown to vanish by the n^{−1/3} floor; X2 no longer claims anything for A₁ ≥ ½.
Optional: 1 — N3X extended (numerics/n3x_softgap.py now also checks the prefix conclusions of (vii)); 2 — dependency
table added to X4.2; 3 — N1X wording already distinguishes the fitted δ̂ from δ.
