# W3-DIST — ROUTES (proof routes, failure points, difficulty; v1.1, 2026-11-15; v1.1 = after blind read S1)

Everything here is a route sketch by the lead (unchecked). Notation: STATEMENT.md. t = nε² up to constants.

## 0. Answer to the brief's question: is (i) "assembly" or new probability?
- **In-probability version: assembly.** Lemma H (deterministic) + Lemma T (classical VC relative deviation, no new
  probability) turn any in-sample contraction statement into the joint (x, y) Hellinger statement. With W3-POST2 D(b)
  this already gives Π(d_H² > C log n/n | D_n) → 0 in probability under (E), (F₀), (OS), and with D(a) the
  parametric rate (needs (TR₀) instead of Lemma T, because Lemma T's remainder is of order d log n / n).
- **Exponential version ([SL] (15)): new proof work, no new probability theory.** The in-sample inputs we have are
  in-probability only, for two separate reasons: (1) the size-tail lemma has a failure probability of order
  1/log L ([W3P] Lemma 1a/1a′); (2) the superset mass is bounded as O_P(r_n). Reason (2) is irrelevant for the
  distribution target — supersets with few extra variables are *good* for the Hellinger distance, which is why the
  inner threshold can be e^{−ct} here although 1 − π(S₀) ≥ n^{−1/2}. Reason (1) needs a new size-tail lemma (Lemma S).
  The tools are Gaussian chi-square tails, exact conjugate formulas and Markov's inequality on truncated moments.

## 1. Why [SL]'s own route does not apply to the coded prior (P5)
(Lead's reading, confirmed with one correction by helper H1, `work/prior_probe/REPORT.md` §1–2; both unchecked.) [SL] Theorems 1–2 follow Jiang (2007):
prior mass near f*, a sieve of models of size ≤ r̄_n, tests. Mapped to the coded prior: r̄_n ↔ K = min(p, ⌊n/2⌋);
V_ξ ↔ n(G_S + I)⁻¹; λ_n = r_n/P_n ↔ BB(1, p), whose size law is P(|S| = k) = ½C(p,k)/C(2p−1,k) ≈ 2^{−k−1}.
- The covariance envelopes behind (11) and (14) are benign for every design: ch₁(V_S⁻¹) = (λ_max(G_S) + 1)/n ≤ |S| + 1
  (standardised columns) and ch₁(V_S) ≤ n (ridge +I). (S1-04: this is a statement about the envelopes; the coded
  beta-binomial mixture has no fixed Bernoulli parameter r_n/P_n, so (14) cannot be called literally satisfied.)
- (9), (10) and (11) **fail** (H1 corrected the lead on (11): B̃_n is harmless, but (11) also carries r̄_n); "r_n ≻ 1" fails too: r̄_n log P_n ≺ nε_n² is false with r̄_n = ⌊n/2⌋. Replacing the hard cap by the prior's own tail does
  not rescue the sieve argument: a sieve {|S| ≤ m} needs prior tail 2^{−m} ≤ e^{−Cnε²} and entropy m log p ≲ nε², which
  are incompatible when log p → ∞. (BB(1, p) is the boundary case of the Castillo–van der Vaart complexity priors.)
- The prior depends on the data (slab through the sample Gram and the sample SDs; IG rate through s_y), which is
  outside the i.i.d. prior-mass/testing framework as stated.
**Route that works for the coded prior:** condition on the design, use the closed-form marginal likelihoods, and let
the slab's Occam factor n^{−1/2} per variable (not the prior on size) control dimension. This is why (ND) appears: it is
exactly the statement that the Occam factor is present. Without (ND) the only dimension control is the prior tail
2^{−k}, which gives dimension of order log n + t and the slower rate of DIST-2.

## 2. Route for Theorem DIST-1 (and DIST-2)
**Step 1 (Lemma H; deterministic; done up to checking).** STATEMENT §3.
**Step 2 (Lemma T; classical).** STATEMENT §3. Apply with d = min(p_raw, n − 1, d_t + s₀^r) (Lemma T's repaired range, S1-01), δ = e^{−ct}: η² ≤ C(t + d_t log n)/n = C′t/n.
On the event, for every posterior draw with |S| ≤ d_t:
  d_H²(f, f*) ≤ (v/σ*² − 1)² + (ε̄² + ‖μ̂ − μ‖²/n)/(2σ*²) + η².
*Failure points:* (a) the exact form/constant of the relative-deviation inequality (citecheck; any version with
log S(2n) works); (b) the level-set class must include the dropped constant columns and the intercept — it does, the
class is over all (a, u) with sparse u, whether or not a column is retained; (c) supports must be uniformly small
under the posterior: that is Step 3's size control (models above d_t are in the bad set). *Difficulty: low.*
**Step 3 (Lemma X; fixed design; the core).** Contrast coordinates, N = n − 1, y_c = μ_c + e.
- X1 noise event 𝓔_t: (i) |‖e‖² − Nσ*²| ≤ σ*²(2√(Nt) + 2t); (ii) ‖P_Te‖² ≤ σ*²(C_A|T| log n + 3t) for all T with
  |T| ≤ m_n(t) + s₀ (union over ≤ p^{|T|} sets, χ² tails); (iii) cross terms |eᵀa_S| ≤ σ*‖a_S‖√(2(|S| + s₀) A log n + 6t)
  for a_S = (I − M_S)μ_c and all |S| ≤ m_n(t); (iv) s_y² ≤ 3(M + σ*²). P(𝓔_tᶜ) ≤ e^{−t}. *Low.*
- X2 good models. For |S| ≤ d_t and L_S ≤ C″σ*²t: [D] D1(a),(b),(d) give, on 𝓔_t, ‖M_Sy_c − μ_c‖² ≤ C σ*²t and
  |Q^c_S/N − σ*²| ≤ Cσ*²√(t/n); the conditional law is explicit (v ~ IG(ν, b + Q^c_S/2); ‖X_c(θ − θ̂)‖² | v ≤_st vχ²_{|S|}),
  so Π(bad | S, y) ≤ e^{−ct} by χ² and Gamma tails. *Failure point:* needs d_t log p ≲ t, i.e. d_t = s₀ + O(t/log n) —
  this is where the dimension bound sets the rate. *Low–medium (bookkeeping).*
- X3 small far models (|S| ≤ d_t, L_S > C″σ*²t). On 𝓔_t, Q^c_S − Q^c_{S₀} ≥ L_S/2 − Cσ*²t ≥ C″σ*²t/4, so
  ((2b + Q_{S₀})/(2b + Q_S))^ν ≤ e^{−C″t/20}; with D_{S₀}^{1/2} ≤ (n+1)^{s₀/2}, D_S ≥ 1 and Σ_S w(|S|)/w(s₀) ≤ 2(2p)^{s₀}:
  π(far small)/π(S₀) ≤ 2(2p)^{s₀}(n+1)^{s₀/2}e^{−C″t/20} ≤ e^{−ct} once t ≥ M₀ log n, M₀ ≍ s₀(A + 1)/C″. This is the only
  place the constant M₀ ∝ s₀(A+1) comes from (the rate s₀ log p/n). Template: [P2] Lemma E1(b). *Medium.*
- X4 large models (|S| > d_t). (a) |S| > m_n(t): Lemma S. (b) supersets S₀ ∪ J, d_t − s₀ < |J| ≤ m_n(t) − s₀: on 𝓔_t the
  likelihood gain is truncated at τ_j = C_Aj log n + 3t; the truncated moment of the Bayes factor is
  ≤ (D_{S₀}/D_{S₀∪J})^{1/2}·2^{j/2}(eτ_j/max(d_J,1))^{d_J/2} ([P2] A_occam's a_J with C_A log n → τ_j/j); sum with (ND):
  Σ_{j>d_t−s₀} [C(s₀+j, j)2^{−j}]·(C t /(c_D n))^{j/2}-type ≤ (Ct/(c_Dn))^{(d_t−s₀)/2} ≤ e^{−3ct} when
  (d_t − s₀) log(n/(Ct)) ≥ 6ct; Markov at level e^{−ct}. (c) non-supersets with d_t < |S| ≤ m_n(t): compare with S ∪ S₀
  ([T03R] (C6)/(C8) device, loss ≤ 2^{s₀}(2p)^{s₀}(n+1)^{s₀/2}, absorbed as in X3).
  *Budget before Markov (S1-06; H1 A3):* the superset sum carries (1) the j-independent factor
  exp(‖P_{S₀}e‖²/2σ*²) ≤ e^{C(t + s₀ log n)} from Lemma V(c) (no (F₀)); (2) the union multiplicity
  2^{s₀}(2p)^{s₀}(n+1)^{s₀/2} for non-supersets; (3) the variance surcharge: ν/(2b + Q_{S₀∪J}) ≤ (1 + ε_{n,t})/(2σ*²),
  ε_{n,t} = O(√(t/n) + (m_n(t)+s₀) log n/n), costing e^{ε_{n,t}(j log n + t)} in the truncated moment. All three are
  absorbed by taking C′ in d_t − s₀ = ⌈C′t/log n⌉ large, using log(n/t) ≥ κ₀ log n; C′ is chosen after budgeting them.
  *Failure points:* (a) uniformity: **one n₀ for all t in [M₀ log n, n^{1−κ₀}]** (H1's Theorem P has n₀(u)); (b) (ND) is
  an average over J of fixed size, but the truncation weights depend on J through d_J — replace by the uniform
  envelope before averaging; (c) unions S ∪ S₀ outside Ω (handled in [P2] by letting the sum run to min(m, p − s₀));
  (d) the conclusion of X must include the size statement Π(|S| > d_t | y) ≤ e^{−ct} on the same event.
  *Medium–high; this is the kill-budget item.*
**Step 4 (Lemma S).** Re-run the proof of [P2] Claim B (`W3-POST2/lemmas/B_tail_approx.md`, Steps 1–4) with T = S₀,
ϑ = θ*: on 𝓑_n, π(|S| > m) ≤ R_m√(D_{S₀})√n · c♯ e^{Λ″_n} Θ^{(1)}_{n,m}, with E Θ^{(1)} = 1 and
Λ″_n = |E′ − N|/(2√n) + E′/(2n) + ρ″/(2σ*²). The weak tail of Claim B comes only from applying Markov's inequality to
Λ″_n and Chebyshev's to 𝓑_n. Replace them by χ² and Gaussian tails: P(Λ″_n > C + C√t + t/√n) ≤ e^{−t},
P(𝓑_nᶜ) ≤ e^{−cn} (s_y² is a non-central χ² average), and P(Θ^{(1)} > e^{t}) ≤ e^{−t} (Markov, which is already an
exponential-form bound). With R_m ≤ 2(2p)^{s₀}2^{−m} and D_{S₀} ≤ (n+1)^{s₀} this gives the cutoff m_n(t). The
data-dependent IG rate b = b₀s_y² is already handled there by the bracket b₋ ≤ b ≤ b₊ on 𝓑_n ([P1] `lem:num`, `thm:Ta`).
*Failure points:* (1) 𝓑_n's exact definition must admit an exponential bound (lead's reading: yes, two-sided bound on
s_y²; to be confirmed against [P1]); (2) the t/√n term needs t ≤ n^{1−κ₀} to stay o(t). *Difficulty: low–medium* (lead's
estimate after reading Claim B's proof; an earlier draft of this file rated it medium–high). *If it fails:* fall back
to Claim B as it is, which gives the (16)-form (in probability) for DIST-1/2 but not (15).
**Step 5 (random design).** Lemma X is uniform over designs satisfying the interfaces with the given constants, for
n ≥ n₀(constants), and ε is independent of X: integrate over X, add P(interfaces fail) and Lemma T's δ. No diagonal
transfer is needed for the exponential form. *Low.* (For DIST-3: the diagonal transfer of [POST] step (5), as in
[W3P] item 6.)
**DIST-2:** Steps 1–5 with d_t := m_n(t) and no X4(b),(c); the rate is (m_n(t) log p + t)/n ≍ t log p/n.

## 2b. Route for the reader versions (bridges; on the critical path since HQ steer A5)
Theorem A = (1.1) + B0 + B1 + B2 (second sentence: (1.2) + B0 + B1). All three bridges are standard probability:
- **B0**: W3-MISR Lemma R′ (a′) (PROVED-CHECKED), used pathwise with ỹ = (y − α*)/σ*, plus the transformation of the
  plug-in intercept (P1-05: a statement about the law of the posterior alone would not suffice, because d_H also
  depends on ȳ and x̄). *Low.*
- **B1**: Bernstein for the squares of sub-Gaussian variables, union over p ≤ n^A columns; then the triangle
  inequality for ‖μ‖ and the definition of θ*. *Low.* *Failure point:* none seen; the S1-05 counterexample is excluded by
  (A5) (bounded standardised coefficients), not by tails.
- **B2-core**: one-sided (lower) uniform bound for sparse sample second moments with an intercept: net on the unit
  sphere of ℝ^{q+1} for each of C(p, q) supports, Bernstein for sub-exponential (a + uᵀz)², union; needs
  q log(ep/q) ≤ c n/K⁴, true for q = q_n, M ≤ √n. *Low–medium.* *Failure points:* (1) the sub-Gaussian assumption must be
  the ψ₂–L₂ form on sparse directions ((A3) as written), not marginal sub-Gaussianity of coordinates — with marginal
  tails only, a sparse direction can have tiny variance and heavy relative tails; (2) centring by the sample mean
  (handled by the augmented vector (1, z)); (3) exact constants.
- **B2**: algebra from B1 and B2-core to (F_w; c_ψ/8), then eigenvalue interlacing for the one-column determinant
  ratio (≥ (n+1)g₀/(1+g₀)) to (DG) and (ND). *Low.*
  *Failure point:* the range — (ND) is needed on |J| ≤ m_n(t), so (A3), (A4) are needed on sets of size
  q_n = O(M log n); this is why q_n depends on M in the reader statement.
- **B3** (Theorem B only): the same events give (TR₀; 2), (F_λ), (F_w), BM-∞ with common constants; then W3-POST Theorem 1
  item 6 (consumed; Theorem B is conditional on it). *Low.* *Failure point:* W3-POST Theorem 1 is stated for fixed σ*²
  and s₀ ≥ 1: use B0 and assume exactly s ≥ 1 nonzero coefficients.
If B2-core failed in the stated generality, the fallback is Gaussian rows (W3-POST Corollary 1R's argument, with a
stronger eigenvalue requirement) — a WEAKER change to the reader target clause, hence an early checkpoint.

## 3. Route for Theorem DIST-3 (oracle bound; v1.1 after S1 Better-theorem 1–2)
Given S = S₀ only one support is involved, so no union over models and no logarithm: [D] D1 gives
‖M_{S₀}y_c − μ_c‖² ≤ 2‖P_{S₀}e‖² + 2L_{S₀} ≤ C(s₀ + u + B) outside probability e^{−u}; the conditional fitted-mean
fluctuation is ≤_st vχ²_{s₀}; Q^c_{S₀} − ‖e‖² is O(u) (cross term variance ≤ σ*²L_{S₀}); v has Gamma tails at scale
√(u/n); ε̄² ≤ 2σ*²u/n. Lemma H without truncation and (TR₀) give E_xΔ(x)² ≤ C_T(ε̄² + ‖μ̂ − μ‖²/n). Add δ_n for S ≠ S₀.
(F₀) is not used; W3-POST2 D(a) is not consumed. *Failure point:* Lemma T cannot replace (TR₀) at this scale (its
remainder is of order log n/n); (TR₀) needs second moments of x on supp β* and is automatic only for a fixed law.
*Difficulty: low.*

## 4. Route for Theorem DIST-C (coded output)
Lemma P6 is one line each (domination Q ≤ Lπ; Markov over models, a > 0). Statements are under the joint law P⊗; bad
output events are contained in bad data events. (C-ii)(α): retention is the top-store order
(`cpp/v3_ledger.h:49-56`: an offered model is kept unless ≥ cap better ones are present; S₀ is the unique maximiser of
F when δ < ½ — C-PACK SL0(iv)), discovery from the cited delivery results under their premises. *Failure points:*
(1) **overclaim risk**: the code returns no distribution; the theorem must say "the store BMA / HPM plug-in defined
from the returned output", never "the SMC's posterior approximation"; (2) EX-A (exact scores) — floating point is
outside; (3) without beta-min the premise P-STORE (store holds a fixed fraction of the mass) has no proof and no
output certificate; a weaker observable sufficient condition (Σ_𝒯e^F ≥ η·Ẑ and Ẑ ≥ Z/2) would need [SAMP] Theorem C's
regime. *Difficulty: low for what is stated; P-STORE without beta-min is OPEN and not attempted.*

## 5. Stretch routes
- **S-APX:** carry a reference (T, ϑ) through X3 and Lemma S in place of (S₀, θ*) ([P2] Claim B does this for the size
  tail). Expected cost: + C·Δ_n² in ε². *Medium;* decide at CP2.
- **S-FIT (sharp rate without (ND); was S-DIM):** the size-tail route cannot close without a floor (H1 F4 and §2: a
  p-free geometric size tail against an entropy of log p per variable). The only open route is a fit tail: bound the
  posterior mass of {eᵀM_Se > t} directly. Per new direction with Occam factor d ∈ [1, n+1], the truncated moment is
  P(|N(0, d)| ≤ √τ) and the fitted noise is (1 − 1/d)²z²; the dangerous scale is d ≍ log n (unnormalised Schur eigenvalue
  ≍ log n/n), where neither factor is small. There the lead's heuristic gives mass ≈ c^k at in-sample error k log n — an
  in-probability rate M_n log p/n at best, not the exponential form — while N4 shows no degradation in one such family.
  Unresolved. *High; one Fable attempt + one Astra break review (PROTOCOL rule 14), only after DIST-1/2.*
- **S-EXP:** track log(p ∨ n) explicitly in X1–X4 and Lemma T (η² ~ d log p/n). The constants c₀(s₀, A) of the inherited
  selection results are not needed by DIST-1/2. *Medium;* by-product if Lemma X is written with ℓ_n = log(p ∨ n).

## 6. Route ranking
1. DIST-1 via H + T + X + S (target; reaches P1, P2, P3, P5). Risk concentrated in X4 and S.
2. DIST-2 via H + T + X′ + S (no design condition; needs S).
3. In-probability fallbacks (no new lemma): D(b) + H + T (sharp rate, in probability, conditional on W3-POST2:D);
   D(a) + H + (TR₀) (parametric).
4. DIST-C via P6 + existing delivery results.
5. Stretch: S-APX, S-EXP, then S-FIT.
