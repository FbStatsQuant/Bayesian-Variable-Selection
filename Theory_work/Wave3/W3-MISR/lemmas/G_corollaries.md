# G — Corollary G, Corollary H, Remarks SNR, P, U (W3-MISR)

Status, one line per claim (verbatim source for the registry):
- Corollary G(a): **PROVED (by this seat, unchecked)**
- Corollary G(b): **PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1, W3-POST2:A0**
- Corollary H: **PROVED (by this seat, unchecked), conditional on W3-POST2:D, W3-POST2:C**
- Remark SNR: **PROVED (by this seat, unchecked), conditional on W3-POST2:A1, W3-POST2:B, W3-POST2:C, W3-POST2:D, W3-POST2:E**
- Remark P: **PROVED (by this seat, unchecked)**
- Remark U: **PROVED (by this seat, unchecked), conditional on W3-POST2:C**

(G(b) uses MIS-R (ii)(a) on 𝒦^λ_n, whose proof needs only W3-POST2:C and the bridge W3-POST2:A0; it carries the
full condition of the claim MIS-R (ii) because it consumes that claim. Remarks SNR and P are transfers: each
transferred claim keeps its own status; SNR is conditional on the transferred W3-POST2 claims.)

Check record: line check K2 (gpt-6.1-sol high, blind, `../reviews/K2_G_check_sol.md`): G(a), H(a), H(b), reference law,
SNR, P (all four parts), U VERIFIED; G(b) VERIFIED-WITH-AMENDMENTS (0 FATAL / 0 MAJOR / 2 MINOR, applied [K2-1, K2-2],
`../reviews/K_disposition.md`).
Notation: `../STATEMENT.md` (v1.3); `R_reduction.md` ((R1)–(R3), table R.6); `M_misr.md` ((M0), M.1–M.3). Sources:
[POST2] = `Theory_work/Wave3/W3-POST2/STATEMENT.md`; [A] = `Theory_work/Wave3/W3-POST2/lemmas/A_occam.md`; [D] =
`Theory_work/Wave3/W3-POST2/lemmas/D_hellinger.md`; [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`; [MIS1] =
`Theory_work/Wave1C/C-MIS/STATEMENT.md`; [L2] = `Theory_work/Wave1C/C-MIS/lemmas/L2_gaussian.md`; [L4] =
`Theory_work/Wave1C/C-MIS/lemmas/L4_theoremF.md`.

## G.1 Corollary G(a): Gaussian rows give GR^c at each n

Fix n. Rows (x^r_{𝒞,i}, x^r_{𝓜,i}) iid N(m, Σ), Σ_𝒞𝒞 ≻ 0; ε ~ N_n(0, σ²I) independent of X^r, σ² ≥ 0. By Gaussian
conditioning ([L2] lines 40-44, a computation at one n that uses neither σ² > 0 nor any relation between different
n): ζ_i := x_{𝓜,i} − m_𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁻¹(x_{𝒞,i} − m_𝒞), i ≤ n, are iid N(0, Σ_{𝓜·𝒞}) and independent of X^r_𝒞; with
γ := Σ_𝒞𝒞⁻¹Σ_𝒞𝓜β_𝓜 and a := (m_𝓜 − Σ_𝓜𝒞Σ_𝒞𝒞⁻¹m_𝒞)ᵀβ_𝓜, X^r_𝓜β_𝓜 = a1 + X^r_𝒞γ + ξ, ξ_i := ζ_iᵀβ_𝓜 iid N(0, τ²). ε is independent of
X^r, hence of (X^r_𝒞, ξ). So y^r − X^r_𝒞β^𝒞 = (α + a)1 + ξ + ε with ξ + ε ~ N_n(0, σ²_𝒞 I) independent of X^r_𝒞, and
(Uᵀ1 = 0) W_n = Uᵀ(ξ + ε)/σ_𝒞 ~ N_N(0, UᵀU) = N_N(0, I_N), independent of σ(X^r_𝒞), provided σ²_𝒞 = σ² + τ² > 0.
(β^𝒞, σ²_𝒞) are deterministic, so κ_n = (X^r_𝒞, β^𝒞, σ²_𝒞) is σ(X^r_𝒞)-measurable on the event that all candidate columns
are non-constant (probability one, since Σ_𝒞𝒞 ≻ 0 and n ≥ 2); off that null event κ_n is set to a fixed reference
configuration, so that it is a random configuration in the sense of STATEMENT §4 [R1-F7]. This is (GR^c | σ(X^r_𝒞)). ∎

## G.2 Corollary G(b): a growing-p envelope without a fixed variance

Hypotheses as in the statement: 2 ≤ p_𝒞 ≤ n^A; σ²_𝒞 > 0; s := |supp β^𝒞| ≥ 1 fixed; λ_min(Σ_TT) ≥ c_pop for T ⊆ 𝒞,
|T| ≤ k_n := s + max(j₀, m♯_n); max_j Σ_jj ≤ C₀; β^𝒞ᵀΣ_𝒞𝒞β^𝒞 ≤ M₀σ²_𝒞; ρ_n^{BM} := n·min_{j∈supp β^𝒞} Σ_jj(β^𝒞_j)²/(σ²_𝒞 log n) → ∞.
Put φ₀² := c_pop/(8C₀), M := 2M₀ + 1, g₀ := 1, and (n_OS, C_OS) := those of [A] Lemma A0 for (s, A, c_D = ½)
([A] lines 14-15, 25-27: (F_w; 1) ⇒ (DG; ½) ⇒ (ADG; ½) ⇒ (OS; C_OS) for n ≥ n_OS). Fix c := c₀(s, A) + 1.
Follow [L2] lines 88-105 (proof of Lemma GD(b)); W := UᵀX^r_𝒞 has iid N(0, Σ_𝒞𝒞) rows.
1. *SDs* ([L2] lines 91-93; no variance of the response involved): with probability ≥ 1 − 2n^{−2}, ½Σ_jj ≤ σ̂_j² ≤ 2Σ_jj for
   all j ∈ 𝒞, for n ≥ n₀(A).
2. *Sparse eigenvalues* ([L2] lines 94-100; design only) [K2-2]. Raw event: with probability ≥ 1 − 2k_n n^{−2}, for
   n ≥ n₀, λ_min(W_TᵀW_T) ≥ c_popN/2 for every non-empty T ⊆ 𝒞 with |T| ≤ min(p_𝒞, k_n). On the intersection of this
   event with that of step 1 (σ̂_j² ≤ 2Σ_jj ≤ 2C₀), standardisation gives λ_min(R̂_T) = λ_min(G_T)/N ≥ (c_pop/2)/(2C₀) =
   c_pop/(4C₀) ≥ φ₀² and λ_min(G_T) ≥ Nφ₀² ≥ 1 for all such T (the last for n ≥ 1 + 1/φ₀²). This gives (F₀; φ₀),
   (F_λ; φ₀) (S₀ ∪ J with |J| ≤ j₀ has size ≤ k_n) and (F_w; 1) (S₀ ∪ J with |J| ≤ m♯_n), hence (OS; C_OS) for n ≥ n_OS.
3. *Energy, in signal-to-noise form* (changed step of [L2] lines 101-102): Wβ^𝒞 ~ N_N(0, (β^𝒞ᵀΣ_𝒞𝒞β^𝒞)I_N) and
   β^𝒞ᵀΣ_𝒞𝒞β^𝒞 > 0 (β^𝒞 ≠ 0, Σ_𝒞𝒞 ≻ 0), so ‖Wβ^𝒞‖²/(β^𝒞ᵀΣ_𝒞𝒞β^𝒞) ~ χ²_N ≤ 2N with probability ≥ 1 − 1/n for n ≥ n₀
   ([P3] `lem:chi`(a), as there). On that event ‖μ(κ_n)‖² = ‖Wβ^𝒞‖² ≤ 2NM₀σ²_𝒞 ≤ nMσ²_𝒞: (E^σ; M).
4. *Relative beta-min* (changed step of [L2] line 103): on the event of step 1, θ_j(κ_n)² = σ̂_j²(β^𝒞_j)² ≥ ½Σ_jj(β^𝒞_j)², so
   min_j θ_j(κ_n)²·nφ₀²/(σ²_𝒞 log n) ≥ ½φ₀²ρ_n^{BM} ≥ c for all n ≥ n_BM (ρ_n^{BM} → ∞; n_BM depends on the sequence):
   (BM^σ; c).
5. *Sizes*: 2 ≤ p_𝒞 ≤ n^A by hypothesis; s ≤ K = min(p_𝒞, ⌊n/2⌋) for n ≥ 2s (p_𝒞 ≥ s); s(κ_n) = s (β^𝒞 deterministic).
Let 𝒜_n ∈ σ(X^r_𝒞) be the intersection of the SD event of step 1, the raw eigenvalue event of step 2 and the energy
event of step 3. For n ≥ n* (the largest threshold above, n_OS, n_BM and the n₀ of MIS-R (i) for 𝒦^λ_n included),
𝒜_n ⊆ {κ_n ∈ 𝒦^λ_n(s, A, M, φ₀, C_OS, c)} and P(𝒜_nᶜ) ≤ 2n^{−2} + 2k_n n^{−2} + n^{−1}, with k_n = O(log n) ([L2] lines 96-97, 105).
By G.1, (GR^c | σ(X^r_𝒞)) holds. MIS-R (ii)(a) on 𝒦^λ_n (c > c₀(s, A)) gives E δ_n ≤ C r_n + P(𝒜_nᶜ) = O(r_n), and
P(HPM ≠ supp β^𝒞) ≤ 2C r_n + P(𝒜_nᶜ) = O(r_n). ∎
(Compared with [L2] Lemma GD(b): the requirement "σ²_𝒞 fixed in n" is dropped; the population energy and beta-min
conditions are relative to σ²_𝒞; the conclusion is an expectation rate. [L2] line 74's example — an omitted column of
variance n² — fails step 4 unless the candidate coefficients grow accordingly: a margin failure, not a failure of
the transfer.)

## G.3 Corollary H: density contraction

Let κ_n ∈ 𝒦⁰_n(s, A, M, φ₀, C_OS) for all large n, with laws P_{κ_n}. By table R.6 the unit-noise models
(x_n, β_n/√v_n, 1) form an array in regime R1 ([W3P] lines 63-64: s₀ = s ≥ 1 fixed, 2 ≤ p ≤ n^A, s ≤ K, σ*² = 1 fixed, G)
satisfying (E), (F₀), (OS) for all large n. [POST2] Claim D(b) (lines 112-116) gives C_H = C_H(s, A, σ*² = 1) such that for
every M_n → ∞, with B̃_n := {(S, θ̃, ṽ) : ‖X_Sθ̃ − μ̃‖² > C_H log n or |ṽ − 1| > M_n n^{−1/2}},
  Π(B̃_n | x_n, ỹ) → 0 in P̃-probability.
Let B_n := {(S, θ, v′) : ‖X_Sθ − μ(κ_n)‖² > C_H v_n log n or |v′/v_n − 1| > M_n n^{−1/2}}. The scaling
T := T_{1/√v_n} : (S, θ, v′) ↦ (S, θ/√v_n, v′/v_n) is a bijection with T(B_n) = B̃_n (‖X_Sθ/√v_n − μ(κ_n)/√v_n‖² =
‖X_Sθ − μ(κ_n)‖²/v_n). Hence Π(B_n | x_n, y^r) = (T♯Π(· | x_n, y^r))(B̃_n), and by Lemma R′(b) (parameter-posterior part)
the random measure T♯Π(· | x_n, y^r) under P_{κ_n} has the law of Π(· | x_n, ỹ) under P̃. So Π(B_n | x_n, y^r) has the law
of Π(B̃_n | x_n, ỹ) and tends to 0 in probability. This is the first display of (b).
Hellinger: for normals, H²(N(a, v′), N(b, w)) depends on (a, b, v′, w) only through v′/w and (a − b)²/(v′ + w)
([D] line 12), so h̄_n² computed from (μ̂, v′) against (μ(κ_n), v_n) equals the unit-noise h̄_n² computed from
(μ̂/√v_n, v′/v_n) against (μ̃, 1): the event {h̄_n² > (1 + C_H/4) log n/n} is mapped by T to the corresponding
unit-noise event, whose posterior mass → 0 in probability by [POST2] line 114-115 (C_H′ = 1 + C_H/(4σ*²) at σ*² = 1).
(a): if κ_n ∈ 𝒦_n(…, c), c > c₁(s, A) (or 𝒦^λ_n, c > c₀(s, A)), then δ_n → 0 in P̃-probability by MIS-R (i), and the
array satisfies R1, G, (E), (F₀): the hypotheses of [POST2] Claim D(a) (lines 107-111). Its bad set, in unit-noise
variables, {‖μ̃̂ − μ̃‖² > M_n or |ṽ − 1| > M_n n^{−1/2} or S ≠ S₀ or ‖θ̃ − θ̃*‖ > M_n n^{−1/2}}, is the image under T of
{‖μ̂ − μ(κ_n)‖² > M_n v_n or |v′/v_n − 1| > M_n n^{−1/2} or S ≠ S₀(κ_n) or ‖θ − θ(κ_n)‖ > M_n√(v_n/n)} (θ zero-padded);
conclude as for (b); the Hellinger clause likewise. ∎
**Reference law.** N(μ_i(κ), v) is by definition the i-th marginal of μ(κ) + √v ε̃. Under [MIS1]'s GR
([MIS1] lines 54-58): given x, y^r = (α + a)1 + xβ^𝒞 + ε′ with ε′ ~ N_n(0, vI); subtracting the constant
α + a + n⁻¹Σ_l(xβ^𝒞)_l from y^r_i leaves (Cxβ^𝒞)_i + ε′_i ~ N(μ_i(κ), v). In contrast Cy^r = μ(κ) + Cε′ has covariance vC,
whose diagonal entries are v(1 − 1/n). In the setting of Corollary G, G.1 shows y_i | x_{𝒞,i} ~ N(α + a + x_{𝒞,i}ᵀβ^𝒞, σ²_𝒞)
independently over i; this conditional density is a member of the family {N(a₀ + x_𝒞ᵀb, w)}, so it minimises the
Kullback–Leibler divergence from the true conditional law over that family (the minimum is 0).

## G.4 Remark SNR (the scale is written a_n; in Claim B, t = |T| as in [POST2] [SW1-9])

Take 𝒞 = [p] and the true model G with variance σ*²_n > 0 ([W3P] line 31), or G′ for Claim B ([POST2] line 70). Put
a_n := σ*_n and ỹ^r := y^r/a_n = (α*/a_n)1 + X^r(β*/a_n) + ε/a_n (G′: f/a_n): model G (G′) with variance 1, coefficient β*/a_n, mean
μ/a_n. By Lemma R′(a) the model-space posterior computed from ỹ^r is the one computed from y^r, and by R′(a′) the
parameter posterior from ỹ^r is the image of the one from y^r under (S, θ, v) ↦ (S, θ/a_n, v/a_n²). Now go through the list.
- [W3P] Theorem 1 items 1–5 and [POST2] A1, C, E: hypotheses (E), (F₀), (F_λ), (F_w), (OS), (BM), (ID^M) for
  (X, β*/a_n, 1) are (E) with ‖μ‖² ≤ nMa_n² and the others as stated relative to σ*² = a_n² (table R.6); every conclusion
  is about δ_n, PIPs, HPM, MPM, ξ_q, π(S ⊋ S₀), π(|S| = s₀), π(S ⊉ J_n(c)), π(S ∌ j) — functionals of the model-space
  posterior and of sets (S₀, J_n(c)) that are the same for both parametrisations (J_n(c) is defined by a relative
  inequality). So each conclusion for the unit-variance array is the conclusion for the original array.
- [W3P] item 6 and the random-design clauses of A1, C, E: if σ*² is a measurable function of (X, θ*) and, given
  (X, θ*), ε ~ N_n(0, σ*²(X, θ*)I), then ε/σ*(X, θ*) is N_n(0, I) and independent of (X, θ*); the scaled problem
  satisfies the clause with θ*/σ*(X, θ*) and common constants.
- [POST2] B (lines 68-77): design, T, |T|, D_T, R^T_m, A^T_m do not involve the response; π(|S| > m) is invariant, so
  Θ″_{n,m} is unchanged. For the scaled problem ‖μ/a_n‖² ≤ nM iff ‖μ‖² ≤ nMa_n², and B_T(ϑ/a_n) = B_T(ϑ)/a_n² ([POST2] line 44:
  every term is quadratic in (μ, ϑ)), so the reference ϑ/a_n has cost ≤ B iff B_T(ϑ) ≤ Ba_n². The bound of B at σ*² = 1 follows.
- [POST2] D: as in G.3 (which is this transfer with a_n² = v_n): thresholds ‖μ̂ − μ‖² > C_H a_n² log n, resp. > M_n a_n²,
  |v/a_n² − 1| > M_n n^{−1/2}, ‖θ − θ*‖ > M_n a_n n^{−1/2}; h̄_n against N(μ_i, a_n²) is invariant. ∎

## G.5 Remark P

**MIS (i)** ([MIS1] lines 52-72). Fixed design; suppose GR holds with ε + ξ ~ N_n(0, σ²_{𝒞,n}I), σ²_{𝒞,n} > 0 arbitrary,
and (H-MIS) holds with ‖μ^𝒞‖² ≤ Mnσ²_{𝒞,n} in place of ‖μ^𝒞‖² ≤ Mn. Put t := σ_{𝒞,n}. ỹ^r := y^r/t satisfies [MIS1]'s model
with α̃ = (α + a)/t, β̃_𝒞 := β^𝒞/t, ω̃ := 0 (ã = 0, γ̃ = 0, τ̃² = 0) and ε̃ := (ε + ξ)/t ~ N_n(0, I): GR with the fixed
variance σ̃²_𝒞 = 1. Its (H-MIS): the design conditions and s₀^𝒞 are unchanged; ‖μ^𝒞/t‖² ≤ Mn; BM-∞ and BM(c) "with σ²_𝒞"
([MIS1] line 62) read θ^𝒞²_min/t² against 1·log n/(nφ₀²), i.e. the original inequalities relative to σ²_{𝒞,n}. So [MIS1]
Theorem MIS (i) applies to the scaled array. Its conclusions concern π_𝒞 and the sets S₀^𝒞, J_n^𝒞(c) (relative
threshold): unchanged by Lemma R′(a). ∎
**MIS (ii), (ii′)** ([MIS1] lines 73-78). Suppose that, given X^r_𝒞 = x, ε + ξ ~ N_n(0, σ²_𝒞(x)I) with σ²_𝒞(·) > 0
measurable, and the envelope sets 𝒜_n are defined with ‖μ^𝒞(x)‖² ≤ Mnσ²_𝒞(x) and beta-min relative to σ²_𝒞(x). With
ỹ^r := y^r/σ_𝒞(X^r_𝒞): ε̃ := (ε + ξ)/σ_𝒞(X^r_𝒞) is N_n(0, I) given X^r_𝒞, hence independent of X^r_𝒞; the scaled problem is
[MIS1]'s random-design model with β̃_𝒞 := 0, ω̃ = ã(x)1 + xγ̃(x), ã(x) := (α + a(x))/σ_𝒞(x), γ̃(x) := β^𝒞(x)/σ_𝒞(x)
(measurable), ξ̃ := 0, fixed σ̃²_𝒞 = 1, and the same sets 𝒜_n now satisfy the finite-n inequalities of (H-MIS) with the
fixed constants (A, s, M, φ₀, g₀, 1). [MIS1] (ii), (ii′) apply; conclusions unchanged by R′(a), applied for each
realisation of the design with the scale σ_𝒞(X^r_𝒞). ∎
**Theorem F** ([MIS1] lines 124-141). Deterministic design and mean; e ~ N_N(0, σ²_nI), σ²_n > 0 arbitrary; t := σ_n.
Scaled problem: ỹ_c = μ_c/t + e/t, e/t ~ N_N(0, I). Check each hypothesis for the scaled problem with σ̃² = 1:

| [MIS1] item | scaled object | condition in original units |
|---|---|---|
| EP (line 126) | θ̃^𝒞 = θ^𝒞/t, r̃ = r/t; X_{c,𝒞}ᵀr̃ = 0; same support | EP as stated |
| Δ_n, σ²_{𝒞,n} (line 129) | Δ̃_n = Δ_n/t², σ̃²_{𝒞,n} = 1 + Δ_n/t² = σ²_{𝒞,n}/t² | definitions unchanged; the range is [σ²_n, σ²_n(1 + 2M)] |
| s₀^𝒞, p_𝒞 ≤ n^A, K, G (line 130) | unchanged; e/t Gaussian with variance 1 | as stated |
| R^𝒞 (line 130) | ‖μ_c/t‖² ≤ Mn; λ_min(R̂_{S₀^𝒞}) ≥ φ₀² | ‖μ_c‖² ≤ Mnσ²_n; floor as stated |
| SE_λ(j₀), SE_w(m_n; g₀), m_n (lines 131-132) | design and prior only | as stated |
| BM-∞ (line 132) | θ̃^𝒞²_min nφ₀²/log n → ∞ | θ^𝒞²_min nφ₀²/(σ²_n log n) → ∞ |
| BM(c) (line 133) | θ̃^𝒞²_min ≥ cσ̃²_{𝒞,n} log n/(nφ₀²) | θ^𝒞²_min ≥ cσ²_{𝒞,n} log n/(nφ₀²), as stated |
| TAIL^𝒞(m_n) (line 133) | same posterior (R′(a)) | as stated |
| (TL) (line 140) | 1/(Δ̃_n + (1 − d_n/N)) | σ²_n/(Δ_n + σ²_n(1 − d_n/N)), as stated |

So with every row's right-hand condition, [MIS1] Theorem F, Corollary F(a), F(b) apply to the scaled problem (σ̃² = 1
fixed, energy constant M). Conclusions (lines 134-137): posterior masses, PIPs, MPM, S† and the set
J_n^{𝒞,F}(c) = {j : θ̃^𝒞_j² ≥ cσ̃²_{𝒞,n} log n/(nφ₀²)} — all unchanged. ∎
*The unnormalised BM-∞ is not enough* (reviewer's example, `../reviews/L01_statement_lock_sol.md` finding 1): p_𝒞 = 2,
orthogonal standardised columns, θ^𝒞 = (1, 0), r = 0, σ²_n = n². θ^𝒞²_min nφ₀²/log n → ∞, but the scaled mean has
‖μ_c/t‖² = (n − 1)/n² → 0, so the scaled experiment is within vanishing total-variation distance of the pure-noise
experiment (two Gaussians with the same covariance and means at distance → 0); under pure noise with p_𝒞 = 2 bounded
and λ_min(X_𝒞ᵀX_𝒞) = N, [MIS1] Lemma Z ([MIS1] lines 101-105) gives π_𝒞(∅) → 1 in probability; hence π_𝒞({1}) → 0 in
probability for the original problem.

## G.6 Remark U

Let (β, v), (β′, v′) both satisfy GR^c for the same law of y^r at the same x, with κ = (x, β, v) and κ′ = (x, β′, v′)
each in 𝒦_n or 𝒦^λ_n, and let n ≥ n₀ and C be the maxima of the constants of MIS-R (i) for the two classes, with
C r_n < ½. Under this one law, E π_𝒞(supp β) ≥ 1 − C r_n > ½ and E π_𝒞(supp β′) > ½. If supp β ≠ supp β′ the two events
are disjoint models, π_𝒞(supp β) + π_𝒞(supp β′) ≤ 1 for every data set, so the expectations sum to at most 1: a
contradiction. ∎
