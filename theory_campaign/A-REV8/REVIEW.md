# A-REV8: independent cross-family referee, XV-MASKED-LS0

Referee: GPT-6 Astra; 2026-11-02. Task 4 of W8-SYNTH §8. **Overall verdict on the conditional consistency conclusion of Thm 5(b1): VERIFIED.** It is a theorem about v3 **plus LS0**, under (P), (M1)–(M3), the stated execution assumptions and ideal arithmetic. It is not a theorem that the study's original sampler executes LS0, completes with probability tending to one, or works quantitatively at n = 200. The exact-Gram LH consistency instance is VERIFIED under its fixed-parameter hypotheses. The broader printed package retains the GAP and minor ERROR findings below. No campaign status is upgraded, no result is locked or adopted, and A-REV3's p ≫ n GAP is retained.

## Scope and source control

The prescribed reading order was W4-T38FULL §3 with W5-VMASK R1–R7; W3-PXN P6/P7 with those repairs; W5-VPGD R6.2–R6.3; then W6-FIXREV1 against A-REV1 §7. Both W4 statement/proof and W6 statement/proof were inspected. W1-EXP's reference-concentration and exact-Gram LH proofs were followed as load-bearing dependencies. O-LS0's now-landed report and paired totals supply empirical context; the older synthesis says the report was missing and is stale on that point.

Exact branch heads, source paths and SHA-256 hashes are in [sources/manifest.json](sources/manifest.json). Frozen copies accompany this review. Authoritative comparisons are Methodology v3 §§6.3/6.10, 00_COMMON, the locked register (especially T03, T21, T22 and T27), and the scoring, ledger, local-search and guard code. These retain the BB(1,p) capped size prior and ridge g=n target, not the unrelated quantile-sampler lambda prior. I did not review W7-PART or duplicate A-REV6's assigned closure work.

## Verdict table

VERIFIED below is a referee verdict on the specified claim and scope, not a status change to its source.

| Item | Verdict | Scope |
|---|---|---|
| LS-score: truth is scored | VERIFIED | Feasible progress, complete last scan, emitted initial truth; no local-max premise needed |
| LS-score: “at most Φ(C₀)−1 moves” without exception | ERROR | C₀=S₀ gives a negative bound; explicit counterexample E1 below |
| Lemma M, including uniformity and standardisation | VERIFIED | Fixed k, polynomial p, fixed positive noise variance and eigenvalue floor on the preferred model |
| ELIG and POP-LAT ⇒ discovery | VERIFIED | Deterministic reference, bounded distance/extras, completed LS0 |
| Thm 5(b1) consistency conclusion | VERIFIED | Conditional implication; joint output-and-error probability, not error conditioned on output |
| Prop. LH-LAT | VERIFIED | Fixed exact-Gram LH parameters; m₀ is a valid lower bound, not a universal sharp margin |
| Exact-Gram LH eligibility and posterior premises | VERIFIED | Actual groups under g≤B<2g; fixed nonzero suppressors and uniform correlation bounds |
| Exact-Gram b1-LH consistency | VERIFIED | With LS0; c=1 needs only its initial scan |
| b1-LH assertion that c≥2, p→∞ suffices for iid-draw failure | GAP | c=2 logarithmic growth issue G1; not needed for LS0 consistency |
| W5-VPGD W_Lat reduction | VERIFIED | Reduction to the cited Theorem W comparison and fixed-extra Lemma S; no region-wide PGD claimed |
| W5-VPGD LH-PGD lower bound | VERIFIED | All nontruth lattice states, including Φ=1; sharpness remains a numerical claim |
| W3-PXN P6 after W5-VMASK | GAP | R2 repairs the constant, but the general-dimensional uniformity obligation remains in the supplied text |
| W3-PXN P7 after R1/R3/R6 | GAP | Peeling and rate argument substantially repaired; remaining bounded-dimension interface below; original sketch is not upgraded |
| W6 formulation versus A-REV1 §7 | VERIFIED | Strict output convention, potential execution, explicit rate/delivery interfaces, emitted centre and +1 cost |
| Literal GUARD claim that every reported output equals the guard-free output | ERROR | Runtime diagnostics differ even without a stop; E2 below. Statistical-output transfer survives |
| O-LS0 zero-change summary | VERIFIED | As a reading of saved aggregate records, not a new replay or bitwise identity certificate |
| Identifying O-LS0 empirical checks with all asymptotic M1–M3 premises | GAP | Finite-sample D_S is not POP-LAT; positive eigenvalue at one n is not a uniform asymptotic floor |

## Proof audit

**LS-score.** A feasible progress flip adds a missing truth or removes an extra; a progress swap replaces an extra by a missing truth. Thus the lattice is closed. At Φ≥2, D_S forces the best scanned neighbour to be a strict improvement with smaller Φ; ties among progress moves cause no problem. At most Φ(C₀)−1 accepted moves reach Φ≤1. The scan is performed before testing the move cap, so a distance-one centre scores S₀ even with no remaining moves. If a swap reaches S₀ directly, the preceding scan already scored it. If the initial centre is S₀, emission supplies discovery immediately. Neither certification nor D_S at Φ=1 is necessary. The feasibility assumption s₀+|C₀\S₀|≤K covers every needed addition.

**E1 (literal counterexample).** Take n=4, p=1, any centred nonconstant column and response, S₀=C₀={1}, ℓ=0, and emit the centre. The lattice has no Φ≥2 state, so (i) is vacuous, (ii) is 0≥−1, and (iii) holds. Truth is scored at zero moves, but zero is not at most −1. Repair only the move-count sentence to `max{Φ(C₀)−1,0}`. This does not refute the scoring conclusion or masked LH, where c≥1.

**Lemma M.** The prior increment is (k+1)/(2p−1−k), including the endpoint value one. The determinant bound is conservative but valid; equivalently each eigenvalue contributes log[(1+(n+1)λ)/(1+λ)] between zero and log(n+1). The ridge minimisation identity gives Q_B≥RSS_B/s_y² with no eigenvalue assumption on B, and Q_A≤RSS_A/s_y²+1+1/(nφ₀²) on the preferred model. With the common 0.02 inverse-gamma term retained, log(1+x)≤x gives displayed (3.2) in the correct direction. It does not replace a fixed-signal logarithmic gain by a quadratic equality (the error A-REV3 found in W4-SHARE is absent here).

The three events E1–E3 control projection noise, signal-noise cross terms, and total noise norm uniformly. The polynomial family has at most (2n^A)^(k+s₀) sets; L/4=A(k+s₀)+1 leaves a genuine union-bound margin. The cross term is O(sqrt(n log n)), whereas (n−1)m_n dominates it. The RSS lower bound uses A∪S₀ to remove signal before bounding noise; in the application this union has size ≤s₀+d≤k. Dividing by s_y² costs only a fixed constant. The positive score term is at least M_n sqrt(n log n)/(4C_R); prior and determinant penalties are O(log n), and the ridge correction is O(1). Uniformity therefore holds before choosing any comparisons. Interpret c₀ as a fixed upper envelope of the displayed n-dependent bound and “for n≥n₀ on E_n” pointwise in n, not as an almost-sure eventual event. Neither clarification changes the result.

**Assembly.** Set k=s₀+d+1. Every nonprogress neighbour has size ≤k, and every progress neighbour lies inside S°∪S₀, inheriting the M3 eigenvalue bound. Lemma M supplies all the D_S comparisons simultaneously. ELIG gives a unique start mode because a state of mass above one half is unique. The move budget diverges and the distance is bounded. On the good data event, every completed LS0 scores truth, independently of how the SMC populations moved. Hence the miss probability is bounded by the eligibility exception, Lemma M's exceptional event and eventual deterministic feasibility/budget exceptions. Finally

`{output and wrong} ⊆ {π(S₀)≤1/2} ∪ {output and truth not scored}`.

Markov and bounded convergence give the claimed limit. This direct argument also avoids needing equality of runtime metadata under GUARD. It proves `P(output and correct)=P(output)−o(1)`. It does not imply `P(wrong | output)→0` if output probabilities can vanish.

**LH-LAT.** Orthogonality between units makes the residual variance additive. In pair i the missing suppressor costs R_i=β_i²ψ_i²(1−ψ_i²); its proxy removes only κ_iR_i with κ_i<1. Select a missing hub of largest R_i. Nontruth additions lose at least (1−κ_max)R_i against that move. Deletions cannot decrease residual variance. A truth-to-nontruth swap is bounded by the corresponding addition through subspace inclusion. A truth-to-truth swap incurs a positive deletion loss after the addition, plus R_max−R_i≥0. The listed deletion losses bound these uniformly. These are all feasible neighbour types; other progress additions need not be strictly worse. Empty minima over visible hubs are interpreted as +infinity. When c=1 POP-LAT at Φ≥2 is vacuous and LS-score still applies.

**Joint exact-Gram premises.** The linked cross-correlations are strictly weaker than the within-group correlations in each linked group, so each group finishes before merging outside itself. Cutting and packing retain groups when g≤B<2g. The block signal projection is supported on S°: zero in masked/null groups, β_i(1−ψ_i²)x_a in a-groups. The residual outside any block remains positive even for a single linked pair, so SPREAD holds; the fixed eigenvalue floor gives VIS-lin. W1-EXP Thm 6 then supplies ELIG through the locked deterministic T22 reference bound on its event u<1. Global SE and fixed nonzero coefficients supply locked T03. This proves the joint premises without invoking T22(iii) at the masked truth or the erroneous unrestricted E3(ii).

**G1 (iid-draw separation).** W4 §3.4, retained by W6, derives only
`Q_f π₀(S₀)=O_P(n^(1−c/2) p^(−c) log² n)`.
For c=2, p→∞ alone does not make the displayed deterministic multiplier vanish: p of order log n leaves a constant; slower growth makes it larger. This is a GAP in the implication from the ceiling, not a demonstrated counterexample to actual production Q_f (which may be much smaller or may not exist on the exact branch). Repair the sufficient condition to `n^(1−c/2)p^(−c)log²n→0`; in particular require p/log n→∞ for c=2. The c≥3 and stated c=1 sufficient conditions are sound. Masking π₀(S₀)→0 itself and LS0 consistency are unaffected. Fixed p eventually enters exact enumeration and must not be marketed as an asymptotic SMC separation.

## W_Lat and the p ≫ n interface

W_Lat correctly replaces a whole near-truth region by the progress-closed lattice. Its comparison families are polynomial and its superset states use only subsets of the fixed P°. Thus the cited Lemma S can take the deterministic extra universe P° of fixed size, which supplies its H2 condition without a growing-universe LD condition. This verifies that reduction, not a new independent review of every lemma in W3-PGD. On LH, the previous case analysis also works when one suppressor remains missing. Dividing the margin by the best addition gain yields the stated η_LH. Its bound is sufficient; the claimed numerical sharpness is not needed. POP-LAT alone only constrains Φ≥2, so it must not be presented as a general guarantee of certification at Φ=1. Also a local certificate by itself cannot override a better model scored earlier; the asymptotic reported-HPM conclusion uses (P).

W5-VMASK R1–R7 were inspected individually:

* R2 replaces the false `≤1` ridge correction by a sufficiently large O(1) constant; valid. R3 uses the correct r*=(11+2sqrt(10))/9. R4 labels its s₀=5 numerical context. R5 keeps a valid margin and separates its sharper expression. R6 supplies the neutral within-block conditional Gaussian identity. R7 correctly adds the emitted centre to the score-call ceiling.
* R1 now sums the extras tail, handles missing-reference peeling including unions beyond K, controls visits to a masked group at the necessary H≈p scale, and cancels determinant terms in each neutral discrepancy increment. The choice k₀+1>2A makes H q^(k₀+1) vanish. The O(log n) range then fits the Θ(log²n) pilot floor. These are substantive repairs to the old sketch, not just empirical evidence.
* Nevertheless P6's Lambda(a) still cites Tr(c) beyond its stated family size and bounded dimensions. R2 fixes the constant but R1–R7 do not explicitly rewrite that lemma. R1 enlarges the family exponent for its own chain, but its full-set conditioning dimension s+k₀ can also exceed the printed u≤16 range. R6's Beta identity does not itself extend Tr's quantified range. P7 also prints `(n−3−s)/2` where B(ii) gives `(n−2−s)/2`.

Retain GAP for the supplied general P6/P7 package; this is not a counterexample to LH-iid consistency. A repair is to state the Beta tail/moment lemma for every fixed upper dimension J and conditioning dimension U, enlarge the family exponent accordingly, and shrink positive comparison margins before absorbing RSS noise. Uniform covariance/Schur-complement control is another repair. A-REV3 already gives this obligation. I do not adjudicate whether A-REV6's W7-PART work supplies it or upgrade that earlier verdict.

## Method and output fidelity

The scorer uses H=(n+1)G+I, the determinant ratio against G+I, Q=y'y−n z'H⁻¹z, and ν=.01+n/2 exactly as in 00_COMMON. All theoretical score comparisons are under EX-A; this review supplies no floating-point error theorem.

`v3_engine.h` local_search evaluates the centre, scans all feasible flips and swaps with the centre fixed, then tests `moves>=ell`. Its `returned` neighbour on a move-limit exit need not be an accepted centre; discovery counts the scan either way. `v3_ledger.h` offers the HPM on fresh score events. An un-emitted centre can be cached without being offered, so a later emitted cache hit is not a repair. W6's first-emission or explicit-ledger-insertion requirement is necessary. The existing Methodology §6.10 centre is the current best scored model; it does not specify the exact start mode. LS0 remains an additional algorithm step, with at most `1+(ell+1)max_{k≤K}[p+k(p−k)]` calls.

W6 incorporates A-REV1's explicit strict-output convention, K=min(p,floor(n/2)), potential-run treatment, D2 rate margins and eligible-set interface for (b2). For LS0 its HPM-convention version also needs LS0 on schedule-limit reports, as OP-LS0 explicitly says. No conditioning on completion is used. No new verdict on the entire Gibbs-route statistical instance or T32 is implied.

**E2 (literal GUARD counterexample).** `RuntimeGuard::check` appends a GuardRecord even when elapsed+operation is below allocation; guard-free execution does not append that record. Thus an otherwise identical successful fit with a nonstopping check has different operational diagnostics from the guard-free run. “Every reported output equals” is false if it includes those diagnostics. Restrict the transfer to statistical outputs, scored sets, decisions and execution/status semantics. The guard reads elapsed time and the operation forecast, consumes no random draw, and its nonstopping checks do not alter statistical settings. This is the known diagnostic-scope issue, not a new failure of the LS0 theorem.

## Empirical context and reproduced evidence

O-LS0's saved paired totals report 2,400 matched records, 2,394 completed production fits, 1,829 production-exact fits and zero HPM changes, gains or harms. Six resource-stopped fits must not become six completed paired claims. Its report interprets the 5/7 byte-hash mismatches as BLAS last-bit differences; it reports matching truth supports, truth-score discrepancies at most 5e−8, and minimum compared nonidentical-model margin .002. Matching F(S₀) alone is not a uniform perturbation bound for every score or greedy path. I retain the reported cross-platform qualification rather than certify identical trajectories or general safety.

The report's “M1 holds 18/2400” uses the observed mode mass, not the asymptotic deterministic-reference ELIG statement. Its “M2” is a D_S lattice diagnostic on a selected tractable subsample (297 fits), not the population POP-LAT margin. Its positive eigenvalues at n=200 are not proof of M3 along a sequence. The deterministic LS-score implication is the correct finite-n check; the source reports all 18 premise-satisfying checked fits scored truth. These observations do not validate the theorem's premises at study scale.

All new numerical computation ran on **owls.stat.rice.edu**, not on the laptop. [scripts/check.py](scripts/check.py) is an independent Python implementation of the exact score formula and complete scans, not an invocation of the compiled production engine. Seed 20261102; one BLAS/OpenMP thread. Remote commands, environment, failures and process IDs are recorded in [RUN.md](RUN.md); the final exit status is zero. Saved raw sufficient statistics and all results are under results/ with SHA-256 evidence.

* Forty heterogeneous population cases enumerate every nonprogress neighbour of the c=2 reference (g=2, p=12 algebra test): zero violations of the LH-LAT lower bound. This is a unit-algebra test, not a production partition experiment.
* Six exact-Gram score experiments use p=108, g=9, c=2, ρ=.7, ψ=.5, β=(1.4,−1), one visible hub, and n=200 or 800 (three each). Exact table convolution and max-plus mode agree with S° in all six; LS0 scores truth in all six with two moves; truth is best among those scored in all six. Required D_S margins are positive in every case. The raw records, including reference masses and margins, are [results/ls0.json](results/ls0.json).
* Blocks are analytically assigned as groups, as in W4's experiment; no C++ partition replay or p≫n experiment is claimed. Saved G, z_raw, y_raw'y_raw and θ are sufficient to reconstruct every score. These few finite-n tests support the algebra, not an asymptotic proof or a reproduction of all 2,400 study fits.

## Repairs and overall disposition

Retain Thm 5(b1) as a conditional candidate for **v3 + LS0** with a concrete, jointly justified exact-Gram LH instance. Correct E1's zero-distance bound, G1's separation rate and E2's statistical-output scope; retain the source statuses and the p≫n GAP pending the assigned review. Label the finite-study diagnostics accurately and keep output availability separate from conditional accuracy. Confidence in the conditional LS0 implication and fixed-parameter exact-Gram instance is high; confidence that the p≫n bookkeeping is repairable is high, but it is not closed here. No claim about masked PIPs/evidence, superiority, integrated production deployment or finite-n error rates is added.

## Eight-line summary

1. Thm 5(b1) conditional consistency: VERIFIED for v3 plus LS0.
2. LS-score discovery and Lemma M: VERIFIED; zero-distance move wording: ERROR.
3. LH-LAT and joint exact-Gram consistency: VERIFIED under fixed parameters.
4. The c=2 iid-draw separation inference: GAP without a stronger growth condition.
5. W_Lat/LH-PGD reductions: VERIFIED in the stated lattice scope.
6. Supplied p≫n P6/P7 package: GAP retained; A-REV6's closure is not duplicated.
7. Owls: 40 population checks and six score experiments passed; O-LS0 reports zero changes.
8. Reviewed evidence head SHA: `c70df7c7f383e01978acc5ba29227e941f7adfb1`; final report commit supplied at delivery.
