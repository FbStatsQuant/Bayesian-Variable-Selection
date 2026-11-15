MANIFEST 867e1c933d6fbbcbfd47b5deccf3b7f132d156fef1a29113de20e55eb5fefe38

Verdict: VERIFIED — lemmas/L2_TK.md
Verdict: VERIFIED-WITH-AMENDMENTS — lemmas/L4_VIS.md

Findings

1. MINOR — lemmas/L4_VIS.md:45. The symbol ϑ̄_n is used without being introduced in this file or in the listed L2 inputs. The needed quantity is defined in lemmas/L3_LEAK.md:45, but this dependence is implicit. Exact local repair: before Step 4 define 1 + ϑ̄_n := (n + 0.02)/((n − 1)(1 − ω̄_n)), for n ≥ n₁, and state ϑ_n ≤ ϑ̄_n → 0. Then the threshold condition in line 45 is justified using quantities depending only on (n, A). This is a notation amendment, not a missing substantive argument; it changes no hypothesis, constant in the locked statement, or conclusion.

2. MINOR (auxiliary numerical reporting; no L2 proof amendment required) — numerics/lemmas/falsify_L2_L3.R:33,46,64–65 and numerics/lemmas/RESULTS_LEMMAS.md:10. The identity errors and comparison of realised max|ρ| with ω_n are printed diagnostics, not checks that call bad(). Thus TOTAL VIOLATIONS: 0 does not itself certify those comparisons. Moreover c_E is replaced by the observed minimum RSS^y_U/n at script line 50, and g_* by the observed minimum sampled eigenvalue: the remainder test is not a direct test of the prescribed deterministic c_E, κ₁ under the full event. Exact repair: describe these as diagnostics and realised-constant checks in RESULTS_LEMMAS.md; alternatively add assertions for the identities with explicit tolerances, and test the theoretical remainder constants only after checking the stated event and n-threshold. An RSS deviation exceeding ω_n on an unconstrained draw is an event failure, not by itself a counterexample to TK-a. This finding does not undermine the independently checked L2 proof.

No CRITICAL or MAJOR finding. The L4 amendment above is local and leaves STATEMENT.md v1.3 unchanged.

Checks performed

Frozen inputs and scope

- Ran the authorised manifest verification command with python -B: verify: OK, with the digest quoted above. Read every line of L2 and L4, the locked definitions and hypotheses and relevant interface/bridge statements, L3.4 and its supporting definitions, and the statement of AGG-d. Took AGG-d as given, as instructed. Inspected the pinned scorer at Scripts/SMC_BVS/core/cpp/v3_score.h:204–224. No registry result or another ticket's theorem was used as a premise.

L2.0–L2.1: projections, identity and event

- Since the columns and μ are centred, P_U C = P_U, C − P_U is a projection, and the mixed term in the residual square is exactly 2〈r_U, ε〉. Orthogonality gives the subtraction of ||P_U ε||² in (2.1), with the displayed sign.
- The block family has at most p blocks times 2^16 subsets. GF-blk gives ranks |U| ≤ 16. With t_n = 4 log(2^24 pn), the χ² moment bound is 2^8 exp(−t_n/4) = 2^−16/(pn), giving 1/n after the union. For q_n² = 2 log(2^17 pn), the two-sided Gaussian bound is also 2^−16/(pn). Zero residual means contribute no failure probability. Laurent–Massart with x = n^(1/3) supplies the other 2 exp(−n^(1/3)). Independence is unnecessary.
- Recomputed the additive constants: 96 log 2 < 67 and 34 log 2 < 24. The leading contribution to ω̄_n is of order n^−1/3; sqrt(log n/n), n^−2/3 and log n/n are smaller. Therefore ω̄_n log n → 0, precisely the rate required by [TK]. The threshold n₁ depends only on A.

L2.2: TK-a through TK-f

- TK-a: 2σ sqrt(Λ_U) ≤ σ² sqrt(n−1) + Λ_U/sqrt(n−1) = sqrt(n−1) τ²_U. Multiplication by q_n and division by (n−1)τ²_U give exactly q_n/sqrt(n−1). The remaining two absolute errors are bounded using σ² ≤ τ²_U. No energy bound is needed here.
- TK-b: RSS_empty ≤ 3[σ²(n−1)+||μ||²]/2 ≤ C_R n; RSS_U ≥ (n−1)σ²/2. Rescaling yields RSS^y_U ≥ (n−1)²σ²/(2C_R n) ≥ σ²n/(4C_R) = c_E n for n ≥ 4. Both constants and strict positivity are correct.
- TK-c: the pinned determinant ratio is det((n+1)G+I)/det(G+I). Each residual determinant factor lies between g_*/(g_*+1) and 1. The exact eigenvalue in the quadratic correction is (g+1)/((n+1)g+1), bounded by (1+1/g_*)/(n+1). Multiplication by ||P_U y||² ≤ n−1 gives E2. Neither argument needs a normalised Gram floor.
- The scorer adds 0.02 before the logarithm, so a_U ≤ 1.02+1/g_*. The log(1+x) ≤ x bound with ν/n ≤ 0.51 gives the stated κ₁; |U|/2 ≤ 8 gives κ₂. The sign of each term in R_U is correct. The common c′_n has the correct positive rescaling term. For the empty set D = 1, Q = RSS^y, and the same lower remainder bound applies.
- TK-d follows by subtraction; the common normalisation m(empty) cancels. The 2κ_E bound is conservative and valid.
- TK-e: for nested sets Π = P_W − P_U is a projection of rank |W|−|U|, ΠC = Π. The projected signal energy is Λ_U−Λ_W and the one-step projection is uuᵀ. Thus the displayed squared Gaussian one-step gain is exact.
- TK-f: f1 uses −log(1−x) ≥ x and the upper bound on RSS_U, hence τ²_U; f2 uses log u ≤ u−1 and the lower bound on RSS_W, hence τ²_W; f3 uses −log(1−x) ≤ x+x² on [0,1/2] and the lower bound on RSS_U, hence τ²_U. The multiplier (n+0.02)/((n−1)(1−ω_n)) is correct in both upper bounds.
- These derivations use no lower bound on s₀. At s₀ = 0, μ = 0 and all residual-mean cross terms vanish. L2 delivers [TK] and B-TK with the claimed constant dependence and uniformity.

L4.0–L4.1: margin bridge

- A column has three statuses in a nested pair: outside W, in W\U, or in U. This gives 3^|C_b| ≤ 3^16 pairs per truth block. The rank is at most 16, so 2^8 exp(−ζ_n/4) times s₀3^16 is exactly 1/log n. For a one-step pair this also bounds Z². Both sides of Q± follow by Young's inequality, including the lower coefficient −(1/ε₁−1).
- The construction V = U*_b, D = V\U, R = (U∩Q)\S₀, N = U\Q is an admissible instance of V-m. In particular R ⊆ Q\S₀, N ⊆ [p]\Q, D is nonempty, and |V|+|R|+|N| ≤ 16. T = V∪R is exactly T_b(U), including when Q ≠ S₀ and R is nonempty. The cardinality difference is |U|−|T| = a−d.
- Step 1 has the correct sign: the residual logarithm is −A₁+A₂. In Step 2 the negative noise term can safely be weakened to −ζ_n/(2ε₁); the signal denominator is τ²_U. Step 3 uses τ²_W in f2; its noise term is bounded because σ² ≤ τ²_W. No assumption that L₂ is small is needed.
- Re-derived both ε₁ claims. Its first upper bound gives ε₁(2+ε₀) ≤ ε₀/2, and ε₁ ≤ 1/2 gives ε₀/2 ≥ (1+ε₁)ε₀/3. Its second upper bound gives ε₁P ≤ (c_m−2κ)/2, since P ≤ 16(1+2A)+c_m. Hence (1−ε₁)P ≥ (1+2A)(d−a)_+ + κ+c_m/2.
- Step 4 then drops a nonnegative L₂ coefficient for sufficiently large n; C₁ correctly bounds the two noise coefficients when ϑ_n ≤ 1. The notation repair in finding 1 makes that threshold explicit.
- Step 5: for d ≥ a use log p ≤ A log n and log(n+1) ≤ log n+log(5/4). For a>d, a≤15 and c_Q/p≤1+15s₀≤16s₀, so the claimed constant bound is valid even if c_Q/p exceeds 1. Both are covered by C₂ = 16 log(32s₀).
- Step 6 loses at most 8(1+2A)ω̄_n log n from the price coefficient. Its negative limiting coefficient is (κ+c_m/2)/2 > κ, while ζ_n/log n → 0. This absorbs every constant, including 16 log 2. Step 7 sums at most 2^16 terms per fibre and then takes maxima; no additional factor for the number of truth blocks is needed. All thresholds involve only the listed fixed constants.

L4.2–L4.3: constant visibility bridge

- Each intermediate conditioning set before adding a missing truth has size at most 15. The V-c lower bound uses τ²_U at that intermediate set. The ε₁ choice guarantees ε₁c_V ≤ (κ_V−κ)/2. In fact the second entry of the minimum is below 1/4, so ε₁ is in (0,1).
- Checked lines 66–68: replacing ω_n by ω̄_n weakens the negative signal term, and 1/(1+ω̄_n) ≥ 1−ω̄_n leaves an error bounded by (c_V/2)ω̄_n log n. The exponent slack (κ_V−κ)/4 absorbs ζ_n/(2ε₁), all fixed constants, and 17 log 2.
- Multiplying the a′ one-step inequalities and taking the a′-th root preserves the factor 2^−17; it is not raised to an unaccounted power. Multiplication by 2p gives 2^−16, and A−(c_V−1)/2+(κ_V−κ)/2 = −(κ_V+κ)/2. Thus the claimed bound on e_n follows without any null-gain smallness premise.
- With e_n≤1 and c_QU_Q≤1, the assumed AGG-d gives 2^16 max(e_n,e_n^16) = 2^16e_n. This supplies the bound for Ξ for arbitrary Q.
- In L4.3, AL and block domination supply the premise of L3.4(a). For s₀≥1, c_Q≤16s₀(|Q|+1), so c_QU_Q = O_P(ϱ_n(Q;h)) → 0. This is where AL is used; neither visibility proposition needs small null gains. For κ≤0 the interface claims follow from any admissible positive exponent, so the proofs for 0<κ<κ_V suffice.

Edge cases

- s₀=0: L2 remains valid; L4 needs no event ζ_n involving log s₀, since Ξ=e_n=0 by definition and visibility is immediate.
- A truth block containing all S₀ requires no change: its residual signal after all truths are included is zero. A block consisting of 16 truths allows d=16,a=0, and its final one-step conditioning set has size 15.
- At the other cardinality extreme d=1,a=15, the positive-excess price is at most 15 log(16s₀); the proof does not assume d≥a. The equality d=a is covered by Step 5's first case. Retained nulls R cancel from the cardinality difference and are preserved in T_b(U).

Numerical attempts

- Re-ran both supplied scripts read-only with seed 731: Rscript numerics/lemmas/falsify_L2_L3.R 731 and Rscript numerics/lemmas/falsify_L4_L5.R 731, using their full ticket-relative paths. Both completed with TOTAL VIOLATIONS: 0. The former covers 3,200 sampled toolkit configurations and 240 integration points; the latter tests the visibility chain on six designs with 20 noise draws each. The minimum L4 chain slack in this rerun was about 0.52. Locale startup warnings did not stop execution.
- Ran a separate inline R falsification attempt, seed 8671, with an independently written scorer: 600 random configurations, n in {40,100,400}, block size 6 or 16, near-twin columns, empty and nonempty truth sets, and Q drawn to include retained nulls. Also forced an all-truth block with U empty. Checked (2.1), E2, f1–f3, and the actual-score L4 Steps 1–3 comparison, using realised residual-error/noise constants. No failures: maximum relative (2.1) error 1.92e−15; maximum E2/bound 0.9382; minimum L4 chain slack 0.05394. These are local inequality tests, not tests that every sampled design satisfies global V-m or V-c.
- Independently sampled 10,000 choices of A,c_m,ε₀,κ and net deletion count 0…16, checking both ε₁ inequalities of L4.1: no failures.
- The supplied L4 script correctly labels its reported quantity as the largest Ξ term, rather than Ξ itself. It checks Steps 1–3 with realised constants, not the final fixed-constant threshold n₃ or the full partition-free V-m quantifier. Its A=log(p)/log(n) and realised visibility levels are diagnostic at each n, not a proof of uniform asymptotics. The supplied scripts do not numerically cover Q≠S₀ or a 16-column block; the inline checks extend those local algebra cases. The asymptotic conclusions rest on the analytic arguments above.

Not checked

- Proof of AGG-d (explicitly taken as given), the other AGG/FLOOR claims, assembly, necessity claims, random-design bridges, or the remainder of L5.
- Full independent review of L3 beyond the statements/definitions used in L4.3 and their compatibility with AL; its numerical integration was rerun incidentally.
- Calibration of astronomically large finite n₃,n₄, empirical verification of their uniform thresholds, floating-point accuracy of compiled production code, or every instance of partition-free visibility in the simulated designs.
- No repository files were edited other than this review; no git state was changed and no subagents were started.
