# R04: cross-family key-lemma check of L2 (Claude Opus 5.5 review seat)

Reviewer: Claude Opus 5.5, continuous lemma review (not the midpoint review or the council). Date: 2026-11-09.
Inputs read: Wave2/PROTOCOL.md, Wave1C/PROTOCOL.md, Wave1/PROTOCOL.md; W2-FAC-PKA STATEMENT.md (v2), SINGLETON_TARGET.md (v2),
lemmas/L2_singleton_start_swaps.md; numerics n3_singletons.py / N3_singletons.jsonl, n4_singleton_controls.py /
N4_singleton_controls.json, and the source imports n1_exact_grid.py and W2-FAC-B/numerics/cs_core.py; production code
Scripts/SMC_BVS/core/cpp/{v3_core.cpp, v3_engine.h, v3_start.h, v3_score.h}, read-only.
Not read: LOG, REPORT, CHECKPOINT, or any earlier reviewer conclusion. L2 was checked as one self-contained lemma. I
rederived the score identities myself and relied on no L0/L1 status.
Scratch: reviews/R04_scratch/ (fastcs.py, check1_real_design.py → check1_out.json, check2_early.py → check2_out.json /
check2_log.txt, check3_edges.py → check3_out.json / check3_log.txt). All runs used `C:/Users/felip/anaconda3/python.exe -B`.
The independent simulator `fastcs.py` is my own code; it does not import cs_core.

## VERDICT: VERIFIED-WITH-AMENDMENTS

Every step of L2 holds under the stated hypotheses: G, singleton blocks, rho=1/2, sigma=1, p=floor(cn) with fixed
c in (1/2,1), K=floor(n/2), s0 in {1,2}, all truth coefficients 1, and the method premises (EX-A/e4' exact start
maximizer, complete scans, OP-LS0). I found no false step, no counterexample and no constant that fails to track. The
amendments below are presentational or citation gaps. None changes a conclusion. Asymptotic scope is respected
throughout.

The conclusions verified are:
- **S1 (start).** With probability → 1, the start has size K, contains S0, and its nulls are exactly the K−s0 largest
  null xi_j. The mean of the retained nulls converges in probability to mu=phi(t)/q, where q=1/(2c) and t=Phi^-1(1−q).
- **S2 (early path).** For every fixed C>0, with probability → 1, the first ceil(C log n) moves of the uncapped LS0
  path are strictly improving null-null swaps.
- **Size-only consequence.** With C>1/log 2, P(S0 not in N_LS0) → 1 under cap a=ell+K.
- **Scope.** For s0=1, D_n=0 through table ingestion. For s0=2, SMC and final-search discovery are not decided. The
  singleton partition is NONPRODUCTION, so the result refutes only a uniform-partition guarantee that LS0 alone
  discovers S0 under the original cap.

## Line-by-line check

### §1 Gaussian representation
- e=Cε. X'X=hΣ and CX=X give Cov(X'e/√h)=Σ. P_X ≤ C because col(X) ⊥ 1, so P_X e and (C−P_X)e are independent.
  rank X=p because Σ is positive definite and p ≤ n−1, so r ~ χ²_{n−1−p}. The scores depend on the data only through
  z=X'y and y'y=h. In turn, z and s are functions of (g, r):
  - s² = [hθ'Σθ + 2√h θ'g + g'Σ⁻¹g + r]/h;
  - z = (hΣθ + √h g)/s.
  I checked both formulas on real exact-CS designs. Relative errors were 5e-16 for s² and 2e-15 for z
  (check1_out.json, `s2rep`, `zrep`). The closed form Σ⁻¹ = 2(I − J/(p+1)) also checked.
- The decomposition z_j = b + d xi_j + f θ_j holds with b=(h s0/2+√(h/2)η)/s, d=√(h/2)/s and f=h/(2s), because
  (Σθ)_j = θ_j/2 + s0/2. Correct.
- Events: P(max_{j≤p}|xi_j| > 2√log n) ≤ 2p n^{-2} → 0, and s² → v = s0/2 + s0²/2 + 1. On these events every null z is
  positive (b is of order n) and every truth z exceeds every null z (gap f ≍ n against noise O(√(n log n))). Correct.

### §2 Exact singleton start
- For a singleton j: G_j=h, H_j=(n+1)h+1 and quad_j = z_j²/H_j. Q_j is strictly decreasing in z_j², so log BF_j is
  strictly increasing in z_j². Correct.
- n⁻¹ log BF_j → −½ log(1 − a_j²/v), with a_j = s0/2 (null) or (s0+1)/2 (truth). Here v − a_j² ≥ 1, and
  z_j/h → a_j/s uniformly at rate √(log n/n). Correct.
- The size increment log w(k+1)/w(k) = log((k+1)/(2p−k)) ≥ −log(2p). The minimum BF grows like b_* n, so every
  maximizer has size K. Numerically, n⁻¹·min log BF was 0.056–0.13 at n=4000 (check2_out.json, `min_logBF_over_n`).
- Selection: top K of z², which equals top K of z, which gives truths plus the top K−s0 null xi. Ties have
  probability 0. Verified:
  - against brute-force maximization of γ0 on real X at n=40 (check1, `topz`=true);
  - in all 94 large-n runs, n=1000–10^6 (`start_ok`=true).
- Trimmed mean: q_n=(K−s0)/(p−s0) → 1/(2c) ∈ (1/2,1), so t is finite and negative, and mu=phi(t)/q > 0 > t. The
  quantile sandwich argument is standard. Numerically, x_T0 matched mu to 3 decimals at n ≥ 10^5 for c ∈
  {.51,.55,.75,.95,.99}.
- Amendment M1 applies to the LLN wording (see below).

### §3 Score identities, rederived independently
- For CS with ρ=1/2: G_U = h(I+J)/2, so H_U = αI + βJ with α=(n²−1)/2+1 and β=(n²−1)/2, and G_U+I = α'I + β'J. The
  determinant identity det(aI+bJ) = a^{k−1}(a+kb) gives L_k. Sherman–Morrison gives H⁻¹ = α⁻¹(I − γ_k J). Verified on
  real X: L_k error 9e-14, closed-form F relative error 1e-14 (check1, `Lk`, `Fclosed`).
- **Deletion identity.** Write γ' = γ_{k−1} = γ/(1−γ), so γ'−γ = γγ'. Then
  −z² − γ'(B−z)² + γB² = −(1+γ')(z−γB)².
  This holds exactly; numerical relative error 1e-14 (check1, `del_id`).
- **Swap identity.** z_l² − z_j² − 2γB(z_l−z_j) = t_l² − t_j², and −γ(z_l−z_j)² = −γ(t_l−t_j)². Correct; numerical
  relative error 1e-14 (check1, `swap_id`).
- **Deletion gain bound.** The deletion gain is log((2p−k)/k) + (L_k − L_{k−1})/2 − ν·log(ψ_{T−j}/ψ_T), and the last
  term is ≤ 0 since Q_{T−j} ≥ Q_T.
  - At k=K: log(α/α') = log((n²+1)/(n+1)) = log n + O(1/n), and the two ratio terms cancel to O(1/n²). So
    Δ_K = log((2p−K)/K) + ½ log n + O(1/n).
  - Numerically, the maximal deletion gain equals Δ_K to 1e-8: the bound is attained by the null with t_j ≈ 0.
    Δ_K/log n = .526, .520, .516, .513 at n = 10³, 10⁴, 10⁵, 10⁶ for c=.55 (check2_out.json).
- **Centre.** t_j = d(xi_j − x_T) + f θ_j. The offset is [√(h/2)·s0 + ηα]/(α + kβ) = O((|η|+1)/k), because
  bα − βf s0 = h s0(α−β)/(2s) + √(h/2)ηα/s and α−β=1. Correct.

### §4 Uniform early candidate supply
- The family of all T reachable by ≤ L null-null swaps works deterministically on the max-event. Each swap changes
  Σξ by ≤ 4√log n and γ_K ≈ 2/n, so the drift is O(log^{3/2} n / n). Numerically the maximum drift over the first L
  moves was 0.0002 at n=10⁶ and 0.002 at n=10⁵ (check2/check3).
- **Near-centre supply.** There are Θ(n) nulls in [mu−δ, mu+δ], all above the threshold. Removing ≤ L of them leaves
  a null j with |ξ_j − x_T| ≤ 2δ, using |x_T − mu| ≤ δ eventually (see M3). Correct.
- **Tail supply.** Φ(−a_n) ~ n^{−3/4}/(√(2π)·a_n), so E[count] ~ (c/√(3π))·n^{1/4}/√log n, which grows faster than
  2L = O(log n). Chebyshev with Var ≤ mean gives count ≥ 2L with probability → 1. All tail nulls lie outside T0
  because the threshold tends to a finite t. At most L of them enter T. Correct.
- **V bound.** V_jl ≥ (a_n − |x_T|)² − 4δ² − γ_K(4√log n + O(1))² ≥ 1.4 log n eventually. Correct.

### §5 Residual control and the strict preference for null swaps
- Q_T − RSS_T/s² = z'(G⁻¹ − nH⁻¹)z ≥ 0. The relative eigen-factor is (g+1)/((n+1)g+1) ≤ 1/(n+1) + 1/((n+1)g), with
  g ≥ h/2 because λ_min(Σ_T) = 1/2. Together with z'G⁻¹z ≤ y'y = h this gives a bound ≤ 1 + 2/(n−1). Correct.
  - RSS_T = ‖(I−P_T)e‖² ≤ ‖e‖² holds when S0 ⊆ T.
  - Every sampled set containing S0 (from 240 random sets on real X) gave zero violations of 0 ≤ Q − RSS/s² ≤ 1+2/(n−1) (check1, `QRSS_viol`=0).
- **Multiplier.** M_T = ν n d²/(αψ_T) = ν n h/(2α·s²ψ_T), and s²ψ_T ≤ ‖e‖² + O(1), so M_T ≥ ½ − o(1). The observed
  minimum of M_T over the first L moves was 0.57–0.91 across all runs and never below 0.5 (`min_M`).
- **Swap gain.** The gain is −ν log(1−x) ≥ νx = M_T·V_jl ≥ (.7 − o(1)) log n. The argument of the log is positive
  because it equals ψ_{T−j+l}/ψ_T, and Q_U ≥ y'y/(n+1) > 0 (needs G_U nonsingular; see M6).
  - The margin over deletions is about 0.2 log n − log(4c−1) − o(1) > 0 eventually.
  - Observed: (best swap gain − best other move gain) was positive at every one of the first L steps for all n ≥ 2000
    runs. At n=10⁶ it was 5.3–7.5 nats (check2/check3, `min_swap_minus_other`).
- **Truth-out moves.** t_j = f + O(√(n log n)) for a truth and t_l = O(√(n log n)) for an outside null, so
  t_l² − t_j² − γ(·)² < 0. Observed: the maximal truth-out gain was −2.4e5 nats at n=10⁶ and −190 nats even at
  n=1000 (`max_truthout_gain`). Additions are infeasible at |S|=K: production excludes additions beyond K
  (v3_engine.h:370 comment and the add check in local_search; D.K=min(p,n/2) at v3_score.h:40).
- **Induction.** Each T_i (i < L) lies in the §4 family, the best move is a strictly improving null-null swap, and
  T_{i+1} stays in the family. The conclusion holds for every lexicographic tie choice. Correct.
- My exact simulator, run on its own (z from the representation, neighborhood search reduced to O(p) by the convexity
  of the swap quad in z_l):
  - matches a brute-force production-rule LS0 on real X move-for-move, for 4 paths of up to 21 moves
    (check1, `identical`=true);
  - gives all first L moves as null-null swaps in 76/76 runs with n ∈ {2000, 4000, 10⁴, 10⁵, 10⁶},
    c ∈ {.51,.55,.75,.95,.99} and s0 ∈ {1,2}, with L = max(ell+s0+2, ceil((1/log 2 + .05) log n)).

### §6 Size-only miss consequence
- Code check. LS0 calls start_mode at v3_core.cpp:469 and sets cap=ls0_ell+|mode| at :473–475. local_search makes at
  most `ell` moves and then one further scan (v3_engine.h:408–409), so the scanned centres are exactly C_0..C_a and a
  move-limit return is a neighbor of C_a. The objective is q.F = logprior[k] + logm (v3_engine.h:97). So N_LS0 with
  t ≤ min(a, m*) is exactly the LS0 score set.
- Size argument. ell = ceil(log₂(n+p+1)) < log n/log 2 + 2, so C > 1/log 2 gives L ≥ L0 = ell+s0+2 eventually. Every
  scanned centre then has size ≥ K − (a − L0) = s0+2, and every neighbor has size ≥ s0+1. Correct.
- Full uncapped paths at n=1000–4000 with c ∈ {.55,.75,.95}: the first scan with S0 in its neighborhood came after the
  cap a=ell+K in 28/30 runs (check2, `LS0_scores_S0`). The two exceptions are at n=1000, c=.55; see the observations.
- Table ingestion for s0=1 checked. ingest_tables is at v3_core.cpp:372 and is called at :408. For singleton blocks
  the table entry is computed whenever |U| ≤ K (v3_start.h:92). Every computed entry is a ledger event, so S0={0} is
  always scored and D_n=0, as long as a NumericalFailure is a stop, i.e. no output. Correct as stated.

## Issues and amendments (none blocking)

- **M1 (§2, wording).** The ξ vector has a new law for each n (a triangular array). "iid LLN" should read "weak LLN
  for row-iid triangular arrays (Chebyshev)". Alternatively, couple all n on one iid sequence ξ_1, ξ_2, …, which is
  legitimate because only the law at each n matters. Apply the same fix to the empirical-quantile convergence.
- **M2 (premises, citations).** The lemma calls the LS0 scan rules premises but cites no code. Add the following:
  - v3_engine.h:370–378 (rules);
  - v3_engine.h:408–409 (strict improvement; ell moves then one further scan);
  - v3_engine.h:97 (the objective is F = log prior + log m, not γ0);
  - v3_core.cpp:469–475 (start_mode, cap = ell + |mode|);
  - v3_score.h:40 (K=min(p, floor(n/2))).

  The fact that LS0 maximizes F and not γ0 is essential to S2. Under γ0 the singleton start would already be
  stationary.
- **M3 (§4, implicit event).** State explicitly that the events |x_T0 − mu| ≤ δ/2 and sup-drift ≤ δ/2 hold with
  probability → 1. Together they give |x_T − mu| ≤ δ, which is what the near-centre supply step uses.
- **M4 (§3, constant).** Write Δ_K = log((2p−K)/K) + ½ log n + O(1/n), where log((2p−K)/K) → log(4c−1) ∈ (0, log 3).
  The O(1) then depends only on c, and the final margin of about 0.2 log n − log(4c−1) is explicit.
- **M5 (§1).** Add one line: r is independent of g because P_X ≤ C (col X ⊥ 1), and rank X = p because Σ ≻ 0 and
  p ≤ n−1.
- **M6 (§5).** Q_U ≥ y'y/(n+1) needs G_U nonsingular. This holds for every |U| ≤ p since Σ ≻ 0; state it.
- **M7 (§6, scope; keep).** The scope paragraph is accurate. Keep "NONPRODUCTION singleton partition", "s0=2
  SMC/final-search not decided" and "s0=1: the full table scores the truth", and do not strengthen any of them.
  STATEMENT allows partitions with blocks of size ≤ B, so the singleton partition is an allowed deterministic
  partition. The result is therefore a valid obstruction to the uniform-partition T2 claim for LS0 alone under
  a=ell+|start|, and to nothing more.

## Observations (not defects; asymptotic scope respected)
- **The tail-supply step cannot be exercised numerically.** At n ≤ 10⁶ the count of nulls with ξ ≤ −√(1.5 log n) was
  0–6, against 2L = 28–50 (`tail_count`). In practice the best swap uses the most negative outside nulls, and the
  numerical margins come from those. The §4 Chebyshev step is purely analytic, and I confirmed it as correct above.
  The numerics corroborate S2's conclusion, not that specific mechanism.
- **Small-n exceptions are not counterexamples.** At n=1000, c=.55, two of six runs left the null-swap regime before
  L, and in those two LS0 did score S0 within the cap. The author's N4 shows the same at n=800, c=.6. These are
  finite-n diagnostics, consistent with the asymptotic statement, and not asymptotic counterexamples. Every run at
  n ≥ 2000 conforms.
- **The author's numerics share the representation and score code with cs_core** (W2-FAC-B). My check1 closes that
  dependence: on real exact-CS designs, the representation, closed-form F and fast path all agree with direct linear
  algebra and a brute-force production-rule path.

## Hypotheses and constants used
- G with exact CS, ρ=1/2, σ=1, singleton blocks, s0 ∈ {1,2}, θ=1_{S0}, p=floor(cn) with c ∈ (1/2,1), K=floor(n/2).
- Method premises: EX-A/e4' (the start is an exact γ0 maximizer), complete scans, OP-LS0, and production K = min(p, n/2).
- Probability events: |η| ≤ √log n; max|ξ| ≤ 2√log n; s → √v; ‖e‖²/n → 1; the threshold tends to t; |x_T0 − mu| < δ/2.
- Constants:
  - δ < min(1/4, (mu−t)/3);
  - a_n = √(1.5 log n);
  - V ≥ 1.4 log n;
  - M ≥ ½ − o(1);
  - swap gain ≥ .68 log n;
  - deletion gain ≤ ½ log n + log(4c−1) + o(1);
  - C > 1/log 2 for the miss.
