# Statement checker reply, round 1 (Opus 5.5 xhigh, CP; ruled on the p=1 version of (T)(b))

# STATEMENT_CHECK_R1: T01 and T02 (wave 3)

I'm returning this inline because I'm in read-only mode and can't write `review\STATEMENT_CHECK_R1.md`. I read only the five listed files and skipped the proof-route hints. No FAILED_ATTEMPTS.md exists for this run. I ran no commands. Every check below was done by hand.

## 0. Hand checks (the evidence behind the rulings)

**E1. T01(i).**
- Both y and X_Sβ lie in 1^⊥. Uᵀ is an isometry on 1^⊥ and Uᵀy = y_c/s_y. So ‖y − X_Sβ‖² = ‖y_c − X_{c,S}θ‖²/s_y².
- Substitute β = θ/s_y and σ² = v/s_y², with Jacobian s_y^{−k−2}. Each factor of the v3 joint density changes as follows:
  - the likelihood becomes (2π)^{−n/2} s_y^n v^{−n/2} e^{−‖y_c−X_{c,S}θ‖²/(2v)};
  - the β-prior becomes s_y^k N_k(θ; 0, nv(G_S+I)⁻¹);
  - the IG(0.01, b₀) density becomes s_y^{2.02} b₀^{0.01}Γ(0.01)⁻¹ v^{−1.01} e^{−b₀s_y²/v}.
- The power of v is v^{−n/2−1.01}. The contrast joint at b = b₀s_y² has the same power, v^{−(n−1)/2−1.51}. So the two joints differ by a factor free of (S, θ, v), and the posteriors coincide.
- Integrating out (Woodbury gives det(I + nX_{c,S}(G_S+I)⁻¹X_{c,S}ᵀ) = D_S):
  m^c_b(S) = 2^ν(2π)^{−(n−1)/2} Γ(ν) b^{0.51}/Γ(0.51) · D_S^{−1/2}(2b + Q^c_S)^{−ν}, with ν = 0.51 + (n−1)/2 = 0.01 + n/2.
- z^c_S = X_SᵀUUᵀy^r = X_SᵀCy^r = s_y z_S, and y_cᵀy_c = s_y² yᵀy. Hence Q^c_S = s_y²Q_S and 2b₀s_y² + Q^c_S = s_y²(2b₀ + Q_S).
- The ratio m/m^c then has 2-power 2^{−1/2}, π-power π^{−1/2} and b₀-power b₀^{−1/2}, so it equals s_y^{n−1}Γ(0.51)/(√(2πb₀)Γ(0.01)) = c_n(s_y).
- The θ-precision is H_S/(nv) and the posterior mean is nH_S⁻¹z^c_S. The v-posterior is IG(ν, b + Q^c_S/2).
- Every clause of (i) checks.

**E2. T01(ii).**
- Pointwise in (S, θ, v): IG(v; 0.51, b)/IG(v; 0.51, b₋) = (b/b₋)^{0.51}e^{−(b−b₋)/v} ≤ κ.
- Also: IG(v; 0.51, b)/IG(v; 0.51, b₊) = (b/b₊)^{0.51}e^{(b₊−b)/v} ≥ κ⁻¹.
- So both inequalities hold for every E, every S and every y_c, including y_c = 0.
- Side remark: the exact factors give Π_b(E) ≤ (b/b₋)^{0.51}(b₊/b)^{0.51} I_{b₋}(E)/Z^c_{b₊} = κ I_{b₋}(E)/Z^c_{b₊}. So κ² is true but loose by one factor of κ. No change is needed, since κ² is the original's constant.

**E3. T01(iv).** log m^c_b(S) = c_S + 0.51 log b − ν log(2b + Q^c_S). Differencing the b-derivatives for S and S′ gives the stated formula. The denominators are positive because Q^c ≥ 0.

**E4. T01(iii).**
- s_y² = (‖μ‖² + 2μᵀε + ‖Cε‖²)/(n−1), where ‖Cε‖²/σ*² ~ χ²_{n−1}.
- The cross term has sd 2σ*‖μ‖/(n−1) ≤ 2σ*√(Mn)/(n−1).
- The centring lies in [σ*², σ*² + 3M/2] for n ≥ 3. That is strictly inside [σ*²/2, 2(σ*²+M)+1], so P₀(𝓑_n) → 1.
- Uᵀ1 = 0 and UᵀX^rβ* = Uᵀμ = X_cθ*, so y_c = X_cθ* + Uᵀε holds.

**E5. (T)(b), p = 1 witness.**
- Setup: Ω = {∅, {1}}, w(0) = w(1) = ½ (prior odds 1), G = n−1, H = n², D_{1} = n.
- With T = ‖y_c‖², z = x_cᵀy_c and Δ = z²/n, we get Q^c_{1} = T − Δ and
  log[m^c_r({1})/m^c_r(∅)] = −½ log n − ν log(1 − Δ/(2r+T)).
- Take T = t > 0 fixed and Δ = a log n/n with a = r₁ + r₂ + t. This is feasible because Δ ≤ (n−1)t/n.
- Then the log Bayes factor is ½ log n·(a/(2r+t) − 1) + o(1). It tends to +∞ at r₁ and −∞ at r₂.
- So the first sentence of (b) is true. On these inputs s_y² = t/(n−1) → 0.

**E6. Every p = 1 flip witness lies outside 𝓑_n.**
- Write q = Q^c_{1}, Δ = T − q and x_r = Δ/(2r+q). Then log BF_r = −½ log n + ν log(1 + x_r).
- log BF_{r₂} → −∞ forces x_{r₂} ≤ (1+o(1)) log n/n.
- Then log BF_{r₁} − log BF_{r₂} ≤ ν(x_{r₁} − x_{r₂}) = ν x_{r₂}·2(r₂−r₁)/(2r₁+q) ≤ (1+o(1))(r₂−r₁) log n/(2r₁+q).
- That difference must tend to ∞, which forces q = o(log n). Then T = q + Δ = o(log n), and s_y² = o(log n/n) → 0, which is below σ*²/2 for large n.

**E7. Witnesses inside 𝓑_n (p = 2, model events).**
- Fix σ*² > 0 and M ≥ 0, and let b* = b₀σ*², which lies in (b₋, b₊).
- Take orthonormal u₁, u₂, u₃ in ℝ^{n−1}, x_{c,j} = √(n−1)u_j for j = 1, 2, and y_c = αu₁ + βu₂ + u₃, with β²(1−1/n) = a log n/n and α² = (n−1)σ*² − β² − 1.
- Then s_y² = σ*² exactly, so the input is in 𝓑_n and the data rate is b*. Also D_{1} = n, D_{12} = n², ϖ({1}) = ϖ({1,2}), Q^c_{1} → q := σ*² + 1, and Q^c_{12} = Q^c_{1} − a log n/n.
- Q^c_{2} and Q^c_∅ are about nσ*², so {1} and {1,2} beat ∅ and {2} by log-margins of order n log n at every rate in [b₋, b₊].
- log[m^c_b({1,2})/m^c_b({1})] = ½ log n·(a/(2b+q) − 1) + o(log n).
- With a ∈ (2b*+q, 2b₊+q): Π_{b₊}(S = {1,2}) → 0, while Π(S = {1,2} | y) → 1 by (i).
- With a ∈ (2b₋+q, 2b*+q): Π_{b₋}(S = {1}) → 0, while Π(S = {1} | y) → 1.
- Joint-endpoint version: use p = 3, orthogonal columns, increment for x₂ in (2b*+q, 2b₊+q) and for x₃ in (2b₋+q, 2b*+q). Then {1,2} wins only at b*. Alternatively use p = 1 with a v-window event, since v | S ~ IG(ν, b + Q^c_S/2).

**E8. Sketch only, not a proof: a P₀ version of the negative clause would be false for model events.**
1. nX_{c,S}H_S⁻¹X_{c,S}ᵀ ⪯ P_{X_{c,S}}, because its eigenvalues are nλ/((n+1)λ+1) < 1. Hence Q^c_S ≥ ‖(I − P_{S∪S₀})ε_c‖².
2. A union bound over |S| ≤ m_n (log count O(log² n) = o(n)) gives min_{|S|≤m_n} Q^c_S ≥ σ*²n/2 with P₀-probability → 1.
3. By (iv)-type differentiation, |∂_b log m^c_b(S)| ≤ 0.51/b₋ + 2ν/Q^c_S = O(1) for those S.
4. So Π(𝒜 | y) ≤ C·Π_{b₋}(𝒜)/(1 − Π_{b₋}(|S| > m_n)) for every model event 𝒜, with C fixed.
5. The last factor tends to 1 by the same Markov argument as T02(i), run at rate b₋.

So under G and R, a same-rate b₋ bound does transfer with probability → 1, at a cost bounded in n (not κ²). The negative clause is therefore true only as a worst case over inputs.

**E9. T02.**
- The equality-defined Θ_{n,m} is the smallest Θ satisfying the original inequality, and the prefactor is positive. So "some Θ satisfies ≤ and is tight" is equivalent to "the equality Θ is tight".
- 2^{−m_n(ω)} ≤ (2p)^{−s₀}n^{−(s₀+1)/2}e^{−ω}, so the prefactor at m_n(ω_n) is at most (4/3)^{s₀/2}e^{−ω_n}. This gives the "Consequently" clause.
- ϖ(|S|>m) ≤ 2^{1−m} and 1/ϖ(S₀) ≤ 3(2p)^{s₀}/s₀!. This matches the prefactor.
- For (ii), a heuristic gives a rate of order √(log n/n) = r_n: prior ratio (s₀+1)/(2p−1−s₀), Occam factor about n^{−1/2}, and a truncated mean of e^{Z²/2} of order √(log p).
- I found no counterexample to either part. The heuristic is only an order-of-magnitude check.

## 1. Rulings on items 1–8

1. **Approved.** This is a pure renaming, and (iv) holds for every pair of models (E3).

2. **Approved, subject to change C3.**
   - The reading matches 00_COMMON ("Contrast-scale parameters θ = s_yβ, v = s_y²σ²") and the original (i). The identity is verified (E1), and the plug-in reading of Π_{b₀s_y²} is correct.
   - The objects in (i), (ii), (iv) and (T)(a) do not depend on U, because ‖y_c − X_{c,S}θ‖ = ‖Cy^r − X_Sθ‖.
   - The exact law of ε_c in (iii) does depend on U (see §3).

3. **Approved.**
   - It matches "nonnegative joint numerator integrals I_b(E) over parameter events E", with ϖ included. The envelope holds pointwise (E2).
   - Optional: the same argument covers ∫f·(joint) for any nonnegative measurable f that does not depend on b.

4. **Approved.**
   - b₋ and b₊ are b₀ times the endpoints, and κ = (2(2(σ*²+M)+1)/σ*²)^{0.51} is a fixed constant.
   - Minor point 1: in (ii), b₋, b₊ and κ are generic numbers, but in §1 and (T) they are specific constants. Use different letters in (ii).
   - Minor point 2: the word "fixed" in (ii) is unnecessary because the statement is pointwise in b and y_c. Under §1's convention it also misreads (T)(a), which applies (ii) at the data-dependent b = b₀s_y². That use is legitimate.

5. **(a) approved; (b) rejected as written; the Gaussian-discipline clause approved with a wording note.**
   - **(a).** On 𝓑_n, b₀s_y² lies in [b₋, b₊]. (i) and (ii) give the first inequality, and Z^c_{b₊} ≥ ϖ(S₀)m^c_{b₊}(S₀) gives the second. The "Consequently" clause uses only P₀(𝓑_n) → 1 and the unconditional P₀. This is faithful to the original's positive content.
   - **(b).** The first two sentences are true (E5). The final "in particular … on 𝓑_n" clause is the only part that speaks about "the event of (iii)", and it does not follow from them. Every p = 1 flip witness has s_y² → 0 (E6), so it lies outside 𝓑_n and its data rate is outside [b₋, b₊].
     - The clause itself is true (E7), so this is a gap in the logic, not a false claim.
     - It must be a worst case over inputs, because a P₀ reading is false for model events (E8). As written, "does not bound Π(E | y) on 𝓑_n" is ambiguous between the two readings.
   - **Your question.** Yes, the negative statement needs a different form. It should be a worst-case statement witnessed by inputs inside 𝓑_n; proposed text is in C1.
   - **Discipline clause.** The original reads "Errors are never treated as Gaussian conditional on s_y". STATEMENT reads "the proofs never use a conditional law of ε given s_y".
     - STATEMENT's version is stricter. It would forbid correct conditional arguments: for example, with μ = 0, Cε/‖Cε‖ is uniform and independent of ‖Cε‖.
     - Suggested wording: "the proofs never treat ε or ε_c as N(0, σ*²I) conditionally on s_y or on 𝓑_n". This is not blocking.

6. **Approved.**
   - Defining Θ by equality is equivalent to the original (E9), and the quantifier order lim_L limsup_n sup_m P₀ matches.
   - Negative m and m ≥ K are trivial cases.
   - "S₀ ∈ Ω for large n" is in R ("eventually s₀ ≤ K").
   - "Not claimed: tight sup_m inside P₀" matches the original.

7. **Approved.** 00_COMMON §1 says "m_n := m_n(½ log n)", and SE is copied verbatim. The superset reading is the natural one.

8. **Approved.** This matches 00_COMMON §1 ("P₀ is over ε") and G ("Fixed design"). Since C1 = 0 and Uᵀ1 = 0, nothing depends on α*, even if α* depends on n.

## 2. Misstatements (both texts quoted)

- **M1, (T)(b).**
  - Original: "a target bound holds for v3 on the event of (iii) at multiplicative cost κ² only in the mixed-endpoint form (numerator sums at b₋, S₀-denominator at b₊); same-rate bounds alone do not establish it."
  - STATEMENT: "For any fixed rates 0 < r₁ < r₂ there are valid inputs (n → ∞, p = 1) … Hence … in particular a bound on Π_{b₋}(E) or on Π_{b₊}(E) alone does not bound Π(E | y) on 𝓑_n at a cost bounded in n."
  - Problem: the "in particular" does not follow (E6), as explained in item 5.
- **M2, notation.**
  - §1 sets the convention "parameter event E ⊆ ⋃_{S∈Ω} {S} × ℝ^S × (0,∞)". (b) then writes "(so Π_{r₂}(∅) → 1 and Π_{r₁}(∅) → 0)".
  - Under that convention Π of the empty event is 0, so the text is literally false. "{1}" has the same ambiguity.
- **M3, U.**
  - Original texts: 00_COMMON says "U ∈ ℝ^{n×(n−1)}, UᵀU = I, UUᵀ = C", and T01(iii) says "Uᵀε ~ N_{n−1}(0, σ*²I) exactly".
  - STATEMENT says "U … is any matrix with UᵀU = I_{n−1}, UUᵀ = C" and "(all statements hold for each such U)".
  - The original is equally silent, but "any" invites a choice of U that depends on the data (see §3).
- **M4, discipline wording.** Quoted in item 5. It is stricter than the original, but it is not a mathematical claim.

**Readings the change report does not list.** All are acceptable, and should be added to §4 of STATEMENT.md:
- U1. The original defines "z_S^c = s_y z_S; Q_S^c = s_y²Q_S". STATEMENT defines z_S^c = X_{c,S}ᵀy_c and Q^c_S from y_c, then claims the identities as a conclusion.
  - The two agree on every valid input (E1).
  - The direct definition is needed for "every y_c ∈ ℝ^{n−1}" in (ii), because y_c = 0 has no s_y, and for (iv).
- U2. (iii) adds "y_c = X_cθ* + ε_c". This is true (E4).
- U3. R adds "(void if s₀ = 0)".
- U4. The valid input adds "p ≥ 1". This is harmless; for p = 0, (i) is trivial.
- U5. The original says "No eigenvalue condition near the cap is imposed", and STATEMENT says "No eigenvalue condition beyond λ_min(R_{S₀}) ≥ φ₀² is imposed". These are consistent, since only R is assumed.

**Checked and found to agree:**
- the model objects: m(S), ν, a₀ = b₀ = 0.01, w(k), W_K, ϖ, K, Ω, G_S, H_S, D_S, Q_S;
- c_n, the conditionals, κ and the 𝓑_n endpoints;
- r_n, m_n(ω) and m_n;
- the assumptions and regime: SE, R, G, R1.

I did not check "Target (method §5)" against the method file, which was not on my read list.

## 3. Counterexample referee

- **(iii) with a data-dependent U.**
  - Take s₀ = 0, which R permits. Then Cy^r = Cε.
  - Let the first column of U be Cy^r/‖Cy^r‖, completed to an orthonormal basis of 1^⊥.
  - Then (Uᵀε)₁ = ‖Cε‖ > 0 almost surely, which is not N(0, σ*²). The claim "~ N_{n−1}(0, σ*²I) exactly" fails. The fix is C3.
- **"Π_{r₂}(∅) → 1" is literally false** under §1's event convention. The fix is C2.
- **No counterexample to any substantive claim.**
  - All algebra in T01 (i)–(iv) and (T)(a) checks (E1–E4).
  - (T)(b) is true, including its 𝓑_n clause (E7), but that clause lacks a supporting witness.
  - For T02(i)–(ii) I found none (E9).

## 4. Overall verdict: **changes required**

**C1. Replace (T)(b) with:**

> (b) *Same-rate bounds do not transfer (worst case over inputs).* (b1) For fixed 0 < r₁ < r₂ there are valid inputs (n → ∞, p = 1) with Π_{r₁}({S = {1}}) → 1 and Π_{r₂}({S = {1}}) → 0. Hence for distinct fixed rates b, b′ there is no function g with g(x) → 0 as x ↓ 0, independent of n and the data, such that Π_{b′}(E) ≤ g(Π_b(E)) for all valid inputs and E. (b2) Fix σ*² > 0, M ≥ 0 and b₋ < b₊ as in §1. There are valid inputs (n → ∞, p = 2) in 𝓑_n and model events E_n, E′_n with Π_{b₋}(E_n) → 0 but Π(E_n | y) → 1, and Π_{b₊}(E′_n) → 0 but Π(E′_n | y) → 1. So for b ∈ {b₋, b₊} no constant C independent of n gives Π(E | y) ≤ C·Π_b(E) for all inputs in 𝓑_n and all E. This is not a claim about P₀ under G and R.

   Optional (b3): the same with I_b(E)/(ϖ(S₀)m^c_b(S₀)) for a designated S₀, and with the b₋ and b₊ bounds held jointly (E7). This is a closer match to "only".

**C2.** In (b), write model events as {S = ∅} and {S = {1}}.

**C3.** In §1 and §4.2, require U to be fixed: non-random, for example a function of n only.

**Recommended, not blocking:**
- Use different letters in (ii) and drop the word "fixed" there (item 4).
- Reword the proof-discipline clause (item 5).
- Record U1–U5 in §4.
- Optionally extend I_b to nonnegative integrands (item 3).
- Optionally note that κ suffices in place of κ² (E2).

### Critical Files for Implementation
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\proofs\T01_T02_contrast_dimension\STATEMENT.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\theorems\T01_A0_contrast_reduction.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\theorems\T02_A1_dimension_supersets.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\theorems\00_COMMON.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\proofs\T01_T02_contrast_dimension\review\STATEMENT_CHECK_REQUEST.md