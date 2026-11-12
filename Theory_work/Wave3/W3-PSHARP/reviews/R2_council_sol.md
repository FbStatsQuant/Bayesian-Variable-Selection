# R2 blind council review — seat sol

Overall score: **9.2 / 10.0**. All six gates **PASS**. Findings: **0 FATAL / 0 MAJOR / 0 MINOR / 2 NIT**.

Reviewed the frozen content identified in the brief as manifest `4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14`. I read the authorized statement, four lemma files, report, assumption map, plan, task brief, citation checker, numerical scripts and outputs, and the authorized parent definitions/statements and code excerpts. I did not consult other reviews, dispositions, logs, checkpoints, or other seats. This is an independent derivation, not reliance on the review-trail table. No source file was changed; no commit or subagent was used.

## Gates and mathematical audit

### G1 — correctness: PASS

**Lemma V and S.** Expanding the penalized objective gives Hessian H_S/n and minimizer n H_S^{-1}z_S. Rescaling the response rescales the minimum by s_y^2. Positive definiteness comes from the identity ridge term, including at rank deficiency. The two Schur complements are exactly s and n-g'(G+I)^{-1}g. For the determinant bound, the eigenvalue of (n+1)^2 H^{-1}-n(G+I)^{-1} is

`((n+1)lambda + n^2+n+1)/(((n+1)lambda+1)(lambda+1)) > 0`.

Thus the bound is n, with equality precisely g=0; iteration is valid even for the algebraic determinant of sets outside Omega. Block inversion gives the stated Q gain. Its lower bound uses s<=n^2, and nonnegativity of the resulting Q uses Lemma V. The binomial prior ratio, gamma in [0,1), exponential lower bound, and sum over distinct feasible one-step supersets are correct. Empty S is handled explicitly.

**Claim A.** I checked Lemma W's Chebyshev constants, both truncated moments, and the sphere-density comparison. The gamma-function bounds follow from log convexity; on t^2<=tau<=d/2 the two exponential envelopes are valid. Lemma R loses at most exp(-epsilon/2) on the truncation and its displayed constant 8 follows from epsilon'=epsilon/4. It needs no independence of kappa and the scores.

For W-orth the noise projections are independent normals, the Q decrement has factor (n-1)/(n s_y^2), and the variational upper bound on V yields the required kappa deficit o(1/log N), uniformly. For W-sph the conditional projection law does not depend on epsilon, so the scores really are iid unconditionally. The identity for Q-||rho||^2, singular-value bounds, lower bound by sigma^2 chi-square_{n-1-r0}, and Markov/Chebyshev events all have the asserted constants. In particular m>=n/2 follows from s0+1<=K; neither a spectral floor nor independence of the outside columns is used. Both logarithmic restrictions have explicit roles. The uniform bound gives the conditional-to-joint transfer. A1's conversion from odds to delta and its expectation liminf are valid; A2 correctly keeps odds when Lambda need not vanish and derives the two necessary sparsity conditions. The Gaussian and orthogonal examples in A3 satisfy the stated parent hypotheses, with the upper bounds expressly conditional on the parents.

**Claim B.** Multiplying the exact prior ratio by C(p-s0,j) produces precisely the displayed binomial coefficient and product. Every intermediate model is feasible. The j=1 term, all four assertions about c(p,s0), and B1/B2 follow as written. At the critical scale K-s0 tends to infinity; each fixed j term converges to (lambda/2)^j/j!. Taking finite partial sums before letting their length grow proves liminf O_lb>=exp(lambda/2)-1 without an unjustified interchange of an infinite sum and a limit. The resulting deterministic cap is exp(-lambda/2). B3 has the stated witness and s0<=p/2 qualifications.

**Claim C.** The near-collinear pair gives exactly the stated representation and divergent coefficient norm. Projecting onto the missing orthogonal truths and minimizing A(beta+gamma x)^2+x^2/n proves Lemma P, including models lacking column 2. The bounds on the reference costs follow, and the bounded-cost alternative T' is correctly identified. The prior-tail cutoff calculation and the two-column determinant bound are valid. The uniform lower fit bound preserves the common noise norm; subtracting the T' upper fit bound yields Delta>=nb^2/10 on F_n. No independence between the two chi-square statistics is needed for the union bound. The fit penalty exp(-nb^2/(42 V0)), the prior/determinant/count payment <=exp(12 log^2 n), and the final constant 1/(73 V0) are all correct. The two normalized tail variables diverge, which establishes failure of the parent conclusions after removal of reference-cost control.

### G2 — hypotheses used equal stated: PASS

Every substantive item of STATEMENT v1.2.2 is covered: S(1)-(4), A and A1-A2, the conditional reading A3, B and B1-B3, and C(1)-(3) and its parent-conclusion reading. A assumes coefficient and energy bounds only where needed to control the reference fit. B and S are deterministic and allow arbitrary S0. C makes no uniform claim outside its explicitly constructed sequence. The finite-n range n>=200 is not confused with feasibility of its strong signal condition. No new upper bound is presented as proved here.

### G3 — no hidden assumptions: PASS

The capped model space, p>=2, n>=3, nonconstant response, empty models, singular Gram matrices, and feasible one-step extensions are accounted for. Under Gaussian truth the excluded event s_y=0 has probability zero. The W-sph conditional laws and the conditioning required for random true blocks are explicit. The two uniform little-o envelopes are stated. Arbitrary outside columns do not affect score ratios of the summed models. Consequences requiring multiplicity comparable to s0+1 retain s0<=p/2. The C construction fits within the centered ambient dimension for every n>=200, and all references and means used there are deterministic.

### G4 — statuses and citations: PASS

The four proof statuses are consistently quoted as `PROVED (by this seat, unchecked)`. The main report distinguishes new lower bounds from upper bounds inherited conditionally in A3. The parent L1a' statement really requires an exact representation and the coefficient bound; L1a'' really requires bounded penalized approximation cost. Their normalizations match the quantities shown to diverge. The counterexample disproves unqualified removal, while leaving the intermediate growing-cost regime open; it does not claim boundedness is necessary for every reference. The numerical boundary experiment is correctly limited to one-step odds. Citation-check rerun: **42 checks, 0 MISS**. Historical reviewer verdicts in the report were not independently authenticated because the blind brief prohibits reading those reviews; none is needed for this verdict.

### G5 — constants and rates: PASS

The truncated normal mean is exactly 2 sqrt(log N/pi), giving precisely the stated Lambda constant 1/sqrt(pi). The full B sum and critical-scale exponential constant are correct.

For C, the analytic envelope 3.78(12 log n+3)^2 n^{-2.158} is decreasing for n>=200 (its logarithmic derivative is 24/(12 log n+3)-2.158<0), and its value at 200 is about 0.18137<1. The dimension envelope is decreasing relative to n/2 there. The determinant estimate uses (1+1/n)^2<=2 and the stated bound on k. The Delta constants are conservative, the logarithmic count bound holds at log 200 and improves thereafter, and 1/42-1/100>1/73. Thus the proof covers all n>=200 subject to the signal condition, not just the sampled n. The signal condition permits b_n^2=1200 V0 log^2 n/n eventually and gives the advertised cost range and growing-cost counterexamples.

### G6 — coded target and numerics: PASS

The target agrees with the authorized C++ excerpts: cap min(p,n/2), prior -log 2-log C(2p-1,k), nu=a0+n/2, determinant ratio, and Q=y'y-n z'H^{-1}z. This is the real-arithmetic target; no floating-point implementation theorem is claimed.

I inspected the Gamma-integral/elementary-symmetric algorithm, the direct and exact-in-law spherical reductions, the generic enumeration, the cancellation-free structured C formulas, and the cutoff implementation. Their statistical targets and normalization match the report. Restricted-size odds and one-step odds are correctly described in REPORT as lower bounds before numerical integration error. Quadrature is not advertised as a certified enclosure. The C experiments explicitly use scaled-down k and do not purport to satisfy the theorem's signal constant.

Reruns and independent checks:

- `a_orth.py V1 E3`: reproduced the 1.37e-13 maximum relative validation error and the recorded moment calculations.
- `b_check.py`: reproduced all 8,064 Schur checks, all 55,740 posterior cases, minimum odds/O_lb=1.033240, equality cases, and the critical-scale table.
- Scratch `check.py`: reran spherical one-step validation (8.1e-14); C structured validation at eta=.05 (2.4e-13) and eta=n^-2 against 60-digit arithmetic (1.4e-15); reproduced C's cutoff rows including n^2 R=3.564e-4 at n=200.
- Independently integrated 24 sphere moment cases, including d=3 and tau=d/2: all bounds passed. Scanned all integer n=200..200000 for dimension, cutoff-envelope, determinant, Delta and count inequalities: all passed. The analytic monotonicity and inequalities above, rather than this finite scan, cover the remaining n.

The expensive full Monte Carlo grids were inspected with their stored outputs, not rerun in full. The numerical scripts support the stated scope; the proof does not depend on Monte Carlo evidence.

## Findings and exact corrections

**NIT N1 — omitted finite upper summation limit in the report.** `Theory_work/Wave3/W3-PSHARP/REPORT.md:39` writes the full lower-bound sum as `Sigma_{j>=1}` without stating a convention that stops at feasible extensions. The locked statement and proof correctly use j<=K-s0. Replace `Sigma_{j>=1}` with `Sigma_{j=1}^{K-s0}`. This is a transcription issue in a summary, not a defect in Claim B.

**NIT N2 — stale numerical-plan description.** `Theory_work/Wave3/W3-PSHARP/PLAN.md:28` calls the large-p output “exact delta_n,” and line 29 proposes delta_n/Lambda_n. The delivered main experiment reports restricted-size odds/Lambda_n; its transformed delta value is also only a lower bound before quadrature error. Replace lines 28-29 with: “Orthogonal design; compute odds over |S|<=min(K,s0+60) (s0+80 in E2) by Gamma-integral/elementary-symmetric DP, evaluated by quadrature and validated against brute force. Report restricted odds/Lambda_n, one-step odds/Lambda_n, and the transformed lower bound on delta_n sqrt(n).” REPORT §3 and the implementation already supply the correct qualifications, so this does not fail G6.

No mathematical correction is required for acceptance. Neither nit changes a gate verdict.

COUNCIL-VERDICT round=R2 manifest=4513e05a40ddc3bf8baeebf04d7156d3c0ac84442dbe0d9b2c6c59244afdac14 seat=sol score=9.2 gates=PASS

## Addendum — per-claim decisions (seat sol, round R2; 2026-11-12; same seat model, fresh thread; no rescoring)

| id | decision |
|---|---|
| W3-PSHARP:S | ACCEPT |
| W3-PSHARP:A | ACCEPT |
| W3-PSHARP:B | ACCEPT |
| W3-PSHARP:C | ACCEPT |

Where examined: W3-PSHARP:S: G1 — correctness, **Lemma V and S.** beginning at line 11; G2 confirms coverage of the stated clauses; Findings and exact corrections contains no blocking finding.
W3-PSHARP:A: G1 — correctness, **Claim A.** beginning at line 17; G2 confirms coverage of the stated clauses; Findings and exact corrections contains no blocking finding.
W3-PSHARP:B: G1 — correctness, **Claim B.** beginning at line 21; G2 confirms coverage of the stated clauses; Findings and exact corrections contains no blocking finding.
W3-PSHARP:C: G1 — correctness, **Claim C.** beginning at line 23; G2 confirms coverage of the stated clauses; Findings and exact corrections contains no blocking finding.
