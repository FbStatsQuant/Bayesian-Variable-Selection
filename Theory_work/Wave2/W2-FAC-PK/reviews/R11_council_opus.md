# W2-FAC-PK — council round 2, Claude seat (Opus 5.5, fresh seat)

**Score: 9.2 / 10 (uncapped). All six gates PASS. Every round-1 required fix has been applied correctly.
Required fixes: one minor wording fix to a labelled heuristic in REPORT §5 (F1). It does not block a pass and affects no
claim.**

Scope. I read STATEMENT v3.1, L0–L4, METHOD_REQUIREMENTS and REPORT, and re-derived every inequality chain by hand. Sources
compared:
* FACB L1 (L1.2/L1.3/L1.5), L2.3(i) and L4.0(d)/(e);
* W1-GEN STATEMENT:169 ([OP]) and W1-GEN REPORT:20;
* FINAL s7:64 (Lemma CAP status and council history);
* FACB R03/R04/R05 verdicts;
* the production code: `v3_engine.h:379–418`, `v3_core.cpp:394–404, 466–480`, `v3_run.R:92–101`, `v3_fit.R:30–66, 113–145`.

I used R01–R09 only after forming my own assessment. Scratch is in `reviews/R11_scratch/`:
* `citecheck_rerun.py` and `CITECHECK_rerun.txt`: the registry rerun to a separate file. Result: 38 checked, 0 misses.
* `r11_checks.py` and `r11_checks_output.txt`: N1/N3 aggregates, a check of the generic G1 inequality, the L2.2(iii)
  constants, and the p ≫ n heuristic count used in required fix 1.

The frozen hashes in `numerics/FROZEN_SNAPSHOTS.sha256` verify (both files OK). I wrote nothing else. No git state was
changed.

## Verification of the round-1 required fixes

| item | where | verdict |
|---|---|---|
| R08-1 (MAJOR): G2 not design-free | REPORT:98–102. G2 is now restricted to T ⊇ S₀, \|T\| ≤ K, p ≤ n − 1. R08's p = Kn counterexample is recorded, and p ≫ n is listed as an extra proof obligation. The §5 heuristic is qualified ("not automatic for p ≫ n", REPORT:83). | **applied, correct** |
| R08-2: generic G1 | REPORT:93–97. I checked the generic bound independently (see below). | **applied, correct** |
| R08-3: mechanism paragraph | REPORT:40–51. It now says ≥ p − K − s₀ exclusions, G_sw ≥ M_TV_{jl} ≥ ½log n + 2 (L2.2(iii)) and (c_D − ε)log n. The budget runs from the first truth-containing centre, with an O(log n) initial phase and an O(log²n) remainder. | **applied, correct** |
| R08 optional: citation count | REPORT:63 says 38, matching CITECHECK and my rerun. | applied |
| R09-M1: delivery refers to plumbed code | STATEMENT:85–87 and L4:57–59. | **applied** (see optional 2) |
| R09-E1: L2.2(i) needs neither (PK) nor (PB) | L3:96 | applied |
| R09-E2: \|E\| ≤ 6H̄ | L1:58 | applied, correct |
| R09-E3: c₅ := min(c₄²/8, ½) | L2:40 | applied |
| R09-E4: "(PK′)" | L1:49 | applied |
| R09-E5: citation count | REPORT:63 | applied |
| R09 optional 1 and 3 | METHOD_REQUIREMENTS:48–49, L3.5 remark 0 | applied |

The disposition explains why it did not adopt R09 optional 4: stating G2 through |T| ≤ K ≤ n/2 alone. The R08 plane
counterexample shows that the union bound needs p ≤ n − 1 (2^p ≤ 2^n). That counterexample is correct: in each plane the
nearest of n directions to the noise direction leaves residual O(n⁻²)‖Z_b‖². I agree with keeping the stricter version.

**Generic G1 check.** For any Gram G, write H = (n + 1)G + I. The Schur-complement ratio for adding column j is

  [(n + 1)g_jj + 1 − (n + 1)²vᵀH_U⁻¹v] / [g_jj + 1 − vᵀ(G_U + I)⁻¹v].

This is ≤ n + 1 if and only if (n + 1)vᵀ[(G_U + I)⁻¹ − (G_U + I/(n + 1))⁻¹]v ≤ n. That holds because the bracket is ⪯ 0.
So each increment of L_U is ≤ log(n + 1) for every design. The nested quadratic z_UᵀH_U⁻¹z_U is nondecreasing, so Q is
nonincreasing. Also, w(s₀)/w(k) = Π_{i=s₀+1}^{k}(2p − i)/i ≤ C(2p − 1, K) for k ≤ K < p, because every factor is ≥ 1.

I confirmed this numerically on 400 random correlated designs. The largest value of (increment − log(n + 1)) was
−0.59 < 0, and Q never increased. The generic G1 is valid as written.

## Gate verdicts

**1. Correctness of every step (L0–L4): PASS.** These are the points I tried to break.
* **L0.**
  * The representation needs only p ≤ n − 1 (r ≡ 0 at p = n − 1).
  * The closed forms and gains are pure algebra.
  * τ-form: n t²/(αψ_T) = M_Tτ²/ν, and −log(1 − v) ≥ v gives G_sw ≥ M_TV.
  * The only uses of p ≤ n/2 are FACB's E2 lower bound on r and the bulk bound of FACB L4.0(d). Both are correctly
    excluded.
  * The (M2) refinement uses only Φ(T) ≤ ‖g_T‖²/(1 − ρ) ≤ 2Σ_Tξ² + 2kρη²/(1 − ρ). I checked this against FACB
    L4_path.md:45–48.
* **L1.**
  * (a) Truth-free blocks hold ≥ p − 16s₀ ≥ K + 1 elements. FACB L2.3(i) uses ψ_U ≤ n (from Q_U ≤ yᵀy), w(k+1)/w(k) ≥ 1/(2p)
    and k < p, all valid here. For u = 0 the formula for c(U, l) correctly reduces to ρθ̄.
  * (b) I re-expanded the exchange factorisation: bracket = 2κ_cκ/(u + κ) + κ₁E. The bound |E| ≤ 2H̄ + 2H̄ + 2γ_uH̄ ≤ 6H̄
    holds, using γ_u ≤ 1/(1 + κ) since u ≥ 1.
  * (c) h″ < 0 if and only if (1 − A)κ < κ. The swap difference telescopes into ≥ 1 second difference with v ∈ [1, 15].
  * (d) |𝔅| ≥ (p − 16(J₀ + s₀))/16 contradicts liminf p/K > 16/15.
* **L2.**
  * (N2): t_n² = log n + 34 + 4√(log n + 30), so φ(t_n) is exactly as written. Φ̄(t) ≥ φ(t)/(2t) holds for t ≥ 1.
    |𝔅| ≥ n/33. The block minima are independent because the regular blocks are deterministic and ξ is iid. The mean is
    n^{1/2−o(1)}.
  * (i) (2p − K)/K ≤ 3 + 2/K, so Δ_K < ½log n + 1.2. This holds deterministically for every |T| = K.
  * (ii) t_l − t_j = z_l − z_j (the γ_KB_T term cancels). |t_j| = O(√nH̄) because κ_cκ/(K + κ) = O(1),
    γ_K|s_T| ≤ 1.7 and γ_Kλ₁Σϑ = O(1).
  * (iii) |x_T| ≤ 2. The count of nulls with |τ| > 3.5 is ≤ 0.28K + 0.14 < K − s₀. The chain V ≥ log n + 5 holds with
    about 12.7 units to spare (scratch §3). M_T ≥ ½(1 − 3n^{−1/3}).
  * L2.3: O* ∩ C₀ = ∅ by L1(d), and each move absorbs ≤ 1 element of O*.
  * L2.4: deletions ≤ max(0, i − N_n). So every scored set has size ≥ s₀ + 1, including N(C_a) at the cap. This matches the
    code, where the last scan completes before the `move_limit` exit (`v3_engine.h:407–410`).
* **L3.**
  * (E3): the Bernstein step gives exp(−3λ/8) with λ = 4log n. The union over an O(n√log n) grid → 0. Interpolation
    costs ≤ 2p/n ≤ 2.
  * (E4): the case split n − 1 − p ≥ n/5 versus p − K ≥ n/4 is exhaustive (0.3n − 1 ≥ n/4). The χ² lower tail plus the
    2^n union gives 2^{−n/8}.
  * (a) As in FACB L4.0(e): only (X), (E1) and M_T ≥ ¼ are used, and here M_T ≥ ½ − o(1).
  * (b) The ½h terms cancel through log p = ½h − L_n − log 2.
  * (c) Two-sided case: d_T ≤ H̄ and γ_{k−1} ≤ 1/(s₀ + 1 + κ_∞), which gives c_D. One-sided case: the maximum over m ≥ 1
    of (s₀ + κ)²/((m + s₀ − 1 + κ)(m + s₀ + κ)) is t/(t + 1).
  * (d) The layer-cake identity S₊ = dU₊(x + d) + ∫U₊ holds. ∫_a^∞Φ̄ = φ(a) − aΦ̄(a) ≤ φ(a), and Mills' ratio requires
    a > 1, which holds. In (d-i) the d² error terms are O(1). In (d-ii), 4C_Mc₀ = ε/2.
  * Zero or small d_T is dispatched first, through Δ_k − 2C_M.
* **L3.4.**
  * The endpoint is proved before any budget is used.
  * Phase A stays at size K. The count is (K log n + Cn)/(c₃n).
  * Main phase: log C(2p − 1, K) ≤ K(1 + log 4) + o(K). The ratio K/(1 − 2ε) is ≤ (1 + 6ε)K for ε < 1/3.
  * Remainder: ≤ 2(m_e + 1)/(c_D − ε) moves, even if additions leave the small region.
  * With ε = min(δ/12, c_D/4), (1 + δ/2)K + O(log²n) ≤ (1 + δ)K.
* **L4.**
  * (H0) with A = 1 because p ≤ n − 1 ≤ n¹.
  * [OP] is cap-free.
  * The pathwise inclusion goes in the correct direction.
  * The third example rule is ≥ ⌈17|S̃₀|/16⌉ deterministically under (PK), and ≤ ℓ_n + 2K because p ≤ 2K + 1.
  * The archive charge is affine in the scan count with a nonnegative intercept, so the ratio bound r ≤ 2 holds.

**2. Hypotheses used = hypotheses stated: PASS.**
* (P1)(a)(b) use (PK′) and blocks ≤ 16 only; (c)(d) also use (PK) and (PB).
* (P2) uses (PK) through (N1), p → ∞ and L1(d), and (PB) through (N2) and L1(c)(d).
* (P3) uses (PK′) through L1(a), and through L3 (p > K, p ≤ n − 1). Blocks enter only through L1(a), and every ϑ_r ≠ 0 is
  used in L3(a)/(e).
* (P4)(iii) states (α) and (β), the allocation, total tier-1 fallback and the plumbing premise.
* No (TK) and no sign-alignment hypothesis is used anywhere.

**3. No hidden assumptions: PASS.**
* Events: E^S, E^N, E1–E4 and 𝒟_n are explicit.
* Uniformity: (E3) holds for all real t, (E4) for all T ∈ 𝒯, and L2.2/L3 for every T. Data-dependent evaluation points
  (t = a, T = C_i) are therefore covered.
* Ties: L2.2's maximum is attained only by swaps. L3 uses only "chosen gain ≥ best deletion". 𝒟_n handles ξ ties.
* Cap-rule evaluation is covered by (β).
* Imports are re-read for p ≤ n − 1, and the two p ≤ n/2 steps are excluded.
* The R08 G2 overreach is gone; REPORT §6 now states its model-count restriction.
* The one remaining inaccuracy is in an explicitly labelled heuristic, REPORT §5 (F1). It is not an exported property and
  not a step of L0–L4, so it does not fail this gate (required fix 1).

**4. Citations and statuses: PASS.**
* The registry rerun gives 38 checked, 0 misses.
* I checked these statuses by hand: [OP] "PROVED (by this seat, unchecked)" (W1-GEN STATEMENT:169); GEN "PROVED-CHECKED"
  (W1-GEN REPORT:20); Lemma CAP "PROVED (by this seat)", council round 3 (s7:64); FACB R03/R04/R05
  VERIFIED-WITH-AMENDMENTS; A1, A2 and A4 as quoted.
* L0–L4 remain "PROVED (by this seat, unchecked)" together with their lemma-check verdicts. No status is upgraded.

**5. Constants and rates: PASS.**
* L_nH̄ = O(√log n · log log n) = o(log n).
* The O(log log n) terms are dominated by ε log n.
* Chain: c_D > 0 (s₀ ≥ 1, κ_∞ > 0) → ε < c_D/2 → c₀ = ε/(8C_M) → n^{1−c₀}.
* m_e = ⌈log²n⌉ ≫ 12H̄ log n.
* c₃, c₄, c₅ and β′ ∈ (β, ½) are consistent.
* The numerical constants (1.2, 2, 2.39, 2.4, 6ε) all check. Scratch §3 shows that ½(1 − 3n^{−1/3})(log n + 5) ≥ ½log n + 2
  needs n beyond about 10⁵. That is a finite-n onset, which is out of scope.

**6. Fidelity to the coded method: PASS.**
* Loop rule (`v3_engine.h:385–413`): the full scan of the centre, then the best neighbour (lexicographic ties), then a
  strict-improvement test, then the `move_limit` exit once `moves >= ell`, otherwise a move. This gives the prefix property
  and scored set {C₀} ∪ ⋃_{i ≤ min(a, m*)} N(C_i).
* Additions are skipped at size ≥ K, swaps are always scanned, and q(p) = p + p²/4.
* The MR1 cap is computed after `start_mode` with a long-long range check (`v3_core.cpp:473–474`).
* `v3_run.R:101` collapses every non-legacy value. The Boolean is at `v3_core.cpp:394/404`. The preflight scan count
  `b$ell + K + 1` and the archive formula are at `v3_fit.R:44–45`. Both preflight call sites are at `v3_fit.R:115, 145`.
* Each of these matches L4.2 and METHOD_REQUIREMENTS.
* LS0 runs only on a completed run and after the final local search, followed by a GUARD-W check (`v3_core.cpp:466–480`).
  This is consistent with the [OP]/delivery reading.

## Required fixes

**1 (minor; REPORT §5 F1 heuristic wording; non-blocking).** REPORT:78–80 says the p ≫ n NEG mechanism needs "excluded
nulls whose residual statistic exceeds (1 + ε)log n — for p ≫ n there are many more such nulls."

The relevant threshold is not (1 + ε)log n. At size K a swap must beat the best deletion, whose gain is close to
Δ_K = ½log n + log((2p − K)/K) + o(1). That threshold rises with p. With M_T ≈ ½ (so M_Tτ² > Δ_K means τ² > 2Δ_K), the
expected number of qualifying nulls is about pΦ̄(√(2Δ_K)) ≈ K/(2√n)/polylog. This is n^{1/2−o(1)} whatever p is, and it is
not increasing in p. Scratch §4: at n = 10⁶ the count falls from ≈ 31 (p = n − 1) to ≈ 12 (p = n³).

The heuristic conclusion still stands: polynomially many qualifying nulls exist, far more than O(log n), so MR1 should
still fail. The stated reason does not.

**Fix:** replace "(1 + ε)log n … many more such nulls" with "a swap gain exceeding Δ_K = ½log n + log((2p − K)/K) + o(1).
With M_T ≈ ½ the expected number is ≈ K n^{−1/2}/polylog regardless of p, still ≫ log n". Note also that M_T and the
centre are not one-dimensional for iid rows. Wording only; no claim changes.

## Optional suggestions

1. **REPORT placeholders.** Fill REPORT:18, 64 and 74 ("[to be filled]") at the end of the council.
2. **Range check in the plumbing (refines R09-M1).** P(no output) = 0 "for every admissible n ≥ 3" needs the
   `LS0 move cap out of range` stop at `v3_core.cpp:474` to be unreachable under the new rule. With the validated base cap
   ≤ 10⁶, ℓ_n + 2K < INT_MAX requires K below about 1.07·10⁹. MACH or the allocation premise certainly implies this, since
   such n × p data could not be held. Still, one clause in METHOD_REQUIREMENTS ("the range check must remain unreachable
   on admissible inputs: compute in 64-bit and note ℓ_n + 2K ≤ INT_MAX under MACH") would close the gap explicitly.
3. **L2.2(iii) slack.** The final step ½(1 − 3n^{−1/3})(log n + 5) ≥ ½log n + 2 has a late onset, while V carries about
   12.7 spare units. Using V ≥ log n + 15 would make the step hold for moderate n. This is cosmetic, because onsets are out
   of scope.
4. **G1 remark.** The generic proof is one line: the Schur ratio ≤ n + 1 because (G_U + I)⁻¹ ⪯ (G_U + I/(n + 1))⁻¹.
   Adding it to REPORT §6 would make G1 self-contained for W2-UNI.

## Summary

The package is correct and honestly scoped.
* Theorem NEG is a clean static argument plus counting. Saturation and the within-block order (L1) leave n^{1/2−o(1)}
  regular-block minima outside the start. Size-K swaps that bring them in beat every deletion (L2.2). The prefix property
  then keeps S₀ unscored for any cap ≤ |S̃₀| − s₀ − 2 + n^β.
* Theorem PATH gives uniform deletion gains on the lattice above S₀ (centring identity, two-sided tail counts, the
  p ≤ n − 1 residual floor and the small-energy multiplier). The CS potential budget turns these into m* ≤ (1 + δ)K. The
  endpoint is established before the budget uses F(S₀).
* The assembly and the cost statements are restricted correctly to cheaply evaluated rules with a ≤ ℓ_n + 2K, and to the
  plumbed method.
* All round-1 fixes are in place, and the three REPORT repairs requested by R08 are mathematically correct. I verified the
  generic G1 independently.
* The narrowing is declared in STATEMENT §0/§5 and REPORT flags 2–3: the exact-Gram stage only, frontiers F1/F2/F2′, and
  (P6) numerical and pending.
* The only new item is a mis-stated reason inside a labelled p ≫ n heuristic.

Score 9.2.
