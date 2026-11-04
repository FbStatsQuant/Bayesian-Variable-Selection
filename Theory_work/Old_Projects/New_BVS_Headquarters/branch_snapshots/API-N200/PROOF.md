# API-N200 — PROOF.md: a finite-n composition theorem for the reported HPM, and what is rigorous at n = 200

Run API-N200 (Fable 5.1), branch `theory/API-N200`, 2026-11-02. Everything here is a **candidate**: not reviewed, not adopted.
Notation: `Docs/Theory/theorems/00_COMMON.md` and the T21 statement as proved (`Docs/Theory/proofs/T21_T14H_HPM_composition/STATEMENT.md`).

## 0. Setting (fixed n, p, design, truth)

Fix n ≥ 3, p ≥ 1, the standardised design X, the truth S₀ ∈ Ω, θ* and σ*² (hypothesis G: ε ~ N(0, σ*²I); P₀ is the law of y given X). Ω = {S ⊆ [p] : |S| ≤ K}, K = min(p, ⌊n/2⌋). F(S) = log[ϖ(S)m(S)] is the exact score (EX-A). Let ≻ be T21's **total order** on Ω: S ≻ S′ iff F(S) > F(S′), or F(S) = F(S′) and |S| < |S′|, or F and size equal and S is lexicographically smaller. S† := max_≻ Ω is the global HPM (unique, by totality).

The run: 𝒪 is the output-available event, U := 𝒪ᶜ. On 𝒪 the run has a nonempty scored set 𝒮 ⊆ Ω and reports Ŝ := max_≻ 𝒮 (the same total order; T21 §1). P is the joint law of data and algorithm randomness (EX-S), with data marginal P₀. Nothing below uses anything about *how* 𝒮 is produced: tables, pilot, final run, rejected proposals, scans. In particular no coupling, no SR, no CAL is needed for Theorem N200 itself; they enter only through the discovery bounds of T21 that one may plug into its last term.

Three classes of fit with output (the S-ELS classification, made order-exact):
- **exact recovery:** Ŝ = S₀;
- **posterior miss:** Ŝ ≠ S₀ and Ŝ ≻ S₀;
- **search miss:** S₀ ≻ Ŝ.

Since ≻ is total, on 𝒪 exactly one of the three holds. (With continuous noise, F-ties have P₀-probability zero, so "posterior miss" is a.s. the event {Ŝ ≠ S₀, F(Ŝ) ≥ F(S₀)} used by S-ELS, and "search miss" is a.s. {F(S₀) > F(Ŝ)}.)

## 1. Lemma 1 (deterministic inclusions). PROVED.

On 𝒪:
- (a) {posterior miss} ⊆ {S† ≠ S₀};
- (b) {search miss} ⊆ {S₀ ∉ 𝒮};
- (c) {S† ∈ 𝒮} ⊆ {Ŝ = S†}; hence {S† ≠ S₀, S† ∈ 𝒮} ⊆ {Ŝ ≠ S₀};
- (d) {S† ≠ S₀} ⊆ {π(S₀) ≤ ½}.

*Proof.* (a) Ŝ ∈ 𝒮 ⊆ Ω and Ŝ ≻ S₀, so S₀ is not the ≻-maximum of Ω, i.e. S† ≠ S₀. (b) If S₀ ∈ 𝒮 then Ŝ = max_≻ 𝒮 satisfies Ŝ ⪰ S₀, contradicting S₀ ≻ Ŝ. (c) S† is the ≻-maximum of Ω ⊇ 𝒮; if S† ∈ 𝒮 it is also the ≻-maximum of 𝒮, which is Ŝ by definition (uniqueness of the maximum of a total order). (d) If π(S₀) > ½ then e^{F(S₀)} > Z/2 > e^{F(S)} for every S ≠ S₀, so F(S₀) > F(S) for all S ≠ S₀ and S₀ = S†. ∎

(d) is the deterministic core of T21's C1 (`hpm_eq_truth` in the Lean file `theory/L-LEAN:…/T21HPM.lean`); (a)–(c) are the same kind of one-line order facts. None needs a probability.

## 2. Theorem N200 (finite-n composition, two-sided, every term explicit). PROVED.

For every n, p, X, S₀, θ*, σ*², and every law of the algorithm's randomness:

**(i) Identity.** P(U ∪ {Ŝ ≠ S₀}) = P(U) + P(𝒪, posterior miss) + P(𝒪, search miss).

**(ii) Upper bound.**
  P(U ∪ {Ŝ ≠ S₀}) ≤ P(U) + P(𝒪, S† ≠ S₀) + P(𝒪, S₀ ∉ 𝒮) ≤ P(U) + **Π(X)** + P(𝒪, S₀ ∉ 𝒮),
where **Π(X) := P₀(S† ≠ S₀ | X)** is the *posterior-miss probability of the design*: a function of (X, θ*, σ*²) only, free of the algorithm.

**(iii) Lower bound.**
  P(U ∪ {Ŝ ≠ S₀}) ≥ P(U) + P(𝒪, S† ≠ S₀) − P(𝒪, S† ∉ 𝒮).

**(iv) Comparison with T21 (C1).** P(𝒪, S† ≠ S₀) ≤ P(𝒪, π(S₀) ≤ ½) ≤ P(π(S₀) ≤ ½) ≤ 2E₀δ₁, with δ₁ = 1 − π(S₀). So (ii) implies T21's C1 term by term, and is strictly sharper whenever P₀(S† ≠ S₀) < 2E₀δ₁. (At n = 200 the right side exceeds 1, see §4; the left side is 5–75% per cell.)

*Proof.* (i) is the trichotomy of §0 (the three events partition 𝒪, and U is disjoint from 𝒪). (ii): Lemma 1(a) bounds the second term of (i) by P(𝒪, S† ≠ S₀) ≤ P(S† ≠ S₀) = E₀[Π(X)] = Π(X) (X is fixed); Lemma 1(b) bounds the third. (iii): by Lemma 1(c), {𝒪, S† ≠ S₀} ⊆ {𝒪, Ŝ ≠ S₀} ∪ {𝒪, S† ∉ 𝒮}, so P(𝒪, Ŝ ≠ S₀) ≥ P(𝒪, S† ≠ S₀) − P(𝒪, S† ∉ 𝒮); add P(U) (U and {𝒪, Ŝ ≠ S₀} are disjoint). (iv): Lemma 1(d) and Markov's inequality P(δ₁ ≥ ½) ≤ 2E₀δ₁ (T21, `markov_half`). ∎

*Remarks.*
1. The theorem is exact at every n and needs no hypothesis beyond EX-A (exact scores) and the definition of Ŝ as the ≻-maximum of the scored set. Floating point enters through O-CERT's score contract SC(η_F): under SC(η_F) replace "Ŝ ≻ S₀" by a margin 2η_F; S-ELS's smallest observed margin is 0.0049 nats, about 10⁶ times the measured η_F ≈ 3·10⁻¹².
2. The three terms of (ii) are of different natures. P(U) is operational (resource limits); it is **measured**, not bounded. Π(X) is **statistical**: it is what Thm 1 (T03) drives to zero as n → ∞, and at n = 200 it is a computable quantity (§3). The discovery term is **algorithmic**: T21's routes (a)–(f) bound it a priori; at n = 200 those bounds are vacuous (§5) and the term is **measured per fit** (S-ELS: 0 of 2,394) and **certifiable per fit without S₀** (O-CERT C5).
3. (iii) is new relative to T21 and is what justifies reading the observed miss rate as an estimate of Π(X): the observed rate is sandwiched between Π(X) − P(𝒪, S† ∉ 𝒮) − P(U) and Π(X) + P(𝒪, S₀ ∉ 𝒮) + P(U) (both correction terms are discovery terms).
4. Nothing is claimed about PIPs or Ẑ.

## 3. The posterior-miss term Π(X) at finite n: what is rigorous

Let 𝒩(S₀) be the one-move neighbourhood of S₀ (p − s₀ adds, s₀ drops, s₀(p − s₀) swaps), L := {∃S′ ∈ 𝒩(S₀): F(S′) > F(S₀)} the **one-move posterior-miss event**, and p_e := P₀(F(S_e) > F(S₀) | X) for each one-move event e. For d ≥ 1 let L_d := {∃S′ ≠ S₀, |S′ Δ S₀| ≤ d : F(S′) > F(S₀)}; L_1 ⊆ L = L_1 ∪ {swaps} ⊆ L_2.

**Proposition 2 (brackets). PROVED (exact score, no PA).**
  max_e p_e ≤ P₀(L | X) ≤ P₀(L_2 | X) ≤ … ≤ Π(X),   and   P₀(L | X) ≤ Σ_e p_e.
*Proof.* Every S′ beating S₀ strictly makes S₀ ≠ S†, as F(S′) > F(S₀) means S′ ≻ S₀; monotonicity and the union bound give the rest. ∎ (This is O-SWAP's Theorem 4 with the chain of Hamming balls added.)

**What is computable.**
- **P₀(L | X) by exact-score Monte Carlo** given X (fresh ε, the exact F): rigorous up to a binomial Monte Carlo error. O-SWAP did this on the study's own 1,200 designs (R = 40 draws per design, 4,000 per cell); the per-cell values are in `results/n200_table.md`. Its exact-score "L or double drop" event is a lower bound for L_2.
- **The p_e in closed form under PA** (O-SWAP Props 1–3; PA = Lemma 0's projection approximation, error O(10⁻³) nats in a log-score difference): swap Φ(−d₋)Φ(d₊) + Φ(d₋)Φ(−d₊) at λ = 1, add P(χ²₁(1 − λ/(n+1)) > (λ − 1)(χ²_{n−2−s₀} + ω₀)), drop E[Φ(t − |δ_j|) − Φ(−t − |δ_j|)]. So max_e p_e and Σ_e p_e are computable per design; they are rigorous only up to PA and O-SWAP's treatment of the residual χ² (E_U replaced by its mean in the swap quadrature, error ≤ 0.03σ²). Turning the PA error into a bound on a *probability* needs an anti-concentration margin for the score gap at 0 (O-SWAP §7.3): unwritten, so the closed forms are **PA-exact, not rigorous**.
- **An upper bound on Π(X)** at n = 200: **OPEN**. Π(X) = P₀(L) + P₀(Lᶜ, S† ≠ S₀), and the second term has no proved bound. The evidence that it is small is (a) exact-score MC with double drops: ≤ 1.1 points per cell (O-SWAP; column "excess" in the table); (b) the realised one-move + double-drop + hill-climb check on the study's own y reproduces the observed SMC count in all 24 cells to ±1; (c) exact enumeration at p = 12 (`results/small_p_exact.txt`): the excess P_post − P(L) is 0.2–1 point at c = 1, 0.3–3 points at c = 0.75, and up to 8 points at c = 0.35–0.5, where the Hamming-2 event L_2 leaves at most 2 points. This is **empirical, not a theorem**.

**Why a union bound over Hamming balls cannot close it (recorded as a failed route).** The distance-2 supersets alone number C(p − s₀, 2) ≈ 1.2·10⁵ at p = 500. Under PA with orthonormal residualised nulls, the two-add gain is g(B_l² + B_{l′}²) − 2κ⁺ with g convex, g(0) = 0, and (B_l, B_{l′}) ~ N(0, I): the union bound Σ P(χ²₂ > 4κ⁺(1+η)) ≈ 1.2·10⁵·e^{−2κ⁺(1+η)} ≈ 0.07 at p = 500, c = 1, the same size as the whole one-add rate. The bound is loose because the two-add event is almost entirely contained in the one-add events: by convexity g(x + y) ≥ g(x) + g(y), so "two-add beats, neither single add beats" forces both B_l² and B_{l′}² into the shell [thr − c_n, thr] with c_n ≈ g(2·thr) − 2g(thr) ≈ ν(thr/Q)² ≈ 0.5 nats; the shell has probability ≈ 7·10⁻⁵ per null, so the two-add-only event has probability ≈ C(p − s₀, 2)(7·10⁻⁵)² ≈ 6·10⁻⁴ for orthogonal nulls. **PROOF SKETCH** for orthogonal nulls only; for correlated nulls the quadratic form (B_l, B_{l′})Γ⁻¹(B_l, B_{l′})ᵀ ~ χ²₂ remains exact (central) but the shell argument must be redone in the Γ-metric, and the drops/swaps at distance 2 are not covered. A rigorous upper bound on Π(X) via "L plus a controlled remainder" is the research item (needs escalation).

## 4. T21's middle term is vacuous at n = 200; Π(X) is not

By Lemma 1(d) and Markov, T21 bounds the posterior part by 2E₀δ₁. At n = 200 this exceeds 1:
- O-CERT (4 regenerated study fits, production engine): π(Ŝ) ≤ 0.37 **even when Ŝ = S₀** (certified, deterministic: Z ≥ Z_𝒯), with the local share π(Ŝ | N̄(Ŝ)) = 0.46 at c = 1. So δ₁ = 1 − π(S₀) ≥ 0.63 on those fits and 2δ₁ ≥ 1.26.
- Mechanism (O-SWAP Prop 2): the p − s₀ ≈ 486–986 supersets S₀ + l each carry posterior ratio e^{F(S₀+l) − F(S₀)} = e^{−κ⁺_l + g(B_l²)} with B_l ~ N(0, σ²) central and κ⁺ ≈ 6.8–7.5 nats, and the sum over nulls of these ratios has a heavy right tail; π(S₀) = (1 + Σ_{S ≠ S₀} e^{F(S) − F(S₀)})⁻¹ is therefore typically well below ½ although S₀ is the mode.
- Exact small-p enumeration (`results/small_p_exact.txt`, p = 12, n = 40): the columns P(π(S₀) ≤ ½) and 2E₀δ₁ against P_post.

So the finite-n content of Theorem N200 lies entirely in replacing {π(S₀) ≤ ½} by {S† ≠ S₀}: the HPM is right whenever S₀ is the *mode*, not only when it carries half the mass. (T03's asymptotics make the two coincide; at n = 200 they are far apart.)

## 5. The discovery terms at n = 200

Upper term P(𝒪, S₀ ∉ 𝒮); lower term P(𝒪, S† ∉ 𝒮).

**A priori (T21 routes), rigorous but vacuous.**
- Route (a), fresh iid draws: P(S₀ ∉ 𝒮) ≤ P(F_cal^c, S₀ ∉ 𝒮_cal) + E[1_{F_cal}1{S₀ ∉ 𝒮_cal}(1 − π₀(S₀))^{Q_f}]. At the study budgets N₀ = 2500, L = 8, Q_f ≥ 4N_e(L + 6) = 1.4·10⁵ (e = 0), and π₀(S₀) has per-cell median 10^{−11}–10^{−26} (O-DILUTE, 480 regenerated fits; the study's H2 tables say ≈ 10^{−12} or smaller; 1 favourable fit of 2,394). So Q_fπ₀(S₀) ≲ 10⁻⁶ and the bound is ≥ 1 − 10⁻⁶: **vacuous**. The deficit is σ²-dilution (O-DILUTE Thm E: −log π₀(S₀) = V + C − log A, V ≈ 83% of it), so no restatement of (a) helps at this n.
- Route (d), tables and scans: S₀ is not inside one block (14 truths over blocks of size ≤ 14 with proxies), so table scoring does not apply. The final scan's centre S_c = Ŝ had S₀ ∈ N(S_c) in 434 of the 541 near-truth misses and in all 1,829 recoveries trivially; a completed scan from such a centre scores S₀ (T20(ii)), which is a **per-fit certificate** of the (already observed) scoring, not an a-priori bound.
- Routes (b), (c), (e): E_G, PX, H24 are open at every n.
So the best rigorous a-priori discovery bound at n = 200 is 1.

**Measured per fit (S-ELS, the actual 2,400 fits).** S₀ ∈ 𝒮 in 2,394 of 2,394 completed fits (it sits in the fit's top-20,001 store with F(S₀) equal to the offline value to 10⁻¹²); search misses 0 of 2,394; exact 95% Clopper–Pearson upper bound on the per-fit search-miss rate: 1 − 0.05^{1/2394} = 0.125%. The lower-bound term P(𝒪, S† ∉ 𝒮) is not observable (S† is unknown at p = 500), but every reported Ŝ is a certified 1-flip/swap local maximum (`local_certified` in 2,394 of 2,394), and the realised hill-climb check matches the counts (§3), so the term is empirically consistent with 0. This is **measured, not proved**.

**Certifiable per fit without S₀ (O-CERT C4–C5).** For any data-measurable U = U(X, y, Ŝ) with Ŝ ⊆ U: {𝒪, search miss} ⊆ {𝒪, box certificate C4(a) fails for U} ∪ {𝒪, S₀ ⊄ U}. The first event is decided by a branch-and-bound over 2^U (≤ 38 s at |U| = 31 on the four illustrated fits, all passing); the second is a screening probability, measurable in simulation and not yet tabulated over the 2,400 fits (OPEN bookkeeping; S-ELS shows S₀ within 4 moves of Ŝ in 2,370 of 2,394 completed fits).

## 6. Assembled statement for the paper (candidate wording)

**Theorem (finite-n composition).** For every n, p, design, truth and noise level, and for the method as run,
  P(no output or Ŝ ≠ S₀) = P(no output) + P(output, Ŝ ≻ S₀) + P(output, S₀ ≻ Ŝ)
  ≤ P(no output) + P₀(S† ≠ S₀ | X) + P(output, S₀ never scored),
and P(output, Ŝ ≠ S₀) ≥ P(output, S† ≠ S₀) − P(output, S† never scored). The posterior-miss probability P₀(S† ≠ S₀ | X) depends only on (X, θ*, σ*²); it is bounded below by the one-move event P₀(L | X), which is a Gaussian/χ² computation in the residual projections of X (O-SWAP Props 1–3), and above by nothing proved at finite n.

Status: Theorem PROVED (elementary; a candidate for Lean after T21HPM.lean, where `hpm_eq_truth`, `t21_event_subset` already carry the ≤ ½ version). The evaluation of Π(X) at n = 200 is a computation (rigorous lower bracket, PA closed forms, empirical remainder); the discovery term is measured.
