# W3-SCR — STATEMENT (certified screening; PROGRAM item 5)

Status: **v3.4** = v3.2 (LOCKED by R05c) + wording/notation fixes of the mid-point R06 and the sweep R07 (v3.3, the
version scored by council C1: Astra 9.3, Opus 8.9, all gates PASS) + the council's post-pass edits (M6 prose; "κ, b,
M fixed" made explicit in A1 / SCR-G; M_𝓗 renamed). No conclusion or constant changed. v2 (= v1 + all fixes of the statement-lock review R01 + the self-normalised refinement SCR-A°) was
LOCKED by R01b. v3 adds, from the better-theorem review R02 (sharpness gate): the master gap theorem SCR-M with a
geometric noise complexity, its corollary SCR-G for uncertified runs, the directional floor φ^d, the (α, ω) form of
the excess-set inequality; and the minor fixes of the lemma checks R03, R04. Nothing locked in v2 is weakened.
Lead: Claude Fable 5.2 (W3-SCR). Target card: `Theory_work/Wave3/PROGRAM.md:26-27`; origin
`Theory_work/Wave2/SR/BLIND_fable.md:154-164` (Thm 5), `Theory_work/Wave2/SR/CRITIQUE_fable.md:67-70, 245`.

## 0. Setting

**Model G (fixed standardised design, triangular array).** n ≥ 3, p ≥ 1 (p ≥ 2 in asymptotic statements) is the number
of retained (nonconstant) columns. X ∈ R^{n×p} is the standardised design (columns centred, ‖x_j‖² = n−1), treated as
deterministic. y_c := C y^r = μ + Cε with C = I − 11ᵀ/n, μ = Xθ*, ε ~ N_n(0, σ²I), σ² > 0 (σ may depend on n; every
bound below is explicit in σ). S₀ = supp θ*, s₀ = |S₀| ≥ 1, θ_min := min_{t∈S₀}|θ*_t|. The method uses y = y_c/τ̂ with
τ̂² = ‖y_c‖²/(n−1) (> 0 a.s.), so y′y = n−1. K = min(p, ⌊n/2⌋), Ω = {S ⊆ [p] : |S| ≤ K}.
This is the setting of `Theory_work/Wave1C/FINAL/sections/s1_setting.tex:7-24`, **except** that s₀ and p are not
restricted (the chapter fixes s₀ and takes p ≤ n^A) and σ = σ_n > 0 may vary with n (the chapter fixes σ); where a
result needs s₀ bounded, p polynomial or σ fixed it says so.
Random designs are covered only by conditioning on X (errors independent of X) and checking the design conditions on
the realised standardised X.

**Score.** With G_S = X_SᵀX_S, z_S = X_Sᵀy, H_S = (n+1)G_S + I, Q_S = y′y − n z_SᵀH_S^{-1}z_S, ν = 0.01 + n/2:
F(S) = log w(|S|) − ½ log det H_S + ½ log det(G_S + I) − ν log(0.02 + Q_S) + const, w(k) = [2 C(2p−1, k)]^{-1}.

**Coded neighbourhood and local optimality.** For C ∈ Ω, 𝒩(C) is the set of models obtained from C by one deletion,
one addition (only if |C| < K) or one swap. C is **locally optimal (LO)** if F(N) ≤ F(C) for every N ∈ 𝒩(C).

**Coded certificate (CODE_CHECK.md, CC1-CC4).** `fit$local_certified = TRUE` implies: the output event 𝒪 holds
(status `completed` or `exact`) and the reported model Ŝ = `fit$hpm` is LO (on the SMC branch it is a certified
scanned centre of the final local search or of LS0; on the enumeration branch it is the enumerated maximiser of F
over Ω). The **set 𝒞 of certified models of a fit** is: ∅ if the status is neither `completed` nor `exact`; {Ŝ} if
the status is `exact`; and, if the status is `completed`, the set of the endpoints `returned` of those search archives
(`fit$local_search`, `fit$ls0`) whose own `local_certified` is TRUE. Every element of 𝒞 is LO, and
`fit$local_certified` ⇒ Ŝ ∈ 𝒞. An intersection over an empty family of models is [p].
**Scanned centres (CODE_CHECK CC6).** On a completed run, a *scanned centre* is a completely scanned centre of a
search that was run: `fit$local_search`, and `fit$ls0` when LS0 is enabled (the default) (printed with its score in
`scanned_centres`, `scanned_F`). Every model of the coded
neighbourhood of a scanned centre was scored and reached the ledger, so F(Ŝ) ≥ F(N) for each such N. A search that
stops on its move cap returns the best scanned neighbour N of its last scanned centre C, with F(N) > F(C).
Model indices are those of the retained columns (raw-index output uses the inverse of the retained-column map).

**Premise.** EX-A (exact scores and arithmetic; a named idealisation, as in the chapter — the coded flags apply no
numerical error margin). Nothing else: no premise on the uniforms, the calibration, the start mode, leakage, or the
blocks. All statements hold for every seed. q always denotes an integer in {0, …, K−1}.

## 1. Quantities (functions of (X, θ*, σ) only)

λ₀ := 1/(n+1). For S ⊆ [p] let R_S := I_n − X_S(G_S + λ₀I)^{-1}X_Sᵀ (ridge residual operator; R_∅ = I; 0 ≺ R_S ⪯ I).
For t ∉ S:
- a(t|S) := x_tᵀR_S x_t + λ₀ (∈ (0, n));
- **noiseless gain** γ(t|S) := (x_tᵀR_S μ)² / a(t|S). It is the decrease of the method's own quadratic form when t is
  added to S and the response is replaced by its mean: γ(t|S) = ((n+1)/n)(Q^μ_S − Q^μ_{S∪t}),
  Q^μ_S := μᵀμ − n μᵀX_S H_S^{-1}X_Sᵀμ.
- **residual scale** of S: σ_S² := σ² + μᵀR_Sμ/(n−1) (noise variance plus unexplained mean energy);
  τ_n² := σ_∅² = σ² + ‖μ‖²/(n−1); σ ≤ σ_S ≤ τ_n.
- **Sparse visibility** Γ_n(q) := min{ max_{t∈S₀∖S} γ(t|S) : S ⊆ [p], |S| ≤ q, S ⊉ S₀ } and its **normalised** form
  Ψ_n(q) := min{ max_{t∈S₀∖S} γ(t|S)/σ_S² : S ⊆ [p], |S| ≤ q, S ⊉ S₀ } (≥ Γ_n(q)/τ_n²).
- T_n := (1 + 1/n)(2 log(2p−1) + log(n+1)); N_q := Σ_{k=0}^{q} C(p,k); r_n(q,x) := (2 log(2N_q) + 2x)^{1/2};
  a_x := √(x/(n−1)); τ̄_n(x) := τ_n(1 + 2a_x);
  ϑ°_n(q,x) := 2a_x + 2a_x² + r_n(q,x)/√(n−1) + 1.02(n+1)τ̄_n(x)²/(n(n−1)σ²).

**Margin conditions.**
 MC(q, x):  √Γ_n(q) > τ̄_n(x)·√T_n + σ·r_n(q, x).
 MC°(q, x): √Ψ_n(q) > √(T_n(1 + ϑ°_n(q, x))) + r_n(q, x).

Primitive design quantities used by the bridges and by SCR-C / SCR-R:
- identifiability margin Δ_n(q) := min{ ‖(I − P_S)μ‖² : |S| ≤ q, S ⊉ S₀ } (P_S = orthogonal projector on span X_S);
- anchored floor φ^a_n(q) := min{ λ_min(X_Tᵀ(I − P_S)X_T)/(n−1) : |S| ≤ q, S ⊉ S₀, T = S₀∖S };
- directional floor φ^d_n(q) := min{ ‖(I − P_S)X_Tθ*_T‖²/((n−1)‖θ*_T‖₂²) : |S| ≤ q, S ⊉ S₀, T = S₀∖S } (≥ φ^a_n(q); only
  the realised combination of the missing true columns must keep a fraction of its energy outside span X_S);
- superset floor φ_n(q) := min{ λ_min(G_S)/(n−1) : S ⊇ S₀, |S| ≤ q } (:= +∞ if q < s₀; then SCR-C, SCR-R are vacuous).
  A sparse eigenvalue floor κ on all sets of size ≤ q + s₀ gives φ^a_n(q) ≥ κ and φ_n(q + s₀) ≥ κ (Lemma B3).

## 2. Results

### Theorem SCR-A (certified screening) — the target, non-asymptotic
Model G, EX-A. Let q ∈ {0, …, K−1} and x > 0 satisfy MC(q, x). Then there is an event 𝓔_A with P(𝓔_A) ≥ 1 − 3e^{-x} on
which **every LO model S with |S| ≤ q contains S₀**. Consequently

  P( 𝒪 ∩ {`local_certified`} ∩ {|Ŝ| ≤ q} ∩ {S₀ ⊄ Ŝ} ) ≤ P( ∃ C ∈ 𝒞 : |C| ≤ q, S₀ ⊄ C ) ≤ 3e^{-x};

on 𝓔_A, S₀ is contained in the intersection of all certified models of size ≤ q.

**(A∞).** Let q_n ∈ {0, …, K−1}, n → ∞, and
  liminf_n √Γ_n(q_n) / [ τ_n·√(2 log p + log n) + σ·√(2 q_n log p) ] > 1.
Then P(𝒪 ∩ {`local_certified`} ∩ {|Ŝ| ≤ q_n} ∩ {S₀ ⊄ Ŝ}) → 0 (and likewise for 𝒞). No condition p ≤ n^A, no bound
on s₀, no condition on the start mode, leakage, blocks, or on the mutual collinearity of the non-true columns is used.

### Theorem SCR-A° (self-normalised refinement)
Model G, EX-A. Let q ∈ {0, …, K−1} and x > 0 satisfy MC°(q, x). Then there is an event 𝓔_A° with
P(𝓔_A°) ≥ 1 − 4e^{-x} on which every LO model S with |S| ≤ q contains S₀; the two probability bounds of SCR-A hold
with 4e^{-x}.
**(A°∞).** If q_n log p = o(n), ‖μ‖ = o(nσ), and liminf_n √Ψ_n(q_n) / [√(2 log p + log n) + √(2 q_n log p)] > 1, then
the probabilities in (A∞) tend to 0. (Here each missing truth competes against the residual scale σ_S of the model at
hand, not against the total scale τ_n: the signal of truths already in S enters σ_S only through ridge shrinkage
(attenuated, not removed: an included orthogonal truth with coefficient A contributes A²/n² to σ_S²), while strong
truths that are still missing contribute fully, through the unexplained mean energy μᵀR_Sμ; the term in τ̄_n of ϑ°_n
also retains a dependence on the total signal.)

### Theorem SCR-M (master gap theorem; deterministic families; geometric noise complexity) — proved in L7
Let 𝓗 be a family of models of size ≤ K−1 that is a function of (X, θ*, σ) only, 𝓗⁻ := {S ∈ 𝓗 : S ⊉ S₀}, M_𝓗 := |𝓗⁻|,
and t(S) ∈ S₀∖S a witness depending on (X, θ*, σ) only; the **maximising witness** is the smallest index maximising
γ(·|S) over S₀∖S (any deterministic witness is allowed in the theorem; M3, M4 and SCR-G use the maximising one). With
the unit-ball vectors d_S (signed witness direction R_Sx_t/a(t|S)^{1/2}) and e_S (R_Sμ normalised) of L7, the Gaussian width w(𝓓) := E max_{d∈𝓓∪{0}} dᵀg, g ~ N(0, I_n), and
 b_𝓗(x) := min{√(2 log M_𝓗 + 2x), w({d_S}) + √(2x)},  c_𝓗(x) := min{√(2 log M_𝓗 + 2x), w({e_S}) + √(2x)},
define for S ∈ 𝓗⁻ (k = |S|, t = t(S), m_S² = μᵀR_Sμ, D(t|S) := (n+1)a(t|S)/a_1(t|S) ∈ [1, n+1] the determinant ratio of L1,
a_1(t|S) := x_tᵀ[I − X_S(G_S + I)^{-1}X_Sᵀ]x_t + 1):
 B_S := log((2p−1−k)/(k+1)) + ½ log D(t|S);  g⁻_S := (√γ(t|S) − σ b_𝓗(x))₊² (a scalar lower bound for the gain);
 U_S := 1.02τ̄_n(x)² + (n/(n+1))[m_S² + 2σ m_S c_𝓗(x) + σ²(n−1)(1 + 2a_x + 2a_x²)];  Ū_S := min{U_S, (n−0.98)τ̄_n(x)²};
 u_S := n g⁻_S/((n+1)Ū_S);  **δ_S := −ν log(1 − u_S) − B_S** (:= +∞ if u_S ≥ 1);  δ_𝓗 := min_{S∈𝓗⁻} δ_S.
Conventions: δ_S := +∞ for S ∈ 𝓗∖𝓗⁻; if 𝓗⁻ = ∅ then δ_𝓗 := +∞ and b_𝓗, c_𝓗 are not used (everything is vacuous).
Model G, EX-A, x > 0. There is an event 𝓔_M with P(𝓔_M) ≥ 1 − 4e^{-x} on which **F(S ∪ t(S)) − F(S) ≥ δ_S for every
S ∈ 𝓗⁻** (and S ∪ t(S) ∈ 𝒩(S)). Consequently, on 𝓔_M:
- (M1) if δ_S > 0 for all S ∈ 𝓗⁻, every LO model in 𝓗 — in particular every certified model in 𝓗 — contains S₀;
- (M2) every scanned centre C ∈ 𝓗⁻ has F(Ŝ) − F(C) ≥ δ_C; hence every scanned centre C ∈ 𝓗 with F(Ŝ) − F(C) < δ_𝓗
  contains S₀ (no certificate needed);
- (M5) if δ_S > 0 for all S ∈ 𝓗⁻: when a search moves (or, on its move cap, returns) from a scanned centre C ⊇ S₀ to
  its best neighbour N ∈ 𝓗, then N ⊇ S₀ — the coded search does not drop truths inside 𝓗.
(M3) For 𝓗 = {|S| ≤ q} **with the maximising witness**: MC(q, x) ⇒ δ_S > 0 for all S ∈ 𝓗⁻, and MC°(q, x) ⇒ δ_S > 0
for all S ∈ 𝓗⁻; so SCR-A and SCR-A° are special cases (with b_𝓗, c_𝓗 ≤ r_n). (For another witness these implications
can fail: visibility controls the largest missing-truth gain, not every one.) (M6) b_𝓗 has an upper bound that involves
only the geometry of the witness directions and not the number of models: b_𝓗(x) ≤ √(dim span{d_S}) + √(2x) (b_𝓗 itself
is the smaller of this kind of geometric bound and the counting bound). A low-dimensional witness span lowers b_𝓗, and M1 then applies to
larger families **provided the resulting gaps δ_S are positive** (geometry alone does not make them positive: the
signal must still exceed the threshold). Illustration (L7, M6): S₀ = {1}, x_1 orthogonal to all other columns, θ*_1 ≠ 0
fixed (not depending on n), σ fixed, x fixed, log p = o(n): then δ_S > 0 for all models of size ≤ K−1 missing the truth, for all large n, with
no entropy term q log p.

### Corollary SCR-G (uncertified runs: near-best scanned centres and capped searches) — proved in L7 (M2, M4, M5)
Assume the hypotheses of Corollary A1 below (κ, b, M, σ fixed) and (q_n + 1) log p + log n = o(n), and let
c₂ := κ²b²/(104(M² + σ²)) (M is the bound on ‖θ*‖₁ of A1; SCR-M is applied with 𝓗 = {|S| ≤ q_n} and the maximising
witness).
Then with probability → 1, on every completed run:
 (i) every scanned centre C with |C| ≤ q_n and `hpm_F` − F(C) ≤ c₂n contains S₀;
 (ii) if a search stopped on its move cap (its own archive has `termination = "move_limit"`) with last scanned
 centre C and returned model N, both of size ≤ q_n, and `hpm_F` − F(C) ≤ c₂n, then N ⊇ S₀ — in particular Ŝ ⊇ S₀ when
 Ŝ = N, even if the top-level `local_certified` is FALSE (the capped search itself is uncertified; the top-level flag
 can still be TRUE when the other search certified the same model);
 (iii) along either search path, once a scanned centre contains S₀, so does every later model of the path, as long
 as the sizes stay ≤ q_n.
(The certified case is `hpm_F` − F(C) = 0 with C = Ŝ. Under these hypotheses the deterministic gap δ of SCR-M
exceeds c₂n for all large n, L7 M4.)

### Lemma B (bridges: primitive conditions give lower bounds for visibility)
Let c_θ := ‖θ*‖₂/√(n+1).
(B1, identifiability margin.) If Δ_n(q) ≥ c_θ², then Γ_n(q) ≥ Δ_n(q)·(√Δ_n(q) − c_θ)² / (n ‖θ*‖₁²).
(B2, anchored floor.) Δ_n(q) ≥ φ^a_n(q)(n−1)θ_min², and if √(φ^a_n(q)(n−1))·θ_min ≥ c_θ, then
  Γ_n(q) ≥ (φ^a_n(q)(n−1)/n)·(√(φ^a_n(q)(n−1))·θ_min − c_θ)².
(B2°.) If √(φ^a_n(q)(n−1))·θ_min ≥ 2c_θ, then
  Ψ_n(q) ≥ ((n−1)²/n)·φ^a_n(q)²θ_min² / (4σ² + 9φ^a_n(q)·s₀·θ_min²).
(B2d.) B2 and B2° hold with the directional floor φ^d_n(q) (≥ φ^a_n(q)) in place of φ^a_n(q).
(B3.) A sparse eigenvalue floor κ on all sets of size ≤ q + s₀ implies φ^a_n(q) ≥ κ and φ_n(q + s₀) ≥ κ.
These are lower bounds for Γ_n, Ψ_n; the coefficient-size and growth conditions that make MC / MC° hold are in A1, A1°.

**Corollary A1 (the PROGRAM statement).** Assume φ^d_n(q_n) ≥ κ > 0 (in particular: φ^a_n(q_n) ≥ κ; in particular: a
sparse eigenvalue floor κ on all sets of size ≤ q_n + s₀), θ_min ≥ b > 0, ‖θ*‖₁ ≤ M, with κ, b, M, σ fixed (not
depending on n), q_n ∈ {0, …, K−1} and
  (q_n + 1)·log p + log n ≤ c₁ n,  c₁ := κ²b² / (200(M² + σ²)).
Then P(𝒪 ∩ {`local_certified`} ∩ {|Ŝ| ≤ q_n} ∩ {S₀ ⊄ Ŝ}) → 0 (and likewise for 𝒞). In particular this holds for
p ≤ n^A and every q_n = o(n / log n), q_n ≤ K−1; the admissible q_n go up to order n / log(p ∨ n).

**Corollary A1° (beta-min at the rate σ√(𝐋_n/n); no fixed bound on the total signal).** Assume φ^d_n(q_n) ≥ κ > 0,
q_n ∈ {0, …, K−1}, and with 𝐋_n := (q_n + 1) log p + log n:
 𝐋_n = o(n); θ_min ≥ 16σκ^{-1}√(𝐋_n/n); s₀·𝐋_n ≤ κn/576; ‖θ*‖₂ ≤ ½√(κ(n²−1))·θ_min; ‖μ‖ = o(nσ).
Then the same conclusion holds. (For bounded q_n and log n = O(log p) the beta-min is of order σ√(log p/n). The
total signal is still restricted by ‖μ‖ = o(nσ) and by the condition on ‖θ*‖₂/θ_min.)

### Theorem SCR-C (exact recovery from the certificate under a near-orthogonality floor)
Model G, EX-A. Assume: the hypothesis of (A∞) or of (A°∞) for q_n ∈ {0, …, K−1}; **s₀ = O(1)**; ‖θ*‖₂ = O(σ√n);
q_n log p = o(n); n → ∞; and for some fixed ε > 0 and all large n
  φ_n(q_n) ≥ 2 log p / (2 log p + log n) + ε
(for p ≤ n^A it suffices that φ_n(q_n) ≥ 2A/(2A+1) + ε). Then
  P( 𝒪 ∩ {`local_certified`} ∩ {|Ŝ| ≤ q_n} ∩ {Ŝ ≠ S₀} ) ≤ P( ∃ C ∈ 𝒞 : |C| ≤ q_n, C ≠ S₀ ) → 0.
**Excess set in general designs (Lemma L5.1, non-asymptotic, any s₀).** For a strict superset S = S₀ ∪ E, m := |E|,
let α(S) be the smallest conditional length a(j|S∖j)/(n−1), j ∈ E, and ω(S) ∈ [1, m] the largest eigenvalue of the
correlation matrix of the dual directions of the excess columns (L5). Let x, x′ > 0 and let η_n(k, x) ∈ [0, 1] be the
explicit quantity of L5.1 (1 − η_n(k, x) := [(1 − 2a_x − U(k, x)/(n−1))₊^{1/2} − ‖θ*‖₂/(σ√(n²−1))]₊²,
U(k, x) := (√k + √(2 log C(p,k) + 2x))²). On an event of probability ≥ 1 − (1 + 2q)e^{-x} − e^{-x′}/(1 − e^{-x′}), every
LO strict superset S of S₀ with |S| = k ≤ q ≤ K−1 satisfies
 (EC′): (1 − η_n(k, x))(1 − 1.02/n)(2 log((2p−k)/k) + log(α(S)(n²−1)/n))₊ ≤ ω(S)·(1 + √(2 log C(p−s₀, m)/m + 2x′) + ‖θ*‖₂/(σ√(m(n+1))))².
So, intersecting with a screening event (SCR-A / SCR-A°), the excess set E of a certified model of size ≤ q is empty
or belongs to the deterministic family of sets satisfying (EC′). Writing A := (1 − η_n(k, x))(1 − 1.02/n),
Λ := 2 log((2p−k)/k) + log(α(S)(n²−1)/n) and R_m for the right-hand bracket squared, (EC′) says ω(S) ≥ A·(Λ)₊/R_m, and
for m = 1 (ω = 1) and A > 0 it is the explicit upper bound α(S) ≤ (n/(n²−1))·exp(R_1/A − 2 log((2p−k)/k)). If A = 0,
(EC′) is vacuous; for A > 0, whether these bounds are restrictive depends on their numerical values (x, x′, the
coefficient bias and the other displayed parameters); they are not claimed to force small α or large ω in general
(U(k, x) = o(n), x = o(n) and ‖θ*‖₂/(σn) = o(1) are sufficient for A → 1). No bound on |E| is claimed. With growing s₀ the floor of SCR-C is **not**
sufficient (R01 finding 2: the size prior charges log((2p−k)/k) at size k), and a condition on ω alone is not
sufficient either (R04 finding 1).

### Corollary SCR-R (accuracy of the least-squares refit on a certified model; a statement about a refit, which the
### method does not output)
Under the hypothesis of (A∞) or (A°∞): with probability → 1, every certified model C ∈ 𝒞 with 1 ≤ |C| ≤ q_n
satisfies ‖P_Cy_c − μ‖² ≤ σ²·(√|C| + √(2|C| log(ep/|C|) + 4 log n))² (least-squares fitted mean; no floor needed); and
if moreover φ_n(q_n) ≥ φ > 0, the refit θ̂_C := (G_C^{-1}X_Cᵀy_c on C, 0 elsewhere) satisfies
‖θ̂_C − θ*‖₂² ≤ that bound / (φ(n−1)).

### Proposition SCR-N (sharpness of the empty-model visibility threshold, q = 0)
Model G, EX-A. Let L_n := 2 log(2p−1) + log n and B_n := ((n+1)/n)(n − 0.98)(1 − exp(−L_n/(n + 0.02))). Let x > 0
with 4a_x ≤ 1. If
 (i) √γ(t|∅) + σ√(2 log(2s₀) + 2x) ≤ τ_n(1 − 4a_x)√B_n for every t ∈ S₀, and
 (ii) √γ(j|∅) + σ√(2 log(2p) + 2x) ≤ τ_n(1 − 4a_x)√B_n for every j ∉ S₀,
then P(∅ is LO) ≥ 1 − 4e^{-x}: the empty model is then a locally optimal model of size 0 missing every truth. Here
γ(j|∅) = (x_jᵀμ)²(n+1)/n², B_n ≤ L_n, and B_n = L_n(1 + o(1)) when log p = o(n).
Consequences (proved in L6 on explicit sequences): (1) the constant 1 in front of τ_n√(2 log p + log n) in (A∞) cannot
be lowered at q_n = 0, as a statement about LO models (it is the statement "every LO model of size ≤ q contains S₀"
that fails; no claim is made that the code then reports ∅); (2) a hypothesis on the identifiability margin of the
form Δ_n(0) ≥ C log(p ∨ n) alone (without ‖θ*‖₁ control) does not give screening: there are sequences with
Δ_n(0)/log n → ∞ along which ∅ is LO with probability → 1.

## 3. What is and is not claimed
- Claimed: SCR-A (+A∞), SCR-A° (+A°∞), SCR-M (M1-M6), SCR-G, Lemma B (B1-B3, B2°, B2d), A1, A1°, Lemma L5.1 (EC′),
  SCR-C, SCR-R, SCR-N, for the method as coded on main (CODE_CHECK.md), under Model G and EX-A.
- **Not claimed:** that the event {`local_certified`, |Ŝ| ≤ q_n} has probability → 1 (it is printed; its frequency is
  reported from numerics only); any statement when |Ŝ| = K (additions are not scanned there; a swap/deletion-based
  argument is not attempted) or outside the family 𝓗 / the size q_n; exact recovery outside the floor of SCR-C
  (supersets of S₀ can be LO under correlation — numerics N2, R01's and R04's constructions); a bound on |Ŝ∖S₀| in
  general designs; any statement about a reported model that is neither certified nor covered by SCR-G; any statement
  about PIPs, the MPM or the evidence; any floating-point guarantee. SCR-N concerns the empty-model threshold only
  (not the entropy term for q ≥ 1, and not what the code reports).
- Design-agnostic: no design family in any statement. Illustration only (not proved here, not used): for i.i.d.
  Gaussian rows whose **correlation** matrix has smallest eigenvalue ≥ c, sparse eigenvalue floors of the standardised
  design on sets of size ≤ c′n/log p are standard (Raskutti–Wainwright–Yu 2010 type results); equicorrelated and
  factor designs at p ≫ n are of this kind.
- Changes vs the card: (1) the hypothesis "sparse eigenvalue floor on sets of size q_n + s₀" is replaced by the
  functional Γ_n(q_n) (or Ψ_n(q_n)) with an explicit margin; Lemma B bounds it below by the anchored floor (which the
  sparse floor implies and which allows arbitrary collinearity among non-true columns) or by the identifiability
  margin, and A1 / A1° give explicit coefficient and growth conditions; (2) q_n may be as large as c₁n/log(p ∨ n);
  (3) the conclusion covers every certified search endpoint, and — new — uncertified runs through near-best scanned
  centres and capped searches (SCR-G); (4) fixed coefficients are relaxed to a beta-min at the rate σ√(𝐋_n/n) (A1°);
  (5) the model-count entropy is replaced by a geometric complexity in the master theorem (SCR-M); (6) the excess set
  is characterised (L5.1), with exact recovery under a near-orthogonality floor (SCR-C, s₀ bounded); (7) refit rates
  (SCR-R) and a sharpness proposition (SCR-N). The card's statement is Corollary A1.

## 4. Interface (PROTOCOL item 5)
Assumption ids: **GAP(𝓗)** positive deterministic gap δ_S > 0 on 𝓗⁻ (consumed by M1 and M5; SCR-M itself proves the
gap bound without assuming positivity, and M2 uses the model-specific gap bound and its comparison threshold);
**SV(q)** sparse visibility with margin MC and **SV°(q)** normalised visibility with margin MC° (each ⇒ GAP({|S| ≤ q})
with the maximising witness, by M3; consumed by SCR-A, SCR-A°); **ID(q)** identifiability margin, **DF(q)** directional
floor, **AF(q)** anchored floor (⇒ DF), **SF(q+s₀)** sparse floor (⇒ AF) — these enter only through Lemma B's lower
bounds for Γ_n, Ψ_n; together with the coefficient, noise and growth conditions of A1 / A1° they establish SV / SV°;
**NF(q)** near-orthogonality floor on supersets of S₀ (an additional condition, consumed only by SCR-C); **EX-A**;
**G** (Gaussian errors, fixed standardised design).
