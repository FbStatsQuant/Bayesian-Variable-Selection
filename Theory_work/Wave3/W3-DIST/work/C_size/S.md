# S — Lemma S (size tail with an exponential tail; reference-adaptive) — W3-DIST stream C

Status: **DRAFT (by this seat, unchecked)**. Author: stream C (Claude Opus 5.5, Claude Third, high), 2026-11-15.
Target: STATEMENT.md v1.3.1 §3 "Lemma S" (= API_CARDS.md "Card S"), and the corollary for T = S₀, ϑ = θ* (brief item 1).
Route: S-a (re-run of W3-POST2 Claim B, `Theory_work/Wave3/W3-POST2/lemmas/B_tail_approx.md`, Steps 1–4, with every
Markov/Chebyshev step except the one on Θ^{(1)} replaced by a χ² or Gaussian tail). Claim B's status is "PROVED (by this
seat, unchecked)" (`B_tail_approx.md:3`), below PROVED-CHECKED, so its Steps 2–4 are **re-derived** here from [P1]
(locked; `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`,
cited as [P1] with line numbers). Numerical check: `c_checks.py` → `c_checks_out.txt` (lines "S:" and "B_n:").

**No STATEMENT-CHANGE REQUEST.** The lemma is proved as stated, in a slightly stronger form: the conclusion holds for
**every n ≥ 3 and every real t > 0** (so n₀ = 3, and the constants do not depend on κ₀); κ₀ enters only when the term
Ce^{−cn} is absorbed into Ce^{−t} (Corollary S.2). The corollary for T = S₀ holds for every t ≥ log n (no upper limit) with
one n₀ depending on (σ*², M, M′, s₀^r).

## Setting
Fixed n ≥ 3 and a design X with sample-centred columns, ‖x_j‖² = N := n − 1, p ≥ 2 (no other condition). Truth **G′**:
y^r = α*1 + f + ε, f ∈ ℝⁿ arbitrary, ε ~ N_n(0, σ*²I), μ := Cf ∈ 1^⊥ with ‖μ‖² ≤ nM (M ≥ 0). (Strict sparsity, μ = Xθ*, is the
special case f = X^rβ*.) Contrast coordinates: U ∈ ℝ^{n×N}, UᵀU = I, UUᵀ = C; y_c = Uᵀy^r, ε_c := Uᵀε ~ N_N(0, σ*²I),
E′ := ‖ε_c‖²/σ*² ~ χ²_N; X_c = UᵀX. Since Uᵀ1 = 0 and Uᵀ = UᵀC: y_c = Uᵀμ + ε_c. f₀(x) := N_N(x; Uᵀμ, σ*²I) is the
density of y_c, f₀ > 0 everywhere. All other notation (G_S, H_S, D_S, Q^c_S, K, Ω, w, q_k, ν, b = b₀s_y², b₀ = 0.01) as in
API_CARDS "Common definitions" and [P1] §1 (`PROOF_v3.tex:40-58`): ϖ(S) = w(|S|)/W_K, W_K = Σ_{k≤K}C(p,k)w(k), m^c_b(S), I_b(E),
Z^c_b, Π_b. The posterior π(·) = π(· | y) on Ω is Π_b with b = b₀s_y² ([P1] `thm:T01i`, `PROOF_v3.tex:173-209`; deterministic,
valid for every input with s_y > 0, which holds a.s. under G′ because Cy^r = μ + Cε has a non-degenerate law on 1^⊥).

Constants from [P1] §1 (`PROOF_v3.tex:58`) and [T03R] (`branch_snapshots/W1-T03R/PROOF.md:76`):
b₋ := b₀σ*²/2, b₊ := b₀(2(σ*² + M) + 1), κ := (b₊/b₋)^{0.51}, 𝓑_n := {b₋ ≤ b₀s_y² ≤ b₊} = {σ*²/2 ≤ s_y² ≤ 2(σ*² + M) + 1},
c_IG := min_{v∈[σ*², 2σ*²]} IG(v; 0.51, b₊) ≥ b₊^{0.51}(2σ*²)^{−1.51}e^{−b₊/σ*²}/Γ(0.51) > 0 (bound: on [σ*², 2σ*²], v^{−1.51} ≥ (2σ*²)^{−1.51}
and e^{−b₊/v} ≥ e^{−b₊/σ*²}), c♯ := κ²/(c_IG σ*²). All depend only on (σ*², M) (b₀ = 0.01 fixed).

Reference: T ∈ Ω and ϑ ∈ ℝ^T, design-measurable (non-random given X), with
  B_T(ϑ) := ‖μ − X_Tϑ‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n ≤ B,   R^T_m := Σ_{k=max(m+1,0)}^{K} q_k / w(|T|)  (m ∈ ℤ).

## Statement (Lemma S)
Put c_B := min{1/150, σ*²/(288M)} (c_B := 1/150 if M = 0),
  C₁ := max{½ + B/(2σ*²), 2 + √(2B)/σ*},  C_S := max{5, C₁ + max(0, log c♯)}.
For every n ≥ 3, every real t > 0 and every integer m with
  log R^T_m + ½ log D_T + ½ log n + C_S[1 + √t + t/√n] ≤ −2t      (S-hyp)
(automatically true if R^T_m = 0, with log 0 := −∞):
  P_ε[ π(|S| > m) > e^{−t} ] ≤ 5e^{−t} + 4e^{−c_B n}.
Moreover the bad events are nested in m: the set of m satisfying (S-hyp) is an up-set {m ≥ m*}, and on the
complement of the single event used for m* (probability ≥ 1 − 5e^{−t} − 4e^{−c_Bn}) one has π(|S| > m) ≤ e^{−t} for
**all** m satisfying (S-hyp) simultaneously.
The constants depend only on (σ*², M, B). This implies the STATEMENT form (C := C_S, c := c_B, n₀ := 3, any κ₀).

## Toolbox (classical; stated exactly)
- **(LM) Laurent–Massart** (B. Laurent, P. Massart, Ann. Statist. 28 (2000) 1302–1338, Lemma 1, p. 1325): if ξ₁, …, ξ_D are
  i.i.d. N(0, 1), a_i ≥ 0, Z := Σ_i a_i(ξ_i² − 1), then for every x > 0:
  P(Z ≥ 2‖a‖₂√x + 2‖a‖_∞x) ≤ e^{−x} and P(Z ≤ −2‖a‖₂√x) ≤ e^{−x}.
  For a_i ≡ 1 (Z + D ~ χ²_D): P(χ²_D − D ≥ 2√(Dx) + 2x) ≤ e^{−x}, P(D − χ²_D ≥ 2√(Dx)) ≤ e^{−x}.
- **(G) Gaussian tail:** for g ~ N(0, s²) and x > 0, P(|g| ≥ s√(2x)) ≤ 2e^{−x}. (Chernoff: P(g ≥ u) ≤ inf_λ e^{−λu + λ²s²/2} = e^{−u²/(2s²)}.)
- **(Mk) Markov:** for Θ ≥ 0 with E Θ ≤ 1, P(Θ > e^x) ≤ e^{−x}.

## Proof

**Step 1 (inputs from [P1] that do not see the form of the mean).** Each item is quoted with the hypothesis it uses.
(1a) [P1] `lem:num` (`PROOF_v3.tex:317-322`): "Fix b > 0 not depending on the data. For every S ∈ Ω, m^c_b(S), as a function
of y_c, is a probability density on ℝ^{n−1}. For every set 𝒜 ⊆ Ω, E₀[Σ_{S∈𝒜}ϖ(S)m^c_b(S)/f₀(y_c)] = ϖ(𝒜)." Its proof uses only
that f₀ > 0 is the density of y_c (Tonelli), so it holds under G′ with f₀ as above.
(1b) [P1] `thm:Ta` (`PROOF_v3.tex:255-265`), first inequality: "on the event 𝓑_n, and every measurable parameter event E,
Π(E | y) ≤ κ² I_{b₋}(E)/Z^c_{b₊}". Its proof uses thm:T01i and thm:T01ii (`PROOF_v3.tex:213-222`), both deterministic in y, and
b₀s_y² ∈ [b₋, b₊] on 𝓑_n; nothing about μ. Since Z^c_{b₊} = Σ_{S∈Ω}ϖ(S)m^c_{b₊}(S) ≥ ϖ(T)m^c_{b₊}(T) for T ∈ Ω:
  on 𝓑_n:  π(E) ≤ κ² I_{b₋}(E) / (ϖ(T)m^c_{b₊}(T)).                                                        (1.1)
(1c) [P1] `lem:slab` (`PROOF_v3.tex:68-81`): ∫N_N(y_c; X_{c,T}φ, vI)N(φ; 0, nv(G_T + I)⁻¹)dφ = (2πv)^{−N/2}D_T^{−1/2}e^{−Q^c_T/(2v)}, and
Q^c_T = min_φ{‖y_c − X_{c,T}φ‖² + φᵀ(G_T + I)φ/n}. Deterministic. Hence (Tonelli, [P1] `lem:den`'s integral representation,
`PROOF_v3.tex:340-347`):
  m^c_{b₊}(T)/f₀(y_c) = D_T^{−1/2} ∫₀^∞ exp{−(N/2)log(v/σ*²) + E′/2 − Q^c_T/(2v)} IG(v; 0.51, b₊) dv,               (1.2)
using f₀(y_c) = (2πσ*²)^{−N/2}e^{−‖y_c − Uᵀμ‖²/(2σ*²)} = (2πσ*²)^{−N/2}e^{−E′/2}.

**Step 2 (reference bound; Claim B Step 2 re-derived).** Put r := μ − X_Tϑ. Both μ and X_Tϑ are centred (columns of X are
centred), so r ∈ 1^⊥ and ‖Uᵀr‖² = rᵀCr = ‖r‖². Since X_{c,T}ϑ = UᵀX_Tϑ, y_c − X_{c,T}ϑ = Uᵀr + ε_c, and
ε_cᵀUᵀr = εᵀUUᵀr = εᵀCr = εᵀr. Taking φ = ϑ in (1c) and using ϑᵀ(G_T + I)ϑ = ‖X_Tϑ‖² + ‖ϑ‖² (G_T = X_TᵀX_T):
  Q^c_T ≤ ‖ε_c‖² + 2εᵀr + ‖r‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n = σ*²E′ + 2εᵀr + B_T(ϑ) ≤ σ*²E′ + ρ″,   ρ″ := B + 2|εᵀr| ≥ 0.   (2.1)
If T = ∅: Q^c_∅ = ‖y_c‖² = ‖Uᵀμ + ε_c‖² = σ*²E′ + 2εᵀμ + ‖μ‖², which is (2.1) with r = μ, B_∅ = ‖μ‖².
Here εᵀr ~ N(0, σ*²‖r‖²) and ‖r‖² ≤ B_T(ϑ) ≤ B.

**Step 3 (denominator; [P1] `lem:den` exponent bound, `PROOF_v3.tex:348-356`, with R_n → ρ″ and D_T kept).**
Let v = σ*²u with 1 ≤ u ≤ 1 + n^{−1/2}. Using log u ≤ u − 1, (2.1), u ≥ 1, ρ″ ≥ 0 and 1/u ≥ 2 − u:
  −(N/2)log u + E′/2 − Q^c_T/(2σ*²u) ≥ −(N/2)(u − 1) + (E′/2)(1 − 1/u) − ρ″/(2σ*²u)
    = ((u − 1)/2)(E′/u − N) − ρ″/(2σ*²u) ≥ ((u − 1)/2)(E′ − N − E′(u − 1)) − ρ″/(2σ*²)
    ≥ −|E′ − N|/(2√n) − E′/(2n) − ρ″/(2σ*²) =: −Λ″,
the last step by 0 ≤ u − 1 ≤ n^{−1/2}. Restrict the integral in (1.2) to v ∈ [σ*², σ*²(1 + n^{−1/2})] ⊆ [σ*², 2σ*²] (length
σ*²n^{−1/2}; there IG(v; 0.51, b₊) ≥ c_IG; the integrand is ≥ 0 elsewhere):
  m^c_{b₊}(T)/f₀(y_c) ≥ D_T^{−1/2} c_IG σ*² n^{−1/2} e^{−Λ″}.                                                         (3.1)
(The bound D_T ≤ (n+1)^{|T|} is not used.)

**Step 4 (assembly; Claim B Step 4 re-derived).** Fix m with R^T_m > 0 (if R^T_m = 0 then {S ∈ Ω : |S| > m} = ∅, π(|S| > m) = 0,
nothing to prove). E_m := {S ∈ Ω : |S| > m}; v_m := ϖ(E_m) = Σ_{k=max(m+1,0)}^K C(p,k)w(k)/W_K = R^T_m w(|T|)/W_K = R^T_mϖ(T) > 0;
N_m := I_{b₋}(E_m)/f₀(y_c) = Σ_{S∈E_m}ϖ(S)m^c_{b₋}(S)/f₀(y_c) (I_{b₋}(E_m) = Σ_{S∈E_m}ϖ(S)m^c_{b₋}(S) because E_m is a model event);
Θ^{(1)}_m := N_m/v_m ≥ 0. Since b₋ is data-free, (1a) gives E Θ^{(1)}_m = 1. On 𝓑_n, by (1.1) and (3.1):
  π(E_m) ≤ κ² v_mΘ^{(1)}_m / (ϖ(T) m^c_{b₊}(T)/f₀(y_c)) = κ² R^T_m Θ^{(1)}_m / (m^c_{b₊}(T)/f₀(y_c)) ≤ R^T_m √(D_T) √n · c♯ e^{Λ″} Θ^{(1)}_m.   (4.1)
This is Claim B's inequality (`B_tail_approx.md:40`), now re-derived.

**Step 5 (exponential tail of Λ″; replaces Markov on Λ″).** For x > 0 let 𝒜_x := 𝒜¹_x ∩ 𝒜²_x with
  𝒜¹_x := {−2√(Nx) ≤ E′ − N ≤ 2√(Nx) + 2x},   𝒜²_x := {|εᵀr| ≤ σ*‖r‖√(2x)}.
By (LM) with D = N, P((𝒜¹_x)ᶜ) ≤ 2e^{−x}; by (G) with s = σ*‖r‖, P((𝒜²_x)ᶜ) ≤ 2e^{−x} (if r = 0, 𝒜²_x is sure). So
P(𝒜_xᶜ) ≤ 4e^{−x}. On 𝒜_x, using N ≤ n, √N/√n ≤ 1, n^{−1/2} ≤ 1 and 1/n ≤ 1/√n:
  |E′ − N|/(2√n) ≤ (2√(Nx) + 2x)/(2√n) ≤ √x + x/√n;
  E′/(2n) ≤ (N + 2√(Nx) + 2x)/(2n) ≤ ½ + √x·√N/n + x/n ≤ ½ + √x + x/√n;
  ρ″/(2σ*²) = (B + 2|εᵀr|)/(2σ*²) ≤ B/(2σ*²) + ‖r‖√(2x)/σ* ≤ B/(2σ*²) + (√(2B)/σ*)√x.
Summing: Λ″ ≤ (½ + B/(2σ*²)) + (2 + √(2B)/σ*)√x + 2x/√n ≤ C₁(1 + √x + x/√n) on 𝒜_x.                                  (5.1)

**Step 6 (exponential bound for the bracket 𝓑_n; replaces Chebyshev in [P1] `thm:T01iii`).** As in [P1] `thm:T01iii`'s
proof (`PROOF_v3.tex:240-250`), which uses only Cy^r = μ + Cε (true under G′: C1 = 0, Cf = μ): Ns_y² = ‖μ‖² + 2μᵀε + σ*²E′ and
  Δ_n := s_y² − (σ*² + ‖μ‖²/N) = σ*²(E′/N − 1) + 2μᵀε/N.
*Inclusion 𝓑_nᶜ ⊆ {|Δ_n| > σ*²/2}.* If s_y² < σ*²/2 then Δ_n < σ*²/2 − σ*² − ‖μ‖²/N ≤ −σ*²/2. If s_y² > 2(σ*² + M) + 1 then,
since ‖μ‖²/N ≤ nM/(n − 1) ≤ 3M/2 (n ≥ 3), Δ_n > 2σ*² + 2M + 1 − σ*² − 3M/2 ≥ σ*² > σ*²/2.
*Tail.* {|Δ_n| > σ*²/2} ⊆ {|E′ − N| > N/4} ∪ {|μᵀε| > Nσ*²/8}. By (LM) with x = N/100 (then 2√(Nx) + 2x = 0.22N ≤ N/4):
P(E′ − N > N/4) ≤ e^{−N/100}; with x = N/64 (2√(Nx) = N/4): P(N − E′ > N/4) ≤ e^{−N/64} ≤ e^{−N/100}. μᵀε ~ N(0, σ*²‖μ‖²),
‖μ‖² ≤ nM; by (G) with s = σ*‖μ‖ and s√(2x) = Nσ*²/8, i.e. x = N²σ*²/(128‖μ‖²) ≥ N²σ*²/(128nM) ≥ Nσ*²/(192M) (N/n ≥ 2/3):
P(|μᵀε| > Nσ*²/8) ≤ 2e^{−Nσ*²/(192M)} (the event is empty if μ = 0). With N ≥ 2n/3:
  P(𝓑_nᶜ) ≤ 2e^{−N/100} + 2e^{−Nσ*²/(192M)} ≤ 2e^{−n/150} + 2e^{−nσ*²/(288M)} ≤ 4e^{−c_B n}.                       (6.1)

**Step 7 (conclusion).** Fix t > 0 and m satisfying (S-hyp) with R^T_m > 0. On 𝓑_n ∩ 𝒜_t ∩ {Θ^{(1)}_m ≤ e^t}, by (4.1) and (5.1),
  log π(E_m) ≤ log R^T_m + ½ log D_T + ½ log n + log c♯ + C₁(1 + √t + t/√n) + t
          ≤ log R^T_m + ½ log D_T + ½ log n + C_S(1 + √t + t/√n) + t ≤ −2t + t = −t,
using log c♯ + C₁(1 + √t + t/√n) ≤ (max(0, log c♯) + C₁)(1 + √t + t/√n) ≤ C_S(1 + √t + t/√n) (as 1 + √t + t/√n ≥ 1), then (S-hyp).
By (Mk), P(Θ^{(1)}_m > e^t) ≤ e^{−t}; with (6.1) and P(𝒜_tᶜ) ≤ 4e^{−t}:
  P(π(|S| > m) > e^{−t}) ≤ P(𝓑_nᶜ) + P(𝒜_tᶜ) + P(Θ^{(1)}_m > e^t) ≤ 4e^{−c_Bn} + 5e^{−t}.
*Nesting.* q_k > 0 for 0 ≤ k ≤ K, so R^T_m is non-increasing in m, and the left side of (S-hyp) is non-increasing in m; the
qualifying m form an up-set {m ≥ m*}, and m* ≥ 0 when it exists (for m ≤ −1, R^T_m = W_K/w(|T|) ≥ 1 since W_K ≥ ½ ≥ w(|T|), so
the left side of (S-hyp) is ≥ 0 > −2t). π(|S| > m) is non-increasing in m. Applying the above to m* only: on the event
𝓑_n ∩ 𝒜_t ∩ {Θ^{(1)}_{m*} ≤ e^t}, π(|S| > m) ≤ π(|S| > m*) ≤ e^{−t} for all m ≥ m*. ∎

## Corollary S.1 (reference T = S₀, ϑ = θ*; cutoff m_n(t); brief item 1)
Assume strict sparsity on the retained columns, μ = Xθ* with S₀ = supp θ*, s₀ = |S₀| ∈ {0, …, s₀^r}, (E; M): ‖μ‖² ≤ nM and
(C; M′): ‖θ*‖² ≤ nM′. Let C_S, c_B be the constants of Lemma S with B := M + M′, and
  n_S := max{3, 2s₀^r, ⌈4C_S²⌉, ⌈exp((2C_S + 1)²)⌉}.
Then for every n ≥ n_S, every s₀ ∈ {0, …, s₀^r} (with s₀ ≤ p) and every real t ≥ log n:
  P_ε[ π(|S| > m_n(t)) > e^{−t} ] ≤ 5e^{−t} + 4e^{−c_B n},
  m_n(t) := min{K, s₀ + ⌈(s₀ log(2p) + ((s₀+2)/2) log(n+1) + 3t)/log 2⌉}.
(One n_S for all s₀ ≤ s₀^r and all t ≥ log n; no p ≤ n^A, no (ND), no upper limit on t.)
*Proof.* (i) T = S₀ ∈ Ω: s₀ ≤ p always, and s₀ ≤ s₀^r ≤ ⌊n/2⌋ for n ≥ 2s₀^r; so s₀ ≤ K. (ii) B_{S₀}(θ*) = ‖μ − X_{S₀}θ*‖² +
(‖X_{S₀}θ*‖² + ‖θ*‖²)/n = 0 + (‖μ‖² + ‖θ*‖²)/n ≤ M + M′ = B. (iii) If m_n(t) = K then R^{S₀}_K = 0 (empty sum) and the claim is
trivial (π(|S| > K) = 0). Otherwise m := m_n(t) ≥ 0 and m·log 2 ≥ s₀ log(2p) + ((s₀+2)/2)log(n+1) + 3t. By [P1] `lem:prior`(c)'s
proof (`PROOF_v3.tex:128`: "q_k ≤ 2^{−(k−1)}q₁ ≤ 2^{−k} for 1 ≤ k ≤ p"), Σ_{k=m+1}^K q_k ≤ Σ_{k≥m+1}2^{−k} = 2^{−m}; and
1/w(s₀) = 2C(2p−1, s₀) ≤ 2(2p)^{s₀}. Hence log R^{S₀}_m ≤ log 2 + s₀ log(2p) − m log 2 ≤ log 2 − ((s₀+2)/2)log(n+1) − 3t.
By [P1] `lem:spec`(e) (`PROOF_v3.tex:97`), D_{S₀} ≤ (n+1)^{s₀}, so ½ log D_{S₀} ≤ (s₀/2)log(n+1); and ½ log n ≤ ½ log(n+1). So
  log R^{S₀}_m + ½ log D_{S₀} + ½ log n ≤ log 2 − log(n+1) + ½ log(n+1) − 3t = log 2 − ½ log(n+1) − 3t ≤ −3t
(½ log(n+1) ≥ ½ log 4 = log 2). (S-hyp) therefore follows from C_S(1 + √t) + C_S t/√n ≤ t. For n ≥ 4C_S²: C_S t/√n ≤ t/2.
For t ≥ (2C_S + 1)², with s := √t ≥ 2C_S + 1: t/2 = s²/2 ≥ (2C_S + 1)s/2 = C_S s + s/2 ≥ C_S s + C_S + ½ > C_S(1 + √t). Since
t ≥ log n ≥ log n_S ≥ (2C_S + 1)², both hold. Apply Lemma S. ∎

## Corollary S.2 (absorbing the bracket term; where κ₀ enters)
In Corollary S.1, if in addition t ≤ n^{1−κ₀} and n ≥ n_S′ := max{n_S, ⌈(1/c_B)^{1/κ₀}⌉}, then e^{−c_Bn} ≤ e^{−t} (because
t ≤ n^{1−κ₀} ≤ c_Bn ⇔ n^{κ₀} ≥ 1/c_B), so P_ε[π(|S| > m_n(t)) > e^{−t}] ≤ 9e^{−t}. Equivalently, for c ∈ (0, 1] and t′ := ct,
the same holds at level e^{−ct} for t ≥ (log n)/c, with failure probability ≤ 9e^{−ct} (apply S.1 with t′ in place of t
and note m_n(t′) ≤ m_n(t)).

## Remarks
- **R1 (what was replaced).** Claim B's two weak steps were Markov on Λ″ (`B_tail_approx.md:41`, giving C″_Λ/log(√L/c♯))
  and Chebyshev for 𝓑_n ([P1] `thm:T01iii`, giving (8 + 24M/σ*²)/(n − 1)). They are replaced by (5.1) (LM + Gaussian tail)
  and (6.1). Markov on Θ^{(1)} at level e^{t} is kept; it is already an exponential-form bound.
- **R2 (the t/√n term).** It comes from E′/(2n) and |E′ − N|/(2√n) in Λ″ at deviations x ≍ t. In Corollary S.1 it costs
  C_S t/√n ≤ t/2 once n ≥ 4C_S², for every t; so the upper limit t ≤ n^{1−κ₀} is needed only for the bracket term (S.2).
- **R3 (reference-adaptivity, S-APX).** Lemma S needs only B_T(ϑ) ≤ B for a design-measurable (T, ϑ); μ need not lie in
  col X. With T ⊊ S₀ (weak coefficients dropped) the cutoff uses |T| < s₀ (cf. `B_tail_approx.md:51-53`).
- **R4 (S-EXP).** No step uses p ≤ n^A. In S.1, log R^{S₀}_m carries s₀ log(2p) exactly, which m_n(t) pays.
- **R5 (c♯ explicit).** With the bound on c_IG above: log c♯ ≤ 2·0.51·log(b₊/b₋) + log Γ(0.51) + b₊/σ*² + 1.51 log 2 + 0.51 log(σ*²/b₊);
  all terms are explicit in (σ*², M).
- **R6 (numerics).** `c_checks.py` check_S: (3.1) by quadrature (60 draws, n ∈ {20, 40, 80}, a truth with a component
  orthogonal to col X, a duplicated column in a third of the draws) and the assembled inequality (4.1) by exact
  enumeration of all models (p = 8) on 𝓑_n, for every m ≥ |T|. check_Bn_tail: Monte Carlo of P(𝓑_nᶜ) against (6.1)
  (the bound is far from tight for small n; it is only needed as an exponential rate). Results: `c_checks_out.txt`.
