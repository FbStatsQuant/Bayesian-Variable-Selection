# L6 — Proposition SHARP: the exponent 1/6 is optimal for the full-lattice route (exact-Gram compound symmetry)

Status: **PROVED (by this seat, unchecked)** — v1.1, 2026-11-09; lemma check R04 (Sol high): VERIFIED-WITH-AMENDMENTS
(applied). Scope note (R04): the proof does not use p ≤ K (the witness has size O(log p) < K), a strengthening of the
locked Part II. Falsification: numerics/fna_check.py → FNA_summary.md (the n = 10¹² rows use a normal approximation of the
χ²_{n−1−p} variate and are therefore approximate draws; R06 item 13)
(one-sided NA failures grow with n at log p/log n = 0.30; none at ≤ 0.14 for n ≥ 1e9).

**Setting.** Model G with exact Gram XᵀX = (n − 1)Σ, Σ = (1 − a)I + a11ᵀ, fixed a ∈ (0, 1) (so p ≤ n − 1); fixed s₀ ≥ 1,
fixed nonzero θ*_{S₀}, fixed σ² > 0; 𝓛 = [S₀, [p]] and NA(𝓛) as in STATEMENT §1.

**Proposition SHARP.** If liminf_n log p_n/log n > 1/6, then P(NA(𝓛)) → 0. (Nothing is claimed at equality.)
This is a statement about the full-lattice route (the event NA(𝓛) used by GROW-type descent), not about the method.

*Witness.* N := [p] ∖ S₀, |N| = p − s₀. Represent g := Xᵀε/(σ√(n − 1)) ~ N(0, Σ) as g = √a·1·ξ₀ + ζ, ζ = √(1−a)·η,
(ξ₀, η) iid N(0, 1) (L1 U(a) with singleton groups, λ = √a 1, Ψ = (1 − a)I; enlarged space as in L1 Corollary U —
the event below is an original-space event). Let m := ⌈log p⌉, E := the m elements of N with the largest η,
T := S₀ ∪ E (|T| = k := s₀ + m), and l := argmin_{j∈N} η_j (l ∉ E for p large).

**Step 1 (the add statistic of the witness).** By L1 (1.1) with U = ∅, ψ = 1 − a, λ̃ = √a, s_T = ak/(1 − a), and with
c := (1 − a)/a, a direct computation gives
  Z_{T,l} = [η_l − H_T/(k + c) + ξ₀√c/(k + c)] / √(1 + 1/(k + c)),   H_T := Σ_{j∈T}η_j.
(Indeed √(1−a)Ξ_l = √(1−a)η_l, (λ̃/√(1+s_T))W_T = √a(ξ₀ − √(a/(1−a))H_T)/(1 + s_T), and a/((1 − a)(1 + s_T)) =
1/(k + c); divide numerator and denominator by √(1 − a).)
Gaussian order statistics for N' := p − s₀ iid N(0,1) (standard; elementary proofs: P(min > −t) ≤ exp(−N'Φ̄(t)) and
P(m-th largest < t) = P(Bin(N', Φ̄(t)) < m), with Mills' ratio): with probability → 1,
  min_N η ≤ −√(2 log N' − 3 log log N'),  and  Σ_{j∈E}η_j ≥ m √(2 log(N'/m) − 3 log log(N'/m)),
using m = ⌈log p⌉ → ∞ and N'Φ̄(t) ≫ m at the chosen thresholds. Also |Σ_{S₀}η_j| + |ξ₀| ≤ log log p w.p. → 1.
Hence, since m/(m + s₀ + c) → 1 and log(N'/m) = log p − O(log log p),
  |Z_{T,l}| ≥ (1 − o(1))[√(2 log p) + √(2 log p)] = (2 − o(1))√(2 log p),  i.e. Z²_{T,l} ≥ (8 − o(1)) log p,
with probability → 1 (p → ∞ under the hypothesis).

**Step 2 (score comparison, small-model argument; p may be comparable to n).** (R04 item 5) Only the deterministic
identities (E1), (E2) of L3 are reused, by their algebraic proofs on the particular sets T, A (they need only the Gram
floor λ_min(G_A) ≥ (n − 1)(1 − a), not (P), K = p or L3's RSS lower bound). Work on the intersection of the witness
event of Step 1, the event s_Y² ≤ s̄² of L3's E_Y, and the additional Laurent–Massart event
‖Cε‖²/σ² ≤ n − 1 + 2√((n − 1) log n) + 2 log n (complement ≤ 1/n). Let A := T ∪ {l}; |A| = k + 1 = O(log p)
≤ K. Since T ⊇ S₀, RSS_T − RSS_A = σ²Z²_{T,l}/s_Y² (L3 notation, y = Y/s_Y). By L3 (E1) with φ² = 1 − a,
−2(ρ_A − ρ_T) ≥ 2ρ_T ≥ −k/((n − 1)(1 − a)) = o(1); by (E2), ω ∈ [0, 2]. With log(u/v) ≥ (u − v)/u:
  2ν log((0.02 + Q_T)/(0.02 + Q_A)) ≥ (n + 0.02)(Q_T − Q_A)/(0.02 + Q_T) ≥ (n + 0.02)(σ²Z²/s_Y² − 2)/(‖Cε‖²/s_Y² + 2.02),
because Q_T ≤ RSS_T + 2 ≤ ‖Cε‖²/s_Y² + 2. On these events (the numerator σ²Z²/s_Y² − 2 is eventually positive since Z² → ∞ and s_Y² ≤ s̄², which
justifies replacing the denominator by its upper bound), the right side is ≥ Z²(1 − o(1)) − C₀ with C₀ := 2s̄²/σ² + 1. The prior
term is 2 log((k + 1)/(2p − 1 − k)) ≥ −2 log p − 2 log 2. Hence, by (E1) for the determinant part,
  2[F(A) − F(T)] ≥ −2 log p − log(n + 1) + Z²_{T,l}(1 − o(1)) − C₀ − 2 log 2 − o(1)
               ≥ (6 − o(1)) log p − log(n + 1) − C₀ − 2,
with probability → 1. If liminf log p/log n > 1/6, pick ε > 0 with 6 log p ≥ (1 + 2ε) log n eventually; since p ≤ n − 1, o(log p) =
o(log n), so the right side is ≥ (1 + 2ε) log n − o(log n) − log(n + 1) − O(1) ≥ ε log n − O(1) > 0 for n ≥ n₀. So F(T ∪ {l}) > F(T) with T ∈ 𝓛, |T| < K: NA(𝓛) fails. ∎

**Remarks.** (1) The witness depends on the noise; this is legitimate because NA(𝓛) quantifies over every T ∈ 𝓛.
(2) The upper bound of L3 (Part I) and this lower bound match: in the worst case s = 1 of the α₀ computation the
factor term contributes κ̄√(2 log p) with κ̄ = 1. (3) The proposition says nothing about whether the method (or even
LS0) finds S₀ above 1/6; numerics D2/D3 show LS0 paths that are pure deletions there (Part III).
