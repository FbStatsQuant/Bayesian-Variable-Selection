# Audit auditD3-s2: W3-D3 API card
claims: Thm2SG, B3w, ExSG
stop_reason: end_turn

No ERROR and no GAP found in any of the three spans. The only findings are MINOR.

**W3-D3:Thm2SG**

- **MINOR — ASSEMBLY.md:17-18, used at :27-28.** B0 (e) is quoted with its hypothesis elided. The source (B0.md:28-29) reads "If the rows satisfy (RD) ([DIST] `STATEMENT.md:17-20`) — or the reader assumption (A1) (`:161-162`) …". That "(A1)" is [DIST]'s, not this ticket's (A1) = (S1)+(S2), and neither (RD) nor [DIST] (A1) is restated or checked in the present setting (sub-Gaussianity on sparse directions only). The claim is unaffected because the fact used is direct: ỹ = (y^r − α*1)/σ* = X^rβ̃* + ε/σ*, with ε/σ* ~ N(0, I_n) independent of X^r by (S1). Step 3 (ASSEMBLY.md:37) in fact uses only this identity.

- **MINOR — STATEMENT.md:47 with :26-28.** (A1) is copied verbatim from the recorded Theorem 2 as "(S1) and (S2)", but in the recorded (S2) ([RV]:29, [NOT]:12-13) p is the retained column count, while here p is the raw count. The words are quoted faithfully; the symbol is not the recorded one. This is disclosed at :26-28. The coverage claim in remark 4(a) is unaffected, since Gaussian rows with unit variances have p_ret = p almost surely.

**W3-D3:B3w**

- **MINOR — B3w.md:89-92 (Step 4).** B2 (a) is invoked at q = q_n = ⌊W̄_n⌋, which may exceed p. The statement header of B2 (B2.md:7-21) is not among the consumed excerpts, so the list "B2's other hypotheses" at :90 cannot be confirmed complete. B2's own parts (d), (e) take q_n = min{p, ·}. The claim is unaffected because the display at B3w.md:86 already gives λ_min(G_T) ≥ nφ²/4 ≥ φ²/8 = g₀ for every T with 1 ≤ |T| ≤ w_n, since (A3) covers all such T. Alternatively, invoke B2 at q = w_n, using 𝓔₂(q_n) = 𝓔₂(w_n) from :22-23.

**W3-D3:ExSG**

- **MINOR — ASSEMBLY.md:65-66, STATEMENT.md:87.** "In particular (A4) holds with this L" is proved for one law x = m + Bξ. (A4) in Theorem 2SG is a condition on the whole array with one fixed L. For an n-dependent family (m_n, B_n, ξ^{(n)}), the scalar bound E exp(λξ_k) ≤ exp(L²λ²/2) must hold with the same L for all n and k. This is true in all the examples of (b), but it is not said in the statement.

AUDIT W3-D3:Thm2SG FINDINGS=0
AUDIT W3-D3:B3w FINDINGS=0
AUDIT W3-D3:ExSG FINDINGS=0