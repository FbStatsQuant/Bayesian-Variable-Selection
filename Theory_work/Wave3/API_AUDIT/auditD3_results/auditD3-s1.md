# Audit auditD3-s1: W3-D3 API card
claims: Thm2SG, B3w, ExSG
stop_reason: end_turn

**No ERROR or GAP found in any of the three claims.** I checked every step named in the brief against the supplied excerpts, including the constants, the quotations, the Hoeffding proof and the unstated-hypothesis question, and each holds as written. The only findings are four MINOR slips.

**MINOR 1 — `ASSEMBLY.md:75` (ExSG (b), Hoeffding's lemma, degenerate case).**
The stated reason "if a = 0 then b ≥ 0 = E Y forces Y = 0 a.s." is not the operative one. What forces Y = 0 a.s. is Y ≥ a = 0 together with E Y = 0 (symmetrically Y ≤ b = 0 in the other case). The conclusion is correct, and the case cannot occur for ξ_k with variance 1.

**MINOR 2 — `B3w.md:89-92` (Step 4, citing B2 (a)).**
The line "B2's other hypotheses: 2 ≤ p, Var(x_j) = 1, (SG_{q_n})" cannot be checked against the excerpt, because the standing hypotheses of `B2.md` (lines 1–21) are not supplied. The conclusion does not depend on them. Repeating the chain of `B3w.md:86` (Step 3) for |T| ≤ q_n gives λ_min(G_T) ≥ nφ²/4 ≥ φ²/8 = g₀ directly from 𝓔₁, 𝓔₂(q_n), the Gram identity and (A3).

**MINOR 3 — `ASSEMBLY.md:27-28` (Step 1, citing B0 (e)).**
B0 (e) is stated under "(RD)" or "reader assumption (A1)" of the W3-DIST statement, neither of which is in the excerpt. The citation is not needed: Step 3 (`ASSEMBLY.md:37-38`) builds Y° = X°θ° + Cε/σ* explicitly and verifies Y° = Cỹ on {p_ret = p} by direct computation. Only B0 (a) is used, and its hypotheses (n ≥ 3, p_ret ≥ 1, y^r non-constant) are met on the data sets fixed in Step 1.

**MINOR 4 — `STATEMENT.md:33-38`, `ASSEMBLY.md:23, 36-37` (outputs on a null set).**
The conventions do not define δ_n, PIP_j, HPM, MPM when y^r is constant, nor the °-outputs when Y° = 0. Both events have probability zero (n ≥ 3, ε Gaussian and independent of the design), so the bounds in `ASSEMBLY.md:45-48` hold after discarding one null set. The discard should be stated in Step 4.

AUDIT W3-D3:Thm2SG FINDINGS=0
AUDIT W3-D3:B3w FINDINGS=0
AUDIT W3-D3:ExSG FINDINGS=0