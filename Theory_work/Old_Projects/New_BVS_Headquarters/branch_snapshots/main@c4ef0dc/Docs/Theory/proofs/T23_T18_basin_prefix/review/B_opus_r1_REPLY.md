# Stage B — Opus 5.5 (xhigh) reviewer, round 1 reply (verbatim)

Reviewer: native Agent, Plan (read-only) type, model opus, effort xhigh; packet <PC_TEMP_PATH> only. Usage reported by the harness: 81,343 tokens, 4 tool uses, 277 s.

---

# Review of PROOF_v1.tex (T23(ii)) against STATEMENT.md

**Inputs read:** STATEMENT.md, REPORT_FORMAT.md, PROOF_v1.tex and PROOF_v1.pdf, all from the packet folder and nothing else. The PDF matches the TeX source on all 5 pages. No commands were run and no files were written.

## Steps checked and found correct

- **Setting (l.29–64).** Both sets in the first case of o_j lie in Ω, so o_j(S) ∈ [0,1]. The end-of-round bounds (eq. 1) follow because m = p+B+2 ≥ 1, so the event {X^(m) ∉ A} is contained in the path event. Conditions (B1)–(B4) match the four BASIN conditions of STATEMENT §2 word for word, including the path versions of the exit and departure conditions and "for every island" in the occupancy condition.
- **Lemma 1 (l.70–80).** On finite Ω the substitution step can be checked directly. For F ∈ 𝓕_s, P(F ∩ {Φ(X_{i,s},U) ∈ Γ}) = Σ_x P(F ∩ {X_{i,s}=x}) · P(Φ(x,U) ∈ Γ), because F ∩ {X_{i,s}=x} ∈ 𝓕_s and U is independent of 𝓕_s. The r-step version used in Lemma 4 follows from the tower property, since 𝓕_s increases with s and X_{i,s} is 𝓕_s-measurable.
- **Lemma 2 (l.84–102).** k_{i,h}(j) ∈ [1,m], so S_{i,h,j} is one of X^(0),…,X^(m−1). If B_{i,h} = 0 then S_{i,h,j} = S₀. Averaging the per-round bound B + (1−B)t gives exactly B̄_r + (1−B̄_r)t. The right-hand side does not depend on j, so the bound passes to max_j.
- **Lemma 3 (l.104–118).** Both cases (j ∈ S₀; j ∉ S₀ with |S₀| = K or |S₀| < K) are correct. Each neighbouring set used lies in Ω∖{S₀}, so its π-mass is at most 1 − π(S₀). π(S₀) > 0 because γ₁ > 0 on Ω.
- **Lemma 4 (l.125–158).** The inclusion {X_H ≠ S₀} ⊆ E₁ ∪ E₂ ∪ E₃ ∪ E₄ holds. Both inductions are valid, and kr₀ ≤ H puts every index jr₀ (j ≤ k) inside [0,H]. E₂ and E₃ each take a union bound over the H transitions s = 0,…,H−1. The recursion G_l = G_{l−1} ∩ {X_{(l−1)r₀} ∈ 𝓡} ∩ {X_{lr₀} ≠ S₀} is correct, and the conditioning event is 𝓕_{(l−1)r₀}-measurable. (B1) applies to the unrestricted r₀-step kernel, which is how it is used. The case k = 0 is consistent (G₀ is the whole space and (1−a)⁰ = 1).
- **Lemma 5 round counts.** Measured round h is terminal round L+h, so H = L+h−1 transitions come before it and H runs from L to L+3. The measured round contributes one extra ρ. That gives coefficient H ≤ L+3 on η and H+1 ≤ L+4 on ρ, and (L+3)η + (L+4)ρ ≤ (L+4)(η+ρ). Also (1−a)^⌊H/r₀⌋ ≤ (1−a)^⌊L/r₀⌋ because 1−a ∈ [0,1] and the floor is monotone.
- **Theorem (c).** The step from max over j to the island average uses only the triangle inequality. Linearity over (i,h) turns Σ_i P(X_{i,0} ∉ 𝓡)/N into the (B4) expectation, so each island gets the bound δ separately and island independence is not needed. The resulting constant is exactly 𝓑_n.
- **Theorem (d).** The inclusion {MPM̂ ≠ S₀} ⊆ {max_j |PIP̂_j − 1{j∈S₀}| ≥ ½} holds in both directions of the symmetric difference. Markov's inequality then gives the factor 2.
- **Final clause of STATEMENT §3.** Remark 7 is accurate. No independence between particles is used, only conditional independence of particle i's round-(s+1) randomness from 𝓕_s. The only union bound is over rounds in Lemma 4, not over coordinates.

## Findings

**Finding 1**
- **Location:** Lemma 1 proof (l.79) and the definition of 𝓕_s (l.68).
- **Severity:** exposition.
- **Claim:** The proof says the round's variates are "fresh uniforms from island r's stream, independent of everything drawn before", and that U is independent of 𝓕_s with a law that does not depend on s or i. It does not cover the case where the number of uniforms consumed is random. That happens with state-dependent index choices in swaps, rejection-type draws from π₀, or sequential processing of particles 1,…,i−1 in round s+1. In that case particle i's block starts at a random position in the stream, and 𝓕_s ("randomness used up to the end of round s") is a stopped σ-field.
- **Evidence:** The conclusion still holds. Let (U_n) be the i.i.d. stream and 𝒢_n = σ(𝓒, U_1,…,U_n). Let τ be the index of the last uniform used before the block starts; τ is a stopping time, and 𝓕_s ⊆ 𝒢_τ. For A ∈ 𝒢_τ, P(A ∩ {(U_{τ+1},…) ∈ B}) = Σ_n P(A ∩ {τ=n}) · P((U_{n+1},…) ∈ B) = P(A) · P(B). So the tail block is i.i.d. uniform and independent of 𝓕_s. This repair is local and elementary, but the proof does not state it.

**Finding 2**
- **Location:** Lemma 1 proof (l.79): "Φ (determined by the data and 𝓒)".
- **Severity:** exposition.
- **Claim:** The proof assumes, without pointing to the statement, that every ingredient of the terminal-round kernel (π₀, the swap neighbourhoods, B) is fixed by (data, 𝓒) and does not adapt to the current particle population. If π₀ were fitted from the stage-T particle cloud, the kernel would be 𝓕₀-measurable rather than 𝓒-measurable. Lemma 1 would then fail as written, and BASIN "given 𝓒" would need to be reinterpreted.
- **Evidence:** STATEMENT §1 supports the proof's reading. It describes 𝓒 as "all settings", calls K₁ "the one-round transition kernel" (a single kernel), and says the terminal rounds are "all with the kernel K₁". BASIN is stated "given 𝓒". So within the statement as given the step is valid; it just needs a citation of these clauses.

**Finding 3**
- **Location:** Lemma 2 statement (l.87–90) and Theorem (a) (l.179); the parenthetical of STATEMENT (ii-b).
- **Severity:** exposition.
- **Claim:** When S₀ ∉ Ω, o_l(S₀) is undefined, because STATEMENT §1 defines o_j only for S ∈ Ω. So the right-hand side of (ii-a) is undefined in that case, and the proof adopts a convention ("whatever value in [0,1]"). Two smaller points: the restriction to [0,1] is unnecessary, and the case is written inside the lemma statement after a display that ends with a comma. The parenthetical of (ii-b) ("If S₀ ∉ Ω, u_π = +∞") is never addressed; it implicitly extends π by zero outside Ω.
- **Evidence:** The argument under the convention is correct. Every path state lies in Ω, so B_{i,h} = 1 for all (i,h), hence B̄_r = 1. Then |PIP̂_{rj} − 1{j∈S₀}| ≤ 1 ≤ 1 + |c| for any real value c. No mathematical defect.

**Finding 4**
- **Location:** Lemma 4 statement (l.126): "for every integer H ≥ 0".
- **Severity:** exposition.
- **Claim:** X_H is only defined for 0 ≤ H ≤ L+4, because the terminal rounds stop after L+4 rounds. The range should read 0 ≤ H ≤ L+4.
- **Evidence:** The lemma is only applied with H = L+h−1 ≤ L+3, so nothing downstream is affected.

**Finding 5**
- **Location:** Remark 8 (l.212–214), and the hypothesis list of Lemma 4 (l.126).
- **Severity:** exposition.
- **Claim:** Remark 8 says Lemma 4 uses (B2)–(B3) through their end-of-round consequences (1). In fact Lemma 4's conclusion is written in terms of η̄ and ρ̄, so it uses neither (B2) nor (B3). The comparisons η̄ ≤ η and ρ̄ ≤ ρ from (1) are made at l.123 and used in Lemma 5 (l.172).
- **Evidence:** The proof of Lemma 4 (l.145–157) invokes only Lemma 1, (B1), and the definitions of η̄ and ρ̄. The extra hypotheses are harmless.

**Finding 6**
- **Location:** Lemma 2 and Theorem (a) (l.84–91, l.179); the notation throughout §§1–4.
- **Severity:** exposition.
- **Claim:** (i) STATEMENT §2 says (ii-a) uses EX-A, but Lemma 2 and Theorem (a) do not list it. Exactness is instead built into the definition at l.40 ("it records o_j(X^(k−1))"). (ii) The island index r is suppressed in X_{i,s}, S_{i,h,j}, B_{i,h} and 𝓕_s, even though (B4) and Theorem (c) quantify over islands.
- **Evidence:** (i) matches STATEMENT's own definition of PIP̂_{rj} through exact o_j, so the conclusions are unchanged. (ii) is clear from "Fix an island r" (l.68, l.122).

## Summary

The proof proves exactly (ii-a)–(ii-d) under exactly the hypotheses of STATEMENT.md, with the same constant 𝓑_n. I found no fatal error and no gap. The probabilistic conditioning step (Lemma 1) and the round counts (H = L+h−1, the (L+3)η + (L+4)ρ split, and ⌊L/r₀⌋) are correct. All six findings are exposition-level; the only one that needs a short added argument is Finding 1 (the stopping-time step).

VERDICT: verified
