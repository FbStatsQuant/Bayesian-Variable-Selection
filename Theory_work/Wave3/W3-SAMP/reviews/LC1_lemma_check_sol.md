# LC1 — adversarial lemma-by-lemma check

Reviewer: Codex gpt-6.1-sol, high effort. Date: 2026-11-09.
Scope: locked STATEMENT v2; all seven requested proof files; the specified T12 and W1 imports; cited production code; all four numerical drivers and their saved results. Read-only review except this file. No git state changes, source edits, or delegated reviewers.

**Overall verdict: GAP for the complete locked package, because LT-f's asymptotic sharpness assertions are not established.** The principal finite-sample arguments survive the adversarial check. In particular, I find no defect in LT's simultaneous-coordinate decomposition, its unweighted leave bound, or C's stopped-sum argument. There is also a concrete false description of the R interface, and a malformed off-success-event expression in D's asymptotic proof. Both have small repairs that preserve the mathematical component results.

| Result | Verdict | Scope of qualification |
|---|---|---|
| CC | VERIFIED WITH AMENDMENTS | CC1–CC7's substantive code facts hold; the surrounding claim about arbitrary parameters through `v3_frozen` needs correction (issue 1). |
| PC | VERIFIED | Equality of the latent computation on completed runs; it does not assert that all populations are serialized. |
| MR | VERIFIED WITH AMENDMENTS | The extension is complete; correct the account of differences between engine versions (issue 4). |
| ST | VERIFIED WITH AMENDMENTS | Proof correct; numerical-summary formula has the wrong truth indicator (issue 5). |
| D | VERIFIED WITH AMENDMENTS | D-i–D-iv hold; repair D-iv's displayed integrand (issue 2), and the interface description inherited from issue 1. |
| LT♯ | GAP | LT-a–LT-e verified; LT-f's “cannot be dropped / not necessary” claims lack asymptotic witnesses in the stated domain (issue 3). Numerical sharpness description also needs correction (issue 6). |
| C | VERIFIED WITH AMENDMENTS | C-i–C-v and constants hold; clarify interface scope and update the posterior-rate citation (issues 1, 7). |

No CRITICAL issue found. “VERIFIED” here means conditional on the explicitly named imported premises and their recorded statuses; it does not upgrade START/KERNEL or prove the idealizations for floating point or seeded pseudorandom streams.

## Numbered findings

### 1. MAJOR — custom N and L in `v3_frozen` do not reach the production runner

Locations: `STATEMENT.md:36-39`; `lemmas/CC_code_check.md:102-103` (read with the component-interface assertion); `Scripts/SMC_BVS/core/v3_run.R:68-75,88-92,223-228`; `cpp/v3_core.cpp:396,446`.

The locked statement says the arbitrary frozen N_e ≥ 1 and L ≥ 0 regime is “as accepted by `v3_frozen`.” The constructor indeed stores `fr$N` and `fr$L`, but `v3_run_settings` takes **both** N and L from `setup$budgets`, not from those fields. `v3_final_run` passes that `ro` to C++, and C++ calls `run_island` with `o.N` and `o.L`. For example, storing N = 1 and L = 0 in a frozen object does not make the ordinary final-run wrapper execute those settings. The grid does reach C++ unchanged.

This is a false code-interface claim, not a counterexample to the arbitrary-parameter mathematical island. `Engine::run_island(r,N,grid,L,4,...)` is the appropriate component entry point. PC and all production results remain correct when N_e and L mean the settings actually executed. D's exact draw count is wrong if one substitutes the ignored `frozen$N` and `frozen$L`.

Suggested fix: identify arbitrary-parameter results with the engine component, and explicitly say that the public production wrapper obtains N_e and L from its budgets. Keep the arbitrary-grid statement for `v3_frozen`. No code change is required for the theory repair. Do not silently change the production code during a proof disposition.

### 2. MINOR — D-iv's displayed exponential does not vanish off 𝒜

Location: `lemmas/D_theorem.md:52-54`.

The written upper bound is `E[min(1, exp(-1_𝒜 D_r π₀(S₀)))]`. Under the ordinary zero extension of the product, its integrand equals 1 on 𝒜ᶜ. P-OVL does not require P(𝒜ᶜ) → 0. Thus the displayed bound need not tend to zero. The following parenthetical says the term is zero there, but that is not the displayed formula. The convention that the overlap is infinity off 𝒜 must be attached to the *whole overlap variable*, not to ordinary multiplication by an indicator.

Suggested fix: use `E[1_𝒜 exp(-D_r π₀(S₀))] → 0`, defining this integrand to be zero off 𝒜; equivalently define Q = D_r π₀(S₀) on 𝒜 and Q = ∞ off 𝒜, then use E[e^{-Q}]. P-OVL gives convergence in probability to zero of the bounded integrand, hence convergence of its expectation. This fully repairs D-iv without any launch-probability assumption.

### 3. MAJOR — finite numerical probes do not establish LT-f's asymptotic assertions

Locations: `lemmas/LT_theorem.md:66-70`; locked `STATEMENT.md:112-114`; `ASSUMPTION_MAP.md:12-13`; `numerics/run_checks.py:93-120`; `numerics/RESULTS_v1_sec4b.txt:4-6`.

NC_r is a sequence-level property: `lim_{η↓0} limsup_n P(𝒜 ∩ {W_r < η}) = 0`. A tiny W at one fixed problem, or P(W < .01) near one, does not demonstrate failure of NC_r. Indeed every fixed finite target has the deterministic positive lower bound W ≥ exp(min d − max d). Repeating a fixed target and bridge therefore satisfies NC_r, however tiny its typical W may look at .01. The analogous point applies to P-CONC: a displayed δ = .0099 is not δ_n → 0.

Likewise, 0.9% error at tolerance .1 at one finite problem does not prove consistency while NC_r fails. There is no asymptotic construction or proof in the cited assumption-map rows. The trap and near targets also specify arbitrary positive γ₀ and γ₁. That is legitimate for testing T12 §1–§2, but it is not a demonstrated realization of the locked regression target and its block-product start. The v2 regression examples test identities and inequalities; they do not supply these missing sharpness constructions.

The proof appropriately calls the trap a finite illustration at line 69; that caveat does not discharge the categorical locked LT-f clause or the corresponding assumption-map claims.

Suggested fix: either (a) downgrade LT-f to “these probes illustrate why a lower-tail premise is useful and suggest it may be replaceable,” explicitly leaving necessity/non-necessity unresolved, or (b) provide rigorous triangular-array witnesses. For “cannot be dropped,” prove P-CONC, nonvanishing output error, and failure of NC in an admissible sequence. For “not necessary,” prove output consistency and failure of NC in another admissible sequence. If witnesses use arbitrary targets, label that broader component domain and explain the logical limit for the regression claim. The finite-sample transfer bounds LT-a–LT-d and the sufficiency theorem LT-e do not depend on settling this issue.

### 4. MINOR — MR overstates what changed between the engines

Location: `lemmas/MR_identities.md:14-16`.

The engine does not differ “only by the removed write-only plain-PIP lines.” The actual diff also changes the local-search signature and phase assignment, as CC's header correctly records. The ledger also gains PH_LS0 while losing the registry hook. None changes the island's statistical transitions.

Suggested fix: say **the island computation** differs only by removal of write-only plain-PIP lines; explicitly refer to the harmless local-search and ledger differences listed in CC. I compared the actual files: `v3_score.h` and `v3_util.h` are identical to the frozen tree, and the changed portion of `v3_start.h` is the later start-mode machinery, not `draw_pi0` or the start tables. This does not create a measurability or freezing gap.

### 5. MINOR — ST's numerical summary prints an incorrect formula

Locations: `lemmas/ST_stay.md:50-52`; `numerics/run_checks.py:40`; corresponding labels in `RESULTS_v1.txt:5,11,17`.

`Σ_j |o_j(S₀) − 1|` is not the Gibbs leave sum unless all coordinates belong to S₀. The tested cases include absent coordinates. The simulator actually computes the correct expression, subtracting `1{j ∈ S₀}` (`samp_sim.py:180-184`).

Suggested fix: replace the printed/prose “1” with the truth indicator. ST-b's proof already uses the correct formula; no change to its bound is needed.

### 6. MINOR — the numerical filter does not select particles that stayed at S₀ throughout all measured rounds

Locations: `lemmas/LT_theorem.md:79-81`; `numerics/run_checks.py:76`; `RESULTS_v1.txt:36`.

The filter requires A_1 = ... = A_4 = 1 and Λ_1 = ... = Λ_4 = 0, but omits A_0 = 1. A particle that enters the first measured round away from S₀, moves to S₀, and remains there satisfies this filter: Λ counts only departures by particles **entering at** S₀. Thus the reported minimum error 0.067458 versus κ₀ = 0.070626 is not evidence that an everywhere-at-S₀ path can have error different from κ₀. For a genuinely good path the error equals κ₀ exactly in ideal arithmetic.

Suggested fix: also require `R['A'][:,0] == 1` (or all columns of A equal one), retain the zero-Λ filter, and handle an empty selected sample. Alternatively remove this numerical sharpness sentence: the deterministic equality already establishes the conditional pathwise fact.

### 7. MINOR — the external posterior-rate line citation has moved

Location: locked `STATEMENT.md:55-58` (P-CONC source); related rate references in `lemmas/C_theorem.md:63-64`.

The current W3-POST statement places Theorem 1 and its rate at `Theory_work/Wave3/W3-POST/STATEMENT.md:79-80`; lines 76–77 now contain source/status information. The substantive rate is present, with its antecedents. It states δ_n = O_P(r_n); obtaining o₁ = O_P(r_n) also uses δ_n → 0 and `o₁ = δ_n/(1−δ_n)`. That implication is valid, but worth making explicit in C's corollary.

Suggested fix: refresh the source range and add that one-line implication. With p ≤ n^A, the production ceiling gives T = O(log² n), so T r_n = O(log^{5/2} n / √n) → 0 as required.

## Detailed proof check

### CC — code paths and ledger semantics

I checked the cited current production ranges directly, not only the existing CITECHECK file. The following anchors support the claims (paths below are relative to `Scripts/SMC_BVS/core/`):

| Claim | Checked source anchors | Assessment |
|---|---|---|
| Initial/proposal draws, scoring before accept, exact count | `cpp/v3_engine.h:108,182-192,195-218,286-292,303-339,343-365`; `cpp/v3_start.h:158-176` | Exactly N initial calls and one I label per particle per round. No hidden extra draw in the final island. |
| Stream assignment and final islands | `cpp/v3_core.cpp:443-452` | Serial islands, independently seeded stream indices 10–13; probabilistic independence is an idealized premise. |
| Cache and first offers | `cpp/v3_engine.h:89-105`; `cpp/v3_score.h:271-292`; `cpp/v3_core.cpp:407-411` | Empty run-owned cache; exact scores independent of cache history. Cache clearing causes repeated offers only. |
| Ledger HPM and tie order | `cpp/v3_ledger.h:43-57,84-113`; `cpp/v3_util.h:121-126` | Offers preserve the total-order maximum; all earlier losing offers remain irrelevant even if evicted from top stores. |
| Tables, inheritance, final local search, LS0 | `cpp/v3_core.cpp:372-386,418-429,456,476`; `cpp/v3_start.h:89-95`; `cpp/v3_engine.h:379-405` | Tables/inherited models feasible; final-search un-emitted centre is already offered; LS0 centre is emitted. |
| RB, pooling, strict MPM threshold, evidence | `cpp/v3_engine.h:113-132,299,317-322,350-365`; `v3_run.R:142-163` | RB records the pre-uniform conditional. Equal island pooling; evidence pooled on its original scale. |
| State-space preservation | `cpp/v3_engine.h:116,146-180,397`; `cpp/v3_core.cpp:425`; `cpp/v3_start.h:92` | All models offered are in Ω. |
| Production ceiling/budgets | `v3_preprocess.R:19-30`; `cpp/v3_calib.h:30-45,89-94`; `v3_calib.R:122-124`; `v3_run.R:88-92` | Constructed grid fails above T_e; pilot has the floor and terminal snap; tiers are 0 and 1. B ≤ 16. |

The `4676af6`–HEAD diff restricted to `Scripts/SMC_BVS/core` is empty. The engine/ledger differences against the frozen v2.2.1 copy are those discussed above. Normalization `Σ e^F = Z`, used in the ledger lower bound, is correct: `cpp/v3_score.h:63-70` normalizes the capped prior, and engine line 97 adds the full marginal log likelihood.

### PC — completed versus potential records

Lines 10–19: correct. The bridge guard is the only island early return; it sets `partial`, which changes the run status at core line 451. Later local-search/LS0 checks can only change status away from completed. Under EX-A, cache/ledger/clock history changes timing or stopping, not the statistical computation. A completed run therefore follows the same statistical computation as the uninterrupted island on the same stream, including all latent populations and the RB accumulator. This does not assert that all populations appear in `IslandResult`.

Lines 21–28: correct. Reported fields are assembled from complete island results. A cache hit need not cause a new HPM offer because its first inserting evaluation already did; the one un-emitted centre is already the running HPM. The ledger inclusion is valid for the *set of all offers*, not just the bounded top store.

Lines 30–31: correct for corresponding measurable error events. `v3_fit.R:154-162` returns before launching finals when calibration fails. “Completed” in this ticket excludes the separately labelled exact branch. There is no conditioning on completion here.

### MR — full extension, including prefixes and random indices

Lines 34–45: each imported clause says exactly what is used. T12 (i.a), (i.b), (i.c), (ii) are at statement lines 59–64. The prefix κ(σ) = σ⁻¹(ℓ)−1 depends only on order, not on the trajectory. The Gibbs conditional includes the capped-addition case.

Lines 47–54: the augmented record really contains orders and full within-round paths (`W1-N1/L1_bridge.md:14-20`). Reading the state at a permutation-defined position is measurable. Integer-valued N_e, T, L give a countable measurable partition; one need not assume bounded N_e, T or L over calibration outcomes.

Lines 56–63: the data-dependent but calibration-uniform bound on Ẑ_t/Z_t is correct, also at t = 0 and at terminal times. Thus bounded measurable freezing applies at fixed data, exactly as stated in `PROOF_v6.tex:157-162`. No independence between final islands is needed. The admissible h class has the necessary deterministic bound and calibration measurability.

The use downstream of s = L + q − 1 and t = T is legitimate despite the fixed-index wording: take the countable intersection of the fixed-index almost-sure identities, then restrict to cells {L = l} or {T = t}. No uncountable exceptional-set selection occurs. The same device justifies summing to the calibration-measurable T in C. Explicitly stating this would improve exposition, but its omission is not a gap.

### ST and LT — simultaneous pre-step states and the unweighted expectation

ST-a's stationarity flux calculation is exact and uses no reversibility. ST-b sums distinct feasible Hamming-one neighbours, so the p Gibbs leave probabilities sum to at most o₁ without a factor p. In ST-c the first-exit decomposition is conditioned on the order. Each preceding-stay probability is at most one, and the order contains each label once. Gibbs contributes o₁, U and I contribute 2o₁, and B neighbour labels contribute Bo₁: λ₀ ≤ (B+3)o₁ ≤ 19o₁. The argument presumes the fresh-step conditional Markov law, supplied here by KERNEL/H-U and the code bridge.

LT lines 15–21: the good-pair event requires being at S₀ at **every** within-round time. It consequently includes every Gibbs pre-step state, simultaneously across coordinates. Bad pairs form the disjoint union of entering-away pairs and entering-at-S₀/ever-leaving pairs. All good terms have error at most κ₀, all other terms at most one. The triangle inequality gives (1) with room to spare; a union over j would be unnecessary.

LT lines 25–31: weighted endpoint error is δ by MR-b. For the unweighted quantity, fix c first and condition on the population-round history. R3 gives the fresh round law for every entering particle, including its order. ST-c bounds its departure probability by λ₀ on the event it enters at S₀. Therefore `E_c[Λ_q | H_q] ≤ λ₀(1−B_q)`; independence across particles is not needed to sum these expectations. Λ̄ is a bounded measurable function of the augmented path record. Single-stream freezing then gives the claimed unweighted bound conditional on 𝓒, localized to 𝒜. There is no illicit conversion from a W-weighted expectation to an unweighted one.

LT lines 35–49: Markov, lower-tail splitting, all constants, strict MPM threshold/ties, and the HPM implication check out. In particular ε = 1/8 gives 8 and 152, with κ₀ ≤ 1/4 on the event used.

LT lines 53–64: the integrations are valid. For fixed η, bounded random upper bounds converge in probability to zero and hence in expectation; then η decreases using NC. “Bounded convergence” here should be understood as this elementary bounded-convergence-in-probability implication, not as an unstated almost-sure limit. There is no requirement that 𝒜 or completion have probability tending to one. Transfer to reported fields uses PC only after taking unconditional intersections.

LT-f's discharge by C and the one-sided ledger falsifier are valid. The finite numerical necessity/non-necessity assertions are the unresolved part described in issue 3. “No output certifies” should be read as lack of a supplied general lower-bound certificate, not as a separately proved impossibility theorem about every conceivable diagnostic.

### D — adaptive uniform consumption does not destroy iid proposals

Lines 7–22: correct. At fixed c the number of calls is deterministic. Each start time is a stopping time in the consumed-uniform filtration. Past draws are measurable before the next call. The iid-sequence strong Markov property gives a fresh continuation; `draw_pi0` reads only this continuation and fixed start tables, not the entering state. Its variable consumption count is bounded by 1+2J. Thus sequential draw values are iid π₀ even though the gaps between calls depend on earlier moves. Scoring every proposal before accept makes the discovery inclusion correct, including rejected proposals.

Lines 24–35: augmenting the record by rejected proposals is needed and done. A finite algorithm on each parameter cell is jointly measurable. Product freezing for D-ii uses precisely IND-T; no unjustified fourfold improvement is made under SI alone.

Lines 39–50: π(S₀)>1/2 implies unique maximal F, so discovery plus completion implies the reported HPM is S₀. The unconditional bound and N₀(L+6) production lower bound are correct. Lines 52–54 need issue 2's repair; thereafter the integration argument proves the claimed limit.

### C — stage identities are used correctly in the stopped sum

Lines 13–15: finite-sum Hölder bounds the bridge odds by max(o₀,o₁), including the endpoint cases separately.

Lines 19–23: every stage factor dominates the S₀ contribution of its entering population. The normalizer ratio is q_t(S₀)/π₀(S₀). The product bound and positive-part inequality are correct, including t = 0 via the empty product.

Lines 27–35: the first crossing of u is included in Y, so min(U,u) ≤ Y even if it overshoots or occurs at t = 0. On the predictable event {V_{t−1} ≤ u}, the *deterministic* product lower bound gives W_t ≥ (1−u)/(1+δ̄). Dropping the indicator on the nonnegative W_t x_t side permits use of the **unconditional-in-the-island**, stagewise MR-a identity. No stagewise identity is being asserted conditional on the crossing event. This is precisely why no optional-stopping theorem is necessary. Summing t = 0,...,T yields the claimed bound. The factor 4 is valid.

Lines 39–50: the product lower bound controls (1−W)⁺. Mean-one W gives E|W−1| = 2E(1−W)⁺. The arithmetic `2o₁+8(T+1)δ̄ ≤ 18Tδ̄` holds for T ≥ 1. Pooling needs only the triangle inequality. Applying LT with η = 1/2 gives 21o₁/ε + 36Tδ̄. Initial iid draws give the discovery bound (1−π₀(S₀))^{N_e} ≤ δ₀ ≤ δ̄.

Lines 54–64: all asymptotic events remain intersected with 𝒜 or completion. Bounds truncated at one can be integrated without moment assumptions on Tδ̄. The logarithm inclusion is valid for both tails. C implies NC even if 𝒜 has small probability. Constants 63 and 168 come from ε/3 and 1/8 respectively. The production corollary is correct after the scope/citation corrections above.

## Simulator and numerical-evidence audit

**Simulator verdict: VERIFIED as a floating-point simulation of T12 §1–§2 on the supplied positive finite targets.** It is not literally an exact-arithmetic implementation, and is not a production block-construction/start-sampler validation. Those limits matter chiefly for issue 3, not for the finite-state identity tests.

I inspected every line of `samp_sim.py`:

- Lines 21–58 enumerate capped Ω and compute normalized starts/targets and Gibbs conditionals correctly, including infeasible additions.
- Lines 74–104 implement the uniform swap, the neighbour-swap Hastings cardinality ratio, B separately labelled copies, and independence proposals. These match T12's formulas. The ring is a symmetric test graph; it need not be the graph that production constructs for those data. For p = 2 the duplicate ring entries give the same effective unique-neighbour kernel; they did not produce a counterexample in my boundary check.
- Lines 123–150 use an independent random order for each particle. At each Gibbs label RB is recorded before the transition, and `np.add.at` correctly accumulates repeated island indices. Independence proposals are explicit, counted whether accepted or rejected; their accept uniforms are fresh and independent. Other labels sample the precomputed kernel rows, which is distributionally sufficient for R3 even though uniform consumption differs from production.
- Lines 153–164 compute the log mean incremental potential before multinomial resampling, select independent ancestors conditional on weights, and then apply one round at the new temperature. Stage populations and Wstage are recorded after the round.
- Lines 165–175 retain evidence after the bridge, run L unmeasured rounds and Hm measured rounds, record A_0 and measured endpoints correctly, and divide RB by N·Hm. `away` records departures only for entering-at-S₀ particles, exactly Λ; it is not a generic ever-away indicator.
- `run_checks_v2.py:23-44` implements the stated regression marginal BF/prior and supplied block-product start up to cancelling normalization constants. The B and block partitions are test settings, not verified production-generated settings. This is adequate for the advertised component checks.

The original drivers/results were inspected, not rerun wholesale. Their MR z-scores, D counts, C product/stopped bounds, and regression-score formulas match the tested expressions. Many reported probability upper bounds exceed one, so zero numerical violations alone provides weak evidence; the analytic audit is doing the substantive verification.

Additional independent boundary run during this review: seed 813, 15,000 islands each, p/K = 1/1, 2/1, 3/2, 4/2, N = 1, L = 0, B = 2, grid (0,.2,1), random positive targets, including empty S₀ and active caps. Checked pathwise LT decomposition, C-i product domination, and min(U,.5) ≤ Y: **zero violations in all 60,000 islands**. Kernel invariance residuals were at most 1.12e-16. Empirical mean W values were 0.99855, 0.99977, 1.00503, 1.00102; these are diagnostic observations, not exact proofs. Executed via an inline Python program with bytecode writing disabled; no repository scratch files were created.

Two further evidence limitations: `sec4.py` reruns a text-extracted section of the driver and only emits one near result per invocation, whereas the saved sec4b file includes both L = 5 and L = 20 near rows. It is evidently a combined log, not the pristine stdout of one invocation of the current script. Also, “P-CONC holds, NC fails” in those logs is an unsupported sequence-level interpretation, not something measured by the simulator. Preserve the useful finite measurements, label their assembly/settings, and remove the asymptotic interpretation unless issue 3 is resolved analytically.

## Required disposition

Repair issues 1–2 and qualify or prove LT-f as in issue 3 before treating the whole locked package as checked. Issues 4–7 are local exposition/evidence corrections. The successful checks of LT's all-coordinate path event, unweighted freezing, and C's stopped sum do not depend on those repairs and do not require additional hypotheses.
