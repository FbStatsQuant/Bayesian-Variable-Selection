MANIFEST b643f323a2ac2948975e3f01e54d30c0e64cf6643eebe911d1475fac270c3dc6

# LC2-C — line check of `lemmas/L6_examples.md` (claim (C5)), seat Claude Opus 5.5 (high), blind first read

Files read: only files in the manifest (the ticket folder without `reviews/`, `LOG.md` or `CHECKPOINT*.md`, plus the
external inputs of `reviews/INPUTS.txt`). Of the `reviews/` folder I read only this brief, the manifest and INPUTS.txt.
The sha256 of `lemmas/L6_examples.md`, `STATEMENT.md`, `lemmas/L2_width.md`, `L3_assemblyF.md`, `L4_sandR_b.md`,
`L5_formR.md`, `numerics/formR_checks.R` and `formR_checks_out.txt` were recomputed and match the manifest.
L2, L3, L4 and L5 were taken as given, as the brief says. Lemmas BC and IR of POLY were checked only for whether they
are applied within their hypotheses.

## Verdict per lemma/claim

| claim | verdict |
|---|---|
| §0 (BC/IR uniform estimates, refitting identity (0.1), variance bound (0.2)) | VERIFIED |
| E1 (inherited examples, by containment) | VERIFIED-WITH-AMENDMENTS (finding 4, a NIT) |
| E2 (Gaussian rows, polynomial decay, α > 2, RM2-R) | VERIFIED-WITH-AMENDMENTS (finding 3: the status line should name its BC/IR conditions) |
| E3 (exact Gram, polynomial decay, α > 2, RM2-F) | VERIFIED-WITH-AMENDMENTS (finding 3) |
| E4 (one truth, n^b weak proxies, every b < ½) | VERIFIED |
| E5 (equicorrelated group, b < 3/10) | VERIFIED; the stated range is correct but not sharp (finding 1) |
| Examples table and status lines | VERIFIED-WITH-AMENDMENTS (findings 2, 3) |

No statement falls. No FATAL or MAJOR finding. Every status in the file is at most "PROVED (by this seat, unchecked)".
The only "NOT VERIFIED" row (E5 for 3/10 ≤ b < ½) is an honest non-claim.

## Findings

**1. MINOR (sharpness, not correctness): E5's range 0 < b < 3/10 can be extended to b < 3/8, and 3/8 looks like the
true (W) threshold for this construction.** L6:441-453, table L6:465-466, STATEMENT.md:256 and :314.
The proof compares the crude bound (5.1), 2 max_{j≤q}|g_j|, with the *smallest* level a⁰_n(q) ≈ √((3 − 2b) log n). That
bound is close to tight only when |T| is small, and for small |T| the level is ≈ √(3 log n), not √((3 − 2b) log n).
Sketch (my derivation; not written to proof standard):
* *Upper bound.* For a within-group pair with |T| = t: |u_{T,l}ᵀg| ≤ C_a|g₀| + |g_l| + tA_t·m_t, where m_t := mean of
  the t largest |g_j|, j ≤ q, and tA_t ≤ 1. A Chernoff bound over subsets gives E m_t ≤ √(2 log(2eq/t)). m_t is
  t^{−1/2}-Lipschitz, so a union over t ≤ q gives, with probability ≥ 1 − 1/log n,
  m_t ≤ √(2 log(2eq/t)) + √(2 log(q log n)/t) for all t. The extra term is O(1) for t ≥ log n. For t < log n use
  m_t ≤ max|g_j| instead.
  For t < log n the width exceeds the level by at most (√(8b) − √3 + o(1))√log n.
  For t = n^{x}, 0 < x ≤ b, the excess is at most [√(2b) + √(2(b − x)) − √(3 − 2x)]√log n + O(1).
  The bracket is decreasing in x, because 2(b − x) < 3 − 2x, so its supremum is √(8b) − √3 at x = 0.
  Outside pairs need only b < ½, exactly as in the file.
  So Φ ≤ −c√log n with probability ≥ ½ when b < 3/8, and Gaussian concentration (as in Lemma P9 of L5) gives
  𝔴⁰_n → −∞, which is (W) directly, not through (W-unif).
* *Lower bound.* Take l the index of max_{j≥2} g_j and T = {1} ∪ {the t − 1 most negative g_j}, with t → ∞ slowly. Then
  the coefficient (t − 1)A_t → 1, the normaliser √((1 − a)/v_t) → 1 and
  |u_{T,l}ᵀg| ≥ (2 − o(1))√(2b log n), while a⁰_n(t) = √(3 log n − O(log t)).
  So 𝔴⁰_n → +∞ for b > 3/8, and by Lemma W-conv, NA(𝓛) fails with probability → 1.
My numerical check (scratch script, outside the worktree) computes the exact within-group maximum, which is separable
in (l, T). Its ratio to √(2 log q) is 1.42, 1.49 and 1.60 at q = 2·10², 2·10³ and 2·10⁴, increasing slowly towards 2
as the sketch predicts.
*Correction (optional, for the lead):* either prove the range b < 3/8 by the size-dependent comparison above, or keep
3/10 and record in SHARPNESS/(C6) that the width threshold of this construction appears to be b = 3/8 (sketch: (W) holds
below it and fails above it, so the route fails for 3/8 < b < ½). Either way, the "NOT VERIFIED for 3/10 ≤ b < ½" row
should no longer suggest that b < ½ is a live candidate.

**2. MINOR (record): the citations of RM2 `STATEMENT.md` point to an earlier version, and one status is misquoted.**
* L6:474 quotes `STATEMENT.md:4` as "v1.3 (target statement — nothing in it is proved yet)". That text is not in the
  frozen STATEMENT.md. Line 4 reads "Status of this file: **v1.4** = v1.3 with the Form R leak hypothesis (L-R^b)
  weakened …".
* L6:21: "17/2 language still present in RM2 `STATEMENT.md:250` and `:301`" is stale. In v1.4 the only mention is :259
  ("the class of W2-LOC2:Thm-Poly, which needs α > 17/2"), which is accurate context, not old verification language.
* L6:9 `:40` (§1 is :45-71); L6:23-24 `:174` and `:199` (the (D-loc^b) ⇒ (D-R^b) ⇒ (W-R) chain is :183-191, (C2) is
  :205-207); L6:128 `:220` ((C4) is :225-229); L6:476 `:276-282` (§5 is :277-298; the verbatim quotes are at :285-289).
*Correction:* update to the v1.4 line numbers above, quote line 4 verbatim, and delete or rewrite the sentence at
L6:20-22.

**3. MINOR (status carrying): the E2 and E3 status lines and table rows do not name their Lemma BC/IR conditions.**
L6:155, :253, :462-463. STATEMENT.md:294-297 says Lemma-IR and Lemma BC "are consumed as stated by the examples (C5)
only (E2, E3 …), which carry their status." L6 carries this only in the global sentence L6:6-7 and in the sources list
(L6:488-491). The quotes there are correct and not upgraded: POLY:3, :78 and :118 say "PROVED (by this seat,
unchecked)", and POLY:4-8 says VERIFIED-WITH-AMENDMENTS.
*Correction:* E2 status: "PROVED (by this seat, unchecked), conditional on RM2-R as given and on W2-LOC2 Lemma BC
(`L6_poly.md:78`) and Lemma-IR (`:118`), both 'PROVED (by this seat, unchecked)'". Do the same for E3, with RM2-F. In
the table rows, write "conditional on BC, IR".

**4. NIT (E1):** L6:104 says "BM-infinity or (BM-Q) implies (BM-W)". BM-∞ implies (BM-W) only when d_n² = O(log n),
that is under (N-χ). Under (N-D) it is (BM-Q) that is used (`L3_assemblyF.md:47-53`). *Correction:* "BM-∞ under (N-χ),
or (BM-Q) under (N-D), implies (BM-W)".

**5. NIT (§0, optional):** L6:62-63 could say that D is finite for α > 1 and J for α > 2, so the cutoff comes from J
(IR), not D. POLY §6 (P16) gives a shorter route to (0.1), with constant 1 + L₀ in place of 1 + JD: the coefficient
difference on A is −Σ_{w∈E}β_T(l)_w γ_w, with ‖γ_w‖₁ ≤ L₀. Either is correct.

**6. NIT (outside the object):** STATEMENT.md:248 says "[v1.4: verified in `lemmas/L6_examples.md`]". The file's status
is "PROVED (by this seat, unchecked)", so "proved (unchecked) in" would be the accurate word until this check round is
disposed.

## Independent derivations

**§0.**
* *Lemma BC applicability.* For |U| ≤ 15, B = Σ_{U∪{j,k}} has size m ≤ 17. The cofactor/path argument of POLY:86-99
  gives |(B⁻¹)_jk| ≤ (m−1)! K₀^{m−1} (m−1)^α c^{−m} (1+d)^{−α}. It uses (1 + d/h)^{−α} ≤ h^α(1+d)^{−α} for h ≥ 1. Then
  |S_jk| ≤ C²|H_jk|. So the K_15 of L6:45-46 is exactly that bound maximised over 2 ≤ m ≤ 17.
  It is uniform in positions and in U, because only the triangle inequality for d and the spectral bounds of principal
  submatrices are used. Both still hold for an injection into ℤ and for a deterministic Gram matrix G.
  Conditional variances lie in [c, 1].
* *Lemma IR applicability.* The proof (POLY:131-167) uses only "at most two positions at each distance", the spectrum
  [c, C] of principal submatrices, unit diagonal (Var(W_l | W_T) ≤ 1 in the step β_v = −(B⁻¹)_vl/(B⁻¹)_ll) and α > 2
  (POLY:145, :166). All of these hold for E2 (Σ) and for E3 (G).
* *Finiteness of J and D.* J = H f(0) + 2H Σ_{d≥1} f(d), with f(d) = (log(2+d)/(1+d))^{α−1}, is finite iff α − 1 > 1,
  that is α > 2. D = 1 + 2K_dec Σ(1+d)^{−α} is finite iff α > 1. The column-sum bounds hold because each column
  contains at most two indices per distance, and B_AE has no diagonal entry since A ∩ E = ∅.
* *Refitting identity.* The A-rows of B_TT β_T = B_Tl give B_AA β_{T,A} + B_AE β_{T,E} = B_Al, hence
  β_A = β_{T,A} + B_AA⁻¹B_AE β_{T,E}. So
  ‖β̄_T − β̄_A‖₁ ≤ ‖β_{T,E}‖₁(1 + ‖B_AA⁻¹‖_{1→1}‖B_AE‖_{1→1}) ≤ (1 + JD)‖β_{T,E}‖₁.
  E = T ∖ N_l is exactly {v ∈ T : d(l,v) > r}, so ‖β_{T,E}‖₁ ≤ F(r). This is (0.1). The case A = ∅ is immediate.
* *Variance bound.* e_A − e_T = Σ_v(β̄_T − β̄_A)_v W_v has standard deviation ≤ ‖·‖₁ ≤ L, because the coordinates have
  unit variance. e_T ⟂ span W_T ⊇ span W_A. Hence Var e_A = Var e_T + Var(e_A − e_T) ≤ Var e_T + L², and with
  Var e_T ≥ c this is (0.2). With an exact Gram, ‖(I − P)x_l‖² = (n − 1)Var_G.
* *Choice of r.* r = ⌊√log n⌋ gives |N_l| ≤ 2r = o(log n) and L(r) → 0, so L² log(q + 1) ≤ L²(b log n + 1) = o(log n).
  For a fixed h ∈ (0, ½ − b), 2r log 2 ≤ h log n eventually.

**E2** (against STATEMENT §3.2, (C2) and `L4_sandR_b.md` §0 (R-FL)…(R-B)).
* Size and feasibility. R_Q^{−α} ≤ (n^γ(log n)^{−γ/2})^{−α} = n^{−1/2}(log n)^{1/4}, since γα = ½.
  |Q| ≤ 4s₀R_Q + 34s₀ in both branches, and at b = γ this is ≤ n^γ eventually.
  (L-feas): in the first branch K = min(p, ⌊n/2⌋) ≥ 2q + 32s₀ + 1, because q = o(n). In the enlarged branch
  p ≤ 2|Q₀| + 32s₀ = o(n), so K = p = |Q|.
* (L-gain-R) at every U. l ∉ Q₀ implies d(l, j) > R_Q for all j ∈ S₀, and BC applies for any |U| ≤ 15 with l, j ∉ U.
  So ℓ_n√(n/log n) ≤ K_15(log n)^{−1/4} → 0.
* (L-loc-R). Take r₀ = ⌈log n⌉. For v ∉ H_l, v ≠ l, and v ∉ U₀, with d(v, l) > r₀ and d(v, j) > r₀, BC at U₀ gives
  r_n = K_15(1 + r₀)^{−α} → 0. |H_l| ≤ (s₀ + 1)(2r₀ + 1) ≤ n^ρ. For ρ = (½ − b)/30, 15ρ + b = ¼ + b/2 < ½.
* (T1-R): the global floor gives LSF with φ² = ψ_n = c (APP L1_POST:20-25 and RM STATEMENT:129-133).
  (FL-R): Rayleigh. (V-R): assumed.
* (W-R): (D-loc^b) as defined in L5 §2 (pairs in 𝔓⁺, ν_n = o(log n), L_n² log(q + 1) = o(log n), η_n = L²/c → 0, (N1),
  (N0^b)) holds by §0 applied to Σ, uniformly in T.
* Nothing in the list of (C2) is missing; (R-FL) needs c ≤ 1, which unit diagonal gives.
* *17/2 ledger.* POLY (P6) requires 1/(4α) < ρ < (½ − 1/(2α))/15, which is equivalent to 17/(4α) < ½, that is α > 17/2.
  The lower bound on ρ came from w_n → 0 in (P9) (αρ > ¼). In v1.3, (L-R^b-loc) needs r_n(n/log n)^{1/4} → 0, which
  again forces ρ > 1/(4α). v1.4 drops it because BC supplies the leak bound at every U and only r_n → 0 is needed.
  The ledger at L6:240-249 is correct.

**E3** (against GROW STATEMENT:84-88 and RM2 §3.1).
* (H0): R1 holds (fixed s₀, p ≤ n − 1 so A = 1, s₀ ≤ K). R holds: ‖μ‖² = (n−1)θᵀGθ ≤ (n−1)C s₀θ_hi², so L6's
  M = Cs₀θ_hi² + 1 is valid, and λ_min(R̂_{S₀}) ≥ c.
  SE_λ(j₀) and SE_w(m♯; g₀) follow from the global floor ((n − 1)c ≥ g₀; consistent with APP L1_POST(c)). BM-∞ holds.
* (V): x_jᵀ(I − P_U)μ = (n − 1)[θ_j G_{jj|U} + Σ_{k∈S₀∖(U∪{j})} θ_k G_{jk|U}], and BC with (3.1) gives
  ≥ (n − 1)cθ_lo/2. Since G_{jj|U} ≤ 1, δ²_{U,j} ≥ (n − 1)c²θ_lo²/4.
* (L-gain): δ²_{U,l} ≤ (n − 1)B_θ²K_15²(1 + R_Q)^{−2α}/c ≤ (B_θ²K_15²/c)√log n ≤ ησ² log n ≤ ητ²_U log n eventually,
  for every fixed η > 0. Then pick b ∈ [γ, ½) and η < η_A with b < β(η, 1).
* (BM-W) follows through (BM-Q). (W-loc): both inequalities of STATEMENT:149-154 hold. The sample regression equals the
  G-regression because X'X = (n − 1)G; take L_n = (1 + JD)F(r), η_n = L_n²/c and ν_n = 2r.

**E4.**
* G_Q as displayed (proxy–proxy entries r²). ‖G_Q − I‖ ≤ r√m + r²(m − 1), so the floor is ≥ ½ for any b < 1; outside
  columns are orthonormal.
* Var_G(1|U) with t proxies is 1 − r²·t/(1 − r² + tr²) = (1 − r²)/(1 + (t − 1)r²). Checked symbolically, and
  numerically at t = 0, 1, 3, 15.
* (L-gain) holds with η = 0, since x_l ⟂ everything for l > q.
* (W-loc) is exact: x_l − r x₁ = √(n−1)√(1−r²) e_l ⟂ X_T for every lattice T (T ∋ 1). So β_{T,l} = r e₁ = β_{{1},l},
  L_n = η_n = 0, ν_n = 1. l = 1 never occurs in 𝔓.
* (L-feas) holds with p = ⌊n/3⌋ ≥ 2q + 33. (BM-Q) holds with φ₀² = ½. Every clause of (C1) holds.

**E5.**
* A_t = a/(1 − a + ta). Residual norm v_t = a(1 − tA_t)² + (1 − a)(1 + tA_t²) = (1 − a)[1 + a/D_t] with
  D_t = 1 − a + ta. Checked algebraically.
* (5.1) uses 0 ≤ 1 − tA_t ≤ 1 and tA_t ≤ 1. EU and EV are bounded as stated.
* The constant C_G follows from P(max(U, V) − max(EU, EV) > s) ≤ 2e^{−s²/2}.
* (W-unif) holds iff 2δ < 1 − 2b (from the √2 branch) and 2δ < 3 − 10b (from the √(8b) branch). So b < 3/10 is
  correct for this bound, and L2 §3(ii) then gives (W-δ) and (W).
* The other clauses hold with φ₀² = 1 − a and η = 0.

**Numerics.**
* K12 and K13 (`formR_checks_out.txt:8-9`) agree with E4 and E5.
* My own scratch script (outside the worktree) used a Toeplitz Σ with entries (1 + d)^{−2.5}, p = 300, spectrum
  [0.73, 1.68], and 400 random (T, l, r). Refitting identity error 1.7e-16; max of lhs − (1 + JD)‖β_E‖₁ was −4e-11;
  max of Var_A − Var_T − L² was −3e-10.
* It also confirmed the E4 variance formula and computed the E5 exact-maximum ratios of finding 1.

## Not checked

* The proofs of Lemma BC and Lemma IR themselves. I only checked their hypotheses and the parts of the proofs that
  matter for transferring them (injection, exact Gram).
* L2, L3, L4 and L5 (theorems, containments, sufficient forms), taken as given per the brief.
* The internal correctness of the inherited sources in E1 (UNI-0, LOC-BF, GROW (C5)(a)/(b), RM L7). I checked that the
  cited lines exist and say what L6 says they say.
* The b < 3/8 extension and the b > 3/8 failure in finding 1 are sketches, not proofs.
