# Wave-2 closing correctness review: blind verdicts

Date: 2026-10-22. Reviewer: managing review agent, with three independent GPT-6.1 Sol checks through T3. Verdicts are the reviewer's own. This file was written before opening any of the four wave-2 `CLAIMS_OF_FATAL_FLAWS.md` files. No wave-2 `FINAL_REPORT.md`, `review/`, or `helpers/` was read. All writes are confined to `WAVE2_REVIEW/`; no proof was edited.

The explicitly permitted wave-1 collection includes historical review material alongside its proofs. Searches incidentally displayed some of those wave-1 records; they were not used as correctness evidence. The blind verdicts below concern the four wave-2 proofs, whose prior review and flaw records remained unopened. The T25 helper separately disclosed the same collection-search limitation.

Sources: each assigned STATEMENT and final proof; the original theorem files, including T03/T10/T24 for T21's assumptions; `theorems/00_COMMON.md`; relevant method definitions in `THEORY_BRIEF.md` and `METHODOLOGY_v3.md`; and the cited mathematical statements/proofs in `COLLECTED/COLLECTED_PROOFS_v2.tex`. `SOURCE_MANIFEST.json` identifies the principal inputs by SHA-256. No numerical experiment was necessary or run.

Line numbers below are physical source lines. `Collection` means `COLLECTED/COLLECTED_PROOFS_v2.tex`. Scope findings marked exposition are application constraints already handled correctly, not defects requiring edits.

## T22(iii): `T22iii_T16_start_aggregation/proof/PROOF_v1.tex`

**Statement fidelity.** The restatement preserves the source's part-(iii) rates, G/R, within-block SE, VIS, and NL_avg rate condition, with the approved EXP-to-EXP-prime change. It explicitly records leakage-family NL_eta as part of that changed setting (STATEMENT lines 7, 49–73). The strict and weaker remainder cases remain separate. The exact-block tables, capped prior, standardization, and aggregation quantities match the method and wave-1 definitions. This verdict is for that stated EXP-prime/NL_eta formulation, not a claim that the old quadratic EXP assumption has been proved.

**Proof check.** Lines 149–203 obtain uniform residual control over at most p*2^B deterministic projections from fixed-design Gaussian tails, bounded signal energy, and B <= 16. The decomposition uses raw Gaussian noise; it does not assume standardized errors are independent Gaussians. Lines 205–245 combine NL_eta with Gaussian truncation to prove the uniform small-partial-R-squared regime and the o_P(1) quadratic-approximation error on the leakage family.

The two-branch integral bound at lines 249–279 is correct, including zero leakage and zero residual-signal variance. Lines 289–330 use linearity, maximum <= sum, and Markov's inequality; no comparison independence or independence from the EXP-prime remainder is needed. The weaker random exponent is explicitly constructed. Lines 338–402 use VIS to dominate projected noise uniformly, then telescope the logarithmic expansion along true completions. No leakage-only approximation is used there. The gain dominates every fixed polynomial penalty and proves the asserted rate for e_n.

The admissible kappa calculation at lines 406–424 gives the stated strict eta threshold and kappa=1/2 at zero leakage. Lines 429–465 correctly apply wave-1 T22(i-a,b): Collection lines 3657–3662 and 3813–3840 establish exactly the capped aggregation bounds and q <= u used here. Positivity, feasibility, and the u<1 event are supplied. Empty truth and p=s0 are covered. The random-scale O_P notation is justified by the displayed ratio bound.

**Finding B1.** Location: this proof lines 205–245, 362–381; T27 proof lines 133–157. Severity: **exposition**. Claim: leakage control and EXP-prime alone must not be treated as T27's sequential cancellation law. Evidence: the leakage family adds false variables after the block truth is present, whereas the cancellation chain adds missing true variables. T27 correctly requires tightness of max_i n*x_i under its optional EXP-prime assumption; tightness of max_i n*x_i^2 alone controls only a Taylor remainder. Both proofs respect this distinction. Required edit: none.

No fatal flaw or proof gap found. Every asserted conclusion follows from the stated hypotheses.

**Blind verdict: verified.**

## T21: `T21_T14H_HPM_composition/proof/PROOF_v2.tex`

**Statement fidelity.** C1 and all six source routes are retained. H03/H10/H24 explicitly replace uses of the corresponding unproved results with hypotheses. This is a conditional composition theorem: it does not establish T03 from G/R/SE/BM-C, T10 in full, or T24 from leakage/exit/gain conditions. Availability, full execution, and the nonlaunch term are made explicit without changing the algorithm or silently conditioning on future success.

**Proof check.** Lines 63–86 prove C1 directly using strict truth optimality on pi(S0)>1/2 and Markov's inequality. Boundedness of delta1 converts convergence in probability to convergence of its mean; no unsupported frequentist rate is asserted.

- Route (a), lines 92–178: the fixed pre-final count is Q_f=4*N_e*(T+L+5). The fresh-stream argument gives the miss formula conditional on the full pre-final history, so the earlier-absence indicator is legitimate. Collection T11's setting at lines 629–640, reading-scheme proposition at 793–839, and theorem at 844–864 support this use. H10's one-deletion floor and its logarithmic boundary at p proportional to sqrt(n) are calculated correctly; no failure conclusion is drawn from a lower bound.
- Route (b), lines 180–194: SR scores truth at the stated execution-time configuration, including the case j is outside truth and the alternative exceeds the cap. Round-start occupancy is not substituted.
- Route (c), lines 196–253: the conditional uniform-swap hazard is 1/[k(p-k)]. The stopped-opportunity induction uses only predictable eligibility, not independence or conditioning on a future count. It covers D=0 and b=1. Neighbour swaps require the actual edge and an appropriate fixed or conditionally measurable lower bound.
- Route (d), lines 255–278: B<=K and neighbourhood symmetry justify table and completed-scan scoring. Collection T20(ii-A), lines 3354–3366, has a strict-truth-mode premise for its later move/certificate conclusions. Its first scoring step, line 3358, uses only feasibility, neighbourhood symmetry, and a completed scan. T21 identifies this distinction and independently proves the needed step.
- Route (e), lines 280–368: H24's uniform one-round hit and path-exit bounds imply the H-round bound by a first-exit union bound and an endpoint-avoidance induction. Selection uses the available past, future randomness is fresh, and no intervening resampling is assumed. Availability and nonlaunch failures remain in the bound. The fixed positive lower bound on c_n and the asymptotic assumptions give the claimed repair consequence.
- Route (f), lines 370–396: completed enumeration gives exact finite sums and the global tie-broken maximum. The branch inequality eventually holds for fixed p since its left side is <=2^p and its right side is >=4np. This does not claim actual resource completion or truth recovery without H03.

Collection T09(i), lines 342–355, establishes the cited exact start sampler/normalizer. T21 correctly says this is unnecessary for its enumeration identities. No unproved ledger clause is imported: the other scoring/opportunity facts are proved directly.

No fatal, gap, or exposition defect requiring a correction found.

**Blind verdict: verified.**

## T27(i): `T27i_T20C_cancellation_budget/proof/PROOF_v2.tex`

**Statement fidelity.** H1–H3 spell out the original fixed-length feasible chain, joint two-sided sequential log-tightness, and normalized reference-mass premise. Data-selected chains must satisfy the premise after selection. Operational assumptions are retained, but the mass implication is correctly unconditional under P0 and does not require final randomness. The bounded-p component interpretation and empty-chain extension are valid. No budget-exponent result from parts (ii)–(iv) is claimed.

**Proof check.** Line 83 proves score positivity even for singular Gram matrices. The exact odds at lines 85–109 cancel both normalizers and use the correct prior ratio (k+1)/(2p-k-1). The remaining deterministic product lies between (s+c)!/(2^c*s!) and (s+c)!/s!, including bounded p. Successive same-block additions telescope at their actual states. Lines 111–128 use H3 to bound the logarithm of the reference mass and H2 to bound the fixed sum of remainders. This gives the stated two-sided mass multiplier with no independence assumption.

The optional EXP-prime equivalence at lines 140–157 is correct and not used as a proved statistical premise. The cited wave-1 T22(ii-a) is exactly Collection lines 3665–3670 and 3853–3861; T27 also derives it directly.

**Finding B2.** Location: T22(iii) conclusion and T27 H1/H3, proof lines 46–68, 159–160. Severity: **exposition**. Claim: the two statistical regimes cannot be imposed simultaneously for c>=1. Evidence: T22 gives pi0(S0)->1, so every proper subset S^(0) has pi0(S^(0))<=1-pi0(S0)->0, even after data selection. That contradicts T27 H3. T27's own mass law instead gives pi0(S0)->0. T27 cites deterministic T22(i), not T22(iii), for a possible reference-mass bound; neither proof makes an invalid combination. Required edit: none.

**Finding B3.** Location: T27 proof lines 63–68, 111–128, 159–160; Collection lines 3813–3840, 3882–3884. Severity: **exposition**. Claim: q_n<1 or a lower bound on an unnormalized table product cannot replace H3. Evidence: the deterministic bound (1-q)^(s+1)/(1+e)^s may approach zero despite q<1, and the exact chain identity retains pi0(S^(0)). The proof correctly requires a fixed positive normalized reference-mass bound with probability tending to one. Required edit: none.

No fatal flaw or proof gap found.

**Blind verdict: verified.**

## T25(iv): `T25iv_T19_crossing_evidence/proof/PROOF_v1.tex`

**Statement fidelity.** This is exactly the source's PW2-conditional variance implication, including division of the whole bound by four. The statement makes the nonnegative upper-bound coefficient convention explicit and fixes data and successful calibration before final randomness. It does not establish PW2 from RET, OCC, COVER, or another condition.

**Proof check.** Lines 83–92 establish conditional finiteness of all moments. Lines 94–125 correctly prove the weighted empirical-measure identity by induction through resampling and invariant mutation. Thus E_c W_t=1; no martingale assertion or marginal particle stationarity is used. Collection T12(i.a), (iii), and (iv.c) match the citations: statement lines 1225, 1233, 1240; proofs 1366–1378, 1404–1421, 1471–1472. Its exact-start input is supplied by T09(i); the kernel invariance needed here is proved inside the T12 chapter at lines 1303–1329.

Lines 129–158 obtain the exact second-moment increment, apply PW2, and iterate M_t<=(1+a_t/N)M_(t-1)+nu_t. Each slack is multiplied only by later-stage factors. Subtraction of 1 is justified by unbiasedness. Lines 160–176 use conditional island independence to divide the whole bound, including slack, by four, retaining N=N_e per island. No later diagnostic conditioning or random-calibration unconditional independence is asserted.

No fatal, gap, or exposition defect requiring a correction found.

**Blind verdict: verified.**

## Blind summary

| Theorem | Final proof examined | Blind verdict | Required edits |
|---|---|---|---|
| T22(iii) | PROOF_v1.tex | verified | none |
| T21 | PROOF_v2.tex | verified | none |
| T27(i) | PROOF_v2.tex | verified | none |
| T25(iv) | PROOF_v1.tex | verified | none |

The findings are three nonblocking scope constraints; no fatal flaw or proof gap was found. The independent blind checks agree. Step 2 has not yet begun at this file's creation.
