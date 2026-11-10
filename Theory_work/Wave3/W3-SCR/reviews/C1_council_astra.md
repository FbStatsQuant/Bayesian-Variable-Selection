# W3-SCR — C1 independent OpenAI council report

Seat: GPT-6 Astra, reasoning effort high. Reviewed STATEMENT v3.3 and the working-tree sources specified in C1_brief.md. No subagents, git commands, or edits outside this report were used. The other council seat's report was not consulted.

## 1. Gate verdicts

- **G1 PASS — correctness.** The score identities, probability events, screening proofs, bridges, master gap, search consequences, excess-set inequality, exact-recovery comparison, refit, and sharpness arguments are valid. Finding 1 is a wording correction to M6's description; its displayed inequality and proof are correct.
- **G2 PASS — hypotheses used = hypotheses stated.** Deterministic witnesses/families, Gaussian errors, the strict size cap, coefficient controls, and the extra conditions for exact recovery are explicitly present. In particular, M3/M4 use the maximising witness, and SCR-C uses bounded s0.
- **G3 PASS — no hidden assumptions.** Rank deficiency is permitted in the ridge and augmented-space arguments. No start, calibration, seed, or leakage condition enters the proofs. Uniformity over models is established before selecting search outputs. Empty families and absent certificates are handled without conditioning on their occurrence.
- **G4 PASS — dependencies.** Internal mathematical dependencies are proved in L1–L7. Gaussian tails, Laurent–Massart chi-square tails, and Gaussian Lipschitz concentration are named standard results in the forms needed. CC1–CC6 were checked directly against source, including enumeration. The design-family illustration is expressly excluded from the proof. CITECHECK.txt was consulted as supporting information, not as a substitute for checking the claims.
- **G5 PASS — constants and rates.** Rechecked 1.02, the scale bounds, 200 in A1, 16 and 576 in A1°, 104 in SCR-G, the uniform small terms in SCR-C, and the exact empty-model threshold. No incorrect constant or nonuniform asymptotic step found.
- **G6 PASS — code fidelity.** The score, standardisation, K, strict improvements, complete neighbourhood scans, ledger maximum, archive returns, and reported certificate match the source under EX-A. Incomplete outputs are excluded; a move-cap return is correctly distinguished from a certified endpoint.

## 2. Score

**9.3 / 10** (uncapped).

The package is correct and complete for its stated scope. One minor descriptive overstatement should be corrected for publication; no substantive theorem repair is required. Asymptotic scope, the stated EX-A idealisation, and the explicit absence of a guarantee that a small certificate occurs are not defects.

## 3. Findings

1. **MINOR — M6 describes the chosen bound as independent of model count, although only its geometric upper bound is.**
   - **Location:** `Theory_work/Wave3/W3-SCR/STATEMENT.md:123-124`, quote: “b_𝓗 depends on the geometry of the witness directions, not on the number of models”. Compare the definition immediately above: `b_𝓗(x) := min{√(2 log M + 2x), w({d_S}) + √(2x)}`.
   - **Issue:** The first branch still depends on M, even when the set of distinct witness directions does not change. The displayed dimension bound and the M6 illustration are valid; the literal independence assertion is stronger than the definition permits.
   - **Evidence/counterexample:** Take n=6, p=2, S0={1}, theta1>0, and centred orthogonal columns of squared norm 5. Compare H1={empty} with H2={empty,{2}}; both are admissible because K=2. Both have the same singleton direction set {d}, with norm sqrt(35/36), so their Gaussian width is sqrt(35/36)/sqrt(2*pi). At x=1, H1 has b=sqrt(2), whereas H2 has b=sqrt(2)+sqrt(35/36)/sqrt(2*pi) (this is smaller than sqrt(2 log 2+2), but larger than sqrt(2)). Thus the selected b changes solely through the model-count branch despite unchanged direction geometry.
   - **Required fix:** Replace the quoted clause by “b_𝓗 admits an upper bound depending only on the geometry of the witness directions, independently of the number of models”. Retain the minimum definition, dimension inequality, and illustration unchanged. This is a cosmetic clarification, not a failure of the master theorem or its rates.

## 4. What I verified

### Score algebra and noise events

- **L1.1–L1.7:** Re-derived the ridge residual representation and its positive spectrum; Schur complements yield the rank-one update and the gain identity. The determinant ratio satisfies 1 <= D <= n+1 and D >= (n+1)a/n. The prior increment is exactly -log((2p-1-k)/(k+1)). Substitution yields the stated score increment. Both addition criteria are sufficient, including strict improvement at the non-strict gain threshold; the deletion inequality follows from log(1+u) <= u. The augmented representation has the stated ridge-bias norm.
- **L2:** Witness noise has variance <= sigma^2 a. The witness is deterministic, so there is one tail per model rather than one per missing coordinate. The union bounds for E1/E4 and both response-scale events are valid. The upper scale uses 2+sqrt(2) <= 4; the lower scale bound is also valid. Augmented projection noise is a Gaussian quadratic form dominated by a chi-square of the subspace dimension. The E3a bound is 2q exp(-x); the E3b size-weighted union sums to exp(-x')/(1-exp(-x')). Zero-variance directions require no nonsingularity assumption.

### Screening, bridges, and primitive corollaries

- **SCR-A and A-infinity:** The witness gain exceeds the improvement threshold simultaneously for every missing-truth model. The cap q <= K-1 makes each addition legal. For x_n=sqrt(log n), N_q <= (p+1)^q and q/p <= 1 give the required entropy remainder even at q=0 or bounded p; multiplication by sigma is controlled by sigma <= tau_n. No polynomial-p assumption is used.
- **SCR-A° and A°-infinity:** Re-derived the residual denominator bound using 2 sigma m_S <= sigma_S^2 sqrt(n-1), including the 1.02 tau-bar squared term. The stated assumptions make every term of vartheta° vanish, including tau-bar squared/(n sigma squared). The claimed included-orthogonal-truth contribution A^2/n^2 is exact.
- **L4.0 and B1/B2/B2°/B2d/B3:** The augmented missing-signal vector w has norm at least sqrt(Delta(S)); its inner product with the residual mean is at least ||w||(||w||-c_theta). Monotonicity applies on the explicitly imposed domain. The l1/l2 substitutions and the normalised bound's 4 and 9 factors have the correct directions. The directional floor suffices at exactly the same point as the anchored floor. The sparse-floor bridge follows from the Schur-complement variational formula, including the empty-conditioning case.
- **A1:** Gamma >= kappa^2 b^2 n/16 and the squared asymptotic threshold <= 4(M^2+sigma^2)c1 n give ratio squared >= 200/64 > 2.
- **A1°:** The coefficient-ratio condition supplies the twice-bias requirement. Its two primitive bounds imply Psi >= 8 L_n, whereas the squared target threshold is <= 4 L_n. The constants 16 and 576 suffice.

### Master gap and uncertified outputs

- **SCR-M:** Both one-sided complexities have failure probability <= exp(-x). Taking their minimum costs no extra probability because the smaller threshold is selected deterministically. The signed witness yields the positive-part gain bound; the cross-term and scale events yield both denominator bounds and therefore their minimum. The score increment is increasing in the resulting ratio. The convention u_S >= 1 is harmless: on the asserted event the actual ratio is strictly below one, so such a parameter case makes that event empty and cannot contradict a positive probability lower bound.
- **M1–M3:** The local-optimum contradiction and the ledger comparison are valid. MC and MC° imply strictly positive deterministic gaps for the maximising witness. The direct SCR-A proof retains its sharper three-tail failure bound; the master proof explicitly states the corresponding denominator-only variant.
- **M5:** If a best improving neighbour drops a truth, it drops exactly one. Re-adding it gives either C (deletion) or C plus the swapped-in variable (swap). In the swap case the latter was itself scanned at C because |C|=|N|<=K-1. Both possibilities contradict the positive gap at N. This proves the capped-return result and path induction without assuming that the returned model was scanned as a centre.
- **M4/SCR-G:** r_n=o(sqrt(n)) yields g-minus >= kappa^2 b^2 n/25; the denominator gives u_S >= kappa^2 b^2/[26(M^2+sigma^2)]. The penalty is uniformly o(n), yielding a gap strictly exceeding c2 n with c2=kappa^2 b^2/[104(M^2+sigma^2)]. Thus the non-strict near-best cutoff in SCR-G is safe. Also checked kappa b <= M for the directional floor, which need not itself be <=1.
- **M6:** The width bound follows from projection onto the witness span and E||P g|| <= sqrt(rank). In the orthogonal-single-truth illustration, all directions coincide and gain is of order n while the penalty is o(n). Finding 1 concerns only the prose describing b, not these statements.

### Excess models, refit, and sharpness

- **L5 geometric facts and L5.1:** The augmented Schur complement is positive definite even for a singular original design. Its inverse diagonal gives the conditional lengths; the normalised inverse gives the dual-direction correlation matrix. Under the floor, alpha >= phi and omega <= 1/phi. Summing the necessary deletion gains and bounding the dual frame by omega gives EC′ with the displayed coefficient-bias term. The residual norm bound, outer positive part, and (n-1)/(n+0.02) >= 1-1.02/n are valid. The single-excess rearrangement and event probabilities follow.
- **L5.2 and SCR-C:** Screening plus violation of EC excludes every strict superset. Uniformly in k<=q_n, U(k,2 log n)=o(n) and eta_n=o(1). Bounded s0 makes k <= (s0+1)m usable with a bounded penalty loss. The key comparison phi(2 ell+log n)-2 ell >= epsilon(2 log p+log n) dominates all uniform remainder terms and the chosen x'=epsilon log n/8. Cases q_n<=s0 are covered by screening directly.
- **SCR-R:** Once screening holds, the fitted-mean error equals P_C epsilon. The simultaneous sparse projection bound applies to data-selected certified models. The coefficient bound follows from the stated positive superset floor; no floor is needed for prediction.
- **SCR-N:** At the empty model D=n and a=n^2/(n+1), giving the exact threshold B_n. Re-derived B_n<=L_n and its lower bound. The two coordinate unions plus the lower scale event yield the four-tail bound. For consequence 1 the positive solution for theta1 exists eventually, is of order sqrt(log n/n), and the null-coordinate threshold retains a strict asymptotic margin for every fixed A. For consequence 2, Delta is asymptotic to 2(log n)^2 while each true gain is asymptotic to (log n)^2/n; the empty model is LO with probability tending to one. B1's lower bound is asymptotically attained on this sequence. Neither construction asserts that the code must report the empty model.

### Code and scope

- Checked the relevant branches of all eight specified source files: `v3_fit.R`, `v3_run.R`, `v3_exact.R`, `v3_preprocess.R`, `cpp/v3_engine.h`, `cpp/v3_core.cpp`, `cpp/v3_ledger.h`, and `cpp/v3_score.h`; additionally checked `hpm_better` in `cpp/v3_util.h`.
- **CC1/CC4:** Complete flip/swap scans, skipped cap additions, strict comparison, certified no-improvement endpoint, and best-neighbour move-cap return match `local_search`.
- **CC2/CC3:** Final assembly requires identity of the HPM and a certified returned endpoint; an equal-score displaced endpoint does not transfer its flag. Initial/failed outputs remain uncertified. Exact enumeration recursively visits every subset up to K and keeps the maximum; its local flag is tied to status `exact`.
- **CC5:** Sample-SD standardisation, K, prior, H/A determinants, nu, and 0.02 match the formulas. The nonnegative Q fallback is algebraically equivalent under EX-A.
- **CC6:** Fresh scores reach the ledger; cached scores have already been offered. The final search's non-emitting initial score is the existing HPM. Both searches share the run's ledger/cache, and inherited models are offered to that ledger. The archive exports scanned centres, their scores, completeness, path, and returned model. Raw index conversion preserves model identity.
- Read PROGRAM item 5, PROTOCOL, all of STATEMENT, CODE_CHECK, L1–L7, and ASSUMPTION_MAP. The primitive A1 corollary delivers the target card through the stated bridge. No design-family assumption enters a theorem's proof; the geometric example is illustrative. The declared nonclaims accurately delimit the conclusions.

Verification was analytical and source-based. I did not rerun production fits or numerical simulations, and did not use prior review verdicts as evidence of correctness.