# Closing correctness review of the four wave-2 proofs

Date: 2026-10-22. Final decision: **all four proofs are verified under their assigned statements. No proof edit is required.**

This certifies the mathematical implications written in the four STATEMENT files. It does not certify their remaining statistical premises, adoption into the theory, or unconditional accuracy of the production algorithm.

## Review procedure and sources

I reviewed the four statements and specified final proofs against their original conjecture parts, the shared definitions, the methodology, and the actual cited wave-1 results. Three independent GPT-6.1 Sol high-reasoning tasks were delegated through T3: T22(iii)/T27(i), T21, and T25(iv). I inspected their findings and independently checked the arguments. All returned verified. Their notes are preserved here; the decisions in this report are mine.

`BLIND.md` was saved at 2026-10-22 19:38:43 UTC, before any of the four wave-2 `CLAIMS_OF_FATAL_FLAWS.md` files was opened. I then read all four logs and adjudicated their claims below. No wave-2 `FINAL_REPORT.md`, `review/`, or `helpers/` was needed or opened. Searches of the expressly permitted wave-1 collection incidentally displayed embedded historical wave-1 review records; these were not used as mathematical evidence. This limitation is also recorded in BLIND and the T25 helper note. No wave-2 flaw log informed the blind verdicts.

All writes were confined to `WAVE2_REVIEW/`. No proof was changed and no numerical workload was run. `SOURCE_MANIFEST.json` records the principal reviewed sources; the final SHA-256 check confirmed that all 16 remained unchanged (`SOURCE_UNCHANGED_CHECK.json`). References below are to physical source lines; `Collection` means `proofs/COLLECTED/COLLECTED_PROOFS_v2.tex`. Original conjectures are in `../theorems/` relative to the proofs root.

## T22(iii): final verdict

Artifact: `T22iii_T16_start_aggregation/proof/PROOF_v1.tex`.

**Verified.** It establishes all three conclusions and the weaker-remainder variant in STATEMENT, including the exact-zero-leakage endpoint. The restatement is faithful to part (iii) with the approved EXP-to-EXP-prime change and the leakage-family NL_eta setting explicitly recorded in STATEMENT lines 7 and 49–73. The old EXP formulation is not being certified independently. G/R, within-block SE, VIS, and the NL_avg rate condition retain their stated roles. The method's prior, block construction, score, standardization, and cap are unchanged.

The substantive steps are justified:

- Lines 149–203 control all block residuals using fixed-design Gaussian tails, at most p*2^B comparisons, bounded signal energy, and bounded block rank. The proof uses raw Gaussian noise and does not assume independence after response standardization.
- Lines 205–245 derive the quadratic specialization only on the leakage family. NL_eta and Gaussian truncation give x=O_P(log(n)/n), so both the logarithmic Taylor error and the denominator-replacement error are uniformly o_P(1).
- Lines 249–330 prove the two-branch truncated Gaussian integral, sum over comparisons, and apply Markov's inequality. Correlated comparisons and correlated remainder factors cause no problem. The strict tight multiplier and weaker o_P(1) exponent are both justified.
- Lines 338–402 use VIS to dominate projected noise, then telescope the logarithmic expansion along true-variable completions. This does not use the leakage-only quadratic approximation. The resulting gain dominates every fixed polynomial penalty, proving the asserted e_n bound.
- Lines 406–465 obtain the correct eta/kappa threshold and apply precisely wave-1 T22(i-a,b). Feasibility, positivity, the u_n<1 event, random-scale O_P notation, and empty-family cases are all covered.

There is no fatal flaw or gap. Finding B1 below records a nonblocking scope boundary. No required edit.

## T21: final verdict

Artifact: `T21_T14H_HPM_composition/proof/PROOF_v2.tex`.

**Verified.** It establishes C1 and all six discovery routes in STATEMENT. The restatement faithfully makes the conjectural dependency boundary explicit: H03 is posterior concentration, H10 is the required start-addition lower bound, and H24 is uniform terminal repair plus its stated asymptotic inputs. It does not claim that G/R/SE/BM-C or LK/EXIT/GAIN have been proved to imply these hypotheses.

C1 follows at lines 63–86 from strict truth optimality when pi(S0)>1/2, an event inclusion, and Markov's inequality. Boundedness of delta1 justifies convergence of its mean. No frequentist error rate is improperly inferred from an O_P posterior rate.

| Route | Check of the final argument |
|---|---|
| (a), lines 92–178 | The full pre-final history fixes Q_f=4*N_e*(T+L+5). Fresh streams justify the fixed-count iid miss formula with the earlier-absence indicator. The nonlaunch term remains. The H10 floor, one-deletion intensity, and p proportional to sqrt(n) boundary are correct; a lower bound is not used to claim failure above that range. |
| (b), lines 180–194 | SR scores truth at the specified Gibbs execution-time configuration, including cap-boundary cases. Round-start occupancy is not substituted. |
| (c), lines 196–253 | The uniform-swap hazard is 1/[k(p-k)]. Predictable eligible opportunities support the stopped induction without independence or conditioning on their future count. D=0 and b=1 are covered. The final neighbour-swap extension uses the actual edge and correct fixed/conditional lower-bound quantifiers. |
| (d), lines 255–278 | B<=K makes block subsets feasible. A completed scan from a feasible neighbour scores truth by neighbourhood symmetry, including the last scan at the move cap. A strict-mode premise is not needed merely to score truth. |
| (e), lines 280–368 | H24's uniform one-round hit and path-exit bounds give (1-a_n)^H+H*eta_n by an endpoint-avoidance induction and first-exit union bound. Selection uses past information, future randomness is fresh, and intervening resampling is excluded. Availability and nonlaunch terms remain. The asymptotic repair claim uses exactly the explicit assumed rates. |
| (f), lines 370–396 | Completed enumeration gives the exact finite sums and tie-broken global HPM. For fixed p the branch inequality eventually holds because the model count is <=2^p and the threshold is >=4np. Resource completion and truth concentration remain separate requirements. |

The final proof has no fatal flaw or gap. The logged neighbour-swap scope issue is resolved, as detailed in R1 below. No required edit.

## T27(i): final verdict

Artifact: `T27i_T20C_cancellation_budget/proof/PROOF_v2.tex`.

**Verified.** H1–H3 faithfully express the source's fixed-length feasible chain, joint two-sided sequential ratio law, and fixed-positive normalized reference mass. The data-selected-chain qualification is correct: the selected chain itself must satisfy H2. The theorem does not derive H2 or H3 from G/R, EXP-prime, or numerical evidence. It proves only part (i). The unconditional P0 interpretation, bounded-p component interpretation, and empty-chain extension are valid.

Line 83 proves positive finite scores, including singular Gram matrices. Lines 85–109 telescope exact normalized odds and use the correct prior ratio (k+1)/(2p-k-1). The remaining factor A_(p,s,c) is bounded between (s+c)!/(2^c*s!) and (s+c)!/s!, so its logarithm is bounded even when p stays bounded. Repeated additions to a block use the successive states, not the initial state repeatedly.

Lines 111–128 correctly retain pi0(S^(0)), use H3 to make its logarithm tight, and add a fixed number of tight log remainders. Independence is unnecessary. This establishes both tightness of the mass multiplier and of its reciprocal.

The optional EXP-prime discussion at lines 140–157 is correct: under its strict uniform remainder, H2 is equivalent to max_i n*x_i=O_P(1), whereas max_i n*x_i^2=O_P(1) controls only a Taylor remainder. The final wording limits this latter uniformity to the selected chain. Findings B1–B3 below record application constraints already respected by the proof. No fatal flaw or gap remains. No required edit.

## T25(iv): final verdict

Artifact: `T25iv_T19_crossing_evidence/proof/PROOF_v1.tex`.

**Verified.** The result matches the source's conditional PW2 implication and full four-island pooling factor. The statement explicitly fixes data and successful calibration, uses nonnegative upper-bound coefficients, and excludes conditioning on later flags. It does not establish PW2 or useful values of its constants.

Lines 83–92 ensure all conditional moments are finite. Lines 94–125 correctly derive E_c[W_t*qhat_t(f)]=q_t(f) through weighting, resampling, and invariant mutation. This supplies E_c W_t=1 without assuming W_t is a martingale or that the unweighted particles are stationary.

Lines 129–158 square the exact evidence update and apply PW2 to obtain M_t<=(1+a_t/N_e)*M_(t-1)+nu_t. The explicit solution multiplies each slack only by later factors. Unbiasedness justifies subtracting 1 to obtain variance. Lines 160–176 divide the whole bound by four using independence conditional on fixed calibration; N_e remains the per-island count. Terminal rounds and local search do not change evidence.

No fatal flaw, gap, or exposition defect requiring correction was found. No required edit.

## Every logged claim and the lead's response

These rulings concern the final artifacts. They do not independently authenticate all historical claims about earlier review rounds or metadata-only version differences; those histories are unnecessary to verify the final mathematics.

### T22(iii) log

`CLAIMS_OF_FATAL_FLAWS.md` lines 3–9 reports no findings from either reviewer and no repair. There is no mathematical objection to adjudicate. My independent review agrees that the final proof needs no repair. I agree with the lead's no-change disposition.

### R1: T21 neighbour-swap probability scope

- **Location:** flaw log lines 6–18 and 31–33; final STATEMENT line 71; final proof lines 248–251.
- **Severity:** **gap in the superseded probability-scope wording, resolved**. The original statement checker itself assigned no fatal/gap severity.
- **Claim:** A merely predictable random or time-varying positive lower bound cannot be inserted unchanged as a fixed scalar into an unconditional bound delta+(1-b_*)^D.
- **Evidence:** At an opportunity the conditional miss bound may be 1-b_*, but a random b_* does not yield the claimed unconditional scalar expression without appropriate conditioning and averaging. The final text requires a deterministic common lower bound for the unconditional version. It permits a random lower bound only when measurable at the conditioning boundary and valid at every subsequent counted opportunity, then averages (1-b_*)^D. The proof implements exactly this induction and averaging.
- **Ruling:** Agree with the objection and the lead's acceptance. **The fix works.** No further edit is required.

The same log contains six affirmative scope claims at lines 22–27. Each was also checked:

| Logged scope claim | Ruling and evidence in the final artifact |
|---|---|
| H03/H10/H24 remain hypotheses | Agree. STATEMENT lines 27–38 and proof lines 23–25, 287–294, 367–368 preserve the boundary. |
| Full execution matches T11(iii); no future-success conditioning | Agree. STATEMENT line 25, proof lines 45–50 and 103–118, and Collection lines 629–632, 793–839 agree. The one-deletion intensity is explicitly on launched runs at proof line 157. |
| Occurrence/exposure/eligibility remain necessary | Agree. Routes (b)–(e) state their actual execution, exposure, scan, and availability events. None infers these events from a model relation alone. |
| Terminal repair inputs are assumed, not derived | Agree. The one-round bounds and asymptotic inputs are H24; proof lines 293–294 and 367–368 explicitly retain them. |
| The sufficient dimension range supplies no failure theorem outside it | Agree. Proof lines 162–178 distinguish a guaranteed lower bound from the actual intensity and invoke no T27 conclusion. |
| Tables belong to the ledger; unused start components may be defined on the exact branch | Agree. Method sections 6.2, 6.3 and 6.10 support STATEMENT lines 15–19 and proof lines 255–278, 370–396. |

The log's proof-review section reports no additional findings. There is no further fix to assess.

### R2 and R3: T27 Taylor-remainder uniformity, two reviewer entries

- **Location:** reviewer 1 entry at flaw-log lines 9–12; reviewer 2 entry at lines 16–19; lead answer line 21; final proof lines 152–157.
- **Severity:** **exposition, resolved**, for each entry.
- **Claim:** “Uniformly on that family” could refer to the larger optional EXP-prime family, although max_(i<c) n*x_i^2=O_P(1) controls only the selected chain.
- **Evidence:** The final sentence says “uniformly over the selected chain comparisons i=0,...,c-1.” Its displayed expression uses x_i, and the assumption is indexed by exactly those i. The Taylor inequality gives the stated uniform O_P(1) remainder on that finite selected chain; it supplies no bound on unrelated comparisons.
- **Ruling on reviewer 1:** Agree with the objection and lead response. **The fix works.**
- **Ruling on reviewer 2:** Agree with the same objection and lead response. **The same fix works.**
- **Further required edit:** none. The log's final round reports no new objection.

### T25(iv) log

`CLAIMS_OF_FATAL_FLAWS.md` lines 3–7 records no findings and no revision. There is no mathematical objection to adjudicate. I independently checked finiteness, unbiasedness, PW2, slack propagation, conditional independence, and pooling, and agree with the lead's no-change disposition.

## Cross-check of every wave-1 citation

| Use in wave 2 | Actual proved source in Collection | Hypotheses and scope check |
|---|---|---|
| T22(iii), proof lines 429–438: deterministic aggregation | T22(i-a,b), statement 3657–3662; proofs 3813–3840 | Same q,u,e and feasible reference S0; positive tables; cap included. The substituted bound requires u<1, supplied with probability tending to one. No statistical part (iii) is used to prove itself. |
| T27(i), proof lines 85–92, 166: exact reference-to-truth odds | T22(ii-a), statement 3665–3670; proof 3853–3861 | Both endpoints feasible and positive. Data-selected references are allowed because the identity holds pointwise for every reference. The identity is also derived directly. |
| T27(i), proof lines 159–160: possible normalized reference-mass bound | T22(i-a,b), 3813–3840; normalization warning 3882–3884 | Correctly offered as a future way to discharge H3 only if the lower bound stays above a fixed positive constant with probability tending to one. q<1 alone is expressly rejected as sufficient. |
| T21(a), proof lines 103–118: iid designated final calls | T11(iii), setting 629–640; proposition 793–839; theorem 844–864 | Fresh exact draws, frozen full pre-final history, fixed designated count, and full execution all match. The stronger pre-final-history conditioning is in the proved proposition, not an unsupported strengthening of the theorem. |
| T21(d), proof lines 263–270: scan scores a feasible neighbour | T20(ii-A), 3354–3366, specifically first step 3358 | The full clause assumes strict truth optimality for later movement/certification. Its scoring step uses only symmetry, feasibility, and completed execution. T21 isolates and independently proves that step, so it does not discard a needed hypothesis. |
| T21(f), proof lines 387–389: exact start component | T09(i), 331–355 | Exact convolution/backward sampling for positive tables and the capped size prior, with fresh independent uniforms. T21 correctly says this is not needed for direct exact-enumeration identities. |
| T25(iv), proof lines 94–96: stagewise weighted identity | T12(i.a), statement 1225; proof 1366–1378 | Same exact initial normalizer and iid start, weighting, multinomial resampling, and invariant round. T25 also gives the induction directly. |
| T25(iv), proof lines 94–96, 175–182: conditional calibration version | T12(iii), statement 1233; freezing and proof 1404–1421 | Data fixed, calibration determined before fresh final streams, full ideal execution, and no later diagnostic conditioning. |
| T25(iv), proof lines 160–176: island independence | T12(iv.c), statement 1240; proof 1471–1472 | Independence is conditional on fixed calibration, not asserted after averaging over calibration. Divides the entire variance bound by four. |

T12's exact-start input is T09(i). T25 supplies the same exact sampler/normalizer setting, and Collection T09(i), lines 342–355, proves it. The q_t-invariance used in T25 is proved within Collection T12 at lines 1303–1329; it is not an unproved extra statistical assumption. No citation imports the wave-1 collection's unrelated conditional statistical conclusions.

## All remaining findings and hypothesis compatibility

The three blind findings are retained unchanged. They are nonblocking application constraints already respected by the proofs.

**B1.** Location: T22 proof lines 205–245 and 362–381; T27 proof lines 133–157. Severity: **exposition**. Claim: the leakage-family quadratic approximation cannot establish cancellation along missing-true-variable additions. Evidence: the index families differ; even on a common family EXP-prime requires max_i n*x_i=O_P(1) for H2, not merely max_i n*x_i^2=O_P(1). T22 uses logarithmic telescoping for true completions, and T27 retains H2 separately. Required edit: none.

**B2.** Location: T22 conclusion, proof lines 126–140 and 440–465; T27 H1/H3, lines 46–68. Severity: **exposition**. Claim: T22's truth-concentration regime and T27's c>=1 cancellation regime cannot both apply on the same sequence. Evidence: pi0(S^(0))<=1-pi0(S0) for every proper-subset reference, so T22 concentration contradicts T27's positive-reference-mass H3; conversely T27's mass law gives pi0(S0)->0. This is not a contradiction between the conditional theorems: their hypotheses describe alternative regimes. T27 actually refers only to deterministic T22(i), which is valid in either regime when its own conditions hold. Required edit: none.

**B3.** Location: T27 proof lines 63–68, 111–128, 159–160; Collection 3813–3840 and 3882–3884. Severity: **exposition**. Claim: q<1 or an unnormalized table-product bound cannot replace normalized H3. Evidence: (1-q)^(s+1)/(1+e)^s can approach zero despite q<1, and the exact mass identity retains the reference probability. T27 explicitly respects this requirement. Required edit: none.

Other compatibility checks passed. All four use the same standardized working-model score, capped BB(1,p) prior, positive start tables, and B<=16 block rule. T22's P0 is its fixed-design Gaussian data law; T27 is a conditional implication needing only its stated stochastic premises; T21's finite bounds hold for any data law with its explicit algorithmic assumptions; T25 fixes data and calibration. These different scopes do not silently import one another's hypotheses. T21's one-deletion positive-mass route is an alternative sufficient route, not a consequence of T22 truth concentration. Successful execution is treated as execution of the specified ideal run, not selection of favorable realized outcomes.

## Circular-dependence check

The used proof dependencies are acyclic:

- T09(i) supplies exact start sampling to T12; T12's first moments and conditional independence support T25(iv). T11(iii) proves its own exact-sampler and fresh-call argument, so it needs no T09 dependency.
- Deterministic T22(i) supports T22(iii); deterministic T22(ii-a) supports T27(i), which also proves the identity directly.
- T11(iii), the elementary scan step of T20(ii-A), and explicitly assumed H03/H10/H24 support T21. The other ledger facts are proved inside T21.

The wave-1 T22(iv-c) corollary assumes T22(iii), but T22(iii) does not use that corollary. T21 does not use T27's budget interpretation, and T27(i) does not use T21. T25(iv) assumes PW2 and does not use downstream T15/T23 consequences to establish it. Broad “used by” lists in the architecture are not treated as proved inputs. There is no circular reasoning in the four final proofs.

## Required edits

**None.** No replacement wording is required in any final proof or assigned STATEMENT. R1, R2, and R3 are already resolved in the final versions. B1–B3 require care in future applications, not changes to these proofs. No repair has been made by this reviewer.

## Summary for the managing lead

| Theorem | Reviewed final proof | Blind verdict | Final verdict | Required edits |
|---|---|---|---|---|
| T22(iii) | PROOF_v1.tex | verified | **verified** | none |
| T21 | PROOF_v2.tex | verified | **verified** | none |
| T27(i) | PROOF_v2.tex | verified | **verified** | none |
| T25(iv) | PROOF_v1.tex | verified | **verified** | none |

All four proofs establish their assigned conditional statements.
Every logged objection is resolved; no fatal flaw or unresolved proof gap remains.
The wave-1 citations match, and the used dependencies contain no cycle.
Keep EXP-prime/VIS/leakage conditions, H03/H10/H24, H2/H3, and PW2 explicit where applicable.
T22 concentration and T27 cancellation describe different regimes; do not combine their conclusions on one sequence.
No proof files were edited.
