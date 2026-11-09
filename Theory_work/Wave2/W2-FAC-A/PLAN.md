# W2-FAC-A — PLAN

## Route (A, low-rank common-component split), as adapted after the diagnosis

1. **Key lemma L1 (U: uniform factor-aware add bound).** For T ⊆ [p], l ∉ T the add statistic
   Z_{T,l} = (g_l − R̂_{lT}R̂_TT⁻¹g_T)/√R̂_{l|T}, g := Xᵀε/(σ√(n−1)) ~ N(0, R̂) given X (exact identity: u_{T,l}ᵀε/σ).
   (a) Exact case R̂ = Σ = λλᵀ + Ψ: write g = λξ₀ + ζ (ξ₀ ~ N(0,1), ζ ~ N(0,Ψ) independent). With
   𝓗_T = span(g_T) ⊆ 𝓚_T = span(ξ₀, ζ_T) (codim 1), Pythagoras in L²:
   innovation = [ζ_l − P(ζ_l | ζ_{T∩g(l)})] + (P_{𝓚_T} − P_{𝓗_T})g_l, the second along the residual factor
   variable ω_T = ξ₀ − P(ξ₀|g_T) ∝ ξ₀ − λ_TᵀΨ_TT⁻¹ζ_T. Hence the exact formula
   Z = [√ψ_{l|U} Ξ_{l,U} + λ̃_{l|U} W_T/√(1+s_T)] / √(ψ_{l|U} + λ̃²_{l|U}/(1+s_T)).
   The idiosyncratic part has ≤ p2^{γ̄} distinct values (direction count controlled by the groups, not by T); the
   factor part is ONE statistic per T and is bounded uniformly by κ̄ √(top-h mean of group χ²'s) by
   Cauchy–Schwarz in the Ψ-metric + s_T ≥ c_min h_T. Union bounds: max of p2^{γ̄} normals; top-h sums of
   independent χ²_{≤γ̄} (Laurent–Massart + C(G,h) ≤ (eG/h)^h).
   (b) Perturbation: R̂ with ‖R̂ − Σ‖ ≤ δ: couple γ = Σ^{1/2}R̂^{−1/2}g ~ N(0, Σ); innovation coefficients are
   Lipschitz in the matrix (bounded by 1/√ψ₀, NOT by ‖Σ‖ which is ~p); error ≤ C δ (‖g‖ + ‖γ‖) = O(δ√(p loglog n)).
2. **L2 Sandwich** (Q = [p]): re-prove GROW L3.3(a) using its block events in the Q = [p], K = p branch (R01 item 5): the size ladder and |Q| = O(log n) are unnecessary — a maximiser missing a truth has size < p = K, so adding that truth is feasible and TV contradicts maximality; NEG vacuous. Block events from the energy bound, within-block Gram floor, polynomial p and |C_b| ≤ 16.
3. **L3 Descent events on the full lattice 𝓛 = [S₀, [p]]** (exponentially many sets, so no union over 𝓛):
   uniform score expansion for |A| ≤ p + 1 with p = o(n) — det remainder |Σ log((λ_i+1/(n+1))/(λ_i+1))| ≤
   2|A|/((n−1)ψ₀); ridge remainder 0 ≤ Q_A − RSS_A ≤ 1 + o(1); RSS floor from ‖P_{[p]}ε‖² ≤ σ²(p + o(n)).
   NA ⇐ sup Z² ≤ (1 − ε) log n + 2 log((2p−1−k)/(k+1)), from L1 and (P) via the α₀ computation.
   TL: for a truth-removing neighbour, signal θ_i²(a² − b²) ≥ θ_i²(n−1)φ² vs the θ-weighted cross term
   2|θ_i|σ√(n−1)(|Z₁|+|Z₂|) and σ²Z², with |Z| = O(√log n) uniformly (L1); BM-∞ makes both o(signal) (R01 item 3).
4. **L4 Assembly**: GROW L1 (descent, Q = [p], |Q| = p ≤ K), [OP], M5(0), T03♯. (AG) supplies the anchored eigenvalue
   conditions with fixed constants; the energy bound and BM-∞ remain assumptions in the general fixed-design theorem
   (they follow for fixed bounded nonzero θ*_{S₀}) (R01 item 1).
5. **L5 Random design**: design events (Lemma CR / [CONC′]: entrywise ≤ δ'_n = 32√(2(A+1)log n/(n−1)) ⇒
   ‖R̂ − Σ‖_op ≤ p δ'_n, so δ_n√(p loglog n) ≤ p^{3/2}δ'_n √(loglog n) → 0 since p ≤ n^{1/6}); TV on actual
   blocks from (TV-pop) + entrywise control; uniform constants ⇒ diagonal argument (GEN (C4), GROW L6.2).
6. **D Delivery**: A2 template (Lemma S for these classes: nonconstant columns a.s., null response event; allocation
   unchanged — the merged cap ℓ_n + |S̃₀| is already Proposition F's cap a_n); 𝒦_n := deterministic LS0 with cap
   a_n scores S₀ ⊇ Sand ∩ NA ∩ TL; P(Ŝ⁺ ≠ S₀) ≤ 2E[1 − π(S₀)] + P(𝒦_nᶜ).
7. **Instances**: κ = 1 for every block-CS (closed form in STATEMENT §2); TV for CS by the explicit partial-covariance
   formula (1−a)[θ_j + a(Θ − Θ_U)/(1 − a + a|U|)] under (GC-CS); S5 layouts: certificate over all configurations in 𝔅_n —
   either prove that complete-linkage + next-fit yields unions of whole groups on a design event, or certify all
   blocks of size ≤ 16 (R01 item 7).
8. **Part II SHARP** (R01 item 8): exact-Gram CS, m = ⌈log p⌉, T = S₀ ∪ {m nulls with largest ζ}, l = null with smallest
   ζ; |Z_{T,l}| = (2 + o_P(1))√(2 log p); small-model lower score comparison valid for p ≤ K (p may be ∝ n).
9. **Part III frontier**: Lemma CS-1D (exact 1-D reduction, numerics/cs1d.py) and the gap invariant written as tools
   with numerics D2/D3; p > K and k ≥ 2 described with the exact failing step.

## Review pipeline (Wave 2 protocol)
Statement lock (Codex gpt-6.1-sol high) → L1 with falsification numerics + xhigh check (key lemma) → CHECKPOINT →
L2–L5, D, I, SHARP each: falsification numerics + Sol high check → mid-point (fresh Sol xhigh, CONTINUE?) → sweep
(Sol xhigh) → council (Sol xhigh + Opus high, both ≥ 8.0, six gates). CITECHECK before council.

## Falsification numerics planned
* F-U: Monte Carlo of sup over random + one-sided + greedy-adversarial T of |Z_{T,l}| vs the L1 bound (exact Σ and
  iid R̂), CS/S5/block-CS; check the exact formula numerically (identity to 1e-10).
* F-NA: NA/TL on lattice sets at p ≈ n^{0.12} (inside α₀) vs p ≈ n^{0.3} (outside) in the exact simulator.
* F-SHARP: one-sided sets violate NA for log p/log n > 1/6 at large n (exact 1-D simulator).
