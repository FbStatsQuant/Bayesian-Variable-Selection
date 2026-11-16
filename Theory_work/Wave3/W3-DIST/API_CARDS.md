# W3-DIST — cards for the API batch proof attempts (HQ steer A4 item 6; PROTOCOL_v4 H3)

One card per key lemma: a self-contained statement, the context files, and the routes worth attacking in parallel.
Attempts are proof material, never reviews; anything kept is line-checked. Statements are candidates (STATEMENT v1.1).

## Common definitions (prepend to every card)
Fixed design. n ≥ 3; X ∈ ℝ^{n×p}: centred columns with ‖x_j‖² = n − 1, p ≥ 2. N = n − 1; U ∈ ℝ^{n×N} with UᵀU = I,
UUᵀ = C := I − 11ᵀ/n; contrast coordinates y_c = Uᵀy^r = μ_c + e, e ~ N_N(0, σ*²I), μ_c = Uᵀμ, μ = Xθ*, S₀ = supp θ*,
s₀ = |S₀| ≥ 0 (s₀ = 0 allowed). X_{c,S} = UᵀX_S. For S ⊆ [p]: G_S = X_SᵀX_S, H_S = (n+1)G_S + I, D_S = det H_S/det(G_S + I),
M_S = X_{c,S} n H_S⁻¹ X_{c,S}ᵀ (0 ⪯ M_S ⪯ P_S, P_S the projection onto col X_{c,S}), Q^c_S = y_cᵀ(I − M_S)y_c
= min_φ{‖y_c − X_{c,S}φ‖² + φᵀ(G_S + I)φ/n}, L_S = μ_cᵀ(I − M_S)μ_c. K = min(p, ⌊n/2⌋), Ω = {|S| ≤ K}; prior weights
w(k) = ½/C(2p − 1, k); q_k = C(p, k)w(k). ν = 0.01 + n/2, b = 0.01·s_y², s_y² = ‖y_c‖²/N. Posterior on models:
π(S) ∝ w(|S|) D_S^{−1/2} (2b + Q^c_S)^{−ν} on Ω. Given S: v | S, y ~ IG(ν, b + Q^c_S/2); θ_S | v, S, y ~ N(nH_S⁻¹X_{c,S}ᵀy_c, nvH_S⁻¹);
μ̂ := X_Sθ. Interfaces: (E; M) ‖μ‖² ≤ nM; (C; M′) ‖θ*‖² ≤ nM′ (so L_{S₀} ≤ M + M′);
(ND; c_D, m): for 1 ≤ j ≤ min(m, p − s₀), C(p − s₀, j)⁻¹ Σ_{|J|=j, J∩S₀=∅} (D_{S₀}/D_{S₀∪J})^{1/2} ≤ [c_D(n+1)]^{−j/2}.
m_n(t) := min{K, s₀ + ⌈(s₀ log(2p) + ((s₀+2)/2) log(n+1) + 3t)/log 2⌉}. κ₀ ∈ (0, 1) fixed; p ≤ n^A where stated.
Context for all cards: `Theory_work/Wave3/W3-POST/STATEMENT.md` §0; `Theory_work/Wave3/W3-POST2/STATEMENT.md` (notation);
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`
([P1]: `thm:T01i`, `lem:spec`, `lem:slab`, `lem:num`, `lem:den`, `thm:Ta`, `thm:T01iii`); `Theory_work/Wave3/W3-DIST/STATEMENT.md`, `ROUTES.md`.

## Card X — Lemma X (in-sample exponential core) — the key lemma
**Statement.** p ≤ n^A, s₀ ≤ s₀^r, s₀ ≤ K. Under (E; M), (C; M′), (ND; c_D, m_n(t)) there are c ∈ (0, 1], C, C′, M₀, n₀ depending
only on (s₀^r, A, σ*², M, M′, c_D, κ₀) such that for all n ≥ n₀ and all t with M₀ log n ≤ t ≤ n^{1−κ₀} (one n₀ for the whole
range), with d_t := s₀ + ⌈C′t/log n⌉:
  P_e[ Π( ‖μ̂ − μ‖² > Cσ*²t  or  |v/σ*² − 1| > C√(t/n)  or  |S| > d_t | y ) > e^{−ct} ] ≤ 2e^{−ct}.
**Context:** `W3-POST2/lemmas/D_hellinger.md` (D0, D1), `A_occam.md` ((C5′), a_J, Lemma A0), `E_visibility.md` (E1(b)),
`B_tail_approx.md`; `ARC/W1-T03R/PROOF.md` ((C6), (C8)); `W3-DIST/work/prior_probe/REPORT.md` §3, A2–A4 (Lemma V,
Theorem P; unchecked); Cards S and V.
**Routes to attack in parallel.**
- X-a (lead's route, ROUTES §2 Step 3): noise event → good models by conditional Gaussian/IG tails → far small models
  by the likelihood ratio against S₀ → large models: supersets by truncated Occam moments with Lemma V and (ND),
  non-supersets through S ∪ S₀, sizes above m_n(t) by Lemma S. Budget the three factors of S1-06 before Markov.
- X-b (no truncation): use Lemma V(b)'s untruncated moment bound with a small η and Markov directly, paying
  (1 + η)^{s₀+j/2}; compare the resulting size cut with X-a's.
- X-c (fit-based bad set): bound the posterior mass of {eᵀM_Se > τ} ∪ {L_S > τ} directly, without a size cut, and see
  how far (ND) can be weakened (feeds S-FIT).
- X-d (adversarial): look for a design satisfying (E), (C), (ND) with Hellinger-far posterior mass ≥ n^{−c} on an event
  of probability ≫ e^{−ct}. S1 tried duplicates, weak true directions with compensating coefficients, rare design
  points and underfitted proxies without success.

## Card S — Lemma S (size tail with an exponential tail; reference-adaptive)
**Statement.** ‖μ‖² ≤ nM (μ ∈ 1^⊥ arbitrary; need not be in col X). Let T ∈ Ω, ϑ ∈ ℝ^T with
B_T(ϑ) := ‖μ − X_Tϑ‖² + (‖X_Tϑ‖² + ‖ϑ‖²)/n ≤ B, R^T_m := Σ_{k>m} q_k/w(|T|). There are C, c, n₀ depending on (σ*², M, B, κ₀)
such that for n ≥ n₀, 1 ≤ t ≤ n^{1−κ₀} and every integer m with
log R^T_m + ½ log D_T + ½ log n + C[1 + √t + t/√n] ≤ −2t:   P_e[ π(|S| > m) > e^{−t} ] ≤ Ce^{−t} + Ce^{−cn}.
**Context:** `W3-POST2/lemmas/B_tail_approx.md` (the proof to re-run), `W3-POST/lemmas/L1a_size_tail.md`, [P1]
(`lem:num`, `lem:den`, `thm:Ta`, `thm:T01iii`), `ARC/W1-T03R/PROOF.md` lines 77–97; `reviews/S1_astra.md` "S" paragraph.
**Routes.** S-a: Claim B's Steps 1–4 with Laurent–Massart/Gaussian tails for Λ″_n, an exponential bound for the s_y
bracket 𝓑_n, Markov on Θ^{(1)} at level e^{t} (use the fixed-rate proper mixture in Θ^{(1)}). S-b: direct — bound
p*(y_c)/m_b(S₀) explicitly by Stirling ((νu)^νe^{−νu}/Γ(ν) ≤ √ν). S-c (adversarial): models of size near n/2 with small
Q^c_S; a design-measurable reference chosen after seeing X.

## Card T — Lemma T (distribution-free transfer)
**Statement.** x₁, …, x_n i.i.d. from any law on ℝ^P; 1 ≤ d ≤ min(P, n − 1); δ ∈ (0, 1). With probability ≥ 1 − δ,
simultaneously for all a ∈ ℝ, c > 0, u ∈ ℝ^P with |supp u| ≤ d:
E_x min{1, (a + uᵀx)²/c} ≤ 2n⁻¹Σ_i min{1, (a + uᵀx_i)²/c} + (4/n)[d log(eP/d) + 2(d+1) log(2en/(d+1)) + log(4/δ)].
**Context:** none in the repo beyond `W3-DIST/STATEMENT.md` §3 and `reviews/S1_astra.md` S1-01. External: the
relative-deviation (ratio-type) VC inequality — the attempt must **state the exact inequality it uses with a
verifiable reference, or prove it** (symmetrisation by a ghost sample; constants may differ from 4 and 4·log S(2n)).
**Routes.** T-a: VC relative deviation for the class of unions of two half-spaces on d coordinates + layer-cake +
Cauchy–Schwarz. T-b: Bernstein + union over a finite net is *not* available without moments — instead use a
self-normalised/Talagrand-type bound for [0, 1]-valued VC-subgraph classes (Bousquet; Giné–Koltchinskii ratio
bounds) and compare constants. T-c (adversarial): heavy-tailed or atomic laws; d close to n; measurability of the
supremum.

## Card V — Lemma V (variational split and moment bound for supersets)
**Statement.** S = S₀ ∪ J, J ∩ S₀ = ∅, η > 0, c = 1 + η, M^{(c)}_T := X_{c,T}(G_T + c(G_T + I)/n)⁻¹X_{c,T}ᵀ,
D′ := M^{(1/c)}_S − M^{(c)}_{S₀}. Then (a) D′ ⪰ 0, ‖D′‖ < 1 and Q^c_{S₀} − Q^c_S ≤ eᵀD′e + (1 + 2/η)ρ′, where
ρ′ := θ*ᵀ(G_{S₀} + I)θ*/n = (‖μ‖² + ‖θ*‖²)/n (≤ M + M′ under (E), (C));
(b) E[(D_{S₀}/D_S)^{1/2} exp(eᵀD′e/(2σ*²))] ≤ (1 + η)^{s₀+|J|/2}; (c) D′ ⪯ (P_S − P_{S₀}) + R₀ with 0 ⪯ R₀ ⪯ P_{S₀}.
No eigenvalue condition.
**Context:** `W3-DIST/work/prior_probe/REPORT.md` §3 and A2 (derivation, unchecked; numerical check C3 in
`probe_checks.py`), [P1] `lem:slab`, `lem:spec`.
**Routes.** V-a: verify A2 line by line and fix the exact definition of ρ′. V-b: independent derivation through the
Gaussian integral identity for marginal likelihood ratios. V-c (adversarial): singular G_S, duplicated columns,
s₀ = 0, |S| near K.

## Card F — stretch S-FIT (sharp rate without (ND)); attack first among the stretch items
**Question.** Does the distance clause of Lemma X — P_e[Π(‖μ̂ − μ‖² > Cσ*²t or |v/σ*² − 1| > C√(t/n) | y) > e^{−ct}] ≤ 2e^{−ct} —
hold under (E), (C) alone (no (ND)), at least in the in-probability form Π(‖μ̂ − μ‖² > M_n log n | y) → 0 for every
M_n → ∞? Known: the size clause fails without (ND) (duplicates give a geometric size tail of ratio ½); Lemma V gives
the design-free superset bound Σ_{|J|=j} π(S₀∪J)/π(S₀) ≤ poly(j)(√(1+η)/2)^j·O_P(1); non-supersets are open.
**Context:** Cards X, V; `work/prior_probe/REPORT.md` §3 "Design-free", A5; `ROUTES.md` §5; `ARC/W1-T03R/PROOF.md`
Proposition D; `work/numerics/RESULTS.md` N4.
**Routes.** F-a (prove): per new direction with Occam factor d_i ∈ [1, n+1] the posterior weight is
d_i^{−1/2}e^{(1−1/d_i)z_i²/2} and the fitted noise (1 − 1/d_i)²z_i²; bound E[weight; fitted noise > τ_i] jointly and sum
over models with the geometric size prior. F-b (break): construct a design with ≍ log n directions at Schur
eigenvalue γ ≍ log n/n (near-copies with τ² ≍ log n/n²) on which Π(‖μ̂ − μ‖² > M log n | y) stays ≥ c^M with c close to 1,
or ≥ n^{−c} for large M. F-c: non-supersets — replace the comparison with S₀ (cost n^{(A+½)s₀}) by a comparison with
the best submodel T ⊆ S₀ and control ρ′_T.

## Cards for the other stretch items (lower priority)
- **S-APX:** Lemma X and DIST-1 with a reference (T, ϑ), B_T(ϑ) ≤ B, bias ‖μ − X_Tϑ‖² ≤ nΔ_n²; the population part of the
  bias (Lemma T applied to the tail coefficients, which are not sparse) is the open step.
- **S-EXP:** Lemma X with log n replaced by ℓ_n = log(p ∨ n), ℓ_n = o(n^{κ₀}); track where p ≤ n^A is used (X1 unions, X3
  constant, d_t log p ≲ t).
