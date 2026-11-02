# A-REV5 - independent cross-family re-review of Claude's repairs

Reviewer: GPT-6 Astra; Felipe's branch `theory/A-REV5`; 2026-11-02.

**The principal repairs are mathematically sound within their stated restrictions. The complete repaired package is not VERIFIED: it retains ERRORs in ancillary assertions and GAPs in conditioning, cost, random-design extensions, and downstream propagation.** Source statuses are unchanged. "LOCKABLE" below is a recommendation about an exact reviewed component, never an adoption or an upgrade of a sketch, conjecture, or open premise.

## Finding-by-finding verdict table

R1 means `theory/W6-FIXREV1`; CON means its `CONSOLIDATED.md`; T38-S/P mean its `T38_STATEMENT.md`/`T38_PROOF.md`. R2 means `theory/W6-FIXREV2`, ST its `STATEMENTS.md`. Original verdicts refer to A-REV1/A-REV2, not author status labels. VERIFIED applies only to the proposition and hypotheses identified in the row; a corrected restriction is not verification of the old broader assertion.

| Finding | Original verdict | Repair (branch + label) | Re-review verdict | Notes: completeness, changed scope, downstream |
|---|---|---|---|---|
| Theorem B finite inequality; invocation of F | VERIFIED after F'; invocation GAP | R1 CON sections 1.3,2 | VERIFIED | Full bad set, F' union bound, adapted progress domination and feasible family retained. Empty phases, H=0, nonpositive progress, truth already scored and capped beta are supplied. Does not establish statistical premises or delivery. |
| Proposition U independence iff | ERROR | R1 CON section 1.2 U'(iii-1,3) | VERIFIED | Truth removal is restored even when potential is unchanged. MH summation uses the full Bad set. Original witness `{1}->{2}` with truth `{1,2}` remains a counterexample to the old shorthand. |
| Proposition U extra-for-extra neutrality | ERROR | R1 CON section 1.2 U'(iii-2) | VERIFIED | Neutrality now requires family membership; a look-alike exchanged for junk at full junk budget is bad. This is an explicit correction, not a change to B's original three-test definition. |
| Lemma P multiple targets | GAP | R1 CON section 3 | VERIFIED | Earliest of k=card(C)+card(D) labels yields `s_min card(C)/k [1-Q/(k+1)]`; outside killing-label set and denominator are now specified. |
| B-M, IND-T | VERIFIED with uninterrupted-process scope | R1 CON section 2; T38-P section 5.1 | VERIFIED | Past-measurable selection; Markov law needed even for one selected particle; product law for many. Boundary before stage-T mutation gives L+5, after it L+4. No conditioning on eventual completion or global first-fresh score sets. |
| F, F', O, C, B1/B2, c2 floor, scoring refinements, P1, Lemma E | VERIFIED with stated conventions | R1 CON sections 1-3; inherited source proofs | VERIFIED | No substantive replacement; finite algebra remains within original hypotheses. B-sharp/CMP and unrelated premise theorems are not independently certified wholesale here. |
| Lemma S global attainment | ERROR; inequality VERIFIED | R1 CON section 4 S' | VERIFIED | Clipped bound; positive interior equality only for f>1-e, zero unattained infimum for 0<f<=1-e, endpoints separate. Explicit weakening of the false attainment claim; D2 uses the valid interior. |
| D2 finite and r-star | VERIFIED corrected finite form | R1 CON section 5; T38-P section 4.2 | VERIFIED | `r*=(11+2 sqrt(10))/9`; potential first pilot stage, NB' and completed scoring. PXN still prints 1.925: source text is not synchronized. |
| E3(ii) missing q<1 | ERROR | R1 CON section 6 E3' | VERIFIED | Restores locked T22(i-a)'s hypothesis 0<=q<1; u<1 alternative is conditional too. F-REFINE Card 3(i) still repeats the false unrestricted bound. |
| E3 core, centre scoring, scan cost | VERIFIED with qualifications | R1 CON section 6 | VERIFIED | Exact mode DP, eligibility and completed LS0 scans; explicit initial centre emission and +1 score call. LS0 remains a method extension; H3 is not proved by naming E3. |
| Lemma U / EXP' .52 limit, 4.16 multiplier | ERROR | R1 CON section 7; R2 ST sections 3.1,4.1 | VERIFIED | Correct `.51/c=4.08(M+2 sigma^2)/sigma^2`; decreasing for fixed phi. `.52/c` is only an eventual ceiling. PXN's separate <=1 bound is false. |
| NL0 sup/sum quantifiers | GAP | R1 CON section 8 | VERIFIED | Sum of state suprema over labels is the needed object. PG(a) and its multiplicity cost are additional assumptions, explicitly acknowledged; they are not derived from finite B. |
| CE1 blanket correlated-design language | GAP | R1 CON section 9 CE1-narrow | VERIFIED | Explicit exact-Gram sequence with fixed d, one truth/proxy, p=ceil(n^(1/3)); signal gain and Lemma E yield nonvanishing exit. Narrows the claim openly; does not disprove H24 in every family. |
| T38 b1 direct eligibility route | VERIFIED conditional implication | R1 T38-S (b1), T38-P section 3 | VERIFIED | Scoring implication retains eligibility, population margins, posterior ranking and OP-LS0. Does not turn production into an LS0 implementation. |
| T38 b1' rate margins | GAP | R1 CON section 5; T38-S (b1') | VERIFIED | Fixed b0>.1, bounded dangerous set, Dep<=1-c0 and NB' failure vanishing; or explicit diverging exponent rates. These strengthen the incomplete old hypotheses. Masked NB' instance remains sketch. |
| T38 b2 eligibility and repair certificate | GAP | R1 T38-S (b2), T38-P section 5.1 | VERIFIED | Feasible eligible set, capped beta, DELIV and REP, past-selected argmin or product. Genuine delivery premise remains OPEN. D3 surrogate conditioning still GAP (section 3 below). |
| T38 output/execution interface | GAP | R1 T38-S (0),(0_H); T38-P sections 0-1 | VERIFIED | Strict and usable-HPM output conventions distinguished; schedule-limit discovery term retained. Stop-only GUARD, potential execution and no completion conditioning. No vanishing failure probability is inferred. |
| T38 citation and cap | GAP/incorrect citation | R1 T38-P section 1.1, Objects | VERIFIED | Locked T21(C1), not nonexistent T11(vii); K=min(p,floor(n/2)). |
| T03-sharp finite-n onset | ERROR | R2 ST section 1.2 Scope | VERIFIED numerical correction; ERROR replacement gloss | Named thresholds reproduced on Owls. Final suggested sentence still conflates geometric-series and fixed-constant thresholds; see section 3. Core asymptotic theorem unaffected. |
| T03-sharp quantifiers, fixed g0, expectation, anchoring, cutoff, empty strong set | VERIFIED with qualifications | R2 ST sections 1.1-1.2 | VERIFIED | sup_m P, deterministic cutoff; convergence only for expected error; fixed positive g0; global posterior/HPM versus reported HPM. E3 barrier is only for this proof route. Card 1 already has sup_m P, contrary to R2 REPORT. |
| T03 E1/E2, den-prime, I/B, C1-C10, Proposition D | VERIFIED with source hypotheses | R2 ST section 1; source proofs | VERIFIED | Exact BB tail and duplicate example retained; duplicate example violates size-two SE and does not contradict T03-sharp. No finite-n universal onset is supplied. |
| Lemma 0(b) posterior-miss inference | ERROR | R2 ST section 2.4 Lemma 0(b') | VERIFIED | Correct delivery inclusion has previously scored truth and tie alternatives. A below-truth start may discover an above-truth competitor. Does not identify benchmark failures without F_pre. |
| V37 R2 failure dichotomy | ERROR | R2 ST section 2.4 Proposition F | VERIFIED | Three categories by F_pre/F_post versus truth, restricted to failed fits; inferior local optimum and capped search are included. F-REFINE Card 4 remains wrong. |
| Initial centre already truth means trivial success | A-REV2 table shorthand | R2 REPORT section 3.1; ST section 2.4 | VERIFIED disagreement | Starting at truth ensures prior discovery, not final reporting: an improving neighbor can replace it. A-REV2 detailed no-new-delivery sentence is correct; table shorthand is ERROR. |
| A5 literal TD without POS | ERROR | R2 ST section 2.3 A5 | VERIFIED | Adds genuinely necessary positivity premise for this implication. Suppressor example still refutes old A5 at d=0; strict TD at d>=1 remains inconsistent. |
| TD'_P iff strict D_S | ERROR | R2 ST section 2.2 Lemma T | VERIFIED | Tie-broken maximizing map gives exact equivalence; strict separation only sufficient. Duplicate-column tie remains valid counterexample. PGD positive and strict-reversal negative uses survive, with terminology corrected. |
| New null-tie qualification | Not previously reviewed | R2 ST section 2.2 Lemma NT | VERIFIED | Analytic zero-set/rank argument under full-rank union and summed size<n-1; Gaussian noise alone does not suffice. Additional hypotheses are explicit, not a rescue of deterministic iff. |
| "Weakest" prose / at-most-Phi necessity | ERROR | R2 ST section 2.5 | VERIFIED | Withdrawn; necessity is for every move to decrease Phi. A neutral move followed by a two-unit swap can satisfy total length bound. |
| A1-A4 path/cap conclusions | VERIFIED with original qualifications | R2 ST section 2.3 | VERIFIED for feasible path; ERROR literal lattice inclusion | Extra scan gives certification iff ell>=tau, not merely iff truth is scored. New unqualified lattice/count expressions ignore K; see section 3. |
| Selected-centre union bound | GAP outside deterministic cover | R2 ST section 2.6 | VERIFIED restriction | Fixed covering family required; realized 2^Phi of response-selected centre not a probability union budget. Exact printed state count still needs cap correction. |
| V37 R4 Gaussian tail | ERROR | R2 ST section 2.6 | VERIFIED | Use original t with t^2=2 log p+u^2, not p P(abs(Z)>=u). T37 asymptotic extensions stay GAP/sketch. |
| EXP' exact identity and fixed-design bound; R1 certificate | VERIFIED | R2 ST section 3.1 | VERIFIED | Fixed-X bounded blocks, SE and polynomial count; deterministic realized-RSS certificate distinct from probabilistic floor. Does not supply all of locked T22(iii)'s inputs. |
| Theorems 3/4 chain, normalized H3 | VERIFIED with boundary | R2 ST sections 3.2-3.3 | VERIFIED | Deterministic fixed-length chain and bounded leakage; normalized capped H3 retained. Response-selected chain needs a uniform argument; reference transfer remains sketch. |
| Growing leakage iff / "p^-c alone, whatever eta" | ERROR | R2 ST section 3.3 | VERIFIED | Only sufficient exponent condition retained. Zero actual leakage satisfies an arbitrarily loose envelope, so envelope cannot give necessity. |
| Optional limit law | GAP/sketch | R2 ST section 3.3 | GAP | Convergent signal variance and correct fixed/growing-p constants acknowledged; not promoted. |
| Lemma U auxiliary-family quantifier | GAP | R2 ST section 4.1 U(F,H) | VERIFIED asymptotic budget; ERROR printed arrow | H includes all event sets/endpoints; polynomial budget and L>4a_H repair union bound. Printed `1-o(1) ->0` is false; should be ->1, and conclusions are eventual. |
| Lemma U C3 lower with zero leakage only | ERROR | R2 ST section 4.2 C3-low | VERIFIED | Adds mu in span(X_T); this is a real restriction. W2-PREM section 3.4 uses truth supersets and survives. Incomplete-state upper bound remains valid. |
| New weak C3-low' | Not previously reviewed | R2 ST section 4.2 | VERIFIED | RSS_T<=norm(Y)^2<=C_R n gives exponent sigma^2 Z^2/(2C_R). Weaker than old false matching floor, explicitly labelled. |
| Lemma U C1/C2/C4/C5/C6 | VERIFIED within family | R2 ST section 4.2 | VERIFIED | Every telescoping pair must be in F; full all-small-set family covers intended PREM uses. No unbudgeted response-selected family. |
| Random-design EXP' / actual packing | GAP/sketch | R2 ST section 3.4 | GAP | Restricted fixed-partition surrogate retained; B>=2g packing remains unproved. .15 covariance floor and exact Gaussian normalized direction corrected; moment tightness does not prove adaptive packing. |

## Overall verdict per theorem

These distinguish the reviewed mathematical core from the literal complete replacement manuscript.

| Theorem | Overall verdict | Scope |
|---|---|---|
| Theorem B (Gibbs-path) | VERIFIED | Finite feasible uninterrupted bound after F', full Bad definition and beta conventions. Statistical instantiation/delivery remains GAP. |
| T38 statement | ERROR | Unqualified c=2 masking-budget assertion has the counterexample below. Conditional discovery interfaces (0), (0_H), b1', b2 verify; D3 conditioning and cost qualification remain GAP. No unconditional masked production theorem is locked. |
| Lemma S | VERIFIED | Corrected S' including endpoints, positive equality range and unattained zero infimum. |
| D2 | VERIFIED | Corrected finite potential-pilot theorem and explicit-rate implication; masked NB' instance remains GAP/sketch. |
| E3 | VERIFIED | Corrected E3' with q<1, centre emission, completed scans and explicit eligibility; stale CARDS formula is ERROR. |
| Lemma U | ERROR as literally printed; core VERIFIED | The displayed probability limit is false. Budgeted eventual expansion and restricted/new C3 floors verify. The old zero-leakage matching floor stays ERROR. |
| T03-sharp | VERIFIED core | Exact stated asymptotic hypotheses and quantifiers. Replacement onset gloss remains ERROR; it is not a universal finite-n guarantee. |
| Theorem A | ERROR as literally restated; core VERIFIED | Literal untruncated lattice-subset assertion is false under its capped definition. Feasible-lattice path theorem, POS, tie-aware repair and failure partition verify. |
| EXP' | VERIFIED fixed-design core | Correct constant; chain conclusions only with deterministic chain and H3. Random-design/packing and optional limit-law extensions remain GAP/sketch. |

## Residual errors, counterexamples and required qualifications

### 1. Downstream E3, R2, ESS and PXN are not fully repaired

**ERROR - F-REFINE Card 3(i).** Its "any feasible reference" aggregation bound still omits q<1. With n=20, p=2, centered orthogonal columns of norm sqrt(19), y=x2, singleton blocks, and reference {1}, the actual capped normalized mass is 9.441607620478e-14, whereas the printed expression is 1.983334052945e23. The exact BVS score gives q=1.935517816213e12. This is a counterexample within the target formula, not arbitrary table weights. Small p taking enumeration does not validate a false component mass inequality. R1's downstream table missed this CARDS occurrence.

**ERROR - F-REFINE Card 4.** It retains the nonexhaustive R2 split. CEX-1 (n=100,p=12, corr(x1,x2)=.95, mu=3x1-2.8x2, orthogonal noise of squared norm 99) starts at empty below truth, has every singleton gain negative, and certifies empty: F_post<F(truth) and E_LS holds. This is omitted category IIa. The saved original/writer counterexample and the score algebra are inspected; we did not rerun its matrix experiment. Replace the split with Proposition F and retain previously-scored/tie exceptions in the delivery inclusion.

**ERROR - PXN P7's old 1.925 range.** The corrected r-star is 1.924950591148529. As in A-REV1, 77 weights of 1 and 40 of 1.925 have ESS/H<.9. PXN's source must use r-star or directly NB'. Its NB statistical instance remains sketch.

**ERROR - PXN PROOF section 9.1 (U1).** `nu(1.02+1/(n phi^2))/(c_* n)<=1` cannot hold: c_*<=1/16 gives limiting value >=8.16, and M=sigma^2=phi^2=1 gives 12.24. Replace 1 by the displayed O(1) expression and enlarge kappa2. Population margins absorb an O(1) constant; this does not independently verify all PXN results.

### 2. T38's c=2 iid-budget assertion needs a growth condition

**ERROR - T38-S (b1-LH), inherited from W4.** It claims Q_f pi0(S0)->0 for c>=2 and merely p->infinity. Choose c=2 and p asymptotic log log n, rounded to a fixed group-size multiple, with group size 9, fixed admissible LH correlations and coefficients. Exact Gram exists, and eventually B=16 so g<=B<2g. The asserted valid mass law is pi0(S0)=n^-1 p^-2 exp(O_P(1)). The hypothetical final SMC budget has Q_f>=4n(L+6). Thus Q_f pi0(S0) is bounded below by a constant times (log n)/p^2 times exp(O_P(1)), which diverges in probability. Log-tightness of the multiplier makes this a counterexample to the unqualified component assertion.

This slow-p sequence eventually enumerates. Therefore the executed production final-draw count is not the hypothetical SMC count on it: that is an additional branch-qualification GAP, not a justification of the printed component calculation. A direct sufficient condition for the component conclusion is `n^(1-c/2) p^-c log^2 n ->0`; at c=2, p/log n->infinity suffices. State the SMC applicability separately. This error does not refute LS0's scoring implication.

**GAP - T38-P section 5.2 D3.** SHARE is unconditioned, but the conclusion conditions on calibration C and contains data-dependent pi0(X). A rare calibration outcome can contain all losses: an unconditional probability epsilon does not bound a conditional probability 1. State SHARE and EXIT conditional on (data,C), then integrate, or formulate the whole result as an integrated bound. Directly assumed DELIV in b2 avoids this defective surrogate.

**GAP - T38-S (c).** Its proof section 6 says PROVED UNDER T32(i), and dependency k1 calls T32(i) CONJECTURE. The main theorem must retain that qualification. The extra LS0 score count is proved; a full unqualified cost theorem has not thereby acquired a proved source.

### 3. New literal defects in R2

**ERROR - U(F,H) probability arrow, ST section 4.1.** The lower bound `1-C n^(a_H-L/4)-2n^(2/3)/(n-1)` tends to 1 when L>4a_H, not to 0. This is a typographical mathematical error, not a failure of the union-bound proof. Say "for sufficiently large n" (the RSS floor uses theta_n<=1/2) and take nonnegative polynomial budget exponent. E1 costs rank k, E2 costs rank k+s0 including empty V; the displayed constants safely dominate both bounds. No extra SE on V union S0 is needed.

**ERROR - T03 replacement disclosure, ST section 1.2.** The detailed paragraph correctly separates q<=1/2 from exp(2epsilon)<=4. The final proposed sentence saying the proof's deterministic thresholds "as written" hold from roughly two million is too broad. At n=2,116,048 the independent calculation gives q=.499999989 but exp(2epsilon)=4639.924697>4. Specify that the geometric-series threshold crosses there, while the optional displayed fixed-constant threshold crosses at 25,571,897 (and 29,755,302 for the second A). Neither is a universal theorem onset.

**ERROR - cap-free lattice and exact count, ST sections 2.1,2.3,2.6.** With n=4, K=s0=2, S0={1,2}, p>=4, a=1,d=2, the feasible S={1,3} has literal Lat(S) containing {1,2,3}, which is not in R_{a,d}. The displayed missing-truth count also counts {1,3,4} although it is infeasible. A counterexample satisfying the actual TD-P premise is n=8,p=7,K=4, centered orthogonal G=7I, S0={1,2,3,4}, y=(x1+x2+x3+x4)/2, a=d=1. Writing t for the number of truths and k for model size, its exact score up to a common constant is -log binom(13,k)-(k/2)log(8)-4.01 log(.02+7-1.53125t). The 17 feasible region states are truth, the four three-truth models, and the twelve three-truth/one-null models. Their maximizing moves respectively stop, add the missing truth (gain 2.0430749463), or swap null for truth (gain 3.9990864490); direct comparison of the other neighbor types gives smaller scores. Thus TD-P holds throughout the region. Yet Lat({1,2,3,5}) contains infeasible {1,2,3,4,5}. This also directly refutes the conditional A2 subset claim, not just the definition. The independent Owls enumeration verifies all 17 clauses in [cap_witness.json](results/final_run/cap_witness.json). Replace Lat by Lat intersect Omega, and the count by an upper bound, or impose s0+d<=K. This condition is eventually automatic for fixed s0,d, but the deterministic theorem was stated without it. The actual progress path remains feasible; the counting bound used as an upper bound remains useful.

Lemma NT is sound: analyticity reduces persistent ties to `A'-k A''=alpha C`; rank<n-1 forces alpha=0 and k=1, and full rank of the union excludes equal column spaces. In its final sentence, choose the smaller model when one contains the other. This is a proof-writing clarification, not a false theorem. Its extra nondegeneracy conditions must apply at every comparison used.

### 4. W2-T26's exact-branch example is false

**ERROR - PROOF section 1 P1-ex parenthesis and section 3.** The claim that p>=18,n>=22 excludes enumeration fails at p=18,n=262144. K=p, feasible count=262144, whereas the exact-branch threshold is 23706288. The code therefore enumerates. For every fixed p, enumeration eventually holds since the feasible count is bounded and N0 grows with n. Theorem A retains P1-ex as a premise and survives; its example cannot discharge that premise. Theorem B's use of locked T03 and EXP' as an O_P(1) input is consistent with the repairs, but the whole branch is not unconditionally re-verified here.

## Downstream and locked-source reconciliation

| Source | Reconciliation |
|---|---|
| W4-T38FULL | R1 explicitly supersedes its statement/proof. Use the replacement's rate/certificate/execution interface, not the unchanged old text. The slow-p masking and cost qualifications above still require correction. |
| W3-PXN | P3 explicitly retains q<1; P5/P6 use E3(i) and strict progress events as sufficient conditions. Polynomial family budget is compatible with U(F,H). Fix U1 and P7's r-star; do not upgrade random-design/LS0/P7 claims merely from this import audit. |
| W3-PGD | Strict D events imply tie-aware progress; P4/C-LD strict reversals still refute it. Gaussian noise alone does not exclude duplicates; add nondegeneracy or keep tie qualifications. Its separate Lemma U concerns supersets and does not require the invalid omitted-signal floor. Whole Theorem W status unchanged. |
| W2-PREM | section 3.4 matching floor is used at supersets of truth and satisfies repaired C3-low. section 6.3 uses the upper bound at incomplete states, which needs only zero leakage. All-small-set family supplies the budget. CMP, B-sharp and Theorem L are not promoted. |
| W2-T26 | No dependency on false T37 iff or C3 omitted-signal lower bound. It retains start concentration, OUT, realized-stage rates and P1-ex where stated. ORTH sketch stays sketch; false enumeration example removed before use. |
| F-REFINE CARDS | Cards 3(i) and 4 need substantive corrections above. Card 1 already has sup_m P; add fixed-g0 and posterior-versus-discovery clarity where needed. Card 3's deterministic chain/H3 restrictions survive. Broad H24-false prose must be narrowed to CE1's sequence. |

Read against METHODOLOGY_v3, 00_COMMON, individual locked statements/proofs, COLLECTED_PROOFS_v2.tex, LOCKED_PROOFS.md, and the relevant C++ implementation. Locked T22(i-a) and the collected text explicitly say q<1. Locked T27(i) explicitly assumes normalized H3 and H2 for the selected chain; EXP' does not discharge an arbitrary data-selected chain. Locked T21 gives the scored-plus-ranking composition, not H24 or operational success. Locked T03's T02 closure is regime-specific. No locked result was edited or relabelled.

The implementation uses standardized energy n-1, nu=n/2+.01, ridge H=(n+1)G+I, capped BB prior and full-response block tables. These agree with the repairs. No quantile-sampler lambda prior is involved in this model.

`v3_engine.h::local_search` freezes each centre, scores all feasible flips/swaps, uses lex neighbor ties and strict improvement, then scans after ell moves. The ledger uses its separate HPM tie rule. `v3_core.cpp` records the pre-search ledger at lines 445-447 and exports it as **hpm_before_local** at line 479 (the local variable is hpm_before). The proposed benchmark classification needs these actual per-fit values and truth scores; no such extraction was supplied, so section 0/541 forced by monotonicity" remains GAP. A starting truth can be lost even at move cap zero because an improving neighbor is scored on the extra scan.

`RuntimeGuard::check` reads elapsed/operation time and records a stop without RNG use or statistical tuning. The inspected call sites support the stop-only coupling used conditionally in T38. This supplies no probability bound for guards, numerical failures or calibration failure, and is not a claim that machine arithmetic equals EX-A. LS0 must explicitly emit its new centre; production callers' already-scored centres do not implement that extension automatically.

## Independent numerical evidence and audit trail

All new numerical work ran as persistent jobs on **owls.stat.rice.edu**, not on the laptop. Read /home/fb31/AGENTS.md (empty) and checked ancestor/task AGENTS paths before creating the run directories. No scheduler executable was available; used nohup. The original/source scripts and saved outputs are evidence snapshots, not new runs or endorsements.

- First job: `/home/fb31/theory_campaign/A-REV5/run_20261102`, launcher PID 2566728. Independent scalar check exited 0; source threshold replay exited 1 (NumPy missing). The first independent E3 normalizer was also found to omit the size-two model and corrected before relying on its value. This superseded attempt is preserved, not used as final evidence.
- Final job: `/home/fb31/theory_campaign/A-REV5/run_20261102_v2`, launcher PID 2567195, scalar process PID 2567201, started 2026-11-02T21:11:53Z. Both independent scalar and dependency-free threshold checks exited **0**. Inspected logs, saved JSON and exit status; process no longer active. Deterministic scripts: no random seed needed (seed=null).
- Additional persistent cap-witness job: launcher PID 2575341, `nohup sh cap_run.sh > cap_launcher2.log 2>&1 < /dev/null`, exit **0**; saved cap_pid, cap_started/cap_ended, cap_hash, log and JSON. A malformed nested-shell launch was stopped before this file-based launch; it is not evidence.
- Exact launch: `cd /home/fb31/theory_campaign/A-REV5/run_20261102_v2; nohup sh run.sh > launcher.log 2>&1 < /dev/null & echo $! > pid.txt`. Saved run.sh records actual Python commands, environment, SHA-256 hashes, timestamps and exit statuses.
- [Final saved evidence](results/final_run/independent.json), [threshold boundary checks](results/final_run/thresholds.json), [environment](results/final_run/environment.txt), [exit statuses](results/final_run/exit_status.txt), [scripts](scripts/). Source-manifest SHA-256 hashes and baseline hashes are retained separately.

| Decisive check | Inspected final result |
|---|---|
| ESS inadmissible old equality weights | f=.05,e=.9 gives unclipped share -.0226483157 and low weight -.4529663145. |
| E3 old unrestricted bound | 1.983334052945e23 versus normalized reference mass 9.441607620478e-14. |
| U C3 omitted-signal counterexample | Actual centered log BF 16.2502645682; old lower bound 19.5571554183; kappa=12.2400132448. |
| U/EXP' constant and PXN <=1 | Correct limit 12.24 at unit parameters; universal minimum for PXN expression 8.16. |
| T03 q crossing | At 2,116,047/2,116,048: .500000926/.499999989; at 2,457,024/2,457,025: .500000009/.499999191. |
| T03 fixed-constant crossing | exp(2epsilon) crosses 4 at 25,571,897 and 29,755,302; predecessor checks remain above 4. |
| Theorem A cap witness | All 17 feasible states satisfy TD-P; literal lattice still contains an infeasible five-variable model. |
| T26 enumeration witness | 262144 feasible models <=23706288 exact threshold. |

Threshold code uses a separate standard-library log recurrence and suffix sums, checking a geometric tail bracket so truncation cannot change m-sharp. These are point/boundary checks, not a proof that no earlier nonmonotone crossing exists. They decide the disputed onset disclosure without allocating large designs. Numerical evidence corroborates identities/counterexamples, not asymptotic hypotheses or production discovery.

## LOCKABLE components - no status changes made

The requested rule is applied to exact components: author PROVED plus same-family review and cross-family verification, or an author repair now re-verified. Prior same-family reviews are W2-VT24G, W3-VT38E, W2-VT03R, W3-VT37R and W3-VEXP as appropriate. Their old endorsements of erroneous text do not certify that text; the repair/re-review chain below identifies what can be locked instead.

1. **The finite Theorem B with F' and CON section 2 conventions**, plus corrected U' bookkeeping and multi-target P. Lock only the feasible uninterrupted implication, not H24/B-sharp/CMP or delivery.
2. **Lemma S'; finite D2 with r-star/NB'; D2-infinity with explicit rate margins.** The statistical masked NB' instance is excluded.
3. **E3' with q<1, centre emission and completed scans.** Eligibility/TD/H3 remain inputs and LS0 remains a method change.
4. **T03-sharp's core asymptotic statement and exact-tail lemmas** under its explicit hypotheses. Exclude the erroneous replacement onset gloss.
5. **Tie-aware Lemma T, POS-repaired A5, Lemma 0(b'), failed-fit Proposition F, and Lemma NT under nondegeneracy.** Exclude the literal cap-free lattice/count assertion and unavailable benchmark conclusions. The feasible-lattice path theorem can be locked only with that scope written into the adopted text.
6. **Fixed-design EXP' with the corrected .51 constant; deterministic-chain Theorems 3/4 with H3.** Exclude random packing, reference-transfer and optional limit-law sketches.
7. **The re-verified U budget argument and C3-up / signal-contained C3-low / weak C3-low' components.** Do not lock the complete printed Lemma U until its probability arrow and eventual-domain wording are corrected; those corrections are explicitly verified algebraically above.
8. **T38's isolated conditional composition and b1'/b2 interfaces**, under GUARD, execution and named premises. Do not lock the whole T38 statement: masking-budget ERROR, D3 conditioning GAP and T32 cost GAP remain. CE1-narrow can be retained as the re-verified explicit counterexample, not universal failure.

No new result is entered in LOCKED_PROOFS.md. No PROOF SKETCH, CONJECTURE or OPEN item is upgraded. "Now LOCKABLE" does not mean the stale source branch or its ancillary false sentences can be copied without the restrictions just stated.

## Source versions and review integration

All source reads are pinned in [sources/manifest.json](sources/manifest.json), with byte hashes. Baseline methodology/common/C++/proof hashes are in [results/baseline_hashes.json](results/baseline_hashes.json). Supporting independent scoped checks are [REV1_CHECK.md](REV1_CHECK.md) and [REV2_CHECK.md](REV2_CHECK.md); their findings were inspected and adjudicated by the Astra primary. They ran no numerical workloads. The present report controls where its overall verdicts distinguish literal text from valid cores.

| Branch | Inspected head |
|---|---|
| theory/A-REV1 | `26815e841f25cd472a20f8ea251c00b4ffab3e37` |
| theory/A-REV2 | `09dc2307b3b4a133765877239d5cd2149c25cd89` |
| theory/W6-FIXREV1 | `a7833f3d185d188ca48c7cb4a12faf4397ac63de` |
| theory/W6-FIXREV2 | `be2d4568bca74dec2ae6dd08e25fe709c3da44f6` |
| theory/W4-T38FULL | `a0f9cb5e000dedf367e26fd0da019ccd2218fb42` |
| theory/W3-PXN | `4aebea3bf003f5f3c0c7239a24c824ec2d2aa574` |
| theory/W3-PGD | `fdeaec34f5a23ced83ccd85b5bf00ee643cbcba0` |
| theory/W2-T26 | `0e4f1e7f5efd1e67330affa4168b69750eaff2f1` |
| theory/F-REFINE | `db708ca9f98a616ea16c8ce8e950d8f65238835f` |

## Eight-line summary

1. Principal repairs: VERIFIED within explicit restricted hypotheses; no source status upgraded.
2. T38: ERROR in unqualified c=2 budget claim; D3 conditioning and cost remain GAP.
3. S', finite/rate D2, E3' and finite B: VERIFIED; downstream propagation incomplete.
4. T03-sharp and fixed-design EXP' cores: VERIFIED; onset gloss and random extensions excluded.
5. Theorem A feasible core: VERIFIED; literal cap-free lattice is ERROR; U probability arrow is ERROR.
6. CARDS, PXN and T26 retain ERRORs with counterexamples; benchmark pre-search classification remains GAP.
7. Owls final jobs exited 0; source snapshots, scripts, hashes, logs and outputs are saved under A-REV5.
8. Reviewed head SHA: HEAD_SHA_PLACEHOLDER (review-content commit; final audit commit records this immutable head).
