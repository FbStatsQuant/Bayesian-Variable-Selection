# Independent draft checks

Reviewed 2026-11-02. Source snapshots: F-DRAFT `4de6e4c7fab641f11f1ba8bb9f306beae5103b74`, `theory_campaign/F-DRAFT/NEW_TARGETS.md`; A-DRAFT `dbf47f7abfe9940ec7914f89bbe5f28071ad9871`, `theory_campaign/A-DRAFT/REPORT.md` §2. Local reference HEAD `816ec72ed40a35a0bff620ccb3170d947008cebe`. This is a mathematical referee check, with no numerical execution. VERIFIED means the indicated argument checks under its stated qualifications; it does not adopt a candidate or upgrade a source status. Locked results remain adoption-pending as specified in `Docs/Theory/proofs/LOCKED_PROOFS.md`.

## F-DRAFT W1: VERIFIED

Under BO both G and H are block diagonal. Thus D multiplies, t adds, and the displayed expression for d follows exactly from methodology §5. Set a_b=t_{S_b}/c. Positivity and the ridge bound give a_b≥0 and Σa_b<1. Inductively ∏(1−a_b)≥1−Σa_b, strictly when at least two a_b are positive. This proves the sign and equality case. With known common variance, the log marginal BF is −log(D_S)/2+t_S/(2σ²), so it is additive and the *globally prior-coupled* start equals the posterior, including the cap. This does not identify the start with a product of local posterior probabilities. Source status remains PROVED candidate.

## F-DRAFT W2: ERROR in the purported exact identity; GAP in the uniform conclusion

The source explicitly defines x_{T,l}=(RSS_T−RSS_{T+l})/RSS_T. This is ordinary least-squares partial R². The exact v3 marginal score uses Q, not RSS, and additionally 2b0. Consequently the displayed exact identities using x are false, even for orthogonal singleton columns. For a singleton with G=n−1, its v3 explained quantity is n(n−1)/n²=(n−1)/n times its ordinary LS explained quantity; 2b0 supplies another discrepancy. The determinant cancellation under BO is correct.

Repair: define a separate regularised fraction

    h_{T,l} := (t_{T+l}−t_T)/(2b0+Q_T).

Then BO gives exactly h_{S°,l}=h_{T,l}(2b0+Q_T)/(2b0+Q_{S°}), and LR_l=ν[log(1−h_{T,l})−log(1−h_{S°,l})]. These are algebraic statements needing no Gaussian assumption. Require S°+l feasible; it is otherwise outside Ω and its posterior odds are undefined.

The asymptotic leading mechanism κ_b Z²/2 is plausible for fixed null comparisons, but not proved by declaring a common remainder cancels. The regularised increments contain signal-dependent ridge corrections; uniform *relative* o_P(1) errors are particularly stronger than additive errors when the smallest |Z_l| tends to zero. The source's expansion hypotheses are candidates, and an O_P(1) additive expansion does not imply G_l=(Z_l²/2)(1+o_P(1)) uniformly. Supply an additive uniform error with its rate and prove it suffices for each subsequent layer bound, or state explicit lower bounds on |Z_l| on the selected extreme-value subset. Also raw-scale v_T must be compared to working-scale Q after response standardisation; the scale cancels in their ratio but cannot be omitted for individual residual limits. Source conditional PROVED label is not independently verified as written.

## F-DRAFT W4: VERIFIED TV bound; GAP for KL rate and chi-square assertion

For any probability laws P,Q and state a, TV(P,Q)≤P(a^c)+Q(a^c), by inserting δ_a. Therefore the displayed TV bound follows conditional on the two cited concentration-rate inputs. No weight-moment premise is needed for this part.

There is an exact useful KL bound, from E_{π0}e^d≥π0(S0)e^{d(S0)}:

    KL(π||π0) ≤ −log π0(S0) + Σ_{S≠S0}π(S)[d(S)−d(S0)].

The source replaces this whole sum by the single-null layer without controlling positive terms from multiple extras or mixed deletion/addition states. Under BO d increases on adding explained signal in a distinct block, so positive multi-extra terms cannot simply be discarded for an upper bound. That is a proof gap. The asserted sharp chi-square law is W(c), explicitly CONJECTURE, and remains such here; W4 cannot promote it to a proved consequence. Preserve W4's PROOF SKETCH status.

Small KL and TV alone indeed do not force stable importance weights. An explicit abstract construction establishes that point independently: take π0=(1−ε, εe^{−1/√ε}), normalised by its coordinate sum, and π=(1−ε,ε). Then TV→0 and KL→0 while χ² diverges. This does not prove the claimed v3 rate or its sharp threshold.

## F-DRAFT NM: ERROR/GAP as a general proposition; valid fixed-p repair

1. The claimed precise expansion log BF({l})=nc/2−(log n)/2+O_P(1), with c the *population* log residual ratio, is false for fixed nonzero proxy correlation: empirical correlation fluctuates by O_P(n^{−1/2}), giving a nondegenerate O_P(√n) fluctuation in log BF. Use n^{-1}log BF→c/2, or nc/2−(log n)/2+O_P(√n). The displayed BF formula with ordinary x=r_{ly}² is also not exact for ridge/IG scores (W2 issue); it suffices for the exponential rate after an O_P(1) log correction in fixed dimension.

2. The exact odds identity in (ii) verifies π0({j})→0. By itself it does **not** verify π0(j,l∈S)→1, nor that the start mode is exactly {j,l}; all other states must be bounded. Likewise singleton evidence in each block alone does not prove the entire naive union equals exactly {j,l} when other columns/blocks are arbitrary. The assumptions do not explicitly provide uniform global SE/BM hypotheses of locked T03. Saying eigenvalues are bounded on 'sets used' is insufficiently specified for its growing-p application. A correct minimal repair is the identifiable p=2 family in A-DRAFT Proposition M, whose four-state direct comparison supplies all missing normalisation arguments.

3. With that repair, (iii), TV separation, and exponential start truth-mass decay follow directly; the polynomial iid-discovery obstruction follows. An exponential lower bound on M yields a poor *worst-case* independence-sampler rate; do not infer failure for every initial state (starting at truth is an immediate exception). State precisely the initial law and success event before claiming all algorithms fail at every polynomial budget.

4. Part (v) needs occupancy of the stated mode when its Gibbs label is executed. SR scores {j} if the current state at label l is {j,l}; merely starting a round there does not ensure that. The cited candidate's actual lower-bound hypotheses must be retained. The O(1) ideal-grid conclusion is also not established by W″'s thermodynamic-length calculation: a local small-step approximation and finite integral do not prove a uniform finite-threshold discrete stage bound. It remains a separate obligation. No masked-regime estimator-consistency theorem follows.

## A-DRAFT §2: VERIFIED under the stated potential-run and premise qualifications

The conjugate distributions agree with methodology §5: posterior precision H/(nv), mean nH^{-1}z, and IG(ν,b0+Q/2). The inverse preprocessing map correctly distinguishes working and contrast scales.

Theorem A's finite-state induction is sound. Positive bounded potentials make the normalisation map globally Lipschitz; conditional multinomial resampling and independent mutations give O(1/N) coordinate MSE. A finite induction handles stage boundaries, evidence products and fixed terminal prefixes. The pre-label kernel is a state-independent mixture of products of π-invariant kernels, so πR_j=π and πK_j f=πf. Finite averages over four measured rounds do not require independent rounds. Independent conditional parameter draws add the stated conditional variance. This proves the candidate LLN/MSE, not a CLT or uniform growing-dimensional rate. For N-dependent independently calibrated grids with bounded stage count, the displayed unrolled bound is a valid loose uniform bound because temperature increments sum to at most one.

Corollary A1 follows from locked T12 §3(i.a–c). The pre-resampling case cancels the final weight denominator exactly. The pooled product bias is −3 Cov(Zhat_1,muhat_1)/4: diagonal products are unbiased and the twelve off-diagonal products factor conditional on calibration. Equal pooling across infinitely many frozen islands converges to the possibly biased island mean, as stated.

Theorem D checks conditional on (P1), OUT and successful calibration. Hölder gives q_φ(S0)≥min(π0(S0),π(S0)); endpoints give equality for the supremum deficit. T14(i-b) then gives D4. From T12 and 0≤η(S0^c)≤1, D5 is immediate and gives D6 for arbitrary bounded integrated h. This also applies to marked pre-label measures and terminal weighted measures via the same product identity.

D7 uses elementary detailed balance: Gibbs departures have distinct one-flip destinations and their total is ≤δ/(1−δ); each of the B+2 other labels has departure ≤δ/(1−δ). The first-departure union bound works for every random order. Reapplying D5 at each measured-round start removes any need to multiply the departure cost by L. The simultaneous PIP bound has no p-union-bound loss. On the good event with (T+1)Δ≤x, T≥1 implies Δ≤x/2; the constants 8M and 24 are valid upper bounds. Truncation/Markov, followed by n→∞ and x↓0, proves the stated output-intersected convergence. It does not prove output availability tends to one.

The additional weighted conditional-draw argument is necessary and valid: truncated-run T14 controls the count m0 of truth copies; the terminal weighted product identity controls v_out; identical weights on those copies give Σw_i²≤1/m0+v_out²→0. N_e≥n makes the equally weighted version immediate. On the exact branch the report correctly requires integrated sums rather than one parameter draw per enumerated state.

Corollary D1's boundedness/continuity/contraction argument is valid, and the equality-indicator counterexample correctly refutes convergence to truth for every bounded measurable h. All §2 source results remain self-described candidates; this check neither proves their statistical premise (P1) for masked starts nor upgrades T16's conjectured CLT.

References checked: `Docs/Methodology/METHODOLOGY_v3.md` §§5–6; `Docs/Theory/theorems/00_COMMON.md` §§1–3; locked `T09_T7_kernel_validity/STATEMENT.md`, `T12_T8_frozen_run_identities/STATEMENT.md` §3, `T14_LFM_first_moment_evidence/STATEMENT.md` §3; and `Docs/Theory/proofs/LOCKED_PROOFS.md`. No source files were edited.
