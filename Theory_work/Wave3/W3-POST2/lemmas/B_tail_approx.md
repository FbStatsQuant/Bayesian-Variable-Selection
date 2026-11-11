# B — Lemma 1a″: size tail with an approximate reference and the exact determinant (W3-POST2, Claim B)

Status: **PROVED (by this seat, unchecked)**. **Check record [C1B-2]:** line check K-BC (gpt-6.1-sol high, `../reviews/K_BC_check_sol.md`): VERIFIED-WITH-AMENDMENTS, no counterexample in 2,160 enumeration draws, Remark 1 fixed (`K_BC_disposition.md`); M01: sound; S01: remark fixes; council C1 (PASS). Notation: `../STATEMENT.md`; [P1] §1 and
`lem:den` (contrast coordinates, Q^c_S, m^c_b(S), b±, κ, 𝓑_n, c_IG); [L1a′] = `../../W3-POST/lemmas/L1a_size_tail.md`.

## Statement
Fix n ≥ 3, a standardised design X with p ≥ 2, and the truth **G′**: y^r = α*1 + f + ε, f ∈ ℝⁿ arbitrary,
ε ~ N_n(0, σ*²I), μ := Cf with ‖μ‖² ≤ nM. Let T ∈ Ω (t := |T|) and ϑ ∈ ℝ^T be deterministic with
  B_T(ϑ) := ‖μ − X_Tϑ‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n ≤ B.
Put R^T_m := Σ_{k=max(m+1,0)}^{K} q_k/w(t), A^T_m := R^T_m√(D_T)√n, and define Θ″_{n,m} ≥ 0 by
π(|S| > m) = A^T_mΘ″_{n,m} (Θ″ := 0 if R^T_m = 0). Then for every L > c♯² (c♯ := κ²/(c_IGσ*²), [T03R] line 77):
  sup_m P(Θ″_{n,m} > L) ≤ (8 + 24M/σ*²)/(n − 1) + L^{−1/2} + C″_Λ(B)/log(√L/c♯),
  C″_Λ(B) := 1/√2 + 1/2 + B/(2σ*²) + √(2B/π)/σ*.
The right side depends on (X, f, T, ϑ) only through (M, B).

## Proof
**Step 1 ([P1] steps that do not see the form of the mean).** Under G′, Cy^r = μ + Cε, so y_c = Uᵀy^r = Uᵀμ + ε_c
(Uᵀ1 = 0, Uᵀ = UᵀC), ε_c = Uᵀε ~ N_{N}(0, σ*²I), and f₀(x) := N_N(x; Uᵀμ, σ*²I) is the density of y_c. The following
use only these facts and ‖μ‖² ≤ nM, never μ ∈ col X: [P1] `thm:T01iii` (its proof writes (n−1)s_y² = ‖μ‖² + 2μᵀε + ‖Cε‖²;
gives P(𝓑_nᶜ) ≤ (8 + 24M/σ*²)/(n−1)); `lem:num` (any positive density f₀ of y_c; b₋ data-free); `thm:Ta` (deterministic);
`lem:slab`, `lem:spec` (deterministic). [P1] `thm:T01i` (π = Π_b with b = b₀s_y²) is deterministic.

**Step 2 (reference bound; the changed step of `lem:den`).** By [P1] `lem:slab`,
Q^c_T = min_φ{‖y_c − X_{c,T}φ‖² + φᵀ(G_T + I)φ/n}. Take φ = ϑ and put r := μ − X_Tϑ. Both μ and X_Tϑ are centred,
so r ∈ 1^⊥ = range C and ‖Uᵀr‖² = rᵀCr = ‖r‖². Then y_c − X_{c,T}ϑ = ε_c + Uᵀr and ε_cᵀUᵀr = εᵀUUᵀr = εᵀr, so
  Q^c_T ≤ ‖ε_c‖² + 2εᵀr + ‖r‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n ≤ σ*²E′ + ρ″,  ρ″ := B + 2|εᵀr| ≥ 0,
with E′ := ‖ε_c‖²/σ*² ~ χ²_N and εᵀr ~ N(0, σ*²‖r‖²), ‖r‖² ≤ B. (If t = 0: φ is void, Q^c_∅ = ‖y_c‖² and the same
display holds with r = μ.)

**Step 3 (rest of `lem:den`, verbatim with R_n → ρ″, D_T kept).** The integral representation and the exponent bound
of [P1] `lem:den` use only Q^c ≤ σ*²E′ + (a nonnegative random quantity) and u ≥ 1 in −ρ″/(2σ*²u) ≥ −ρ″/(2σ*²). With
  Λ″_n := |E′ − N|/(2√n) + E′/(2n) + ρ″/(2σ*²),
restricting the v-integral to [σ*², σ*²(1 + n^{−1/2})] gives m^c_{b₊}(T)/f₀(y_c) ≥ D_T^{−1/2} c_IG σ*² n^{−1/2} e^{−Λ″_n}.
(The bound D_T ≤ (n+1)^t of [P1] `lem:spec`(e) is **not** applied.) Moments: E|E′ − N| ≤ √(2N) ≤ √(2n),
E E′/(2n) ≤ 1/2, E|εᵀr| = σ*‖r‖√(2/π) ≤ σ*√(2B/π); so E Λ″_n ≤ C″_Λ(B).

**Step 4 (assembly; [T03R] lines 93-97 with S₀ → T).** Fix m with R^T_m > 0, E_m := {|S| > m}, v_m := ϖ(E_m) =
R^T_mϖ(T) (W_K cancels), N_m := I_{b₋}(E_m)/f₀(y_c), Θ^{(1)}_{n,m} := N_m/v_m; E Θ^{(1)} = 1 by Step 1. On 𝓑_n, [P1]
`thm:Ta` (its last inequality needs only T ∈ Ω, since Z^c_{b₊} ≥ ϖ(T)m^c_{b₊}(T)) and Step 3:
  π(E_m) ≤ κ² v_mΘ^{(1)} / (ϖ(T)m^c_{b₊}(T)/f₀) ≤ R^T_m √(D_T)√n · c♯e^{Λ″_n}Θ^{(1)}_{n,m}.
So Θ″ ≤ c♯e^{Λ″}Θ^{(1)} on 𝓑_n, and Markov's inequality for Θ^{(1)} ≥ 0 and Λ″ ≥ 0 gives the display, exactly as in
[T03R] line 96. ∎

## Consequences and remarks
1. **Implies [L1a′].** If μ = X_Tθ exactly with ‖θ‖² ≤ nM′, take ϑ = θ: r = 0, B = (‖μ‖² + ‖θ‖²)/n ≤ M + M′. The general display then holds with the larger
   constant C″_Λ(M + M′) = C′_Λ + √(2(M+M′)/π)/σ*; but in the exact-reference case Step 3 improves (ρ″ = B is deterministic,
   no εᵀr term) to E Λ″ ≤ 1/√2 + 1/2 + B/(2σ*²) ≤ C′_Λ, and Step 4 then gives the display with C′_Λ exactly [K-BC-1].
   L1a′'s normalisation: Θ^T = √(D_T)(n+1)^{−t/2}Θ″ ≤ Θ″, so the tail bound transfers. Since √(D_T) ≤ (n+1)^{t/2},
   A^T_m ≤ R^T_m(n+1)^{t/2}√n, so every cutoff valid for [L1a′] is valid here.
2. **Cutoffs.** For every deterministic m_n with A^T_{m_n} ≤ e^{−ω_n}: π(|S| > m_n) ≤ e^{−ω_n}Θ″_{n,m_n} = O_P(e^{−ω_n}).
3. **Dropping weak coefficients.** With S₀ = T ⊔ W, ϑ = θ*_T: r = X_Wθ*_W, so B = ‖X_Wθ*_W‖² + (‖X_Tθ*_T‖² + ‖θ*_T‖²)/n.
   Since ‖X_Wθ*_W‖ ≤ √N Σ_{j∈W}|θ*_j|, coefficients with Σ_{j∈W}|θ*_j| ≤ √(B₀/N) may be dropped at cost B₀, and the
   cutoff uses t = |T| < s₀.
4. **Weak total signal.** T = ∅, B = ‖μ‖²: if ‖μ‖² ≤ B₀ then R^∅_m = 2Σ_{k>m}q_k ≤ 2^{1−m} (the line Σ_{k>m}q_k ≤ 2^{−m} in the proof of [P1] `lem:prior`(c)) [C1B-12], D_∅ = 1,
   so π(|S| > m) = O_P(2^{−m}√n); hence for every ω_n → ∞, π(|S| > m_n) → 0 in probability with
   m_n := min(K, ⌈(½ log n + ω_n)/log 2⌉ + 1) [S01-12].
5. **Means outside col X (misspecification).** Any reference with bounded cost works; nothing requires f ∈ col X^r.
6. **Effective rank.** D_T = Π_i f(λ_i(G_T)), f(λ) = ((n+1)λ + 1)/(λ + 1) ([P1] `lem:spec`(e)). An eigenvalue λ costs
   √f(λ): λ = 0 costs exactly 1, λ = O(1/n) costs O(1), λ = n^{−a} (0 < a < 1) costs ≍ n^{(1−a)/2}, and any fixed λ > 0 costs
   ≍ √n [S01-11]. So the gain over (n+1)^{t/2} is through the exact product, not "only large eigenvalues pay".
7. **Growing cost.** For B = B_n → ∞ the same proof gives P(Θ″ > L) ≤ … + C″_Λ(B_n)/log(√L/c♯), i.e. an exponential factor
   exp(O_P(B_n)): choosing L_n with log L_n/B_n → ∞ makes the last term vanish. The fixed-B tightness conclusion is not
   transferred verbatim to growing B_n, and nothing here says what a cutoff *must* do [M01-3]. (A sharper explicit payment
   exp{(1/(2σ*²) + ε)L_T} via the Gaussian tail of εᵀr is R03b's proposal B+, recorded, not proved here.)
8. **Falsification.** `../numerics/post2_checks.py` N6 → `post2_checks_out.txt`: max over t ≤ m < K of Θ″ for
   T = S₀ (t = 3), T = S₀ minus a weak coefficient (t = 2), and T = ∅ under weak total signal; all ≤ 1.1·10⁻² (medians),
   decreasing in n. N6b: a mean with a component orthogonal to col X (‖g‖² = 2, T = S₀): ≤ 7.5·10⁻⁶; and outside the
   hypothesis, growing cost (T = ∅, B = n − 1): Θ″ = 0.1 → 0.0125, i.e. bounded cost is sufficient, not necessary [S01-1].
