## 1. Summary

1. **Accept:** retain the block start pending an audited ABL-START comparison; neither poor truth mass nor backfit’s start-only results justify replacement.
2. **Refine:** retain HPM, integrate LS0 additively, and attach local certification only to the actual returned model.
3. **Refine:** adopt concurrent islands and scans; fix worker state, stacking semantics, and work/depth claims before calling the implementation scalable.
4. **Refine:** retain calibration with a precise frozen-run contract; convergence and delivery remain OPEN, not inherent impossibilities.
5. **Change:** make Ẑ-weighted PIPs primary for v3.1; retain equal-weight PIPs as the study-compatible secondary output.
6. **Refine:** preserve operational flags and add the deterministic top-store underestimation certificate; passing flags never certifies accuracy.
7. **Refine:** prioritize posterior-functional accuracy; the proposed theorem list currently overstates several results and does not yet meet every proposal goal.
8. **Refine:** repair unavailable-output fields, distinguish mathematical from numerical certificates, and freeze the output convention.
9. **Meeting verdict:** approve this direction, but do not declare all methodological questions closed by relabelling missing proofs as inherent limitations.

Evidence convention: cited campaign statuses are source-reported candidate results, not independently adopted theorems. I label my own short arguments below explicitly. I inspected the repository read-only and launched no simulations or jobs. ABL-START’s report remained unavailable after the permitted fetch.

## 2. Agenda items 1–8

### Item 1 — Local-to-global versus a plain start

**Verdict: accept the block start for v3.1, provisionally pending ABL-START.**

The burden of proof favors retention. The block start has exact normalization and sampling, full support on the capped model space, and established conditional theory describing both useful reference mass and failure under masking. Tiny \(\pi_0(S_0)\) alone does not establish that the start is useless: its mass on states from which moves repair efficiently also matters.

The strongest relevant study evidence is more specific than HQ’s favorable/unfavorable classification:

- API-RESID reports median \(\log_{10}\pi_0(S_0)=-15.65\), but median \(\pi_0(R_2)=0.813\) for v3.
- Backfit raises the empirical “favorable” count to \(1,888/2,400\) after three sweeps and \(2,203/2,400\) at the last sweep.
- The latter includes 90 fits not settled within ten sweeps; 57 fits exhibited a two-cycle.
- These are start-law calculations, with no SMC evidence about posterior error or total computational cost.

Source: `origin/theory/API-RESID:theory_campaign/API-RESID/REPORT.md`, §§1–3.4, 5. Its “favorable” threshold is \(\pi_0(S_0)\ge10^{-4}\), not the asymptotic favorable-start premise. Its zero favorable v3 fits and THM-INV’s approximately one favorable fit therefore require definition reconciliation, not averaging.

**ABL-START needs an intervention audit before its results are interpreted.** Its task suggests implementing singleton blocks by setting \(B=1\). But \(B\) also controls the neighbor graph and the number of neighbor swaps, and the round has \(p+B+2\) steps. Changing those would confound a start comparison with a kernel change. Moreover,
\[
\pi_0(S)\propto w(|S|)\prod_{j\in S}r_j
\mathbf1\{|S|\le K\}
\]
is not an independent-Bernoulli law: the beta-binomial size weight and cap couple the indicators. Call this arm the **singleton-factor start**. Hold the production graph, swap count, target, and budgets fixed. The start-dependent independence proposal necessarily changes with the start and should be acknowledged.

Sources: `theory_campaign/tasks/ABL-START.md`, “Arms”; `Docs/Methodology/METHODOLOGY_v3.md`, §§6.3–6.5; `Scripts/SMC_BVS/core/cpp/v3_engine.h:72`.

**Result that would change my vote.** An audited ABL-START result showing that a plain start materially reduces total critical-path cost—including setup, pilot, rebuilds, and final sampling—while matching or improving reference-based PIP/evidence accuracy at matched total compute, without concentrated deterioration in weak S4/S5, would justify reconsideration. Reproducible paired dominance would be persuasive; unchanged HPMs or a small stage-count difference would not. A claimed reference must carry its own uncertainty: agreement with a longer run of arm A is not an exact benchmark.

For backfit, such SMC evidence must accompany an exact-normalizer/sampler proof for its frozen positive tables and a deterministic cap/cycle/fallback rule. These are **OPEN**. A proof that the iteration converges is unnecessary if the shipped method explicitly uses a bounded iteration; a claim of convergence would require one.

**Change implications if an alternative wins.** Replacing the start is **WORKHORSE**: it changes the bridge and independence proposals. Existing fits remain v3 evidence; all 2,400 would eventually need replacement to represent the new procedure. No such rerun is justified now. The cheapest decision evidence is the already commissioned ABL-START panel, at most twenty runs per arm, with no additional panel requested here.

**INHERENT LIMITATION.** A product of local factors generally cannot represent global posterior dependence. Masking and dilution can therefore damage this start. That is inherent to using the local product as an approximation, not proof that every such start is ineffective, nor a limitation of the exact endpoint target. The project’s verified separation concerns start-only/one-shot procedures; it does not establish that tempering is necessary for HPM discovery. See `origin/theory/T38-RECORD:theory_campaign/T38-RECORD/T38_STATEMENT.md`, change V11 and Remark 6.

### Item 2 — Selection rule

**Verdict: refine; retain HPM and implement LS0 without changing the sampler.**

The exact posterior mode minimizes posterior expected model-level 0–1 loss. The best-ever-scored model approximates that decision, with the computational discovery term explicitly separated by T21/T38. MPM minimizes unrestricted Hamming loss, a different objective. Neither result says that the sampled HPM is globally optimal or that it estimates the posterior distribution accurately.

Sources: `Docs/Methodology/METHODOLOGY_v3.md`, §§6.10–6.11; `origin/theory/THM-SYNTH:theory_campaign/THM-SYNTH/THEOREM_LIST.md`, R2–R5.

I support:

- Appending LS0 after the existing final run and existing final local search, with the exact start mode emitted and all stipulated scans completed.
- Preserving the old scored set, stream consumption, evidence, and PIPs.
- Keeping `local_certified` as a property of the returned model itself. A certificate for another search center must not transfer after LS0 or stacking changes the HPM.
- Reporting MPMs derived from the explicitly named PIP estimators. If an MPM exceeds \(K\), retain the specification’s disclosure rather than silently truncating it.
- Treating HPM–MPM disagreement as a descriptive difference between decisions, not an accuracy alarm or a reason to switch estimators.

**Real issue.** T38(b1)’s LS0 route is not currently a theorem about the production implementation. All production local-search calls start from the current HPM; the only LS0 is in the test export. The source records Felipe’s conditional approval and the \(0/2,394\) HPM-change result.

Sources: `origin/theory/API-AUDIT:theory_campaign/API-AUDIT/REPORT.md`, §§3–4; `origin/theory/T38-RECORD:theory_campaign/T38-RECORD/T38_STATEMENT.md`, change V1 and Parts I.A–I.B.

**Class and study effect.** LS0 is **ADDITIVE** to the uninterrupted computation. MPMs and disagreement summaries are **POST HOC**. No SMC rerun is needed for the 2,394 completed fits; reuse the existing LS0 audit, subject to production fidelity. However, zero HPM changes does not imply identical stores, certificates, flags, or wall-clock completion.

**Proof route and status.** The scored-set inclusion argument is **PROVED**: appending evaluations retains every old candidate, so the maximum under the fixed HPM order cannot decrease. This guarantees improvement in posterior score, not truth recovery. The source reports LS-score and T38(b1-LH) as **PROVED** under their stated operational/statistical conditions; I have not independently rechecked those full proofs.

**Cheapest check.** On the existing S1, S4, and S5 replay datasets and their recorded seeds, compare integrated production LS0 with the test export: unchanged stream endpoints and island outputs; identical LS0 center, scan paths, and ledger additions; certificate recomputed for the selected HPM. Add deterministic tie and move-limit cases. The registry reports LS0 median costs of 0.17 seconds at \(p=500\) and 0.37 seconds at \(p=1000\); these are existing measurements, not a guaranteed overhead bound. Source: `origin/theory/T38-RECORD:theory_campaign/T38-RECORD/REGISTRY_v2.md`, §D, rows LS0-3/4.

**INHERENT LIMITATION.** Local optimality cannot certify global optimality without additional landscape conditions. Also, an exact posterior-mode decision need not equal the generating support at finite sample size. Changing the search cannot repair a posterior ranking that places a competitor above \(S_0\).

### Item 3 — Parallel execution layer and v3.2

**Verdict: refine and adopt, with narrower equivalence claims and explicit implementation obligations.**

The proposed parallel axis is appropriate. No variable splitting is needed. Adopt (a)–(g), with these requirements:

1. **Workers isolate all mutable state.** Private engines, caches, ledgers, and RNGs are necessary. The nominally read-only `Data` object also contains mutable numerical-route counters, incremented on every score. Sharing it unchanged among C++ threads introduces unsynchronized writes. Use process-private state or private counters with a deterministic merge while sharing immutable numerical arrays.  
   Evidence: `Scripts/SMC_BVS/core/cpp/v3_score.h:20` and `:231`.

2. **Calibration workers persist their streams across rebuilds.** Restarting each worker’s stream at each iteration is a statistical change. Merge all required stores before local search and grid construction.

3. **Parallel scans preserve both orderings.** The scan winner uses strict score improvement with lexicographic ties; the HPM uses score, size, then lexicographic order. Reduce all relevant store contributions, not merely the winning neighbor.  
   Evidence: `Scripts/SMC_BVS/core/cpp/v3_engine.h:370`; `Scripts/SMC_BVS/core/cpp/v3_ledger.h:30`.

4. **Freeze default \(R'=4\), with optional \(R'=4k\) declared before final randomness and unchanged \(N_e\).** Retain streams 10–13. To preserve the old post-search HPM, also preserve the local search from the original four-island center. A better starting score need not lead greedy search to a better terminal score.

5. **Separate baseline and expanded diagnostics.** “Flags on islands 1–4” is insufficient if E1 compares them with an HPM improved by extra islands. Preserve the complete baseline diagnostic reference if bitwise baseline flags are claimed; label expanded-run diagnostics separately.

The worker/store and stacking arguments are in `origin/theory/METH-AUDIT:theory_campaign/METH-AUDIT/PROOFS.md`, Lemma S, W, W-cal, and Corollary W-R.

**Real issues.** These refinements fix concurrency correctness, reproducibility, and a false stacking-monotonicity inference. They also prevent overstating scalability.

**Class and study effect.** Concurrent islands, safe state isolation, deterministic store reductions, and correctly nested stacking are **ADDITIVE**. Weighted PIPs are **POST HOC**. Per-particle streams are **LAW-PRESERVING** under the independent-uniform idealization; changed floating-point reductions need separate numerical analysis. A Gram-free scorer preserves the mathematical target, with numerical fidelity still to establish. No completed-study SMC rerun is required for these classifications.

**Depth must be stated accurately.** With islands alone, the main sampling depth still contains \(N_e(p+B+2)\). Since \(N_0\ge p\), this becomes at least quadratic in \(p\) in elementary-step count beyond \(p=2500\). Particle parallelism removes the multiplicative population factor, but reductions retain \(O(\log N)\) depth, and setup, grid construction, local-search reductions, and pooling remain. “Free of \(N,H,R\)” is too strong for the complete algorithm.

The large-\(p\) roadmap must also address clustering and neighbor construction. Removing the scorer’s Gram matrix alone does not remove their quadratic storage/work. METH-AUDIT itself lists transient correlation/distance storage and sequential linkage merges. Source: `origin/theory/METH-AUDIT:theory_campaign/METH-AUDIT/REPORT.md`, §§2.1–2.2, 4, 7.

**Proof route and status.** Lemma S is **PROVED** by its finite-order invariant. Full implementation equivalence is a **PROOF SKETCH** for the proposed production integration until worker state, guards, reductions, and merge semantics are checked. Operation counting supports the revised depth formula; it does not establish wall-clock superiority over sequential MCMC.

**Cheapest checks.** Reuse the three named replay datasets, recorded seeds, and baseline outputs; execute W-cal, scan-path, and \(R'=8\) nesting checks together. Include a forced worker failure and a threaded-counter check if threads are used. The frozen dossier supports smoke plus two study designs, with the third pending; METH-AUDIT’s “3/3” prose is not a substitute for its unfilled §6 results table. The recorded final-run speedups are about 1.9-fold, not a demonstrated fourfold end-to-end gain.

**INHERENT LIMITATION.** The sequential \(p+B+2\) steps are inherent to this specified kernel: each update uses the preceding state. They are not inherent to SMC or BVS generally. I retain the kernel because changing it would be **WORKHORSE** and invalidate important path arguments. The current quadratic setup memory is an implementation/design limitation, not a mathematical requirement of exact posterior targeting.

### Item 4 — Calibration

**Verdict: refine the contract; keep the calibration rule and budgets.**

Frozen calibration separates validity from calibration quality. For any successfully constructed admissible grid fixed independently of the final streams, the relevant island identities do not require rebuild convergence or diagnostic success. This supports keeping calibration while stating exactly what it guarantees.

The contract should distinguish:

- A valid grid from a grid that stopped changing.
- Restricted ESS control on \(V\) from full-space weight control.
- Successful output from `schedule_limit`, resource stops, and numerical failure.
- Final diagnostic failure from permission to alter or replace final estimates.

Sources: `Docs/Methodology/METHODOLOGY_v3.md`, §§6.6–6.9; `Scripts/SMC_BVS/core/v3_calib.R:84`; `origin/theory/THM-INV:theory_campaign/THM-INV/REPORT.md`, §1 rows 5 and 7.

**Real issue.** The current theory can be misread as proving that the rebuild loop converges, finds the relevant modes, or yields a sufficiently accurate bridge. It proves none of those generally. Shortening calibration also changes discovery opportunities and the law of the schedule.

**Class and study effect.** Contract clarification is **ADDITIVE** specification work; concurrent diagnostics are **ADDITIVE** execution work. Study effect: **none**. Fewer rebuilds or smaller pilots would be **WORKHORSE** and are rejected now.

**Proof route and status.** Frozen-run validity follows the T12/Prop. 2 route, source-reported **PROVED** under its assumptions. The bounded loop is a direct code property. Rebuild convergence, relevant-mode coverage, and a useful bound on \(P(\texttt{schedule_limit})\) are **OPEN**. Theorem G and ideal-grid crossing results do not close those questions.

**Cheapest check.** First perform W-cal replay on the three existing datasets, including a case with multiple rebuilds or escalation. Deterministically exercise successful, unconverged, and construction-failure returns. Inspect saved calibration traces across the existing study without refitting. This is substantially cheaper than testing a replacement schedule and directly tests the claimed contract.

**INHERENT LIMITATION.** A diagnostic restricted to a discovered set cannot, without additional information, control undiscovered mass. However, lack of a rebuild-convergence theorem or delivery bound is merely **OPEN**. Neither is an established inherent failure of SMC.

### Item 5 — Primary PIP

**Verdict: change to Ẑ-weighted primary PIPs; preserve equal-weight PIPs explicitly.**

This is the reporting choice aligned with the intended island-scaling strategy. Conditional on frozen calibration, let \(W_r=\widehat Z_r/Z\) and \(a_{rj}\) be island \(r\)’s PIP. The island identities give
\[
E[W_r]=1,\qquad E[W_ra_{rj}]=\pi_j.
\]
Consequently,
\[
\frac{\sum_rW_ra_{rj}}{\sum_rW_r}\longrightarrow\pi_j,
\qquad
\frac1R\sum_ra_{rj}\longrightarrow E[a_{1j}].
\]
The latter retains any single-island bias. These are **PROVED** consequences of the identities and the strong law for conditionally iid integrable islands.

Source: `origin/theory/METH-AUDIT:theory_campaign/METH-AUDIT/PROOFS.md`, Proposition P(i)–(ii). The secondary weighted estimator is already specified but missing from assembly: `Docs/Methodology/METHODOLOGY_v3.md`, §6.11; `Scripts/SMC_BVS/core/v3_run.R:117`.

This does **not** prove lower MSE for weighted PIPs at \(R=4\). Rare large evidence weights can make them unstable. Neither normalized estimator is generally unbiased at finite budgets. My primary-label choice is a judgment based on the asymptotic axis the paper intends to exploit, not evidence of finite-budget dominance.

**Real issue.** Keeping a primary estimator whose bias does not disappear under island stacking conflicts with the stated posterior-accuracy objective and the proposed scaling argument.

**Class and study effect.** **POST HOC.** Recompute weighted PIPs and their MPM from saved `log_Z_r` and `pip_r` for available fits. Preserve the original equal-weight fields and label all new summaries clearly; do not silently reinterpret historical values. No SMC rerun and no HPM change. Stopped fits receive no posterior estimate.

**Proof route and status.** Proposition P(ii) above is **PROVED** under the island identities. Useful finite-\(R\) precision under study masking is **OPEN**; the second-moment constant may be prohibitive.

**Cheapest check.** Recompute both poolings on the 2,394 completed fits, verifying log-sum-exp normalization and model-index alignment. Cost is \(O(Rp)\) per fit, with no new scores. Compare reference-based error on ABL-START’s benchmark subset; do not use proximity to the binary truth as a substitute for posterior-PIP accuracy.

**INHERENT LIMITATION.** Equal pooling’s persistent bias is inherent to averaging biased island estimators at fixed \(N\). Finite-\(R\) variability is unavoidable, but severe evidence-weight concentration is not a universal property of SMC and must not be declared inevitable for the production grid.

### Item 6 — Flags and diagnostics

**Verdict: refine; retain existing operational flags and add one positive, one-sided certificate.**

E1–E3 have interpretable operational content: an observed score discrepancy, evidence-estimate disagreement, or an observed search improvement. Their failure to fire does not imply accuracy. Preserve their calibration role to avoid changing the schedule policy, but do not market them as validated accuracy tests.

Add the top-store evidence sum
\[
Z_{\mathcal T}=\sum_{S\in\mathcal T}\varpi(S)m(S)
\]
over unique stored models, on the same scale as \(\widehat Z\), and flag \(\widehat Z<Z_{\mathcal T}\).

**PROVED:** positivity gives \(Z_{\mathcal T}\le Z\), hence
\[
\widehat Z<Z_{\mathcal T}\implies\widehat Z<Z.
\]
Indeed, \(\widehat Z/Z\le\widehat Z/Z_{\mathcal T}\), providing a quantitative upper bound on the evidence ratio when the flag fires. This is a sound detection certificate, not a general power theorem.

Source: `origin/theory/API-MASKZPIP:theory_campaign/API-MASKZPIP/REPORT.md`, §2 P3/C1–C3 and §9.

**Real issue.** The existing flag suite lacks a positive accuracy implication; passing island agreement can coexist with severe underestimation.

**Class and study effect.** **POST HOC** where stored scores are available; otherwise bounded rescoring of stored models. No SMC rerun. Do not feed this new final flag back into calibration or an adaptive island count.

**Proof route and status.** The certificate’s exact-arithmetic implication is **PROVED** above. Sensitivity to important evidence errors is **OPEN**. The four previously rescored study fits did not trigger it; that is neither a failure of its implication nor evidence that their evidence estimates were accurate.

**Cheapest check.** Deduplicate stores, check prior normalization and evidence scale, and test against exhaustive enumeration on a small model space. Deliberately understate a test estimate to verify triggering. This is deterministic and needs no simulation seeds. For floating-point certification, a rigorous comparison margin is necessary; otherwise label the output a numerical implementation of an exact-arithmetic certificate.

**INHERENT LIMITATION.** The same observed weights can look stable while all particles miss an important region. Therefore no universal accuracy guarantee follows from weight agreement alone. This does not rule out one-sided certificates or positive power under explicit coverage assumptions.

### Item 7 — Theory fit

**Verdict: refine; the method is compatible with the goals, but the current theorem packaging is not sufficient.**

HPM recovery and posterior-functional accuracy require different arguments. The latter must remain first in the paper’s methodology justification.

Four corrections are needed.

**First, target \(\pi(h)\) directly.** THM-SYNTH A1 largely reaches posterior expectations through concentration at \(S_0\). That can be useful asymptotically, but it does not establish useful posterior approximation at \(n=200\), where the posterior can be diffuse.

A simple complementary result is available. Conditional on calibration, suppose iid islands satisfy
\[
0\le H_r\le1,\quad E[W_r]=1,\quad E[W_rH_r]=\mu=\pi(h),
\quad M=E[W_r^2]<\infty.
\]
For \(\widehat\mu=\sum W_rH_r/\sum W_r\),
\[
P(|\widehat\mu-\mu|>\epsilon)
\le \min\!\left\{1,\frac{4(M-1)}R+
                    \frac{4M}{R\epsilon^2}\right\}.
\]

**PROVED under these hypotheses.** Set \(Y_r=W_r(H_r-\mu)\). Then \(EY_r=0\) and \(EY_r^2\le M\). If \(\bar W\ge1/2\), error exceeding \(\epsilon\) implies \(|\bar Y|>\epsilon/2\). Two applications of Chebyshev and a union bound give the display.

This separates Monte Carlo error from posterior concentration. It does not solve the practical problem of bounding \(M\). Extending the island identity to the specified measured-round estimator of a general \(h\) remains a **PROOF SKETCH** until its exact accumulation point is fixed and the resample–move recursion checked.

**Second, define actual joint estimators.** Joint inclusion probabilities cannot be reconstructed from marginal PIPs, and multiplying marginal Rao–Blackwell estimates is not a valid joint estimator in general. Specify plain particle averages at fixed measured-round endpoints for a deterministic list of joint indicators and other bounded summaries. Accumulation uses no additional randomness. The current `terminal_table` contains operational summaries, not the required particle-level joint information.

Sources: `Scripts/SMC_BVS/core/cpp/v3_engine.h:349`; `Scripts/SMC_BVS/core/v3_run.R:126`; `origin/theory/THM-SYNTH:theory_campaign/THM-SYNTH/THEOREM_LIST.md`, A1.

**Third, do not claim every proposal goal is already met.**

- Proposal §§5.1–5.2 have a clear finite-state invariance/SMC route.
- §5.3 needs a genuine start/weight-stability theorem with explicit conditions. Small cross-block correlations alone do not make the integrated likelihood factorize: the common integrated noise variance still couples blocks.
- §5.4 is conditional on using approximate correction. The shipped method has exact target scores; finite Monte Carlo error remains and requires separate treatment.
- §13, item 1 requires posterior expectations, including meaningful joint summaries. A theorem conditional on an unspecified potentially enormous island budget must disclose that limitation.

Sources: `theory_campaign/inputs/Local_to_Global_proposal.pdf`, §§5.1–5.4 and §13 item 1; `Docs/Methodology/METHODOLOGY_v3.md`, §§5–6.3; `origin/theory/THM-INV:theory_campaign/THM-INV/REPORT.md`, §§3a and 5.

**Fourth, repair theorem overstatements.**

- THM-SYNTH A2’s “can only fail downward” is false literally. **COUNTEREXAMPLE:** a nonconstant nonnegative unbiased estimator cannot lie below its mean almost surely; otherwise unbiasedness forces equality almost surely. Late-crossing lower-tail results do not eliminate upper-tail realizations.
- Ideal two-state stage laws are not laws for the realized candidate-grid rebuild process.
- Particle-parallel depth belongs to the proposed v3.2 execution, not implemented island-only v3.1.
- Discovery does not automatically imply retention in a bounded top store; the retention step needs its own condition.
- The exact-Gram LH results do not cover the study’s \(p\gg n\), groups-of-five generator.
- “Moving off the start is needed” survives; “tempering is needed for selection” does not.

Sources: `origin/theory/THM-SYNTH:theory_campaign/THM-SYNTH/THEOREM_LIST.md`, A2–A3, D1–D3, R5; `origin/theory/T38-RECORD:theory_campaign/T38-RECORD/T38_STATEMENT.md`, changes V11, V18–V19.

**Real issue, class, and study effect.** These repair unsupported claims and the missing general-functional output definition. Specification/proof corrections and deterministic summary accumulation are **ADDITIVE**. Existing HPM/PIP study results require no rerun. Joint summaries unavailable in saved fits cannot be retrospectively claimed; additional runs would be needed only if the final paper requires those empirical results.

**Cheapest checks.** Write the finite-state resample–move identity and verify the chosen accumulation point. Enumerate a correlated \(p\le16\) target and compare singleton, pair, and model-size summaries using an internal SMC harness, since public dispatch may choose exact enumeration. Ten fixed method seeds, 20261103–20261112, suffice as an implementation check, not a proof. Reuse these seeds across checks.

**INHERENT LIMITATION.** Finite-budget universal posterior accuracy without overlap/mixing/weight-moment conditions is unavailable. However, the absence of a production-grid variance bound, a study-generator theorem, or a weak-dependence theorem is **OPEN**, not an inherent impossibility.

### Item 8 — Other real issues

**Verdict: refine output semantics and numerical claims; retain the target prior.**

**Unavailable estimates must be explicit.** The stopped-fit `fit$log_Z` partial-match hazard is real: `log_Zbar0` exists while `log_Z` does not. Add exact named unavailable values for evidence and posterior estimates on every unavailable-output return, and audit downstream consumers. Partial calibration or island values may remain archived but must not masquerade as final estimates.

Sources: `origin/theory/API-AUDIT:theory_campaign/API-AUDIT/REPORT.md`, §2b; `Scripts/SMC_BVS/core/v3_fit.R:55`, `:113`, `:126`; `Scripts/SMC_BVS/core/v3_run.R:111`.

**Freeze the strict output convention.** Count `exact`/`completed` as output; retain other HPMs only as explicitly incomplete records. An LS0 stop must count as no complete v3.1 output if OP-LS0 is a theorem premise.

Crucially, guard coupling does not imply
\[
E[\widehat Z\mid\text{completed}]=Z.
\]
The confidence claim should be stated for the potential run, or as
\[
P\{\mathcal O,\;0.05\widehat Z>Z\}\le0.05,
\]
not as 95% coverage conditional on observed completion.

Source: `origin/theory/T38-RECORD:theory_campaign/T38-RECORD/T38_STATEMENT.md`, Parts I.A–I.B; `origin/theory/API-AUDIT:theory_campaign/API-AUDIT/REPORT.md`, §2.

**Separate numerical evidence from proof.** Long-double agreement is valuable evidence, not an exact-arithmetic error theorem. The scorer’s own `error_bound` is explicitly documented as heuristic. The small-\(p\) VAL-FP measurements must not become universal production-size error bounds.

Sources: `Scripts/SMC_BVS/core/cpp/v3_score.h:240`; `origin/theory/API-AUDIT:theory_campaign/API-AUDIT/REPORT.md`, §6.

**Real issue.** These fix false estimates on failed fits, invalid completion-conditioned interpretations, and unsupported numerical certification.

**Class and study effect.** **ADDITIVE** interface corrections, plus **POST HOC** repair of affected summaries. Completed-fit numerical estimates stay unchanged. Mark the six stopped fits unavailable and inspect consumers; do not rerun the study. Concurrent execution and LS0 do not mathematically guarantee fewer resource stops, because elapsed time, memory, and extra work change.

**Proof route and status.** The partial-match failure is an executed **COUNTEREXAMPLE** in API-AUDIT. The output-event inequality follows **PROVED** from potential-run Markov coverage and event inclusion. A rigorous production-scale floating-point certificate remains **OPEN**.

**Cheapest checks.** Construct stopped-fit objects and test both `$` and exact-name access; force stops at calibration, final-island, and LS0 boundaries in the replay harness; verify that all final-estimate fields remain unavailable. Inspect saved consumers before commissioning any numerical reruns.

**INHERENT LIMITATION.** The size cap excludes larger truths by definition. A size-only prior cannot change rankings between equal-size models because its factor cancels. Those are genuine model/prior limitations. The API hazard and numerical-certification gap are fixable.

## 3. HQ’s objections, 1–8

1. **Block start contributes little — reject as an established conclusion; accept the ablation question.** Tiny truth mass does not measure repair-basin mass, total depth, or posterior error. API-RESID’s median \(\pi_0(R_2)=0.813\) is relevant contrary evidence. Require the intervention audit in item 1.

2. **Backfit is more often favorable but WORKHORSE — accept with qualification.** The empirical improvement is large and reproducible, and replacing the start is WORKHORSE. “Favorable” is an empirical threshold; there is no full-SMC advantage or convergence theorem. Selection recovery is not the principal reason to investigate it.

3. **The two PIP rules pull in opposite directions — accept.** Equal pooling can be stable while retaining bias; weighted pooling has the appropriate island-consistency result but may be noisy. This is a finite-budget tradeoff, not contradictory theory. My reporting choice is weighted primary.

4. **Calibration is least theorized and highly sequential — accept the substantive concern.** Pilot adaptation and rebuild dependence remain sequential after diagnostic islands are parallelized. Whether calibration dominates elapsed time is empirical. Retain it because there is no demonstrated beneficial replacement.

5. **Concurrency evidence is incomplete — accept.** W-cal is unexecuted in the supplied record. Use the dossier’s supported run count, not conflicting summary prose. Add mutable-counter isolation and test guards, stores, provenance, and persistent streams.

6. **LS0 must be additive in production — accept.** The export and zero-HPM-change study result are strong supporting evidence, but production integration must preserve the baseline computation and attach certificates to the correct model.

7. **Default \(R'\) and \(R\)-versus-\(N\) guidance must be fixed — accept.** Default \(R'=4\); optional predeclared \(4k\) islands at unchanged \(N_e\). Do not split the existing population budget or adapt island count from final estimates. No optimal resource-allocation theorem is claimed.

8. **Flags have no positive power result — accept narrowly.** General sensitivity remains OPEN. It does not follow that no useful positive guarantee is available: \(\widehat Z<Z_{\mathcal T}\) has a deterministic soundness implication. Soundness and power must be distinguished.

## 4. HQ’s candidate inherent limitations

### 1. Per-round \(\Theta(p)\) sequential steps

**Agree, for the fixed v3 kernel only.** Its updates depend sequentially on the particle state. **Disagree** that this is inherent to SMC or the BVS problem. Removing it would require a new kernel and new analysis.

### 2. Each worker holds \(X^\top X\)

**Disagree that this is inherent.** It is the current scoring representation. Read-only sharing reduces node-level replication; on-demand Gram submatrices trade memory for computation. However, the large-\(p\) plan must also address clustering/correlation storage. Source: METH-AUDIT `REPORT.md`, §2.1.

### 3. SMC weight variance through a masked crossing

**Agree as a possible failure mechanism; disagree as an unavoidable severity claim.** Rare successful crossings can carry disproportionate evidence weight. But resolved grids and improved mutation can reduce the problem. The exact-refresh variance formula is direct evidence that performance depends on the bridge and kernels. The production masked-regime upper bound is OPEN. Source: `origin/theory/API-MASKZPIP:theory_campaign/API-MASKZPIP/REPORT.md`, §2 E3 and §5.

### 4. “No run can upper-bound \(Z\)”

**Disagree literally.** The model already supplies a finite analytic upper bound.

From `Docs/Methodology/METHODOLOGY_v3.md`, §5, write
\[
m(S)=C_nD_S^{-1/2}(2b_0+Q_S)^{-\nu},
\quad \nu=a_0+n/2.
\]
**PROVED:** if \(\lambda_i\ge0\) are eigenvalues of \(G_S\), then
\[
D_S=\prod_i\frac{(n+1)\lambda_i+1}{\lambda_i+1}\ge1.
\]
Also, the eigenvalues of \(nX_SH_S^{-1}X_S^\top\) are at most \(n/(n+1)\), so
\[
Q_S\ge\frac{y^\top y}{n+1}.
\]
Because the capped prior sums to one,
\[
Z\le C_n\left(2b_0+\frac{y^\top y}{n+1}\right)^{-\nu}.
\]
This bound may be extremely loose, but it refutes impossibility. Exact enumeration also supplies \(Z\).

The defensible limitation is: **the observed particle/store record alone generally provides no useful tight upper bound without further global information.**

### 5. Markov-only evidence lower bound

**Disagree literally.** \(Z_{\mathcal T}\le Z\) is a deterministic lower bound. Under the potential-run convention,
\[
\max\{Z_{\mathcal T},\,0.05\widehat Z\}
\]
retains at least 95% lower coverage: the deterministic term can never cause an exceedance. This is **PROVED** by event inclusion.

What is inherent to relying only on nonnegativity and a first moment is Markov’s weakness. Sharper probabilistic conclusions require additional information; they are not forbidden by SMC.

### 6. Weight diagnostics can certify too early

**Agree after correcting “certify.”** Empirical weight agreement can falsely reassure because it contains no direct evidence about an unvisited region. The project’s blind-grid constructions support that failure. Such diagnostics should never be called accuracy certificates. Additional assumptions or deterministic lower bounds can still provide useful guarantees.

### 7. At \(n=200\), posterior misses limit selection accuracy

**Agree for the fixed posterior and HPM decision, with a precise empirical interpretation.** In 565 fits, a scored competitor strictly outranks \(S_0\); therefore \(S_0\) is not the global posterior mode in those fits, regardless of whether the global maximizer was found. More faithful optimization cannot make HPM recover \(S_0\) there.

**Disagree** that the number 565 is a universal statistical limit or that every remaining fit is globally solved. It is evidence about these datasets and this target. Different data, priors, or losses can change the outcome; no such WORKHORSE change is justified here.

Source: `origin/theory/API-RESID:theory_campaign/API-RESID/REPORT.md`, §4; `origin/theory/T38-RECORD:theory_campaign/T38-RECORD/REGISTRY_v2.md`, §D, ELS-2.

## 5. Open questions that must be closed before the proving phase is commissioned

1. **What exactly did ABL-START change?** Close by inspecting the arm construction: singleton factorization, prior normalization, graph, swap count, independence proposal, and charged setup costs. Then read the paired posterior-error/cost results. A confounded comparison cannot settle item 1.

2. **Which estimator and outputs define v3.1?** Freeze weighted/equal PIP names, MPM conventions, \(R'=4\), optional stacking, baseline-versus-expanded flags, LS0 placement, strict output status, and the actual estimator for general bounded \(h\). Close with one consistent specification-to-code checklist.

3. **Does production parallel execution preserve the promised computation?** Close with W-cal, safe worker-state ownership, persistent streams, deterministic scan/store merges, baseline-center search preservation, and integrated LS0 replay. Reuse the three existing study datasets and seeds.

4. **What posterior-accuracy theorem is actually required?** Close the theorem statement before proving: fixed-data consistency alone, or a finite-error bound with an explicit moment/overlap constant, or an \(n\)-indexed result at the declared budgets. The elementary bound in item 7 offers a clean interface. Calling an unspecified \(R_n\) “scalable” does not close this question.

5. **How will proposal §5.3 be fulfilled?** Supply explicit jointly satisfiable assumptions and a controlled divergence/weight-variance quantity for the actual block-product construction, including shared-noise integration. The current orthogonal/idealized results must be checked against that statement. Failure to prove a broader claim is not an inherent limitation.

6. **Which calibration claims remain in scope?** Freeze the valid-grid contract and identify whether production-grid coverage, rebuild convergence, or delivery probabilities are required claims. If required, close them by a proof or counterexample. If excluded, disclose that exclusion honestly; under the dossier’s literal “no open question” rule, exclusion cannot be disguised as proof of impossibility.

7. **Are all guarantees stated for the correct event and numerical object?** Close with the unavailable-field fix, consumer audit, explicit potential-run/output distinction, and correction of “downward only,” unconditional retention, and numerical-certification language.

8. **What evidence supports “scale \(p\) beyond sequential MCMC”?** Close by stating the implemented execution level and complete work/depth/memory model, including setup and reductions. A future particle-stream/Gram-free plan supports a roadmap, not a current performance claim. Any comparative wall-clock claim needs matched accuracy, resource accounting, and a specified comparator.

These checks should share existing artifacts and one small validation panel, capped at the permitted 10–20 seeds. The six stopped fits may be revisited later to measure operational rescue; they cannot establish an asymptotic delivery theorem. No full-study rerun is warranted for the refinements I support.
