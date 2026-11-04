# Independent closing correctness review: T22(iii) and T27(i)

Reviewer: Codex review helper. Date: 2026-10-22.

Assigned artifacts:

- `T22iii_T16_start_aggregation/STATEMENT.md` and `proof/PROOF_v1.tex`.
- `T27i_T20C_cancellation_budget/STATEMENT.md` and `proof/PROOF_v2.tex`.

All paths below are relative to the proofs root unless specified otherwise. `Collection` means `COLLECTED/COLLECTED_PROOFS_v2.tex`; its line numbers are physical source lines. Original theorem paths are relative to `../theorems/`. This review uses the mathematical statements/proofs and authoritative method definitions, not other reviewers' conclusions. No proof was edited, no work was delegated, and no numerical workload was run.

## Overall determination

No fatal or gap finding in either assigned proof. Each establishes its assigned STATEMENT under its explicit hypotheses. The T22 EXP-to-EXP-prime change is treated as approved; the assigned statement expressly includes NL_eta on the leakage family in that approved package (STATEMENT lines 5–7). Neither proof discharges an assumed statistical expansion or cancellation premise from primitive design conditions.

The following exposition findings document limits on combining the results. They do not invalidate either theorem, and no corrective wording is required for verification of these artifacts.

## Findings

### F1. T22 concentration cannot discharge T27's proper-subset reference-mass premise

- **Location:** T22 proof lines 126–140, 440–465; T27 STATEMENT lines 28, 37, 63; T27 proof lines 46–68, 159–160.
- **Severity:** exposition (cross-theorem application constraint; no defect in the assigned proofs).
- **Claim:** T22(iii) with reference equal to the truth must not be used to supply H3 for a T27 completion chain with c >= 1.
- **Evidence:** T22 proves pi_0(S_0) -> 1. T27 H1 makes S^(0) a proper subset of S_0 whenever c >= 1. Pathwise, pi_0(S^(0)) <= 1-pi_0(S_0), even if the subset is selected using the data. Thus under T22's hypotheses that reference mass tends to zero, contradicting T27 H3's fixed-positive lower bound. Conversely, T27's verified mass law with c >= 1 implies pi_0(S_0) -> 0 because p >= 1 and n^(-c/2) exp{O_P(1)} -> 0. These are distinct conditional regimes, not conclusions that can be combined under a common satisfied hypothesis package. T27's actual discussion cites only the deterministic T22(i) bound for a potential separate reference and does not make the invalid inference.
- **Exact wording required:** none in the assigned proofs. Any later combined claim must explicitly verify H3 for its actual reference; truth concentration is not that verification.

### F2. EXP-prime, leakage control, and cancellation are separate hypotheses

- **Location:** T22 STATEMENT lines 37, 49–57; T22 proof lines 73–89, 205–245, 362–381; T27 STATEMENT lines 30–35, 51–59; T27 proof lines 133–157.
- **Severity:** exposition (hypothesis-scope constraint; correctly handled).
- **Claim:** Neither EXP-prime alone nor T22's leakage-family quadratic specialization establishes T27 H2 on its missing-true-variable chain.
- **Evidence:** T22's leakage family adds l outside S_0 after the block's true variables are already present. T27's chain adds coordinates of S_0 before completion. These families are different. T22 correctly assumes EXP-prime on all additions and uses the logarithms themselves, telescoped, for visibility; it does not extend its leakage-only quadratic approximation to true additions. T27 writes E_(n,i) = -nu log(1-x_i) + R_i - (1/2)log(1+1/n). With the stated strict uniform remainder, joint two-sided H2 is equivalent to max_i[-nu log(1-x_i)] = O_P(1), equivalently max_i n x_i = O_P(1). The proof establishes both directions. Its scalar x_i = n^(-1/2) example correctly distinguishes this from merely controlling n x_i^2. In particular the latter only gives an O_P(1) Taylor remainder and does not give the cancellation law.
- **Exact wording required:** none; the existing scope language is correct.

### F3. A qualitative aggregation condition does not supply normalized prior/start mass

- **Location:** T27 STATEMENT lines 37, 63; T27 proof lines 63–68, 111–128, 159–160; Collection lines 3813–3840, 3882–3884.
- **Severity:** exposition (normalization constraint; correctly handled).
- **Claim:** The normalized reference-mass hypothesis is essential to T27's two-sided absolute mass law. Neither an unnormalized table-product lower bound nor q_n < 1 alone supplies it.
- **Evidence:** The exact odds retain pi_0(S^(0)) as a multiplicative factor. T27 bounds its logarithm using H3 and the probability upper bound 1. Collection T22(i-a) gives pi_0(S°) >= (1-q)^(s+1)/(1+e)^s; this lower bound need not stay above any fixed positive constant merely because q < 1. Collection's reference-to-truth remark expressly retains the need for normalized reference mass. All prior and start normalizers cancel in odds, but cancellation does not determine the initial reference mass. T27 preserves this distinction throughout.
- **Exact wording required:** none.

## T22(iii): detailed correctness verification

### Fidelity and hypotheses

The source theorem's part (iii), `T22_T16_start_aggregation.md` lines 10–16, retains G, R, within-block SE, VIS, NL_avg(kappa), and the strict versus weaker remainder distinction. The assigned STATEMENT lines 41–73 explicitly spells out these conditions with the approved logarithmic EXP-prime and leakage-family NL_eta package. Its conclusions at lines 92–108 match the proof's theorem at lines 126–140, including the weaker exponent formulation, superpolynomial completion penalty, and kappa = 1/2 under zero leakage. The proof incorporates STATEMENT at lines 29–33 and refers back to its exact score and aggregation definitions at lines 66–72 and 118–123; omitted repetitive definitions in the proof are therefore not missing hypotheses.

The common definitions (`00_COMMON.md` lines 9–11, 18–19, 27, 35–51) and methodology lines 85–86, 97–108, 164–175 agree with the scores, prior weights, actual partition, normalization, leakage quantities, and visibility condition used here. The method is not changed. The exact-branch component qualification is present in STATEMENT line 15.

### Residual bounds and leakage specialization

Proof lines 166–202 correctly count at most p*2^B deterministic residual/comparison objects and use fixed-design Gaussian bounds without assuming independence between comparisons. The decomposition at lines 169–175 is exact: the residual-signal cross term, common centered noise norm, and projected noise norm give RSS_T-(n-1)v_T. The rank bound <= 16 makes the displayed exponential moment valid; the union bound is sufficient for uniform O_P(sqrt(n log n)) control. Since v_T >= sigma^2 > 0, the reciprocal estimate for nu/RSS_T follows uniformly. Bounded signal energy also gives a fixed high-probability upper bound C_R*n for ||Y||^2.

Lines 220–242 use Gaussian truncation and NL_eta to bound all leakage numerators by O(log n), so x = O_P(log n/n), n*x^2 = o_P(1), and the difference between the logarithmic score gain and the stated quadratic expression is uniformly o_P(1). Raw Gaussian errors are used before response standardization; invariance of the partial R-squared justifies the comparison with the actual standardized score expansion.

### Averaged rate

The integral calculation at lines 249–279 is correct, including the completed-square branch delta^2/(2 Delta) and the delta = Delta = 0 convention. Lines 290–317 use a sum to dominate each maximum, the NL_avg bound, linearity of expectation, and Markov's inequality. The resulting W_n is tight. Multiplication by exp(rho_n+d_n) preserves tightness under the strict remainder, with no independence needed. Lines 319–329 construct the weaker random exponent explicitly and prove concentration using B <= 16 and fixed kappa > 0. Lines 406–424 correctly derive the eta threshold and zero-leakage endpoint.

### Completion penalty

Lines 339–360 correctly use nested within-block projections and their bounded rank to obtain uniform observed completion gain at least one quarter of the deterministic signal gain, with probability tending to one. Lines 362–381 telescope EXP-prime along missing-true additions without applying the leakage approximation. The inequality -log(t) >= 1-t and RSS_U <= C_R*n give a positive constant times M_n^V log n. Dividing by the number of missing variables costs at most the factor 16. Lines 383–401 then dominate the factor 2p and the n^(1/2) penalty, proving n^m e_n -> 0 for every fixed m under either remainder regime.

### Wave-1 citation audit and final aggregation

The sole used wave-1 result is cited at proof lines 429–438. It matches Collection T22(i-a), lines 3813–3827, and T22(i-b), lines 3829–3840. Those collection proofs include capped normalization via domination by uncapped completion weights and establish q <= u for the same definitions. The reference S_0 is feasible, the actual tables are positive, and the p=s_0 conventions agree. Thus the substitution of u on {u<1} is authorized. The final event {u<=1/2}, random-scale O_P bound, absorption of e_n into the deterministic rate, and weaker exponent argument at lines 440–465 are justified.

**T22(iii): VERIFIED.**

## T27(i): detailed correctness verification

### Fidelity and hypotheses

The source `T27_T20C_cancellation_budget.md` lines 8–14 assumes fixed starting size and cancellation count, feasible successive additions, joint n^(-1/2) exp{O_P(1)} sequential ratios, and a normalized reference mass bounded below by a fixed positive constant with probability tending to one. STATEMENT H1–H4 and proof lines 46–71 faithfully spell these out. Data-selected chains are permitted only if the selected-chain joint premise holds; this is a valid explicit quantification of the conditional implication and does not substitute pointwise pre-selection control. Neither Gaussianity nor EXP-prime is silently used to establish H2 or H3. The original operational assumptions are retained, with the mass law correctly proved unconditionally under P_0 rather than after conditioning on successful execution.

The score and model-prior definitions agree with methodology lines 97–108 and 170–175. The fixed-p exact-branch interpretation at proof line 44 agrees with methodology lines 154–160. The theorem claims only part (i), not a discovery-budget or mixing conclusion. The c=0 extension at line 130 follows directly from H3.

### Positivity, prior cost, and exact chain law

Proof line 83 correctly proves finite positive scores even for singular Gram matrices. The common normalizers cancel in lines 85–91. The exact BB(1,p) addition ratio at line 94 is (k+1)/(2p-k-1), so every fixed-size addition contributes p^(-1) times a factor bounded above and away from zero. The exact factor A_(p,s,c) at lines 101–108 and its factorial bounds are correct for every feasible p, including bounded p. The score law contributes n^(-c/2) and a sum of c tight log remainders. Repeated additions to one block telescope only when evaluated at the successive T_i, as correctly done here.

### Normalized multiplier and EXP-prime discussion

Lines 112–128 correctly use H3 to obtain log pi_0(S^(0)) = O_P(1), sum the fixed number of joint remainders, and conclude two-sided tightness of the positive multiplier and its reciprocal. No independence assumption is necessary. The optional EXP-prime equivalence at lines 140–157 is mathematically correct and is not used in the mass-law proof; see F2.

### Wave-1 citation audit

Proof line 92 and source item 3 at line 166 cite T22(ii-a). Collection lines 3855–3861 state and prove exactly the reference-to-truth odds identity used; T27 additionally derives it directly. The wave-1 reference to deterministic T22(i) at lines 159–160 is accurate as a possible future tool and is accompanied by the necessary normalized-mass qualification; Collection lines 3813–3840 and 3882–3884 support that qualification. No unproved statistical portion of T22 is imported, and no uncited budget conclusion is asserted.

**T27(i): VERIFIED.**
