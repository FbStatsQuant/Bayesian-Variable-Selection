# Changes from PROOF_v1 to PROOF_v2 (unified after Stage B round 1)

All Stage B findings were exposition-level (Opus reviewer, Findings 1–6; Astra #2 had none). The lead accepted all six. No change to the statement, the hypotheses, the conclusions or the constants.

| Finding (Opus reviewer) | Lead's judgment | Change in PROOF_v2 |
|---|---|---|
| 1. Lemma 1: a random number of uniforms consumed (stopping-time step) is not covered | Accepted | Lemma 1 proof now models island r's randomness as an i.i.d. uniform sequence. It defines the stopping time τ (uniforms consumed before particle i's round s+1), shows F_s ⊆ G_τ, and proves that the tail block V = (U_{τ+1}, …) is i.i.d. uniform and independent of G_τ. The substitution step on finite Ω is written out, and the r-step (tower-property) version is stated. |
| 2. Lemma 1: the kernel being fixed given 𝓒 is assumed without citation | Accepted | Lemma 1 proof now opens with "The kernel is fixed given 𝓒". It cites STATEMENT §1 (one kernel K₁ for all terminal rounds) and lists its ingredients (γ₁, the Gibbs conditionals, π₀, B, the neighbour graph), none fitted to the population. |
| 3. S₀ ∉ Ω: o_l(S₀) undefined; the (ii-b) parenthetical is not addressed | Accepted | The setting extends π by 0 outside Ω (so u_π = +∞ exactly when S₀ ∉ Ω) and gives o_j(S₀) an arbitrary real value c_j* in that case. The case is moved from the lemma statement into the proof of Lemma 2, for any real value. |
| 4. Lemma 4: the range H ≥ 0 should be 0 ≤ H ≤ L+4 | Accepted | Lemma 4 now reads "for every integer 0 ≤ H ≤ L+4". F_s is defined for 0 ≤ s ≤ L+4, and Lemma 1 holds for 0 ≤ s ≤ L+3. |
| 5. Lemma 4 lists (B2)–(B3) but uses only (B1); Remark 8 is inaccurate | Accepted | Lemma 4's hypotheses are now EX-A, EX-S, CAL and (B1). The remark now says (B2)–(B3) enter Lemma 5 through η̄ ≤ η and ρ̄ ≤ ρ. |
| 6. (i) EX-A not listed for Lemma 2 / Theorem (a); (ii) island index suppressed | Accepted | Lemma 2 now starts "Assume EX-A …", and Theorem (a)'s proof notes it. The setting now says the island index r is suppressed in X_{i,s}, S_{i,h,j}, B_{i,h}, k_{i,h}(j) and F_s, and kept in PIP̂_{rj} and B̄_r. |

Also changed: the title now reads "version 2 (unified after Stage B review)".
