# Statement checker reply, round 1b (on the intermediate p=2 version of (T)(b))

# STATEMENT_CHECK_R1 (revised): T01 and T02 (wave 3)

I need to send one more change back. The new (T)(b) fixes the earlier gap, and both of its existence claims are true; I built the inputs by hand (E5). But its last clause is false as written: "not even up to a factor that is allowed to grow with n". A data-free factor that grows with n always works (E6). That sentence needs to be cut back to "no factor independent of n". The fixed-U precision from my first reply (C3) is also still open. Overall: **changes required**, both small.

I re-read STATEMENT.md and STATEMENT_CHECK_REQUEST.md after your update; this reply replaces my earlier one. Only (T)(b) and change item 5 differ; everything else is word for word the same. Two consequences:
- The notation issue from before (Π(∅), "{1}") is fixed by the new wording.
- My earlier objection about the p = 1 inputs lying outside 𝓑_n no longer applies.

I'm read-only, so I'm returning this inline rather than writing `review\STATEMENT_CHECK_R1.md`. I read only the listed files, skipped the proof-route hints, and ran nothing.

## 0. Hand checks

**E1. T01(i).**
- Substitute β = θ/s_y and σ² = v/s_y² (Jacobian s_y^{−k−2}). Use ‖y − X_Sβ‖² = ‖y_c − X_{c,S}θ‖²/s_y², which holds because Uᵀ is an isometry on 1^⊥.
- The v3 joint and the contrast joint at b = b₀s_y² then have the same power of v, v^{−n/2−1.01}. So they differ only by a factor free of (S, θ, v), and the posteriors coincide.
- m^c_b(S) = 2^ν(2π)^{−(n−1)/2}Γ(ν)b^{0.51}Γ(0.51)⁻¹ D_S^{−1/2}(2b+Q^c_S)^{−ν}.
- With z^c_S = s_y z_S and Q^c_S = s_y²Q_S, the ratio m/m^c equals c_n(s_y).
- The stated conditionals check.

**E2. T01(ii).**
- Pointwise: IG_b/IG_{b₋} = (b/b₋)^{0.51}e^{−(b−b₋)/v} ≤ κ, and IG_b/IG_{b₊} ≥ κ⁻¹.
- Combining the exact factors gives Π_b(E) ≤ κ·I_{b₋}(E)/Z^c_{b₊}. So the stated κ² is true but loose; no change is needed.

**E3. T01(iv).** It follows directly from log m^c_b(S) = c_S + 0.51 log b − ν log(2b + Q^c_S).

**E4. T01(iii).**
- s_y² = (‖μ‖² + 2μᵀε + ‖Cε‖²)/(n−1).
- The centring lies in [σ*², σ*² + 3M/2], strictly inside the 𝓑_n endpoints.
- y_c = X_cθ* + Uᵀε. The exact Gaussian law of Uᵀε needs U non-random (see C3).

**E5. The two existence claims of the new (T)(b) are true.**
- Construction. Take any n ≥ 4, so that K = 2. Pick orthonormal u₁, u₂ in ℝ^{n−1} and set:
  - x_{c,j} = √(n−1)u_j for j = 1, 2;
  - y_c = αu₁ + βu₂, with β² = a log n/(n−1) and α² = (n−1)s² − β².
- The raw data are y^r = Uy_c and x^r_j = Ux_{c,j}. These are valid inputs with s_y² = s² exactly. Write b* = b₀s², which is strictly between b₋ and b₊.
- Then:
  - D_{1} = n, D_{12} = n², and ϖ({1}) = ϖ({1,2}) = 1/6;
  - Q^c_{12} = (n−1)s²/n and Q^c_{1} = Q^c_{12} + a log n/n;
  - Q^c_{2} and Q^c_∅ are about (n−1)s².
- {1} and {1,2} beat ∅ and {2} by log-margins of order n log n at every rate in [b₋, b₊], and
  log[m^c_b({1,2})/m^c_b({1})] = ½ log n·(a/(2b + s²) − 1) + o(1).
- Choosing a in (2b₋ + s², 2b* + s²) gives Π_{b₋}(S = {1}) → 0 and Π(S = {1} | y) → 1, using (i).
- Choosing a in (2b* + s², 2b₊ + s²) gives Π_{b₊}(S = {1,2}) → 0 and Π(S = {1,2} | y) → 1.
- For the finitely many small n where α² < 0, any valid input with s_y² = s² will do, since the claims are limits.

**E6. The last clause of (T)(b) is false.**
- Let C_n := (b₊/b₋)^ν with ν = 0.01 + n/2. This factor depends only on n, σ*² and M.
- b₋ side, every measurable parameter event E, on 𝓑_n:
  - I_b(E) ≤ (b/b₋)^{0.51}·I_{b₋}(E), pointwise.
  - m^c_b(S)/m^c_{b₋}(S) = (b/b₋)^{0.51}·((2b₋+Q)/(2b+Q))^ν ≥ (b₋/b)^{ν−0.51}, because Q ≥ 0.
  - So Z^c_b ≥ (b₋/b)^{ν−0.51}·Z^c_{b₋}, and therefore Π(E | y) ≤ (b/b₋)^ν·Π_{b₋}(E) ≤ C_n·Π_{b₋}(E).
- b₊ side, every model event 𝒜, on 𝓑_n (E′ = {S = {1,2}} is one):
  - m^c_b(S)/m^c_{b₊}(S) ≤ (b₊/b)^{ν−0.51}, and Z^c_b ≥ (b/b₊)^{0.51}·Z^c_{b₊}.
  - Therefore Π(𝒜 | y) ≤ (b₊/b)^ν·Π_{b₊}(𝒜) ≤ C_n·Π_{b₊}(𝒜).
- So a factor that grows with n does bound Π(E | y) in both cases the witnesses cover.
- On the E5 inputs the ratio Π(E | y)/Π_{b₋}(E) grows only like a power of n. Those inputs therefore rule out bounded factors only.
- Optional sharper fact:
  - The best data-free factor really is exponential in n. Take p = 1 with y_c = αu₁ + γu₂ and γ² fixed. Then Π(∅ | y)/Π_{b₋}(∅) ≍ ((2b*+q)/(2b₋+q))^{n/2}, with q = s² + γ².
  - On the b₊ side, events that restrict v to (0, η) make the ratio unbounded even for fixed n. That is because IG_b/IG_{b₊} ≥ (b/b₊)^{0.51}e^{(b₊−b)/η}.
  - Neither fact is needed for the fix.

**E7. Sketch, not a proof: a P₀ version of (b) would be false.**
- Under G and R, Q^c_S ≥ ‖(I − P_{S∪S₀})ε_c‖² ≥ σ*²n/2 for all |S| ≤ m_n, with P₀-probability → 1.
- Then (iv) gives Π(𝒜 | y) ≤ C·Π_{b₋}(𝒜)/(1 − Π_{b₋}(|S| > m_n)) for model events 𝒜, with C fixed.
- So (b) holds only as a worst case over inputs, not as a statement about probability under the model.

**E8. T02.**
- Defining Θ by equality is equivalent to the original inequality-plus-tightness. The prefactor matches the prior: ϖ(|S|>m) ≤ 2^{1−m} and 1/ϖ(S₀) ≤ 3(2p)^{s₀}/s₀!.
- At m = m_n(ω_n) the prefactor is at most (4/3)^{s₀/2}e^{−ω_n}, which gives the "Consequently" clause.
- A heuristic gives a rate of order √(log n/n) for (ii), matching r_n.
- I found no counterexample to either part.

## 1. Rulings on items 1–8

1. **Approved.** Renaming only; (iv) holds for every pair of models (E3).

2. **Approved, subject to C3.** The reading matches 00_COMMON ("θ = s_yβ, v = s_y²σ²"), and the identity checks (E1). Everything except the law of ε_c in (iii) is unaffected by the choice of U.

3. **Approved.** It matches "nonnegative joint numerator integrals I_b(E) over parameter events E" (E2).

4. **Approved.** Minor point: b₋, b₊ and κ are generic numbers in (ii) but fixed constants in §1 and (T). Use other letters in (ii) and drop "fixed" there; (T)(a) applies (ii) at b = b₀s_y², which is legitimate.

5. **(a) approved; new (b) rejected as written (one sentence); proof-discipline clause approved with a wording note.**
   - **(a)** is faithful to "holds … at multiplicative cost κ² … in the mixed-endpoint form".
   - **(b), the two existence claims: approved.**
     - Both are true (E5).
     - They sit on 𝓑_n itself, as "on the event of (iii)" requires.
     - The strict-interior condition on s² and n ≥ 4 (so that K = 2) are both needed.
     - The notation is now correct.
   - **(b), "Hence … not even up to a factor that is allowed to grow with n": rejected.** It is false (E6). What the witnesses do show is that no factor independent of n works, and no data-free g with g(x) → 0 as x → 0 works either.
   - **Your question.** With that sentence fixed, (a) + (b) is a faithful precise form. Ruling out every constant factor, rather than just κ², is the natural reading of "same-rate bounds alone do not establish it".
   - **Optional strengthening.** Cover the same-rate S₀-denominator form I_b(E)/(ϖ(S₀)m^c_b(S₀)), and bounds at b₋ and b₊ held jointly. These come from the same kind of construction: p = 3 with orthogonal columns, or p = 1 with an event restricting v.
   - **Discipline clause.** The original reads "Errors are never treated as Gaussian conditional on s_y". STATEMENT's "the proofs never use a conditional law of ε given s_y" is stricter, and would forbid correct conditional arguments. Suggested wording: "never treat ε or ε_c as N(0, σ*²I) conditionally on s_y or on 𝓑_n". Not blocking.

6. **Approved.**
   - Defining Θ by equality is equivalent to the original (E8).
   - The quantifier order lim_L limsup_n sup_m P₀ is kept.
   - "S₀ ∈ Ω for large n" comes from R.

7. **Approved.** 00_COMMON §1 says "m_n := m_n(½ log n)"; SE is copied word for word.

8. **Approved.** Since C1 = 0 and Uᵀ1 = 0, nothing depends on α*. P₀ is over ε with the design fixed, as in G.

## 2. Misstatements (both texts quoted)

- **M1, the last clause of (T)(b).**
  - Original: "same-rate bounds alone do not establish it" (where "it" is the bound "at multiplicative cost κ²").
  - STATEMENT: "does not bound Π(E | y) on 𝓑_n, not even up to a factor that is allowed to grow with n."
  - This goes beyond the original and is false (E6).
- **M2, the choice of U.**
  - 00_COMMON: "U ∈ ℝ^{n×(n−1)}, UᵀU = I, UUᵀ = C". T01(iii): "Uᵀε ~ N_{n−1}(0, σ*²I) exactly".
  - STATEMENT: "U … is any matrix with …" and "(all statements hold for each such U)".
  - The word "any" invites a choice of U that depends on the data, under which (iii) fails (§3).
- **M3, §4.4.** It still describes (b) as "a counterexample to any data-free same-rate implication". That describes the old version and should be updated to match the new (b).
- **M4, discipline wording.** See item 5. This is not a mathematical claim.

**Readings the change report doesn't list.** All acceptable; record them in §4:
- z^c and Q^c are defined from y_c, then claimed equal to s_y z_S and s_y²Q_S. The original states the latter as definitions.
- (iii) adds "y_c = X_cθ* + ε_c", which is true.
- R adds "(void if s₀ = 0)".
- The valid-input definition adds "p ≥ 1".
- The T02(i) remark says "No eigenvalue condition beyond λ_min(R_{S₀}) ≥ φ₀²", where the original says "No eigenvalue condition near the cap is imposed".

**Checked and in agreement:**
- the model objects: m(S), ν, a₀ = b₀ = 0.01, w(k), W_K, ϖ, K, Ω, G_S, H_S, D_S, Q_S;
- c_n, the conditionals, κ and the 𝓑_n endpoints;
- r_n, m_n(ω) and m_n;
- the assumptions and regime: SE, R, G, R1.

I did not check "Target (method §5)" against the method file, which wasn't on my read list.

## 3. Counterexample referee

- **New (T)(b), last clause.**
  - The data-free factor C_n = (b₊/b₋)^{0.01+n/2} gives Π(E | y) ≤ C_n·Π_{b₋}(E) for every valid input in 𝓑_n and every E.
  - It also gives Π(𝒜 | y) ≤ C_n·Π_{b₊}(𝒜) for every model event 𝒜.
  - This contradicts "not even up to a factor that is allowed to grow with n".
- **(iii), if U may depend on the data.**
  - Take s₀ = 0, which R allows, and let the first column of U be Cy^r/‖Cy^r‖.
  - Then (Uᵀε)₁ = ‖Cε‖ > 0 almost surely, which is not N(0, σ*²).
- **No other counterexamples.** The existence claims in (b) are true (E5); T01(i)–(iv) and (T)(a) check (E1–E4); none found for T02.

## 4. Overall verdict: **changes required**

**C1′.** In (T)(b), replace the "Hence" sentence with:

> "Hence for b ∈ {b₋, b₊} there is no constant C, independent of n and the data, with Π(E | y) ≤ C·Π_b(E) for all valid inputs in 𝓑_n and all E. Equivalently, no data-free g with g(x) → 0 as x ↓ 0 gives Π(E | y) ≤ g(Π_b(E)) on 𝓑_n. This is a worst case over inputs, not a P₀ statement."

You could optionally add the true remark from E6: the factor (b₊/b₋)^ν does suffice, for all E on the b₋ side and for model events on the b₊ side.

**C3 (still open).** In §1 and §4.2, state that U is fixed (non-random, for example depending on n only).

The earlier notation issue is resolved by the revision.

**Recommended, not blocking:**
- Update §4.4 to describe the new (b).
- Use other letters in (ii) and drop "fixed" there.
- Reword the proof-discipline clause.
- Record the unlisted readings from §2 in §4.
- Optionally extend I_b to nonnegative integrands, and note that κ suffices in place of κ².

### Critical Files for Implementation
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\proofs\T01_T02_contrast_dimension\STATEMENT.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\proofs\T01_T02_contrast_dimension\review\STATEMENT_CHECK_REQUEST.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\theorems\T01_A0_contrast_reduction.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\theorems\T02_A1_dimension_supersets.md
- <OLD_ROOT>\01_Methodology_and_Theory\Theory_architecture_v3\theorems\00_COMMON.md