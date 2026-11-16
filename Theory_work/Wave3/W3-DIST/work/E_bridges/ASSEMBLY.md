# ASSEMBLY — Theorem A (i), (ii), its sentence without (A4), Theorem B, and the Example

**Status: DRAFT (by this seat, unchecked).** Stream E, ticket W3-DIST. Targets: reader versions `STATEMENT.md:152-200`
(v1.3.1, §1R). Inputs: the master displays (1.1), (1.2), DIST-3 (taken as given, as the brief instructs), Lemma X′'s size
clause (for the sentence without (A4) only), W3-POST Theorem 1 (for Theorem B only), and the bridges of this folder:
`B0.md`, `B1.md`, `B2core.md`, `B2.md`, `B3.md`. No STATEMENT-CHANGE REQUEST to the reader statements is needed; one
editorial request on bridge B2's wording is in `B2.md`.

## 0. Consumed statements (hypotheses of this file) and how they are read

**(H1.1) = DIST-1, display (1.1)**, `STATEMENT.md:68-71` (CANDIDATE, to be proved by the other streams):
> There are constants c ∈ (0, 1], C, C′, M₀, n₀ such that, in (RD), for every n ≥ n₀ and every real t with
> M₀ log n ≤ t ≤ n^{1−κ₀}: P*[ Π( d_H(f, f*) > C√(t/n) or |S| > s₀ + C′t/log n | D_n ) > e^{−ct} ]
> ≤ 3e^{−ct} + P*( 𝒟_nᶜ ∪ (E; M)ᶜ ∪ (C; M′)ᶜ ∪ (ND; c_D, m_n(t))ᶜ ).
Constants may depend on (s₀^r, A, σ*², M, M′, κ₀, c_D) (`STATEMENT.md:63-64`).
**(H1.2) = DIST-2, display (1.2)**, `STATEMENT.md:86-88`: there are c, C, M₀, n₀ depending on (s₀^r, A, σ*², M, M′, κ₀)
such that for n ≥ n₀ and M₀ log n ≤ t ≤ n^{1−κ₀}: P*[Π(d_H(f, f*) > C√(tℓ_n/n) | D_n) > e^{−ct}] ≤ 3e^{−ct} +
P*(𝒟_nᶜ ∪ (E; M)ᶜ ∪ (C; M′)ᶜ), ℓ_n = log(p_raw ∨ n).
**(H-X′) = Lemma X′, size clause**, `STATEMENT.md:333-335` with Lemma X's display `:322-325` (CANDIDATE): fixed design
with p ≥ 2, p ≤ n^A, s₀ ≤ min(s₀^r, K), noise G, under (E; M), (C; M′) only: there are c_X, M₀_X, n₀_X (one n₀_X for the
whole range of t) depending on (s₀^r, A, σ*², M, M′, κ₀) such that for n ≥ n₀_X and M₀_X log n ≤ t ≤ n^{1−κ₀}:
P_ε[Π(|S| > m_n(t) | y) > e^{−c_Xt}] ≤ 2e^{−c_Xt}. (Only the size clause of X′ is used.)
**(H3) = DIST-3, first display**, `STATEMENT.md:93-97` (CANDIDATE): there are c₃, C₃, n₀₃ (depending on (s₀^r, A, σ*², M, B,
C_T, κ₀)) such that for n ≥ n₀₃, 1 ≤ u ≤ n^{1−κ₀} and every design in 𝒟_n ∩ (E; M) ∩ (L₀; B) ∩ (TR₀; C_T), outside a noise
event of (conditional) probability ≤ C₃e^{−c₃u}: Π(d_H(f, f*) > C₃√(u/n) | D_n) ≤ δ_n + C₃e^{−c₃u}, δ_n = 1 − π(S₀).
**(H-POST) = W3-POST Theorem 1, items 1 and 6** (W3-POST:Thm-1@1.0.0, status "T03♯: PROVED; SF VERIFIED (W2-VT03R); XF
VERIFIED (A-REV2)"), `W3-POST/STATEMENT.md:80-81, 95-100`: "6. … Let (X, θ*) be random with ε independent of (X, θ*), and
suppose there are (X, θ*)-measurable events 𝒜_n with P(𝒜_n) → 1 on which |supp θ*| = s₀ and (E), (F_λ), (F_w) hold with
common constants (M, φ₀, g₀) and (BM) holds with a common c > c₀ or a common deterministic envelope M_n → ∞. Then 1–4
hold under the joint law"; "1. (Rate) Under (BM): δ_n = 1 − π(S₀) = O_P(r_n)", r_n = √(log n/n). **Consumed premise of
Theorem B** (rule 11: stated as a hypothesis).

**Reading conventions (used throughout; to be confirmed by whoever proves the masters).**
- (R-a) *Per-n, law-uniform reading.* In (H1.1), (H1.2), (H-X′), (H3) the constants do not depend on the law of the
  data; each display is a statement at each fixed n ≥ n₀ about every law satisfying (RD) at that n (triangular arrays:
  ν_x, p_raw, α*, β* may change with n). This is how the masters are phrased and how ROUTES Step 5 proves them.
- (R-b) *s₀^r.* (RD) fixes |supp β*| = s₀^r; the reader only asks |supp β*| ≤ s. At each n we apply the masters with
  s₀^r := |supp β*| ∈ {0, …, s} and use the worst constant over these s + 1 values (min for c's, max for C's, M₀'s, n₀'s).
- (R-c) *Monotonicity.* Each display remains true if c is decreased, C, C′ are increased, M₀, n₀ are increased, or the
  interface constants M, M′, B, C_T are replaced by smaller-or-equal ones that still hold: the bad set and the
  threshold event shrink, the bound grows, the range shrinks. Hence we may and do assume C, C′, C₃ ≥ 1.
- (R-d) *Scale.* By `B0.md` (d)–(f), every event below is the same event whether described with y^r or with
  ỹ = (y^r − α*1)/σ*; we apply the masters to the unit-noise model (σ*² = 1, α* = 0), so their constants are evaluated at
  σ*² = 1 and κ₀ = ½.

## 1. Theorem A (i), (ii)

**Master constants.** Evaluate (H1.1) at σ*² = 1, κ₀ = ½, M = M_E := 2s²b̄², M′ = M_C := 2sb̄², c_D := g₀/(1 + g₀) with
g₀ := c_ψ/8, worst case over s₀^r ∈ {0, …, s} (R-b), and enlarge (R-c): constants c_⋆ ∈ (0, 1], C_⋆ ≥ 1, C′_⋆ ≥ 1, M₀_⋆,
n₀_⋆, all functions of (s, A, b̄, c_ψ) only.

**Reader constants (exact renaming).** Put t := M log n / C_⋆² and
  c_A := c_⋆/(2C_⋆²),  C₁ := C′_⋆/C_⋆²,  M₀ := max{1, C_⋆²M₀_⋆},
  n₀ := max{ n₀_⋆, 3, 2s, n_B(s, A, K), ⌈6^{1/c}⌉, n_R(A, K, c) },
where c is the final exponent of the reader statement (c := c_A in this section; c := the minimum in §2 when the
sentence without (A4) is included — every requirement below is monotone in c, so the n₀ computed with the final c
serves all parts), n_B is defined in `B2.md` (e), and n_R(A, K, c) := the least integer ≥ 3 with
10m^A·exp(−c₂m/K⁴ + c√m) ≤ 1 for all m ≥ n_R (finite since the exponent is −c₂m/K⁴ + O(√m) and m^A = e^{A log m}).
All of c, C₁, M₀, n₀ depend only on (s, A, K, c_ψ, b̄).

**Claim.** If n ≥ n₀, M₀ ≤ M ≤ √n/log n and (A1)–(A5) hold with q_n = min{p, ⌈C_qM log n⌉}, then with
  𝔈_n := { Π( d_H(f, f*) > √(M log n/n) or |S| > s + C₁M | D_n ) > n^{−cM} }:
P*(𝔈_n) ≤ n^{−cM}. Outside 𝔈_n, Π(d_H(f, f*) > √(M log n/n) | D_n) ≤ n^{−cM} and Π(|S| > s + C₁M | D_n) ≤ n^{−cM}, which
are (i) and (ii) (`STATEMENT.md:175-177`), on the same data sets.

**Proof.** *Step 1 (scale).* By `B0.md` (d), (e), 𝔈_n is the same event as the one defined with (x, ỹ) and f̃*, and
the reduced data follow (RD) at this n with intercept 0, coefficients β*/σ*, unit noise, the same ν_x, p_raw = p ≤ n^A,
|supp| = |supp β*| ≤ s. The reader assumptions transfer (`B0.md` (f)): (A2)–(A4) unchanged, (A5) with σ* = 1.
*Step 2 (range of t).* t = M log n/C_⋆² ≥ M₀_⋆ log n because M ≥ M₀ ≥ C_⋆²M₀_⋆; and t ≤ M log n ≤ √n = n^{1−κ₀} because
C_⋆ ≥ 1 and M ≤ √n/log n. n ≥ n₀_⋆. So (H1.1) applies at (n, t).
*Step 3 (event inclusion).* C_⋆√(t/n) = √(M log n/n) and s₀ + C′_⋆t/log n = s₀ + C₁M ≤ s + C₁M (s₀ = |supp θ*| ≤
|supp β*| ≤ s; dropped columns only lower s₀, `STATEMENT.md:33-35`). Hence
  {d_H > √(M log n/n) or |S| > s + C₁M} ⊆ {d_H > C_⋆√(t/n) or |S| > s₀ + C′_⋆t/log n}.
Also e^{−c_⋆t} = n^{−c_⋆M/C_⋆²} = n^{−2c_AM} ≤ n^{−2cM} ≤ n^{−cM} (c ≤ c_A, n ≥ 1). So 𝔈_n ⊆ {Π(bad set of (1.1)) > e^{−c_⋆t}}.
*Step 4 (remainder).* On 𝓔₁ ∩ 𝓔₂(q_n): 𝒟_n holds and (E; M_E), (C; M_C) hold (`B1.md` (b), (c), in units σ*² = 1);
(ND; c_D, m_n(t)) holds because t ≤ M log n (`B2.md` (d), which uses (A3), (A4) with window q_n, |supp β*| ≤ s, p ≤ n^A,
M ≥ 1). By `B2.md` (e) (n ≥ n_B, M ≤ √n/log n, n ≥ 3):
  P*(𝒟_nᶜ ∪ (E; M_E)ᶜ ∪ (C; M_C)ᶜ ∪ (ND; c_D, m_n(t))ᶜ) ≤ P(𝓔₁ᶜ) + P(𝓔₂(q_n)ᶜ) ≤ 4pe^{−c₁n/K⁴} + e^{−c₂n/K⁴} ≤ 5n^Ae^{−c₂n/K⁴}
(c₂ = 10⁻⁵ ≤ c₁ = 1/576, p ≤ n^A, n^A ≥ 1).
*Step 5 (collect).* By (H1.1) and Steps 3–4,
  P*(𝔈_n) ≤ 3e^{−c_⋆t} + 5n^Ae^{−c₂n/K⁴} ≤ 3n^{−2cM} + 5n^Ae^{−c₂n/K⁴}.
(α) 3n^{−2cM} ≤ ½n^{−cM} ⟺ n^{cM} ≥ 6, true because M ≥ 1 and n ≥ 6^{1/c}.
(β) M log n ≤ √n gives n^{−cM} = e^{−cM log n} ≥ e^{−c√n}; and n ≥ n_R gives 10n^Ae^{−c₂n/K⁴} ≤ e^{−c√n}. So
5n^Ae^{−c₂n/K⁴} ≤ ½n^{−cM}.
Hence P*(𝔈_n) ≤ n^{−cM}. None of the requirements on n depends on M within M₀ ≤ M ≤ √n/log n: one n₀ for the whole
range. The bound is uniform over all laws satisfying (A1)–(A5) with the given constants, because each input is (R-a). ∎

**Remark (general radii, `STATEMENT.md:238-239`).** The same proof with t := nε_n²/C_⋆² gives the form
P*[Π(d_H > ε_n | D_n) > e^{−c nε_n²}] ≤ e^{−c nε_n²} for M₀ log n/n ≤ ε_n² ≤ n^{−1/2}, with (ND) needed at m_n(nε_n²/C_⋆²): with
q_n replaced by min{p, ⌈C_q nε_n²⌉} (if nε_n² ≥ log n, `B2.md` (d) applies with M := nε_n²/log n ≥ 1). Not a target clause;
recorded for the reviewer.

## 2. Theorem A, the sentence without (A4) (`STATEMENT.md:185-187`)

Assumptions: (A1), (A2), (A5), and (A3) only for single predictors: every Var(x_j) > 0 and E exp(λz_j) ≤ exp(K²λ²/2)
for all j, λ. (No window, no (A4).)

**Master constants.** (H1.2) at σ*² = 1, κ₀ = ½, (M, M′) = (M_E, M_C), worst over s₀^r ≤ s, enlarged: c_⋆⋆, C_⋆⋆ ≥ 1, M₀_⋆⋆,
n₀_⋆⋆; (H-X′) likewise: c_X, M₀_X, n₀_X. All depend only on (s, A, b̄).
**Reader constants.** t₂ := M log n/C_⋆⋆²;
  C₁^{(2)} := 1 + s + (sA + s + 5)/log 2;
  final c := min{ c_A, c_⋆⋆/(2C_⋆⋆²), c_X/(2C_⋆⋆²) },  final C₁ := max{ C′_⋆/C_⋆², C₁^{(2)} },
  final M₀ := max{ 1, C_⋆²M₀_⋆, C_⋆⋆²M₀_⋆⋆, C_⋆⋆²M₀_X },  final n₀ := max{ n₀ of §1 with this c, n₀_⋆⋆, n₀_X }.
Theorem A (i), (ii) remain true with the final constants by (R-c)-type monotonicity of the reader displays: a smaller c
makes the threshold n^{−cM} larger and the bound n^{−cM} larger; a larger C₁ shrinks the size event; a larger M₀, n₀
shrink the range. (In §1 Step 5 the inequalities (α), (β) were proved for any c ≤ c_A with n ≥ 6^{1/c}, n ≥ n_R(A, K, c).)

**(i′) Claim.** For n ≥ n₀ and M₀ ≤ M ≤ √n/log n: P*[Π(d_H(f, f*) > √(M log n·log(p ∨ n)/n) | D_n) > n^{−cM}] ≤ n^{−cM}.
*Proof.* Scale reduction as in §1 Step 1. t₂ ∈ [M₀_⋆⋆ log n, √n] as in §1 Step 2. Here p = p_raw, so ℓ_n = log(p ∨ n), and
C_⋆⋆√(t₂ℓ_n/n) = √(M log n·log(p ∨ n)/n). e^{−c_⋆⋆t₂} = n^{−c_⋆⋆M/C_⋆⋆²} ≤ n^{−2cM}. On 𝓔₁: 𝒟_n, (E; M_E), (C; M_C) (`B1.md`),
so the remainder of (1.2) is ≤ P(𝓔₁ᶜ) ≤ 4n^Ae^{−c₁n/K⁴} ≤ 5n^Ae^{−c₂n/K⁴}. Then (α), (β) of §1 Step 5. ∎
**(ii′) Claim.** For n ≥ n₀ and M₀ ≤ M ≤ √n/log n: P*[Π(|S| > s + C₁M log n | D_n) > n^{−cM}] ≤ n^{−cM}.
*Proof.* Scale reduction as in §1 Step 1 (|S| is preserved by T_{σ*}). *Cutoff bound.* With s₀ ≤ s, p ≤ n^A,
log(n + 1) ≤ 2log n, t₂ ≤ M log n (C_⋆⋆ ≥ 1):
  m_n(t₂) ≤ s₀ + 1 + [s₀log(2p) + ((s₀+2)/2)log(n+1) + 3t₂]/log 2 ≤ s + 1 + s + (sA + s + 2 + 3M) log n/log 2
         ≤ s + [1 + s + (sA + s + 5)/log 2]·M log n = s + C₁^{(2)}M log n,
using 1 + s ≤ (1 + s)M log n (M ≥ 1, log n ≥ 1 for n ≥ 3) and sA + s + 2 + 3M ≤ (sA + s + 5)M. So
{|S| > s + C₁M log n} ⊆ {|S| > m_n(t₂)} (C₁ ≥ C₁^{(2)}). *Conditioning on the design.* Under (RD), ε̃ is independent of x
and the posterior is a measurable function of (x, ỹ); on 𝓔₁ the fixed design (standardised retained columns X, μ = CX^rβ̃*)
satisfies the hypotheses of (H-X′): p = p_ret ≥ 2, p ≤ n^A, s₀ = |supp β*| ≤ s ≤ K (n ≥ 2s), (E; M_E), (C; M_C); and
t₂ ∈ [M₀_X log n, √n]. Hence, by Fubini,
  P*[Π(|S| > m_n(t₂) | D_n) > e^{−c_Xt₂}] ≤ E[1_{𝓔₁} P_ε(Π(|S| > m_n(t₂) | y) > e^{−c_Xt₂} | x)] + P(𝓔₁ᶜ) ≤ 2e^{−c_Xt₂} + 4n^Ae^{−c₁n/K⁴}.
With e^{−c_Xt₂} ≤ n^{−2cM} ≤ n^{−cM}: P*[Π(|S| > s + C₁M log n) > n^{−cM}] ≤ 2n^{−2cM} + 5n^Ae^{−c₂n/K⁴} ≤ ½n^{−cM} + ½n^{−cM}
(n^{cM} ≥ 6 ≥ 4, and (β)). ∎
(Alternative input for (ii′): Lemma S, `STATEMENT.md:310-316`, with T = S₀, ϑ = θ*, m = m_n(t₂); it gives
P_ε[π(|S| > m) > e^{−t₂}] ≤ Ce^{−t₂} + Ce^{−cn}, which yields the same conclusion with adjusted constants.)

## 3. Theorem B (`STATEMENT.md:194-200`), conditional on W3-POST:Thm-1@1.0.0

**Claim.** Assume (A1)–(A5) with the window of M = 1, exactly s ≥ 1 nonzero coordinates of β*, and (A6). Assume (H3)
and (H-POST). Then for every sequence M_n → ∞, Π(d_H(f, f*) > M_n/√n | D_n) → 0 in P*-probability.

**Proof.** Fix M_n → ∞ and η ∈ (0, 1); we show P*(Π(d_H(f, f*) > M_n/√n | D_n) > η) → 0.
*Step 1 (scale).* By `B0.md` (d), (e), the event {Π(d_H > M_n/√n | D_n) > η} and δ_n = 1 − π(S₀) are the same whether
computed from (x, y^r) or (x, ỹ); work in the unit-noise model, where (A1)–(A6) hold with σ* = 1 (`B0.md` (f)).
*Step 2 (design events).* Let 𝒜_n := 𝓔₁ ∩ 𝓔₂(q_n) with q_n = min{p, ⌈C_q log n⌉}. By `B3.md`: on 𝒜_n (n ≥ max(3, 2s)) the
design lies in 𝒟_n ∩ (E; M_E) ∩ (L₀; B) ∩ (TR₀; 2), B = M_E + M_C; P(𝒜_nᶜ) → 0; and the hypotheses of (H-POST) item 6
hold with the (X, θ*)-measurable events 𝒜′_n ⊇ 𝒜_n, common constants (M_E, φ₀ = √ψ/2, g₀ = c_ψ/8) and the common
deterministic envelope M_n^{BM} := b_n²nψ/(8 log n) → ∞ (BM-∞). By (H-POST) items 6 and 1, δ_n = O_P(r_n) under the joint law
of (design, noise); since r_n → 0, P*(δ_n > η/2) → 0.
*Step 3 (DIST-3).* Apply (H3) with σ*² = 1, κ₀ = ½, (M, B, C_T) = (M_E, B, 2), s₀^r = s: constants c₃, C₃ ≥ 1, n₀₃. Let ϵ > 0
and choose u = u(ϵ, η) ≥ 1 with C₃e^{−c₃u} ≤ min{η/2, ϵ}. Let n be so large that n ≥ max{n₀₃, 3, 2s}, u ≤ √n and
M_n ≥ C₃√u. Then {d_H > M_n/√n} ⊆ {d_H > C₃√(u/n)}, and for every design in 𝒜_n, outside a noise event N_{n,u} with
P_ε(N_{n,u} | x) ≤ C₃e^{−c₃u}: Π(d_H > M_n/√n | D_n) ≤ δ_n + C₃e^{−c₃u} ≤ δ_n + η/2. Therefore
  {Π(d_H > M_n/√n | D_n) > η} ⊆ 𝒜_nᶜ ∪ (𝒜_n ∩ N_{n,u}) ∪ {δ_n > η/2},
and, integrating the conditional bound over x ∈ 𝒜_n (Fubini; ε independent of x),
  P*(Π(d_H > M_n/√n | D_n) > η) ≤ P(𝒜_nᶜ) + C₃e^{−c₃u} + P*(δ_n > η/2) ≤ P(𝒜_nᶜ) + ϵ + P*(δ_n > η/2).
By Step 2 the limsup is ≤ ϵ; ϵ > 0 was arbitrary. ∎
**Status of Theorem B.** Conditional on W3-POST:Thm-1@1.0.0 (consumed premise (H-POST); status quoted in §0) and on
DIST-3 (H3) (CANDIDATE in this ticket). (A4) is used only through (F_w) (`B3.md` Step 4); (A6)(a) through (F_λ) and
(TR₀; 2) needs only (A3) on supp β*.

## 4. The Example (`STATEMENT.md:189-192`)

**(E1) Gaussian predictors satisfy (A3) with K = 1.** If x is jointly Gaussian with positive variances, z = D_σ⁻¹(x − Ex)
is jointly Gaussian with mean 0, so for every u (any number of nonzero entries) uᵀz ~ N(0, Var(uᵀz)) and
E exp(λuᵀz) = exp(λ²Var(uᵀz)/2), i.e. (A3) with K = 1 and any window.
**(E2) Independent predictors satisfy (A3) with the constant K of a single predictor.** If x_1, …, x_p are independent
with positive variances and E exp(λz_j) ≤ exp(K²λ²/2) for every j and λ (one K for all predictors), then for every u,
by independence, E exp(λuᵀz) = Π_jE exp(λu_jz_j) ≤ Π_j exp(K²λ²u_j²/2) = exp(K²λ²‖u‖²/2), and Var(uᵀz) = Σ_ju_j²Var(z_j) =
‖u‖² (independent, unit variances). So (A3) holds with this K and any window.
**(E3) Uniform principal-block floor ⇒ (A4) for all large n.** Suppose every q_n × q_n principal block of Corr(x) has
smallest eigenvalue ≥ ψ > 0 (ψ fixed). Every T with 1 ≤ |T| ≤ q_n is contained in some T′ with |T′| = q_n (q_n ≤ p), and
for u ∈ ℝ^T padded by zeros to ũ ∈ ℝ^{T′}, uᵀCorr(x_T)u = ũᵀCorr(x_{T′})ũ ≥ ψ‖u‖². So λ_min(Corr(x_T)) ≥ ψ ≥ c_ψ/n
whenever n ≥ c_ψ/ψ: (A4) holds for every fixed c_ψ (e.g. c_ψ = 1) and all n ≥ c_ψ/ψ.
(If moreover the floor holds on all blocks of size ≤ (2A + 3)s + 2, as in (E4), (E5), then (A6)(a) holds with the same ψ.)
**(E4) Correlation ρ^{|j−k|}, |ρ| < 1: every principal block has λ_min ≥ ψ := (1 − |ρ|)/(1 + |ρ|).** Put
f(ω) := Σ_{h∈ℤ}ρ^{|h|}e^{ihω}, ω ∈ [−π, π]; the series converges absolutely (Σ|ρ|^{|h|} < ∞), f is continuous and real, and
  f(ω) = 1 + 2Re[ρe^{iω}/(1 − ρe^{iω})] = (1 − ρ²)/|1 − ρe^{iω}|² = (1 − ρ²)/(1 − 2ρcos ω + ρ²).
Its Fourier coefficients are (2π)⁻¹∫_{−π}^{π}f(ω)e^{−ihω}dω = ρ^{|h|} (termwise integration, absolute convergence). For a
finite index set T ⊂ ℤ (not necessarily contiguous) and u ∈ ℝ^T:
  uᵀ[ρ^{|j−k|}]_{j,k∈T}u = Σ_{j,k∈T}u_ju_k(2π)⁻¹∫f(ω)e^{−i(j−k)ω}dω = (2π)⁻¹∫f(ω)|Σ_{j∈T}u_je^{−ijω}|²dω
   ≥ min f·(2π)⁻¹∫|Σ_ju_je^{−ijω}|²dω = min f·‖u‖²,
by orthogonality of e^{−ijω} on [−π, π]. The denominator 1 − 2ρcos ω + ρ² is ≤ 1 + 2|ρ| + ρ² = (1 + |ρ|)², so
min f ≥ (1 − ρ²)/(1 + |ρ|)² = (1 − |ρ|)/(1 + |ρ|) = ψ > 0. (Numerical check: `bridges_checks_out.txt`, "AR(rho) principal
blocks": 2100 random index sets, no violation; the printed minimum gap 0 comes from ρ = 0, where the block is I and ψ = 1.)
**(E5) Equal correlation ρ ∈ [0, 1): every principal block has λ_min = 1 − ρ (or 1 if |T| = 1).** Corr(x_T) =
(1 − ρ)I + ρ11ᵀ has eigenvalues 1 − ρ (multiplicity |T| − 1, eigenvectors ⊥ 1) and 1 + (|T| − 1)ρ ≥ 1 − ρ (eigenvector 1).
So ψ = 1 − ρ > 0. (For ρ < 0 the matrix is not PSD once |T| > 1 + 1/|ρ|, which is why ρ ≥ 0 is required.)
Combining (E1) with (E4) or (E5): Gaussian AR or equal-correlation predictors satisfy (A3) with K = 1, (A4) for every
c_ψ and n ≥ c_ψ/ψ, and (A6)(a) with ψ; (A5) and (A6)(b) are conditions on β* only.

## 5. Constant bookkeeping (summary)

| reader constant | value | depends on |
|---|---|---|
| c₁ (B1) | 1/576 (absolute) | — |
| c₂ (B2-core) | 10⁻⁵ (absolute) | — |
| C_q | 2(s(A + 2) + 4)/log 2 | s, A |
| M_E, M_C, B | 2s²b̄², 2sb̄², M_E + M_C | s, b̄ |
| g₀, c_D | c_ψ/8, g₀/(1 + g₀) | c_ψ |
| c | min{c_⋆/(2C_⋆²), c_⋆⋆/(2C_⋆⋆²), c_X/(2C_⋆⋆²)} | s, A, b̄, c_ψ |
| C₁ | max{C′_⋆/C_⋆², 1 + s + (sA + s + 5)/log 2} | s, A, b̄, c_ψ |
| M₀ | max{1, C_⋆²M₀_⋆, C_⋆⋆²M₀_⋆⋆, C_⋆⋆²M₀_X} | s, A, b̄, c_ψ |
| n₀ | max{n₀_⋆, n₀_⋆⋆, n₀_X, 3, 2s, n_B(s, A, K), ⌈6^{1/c}⌉, n_R(A, K, c)} | s, A, K, c_ψ, b̄ |
(⋆: (1.1); ⋆⋆: (1.2); X: Lemma X′; all at σ*² = 1, κ₀ = ½, worst over s₀^r ≤ s, with C's enlarged to ≥ 1.)
`STATEMENT.md:241` (Remark (4): "C₁ = C′/C²") matches the first entry of C₁; the second entry is needed only for the
sentence without (A4).

## 6. Points for the checker / risks
1. (R-a) is load-bearing: Theorem A's "uniform over all laws" and "one n₀" need the masters' constants and n₀ to be
   law-free and per-n. If a master proof yields constants depending on the law (e.g. through ν_x), the assembly fails as
   written.
2. The sentence without (A4) uses Lemma X′'s size clause (H-X′) — a lemma, not one of the three master displays the
   brief lists; `STATEMENT.md:121` names it as the source. If (H-X′) is not proved, Lemma S (`STATEMENT.md:310-316`) is
   the fallback (§2).
3. Theorem B is conditional on W3-POST Theorem 1 and on DIST-3; B3 verifies item 6's events, nothing about its proof.
4. n_B and n_R are defined implicitly (least integers making explicit inequalities hold for all larger n); they are
   finite and depend only on the listed constants, but no closed form is given.

## Amendments (lead, 2026-11-15, after the same-family pre-check; part of this file)
A-1 (§2 (ii′)). Read "s ≤ K" as s₀ ≤ min(s, p) ≤ K (s may exceed p; s₀ cannot).
A-2 (Example). "Gaussian predictors" means **jointly** Gaussian; "independent predictors" satisfy (A3) with a **common**
single-predictor constant K.
A-3 (constant C₁). The constant of Theorem A (ii) is C₁ := max{C′/C², 1 + s + (sA + s + 5)/log 2}; enlarging C₁ only weakens
(ii), so this is consistent with the statement ("there are constants … C₁").
A-4 (size of n₀). With the absolute constant c₂ = 10⁻⁵ of B2-core and uniformity up to M = √n/log n, the threshold n_B (hence
n₀) is of the order 10¹⁵–10¹⁸. Theorem A is an asymptotic statement; no claim about practical sample sizes is made.
A-5 (reading convention R-a). The master displays (1.1), (1.2) and DIST-3 are used in the form: for each n ≥ n₀ (n₀ and all
constants depending only on the listed constants, not on the law of the data), the bound holds for every law in (RD)
at that n. STATEMENT §0 is to state this explicitly; the proofs of Lemmas X, X′ and DIST-3 are written in this form
(fixed design, bounds uniform over designs satisfying the interfaces at that n).
