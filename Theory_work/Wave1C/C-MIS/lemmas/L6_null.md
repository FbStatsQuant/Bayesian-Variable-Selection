# L6 — Lemma Z: the null projection (s₀^𝒞 = 0), bounded candidate set

Status: Lemma Z — added after the mid-point review (R04 finding 9); R05 VERIFIED-WITH-AMENDMENTS (applied). Council pending.
Self-contained; uses only [P3] lem:red, lem:smoother(b), lem:det (proof), lem:prior(b), lem:chi(a) and eq:score.

**Setting.** Contrast coordinates (L4.0). y_c = r + e with e ~ N_N(0, σ_*²I), σ_*² > 0 fixed, and r ∈ ℝ^N deterministic
with X_{c,𝒞}ᵀr = 0 (r = 0 allowed). Two instances:
(GR) fixed candidate design, GR with β^𝒞 = 0: by Lemma R (L1.1), y_c = Uᵀε′ ~ N_N(0, σ_𝒞²I): r = 0, σ_*² = σ_𝒞²;
(EP) fixed design, EP with θ^𝒞 = 0 (the full mean is orthogonal to every candidate): r = μ_c, σ_*² = σ².
**Hypotheses.** p_𝒞 ≤ P̄ (bounded), and λ_min(X_𝒞ᵀX_𝒞) ≥ g₀ > 0 for all large n (so p_𝒞 ≤ N and X_{c,𝒞} has full
column rank).
**Lemma Z.** 1 − π_𝒞(∅ | y) = O_P(n^{−1/2}); hence every PIP_j ≤ 1 − π_𝒞(∅ | y) → 0, MPM_𝒞 = ∅ and S†_𝒞 = ∅ with
probability → 1, and in the setting of Corollary H the reported HPM bound holds with T = ∅.

*Proof.* ∅ ∈ Ω_𝒞 always. For S ⊆ 𝒞, S ≠ ∅, |S| = k ≤ K, by [P3] eq:score (D_∅ = 1, t_∅ = 0) and eq:ratio,
  π_𝒞(S | y)/π_𝒞(∅ | y) = [w(k)/w(0)]·D_S^{−1/2}·(1 + t_S/(2b + Q^c_S))^ν.
*Determinant.* D_S = ∏_i f(λ_i(G_S)) with f(λ) = ((n+1)λ + 1)/(λ + 1) increasing ([P3] lem:det proof); λ_min(G_S) ≥
λ_min(G_𝒞) ≥ g₀ (interlacing), so D_S ≥ f(g₀)^k ≥ [(n + 1)(1 + 1/g₀)⁻¹]^k.
*Exponent, uniformly in S.* t_S ≤ (n/(n+1))‖P_Sy_c‖² ([P3] lem:smoother(b)) and P_Sr = 0 (r ⊥ col X_{c,S}), so
t_S ≤ ‖P_Se‖² ≤ ‖P_𝒞e‖² =: σ_*²U_n, U_n ~ χ²_{p_𝒞}. Also 2b + Q^c_S ≥ Q^c_S ≥ ‖(I − P_S)y_c‖² ([P3] lem:smoother(b))
= ‖r‖² + 2rᵀe + ‖(I − P_S)e‖² (as (I − P_S)r = r and rᵀP_Se = 0) ≥ ‖r‖² + 2rᵀe + ‖(I − P_𝒞)e‖². With
Z := rᵀe/(σ_*‖r‖) ~ N(0, 1) if r ≠ 0, and then ‖r‖² + 2rᵀe = (‖r‖ + σ_*Z)² − σ_*²Z² ≥ −σ_*²Z²; if r = 0 put Z := 0, and
the bound reads 0 ≥ 0.
Let V_n := ‖(I − P_𝒞)e‖²/σ_*² ~ χ²_{N−p_𝒞}. Then on {V_n − Z² > 0},
  ν log(1 + t_S/(2b + Q^c_S)) ≤ ν t_S/(2b + Q^c_S) ≤ (n/2 + 0.01)U_n/(V_n − Z²) =: Λ_n, for every S ≠ ∅
(define Λ_n := 0 on {V_n − Z² ≤ 0}; all bounds below are asserted only on {V_n − Z² > 0}).
Λ_n = O_P(1): U_n ~ χ²_{p_𝒞} with p_𝒞 ≤ P̄ is tight; Z² is tight; V_n/N → 1 in probability ([P3] lem:chi(a), or
Chebyshev, as N − p_𝒞 → ∞); so (n/2)/(V_n − Z²) → ½ in probability.
*Prior.* By [P3] lem:prior(b) with s₀ = 0: C(p_𝒞, k)w(k)/w(0) ≤ 2·2^{−k} (the bound holds for k ≤ p_𝒞).
*Sum.* On {V_n − Z² > 0}, with a_n := [(1 + 1/g₀)/(n + 1)]^{1/2} ≤ 1/2 for large n,
  1 − π_𝒞(∅ | y) ≤ Σ_{S≠∅} π_𝒞(S | y)/π_𝒞(∅ | y) ≤ e^{Λ_n} Σ_{k≥1} 2·2^{−k}a_n^k ≤ 2e^{Λ_n}a_n.
Since a_n = O(n^{−1/2}), Λ_n = O_P(1) and P(V_n − Z² ≤ 0) → 0, 1 − π_𝒞(∅ | y) = O_P(n^{−1/2}). The PIP/MPM/S† consequences
are the deterministic arguments of [P3] (ii)–(iii) with S₀ = ∅. ∎

**Remarks.** (1) The rate n^{−1/2} (no log factor) reflects bounded p_𝒞. (2) For growing p_𝒞 the uniform bound
‖P_Se‖² ≤ ‖P_𝒞e‖² is too crude (χ²_{p_𝒞}/2 in the exponent); the growing-p null case would need the T03 superset machinery with
s₀ = 0, which the TH09 card (s₀ ≥ 1) does not authorise importing; not claimed. (3) Numerics N6 (null projection) and
N7 (Example E1) in numerics/SUMMARY.md.
