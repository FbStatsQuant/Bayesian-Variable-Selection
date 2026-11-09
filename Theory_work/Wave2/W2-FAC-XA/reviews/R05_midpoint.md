# R05 — Independent midpoint review of W2-FAC-XA (fresh Claude Opus 5.5 seat)

**VERDICT: CONTINUE, with a required change of route.** The key lemma X2 is **not proved**, so this review cannot
stand in for a midpoint taken after the key lemma. The lead should log that, and HQ decides whether a fresh midpoint
is needed once X2 closes.

Inputs read: STATEMENT.md (locked v1); lemmas L1_geometry, L2_robust_path_attempt, L3_fuzzy_attempt (R04-amended
version), L4_score_transfer (R04-amended version); Wave1/Wave2 PROTOCOL midpoint and stop rules; FAC-B STATEMENT
§§1–4, FAC-B L1.3–L1.5 and L4.3–L4.4 (dependencies only). I did not read LOG, CHECKPOINT, REPORT, PLAN, dispositions,
earlier reviews or W2-FAC-X. My scratch work is in reviews/R05_scratch/ (R05_relnorm.py, R05_order.py and their
*_out.json). No git, no subagents, no outside contact.

## 1. Why CONTINUE (summary)

1. I found **no counterexample to the target** (C1, every p ≤ n^a, a < 1/4). L2's three-point example and L3's
   rational 10-point example refute only the exact interval invariant and the sharp hull-depth invariant. They do
   not refute X2. Every safety margin is Θ(log n), and the perturbation that has to be absorbed tends to zero at a
   polynomial rate.
2. **The ingredients already proved are sound** (checked line by line, §2). These are L1a–c, L4 (ST), and L2's
   finite certificate, AA, BAL, FG, END/MAJ/MG and its conditional §5 theorem.
3. **The current plan targets the wrong obstruction.** L3 §5 treats the open problem as "band width O(ε log p)
   rather than ε·p/m". That loss is **forced only by the gain→coordinate conversion ε = sqrt(20ζ)**. L1c already
   gives a much smaller tolerance at the coordinate level. Combined with a relative-norm rate (numerically ≈ 2√(p/n),
   §3), **L3's polynomial bound (1), as proved, is already enough for a < 1/4**. With L1a's crude rate it is enough
   for a < 1/5, which still beats FAC-A's 1/6 baseline for iid CS. The logarithmic-width question only matters for
   a ≥ 1/4.
4. What remains (§4) is a list of specific lemmas. Most are standard. One is a moderate new geometric step (a
   midpoint/straddle bound for the shadow gap). None has been shown false.

## 2. Lemma-by-lemma check (attempting to break each one)

**L1 (proved; holds).**
- L1a: the Wishart second moments, the Chebyshev bound on {S_ii ∈ [1/2, 3/2]}, the Lipschitz constant 2 and the
  explicit 80p(p−1)/d bound all check.
- L1b: B'B = A'(I+E)A = R. The directed gaps are e and e/sqrt(1−e), the sum is ≤ 3e, and the
  residual-direction bound is 8e/sqrt(c). Correct.
- L1c: O'O = I, CO = O, and Z_X(T,j) = q_B(T,j)'z exactly. (z, r) is independent of the entire raw design. Correct.
- Note: λ_min(R) ≥ (1−e)c, so L4's "(1−e)^2" is conservative but valid.

**L4 (deterministic, conditional; holds).**
- The expansion Q^raw = RSS + (V−RSS)/(n+1) + J with 0 ≤ J ≤ CV/n² is exact.
- |V_B − V_A| ≤ Cen, |RSS_B − RSS_A| ≤ 3σ²e‖z‖², and |D_M| ≤ tr G_T^{-1} ≤ Cp/n.
- The representation bridge is correct, with y'y = n−1 = d.
- Scope is correctly limited to T ⊇ S0. Truth-out moves and start tables are outside it, as the lemma states.

**L2 (conditional; the stated content holds).**
- AA's constant 20, BAL, FG, END/MAJ/MG and the swap convexity bound all check.
- Hidden conservatism (not an error): the margins in §5 drop the prior term log[(2p−k)/k] from Δ_k (FAC-B L1.3).
  At the end phase this term is ≈ a·log n, so with it the end-phase deletion margin is (.5 − a)·log n, not
  (.5 − 2a)·log n. The 1/4 in L2 therefore comes from bookkeeping, not from the geometry. FAC-B's exact path holds
  for p ≤ n/2. This matters for the research ambition (exponents above 1/4), not for the lock.
- Gap: UP as stated includes truth-out moves. L4 does not cover them. A direct order-n negativity lemma on the
  actual design is needed (easy: the RSS increase is ≥ dθ_j²c(1−e) − O(sqrt(n·pL_n))). Do not cite L4 for it.

**L3 (holds; scope as amended by R04).**
- I re-derived (2), the "drift that increases |e| has |δ| ≤ ε" case, the recursion (q−1)|e'| ≤ q|e| + ε, the
  identity q_t·e_t = −Σδ_r, and the shadow certificate (drift |v−h|/(q−1) < |v−h| needs q > 2, which holds because
  c > 1 and m ≥ 2). Bound (1) follows because r/q_r increases in r.
- Note: (1) also holds with a step-dependent ε_r (q_t|e_t| ≤ Σ_{r<t} ε_r), which the route below can use.
- §5's rate accounting is valid only for the gain-level route. It is superseded below.

## 3. Main finding: the logarithmic propagation gap does not block a < 1/4

**(R1) Ordering transfer at the coordinate level (proposed lemma OT; must be proved and reviewed).**
- Setup: T ⊇ S0 and j is a null in T. Because S0 ⊆ T∖j, the signal lies in span X_{T∖j}. Therefore, exactly,
  RSS_B(T∖j) − RSS_B(T) = σ²·Z_B(T∖j, j)².
- Hence, writing W_B(T) for the L4 denominator, the actual deletion gain is
  Φ_T(Z²) := Δ_k − ν·log(1 + σ²(n/(n+1))·Z²/W_B(T)), plus ω_{T,j}.
  - Φ_T is common to every j at fixed T and strictly decreasing.
  - ω_{T,j} collects the J and D differences across neighbours. It is O(1/n): tr G_T^{-1} − tr G_{T∖j}^{-1} ≤
    (1 + 1/(c(1−e)))/(dc(1−e)), and the J differences are ≤ C/n.
- Numerical check (R05_order: iid CS, n = 3000, p = 60, |T| = 42, 5 seeds):
  - the production D0 deletion gains are ordered exactly as Z²;
  - the fit c0 − ν·log(1 + c1·Z²) has maximum residual 1.9e-4 to 5.8e-4 (1/n = 3.3e-4), against gain ranges 1.7–4.7.
- By L1c, Z_B = Z_A + O(e‖z‖/sqrt(c)) uniformly. For a null, Z_A(T∖j, j) = λ_k·(ξ_j − x_T), where λ_k depends only
  on k (FAC-B L1.3–L1.4). That λ_k is bounded away from 0 and ∞ is a short check the lead must write out.
- Conclusion: the actual best null deletion is an **ε_n-approximate nearest deletion in the fixed reference
  coordinates**, with ε_n = C(e‖z‖ + n^{-1/2}). This replaces ε = sqrt(20ζ).

**(R2) A relative-norm rate (proposed lemma RN; must be proved).**
- Claim: e = ‖Σ^{-1/2}(R − Σ)Σ^{-1/2}‖ = O_P(sqrt(p/n)) for the centered, sample-sd-standardized R.
- Numerical check (R05_relnorm):
  - e/sqrt(p/n) ∈ [1.92, 2.49] for CS (ρ = .5) and for one-factor loadings drawn from U(.3, .9), with n ∈ {2000, 8000},
    p ∈ {25, 100, 400} and 3 seeds;
  - the absolute norm sits at 0.35–0.65 × p/√n, confirming R01's warning about the absolute norm.
- Proof obligation: the standardization term Σ^{1/2}ΔΣ^{-1/2}, with Δ = D^{-1/2} − I, has a spike component of
  size sqrt(λ_max/λ_min)·‖(I−P_1)Δ1‖/√p. It is O(sqrt(p/n)) only because of how the common factor enters S_jj − 1;
  this must be shown, not assumed. This is a relative norm, so it complies with the norm discipline.

**Arithmetic.** Use ε_n = O(p·sqrt(L_n)/√n) under RN, or O(p^{3/2}·sqrt(L_n)/√n) under L1a alone.
- L3 (1) gives a band width w_m ≤ 3pε_n/m for m ≤ m0.
- Shadow–actual centre gap: |h − x| ≤ pε_n/m.
- End-entry band: m₁·w ≤ 3pε_n.
- All three tend to zero polynomially exactly when **p²/√n → 0, i.e. a < 1/4 under RN**, or a < 1/5 under L1a alone.
- Margin comparisons between deletions, additions and swaps keep the gain-level L4 bound ζ = O(e·pL_n), which is
  far below Θ(log n).

## 4. Exact open conditions preventing assembly (priority order)

- **O1 (key; moderate, new).** Bulk fuzzy geometry on every prefix of approximate deletions:
  - the shadow gap (a, b) straddles x;
  - the asymmetry satisfies |a + b − 2x| ≤ 2ε_b·H. This is the analogue of FAC-B L4.1(iv),
    Δ_i ≤ max(Δ_{i−1}, g + 2d/(q−1)), with an extra term of O(E_t + |e_t|);
  - straddling also holds for one-sided configurations.
  
  Then BAL (with r below) gives |x| ≤ ε_b·H, and FG gives the outside-distance envelope.
  - Requirement: an exception count r = O(1) per band. This follows from a scan-statistic bound: no window of width
    w_m inside the current tail holds more than k0 nulls, where k0 is a fixed constant, because the expected
    occupancy is ≤ m·H·w_m = o(1) polynomially.
  - Do **not** use a generic "+C log n" occupancy term: at m ~ m₁ = O(L_n) it is not o(m).
- **O2 (end entry; short).**
  - Retained points lie outside the open gap (L3 certificate), and deleted points lie within E of [a, b]. So
    #{ξ ≥ b + E} ≤ m₁, hence b ≥ H̄ − δ_e − E, using FAC-B E6 on each side separately.
  - So the END magnitude premise holds with w = δ_e + E and m₁·w = O(L_n) + 3pε_n = o(H̄).
  - The entry imbalance follows from |x| ≤ 2ε_b·H exactly as in FAC-B L4.4.
- **O3.** Prove RN for C1 (and for C2 if C2 is pursued). Otherwise state results at a < 1/5 using L1a.
- **O4.** Prove OT (§3, R1), including that λ_k is bounded and the O(1/n) bound on ω.
- **O5.** Truth-out negativity on the actual design (order n), so that UP is never needed for truth moves.
- **O6.** X1 under iid rows. This involves block tables m(U)/m(∅) on models with |U| ≤ 16 that do not contain S0,
  which L4 does not cover. Sample partial covariances deviate from c(U, l) by O_P(sqrt(log p/n)), uniformly over
  ≤ p·2^16 pairs. All table separations are order n under (FS), so the risk is low. Condition on the X-measurable
  partition.
- **O7.** X3/X4 and the transfer obligation.
  - The noise (z, r) is independent of the whole design, so the A-world is, conditional on X, exactly an exact-Gram
    CS problem.
  - FAC-B's E_n events are noise-only. The lead must verify that their probability bounds are uniform over block
    partitions (|N0| ≤ 15).
  - Then construct the design event A_n = {e ≤ e_n, eigenvalue floor} ∩ residual events.
  - Verify Lemma S inputs and (H0) for random R. Delivery uses the pathwise discovery inclusion, not D_n.

## 5. Counterexamples and hidden assumptions

- **None against X1–X4.**
- **Hidden or misattributed points to fix in the text:**
  - L2's 1/4 is a by-product of conservative margins (the prior term is dropped).
  - L3 §5's a < 1/8 reflects ε = sqrt(ζ), not geometry.
  - L2's UP must exclude truth-out moves and handle them by O5.
  - L1c's reference design X_A = XB^{-1}A depends on X. FAC-B results transfer only because the score law depends on
    the Gram alone, so the lead must state that FAC-B's event bounds are design-free.
- **Ceiling of this route:** it reaches exactly a < 1/4 (from p·ε_n → 0). Going beyond needs either L3's open
  O(ε polylog) width or a sharper sup_T |Z_B − Z_A| than the worst-case ‖z‖ factor.

## 6. C2

- L1, L4, OT and RN are factor-agnostic: they need only the eigenvalue floor 1 − λ_hi².
- What C2 lacks is an **exact-Gram path lemma** for heterogeneous loadings (C2-E). L2 §7 shows that the ordering is
  weighted and depends on leverage, and no BAL or majority analogue exists. C2 is not on a viable route with the
  current material.
- Finish C1 first, as the statement's own ordering says. C2 should end as an X5-style precise obstruction unless
  C2-E gets its own proof.

## 7. What remains, and the partial package if geometry does not close

- **Remaining for the full C1 claim:** O1–O7, each with falsification numerics and a fresh review, before the sweep
  and the council.
- **If O1 fails after the third reviewed attempt,** the protocol's STUCK rule applies. Count the reformulated
  polynomial-width lemma as a new attempt; L2 and L3 targeted the old O(ε log p) form. Report the strongest
  package, labelled honestly:
  1. **PROVED:** L1 and a "Uniform score transfer" proposition (L1 + L4 + O5) for iid one-factor rows with an
     eigenvalue floor and p ≤ n^a, a < 1/4 (a < 1/3 once RN is proved).
  2. **CONDITIONAL:** L2 §5's path theorem, plus OT/RN if proved, stated with O1 as an **explicit named hypothesis**.
  3. **X5 frontier:** the exact remaining obstruction (O1), the L3 counterexample scope, and the 1/4 ceiling of this
     route.
- **No automatic upgrades:**
  - L2 §5 stays conditional until O1 and O4 are proved and reviewed.
  - L4's prospective rate is not a theorem until L1/RN plus the residual events are assembled.
  - D_n → 0 must never be used to infer discovery.
  - Statuses must be quoted verbatim.

## 8. Evidence files (R05 scratch)

- `reviews/R05_scratch/R05_relnorm.py`, `R05_relnorm_out.json`: relative versus absolute Gram deviation.
- `reviews/R05_scratch/R05_order.py`, `R05_order_out.json`: monotonicity of production deletion gains in Z_B².

These are falsification checks, not proofs.
