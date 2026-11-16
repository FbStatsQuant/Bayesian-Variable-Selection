# W3-DIST — PRIOR PROBE (P5) — REPORT

Helper: Claude Opus 5.5 (Claude Third), effort high, 2026-11-15. Brief: `../../briefs/BRIEF_prior_probe.md`.
Labels: every claim is **DERIVED (unchecked)**, **REFUTED** or **OPEN**. Nothing here is checked by a second reader.
Numerics: `probe_checks.py` → `probe_checks_out.txt` (19 s, local). Those are falsification checks, not proofs.

**Notation.** As in `W3-POST/STATEMENT.md` §0 and `W3-POST2/STATEMENT.md` (contrast coordinates N = n−1, y_c = μ_c + e,
e ~ N_N(0, σ*²I), M_S = nX_SH_S⁻¹X_Sᵀ, Q_S = y_cᵀ(I − M_S)y_c, b = b₀s_y²). **Notation clash in the brief:** M is used both
for the energy bound ‖μ‖² ≤ nM and for the rate multiplier in n^{−cM}. Below, M and M′ are the energy and coefficient bounds,
and **u** is the rate multiplier (ε_n² = u log n / n, level n^{−cu} = e^{−c nε_n²}). ρ′ := θ*ᵀ(G_{S₀}+I)θ*/n = (‖μ‖² + ‖θ*‖²)/n ≤ M + M′.

## 1. Song–Liang (8)–(14) for the coded prior (Q1)

Mapping: SL's (6) is iid Bernoulli(λ_n = r_n/P_n) with cap r̄_n. The coded BB(1,p) is a **mixture** of (6) over
λ ~ Beta(1,p): ϖ(S) ∝ ½/C(2p−1,|S|) (checked: B(k+1, 2p−k)/B(1,p) = ½/C(2p−1,k)). There is no single r_n. Given λ, the
prior is (6) with r_n = pλ, and pλ ⇒ Exp(1), so r_n = O_P(1). E|S| = p/(p+1) < 1. Coded cap r̄_n = K = min(p, ⌊n/2⌋).
Coded slab: V_S = n(G_S + I)⁻¹, i.e. SL's own "ridge prior" V⁻¹ = Σ̂_S + c_nI with c_n ≍ 1/n, built from the **empirical** Gram.
Rates: (A) ε² = u log n/n, (B) ε² = u log² n/n, both with p = n^A.

| SL condition | coded counterpart | verdict | reason (computation in Appendix A1) |
|---|---|---|---|
| (8) Δ(r_n) ≺ ε_n | strict sparsity, fixed s₀ | **n.a. / holds in substance** (DERIVED) | Δ(r) = 0 iff r ≥ s₀. Its role (prior mass near the truth) is met directly: ϖ(S₀) ≥ ½(2p)^{−s₀}, so −log ϖ(S₀) ≤ s₀(A log n + log 2) + log 2 ≺ nε² in (A) once u > u₀(s₀, A), and in (B). |
| (9) r̄ ln(1/ε²) ≺ nε² | r̄ = K | **fails** (DERIVED) | For p ≥ n/2: K ln(1/ε²) ≍ (n/2) log n ≫ u log n (A) and ≫ u log² n (B). It holds only if p ≺ nε²/log n. |
| (10) r̄ ln P ≺ nε² | r̄ = K | **fails** (DERIVED) | K·A log n ≍ n log n. (10) would need a cap K ≺ u/A in (A) (bounded) and K ≺ u log n/A in (B). |
| (11) r̄ ln(nε²B̃) ≺ nε² | B̃ = sup_{\|S\|≤K} n/(λ_min(G_S)+1) | **B̃ part benign; (11) fails** (lead's reading partly REFUTED) | 1 ≤ B̃ ≤ n for every design, by the +I (B̃ = n exactly as soon as some \|S\| ≤ K is rank-deficient; check C2). So ln(nε²B̃) ≤ ln(u n log² n) ≍ 2 log n. But (11) carries the factor r̄ = K, so it fails like (10). With a sieve dimension m in place of r̄, it reads m·2 log n ≲ nε², the same form as (10). |
| (12) 1 ≤ r_n ≤ r̄ < P | mixture; K = p if p ≤ n/2 | **nominally fails; technical** (DERIVED) | E\|S\| < 1, and r̄ = P when p ≤ n/2 (the cap is then inactive). Neither matters for the substance. |
| (13) r_n ≺ P | Eλ = 1/(p+1) | **holds in the mixture sense** (DERIVED) | pλ = O_P(1). |
| (14) B(r_n) ≺ nε² | B(r) = sup_{\|S\|=r}(λ_max(G_S)+1)/n | **holds, design-free** (DERIVED; lead confirmed) | 1 ≤ B(r) ≤ (r(n−1)+1)/n < r + 1 by standardisation. Bounded r_n gives B = O(1) ≺ nε². |
| Thm 2: r_n ≻ 1 | prior mean size p/(p+1) | **fails** (DERIVED; lead confirmed) | Its only use is to make (8) automatic (r_n > \|t\|). A proof device. |
| Thm 1 \|x\| ≤ 1 / Cond. 1 | population law of x | design assumption, not prior | Substantive for the exponential form (it links KL/Hellinger to β). |

**Proof devices vs substance (DERIVED).** Substance: (a) the prior mass of a KL-neighbourhood of f* is ≥ e^{−Cnε²}. This
holds for the coded prior: the support term −log ϖ(S₀) = O(log n), and the slab density at θ* costs ≤ ρ′/(2σ²) +
(s₀/2) log(Cn/ε²)). (b) Condition 1 or boundedness, to compare KL with Hellinger. Proof devices: the hard cap as a sieve
with zero complement mass, and the entropy conditions (9)–(11) for that sieve. (12), (13) and r_n ≻ 1 serve only the iid-Bernoulli
prior-mass computation. In short: **the conditions fail only through the cap/sieve.** That failure is not cosmetic (§2).

## 2. Testing/sieve route with the coded prior (Q2)

**Exact size law (DERIVED; check C1).** q_k := P(|S| = k) = ½C(p,k)/C(2p−1,k) = ½∏_{i<k}(p−i)/(2p−1−i).
- Successive ratio: q_k/q_{k−1} = (p−k+1)/(2p−k). This is p/(2p−1) at k = 1, exactly ½ at k = 2, and < ½ for k ≥ 3.
- Bounds: q_k ≤ 2^{−k}p/(2p−1), and q_k → 2^{−k−1} for fixed k (the lead's reading is confirmed).
- Tail (uncapped, m+1 ≤ min(K, √(p/2))): 2^{−m−3} ≤ P(|S| > m) ≤ 2^{−m}p/(2p−1). The capped prior changes this only by
  the factor 1/W_K with W_K ∈ [¾, 1].
- Check C1 at p = 10⁴: q₁₀/2^{−11} = 0.998 and P(|S| > 10) = 4.87·10⁻⁴.

**Verdict: incompatible when log p → ∞ (DERIVED; lead confirmed, made precise).** Let the GGV/Jiang theorem with sieve
F_n = {|S| ≤ m} (coefficients and σ in bounded ranges) have prior-mass constant C (Π(B_KL(ε)) ≥ e^{−Cnε²}; here C ≥ s₀A·log n/(nε²)).
1. It requires Π(F_nᶜ) ≤ e^{−(C+4)nε²}. By the lower tail bound, m ≥ (C+4)nε²/log 2 − 3.
2. It requires log N(ε, F_n, d) ≤ c₁nε². When Σ has bounded sparse eigenvalues on size-m supports, Gilbert–Varshamov
   packing of m-sparse vectors at Hellinger scale ε gives log N ≥ c₂ m log(p/m), plus m log(1/ε) from the radial part.
3. Together: log(p/m) ≤ c₁ log 2/(c₂(C+4)) + o(1), which is impossible once p/m → ∞. The same holds for the
   sieve-free form (Π(F_nᶜ)/Π(B_KL) ≤ e^{−(C+4)nε²}) and for slice-sum forms Σ_j √(N_j Π(F_j)) with N_j ≈ p^{cj}, Π(F_j) ≈ 2^{−j}.

**What fails, precisely.** The prior size tail is p-free (geometric, ratio ½), while the sieve entropy costs log p per
dimension. In the complexity-prior condition A₁p^{−A₃}π(s−1) ≤ π(s) ≤ A₂p^{−A₄}π(s−1) (Castillo–Schmidt-Hieber–van der Vaart
2015, eq. (2.2), cited from memory, PDF not in repo), BB(1,p) has π(s)/π(s−1) = (p−s+1)/(2p−s) → ½. So it satisfies the
condition only with A₄ = 0: it is the u = 1 boundary of their Beta(1, p^u), u > 1 example (the lead's "κ = 1" parametrisation
is not checked).

**Root cause (DERIVED).** Any argument that bounds the posterior numerator by its expectation sees only prior masses:
E₀[∫_{F_nᶜ} (likelihood ratio) dΠ] = Π(F_nᶜ). This is exactly why L1a′ is geometric. Only arguments that use the
likelihood's Occam factor (D_S^{−1/2}, conjugacy) can beat 2^{−m}. That is the §3 route.

**Formal framework (Q2b).** Yes, the coded posterior is formally outside the iid GGV/Jiang framework (DERIVED). The proofs
rely on a data-free prior through Fubini, E₀∫∏(f/f*)dΠ = 1. The coded prior depends on the data in three ways:
- (i) **on X**: through the slab V_S = n(G_S+I)⁻¹ and through standardisation (raw β = s_yD_x⁻¹θ);
- (ii) **on y**: through the IG rate b₀s_y² on the response scale;
- (iii) **centring**: the flat intercept and the centring make the working likelihood an (n−1)-dimensional contrast
  model with non-iid rows (X = CX^rD_x⁻¹ depends on all rows).

Remedies:
- (ii) Sandwich the IG rate between data-free rates b± on 𝓑_n at cost κ² ([P1] `lem` at line 214, thm:Ta). P(𝓑_nᶜ) is
  only ≤ C/n by Chebyshev in [P1], but Gaussian concentration of s_y² gives e^{−c(M,σ*²)n} (A3).
- (i) Condition on X. That makes the problem INID with a y-free prior (Ghosal–van der Vaart 2007, non-iid) and yields an
  **in-sample** Hellinger. Getting SL's integrated (x,y) Hellinger then needs a sample-to-population Gram transfer on
  sparse supports, which uses sparse eigenvalue bounds on Σ. SL's own route needs none, because their V_ξ is data-free;
  their remark "expectation replaced by its sample estimator" is not covered by their proof.

## 3. The direct conjugate route (Q3)

**Lemma V (variational split + MGF; NEW; DERIVED (unchecked); algebra checked numerically, C3).** Let S ⊇ S₀,
η > 0, c = 1+η, and M^{(c)}_T := X_T(G_T + c(G_T+I)/n)⁻¹X_Tᵀ. Then:
- (a) Q_{S₀}(μ_c+e) − Q_S(μ_c+e) ≤ eᵀD′e + (1 + 2/η)ρ′, with D′ := M_S^{(1/c)} − M_{S₀}^{(c)} ⪰ 0 and ‖D′‖ < 1.
- (b) For e ~ N(0, σ*²I): E[(D_{S₀}/D_S)^{1/2} exp(eᵀD′e/(2σ*²))] ≤ (1+η)^{s₀+|J|/2}.
- (c) D′ ⪯ (P_S − P_{S₀}) + R₀, where R₀ ⪯ P_{S₀}. Hence eᵀD′e ≤ σ*²χ²_J + ‖P_{S₀}e‖², with χ²_J ~ χ²_{d_J}.

Proof in A2. **Neither (F₀) nor any floor is used. The coefficient bound enters only through ρ′.**

**Variance step (c) of the brief: no failure (DERIVED).** ((2b+Q₀)/(2b+Q_S))^ν ≤ exp(νΔ/Q_S). Since μ_c ∈ col X_S,
Q_S ≥ ‖(I−P_S)e‖² ≥ ‖e‖² − ‖P_Se‖². On the event E_u (A3) the right side is ≥ σ*²(N − 2√(2cuN log n) − (C_A|S| + 2cu) log n).
So νΔ/Q_S ≤ (1+ε_n)Δ/(2σ*²), with ε_n = O(√(u log n/n) + (|S|+u) log n/n). The surplus ε_n·eᵀD′e ≤ ε_n‖P_Se‖² = o(1)(|S|+u)
is deterministic on E_u. Only a lower bound on ‖(I−P_S)e‖² is needed, not two-sided concentration of ‖e‖².
The b > 0 term only helps.

**Theorem P (exponential size tail; DERIVED (unchecked)).** Assume G, ‖μ‖² ≤ nM, ‖θ*‖² ≤ nM′, s₀ fixed, p ≤ n^A, and
**(ADG; c_D) on the extended range 1 ≤ |J| ≤ m_u**, where m_u − s₀ := ⌈[(3cu + (A+½)s₀ + ½) log n + C₀√(u log n)]/log 2⌉ + C₀s₀
(m_u = O((u+s₀) log n): the upgraded L1a′ cutoff of A3). Then there are c > 0 and C, u₀, n₀(u) (depending on s₀, A, σ*², M,
M′, c_D) with
  **P( π(|S| > s₀ + C u) > n^{−cu} ) ≤ n^{−cu}** for u ≥ u₀ and n ≥ n₀(u).
Here C ≤ 6c + O(s₀(A + C_A))/u₀. Under (F₀), C ≤ 4c + O(s₀A)/u₀. (DG) ⇒ (ADG), so (DG) on that range suffices.
Proof sketch, every inequality in A3:
- **(i) |S| > m_u:** upgraded L1a′. Markov on Θ^{(1)}; the Laurent–Massart tail of Λ′_n gives e^{Λ′} ≤ e^{C√(u log n)} =
  n^{o(1)}; P(𝓑_nᶜ) ≤ e^{−cn}.
- **(ii) Supersets s₀ + j₁ < |S| ≤ m_u:** Lemma V(c) and the variance step, so the A_occam (C5′) sum carries the
  j-independent factor e^{‖P_{S₀}e‖²/2σ*²} ≤ e^{s₀}n^{(C_As₀+2cu)/2} on E_u. (ADG) and the truncated moments
  (eτ_j/d)^{d/2}, τ_j = (C_Aj + 2cu) log n, give E Υ^{>j₁} ≤ C q̃_u^{j₁+1} with q̃_u² = 2e(C_A + 2cu) log n/(c_D(n+1)).
  Then apply Markov at level n^{−cu}.
- **(iii) Non-supersets:** compare with S ∪ S₀ ([T03R] (C6)/(C8)). This costs 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2} =
  n^{(A+½)s₀+o(1)}, which is j-independent and absorbed into j₁. The lead's "small ridge loss" alternative is not needed.

**Failure points (DERIVED).**
- **F1.** (OS) as stated is **insufficient**. It only gives the superset sum at level O(r_n), and Markov at n^{−cu}
  needs n^{−(2cu + (A+½)s₀ + …)}. Either (ADG)/(DG) or a graded (OS_u):
  (2p)^{s₀}(n+1)^{s₀/2}𝒪^{>j}_n(u) ≤ n^{−3cu} for j ≥ C u is needed.
- **F2.** The floor range must grow with u: m_u ≈ (3cu/log 2) log n, not m♯_n. With (ADG) only up to m♯_n, Theorem P holds
  only for u ≤ u_max(s₀, A).
- **F3.** Without the coefficient bound (or (F₀)), ρ′ can be ≍ n. Then S₀ is the wrong reference: a column that "boosts"
  a weak S₀ direction has BF ≈ e^{cn}. The right fix is the approximate-reference form (W3-POST2 Claim B, B_T(ϑ) ≤ B).
  This is a change of reference, not a failure of the posterior.
- **F4.** Without any floor the exponential size tail is **REFUTED** at size s₀ + O(u). [T03R] Proposition D (p duplicates
  of a truth) gives π(|S| > m) ≥ 2^{−(m+4)}e^{−m²/(4(p−m))} w.p. → 1. Exact enumeration with near-duplicates (check C4:
  n = 1500, q = 11 nulls with orthogonal residuals, Schur eigenvalue κ/(n+1), κ ∈ {0.5, 2, log n}) gives
  π(|S| = k+1)/π(|S| = k) ≈ 0.5, 0.48, …. Independent nulls give 0.07, 0.047, 0.035, ….

**No floor at all (DERIVED; lead confirmed with explicit constants).** P(π(|S| > m_u) > n^{−cu}) ≤ n^{−cu}, with
m_u − s₀ ≍ (3cu + (A+½)s₀) log₂ n. By F4 this order u log n is **necessary** in the worst case. Through the T04 master theorem
it gives rate (m_u + s₀)ℓ_n/n ≍ u log² n/n at level n^{−cu}. That is **not** SL's form (15), which needs the same ε in rate and
level. Indeed (15) at ε² = u log² n/n needs level e^{−cu log² n}, hence m ≍ u log² n and rate u log³ n/n. With a p-free
geometric size tail, the size-tail route never closes (rate ≥ ε² log n): this is the §2 obstruction again.

**Design-free poly(j)2^{−j} (Q3, last part).**
- **Supersets (DERIVED (unchecked)):** Lemma V(a, b) with a fixed η gives, on E_u,
  Σ_{|J|=j} π(S₀∪J)/π(S₀) ≤ e^{(1+o(1))(1+2/η)ρ′/2σ*²} e^{o(1)(j+u)} V_j, with E V_j ≤ 2(j+1)^{s₀}(1+η)^{s₀}(√(1+η)/2)^j.
  This is poly(j)·(√(1+η)/2)^j·O_P(1) for every η > 0. Choosing η ≍ √(ρ′/j) gives poly(j)2^{−j}e^{C√(ρ′j)}. With ρ′ = 0
  (μ = 0) it is exactly poly(j)2^{−j}.
- **Non-supersets:** OPEN. The (C6) comparison costs n^{(A+½)s₀}, which is not O_P(1). A bound of the form
  Σ_T π(T)·(superset sum relative to T), T ⊆ S₀, needs control of ρ′_T for references that miss weak truths.
- **Sharpness:** 2^{−j} cannot be beaten design-free (Prop. D; C4).
- **The lead's suspected worst case** is refined (DERIVED): the dangerous scale is the **unnormalised** Schur eigenvalue
  γ ≲ C log n/n, i.e. correlation 1 − O(log n/n²) with the span of S₀. There the A_occam weight √(eτ/((n+1)γ)) exceeds 1.
  The true per-direction expected BF there is ≈ 1, not ≫ 1, so these designs break the *proof's* (OS) and the
  *exponential size tail*, not the geometric tail.

**Recommended key-lemma statement (for the lead).**
> **Lemma KL-exp.** In R1 under G, (E: ‖μ‖² ≤ nM), (coefficient bound ‖θ*‖² ≤ nM′, or an approximate reference with
> B_T(ϑ) ≤ B) and (ADG; c_D) for 1 ≤ |J| ≤ m_u: there are c, C, u₀, n₀(u) such that, for u ≥ u₀ and n ≥ n₀(u), outside an event
> of probability ≤ n^{−cu}: π(|S| > s₀ + Cu) ≤ n^{−cu}. Without (ADG) the same holds with s₀ + Cu replaced by m_u = O(u log n),
> and this is sharp in the worst case (Prop. D).

Pair it with an **exponential master theorem** (T04 §5 with each Markov/Chebyshev step replaced by χ²/Gamma tails; A4)
to get Π(‖Xθ−μ‖²/n + |v/σ*² − 1|² > C′u log n/n) ≤ n^{−cu} w.p. ≥ 1 − n^{−cu}: SL's (15) form, in-sample, at ε² ≍ u log n/n.

## 4. Risks the lead may not have seen

1. **Exponential form ≠ size tail alone.** T04's master theorem has three polynomial steps:
   - Ω_n with P ≤ 8/n;
   - Prop. bad, bounded by e^{−ℓ_n};
   - the 2B/ℓ_n and u^{−2} Markov/Chebyshev steps.
   All need upgrading (A4; DERIVED sketch: threshold shifts by cu log n, χ² and Gamma tails). Likewise 𝓑_n (Chebyshev 1/n →
   e^{−cn}, A3).
2. **Size is a proof device for Hellinger.** Duplicates and near-duplicates kill the exponential size tail (F4) but fit
   almost no extra noise. A floor-free exponential Hellinger theorem at rate log n/n may hold via a **fit tail**
   (eᵀM_Se-type effective dimension) instead of |S| (OPEN; heuristic in A5). If the lead wants design-agnostic P2 without
   (ADG), this is the route. Otherwise (ADG) on an O(u log n) range is a genuine extra assumption against SL, who need no
   design condition.
3. **(OS) does not upgrade.** W3-POST2's weakest interface is calibrated to r_n. The exponential version needs (ADG) or a
   graded (OS_u) (F1), and on a u-dependent range (F2).
4. **SL parity on P1 costs design conditions SL do not have.** The coded slab is empirical, so the iid testing route is
   unavailable (§2). The integrated (x,y) Hellinger then needs sparse-eigenvalue transfer of Σ̂ → Σ at level 1 − n^{−cu}
   on supports of size s₀ + Cu. That is fine under sub-Gaussian rows (union over C(p, s₀+Cu) supports). Under SL's
   Condition 2 (second moments) only an in-probability form is plausible, matching their (16).
5. **Intercept and scale.** SL's f* has no intercept. The coded posterior is on the contrast scale with flat-prior
   intercept and data-dependent D_x, s_y. T04 explicitly does not claim "intercept-posterior … random-design Hellinger".
   P1 needs an explicit plug-in or posterior convention for α and for the map θ ↦ β = s_yD_x⁻¹θ.
6. **Brief's notation clash** (M = energy and M = rate multiplier) will leak into constants: C in "s₀ + C·M" depends on the
   energy M through ρ′ (j-independent amplification). Keep the two separate.

---
## Appendix (proofs and computations)

**A1 (Q1 computations).**
- BB identity: P(S) = B(k+1, 2p−k)/B(1,p) = p·k!(2p−k−1)!/(2p)! = ½·k!(2p−1−k)!/(2p−1)! = ½/C(2p−1,k).
- B(r): λ_max(G_S) ≤ tr G_S = r(n−1) and λ_max ≥ n−1 (mean of the diagonal), so B(r) = (λ_max+1)/n ∈ [1, (r(n−1)+1)/n] ⊂ [1, r+1).
- B̃: λ_min(G_S) ≥ 0, so B̃ ≤ n. A singleton gives V = n/n = 1, so B̃ ≥ 1.
- (10): K ln p ≥ (n/2)·ln p, against nε² = u log n (A) or u log² n (B). The ratio → ∞.
- (8)/prior mass: ϖ(S₀) = w(s₀)/W_K ≥ ½/C(2p−1,s₀) ≥ ½(2p)^{−s₀} ([P1] lem:prior(d)).

**A2 (Lemma V).**
- (a) Write ϑ = θ* + ϑ′ (θ* zero-padded) and A_T = G_T + I. Use
  (a+b)ᵀA(a+b) ≤ (1+η)aᵀAa + (1+1/η)bᵀAb and (a+b)ᵀA(a+b) ≥ aᵀAa/(1+η) − bᵀAb/η.
  Then Q₀(μ+e) ≤ Q₀^{(c)}(e) + (1+1/η)ρ′ and Q_S(μ+e) ≥ Q_S^{(1/c)}(e) − ρ′/η, using θ*ᵀA_Sθ* = θ*ᵀA₀θ* = nρ′. Here Q^{(c)}_T(e) =
  eᵀ(I − M^{(c)}_T)e. Subtract.
- D′ ⪰ 0: M^{(c)} decreases in c, and M_S^{(1/c)} ⪰ M_S^{(c)} ⪰ M₀^{(c)} (nested least-squares-type minima).
- Eigenvalues of M^{(1/c)} are g/(g + (g+1)/(cn)) < 1.
- (b) Woodbury: I − M_T^{(c)} = (Σ_T^{(c)})⁻¹ with Σ_T^{(c)} = I + (n/c)X_TA_T⁻¹X_Tᵀ and det Σ_T^{(c)} =: D_T^{(c)}. So
  D′ = (Σ₀^{(c)})⁻¹ − (Σ_S^{(1/c)})⁻¹.
  E_{N(0,σ*²I)} e^{eᵀD′e/2σ*²} = det(I−D′)^{−1/2} ≤ det(I − D′^{1/2}Σ₀^{(c)}D′^{1/2})^{−1/2}, because Σ₀^{(c)} ⪰ I (Weyl).
  This equals det(Σ₀^{(c)})^{−1/2}det((Σ₀^{(c)})⁻¹ − D′)^{−1/2} = (D_S^{(1/c)}/D₀^{(c)})^{1/2}.
  Finally, eigenvalue-wise 1 + cx ≤ c(1+x) and 1 + x ≤ c(1 + x/c) give D_S^{(1/c)} ≤ c^{|S|}D_S and D₀ ≤ c^{s₀}D₀^{(c)}.
  Hence the bound (1+η)^{(s₀+|S|)/2} = (1+η)^{s₀+j/2}.
- (c) M_S^{(1/c)} ⪯ P_S, and P₀ − M₀^{(c)} =: R₀ has eigenvalues c(g+1)/(ng + c(g+1)) ∈ (0, 1] on col X_{S₀}.
- Check C3: 2000 draws on four adversarial families (incl. coefficients ±50 on a 10⁻³-collinear pair in S₀). Max violation:
  (a) −1.5·10⁻³ and (b) −0.094 (both ≤ 0); min eig D′ = −2.6·10⁻¹⁵.

**A3 (Theorem P, explicit).** Constants: C_A := 4A + 8; t_u := 2cu log n.
- E_u = (1) ∩ (2) ∩ (3) ∩ 𝓑_n:
  1. |‖e‖²/σ*² − N| ≤ 2√(N t_u) + 2t_u. Laurent–Massart, failure probability ≤ 2n^{−2cu}.
  2. ‖P_Te‖² ≤ σ*²(C_A|T| + 2cu) log n for all |T| ≤ m_u + s₀. Failure probability:
     Σ_k p^k(ex/k)^{k/2}e^{−x/2} with x = (C_Ak + 2cu) log n, which is ≤ n^{−cu}Σ_k[n^{A−C_A/2}(e(C_A+2cu) log n)^{1/2}]^k ≤ 2n^{−cu}
     for n ≥ n₀(u). χ²_J ≤ τ_j is a special case.
  3. 𝓑_n: Δ_n = σ*²(E′/N − 1) + 2μᵀε/N, so P(|Δ_n| > σ*²/2) ≤ 2e^{−N/64} + 2e^{−Nσ*²/(192M)}.
- (i) On 𝓑_n ([P1] T02(i) proof with S₀ → T): π(|S| > m) ≤ R_m(n+1)^{t/2}√n·c♯e^{Λ′}Θ^{(1)}, with E Θ^{(1)} ≤ 1.
  Laurent–Massart gives Λ′ ≤ 1 + 2√t_u + 2t_u/√n + ρ′/2σ*² w.p. ≥ 1 − 2n^{−2cu}. P(Θ^{(1)} > n^{2cu}) ≤ n^{−2cu}.
  R_m ≤ 2^{2−(m−t)}·2(2p)^t (A1 tail bound and 1/w(t) ≤ 2(2p)^t), which is ≤ n^{−3cu}e^{−C₀√(u log n)}(n+1)^{−t/2}n^{−1/2} at m = m_u for C₀ large.
- (ii) On E_u, with a common factor F_u := e^{(1+o(1))ρ′(1+2/η)/2σ*²}·e^{s₀}n^{(C_As₀+2cu)/2}, the ratio π(S₀∪J)/π(S₀) is at most
  F_u·[w(s₀+j)/w(s₀)](D₀/D_S)^{1/2}e^{jo(1)}e^{χ²_J/2}1{χ²_J ≤ τ_j}.
  Lemma M of A_occam then gives E[·] ≤ … (eτ_j/max(d_J,1))^{d_J/2} ≤ (e(C_A+2cu) log n)^{j/2}, since d ↦ (eτ/d)^{d/2} increases for d ≤ τ.
  [P3] lem:prior(b) and (ADG) give Σ_{|J|=j} ≤ 2(j+1)^{s₀}q̃_u^j.
- (iii) Amplification a(u) = (A+½)s₀ + C_As₀/2 + cu + o(1) in the exponent of n. Markov:
  P(total > n^{−cu}) ≤ n^{cu + a(u)}Σ_{j>j₁}2(j+1)^{s₀}q̃_u^j ≤ n^{−cu} once (j₁+1)/2 ≥ 2cu + a(u) + 1. Take
  j₁ = 6cu + (2A+1+C_A)s₀ + 4.
- Under (F₀), R₀ ⪯ (c(1+1/(Nφ₀²))/n)P₀, so F_u = O(1) and j₁ = 4cu + (2A+1)s₀ + 4.

**A4 (exponential master theorem, sketch; DERIVED (unchecked)).** T04 §§3–5 with:
- ℓ_n → ℓ_n + cu log n in E₂, E₃ (union bounds unchanged);
- ρ(d) enlarged by the same shift (Prop. bad then gives e^{−(cu+1)ℓ_n});
- given (S,v,y), ‖Z_Sθ_S − M_Sy_c‖²/v ~ Σλ_iχ²₁ with λ_i ≤ 1, so P(> 2k + 3cu log n·…) ≤ n^{−cu} by Laurent–Massart,
  replacing 2B/ℓ_n;
- the Gamma(ν,1) tail of Υ replaces Chebyshev.

The constants depend on (σ*², M, M′) through a_{S₀} ≤ ρ′ (in place of φ₀).

**A5 (fit-tail heuristic, OPEN).** For one new direction with Schur eigenvalue γ, κ = (n+1)γ:
- BF = (κ+1)^{−1/2}e^{(κ/(κ+1))Z²/2}, so E BF = 1.
- Under the size-biased law the fitted noise is ≈ κχ²₁, so E[BF·1{fit > F}] ≈ P(κχ²₁ > F).
- Hence directions that are cheap in Occam (small κ) fit little noise. This suggests
  Π(noise fit > Cu log n) ≤ n^{−cu} design-free for supersets. Not attempted.
