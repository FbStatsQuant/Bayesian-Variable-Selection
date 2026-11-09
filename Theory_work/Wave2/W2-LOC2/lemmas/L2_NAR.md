# L2 — Key Lemma NA-R: no-addition on a polylogarithmic lattice via references and atoms

Status: **PROVED (by this seat, unchecked)**. Falsification numerics: `numerics/n4_nar_check.py` → `numerics/n4_out.txt`
(Part 2: collinearity check of the Step-1 identity — cosine deficit between (I − P_T)x_l and (I − P_T)Ce_{T,l} ≤ 5.6e-16
[R07-8]; the decomposition bound of Step 3 holds in every tested (T, l); max ‖Cr‖/‖Ce‖ ≤ 1.0009; the magnitude difference
| |Z| − |Z^pop| | decreases with n, below |Q|/√n; the analytic identity does not depend on this check). Check record: R03 (Codex gpt-6.1-sol xhigh, `reviews/R03_L2_check_sol.md`): VERIFIED-WITH-AMENDMENTS (1 MAJOR, 1 MINOR, 1 NIT; no FATAL, no counterexample to locked (B)); all applied (`reviews/R03_disposition.md`).

## L2.0 Setting and hypotheses

Notation as GROW L0/L2 and APP L3.0. N := n − 1; C := I − 11ᵀ/n. Raw W (n × p), rows iid N(0, Σ) (WLOG mean 0, APP
L3.0 zero-mean reduction); X = CW diag(1/t_j), t_j := ‖CW_j‖/√N; Y = Xθ* + Cε, ε ~ N(0, σ²I_n) independent of W.
For T ⊆ [p], P_T := orthogonal projection onto span X_T (= span CW_T). For T ∌ l with (I − P_T)x_l ≠ 0:
u_{T,l} := (I − P_T)x_l/‖(I − P_T)x_l‖ and Z_{T,l} := u_{T,l}ᵀε/σ (GROW L2.0 (F2)).

**Latent extension** [R01-2]. For each n a fixed centred jointly Gaussian law on ℝ^{p+p′} (p′ = p′_n arbitrary) whose
first p coordinates have law N(0, Σ_n); the n rows of (W, Ξ) are sampled iid from it, and the whole extension (W, Ξ) is
independent of the entire noise vector ε. A *functional* is a deterministic φ ∈ ℝ^{p+p′} (a fixed linear map, not fitted
to data); it defines the random n-vector 𝒲φ := (W, Ξ)φ (rowwise evaluation) with iid N(0, Var φ) entries,
Var φ := φᵀΣ^{ext}φ; sample comparisons use C𝒲φ. All coefficients below, L_n and η_n are deterministic. No independence
among frame members, atoms or W is assumed.

**Hypotheses (N0)–(N1), (R1)–(R3)** (all objects deterministic, may depend on n; κ, m₀, c fixed):
* (N0) p ≤ n^A; S₀ ⊆ Q ⊆ [p]; q := |Q| ≤ (log n)^κ; q ≤ K_n = min(p, ⌊n/2⌋) (so every T ∈ 𝓛 := {T : S₀ ⊆ T ⊆ Q} is
  feasible).
* (N1) λ_min(Σ_{Q∪{l}}) ≥ c > 0 for every l ∈ [p].
Let 𝔓 := {(T, l) : T ∈ 𝓛, l ∈ [p] ∖ T}; for (T, l) ∈ 𝔓, β_{T,l} := Σ_TT⁻¹Σ_{Tl}, e_{T,l} := W_l − W_Tβ_{T,l},
τ²_{T,l} := Var(W_l | W_T) (the common variance of the iid entries of e_{T,l}). By (N1), τ²_{T,l} ≥ c.
* (R1) *References.* A family of N_n *frames*, each a list of at most m₀ functionals, with
  log N_n ≤ log p + o(log n); for every (T, l) ∈ 𝔓 a frame ι(T, l) and a functional ψ_{T,l} in the linear span of
  that frame's functionals; put r_{T,l} := 𝒲ψ_{T,l}, ϱ²_{T,l} := Var ψ_{T,l}.
* (R2) *Atoms.* A set 𝒜_n of functionals with Var a ≤ 1 (a ∈ 𝒜_n; no cardinality bound beyond the display below), and
  coefficients
  λ_{T,l} ∈ ℝ^{𝒜_n} with
    e_{T,l} = r_{T,l} − Σ_{a∈𝒜_n} λ_{T,l,a} 𝒲a  for every (T, l) ∈ 𝔓,
  L_n := max_𝔓 ‖λ_{T,l}‖₁, and L_n² log(|𝒜_n| + 1) = o(log n) (the locked (R2); R03-1).
* (R3) *Variance ratio.* ϱ²_{T,l} ≤ (1 + η_n)τ²_{T,l} for all (T, l) ∈ 𝔓, with η_n → 0.

**Lemma NA-R.** Under (N0)–(N1), (R1)–(R3): with c_n := log(n + 1) + 2 log p − 2 log(|Q| + 1) − 4κ_E − 2 (GROW
L2.2; κ_E the constant of the common score expansion, L0/L0′), P(Z_{T,l} is defined and Z²_{T,l} ≤ c_n for all
(T, l) ∈ 𝔓) → 1 (vacuous if 𝔓 = ∅); Z_{T,l} is formed from the SAMPLE normalised residual u_{T,l} (GROW L2.0).
Combined with GROW L2.2 on the L0′ event of the lattice family (L1_toolkit §L1.1), P(NA(𝓛)) → 1.

No independence between different frames, atoms, or (T, l) pairs is used; frames and atoms may involve latent
coordinates that are not columns of X.

## L2.1 Proof

Put ℓ_𝔓 := log|𝔓| ≤ log p + |Q| log 2 ≤ A log n + (log n)^κ (κ ≥ 1 WLOG, as in L1_toolkit); all statements below are
for n ≥ n₀, n₀ depending only on (A, κ, m₀, c, κ_E, the sequences in (R1)–(R3)) [R03-3]. Rates used:
x, v_n = O(q + log n), δ_n = O(√((q + log n)/n) + (q + log n)/n), ω′_n = O((q + log n)/n), ϵ_n = O((q + log n)/√n),
all → 0 because q ≤ (log n)^κ.

If 𝔓 = ∅ (Q = S₀ = [p]) there is nothing to prove; assume 𝔓 ≠ ∅.
**Step 1 (exact identity).** Fix (T, l) ∈ 𝔓. Almost surely X_{T∪{l}} has full column rank (the rows of W_{T∪{l}}
are iid nondegenerate Gaussian by (N1) and N ≥ |T| + 1 for n ≥ n₀; a.s. CW_{T∪{l}} has full rank), so
(I − P_T)x_l ≠ 0 and Z_{T,l} is defined; there are finitely many pairs, so this holds simultaneously a.s. Since
W_l = W_Tβ_{T,l} + e_{T,l}, CW_l = CW_Tβ_{T,l} + Ce_{T,l} with CW_Tβ_{T,l} ∈ span X_T, hence
(I − P_T)x_l = t_l⁻¹(I − P_T)Ce_{T,l}. Because range P_T ⊆ 1^⊥, P_TC = P_T. With g := Ce_{T,l} and
h := (I − P_T)g = g − P_Te_{T,l} (so h ⊥ P_Tg = P_Te_{T,l} and ‖h‖² = ‖g‖² − ‖P_Te_{T,l}‖²):
  u_{T,l} = h/‖h‖ (t_l > 0),   σZ_{T,l} = hᵀε/‖h‖ = (gᵀε − (P_Te_{T,l})ᵀP_Tε)/‖h‖.        (2.1)

**Step 2 (events).** Let x := ℓ_𝔓 + 2 log n and δ_n := 2√(x/N) + 2x/N → 0 (x = O((log n)^κ)).
* E_a: for all (T, l) ∈ 𝔓, |‖Ce_{T,l}‖²/(τ²_{T,l}N) − 1| ≤ δ_n and ‖Cr_{T,l}‖² ≤ ϱ²_{T,l}N(1 + δ_n).
  (Ce_{T,l}/τ_{T,l} and, if ϱ_{T,l} > 0, Cr_{T,l}/ϱ_{T,l} are the images under the rank-N projection C of vectors
  with iid N(0, 1) entries, so their squared norms are χ²_N; Laurent–Massart, P(χ²_N − N ≥ 2√(Nx) + 2x) ≤ e^{−x},
  P(N − χ²_N ≥ 2√(Nx)) ≤ e^{−x}; union over 3|𝔓| events: P(E_aᶜ) ≤ 3e^{ℓ_𝔓}e^{−x} = 3n^{−2}. If ϱ = 0, Cr = 0.)
* E_b: ‖P_Te_{T,l}‖² ≤ τ²_{T,l}v_n for all (T, l) ∈ 𝔓, v_n := 4(ℓ_𝔓 + |Q| + 2 log n).
  (Gaussian regression: in each row, e_{T,l,i} = W_{il} − W_{iT}β_{T,l} is independent of W_{iT}; rows are iid; hence
  the vector e_{T,l} is independent of the matrix W_T and has iid N(0, τ²_{T,l}) entries. P_T is a function of W_T,
  of rank d ≤ |T| ≤ |Q|. Conditionally on W_T, ‖P_Te_{T,l}‖²/τ² ~ χ²_d, and P(χ²_d > v) ≤ 2^{d/2}e^{−v/4}
  (mgf at ¼); at v = v_n this is ≤ 2^{|Q|/2}e^{−ℓ_𝔓−|Q|}n^{−2} ≤ |𝔓|⁻¹n^{−2}. Union over 𝔓: P(E_bᶜ) ≤ n^{−2}.)
* E_c: ‖P_Qε‖² ≤ 4σ²(|Q| + log n). (Conditionally on X, ‖P_Qε‖²/σ² ~ χ²_{rank P_Q}, rank ≤ |Q|; the same mgf bound
  gives P(E_cᶜ) ≤ 1/n.) Since span X_T ⊆ span X_Q, ‖P_Tε‖ ≤ ‖P_Qε‖ for every T ∈ 𝓛.
* E_d: for every frame ι, with 𝒮_ι := span{C𝒲φ : φ in frame ι} (dimension ≤ m₀), ‖P_{𝒮_ι}ε‖² ≤ σ²x′_n,
  x′_n := 2 log N_n + (m₀ + 2) log log n.
  (𝒮_ι is (W, Ξ)-measurable and ε is independent of (W, Ξ); conditionally, ‖P_{𝒮_ι}ε‖²/σ² ~ χ²_{dim 𝒮_ι}, which is
  stochastically ≤ χ²_{m₀}; Chernoff: P(χ²_{m₀} ≥ x) ≤ (ex/m₀)^{m₀/2}e^{−x/2} for x ≥ m₀. With x = x′_n
  (= O(log n) by (R1) and p ≤ n^A): N_n·P ≤ (ex′_n/m₀)^{m₀/2}(log n)^{−(m₀+2)/2} = O((log n)^{−1}) → 0.)
* E_e: ‖Cε‖² ≤ 2σ²N, and for every a ∈ 𝒜_n: |(C𝒲a)ᵀε| ≤ y_n‖Cε‖, with the adaptive threshold [R03-1]
  M_n := |𝒜_n|, b_n := √(log n/(1 + L_n²)), y_n² := 2 log(2(M_n + 1)) + 2b_n.
  (If M_n ≥ 1, (R2) gives L_n² = o(log n); if M_n = 0, L_n = 0; so b_n → ∞, and
  L_n²b_n/log n = L_n²/(√(1 + L_n²)√log n) ≤ L_n/√log n → 0. Conditionally on ε — the whole extension is independent of
  ε and C is symmetric — (C𝒲a)ᵀε = (𝒲a)ᵀ(Cε) = Σ_i(𝒲a)_i(Cε)_i ~ N(0, Var(a)‖Cε‖²), Var a ≤ 1; Gaussian union bound
  given ε: P(max_a|(C𝒲a)ᵀε| > y_n‖Cε‖ | ε) ≤ M_n·2e^{−y_n²/2} = (M_n/(M_n + 1))e^{−b_n} ≤ e^{−b_n} → 0. ‖Cε‖²/σ² ~ χ²_N and P(χ²_N > 2N) ≤ e^{−N/8}
  (Laurent–Massart, x = N/8). No cardinality bound on 𝒜_n and no atom-norm concentration is used [R01 suggestion].)
P(E_a ∩ … ∩ E_e) → 1. Work on this intersection.

**Step 3 (population statistic).** Let Z^pop_{T,l} := gᵀε/(σ‖g‖) (g = Ce_{T,l} ≠ 0 on E_a). By (R2),
g = Cr_{T,l} − Σ_a λ_{T,l,a}C𝒲a, and Cr_{T,l} ∈ 𝒮_{ι(T,l)} by (R1). Hence, on E_d and E_e,
  |gᵀε| ≤ |(Cr)ᵀP_{𝒮_ι}ε| + Σ_a |λ_{T,l,a}||(C𝒲a)ᵀε| ≤ σ‖Cr_{T,l}‖√x′_n + L_ny_n‖Cε‖
       ≤ σ‖Cr_{T,l}‖√x′_n + σL_ny_n√(2N).
On E_a, with (R3) and τ² ≥ c: ‖Cr‖²/‖g‖² ≤ (1 + η_n)(1 + δ_n)/(1 − δ_n) =: 1 + η′_n (η′_n → 0) and
‖g‖² ≥ cN(1 − δ_n) ≥ cN/2. Therefore, uniformly over 𝔓,
  |Z^pop_{T,l}| ≤ √((1 + η′_n)x′_n) + L_ny_n√(4/c) =: ζ_n.                                          (2.2)

**Step 4 (sample vs population).** From (2.1), |Z_{T,l}| ≤ |Z^pop_{T,l}|·‖g‖/‖h‖ + ‖P_Te‖‖P_Tε‖/(σ‖h‖). On E_a ∩ E_b,
‖h‖² = ‖g‖² − ‖P_Te‖² ≥ τ²(N(1 − δ_n) − v_n) ≥ τ²N/2 (v_n = O((log n)^κ)), so
‖g‖/‖h‖ ≤ (1 − v_n/(N(1 − δ_n)))^{−1/2} =: 1 + ω′_n with ω′_n → 0, and on E_c
  ‖P_Te‖‖P_Tε‖/(σ‖h‖) ≤ τ√v_n·2√(|Q| + log n)/(τ√(N/2)) = 2√2·√(v_n(|Q| + log n)/N) =: ϵ_n → 0
(ϵ_n = O((log n)^κ/√n)). Hence |Z_{T,l}| ≤ (1 + ω′_n)ζ_n + ϵ_n for all (T, l) ∈ 𝔓.

**Step 5 (threshold; one-sided bounds only [R03-2]).** By (R1), x′_n ≤ 2 log p + o(log n) and x′_n = O(log n). By (R2)
and E_e's choice, L_n²y_n² = 2L_n²log(2(M_n + 1)) + 2L_n²b_n = o(log n), i.e. B_n := L_ny_n√(4/c) = o(√log n). Since
η′_n → 0, expanding ζ_n = √((1 + η′_n)x′_n) + B_n:
  ζ_n² = (1 + η′_n)x′_n + 2√((1 + η′_n)x′_n)B_n + B_n² ≤ 2 log p + o(log n),  ζ_n² = O(log n).
With ω′_n, ϵ_n → 0, the exact expansion
  ((1 + ω′_n)ζ_n + ϵ_n)² = ζ_n² + (2ω′_n + ω′_n²)ζ_n² + 2(1 + ω′_n)ζ_nϵ_n + ϵ_n² ≤ 2 log p + o(log n)
is a deterministic uniform upper bound on the common event. On the other hand
c_n − 2 log p ≥ log n − 2 log((log n)^κ + 1) − 4κ_E − 2 = log n − O(log log n). Hence max_𝔓 Z²_{T,l} ≤ c_n for n ≥ n₀ on
E_a ∩ … ∩ E_e. ∎

## L2.2 Remarks
1. *What replaces the 2^{|Q|} union.* The only unions over 𝔓 (E_a, E_b) use thresholds x, v_n = O(q + log n); they enter
   through the relative errors δ_n, ω′_n AND the additive comparison error ϵ_n = O((q + log n)/√n), all → 0 in the
   polylogarithmic setting here (an extension to larger q must control ϵ_n separately) [R03-3]. The unions that must be sharp at the
   √(2 log p) scale run over frames (E_d: ≤ p·n^{o(1)} subspaces of dimension ≤ m₀ — the whole subspace of each frame is
   controlled, not one chosen direction) and atoms (E_e, weighted by L_n), never over the lattice. For comparison
   [R07-1]: GROW L2.3(a) charges one common χ²_{|𝒫|} projection (needs |𝒫| ≤ (1 − δ₀) log n); GROW L6.6 uses
   ≤ p(q + 1)² AR(1) reference innovations; APP L3.6 uses p·e^{O(log log n)} window references and bounds the far part
   through ‖D‖·‖P_Tε‖, with a contribution of order √(q·κ(r_n)) — stated there for q = O(log n), and possibly retunable
   (larger r_n) for polylog q in the exponential case. NA-R is a different sufficient construction (atoms bounded
   atom-by-atom, conditionally on ε), which also covers one-factor groups and, re-run in L6, polynomial q; no claim is made
   that the earlier routes necessarily fail. In general the remainder is o_P(√log n), not O(√log|Q|).
2. *Sharpness of the L_n condition.* If L_n²log|𝒜_n| were ≍ log n, the bound ζ_n² = 2 log p + Θ(log n) could exceed c_n;
   the condition is what makes the atom part lower order. For the classes of L4, L_n is bounded and |𝒜_n| ≤ |Q|.
3. The conclusion is a joint design/noise limit (frame tails conditional on the extension, atom tails conditional on ε, then integrated); no uniform-in-design guarantee is claimed [R03]. It
   does not use PTV, the partition, or the signal.
