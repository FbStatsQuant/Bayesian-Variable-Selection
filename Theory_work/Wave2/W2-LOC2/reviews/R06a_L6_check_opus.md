VERIFIED-WITH-AMENDMENTS

# R06a — Cross-family line-by-line check of `lemmas/L6_poly.md` (Claude Opus 5.5; author Codex)

Scope: L6_poly.md as it stands on disk (it already carries the R06b-1 amendment to (P13)), against STATEMENT (D3) v1.2 and
the cited sources: GROW L6 §§0–7, L0, L2, L3; GEN L1; APP L2_CT, L3_LOC; LOC2 L1, L2 (NA-R), L3_CTd, L4 A.5, L5. All
results are asymptotic. I raise no finite-n issues.

**Bottom line.** I found no FATAL or MAJOR defect. Each step the brief names holds as written: BC, IR, (P5)–(P19), and the
cutoff α₀ = 17/2. The findings below are MINOR/NIT presentation and citation fixes. None changes a rate or the cutoff.

## Findings

1. **MINOR — IR: the Combes–Thomas reuse needs two steps it does not state, and the citation points to the wrong step.**
   `L6:135–145` cites `APP/lemmas/L2_CT.md:19`. That line is the conjugation step (ii). The argument actually used is the
   Schur test plus Neumann bound, steps (iii)–(iv) at L2_CT.md:22–28. Lemma CT itself is stated for exponential decay, so
   only its algebra carries over. Two facts are used but not written:
   (a) entries of E = DA_BD⁻¹ − A_B are (A_B)_ik(e^{t(d(i,j)−d(k,j))} − 1). The bound uses |e^s − 1| ≤ e^{|s|} − 1 and
   |d(i,j) − d(k,j)| ≤ d(i,k) ≤ B (triangle inequality on the line).
   (b) the weight is column-specific, D_ii = e^{t d(i,j)}. So (DA_B⁻¹D⁻¹)_ij = e^{t d(i,j)}(A_B⁻¹)_ij, because d(j,j) = 0.
   With λ_min(A_B) ≥ c/2 and ‖E‖₂ ≤ √(‖E‖₁‖E‖_∞) ≤ c/4, we get ‖A_B⁻¹E‖ ≤ ½ and ‖(DA_BD⁻¹)⁻¹‖ ≤ 4/c. This is the stated
   4/c, so the result is correct.
   *Fix:* cite L2_CT.md:22–28 ("algebraic part only"), and add (a) and (b) in one sentence each.

2. **MINOR — inconsistent description of D.** §0 (`L6:48–49`) says D has a "required property" that §3 specifies. §3
   (`L6:206–211`) says "choose D sufficiently large" and then "take D ≥ 1". In fact any fixed D > 0 works: (P5) holds with
   H = K₁₅ D^{−α}, since (1 + d_n)^{−α} ≤ D^{−α} n^{−1/2}. Nothing downstream needs D to be large: the spherical tail
   needs ‖m‖ = O(1), and q = O(n^b) holds for any D.
   *Fix:* "D is any fixed positive constant (e.g. D = 1); (P5) holds with H depending on D."

3. **MINOR — the R06b-1 amendment is correct, but one sentence should be added to the rate audit.**
   (P13) is now max(2λ, ½) < τ < 1 − 2b, with existence from λ + b < ½ and b < ¼. I re-derived it:
   - t = 2 log p + τ log n − w_n ≥ (½ + δ) log n eventually, which meets the (P10) lower limit.
   - The upper limit t ≤ (2A + 1) log n already lies inside the source's range (2A + 3) log n (GROW L6:225). So the remark
     about "any fixed B_A" (`L6:286–288`) is harmless but not needed.
   - The explicit choice τ = (2λ + 1 − 1/α)/2 equals ¾ + 9/(8α) > ½, so it still satisfies the new (P13).
   *Fix:* in the §7 rate audit (`L6:451–457`), add that τ > ½ costs nothing for α > 2.
   *Formatting:* `L6:326` is one overlong merged line; re-wrap it.

4. **NIT — overloaded symbols.**
   - B is the bandwidth in IR, but "Apply (P2) to B = Σ_{T∪{l}}" (`L6:155`) and BC's B are matrices.
   - D is the radius constant (§0), the diagonal weight (§2), and E[W_l|W_T] − E[W_l|W_T'] (§6, `L6:367`).
   - H is both a generic constant and the 2×2 matrix in BC (`L6:99–101`).
   - λ is the exponent 15ρ and also λ_vector.
   - t_n is the toolkit threshold (§3) and t_n(k) the ladder threshold (§5).
   - τ is the deletion exponent here but τ² is an innovation variance in the cited sources.
   *Fix:* rename locally, e.g. bandwidth β_n; Δ_{T,l} for the §6 difference; λ_* for 15ρ.

5. **NIT — (P8) last line.** Spell out the expansion. With Δ := √((1 − a′R⁻¹a)(1 − b′R⁻¹b)) = 1 − O(v_n²) ≥ ½,
   z_U − z₀ = [−a′R⁻¹b + z₀(1 − Δ)]/Δ. This gives |z_U − z₀| ≤ H(v_n² + |z₀|v_n²) = O(v_n²), using |z₀| ≤ 1.

6. **NIT — weak falsification numerics.** `numerics/poly_check.py` uses p = 8 and |Σ_ij| ≤ 0.2(1+d)^{−α}, which is nearly
   diagonal. That makes its BC/IR checks weak. Its "recursive algebra" lines show actual/envelope ratios of 1.5–2.0 under
   a 4× allowance; this is an O-constant check only, and the file already disclaims it as proof. My stronger check
   (`reviews/R06a_scratch/check.py`) used p = 600 and Σ_ij = 0.4·2^α(1+d)^{−α} (first off-diagonal 0.4, spectrum ≥ 0.22).
   It also used adversarial |U| = 15 sets: an equispaced chain between j and k, clusters next to j and k, and random
   nearby sets. It found no counterexample:
   - (1+d)^α · max|Cov(W_j,W_k|W_U)| converges to the marginal constant (155.2 at α = 8.6, 3.20 at α = 3). The large
     ratio at d = 10 for α = 8.6 is pre-asymptotic chain products. That is consistent with BC's (m−1)! K₀^{m−1} (m−1)^α
     constant.
   - The full inverse decays with log-log slope ≈ −α (−2.47, −2.95, −4.93 for α = 2.5, 3, 5), which is stronger than IR's
     α − 1. IR is therefore conservative but valid. Optional remark: Jaffard's inverse-closedness would give exponent α
     for α > 1. It is not needed, because IR is not binding anywhere (it enters only NA, where α > 2 suffices).

## Step ledger (all checked; no other defect found)

- **Lemma BC (`L6:74–105`).** A cofactor monomial for (B⁻¹)_ij is a bijection rows∖{j} → cols∖{i}. The walk from i (in-degree
  0) must end at j (out-degree 0) without revisiting, so every monomial contains an i→j path of length h ≤ m−1. Its
  longest edge has distance ≥ d/h, and (1 + d/h)^{−α} ≤ h^α(1+d)^{−α}. The other factors are ≤ K₀, there are (m−1)!
  monomials, and det B ≥ c^m. This gives (P1).
  For the 2×2 step: H is a principal submatrix of B⁻¹, whose spectrum is in [1/C, 1/c]. So det H ≥ C^{−2} and
  |S_jk| = |H_jk|/det H ≤ C²|H_jk|. Correct.
  With Y: Cov(W_v, Y | W_{U0}) = Σ_{j∈S0∖U0} (θ_j/t_j) Cov(W_v, W_j | W_{U0}), with |U0| ≤ 15 (m ≤ 17), and the denominators
  are bounded below by c and σ². With truths: the spherical tail needs only Cov(W_l, W_j | W_{U0}) for |U0| ≤ 15, which is
  (P5). Correct. M = 15 suffices everywhere it is used.
- **Lemma IR (`L6:114–160`).**
  - Truncation: ‖A − A_B‖ ≤ 2K Σ_{d>B}(1+d)^{−α} = O(B^{1−α}). This needs α > 1 and at most two positions per distance,
    which holds for any subset of positions.
  - CT: the row/column sums are ≤ 2K(k/B)e^k Σ d(1+d)^{−α}. The series is finite for α > 2, and a small k gives ≤ c/4
    uniformly in B.
  - Resolvent: ‖A⁻¹ − A_B⁻¹‖ ≤ (2/c²)H₁B^{1−α}.
  - With B = ⌊d/(M₁ log(2+d))⌋: e^{−kd/B} ≤ (2+d)^{−kM₁}, and B^{1−α} ≍ d^{1−α}(log d)^{α−1} = f(d).
  - Σ f(d) < ∞ iff α > 2. β_v = −Ψ_vl/Ψ_ll with Ψ_ll ≥ 1. L₀ and F(r) are as stated.
- **(P5)–(P9).**
  - (P7): |I_l| ≤ 16|H_l|^{15} = O(n^{15ρ}).
  - (P8): V avoids H_l ⊇ S₀ ∪ {l}'s R_n-neighbourhood, so the population a and b are O(R_n^{−α}); the sample errors are
    O(ħ_n); |z₀| = O(√(log n/n)) by (P5); ‖R⁻¹‖ is bounded by the conditional floor.
  - (P9): n|z_U² − z₀²| ≤ n(2|z₀||Δz| + Δz²) = O(√(n log n) n^{−2αρ} + n^{1−4αρ} + polylog/√n) → 0 iff αρ > ¼. Also
    h_{U,l} ≤ 2n z₀² + 2nΔz² = O(log n), as (6.10) requires.
- **(P10).** ‖α_vec‖ = O(n^{−1/2}), so ‖m‖ ≤ 2√n·s₀·max|α_j|(1 + ‖b_j‖₁) = O(1). The GROW (6.9)/(6.5) calculation and the
  CN_D device need nothing more.
- **(P11).** For the ladder: p·|I_l|·e^{−(t_n(k) − w_n)/2 + O(√log n)} = k·n^{−1/2+λ+o(1)}, and t_n(k) ≥ log n − C₀.
- **(P12).** (6.11) and per-block optimality give, for k > 2k₀, a far-null add with h ≥ log(n+1) + 2 log(p/k) − 4κ_E − o(1).
  Markov over O(log n) ladder points gives O(log n)·n^{−1/2+λ+o(1)} → 0 iff λ < ½.
- **Truth inclusion.** The feasibility dichotomy holds: k ≤ 2k₀ < K_n, or Q = [p] with K_n = p.
- **(P14).** The union over p·n^λ references at t = 2 log p + τ log n gives n^{λ−τ/2+o(1)} → 0 iff τ > 2λ.
- **(P15).** The deletion gain is log((2p−k)/k) + ½log(n+1) − ½h − 2κ_E − o(1) ≥ [(1−τ)/2 − b] log n − O(1). This uses
  log k ≤ log(2k₀) ≤ b log n + O(1), and it is positive iff τ < 1 − 2b.
- **Cutoff.** Feasible ρ requires 1/(4α) < ρ and 15ρ < ½ − 1/(2α), i.e. 17/(4α) < ½, i.e. α > 17/2. The explicit ρ, λ and τ
  satisfy every constraint, including the amended τ > ½. α₀ = 17/2 is the exact infimum for this argument; at equality
  there is no fixed slack. This is correctly presented as argument-specific.
- **§3 toolkit.**
  - The family has log|𝔉|, log|𝒱𝒱| = O(q + log n). 𝒟₂ and 𝒟₃ fail with probability ≤ n^{−2} and 2/n (2^{J/2}e^{−J} ≤ 1).
  - RSS floor: h² + t = o(n).
  - The GEN L1.3 remainder needs J_n/n → 0, so κ_E is the same.
  - (P4): ω_n log n = O((q + log n) log n/n) → 0.
  - Sample floors: J_n ħ_n = O(n^{b−1/2}√log n) → 0.
  - TL (GROW L2.1) needs only h² + t = o(n) and a signal ≍ n.
- **§6 NA re-run.**
  - Tower identity: λ on T′ is −Σ_w β_w γ_w; ‖λ‖₁ ≤ (1 + L₀) Σ_{d(w,l)>r_n} |β_w| ≤ (1 + L₀)F(r_n) → 0 (α > 2).
  - (P17): Var(D) ≤ ‖λ‖₁², with e ⊥ span W_T.
  - Frames: log N_n ≤ log p + 2r_n log 2.
  - E_a and E_b: unions with x, v_n = O(q + log n) keep 3n^{−2} and n^{−2}. E_c is unchanged (2^{q/2}e^{−q−log n} ≤ 1/n).
  - E_e: the explicit y_n² = 2 log(2(q+1)) + 2 log log n fails with probability ≤ 1/log n, and L_n² y_n² = o(log n).
  - (P18): ε_n = O((q + log n)/√n) → 0 (b < ½), and ω′_n ζ_n² = O(q log n/n) → 0.
  - (P19): log(q+1) ≤ b log n + O(1).
  - GROW L2.2: x ≤ c_n/(n(1 − ω_n)) ≤ ¼, and its excess is O(log n)(ω_n + log n/n) → 0.
- **"Unchanged/verbatim" claims.** I compared each against its source line: GROW L6:85, 115, 143, 157, 180, 203, 245, 262,
  291, 316, 329–361, 366; L0:33; L2:12, 27, 41; L3:30; GEN L1:3, 33, 74; LOC2 L2:61, 71, 78, 87, 95; L3_CTd:73; L4:51;
  L5:7, 26, 30; APP L3_LOC:28, 63; L2_CT:55. Each is accurate. The only exception is the L2_CT:19 pointer (Finding 1).
  No input status is upgraded.

## Disposition request

Apply findings 1–3; findings 4–6 are optional. No re-check is needed after these edits, because none touches a rate or
inequality.
