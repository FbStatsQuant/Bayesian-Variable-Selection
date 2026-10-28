# STATEMENT — T13 (T10): restricted ESS and the omitted-mass identity

Source: `Theory_architecture_v3/theorems/T13_T10_restricted_ESS.md` (all parts), read with `00_COMMON.md`, `THEORY_BRIEF.md` §2.10 and the method file `METHODOLOGY_v3.md` §6.7 (SHA-256 93043758058a6d422cca6ca4b6be8f3a9e8149b6f6de2e1bab1ce31c44b8019c).
Version 3 (after statement checks 1 and 2). Changes against the source are listed in §2 with reasons.

## 0. Setting and definitions

- **Data and model objects** are those of 00_COMMON §1: standardised X, y; Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋); m(S), BF(S) = m(S)/m(∅); ϖ(S) = w(|S|)/W_K with w(k) = ½/C(2p−1, k).
- **Bridge** (00_COMMON §2, METHODOLOGY §6.3): blocks C₁, …, C_J; tables r_b(U) = BF(U), U ⊆ C_b; γ₀(S) = ϖ(S)∏_b r_b(S ∩ C_b); d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b). For every real ψ: γ_ψ = γ₀e^{ψd}, Z̄_ψ = Σ_{S∈Ω}γ_ψ(S), q_ψ = γ_ψ/Z̄_ψ. (The proof shows from these definitions that γ₀ > 0 and d is finite on Ω, so every q_ψ has full support.) For nonempty A ⊆ Ω: Z̄_ψ(A) = Σ_{S∈A}γ_ψ(S), q_ψ(A) = Z̄_ψ(A)/Z̄_ψ, q^A_ψ = q_ψ(· | A).
- **Candidate set.** V is a nonempty subset of Ω, held fixed. a(ψ) = a_V(ψ) := q_ψ(V); for nonempty W ⊆ V, a_W(ψ) := q_ψ(W).
- **χ² divergence.** For laws μ, λ on a finite set with λ > 0 wherever μ > 0: χ²(μ‖λ) = Σ_{S:λ(S)>0} λ(S)(μ(S)/λ(S))² − 1.
- **Restricted ESS.** For real u, v and w := 2v − u: ρ_V(u, v) = Z̄_v(V)²/(Z̄_u(V)Z̄_w(V)) = exp{2F_V(v) − F_V(u) − F_V(w)}, F_V(t) = log Σ_{S∈V}γ₀(S)e^{td(S)}. An interval (u, v), u < v, is **accepted** if ρ_V(u, v) ≥ 0.9.
- **Grid.** 0 = φ₀ < φ₁ < … < φ_T = 1, T ≥ 1; w_t = 2φ_t − φ_{t−1}; 𝓔_grid = {φ₀, …, φ_T, w₁, …, w_T}.
- **Candidate-grid construction** (METHODOLOGY §6.7). Inputs: an increasing list of pilot temperatures in (0, 1] ending at 1, the candidate set V, T_e. Start at u = 0; for the next pilot temperature b: if ρ_V(u, b) ≥ 0.90 append b; else bisect on (u, b] with u fixed, at most 60 halvings, and append the largest tested endpoint that passes (ρ_V(u, ·) ≥ 0.90); continue from the appended point; validate strict progress and the inequality at every appended point; non-progress, failed validation or more than T_e intervals ⇒ failure. A **successful construction** outputs a grid. An **implementation** of the construction is a fixed deterministic procedure realising these rules (it fixes the bisection points, stopping and endpoint choices); it accesses the bridge only through evaluations of ρ_V.
- **Candidate set of the method's form.** For a set 𝒫 ⊆ Ω of scored models (the *pool*), V(𝒫) := top-20p of 𝒫 by log γ₀ ∪ top-20p of 𝒫 by log γ₁ ∪ {∅} (ties lexicographic; if |𝒫| ≤ 20p each top list is all of 𝒫).
- **COVER(W, ε_C)**, for nonempty W ⊆ Ω, a grid, and **0 ≤ ε_C < 1**: q_ψ(W) ≥ 1 − ε_C for every ψ ∈ 𝓔_grid.
- **EX-A**: exact scores, sums, probabilities and comparisons.
- **Method-class witness** (used in (ii)(c)–(d)): a raw data set (X^r, y^r) satisfying the method's input conditions (n ≥ 3, no constant column, y^r non-constant) on which the exact-branch condition Σ_{k≤K}C(p, k) ≤ (5H₀ + 4N₀)p fails (so the SMC branch runs); the method's blocks, tables, γ₀ and d for these data; a candidate set V = V(𝒫) of the method's form for some pool 𝒫 ⊆ Ω; a tier e ∈ {0, 1} with T_e = 4^eT₀ computed from the data's (n, p) (00_COMMON §2 budgets); a fixed deterministic implementation of the construction as in this section; a list of pilot temperatures; and the grid that this implementation outputs, successfully and under EX-A, from V, that list and T_e. (No claim is made about the probability that the random pilot outputs that list, or that a calibration reaches the pool 𝒫.)

## 1. Statement

Throughout, V ⊆ Ω is nonempty and fixed, u, v are real, w = 2v − u.

**(i) Identity.** For all real u, v (in particular u < v):
  1 + χ²(q_v ‖ q_u) = ρ_V(u, v)⁻¹ · a(v)²/(a(u)a(w)).

**(ii) Coverage corollary.**
(a) Let 0 ≤ ε_C < 1. If (u, v) is accepted and a(u) ≥ 1 − ε_C and a(w) ≥ 1 − ε_C, then 1 + χ²(q_v ‖ q_u) ≤ 10/(9(1 − ε_C)²).
(b) Assume EX-A. Let (φ_t)_{t=0}^T be the output of a successful candidate-grid construction run with candidate set V (in particular the frozen grid of a calibration, paired with the V of the construction that produced it). Then every interval (φ_{t−1}, φ_t) is accepted; its evaluation points φ_{t−1}, φ_t, w_t lie in 𝓔_grid; and if COVER(V, ε_C) holds, then 1 + χ²(q_{φ_t} ‖ q_{φ_{t−1}}) ≤ 10/(9(1 − ε_C)²) for every t = 1, …, T.
(c) Coverage on [0, 1] alone does not supply the hypothesis of (a) when w_t > 1: there is a method-class witness with grid T = 1 (φ₀ = 0, φ₁ = 1, w₁ = 2) such that, with ε_C = 0.1, the interval (0, 1) is accepted and q_ψ(V) ≥ 1 − ε_C for every ψ ∈ [0, 1], but q_{w₁}(V) < 1 − ε_C and 1 + χ²(q₁ ‖ q₀) > 10/(9(1 − ε_C)²).
(d) The largest w_t is not automatically the worst coverage point: there is a method-class witness with grid T = 2 (both intervals accepted) such that the minimum of ψ ↦ q_ψ(V) over 𝓔_grid is attained only at φ₀, not at max_t w_t, and the minimum over {w₁, …, w_T} is not attained at max_t w_t.

**(iii) Restricted working set.** For every nonempty W ⊆ V and all real u, v:
  1 + χ²(q^W_v ‖ q^W_u) = ρ_V(u, v)⁻¹ · (a_V(v)²/a_W(v)²) · (a_W(u)a_W(w))/(a_V(u)a_V(w)).
In particular (W = V) ρ_V(u, v) = 1/(1 + χ²(q^V_v ‖ q^V_u)). Moreover, with 0 ≤ ε_C < 1, if (u, v) is accepted and a_W(v) ≥ 1 − ε_C, then 1 + χ²(q^W_v ‖ q^W_u) ≤ 10/(9(1 − ε_C)²). Hence, for a grid as in (ii)(b), COVER(W, ε_C) gives at every interval t both 1 + χ²(q^W_{φ_t} ‖ q^W_{φ_{t−1}}) ≤ 10/(9(1 − ε_C)²) and (because W ⊆ V, COVER(W, ε_C) implies COVER(V, ε_C)) the bound of (ii)(b).

**(iv) Restricted grid.** Let 𝓜 ⊆ Ω with ∅ ∉ 𝓜.
(a) Let V = V(𝒫) be of the method's form. If 𝒫 ∩ 𝓜 = ∅ (pool avoidance), then V ∩ 𝓜 = ∅. Pool avoidance holds, in particular, when calibration never scores 𝓜 and every member of 𝒫 was scored by the calibration or belongs to an inherited set of scored models (tables, leaders carried across tiers) that is assumed to avoid 𝓜.
(b) Suppose V ∩ 𝓜 = ∅. Let γ′_φ := γ_φ1_{𝓜^c} for real φ (the bridge on Ω′ = Ω ∖ 𝓜 ∋ ∅ with γ₀, d restricted to Ω′; q′_φ = q_φ(· | 𝓜^c)). Then F′_V = F_V and ρ′_V = ρ_V on all real arguments, and, under EX-A, one and the same implementation of the candidate-grid construction, run on the restricted and on the original bridge with the same pilot temperatures, the same V and the same T_e, has the same outcome (the same grid, or failure in both).

No assertion derives particle mixing from ESS.

## 2. Changes against the source statement, with reasons

1. **ε_C ∈ [0, 1)** added (approved in check 1): for ε_C ≥ 1 the bound is undefined or false.
2. **(iv)(a) pool avoidance** made the explicit hypothesis (modification of check 1): 𝒫 ∩ 𝓜 = ∅ is sufficient for V ∩ 𝓜 = ∅. The source's wording "calibration never scores 𝓜" is kept as a sufficient condition, with the provenance condition that every pool member was scored by the calibration or comes from an inherited set assumed to avoid 𝓜 (the method does not say whether tables or carried leaders feed V's top lists).
3. **(ii)(b) the V paired with a grid** is the candidate set of the construction that produced it (approved in check 1).
4. **(ii)(c)–(d) witnesses are method-class** (replaces the rejected abstract-bridge version): real data run through the method's blocks, tables, γ₀ and d, on the SMC branch; V of the method's form; a grid output by the construction. The pilot's random output is not claimed; the pilot temperatures enter as construction inputs, as they do in the source's (iv).
5. **(iii) the bound uses coverage at v** (a_W(v) ≥ 1 − ε_C), supplied by COVER(W, ε_C) because φ_t ∈ 𝓔_grid; both the restricted and the full-space bound are stated (approved in check 1; the condition is sufficient, not claimed necessary).
6. **(i), (iii) for all real u, v** (approved in check 1).
7. **Positivity**: γ₀ > 0 and d finite on Ω are derived in the proof from the definitions of 00_COMMON §1 (ϖ > 0, m(S) ∈ (0, ∞)), not assumed.
8. **(iv)(b) implementation**: the "unchanged construction" conclusion is for one fixed deterministic implementation applied to both bridges (check 1: EX-A alone does not fix bisection and endpoint choices).
9. **(ii)(d) strengthened** (recorded at check 2): the witness must have the grid-evaluation minimum attained **only** at φ₀ (the source asks only that the largest w_t not be the worst point). This is a strengthening, not a weakening.
10. **Witness parameters** (modification of check 2): a witness names its tier e, uses T_e = 4^eT₀ from its own data, and fixes a deterministic implementation.
