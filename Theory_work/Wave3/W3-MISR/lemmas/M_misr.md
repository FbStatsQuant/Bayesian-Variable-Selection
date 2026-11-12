# M — Theorem MIS-R (i), (i′), (ii) (W3-MISR)

Status, one line per claim (verbatim source for the registry):
- MIS-R (i): **PROVED (by this seat, unchecked), conditional on W3-POST2:C**
- MIS-R (i′): **PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1**
- MIS-R (ii): **PROVED (by this seat, unchecked), conditional on W3-POST2:C, W3-POST2:E, W3-POST2:A1**

Check record: line check K1 (gpt-6.1-sol high, blind, `../reviews/K1_RM_check_sol.md`): MIS(i), (i′)(c), (ii)(a)–(c)
VERIFIED; (i′)(a), (b), (d) VERIFIED-WITH-AMENDMENTS (0 FATAL / 0 MAJOR / 1 MINOR, applied [K1-1],
`../reviews/K_disposition.md`).
Notation: `../STATEMENT.md` (v1.3); `R_reduction.md` (Lemma R′, displays (R1)–(R3), R.5 for part (c), table R.6). Sources: [POST2] =
`Theory_work/Wave3/W3-POST2/STATEMENT.md`; [C] = `Theory_work/Wave3/W3-POST2/lemmas/C_expectation.md`; [A] =
`…/W3-POST2/lemmas/A_occam.md`; [E] = `…/W3-POST2/lemmas/E_visibility.md`; [W3P] = `Theory_work/Wave3/W3-POST/STATEMENT.md`;
[D] = `…/W3-POST2/lemmas/D_hellinger.md`; [T03R] = `Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/W1-T03R/PROOF.md`; [P3] =
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T03_A2_selection_consistency/PROOF_v2.tex`.

Throughout, for a configuration κ = (x, β, v), a tilde denotes the unit-noise model (x, β/√v, σ*² = 1) of Lemma R′(b),
P̃, Ẽ its probability and expectation, and δ := 1 − π_𝒞(S₀(κ)). By Lemma R′(b), for every functional F of the posterior
(a measurable function of the probability vector on Ω and of κ): E_κ F(π_𝒞(· | x, y^r)) = Ẽ F(π_𝒞(· | x, ỹ)).   (M0)

## M.1 Proof of MIS-R (i)

Fix s, A, M, φ₀, C_OS, c > c₁(s, A), and (n₀, C) := the constants of [POST2] Claim C, case (iii), for
(s₀, A, σ*², M, φ₀, c, C_OS) = (s, A, 1, M, φ₀, c, C_OS) ([POST2] lines 85-89; [C] lines 9-15: "n₀ and C depending only
on these", "for every n ≥ n₀ and every fixed design X and θ* for which, at that n, … hold").
Let n ≥ n₀ and κ ∈ 𝒦_n(s, A, M, φ₀, C_OS, c). By table R.6 the unit-noise model satisfies, at this n: s₀ = s ≤ K,
2 ≤ p ≤ n^A, G with σ*² = 1, (E) with constant M, (F₀), (OS; C_OS) and (ID^M; c) with c > c₁(s, A) — the hypotheses of
case (iii). Hence Ẽ δ ≤ C r_n, and by (M0) E_κ δ = Ẽ δ ≤ C r_n. The bound holds for every κ in the class, so for the
supremum. For 𝒦^λ_n and c > c₀(s, A): the same with case (ii) ((F_λ), (OS), BM(c), c > c₀) and its constants. ∎
(The constants were chosen before κ and do not involve v: the class constrains v only through the ratios in (E^σ),
(ID^{M,σ}), (BM^σ).)
**Stability.** Let y^r have any law with y^r non-constant a.s., n ≥ n₀, κ in the class. h(π) := 1 − π(S₀(κ)) is a
measurable [0, 1]-valued function of the posterior, so by Lemma R′(c)
E[1 − π_𝒞(S₀(κ) | x, y^r)] ≤ E_κ δ + d_TV(Law(T(y^r)), Law(T_G(κ))) ≤ C r_n + d_TV(Law(T(y^r)), Law(T_G(κ))). The same
applies to every [0, 1]-valued functional below (indicators of {HPM ≠ S₀}, with a tie rule that is a function of the
posterior, and the posterior masses of §3); under (PR) the total-variation term is 0. ∎

**Consequences.** Deterministic facts, for every data set: (1a) max_j |PIP_j − 1{j ∈ S₀}| ≤ δ ([W3P] line 84:
for j ∈ S₀, 1 − PIP_j = π(S ∌ j) ≤ π(S ≠ S₀); for j ∉ S₀, PIP_j = π(S ∋ j) ≤ π(S ≠ S₀)). (1b) for T ≠ S₀:
π_𝒞(T) ≤ 1 − π_𝒞(S₀) = δ (convention π_𝒞(T) = 0 off Ω). (2a) If HPM ≠ S₀ then π_𝒞(S₀) ≤ π_𝒞(HPM) ≤ 1 − π_𝒞(S₀), so
δ ≥ ½. (2b) If MPM ≠ S₀ there is j with |PIP_j − 1{j ∈ S₀}| ≥ ½ (j ∈ S₀ with PIP_j ≤ ½, or j ∉ S₀ with PIP_j > ½), so
δ ≥ ½ by (1a). (2c) If ξ_q ≠ S₀ there is j ∈ S₀ with PIP_j ≤ q or j ∉ S₀ with PIP_j > q, so δ ≥ min(q, 1 − q) by (1a).
Markov's inequality with E_κ δ ≤ C r_n gives items 1–2 of the statement.
Item 3: under [MIS1]'s GR, β = β_𝒞 + γ and S₀(κ) = supp β. If β_𝒞,j = 0 ≠ γ_j then j ∈ S₀(κ) and 1 − PIP_j ≤ δ; if
β_𝒞,j ≠ 0 = β_𝒞,j + γ_j then j ∉ S₀(κ) and PIP_j ≤ δ; if T := S₀^{full} ∩ 𝒞 ≠ S₀(κ) then π_𝒞(T) ≤ δ by (1b). Take E_κ. ∎

## M.2 Proof of MIS-R (i′)

Work in the unit-noise model at a fixed n, with the notation of [C], [A], [E] (σ*² = 1): ℓ(S) := w(|S|)m(S), so that
π(S) ≤ ℓ(S)/ℓ(S₀) for S ∈ Ω ([P3] lines 39-41); Ξ_j := Σ_{J⊆[p]∖S₀, |J|=j} ℓ(S₀ ∪ J)/ℓ(S₀) ([P3] line 227); the events
𝒢^sup_n, 𝒢⁵_n ([POST2] lines 18-21; [A] lines 46-53; [E] lines 23-24); Υ′_n, Υ′^{>j₁}_n ([A] lines 64-66);
T₀ := π(|S| > m♯_n).

**Standing assumption for (I1)–(I6) [K1-1].** At the given n: s₀ = s ≥ 1 and A ≥ 1 are the fixed constants,
2 ≤ p ≤ n^A and s₀ ≤ K (the per-n size conditions of regime R1, [W3P] lines 63-64; in the applications below they are
(SZ)), and σ*² = 1. The sources state (I2)–(I5) "in R1" ([A] line 53: "under G, (E) and R1 alone"; [E] line 26); the
asymptotic part of R1 enters them only through thresholds "n ≥ n₀", which here are the common threshold n₁ below.
**Inputs, each a bound at a single n** (in addition to the standing assumption, the hypotheses named are those at
that n):
- (I1) [C] Lemma C2 with m = m♯_n ([C] lines 31-42), under G, (E), (F₀), s₀ ≤ K, n ≥ 16:
  Ẽ T₀ ≤ (κ²/c_den)(1 + 1/n)^{s₀/2} n^{−1/2} + (8 + 24M)/(n − 1) + e^{−N/8}, with κ²/c_den depending only on (M, φ₀).
- (I2) [A] (G3′) ([A] lines 52-53; [E] lines 26, 31-33): P̃((𝒢^sup_n)ᶜ) ≤ 4/n and P̃((𝒢⁵_n)ᶜ) ≤ 1/n for n ≥ n₀, under
  G, (E) and the size conditions.
- (I3) [A] (C5′)(a) ([A] lines 66, 69-70), under G, (E), (F₀): for n ≥ n₀, on 𝒢^sup_n, for every integer j₁ ≥ 0,
  Σ_{j=j₁+1}^{min(m♯_n, p−s₀)} Ξ_j ≤ e^{ρ_n}Υ′^{>j₁}_n, with ρ_n = 8(M + 1)/(Nφ₀²) ([P3] line 201 at σ*² = 1).
- (I4) [A] (C5′)(b) ([A] lines 67, 71-74): for n ≥ n₀, Ẽ Υ′^{>j₁}_n ≤ 𝒪_n^{>j₁}; with (OS; C_OS):
  Ẽ Υ′_n ≤ C_OS r_n and (2p)^{s₀}(n + 1)^{s₀/2} Ẽ Υ′^{>j₀}_n ≤ C_OS r_n.
- (I5) [E] Lemma E1(b) ([E] lines 26-27, 35-54), under G, (E), (F₀), c > c₁(s₀, A): for n ≥ n₀, on 𝒢^sup_n ∩ 𝒢⁵_n,
  **every** S ∈ 𝔉 with L_S ≥ c log n satisfies ℓ(S)/ℓ(S ∪ S₀) ≤ n^{−2}. (The lemma is stated per model S; no global
  margin is used.)
- (I6) [T03R] (C6)(a) (lines 187-189; every data set, no condition): for every underfitting S,
  ℓ(S)/ℓ(S ∪ S₀) ≤ (2p)^{s₀}(n + 1)^{s₀/2}.
The thresholds "n ≥ n₀" in (I2)–(I5) are those inside the proof of [POST2] Claim C, case (iii) ([C] lines 44-55 uses
exactly (I1)–(I6)); by that claim they depend only on (s₀, A, M, φ₀, c, C_OS) (at σ*² = 1). Let n₁ be the largest of
them, of 16, and of the first n with e^{ρ_n} ≤ 2 (i.e. N ≥ 8(M + 1)/(φ₀² log 2)); n₀′ := n₁.

**(a) Supersets.** Let κ ∈ 𝒦⁰′_n(s, A, M, φ₀, C_OS) (the class with the first (OS) inequality only [R1-F5]) and
n ≥ n₁ᵃ := the largest of 16, the thresholds of (I1)–(I4) and the first n with e^{ρ_n} ≤ 2; none of these involves c, and
n₁ᵃ ≤ n₁ = n₀′. By table R.6 the unit-noise model satisfies G, (E), (F₀), 𝒪_n^{>0} ≤ C_OS r_n and the size conditions at n. Every S ∈ Ω with S ⊋ S₀ either has |S| > m♯_n or is S₀ ∪ J with
1 ≤ |J| ≤ m♯_n − s₀ ≤ min(m♯_n, p − s₀); so ([P3] lines 227-229; [A] line 85)
  π(S ⊋ S₀) ≤ T₀ + Σ_{j=1}^{min(m♯_n, p−s₀)} Ξ_j.
On 𝒢^sup_n the sum is ≤ e^{ρ_n}Υ′_n ≤ 2Υ′_n by (I3) (j₁ = 0); off it use π ≤ 1. Since Υ′_n ≥ 0,
  Ẽ π(S ⊋ S₀) ≤ Ẽ T₀ + 2Ẽ Υ′_n + P̃((𝒢^sup_n)ᶜ) ≤ (κ²/c_den)·2^{s/2} n^{−1/2} + (8 + 24M)/(n − 1) + e^{−N/8} + 2C_OS r_n + 4/n
by (I1), (I4), (I2). Each term is ≤ a constant times r_n for n ≥ 3 (n^{−1/2} ≤ r_n; 1/(n − 1) ≤ 2r_n; e^{−N/8} ≤ 8/N). This
gives Ẽ π(S ⊋ S₀) ≤ C′_a r_n with C′_a depending on (s, M, φ₀, C_OS), and (M0) transfers it to E_κ. ∎
(These are the first two terms and the probability term of the proof of Claim C, [C] lines 47-50, 54; they do not
use the margin. [A] lines 85-86 states the same decomposition for the O_P version. Of (OS), only the first
inequality 𝒪_n^{>0} ≤ C_OS r_n was used — through (I4) with j₁ = 0.)

**(b) Strong coordinates.** Let moreover j ∈ S₀(κ) satisfy (ID^{M,σ}_j; c), c > c₁(s, A); in the unit-noise model:
L_S ≥ c log n for every S ∈ 𝔉 with j ∉ S. Put 𝒰_j := {S ∈ Ω : |S| ≤ m♯_n, j ∉ S}. Every S ∈ Ω with j ∉ S has |S| > m♯_n
or lies in 𝒰_j, so π(S ∌ j) ≤ T₀ + π(𝒰_j) ≤ T₀ + Σ_{S∈𝒰_j} ℓ(S)/ℓ(S₀).
Every S ∈ 𝒰_j is underfitting (j ∈ S₀∖S). Write S′ := S ∪ S₀ = S₀ ∪ J′, J′ := S∖S₀, and
ℓ(S)/ℓ(S₀) = [ℓ(S)/ℓ(S′)]·[ℓ(S′)/ℓ(S₀)]. Here |J′| ≤ |S| ≤ m♯_n and s₀ + |J′| = |S′| ≤ p. Each set S′ = S₀ ∪ J′ arises
from at most 2^{s₀} − 1 models S (S = J′ ∪ (S ∩ S₀) with S ∩ S₀ ⊊ S₀).
- If |J′| ≤ j₀: S ∈ 𝔉 (S ∈ Ω, S₀ ⊄ S, |S∖S₀| ≤ j₀) and j ∉ S, so L_S ≥ c log n, and (I5) gives ℓ(S)/ℓ(S′) ≤ n^{−2} on
  𝒢^sup_n ∩ 𝒢⁵_n.
- If |J′| > j₀: (I6) gives ℓ(S)/ℓ(S′) ≤ (2p)^{s₀}(n + 1)^{s₀/2}.
Summing over S ∈ 𝒰_j, grouped by J′ (J′ = ∅ contributes ℓ(S₀)/ℓ(S₀) = 1; |J′| = i ≥ 1 contributes to Ξ_i), on
𝒢^sup_n ∩ 𝒢⁵_n, with (I3) for j₁ = 0 and j₁ = j₀:
  Σ_{S∈𝒰_j} ℓ(S)/ℓ(S₀) ≤ 2^{s₀} n^{−2} (1 + Σ_{i=1}^{min(j₀, m♯_n, p−s₀)} Ξ_i) + 2^{s₀}(2p)^{s₀}(n + 1)^{s₀/2} Σ_{i=j₀+1}^{min(m♯_n, p−s₀)} Ξ_i
            ≤ 2^{s₀} n^{−2} (1 + 2Υ′_n) + 2^{s₀}·2·(2p)^{s₀}(n + 1)^{s₀/2} Υ′^{>j₀}_n.
(This is the display of [E] lines 61-65 with 𝒰 replaced by 𝒰_j, as [E] lines 67-68 notes; cf. [T03R] (C8) lines
194-197.) Taking expectations on the event (the right side is non-negative) and using π ≤ 1 off it, with (I1), (I2), (I4):
  Ẽ π(S ∌ j) ≤ Ẽ T₀ + 2^{s}[n^{−2}(1 + 2C_OS r_n) + 2C_OS r_n] + 5/n ≤ C′_b r_n,
C′_b depending on (s, M, φ₀, C_OS). (M0) transfers the bound to E_κ. With C′ := max(C′_a, C′_b) this proves (b) for
each such j. For the set J := J^M_n(κ; c): {S ⊉ J} = ⋃_{j∈J}{S ∌ j}, so π(S ⊉ J) ≤ Σ_{j∈J} π(S ∌ j) and
E_κ π_𝒞(S ⊉ J) ≤ |J|·C′ r_n ≤ s·C′ r_n (zero if J = ∅). ∎

**(c) Beta-min form.** Assume also (F_λ; φ₀) at κ and let j ∈ S₀(κ) with θ_j(κ)² ≥ c″v log n/(nφ₀²), c″ ≥ cn/(n − 1).
Let S ∈ 𝔉 with j ∉ S and S′ := S ∪ S₀; |S′∖S₀| ≤ j₀, so (F_λ) gives λ_min(G_{S′}) ≥ Nφ₀², and [P3] `lem:signal` (as used in
[E] lines 76-77) gives Δ_S ≥ Nφ₀²‖θ_{S₀∖S}(κ)‖² ≥ Nφ₀²θ_j(κ)² ≥ (N/n)c″v log n ≥ cv log n. Since L_S ≥ Δ_S ([POST2] line 41;
[E] line 9), (ID^{M,σ}_j; c) holds, i.e. j ∈ J^M_n(κ; c). (The inequality Δ_S ≥ Nφ₀²‖θ_{S₀∖S}‖² is homogeneous of degree
2 in the mean, so it may be read at κ or in the unit-noise model.) ∎

**(d) Localisation.** Let n ≥ n₀′, κ ∈ 𝒦⁰_n(s, A, M, φ₀, C_OS), c > c₁(s, A), and in the unit-noise model
𝒩 := {S₀} ∪ {S ∈ 𝔉 : L_S < c log n} (= 𝒩_n(κ; c), since the unit-noise loss is L_S(κ)/v). Let S ∈ Ω∖𝒩. Then one of
the following holds: |S| > m♯_n; or S ⊋ S₀ with |S| ≤ m♯_n; or S is underfitting (S₀ ⊄ S) with |S| ≤ m♯_n and S ∉ 𝒩.
(S ≠ S₀, and every S ∈ Ω other than S₀ either contains S₀ strictly or does not contain it.) Call the third family
𝒰_far. For S ∈ 𝒰_far with J′ := S∖S₀: if |J′| ≤ j₀ then S ∈ 𝔉, so S ∉ 𝒩 means L_S ≥ c log n and (I5) gives
ℓ(S)/ℓ(S ∪ S₀) ≤ n^{−2} on 𝒢^sup_n ∩ 𝒢⁵_n; if |J′| > j₀, (I6) applies. This is exactly the dichotomy used in (b), with 𝒰_j
replaced by 𝒰_far, so the same computation gives, on 𝒢^sup_n ∩ 𝒢⁵_n,
  π(𝒰_far) ≤ 2^{s₀} n^{−2}(1 + 2Υ′_n) + 2^{s₀}·2·(2p)^{s₀}(n + 1)^{s₀/2}Υ′^{>j₀}_n,
and, with the bound of (a) for the first two families,
  Ẽ π(Ω∖𝒩) ≤ Ẽ T₀ + 2Ẽ Υ′_n + 2^{s}[n^{−2}(1 + 2C_OS r_n) + 2C_OS r_n] + 5/n ≤ C′_d r_n.
(M0) transfers it; enlarge C′ to max(C′_a, C′_b, C′_d). If |S| ≥ s + j₀ then S ≠ S₀ and S ∉ 𝔉 (a model in 𝔉 has
|S ∩ S₀| ≤ s − 1 and |S∖S₀| ≤ j₀, so |S| ≤ s + j₀ − 1); hence {|S| ≥ s + j₀} ⊆ Ω∖𝒩. ∎
(This is the "mass outside 𝒮_n" step of the proof of [POST2] Claim D(b), [D] lines 50-59, taken in expectation; here
it does not need Lemma E0, because models with |S| > m♯_n are charged to T₀ whatever their type.)

## M.3 Proof of MIS-R (ii)

**Set-up.** 𝔎_n := the configuration space at n with its Borel σ-field (STATEMENT §0, Conventions). Define
g_n : 𝔎_n × ℝ^N → [0, 1] by g_n(κ, w) := 1 − Φ(x, Uᵀxβ + √v·w)(S₀(κ)) if Uᵀxβ + √v·w ≠ 0 and S₀(κ) ∈ Ω, g_n := 1 otherwise
(Φ of `R_reduction.md` (R1); Φ(x, u)(T) is the posterior mass of T). g_n is Borel: on each stratum
{p = p′, supp β = T} (a Borel set; finitely many T for each p′) the map (x, β, v, w) ↦ (X, y) is continuous where
it is defined (x has non-constant columns; the contrast vector is non-zero), and the posterior weights are continuous
functions of (X, y).
By (R1) and GR^c | 𝓕_n: Uᵀy^r = UᵀX^r_𝒞β^𝒞 + σ_𝒞W_n, so δ_n = g_n(κ_n, W_n) almost surely. For fixed κ,
G_n(κ) := ∫ g_n(κ, w) N_N(0, I)(dw) = E_κ δ (the law N_N(Uᵀxβ, vI) of the contrast vector is a law satisfying GR^c at κ,
and by R′(b) all such laws give the same value); G_n is Borel by Fubini.

**(a)** κ_n is 𝓕_n-measurable and W_n is independent of 𝓕_n with law N_N(0, I). By the substitution ("freezing")
property of conditional expectations for a bounded jointly measurable function of an 𝓕_n-measurable variable and an
independent one, E[g_n(κ_n, W_n) | 𝓕_n] = G_n(κ_n) a.s. By MIS-R (i), G_n(κ) ≤ C r_n for every κ ∈ 𝒦_n(s, A, M, φ₀, C_OS, c)
and n ≥ n₀. Hence E[δ_n | 𝓕_n] ≤ C r_n a.s. on {κ_n ∈ 𝒦_n(…)} (an event of 𝓕_n: the class is a Borel subset of 𝔎_n,
being defined on each stratum by finitely many inequalities between Borel functions — eigenvalues, determinants and
ranks of Gram matrices, quadratic forms). For 𝒜_n ∈ 𝓕_n inside that event:
E[δ_n 1_{𝒜_n}] = E[1_{𝒜_n}E[δ_n | 𝓕_n]] ≤ C r_n P(𝒜_n), and E δ_n ≤ E[δ_n 1_{𝒜_n}] + P(𝒜_nᶜ) (δ_n ≤ 1). By M.1 (2a)–(2c),
{HPM ≠ S₀(κ_n)} ∪ {MPM ≠ S₀(κ_n)} ⊆ {δ_n ≥ ½} and {ξ_q ≠ S₀(κ_n)} ⊆ {δ_n ≥ min(q, 1 − q)}, so e.g.
P(HPM ≠ S₀(κ_n)) ≤ P(𝒜_nᶜ) + P(δ_n ≥ ½, 𝒜_n) ≤ P(𝒜_nᶜ) + 2C r_n. The same argument with the functionals
π_𝒞(S ⊋ S₀(κ)), π_𝒞(S ∌ j), π_𝒞(S ⊉ J^M_n(κ; c)), π_𝒞(Ω∖𝒩_n(κ; c)) in place of δ (each a Borel function of (κ, w); for the coordinate
clause j is a fixed label and the event is {κ_n ∈ 𝒦⁰_n, j ∈ J^M_n(κ_n; c)}) gives the conditional versions of §3, and
with 𝒦^λ_n that of the second sentence of §2. ∎

**(b)** On 𝒜_n ∩ {s(κ_n) = s′} (an event of 𝓕_n), κ_n ∈ 𝒦_n(s′, A, M, φ₀, C_OS, c) with c > c₁(s′, A), so by (a) for the
slice s′, E[δ_n | 𝓕_n] ≤ C(s′) r_n a.s. there, for n ≥ n₀(s′). The finitely many slices s′ ∈ {1, …, s̄} cover 𝒜_n; take
the maxima of n₀(s′) and C(s′). ∎

**(c)** Fix η > 0 and its constants, events 𝒜^η_n, and (n₀^η, C^η) from (b). For n ≥ n₀^η and L > 0, by Markov's
inequality on 𝒜^η_n: P(δ_n > L r_n) ≤ P((𝒜^η_n)ᶜ) + E[δ_n 1_{𝒜^η_n}]/(L r_n) ≤ P((𝒜^η_n)ᶜ) + C^η/L. Hence
limsup_n P(δ_n > L r_n) ≤ η + C^η/L, and lim_{L→∞} limsup_n P(δ_n > L r_n) ≤ η. As η is arbitrary the limit is 0:
δ_n = O_P(r_n). By M.1 (1a) the same holds for max_j |PIP_j − 1{j ∈ S₀(κ_n)}| ≤ δ_n. Finally
P(HPM ≠ S₀(κ_n)) ≤ P((𝒜^η_n)ᶜ) + 2C^η r_n, so limsup_n ≤ η for every η, i.e. → 0; likewise MPM. ∎

**Remark (what GR^c | 𝓕_n asks).** Only that the normalised contrast residual W_n is a standard Gaussian vector
independent of 𝓕_n. With 𝓕_n = σ(X^r_𝒞) and a regular conditional law this reads: given X^r_𝒞 = x,
Uᵀ(y^r − xβ^𝒞(x)) ~ N_N(0, σ²_𝒞(x)I). A larger 𝓕_n (e.g. containing a random slope, as in [MIS1] Example E2) is
allowed; the target S₀(κ_n) is then 𝓕_n-measurable.
