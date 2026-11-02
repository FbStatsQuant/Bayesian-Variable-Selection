# A-REV4 independent cross-family review

Reviewer: GPT-6 Astra; 2026-11-02. Sol helpers supplied mechanical independent checks in BOOK_CHECK.md and DRAFTS_CHECK.md; the verdicts below are the primary referee's. All changes are confined to this directory. SOURCE_MANIFEST.json pins the four reviewed branch heads, local base and source hashes. Snapshots preserve the reviewed text, including methodology, common definitions, locked register, collected proofs and guard code.

**Overall: GAP.** The favourable-start and posterior-functional compositions are defensible conditional mathematics. F-DRAFT contains two explicit false formulas, and its sharp weight-divergence claims are not proved. No result is adopted, no source status is upgraded, and no floating-point or operational-completion guarantee is inferred.

## Verdict table

VERIFIED means the specified implication checks under its stated hypotheses; it does not replace the source's candidate/sketch/conjecture status. ERROR identifies a false assertion with a counterexample. GAP identifies an unproved step or missing qualification. Mixed results receive the weakest overall verdict.

| Result | Verdict | Scope and overall disposition |
|---|---|---|
| W2-T26 Lemma 1 | VERIFIED | Endpoint identity, positive finite bridge, S0 feasible. |
| W2-T26 Lemmas 2 and 3 | VERIFIED | First departure and refreshed occupancy remove the L factor. |
| W2-T26 Theorem A, actual written statement | VERIFIED | Includes EX-A/EX-S/CAL/START/OUT, feasibility, P1 and P1-ex; output-intersected conclusion only. |
| W2-T26 advertised single-premise shorthand | GAP | P1 restricted to successful SMC says nothing on the exact branch. |
| W2-T26 Theorem B | VERIFIED | Conditional composition of locked T03 and T22(iii); EXP'/VIS/NL remain assumptions. |
| W2-T26 Proposition C | GAP | Retain PROOF SKETCH; missing uniform probability details can be repaired as below. |
| W2-BOOK RO | VERIFIED | For statistical outputs, nonnegative potential values, P(output)>0 when dividing. |
| W2-BOOK GUARD literal full-output claim | ERROR | Timing/allocation metadata differ on successful same-seed executions. Statistical stop-only interpretation checks statically. |
| W2-BOOK completion-selection counterexample | VERIFIED | Stylised component example, not an estimate of production bias. |
| W2-BOOK Proposition 2 island identity and covariance | VERIFIED | Fixed data, frozen calibration, four conditionally iid potential islands. |
| W2-BOOK output Markov bound | VERIFIED | Event bound, not conditional unbiasedness or relative-error coverage. |
| W2-BOOK VAL-FP | GAP | Implication is VERIFIED; no validated eta/epsilon for production is supplied. |
| W2-BOOK package | GAP | Probability convention, operational projection and numerical validation require qualifications; additional HPM overstatement is ERROR. |
| F-DRAFT NM | ERROR | Population-rate expansion has a false O_P(1) remainder; further normalisation/mode/repair claims have gaps. |
| F-DRAFT W1 | VERIFIED | BO algebra and known-common-variance comparison; source remains candidate. |
| F-DRAFT W2 | ERROR | Ordinary partial R² is not the exact v3 score fraction; uniform asymptotic claim also has a gap. |
| F-DRAFT W4 | GAP | TV implication verified; KL omits positive layers; sharp chi-square rate imports a conjecture. |
| A-DRAFT §2 Theorem A and A1 | VERIFIED | Fixed-data bounded-functional LLN/MSE and unnormalised identities; no CLT upgrade. |
| A-DRAFT §2 Theorem D and D1 | VERIFIED | Explicit favourable-start premise and bounded-function/continuity qualifications retained. |

## 1. W2-T26: detailed dependency and proof audit

Methodology §§6.5–6.8 requires a fresh state-independent random permutation per particle/round, multinomial resampling at every stage, independent final streams 10–13, and four recorded terminal rounds. These are exactly the features used. Common §2 defines B<=16 and the capped budgets. The locked T09, T12, T14, T15, T22 and T23 statements, and their chapters in COLLECTED_PROOFS_v2.tex, support the following chain. The collected volume's older scope notes do not independently discharge wave-2/3 statistical assumptions; the current register and individual statements govern those inputs.

1. Write gamma_phi=gamma0^(1-phi) gamma1^phi. Hölder bounds its normaliser by Z0^(1-phi) Z1^phi. Thus q_phi(S0)>=q0(S0)^(1-phi)q1(S0)^phi>=min(q0(S0),q1(S0)). Both endpoints occur: Delta=max(1-pi0(S0),1-pi(S0)), exactly. Feasibility and strict positive scores are essential.
2. Invariance alone implies K_e(S0,y)<=pi(y)/pi(S0). Gibbs destinations for distinct labels are distinct one-flip states, so their total departure is at most u_pi. Each of the B+2 remaining labels contributes at most u_pi. A first-departure union bound, conditional on any label order, gives rho_bar<=(B+3)u_pi. Multiplying the stay probabilities also proves the displayed exact product formula. No union over all p unrestricted destinations is introduced.
3. T14(i-b) gives E_C|W_r-1|<=b=2(T+1)Delta/(1-Delta), independently of N. T15(i),(iii) at c=1/2 gives expected outside occupancy <=min(1,2 delta+2b). T12(i.b) explicitly includes every fixed terminal prefix, even when its length grows with n: each finite-n application is legitimate and the bound does not depend on that length.
4. At each measured-round start the previous occupancy bound applies afresh. Conditional first departure during that one round costs at most rho_bar. Averaging four rounds and using the locked pathwise T23(ii-a,b) inequality gives the displayed simultaneous PIP bound. This removes the old accumulated burn-in departure factor; it does not assert that trajectories never departed during burn-in. Bounded B is needed to deduce rho_bar->0 from delta->0.
5. On (T+1)Delta<=x<=1/4, T>=1 implies Delta<=x/2; b<3x, u_pi<=x and rho_bar<=19x. The source's 27x PIP bound and four-island 108x/epsilon bound are valid. Markov, then limsup in n, then x down to zero proves the output-intersected statements. MPM error implies a coordinate error at least 1/2; log-evidence follows from continuity at one. No completion conditioning occurs.
6. The exact branch has no successful SMC calibration. Its evidence is exact, but truth-PIP consistency needs delta->0 there. The written P1-ex supplies exactly this. A fixed-p sequence with vanishing signal (e.g. theta_n=n^-1, true support {1}) illustrates why SMC-restricted P1 can be vacuous while exact posterior truth-PIPs fail. Repair the shorthand by retaining P1-ex, or use the global deterministic-budget Delta premise. The written theorem already does so.
7. Theorem B: T_max=O(log² n) under polynomial p. T03 gives delta=O_P(sqrt(log n/n)). Global SE implies within-block SE eventually since B<=16 and m_n+s0 grows. Locked T22(iii) supplies the strict start rate; in the weak form restrict to the probability-tending-to-one event zeta_n<=kappa/2. Multiplication by log² n leaves both endpoint deficits negligible. This verifies composition only; it does not prove EXP', visibility or leakage for the study design or discharge EX-A/OUT.

**Proposition C repair, preserving sketch status.** The ORTH calculation H=n²I, D=n^k, Q=y'y-||z||²/n is correct. Its EXP' remainder is bounded by 1/(2n)+nu*1.02/rho_min. For a fixed design, every block residual projection has rank d_b=n-1-|C_b| and noncentral Gaussian squared norm stochastically dominating sigma² chi²(d_b). The elementary bound P(chi²_d<d/2)<=exp(-c d), c=(log 2)/2-1/4>0, follows from exponential Markov at 1/2. A union over at most n blocks tends to zero. Also s_y²=O_P(1) under bounded signal energy. Consequently rho_min/n is bounded away from zero in probability, and the remainder is O_P(1). Be precise: tight s_y² alone gives a constant depending on the desired tail probability, not automatically one fixed constant on an event whose probability tends to one. Here Gaussian concentration plus fixed ORTH signal energy supplies the stronger version if desired. Use centered Y in the residual formulas. VIS follows from (n-1)theta_min²; leakage is zero and NL_avg holds for kappa<=1/2. Ties do not matter because the bound applies to every deterministic partition of bounded block size. This completes the omitted reasoning as a proposed repair, without turning the source's sketch into an adopted theorem. ORTH excludes p>n-1.

## 2. W2-BOOK: run/output, engine and certificate

Static code inspection: v3_runtime.h:13–27 updates clock/guard records without RNG consumption; v3_engine.h:335–336 returns partial at a bridge checkpoint; v3_core.cpp:435–450 uses sequential independent streams and turns a partial run or final local-search stop into resource_limit. Calibration/preflight guard calls also exist in v3_calib.R and v3_fit.R. An untriggered guard does not alter the statistical kernel or budget. Removing it in the same arithmetic computation preserves the statistical path. This is not a proof that floating arithmetic equals EX-A.

**GUARD counterexample and repair.** v3_fit.R returns allocation, timing, peak-memory and runtime-guard metadata. Two completed runs with the same data/seed but different sufficiently large allocations have different reported allocation fields. Therefore a potential record defined only from data and streams cannot equal *every* reported output. Project both records onto statistical estimates, scores, discrete records and statuses; exclude resource/timing metadata from equality and replay tests. RO then gives O=G^c intersect Obar and event inclusion. State nonnegativity/boundedness for the potential statistic on all of Obar, and require P(O)>0 for conditional statements.

For fixed data and successful C, let mu=E_C PIP_hat_1j. Four diagonal terms in E_C[Zbar Pbar] contribute Z PIP/4; twelve off-diagonal terms contribute 3Z mu/4. Hence the bias is (3/4)Z(mu-PIP)=-(3/4)Cov_C(PIP_hat_1j,Zhat_1). Averaging island products is unbiased; multiplying two pooled summaries is not. Conditional iid is used before any completion selection.

Nonnegative evidence plus RO gives P(O,alpha Zhat_rep>Z)<=alpha P(A). Dividing yields only alpha P(A)/P(O). The expectation E[1_O Zhat_rep]<=Z P(A) must be explicitly **conditional on data**; with random data the correct right side is E[1_A Z(data)]. Counterexample to treating the printed expectation as joint: A=O=whole space and exact evidence equally likely 1 or 2 yields expectation 1.5, which exceeds Z on the first data outcome. On the exact branch either define A appropriately or state the separate exact-output result; do not apply an undefined SMC-success event.

On VAL-FP's good event, Zhat_fp<=exp(eta) Zbar; Markov plus the exceptional probability gives alpha exp(eta)P(A)+epsilon. This conditional implication is VERIFIED. Identifying an actual good event, eta and epsilon remains GAP; neither score accuracy alone nor an observed small stop rate establishes it. No replay against exact arithmetic was performed here.

The BOOK cost guard is explicitly stylised and N=1,p=2 component-only: production would enumerate. Its calculation can refute preservation of unbiasedness under output conditioning; it cannot quantify actual engine bias. The remote reproduction below preserves that distinction. Arbitrarily rare discarded high weights can cause substantial conditional bias.

**Additional ERROR outside the requested central identities:** BOOK REPORT's claim that every completed wrong HPM is a posterior miss is false. Let F(S0)=1,F(S1)=0 and scored set={S1}. A completed search reports S1 despite S0 being the global maximiser. Completion does not imply discovery. Replace this sentence by an audit-specific empirical observation, if independently supported, or retain the separate search-miss term. It is not a consequence of locked T07.

## 3. F-DRAFT: counterexamples and repairs

**W1 VERIFIED.** BO makes G,H block diagonal, so D multiplies and t adds. With xi_b=t_b/(.02+n-1), sum xi_b<1 and product(1-xi_b)>=1-sum xi_b, strictly if two terms are positive. This proves the displayed nonnegative discrepancy and equality case. With known common variance the log BF is -log D/2+t/(2 sigma²), additive across blocks. Keep the global capped prior in the start; this is not a product of independent local posteriors.

**W2 ERROR, explicit feasible counterexample.** Take n=20,p=4, centered orthogonal columns with G=19I, blocks {1,3},{2,4}, S°={1}, l=2, ||y||²=19, and squared z coordinates (100,30,0,0). Such a response exists because 130/19<19; the remaining energy can lie in an orthogonal contrast direction. K=4 so the addition is feasible. With nu=10.01, c=19.02, the actual v3 log-odds difference is

    nu [log(1-1.5/19.02) - log(1-1.5/14.02)] = 0.310405538698...

Ordinary RSS partial R² instead gives 0.353784569589..., a discrepancy 0.043379030891. This is not rounding. The source explicitly defines x from RSS, but v3 integrates a ridge-adjusted Q and .02 offset. Repair with h_{T,l}=(t_{T+l}-t_T)/(.02+Q_T); then h_S=h_T(.02+Q_T)/(.02+Q_S) and the displayed log identity holds with h. Require |S°|<K. Uniform multiplicative Gaussian-gain equivalence is a separate GAP: an O_P(1) additive remainder need not cancel and does not give uniform relative errors near Z_l=0. Prove an additive uniform remainder with sufficient rate, or restrict to controlled extreme-value comparisons.

**NM ERROR and scope GAP.** Even the identifiable fixed-p two-column Gaussian family, b=sigma=1 and proxy correlation r=1/2, contradicts the stated O_P(1) remainder around the population linear rate. In orthonormal contrast coordinates the signal coordinate is sqrt(n-1)+E1, the proxy coordinate combines it with an independent E2, and the remaining noise energy is chi²(n-3). The empirical explained fraction has nondegenerate n^-1/2 fluctuations. The derivative of log(1/(1-x)) at x=r²/(1+1)=1/8 is nonzero. The delta method therefore gives a nondegenerate sqrt(n) fluctuation of log BF about n log(8/7)/2, not a tight remainder after adding log(n)/2. Repair to O_P(sqrt n), or simply n^-1 log BF->log(8/7)/2. The exponential local proxy-inclusion phenomenon survives this repair.

The odds pi0({j,l})/pi0({j})->infinity prove only pi0({j})->0. They do not control all other states, identify the exact start mode or show that the complete naive union contains exactly this pair for arbitrary remaining columns. Specify the sets covered by SE, control all normalisers, and retain actual label-time occupancy in the Gibbs repair claim. An iid-discovery obstruction from exponentially small start truth mass is valid. A worst-case independence-MH bound is not failure for every starting state: starting at truth is a counterexample to that interpretation. The O(1) discrete ideal-grid assertion is not proved by a thermodynamic-length heuristic. A safe repair is the explicit fixed-p two-column family with a direct four-state comparison (as in A-DRAFT §3); this is a component construction, since production enumerates at p=2.

**W4 GAP.** TV<=delta+delta0 follows by inserting the point mass at S0; the claimed TV rate follows if both concentration inputs hold. The exact useful KL bound is

    KL(pi||pi0) <= -log pi0(S0) + sum_{S!=S0} pi(S)[d(S)-d(S0)].

Replacing the whole sum by only single-null additions discards potentially positive multi-extra terms, so does not prove an upper bound. The sharp chi-square law is Theorem W(c), explicitly a CONJECTURE; W4 must retain that dependency and its PROOF SKETCH status. Repair requires bounds for all omitted layers and the uniform W2 expansion, not just a one-null extreme-value calculation. The general logical separation is real: pi=(1-1/k,1/k), pi0=(1-1/k³,1/k³) have TV->0, KL~2 log(k)/k->0 and chi²~k->infinity. This abstract counterexample is not the claimed BVS theorem.

## 4. A-DRAFT §2: adversarial audit

The conjugate mean nH^-1 z, covariance nvH^-1 and IG(.01+n/2,.01+Q/2) match methodology §5. Working-scale parameters must be back-transformed as stated. General h estimators are mathematical extensions, not claimed existing engine outputs.

Theorem A's finite-state induction is valid: positive bounded potentials make normalisation Lipschitz, multinomial resampling plus independent mutation supplies conditional O(1/N) variance, and finitely many stages/prefixes preserve the rate. At the pre-Gibbs label, the prefix kernel is a state-independent mixture of invariant products; it and K_j preserve pi. Correlated measured rounds still admit a finite-average MSE bound. Evidence is a finite bounded product. Fresh conditional parameter draws add controlled conditional variance. Bounded-stage independent N-dependent calibration admits the stated loose uniform bound; none of this is uniform in growing dimension. This verifies the LLN/MSE, not the conjectured T16 CLT.

A1's pre-resampling identity cancels the last normalising denominator; all other positions use T12. The covariance formula matches BOOK. Infinitely many fixed-N islands average the biased primary mean, whereas evidence-weighted pooling uses an unbiased numerator/denominator pair. No finite-N normalised unbiasedness follows.

Theorem D supplies a particularly clean valid bound: from E_C[W eta(S0^c)]=delta, 0<=eta(S0^c)<=1 gives E_C eta(S0^c)<=delta+E_C|W-1|. Hence E_C|eta f-pi f|<=2M(2delta+b). Its application to fixed-label RB rewards, terminal weighted supports and the simultaneous PIP path bound is legitimate. The improved constants 8Mx and 24x check. This independently confirms the lack of an L factor. OUT and the exact-branch clause are explicit.

For weighted parameter augmentation, the report correctly proves dispersion rather than assuming it: the truncated bridge gives m0/N->1 truth copies, terminal weighted occupancy gives v_out->0, and identical truth weights imply sum w_i²<=1/m0+v_out²->0. N_e>=n eliminates conditional-draw noise. Exact enumeration uses integrated sums, not one continuous draw per model. D1 correctly adds uniform local continuity and posterior contraction to reach the generating value. Its equality-indicator counterexample refutes unrestricted bounded-measurable generating-value consistency. No missing masked-start or completion guarantee is supplied by these arguments.

## 5. Computation and provenance

All numerical workloads ran persistently on Owls, one process per job. Local Python was used only to extract/hash source files. Checked remote /, /home, /home/fb31 instructions: the home AGENTS.md exists and is empty; no applicable additional instruction file was found for the new directory. Remote path: /home/fb31/theory_campaign/A-REV4. Source snapshots/configuration were copied there before launch. No quantile sampler or lambda prior is involved.

Saved results and manifests are under results/. checks.py uses seed 20261102 (its algebraic enumerations are deterministic), Python 3.9.25 and the recorded host/environment. PID 2507523 exited 0. It checks the W2 discrepancy, W1/endpoint Delta identity on all 16 models, and an independently constructed four-island covariance law. The tiny negative minimum d (-8.9e-16) is floating rounding, not a violation of W1. The grid check corroborates the endpoint algebra; it is not a proof over a continuum. Abstract divergence examples are illustrations only.

book_reproduction.py is an unchanged extraction of BOOK's script. First PID 2508065 failed with missing mpmath (exit 1, preserved). A private remote venv installed mpmath==1.3.0; retry PID 2508546 runs the 50-digit finite-law reproduction. Its provenance and inspected completion are recorded in NUMERICS.md. These are numerical checks, not interval certificates. nm_check.py (PID 2508672, seed 20261102) checks the repaired p=2 proxy family at small scale; saved output retains all reported aggregate values. NUMERICS.md records final statuses, outputs and exact launch forms; no failed attempt is hidden.

## 6. Integration disposition

Retain the conditional T26/A-DRAFT results with their full premise lists. Restrict GUARD to statistical records, fix BOOK's expectation convention and exact-branch extension, and remove its completed-HPM implication. Correct W2's exact fraction and NM's stochastic remainder before using them. Keep W4 and the ORTH compatibility source at their existing sketch status; the suggested repairs here do not modify or adopt any source. No locked result or methodology file was changed.

## 7. Additional T26 exact-branch ERROR

The repeated parenthetical assertion that the exact branch fails whenever p>=18 and n>=22 is false under the actual budgets. Counterexample: p=18, n=2^18. Then K=p, the state count is 2^18, N0=n, and the threshold (5H0+4N0)p is at least 4*2^18*18, strictly larger than the entire state count. The exact branch is therefore taken. More generally fixed p eventually enumerates, as common regime R2 explicitly says. Remove this parenthetical and replace it with the exact combinatorial inequality, or a genuinely sufficient growth condition. This does not invalidate Theorem A's fully written statement because P1-ex is retained, nor Theorem B because T03 supplies it. It does make the W2-T26 package contain an ERROR beyond the main verified implications.
