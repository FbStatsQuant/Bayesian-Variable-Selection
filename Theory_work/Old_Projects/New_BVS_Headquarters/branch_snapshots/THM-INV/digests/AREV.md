# Digest of the cross-family (Astra/Codex GPT) reviews A-REV5 to A-REV9

Source: `git show origin/theory/<ID>:theory_campaign/<ID>/<file>` for A-REV5 (REVIEW, REV1_CHECK, REV2_CHECK), A-REV6 (REVIEW, STATUS, PARTITION, SHARE, WEIGHTS, BOOK), A-REV7 (REVIEW), A-REV8 (REVIEW, RUN), A-REV9 (REVIEW, DILUTE_STAGES_CHECK, MASKED_PW2_CHECK). No computation by this digest. Verdict words are copied from the reviews and are never upgraded. "(?)" marks my own uncertainty about reading or mapping.

## 0. Global caveats that apply to nearly every row

- Every reviewer says VERIFIED means "the stated implication checks under the stated hypotheses". It does not mean adopted, locked, or that a PROOF SKETCH / CONJECTURE / OPEN item is upgraded. A-REV5: "VERIFIED applies only to the proposition and hypotheses identified in the row; a corrected restriction is not verification of the old broader assertion." "LOCKABLE" is a recommendation about an exact component only.
- All affirmative results are in exact arithmetic (EX-A/EX-S), under fresh-randomness assumptions, the "potential execution" convention (the run is imagined to complete), stop-only GUARD coupling, and successful calibration. A-REV5: GUARD "supplies no probability bound for guards, numerical failures or calibration failure, and is not a claim that machine arithmetic equals EX-A." A-REV8: "this review supplies no floating-point error theorem." A-REV9: "These support the exact component model, not a universal floating-point assertion."
- Fixed p eventually takes exact enumeration in production (A-REV7, A-REV8, A-REV5). Any "SMC component" result at fixed p is a component result, not an asymptotic SMC separation.
- Reviews A-REV5, A-REV6, A-REV7, A-REV9 ran no numerical workloads (A-REV5 and A-REV7 and A-REV8 ran small deterministic/scalar checks on owls; see section 6 of this file). Numerics corroborate identities and counterexamples, not asymptotic hypotheses or production discovery (A-REV5).
- Tags in the last column: [AS-RUN] = statement is about the algorithm as it exists (still under EX-A, iid fresh draws, potential run); [LS0] = needs the LS0 method extension (extra emitted centre + completed local scan), not production; [IDEAL] = idealised model (exact two-state or ORTH or four-state abstract example, frozen-run, exact enumeration, etc.); [ABSTRACT] = abstract finite or probabilistic lemma with no BVS-specific claim; [MIXED] = see Notes.

## 1. Verdict table (one row per result reviewed)

Source-task shorthand: R1 = W6-FIXREV1 (CON = CONSOLIDATED.md), R2 = W6-FIXREV2 (ST = STATEMENTS.md).

### 1a. A-REV5 (re-review of W6-FIXREV1 / W6-FIXREV2 repairs)

Overall A-REV5 verdict (verbatim): "The principal repairs are mathematically sound within their stated restrictions. The complete repaired package is not VERIFIED: it retains ERRORs in ancillary assertions and GAPs in conditioning, cost, random-design extensions, and downstream propagation."

| Result (source task) | Reviewer | Verdict (verbatim) | Exact scope | Open gaps listed | As-run vs idealised |
|---|---|---|---|---|---|
| Theorem B finite inequality + invocation of F (R1 CON 1.3, 2) | A-REV5 | VERIFIED (orig. "VERIFIED after F'; invocation GAP"). Overall: "Theorem B (Gibbs-path): VERIFIED" | Finite feasible uninterrupted bound after F', full Bad definition, capped beta; empty phases, H=0, nonpositive progress, truth already scored supplied | "Does not establish statistical premises or delivery." Statistical instantiation/delivery remains GAP | [IDEAL] uninterrupted process, past-measurable selection |
| Proposition U independence iff (R1 CON 1.2 U'(iii-1,3)) | A-REV5 | VERIFIED (orig. ERROR) | Truth removal restored; MH summation over full Bad set | Original witness {1}->{2} with truth {1,2} still counterexample to old shorthand | [IDEAL] |
| Proposition U extra-for-extra neutrality (U'(iii-2)) | A-REV5 | VERIFIED (orig. ERROR) | Neutrality requires family membership | Explicit correction, not change to B's three-test definition | [IDEAL] |
| Lemma P multiple targets (R1 CON 3) | A-REV5 | VERIFIED (orig. GAP) | Earliest of k=card(C)+card(D) labels gives s_min card(C)/k [1-Q/(k+1)] | none listed | [IDEAL] |
| B-M, IND-T (R1 CON 2; T38-P 5.1) | A-REV5 | VERIFIED (orig. "VERIFIED with uninterrupted-process scope") | Markov law needed even for one selected particle; product law for many; L+5 before stage-T mutation boundary, L+4 after | "No conditioning on eventual completion or global first-fresh score sets" | [IDEAL] potential run |
| F, F', O, C, B1/B2, c2 floor, scoring refinements, P1, Lemma E | A-REV5 | VERIFIED (orig. "VERIFIED with stated conventions") | Finite algebra within original hypotheses | "B-sharp/CMP and unrelated premise theorems are not independently certified wholesale here" | [ABSTRACT] |
| Lemma S global attainment (S') | A-REV5 | VERIFIED (orig. "ERROR; inequality VERIFIED"). Overall: "Lemma S: VERIFIED" | Clipped bound; positive interior equality only f>1-e; zero unattained infimum for 0<f<=1-e; endpoints separate | none; "explicit weakening of the false attainment claim" | [ABSTRACT] |
| D2 finite, r-star (R1 CON 5; T38-P 4.2) | A-REV5 | VERIFIED. Overall: "D2: VERIFIED" | r*=(11+2 sqrt 10)/9; potential first pilot stage, NB', completed scoring | "PXN still prints 1.925: source text is not synchronized"; "masked NB' instance remains GAP/sketch" | [IDEAL] potential pilot |
| E3(ii) missing q<1 (R1 CON 6 E3') | A-REV5 | VERIFIED (orig. ERROR). Overall: "E3: VERIFIED" | Restores locked T22(i-a) hypothesis 0<=q<1; u<1 alternative is conditional too | F-REFINE Card 3(i) "still repeats the false unrestricted bound" (stale CARDS formula is ERROR) | [LS0] for centre emission; start mass deterministic bound |
| E3 core, centre scoring, scan cost (R1 CON 6) | A-REV5 | VERIFIED (orig. "VERIFIED with qualifications") | Exact mode DP, eligibility, completed LS0 scans, explicit initial centre emission, +1 score call | "LS0 remains a method extension; H3 is not proved by naming E3" | [LS0] |
| Lemma U / EXP' .52 limit, 4.16 multiplier (R1 CON 7; R2 ST 3.1, 4.1) | A-REV5 | VERIFIED (orig. ERROR) | Correct .51/c=4.08(M+2 sigma^2)/sigma^2; decreasing for fixed phi; ".52/c is only an eventual ceiling" | "PXN's separate <=1 bound is false" | [IDEAL] fixed design |
| NL0 sup/sum quantifiers (R1 CON 8) | A-REV5 | VERIFIED (orig. GAP) | Sum of state suprema over labels | "PG(a) and its multiplicity cost are additional assumptions ... not derived from finite B" | [IDEAL] |
| CE1 blanket correlated-design language -> CE1-narrow (R1 CON 9) | A-REV5 | VERIFIED (orig. GAP) | Explicit exact-Gram sequence, fixed d, one truth/proxy, p=ceil(n^(1/3)); signal gain + Lemma E give nonvanishing exit | "Narrows the claim openly; does not disprove H24 in every family" | [IDEAL] counterexample family; refutes only vanishing uniform exit premise on it |
| T38 b1 direct eligibility route (T38-S b1; T38-P 3) | A-REV5 | VERIFIED (orig. "VERIFIED conditional implication") | Scoring implication retains eligibility, population margins, posterior ranking and OP-LS0 | "Does not turn production into an LS0 implementation" | [LS0] |
| T38 b1' rate margins (T38-S b1') | A-REV5 | VERIFIED (orig. GAP) | Fixed b0>.1, bounded dangerous set, Dep<=1-c0, NB' failure vanishing; or explicit diverging exponent rates | "Masked NB' instance remains sketch" | [IDEAL]/conditional rate interface |
| T38 b2 eligibility and repair certificate (T38-S b2; T38-P 5.1) | A-REV5 | VERIFIED (orig. GAP) | Feasible eligible set, capped beta, DELIV and REP, past-selected argmin or product | "Genuine delivery premise remains OPEN"; D3 surrogate conditioning GAP | [AS-RUN?] conditional on DELIV (?) |
| T38 output/execution interface (T38-S 0, 0_H) | A-REV5 | VERIFIED (orig. GAP) | Strict vs usable-HPM output conventions; schedule-limit discovery term; stop-only GUARD; potential execution | "No vanishing failure probability is inferred" | [IDEAL] potential run |
| T38 citation and cap | A-REV5 | VERIFIED (orig. "GAP/incorrect citation") | Locked T21(C1) not nonexistent T11(vii); K=min(p,floor(n/2)) | none | n/a |
| T38 statement as a whole (overall table) | A-REV5 | **ERROR** | "Unqualified c=2 masking-budget assertion has the counterexample below. Conditional discovery interfaces (0), (0_H), b1', b2 verify; D3 conditioning and cost qualification remain GAP." | "No unconditional masked production theorem is locked." | [MIXED] |
| T38 (b1-LH) c>=2 iid-budget assertion Q_f pi0(S0)->0 for c>=2, p->infinity | A-REV5 | ERROR (inherited from W4) | c=2, p ~ log log n, group size 9, fixed LH parameters | Slow-p sequence eventually enumerates, so executed production final-draw count is not the hypothetical SMC count: "branch-qualification GAP". Sufficient condition n^(1-c/2) p^-c log^2 n -> 0 (p/log n->infinity at c=2) | [IDEAL] hypothetical SMC budget; "does not refute LS0's scoring implication" |
| T38 D3 conditioning (T38-P 5.2) | A-REV5 | GAP | SHARE unconditioned but conclusion conditions on calibration C and data-dependent pi0(X); state conditional on (data,C) then integrate | DELIV assumed directly avoids defective surrogate | [IDEAL] |
| T38 (c) polynomial cost corollary | A-REV5 | GAP | Proof says "PROVED UNDER T32(i)", dependency calls T32(i) CONJECTURE | Main theorem must retain qualification; "LS0 extra score count is proved; a full unqualified cost theorem has not thereby acquired a proved source" | [AS-RUN count] conditional on T32(i) CONJECTURE |
| T03-sharp finite-n onset (R2 ST 1.2) | A-REV5 | VERIFIED numerical correction; ERROR replacement gloss | Thresholds reproduced on owls (geometric-series crossing near 2,116,048; fixed-constant crossing 25,571,897 and 29,755,302) | "Neither is a universal theorem onset"; replacement sentence conflates the two thresholds | [AS-RUN] posterior concentration |
| T03-sharp core (quantifiers, fixed g0, expectation, anchoring, cutoff) (R2 ST 1.1-1.2). Overall: "T03-sharp: VERIFIED core" | A-REV5 | VERIFIED (orig. "VERIFIED with qualifications") | sup_m P, deterministic cutoff; convergence only for expected error; fixed positive g0; global posterior/HPM vs reported HPM | "not a universal finite-n guarantee"; E3 barrier only for this proof route | [AS-RUN] posterior (statistical, not search) |
| T03 E1/E2, den-prime, I/B, C1-C10, Proposition D (R2 ST 1) | A-REV5 | VERIFIED (orig. "VERIFIED with source hypotheses") | Exact BB tail; duplicate example violates size-two SE | "No finite-n universal onset is supplied" | [AS-RUN] |
| Lemma 0(b) posterior-miss inference -> 0(b') (R2 ST 2.4) | A-REV5 | VERIFIED (orig. ERROR) | Delivery inclusion has previously scored truth and tie alternatives | "Does not identify benchmark failures without F_pre" | [AS-RUN] |
| V37 R2 failure dichotomy -> Proposition F (R2 ST 2.4) | A-REV5 | VERIFIED (orig. ERROR) | Three categories by F_pre/F_post vs truth, restricted to failed fits | F-REFINE Card 4 remains wrong; benchmark classification needs actual per-fit F_pre and truth scores (extraction not supplied): GAP | [AS-RUN] |
| "Initial centre already truth means trivial success" | A-REV5 | VERIFIED disagreement (A-REV2 table shorthand is ERROR) | Starting at truth ensures prior discovery, not final reporting; improving neighbour can replace it | none | [AS-RUN] |
| A5 literal TD without POS (R2 ST 2.3) | A-REV5 | VERIFIED (orig. ERROR) | Adds positivity premise POS | "Strict TD at d>=1 remains inconsistent" | [IDEAL] |
| TD'_P iff strict D_S -> Lemma T (R2 ST 2.2) | A-REV5 | VERIFIED (orig. ERROR) | Tie-broken maximizing map gives exact equivalence; strict separation only sufficient | Duplicate-column tie remains counterexample | [IDEAL] |
| Lemma NT null-tie qualification (new) | A-REV5 | VERIFIED (not previously reviewed) | Analytic zero-set/rank argument, full-rank union, summed size<n-1 | "Gaussian noise alone does not suffice"; extra hypotheses must hold at every comparison | [IDEAL] |
| "Weakest" prose / at-most-Phi necessity (R2 ST 2.5) | A-REV5 | VERIFIED (withdrawn; orig. ERROR) | Necessity is for every move to decrease Phi | none | n/a |
| A1-A4 path/cap conclusions; Theorem A overall | A-REV5 | VERIFIED for feasible path; ERROR literal lattice inclusion. Overall: "Theorem A: ERROR as literally restated; core VERIFIED" | Feasible-lattice path theorem, POS, tie-aware repair, failure partition | Literal cap-free Lat(S) and missing-truth count ERROR (counterexample n=8,p=7,K=4; section 2 below) | [IDEAL] |
| Selected-centre union bound (R2 ST 2.6) | A-REV5 | VERIFIED restriction (orig. "GAP outside deterministic cover") | Fixed covering family required; realized 2^Phi of response-selected centre not a union budget | Exact printed state count needs cap correction | [IDEAL] |
| V37 R4 Gaussian tail (R2 ST 2.6) | A-REV5 | VERIFIED (orig. ERROR) | Use original t, t^2=2 log p+u^2 | "T37 asymptotic extensions stay GAP/sketch" | [ABSTRACT] |
| EXP' exact identity and fixed-design bound; R1 certificate (R2 ST 3.1). Overall: "EXP': VERIFIED fixed-design core" | A-REV5 | VERIFIED | Fixed-X bounded blocks, SE, polynomial count; deterministic realized-RSS certificate distinct from probabilistic floor | "Does not supply all of locked T22(iii)'s inputs"; random-design/packing and optional limit-law extensions GAP/sketch | [IDEAL] fixed design |
| Theorems 3/4 chain, normalized H3 (R2 ST 3.2-3.3) | A-REV5 | VERIFIED (orig. "VERIFIED with boundary") | Deterministic fixed-length chain, bounded leakage, normalized capped H3 | "Response-selected chain needs a uniform argument; reference transfer remains sketch" | [IDEAL] |
| Growing leakage iff / "p^-c alone, whatever eta" | A-REV5 | VERIFIED (orig. ERROR) | Only sufficient exponent condition retained | none | n/a |
| Optional limit law (R2 ST 3.3) | A-REV5 | **GAP** | Convergent signal variance, fixed/growing-p constants acknowledged; not promoted | sketch | [IDEAL] |
| Lemma U auxiliary-family quantifier / U(F,H) (R2 ST 4.1). Overall: "Lemma U: ERROR as literally printed; core VERIFIED" | A-REV5 | VERIFIED asymptotic budget; ERROR printed arrow | H includes all event sets/endpoints; polynomial budget; L>4a_H | "Printed 1-o(1) -> 0 is false; should be ->1, and conclusions are eventual" | [IDEAL] |
| Lemma U C3 lower with zero leakage only -> C3-low (R2 ST 4.2) | A-REV5 | VERIFIED (orig. ERROR) | Adds mu in span(X_T) (real restriction) | Old zero-leakage matching floor "stays ERROR"; incomplete-state upper bound valid | [IDEAL] |
| Weak C3-low' (new) | A-REV5 | VERIFIED (not previously reviewed) | RSS_T<=norm(Y)^2<=C_R n gives exponent sigma^2 Z^2/(2 C_R) | "Weaker than old false matching floor" | [IDEAL] |
| Lemma U C1/C2/C4/C5/C6 | A-REV5 | VERIFIED (orig. "VERIFIED within family") | Every telescoping pair in F; all-small-set family | No unbudgeted response-selected family | [IDEAL] |
| Random-design EXP' / actual packing (R2 ST 3.4) | A-REV5 | **GAP** | Restricted fixed-partition surrogate retained | "B>=2g packing remains unproved"; ".15 covariance floor ... corrected"; moment tightness does not prove adaptive packing | [IDEAL] surrogate only |

A-REV5 REV1_CHECK / REV2_CHECK (helper checks, adjudicated by Astra primary). REV2_CHECK overall verdict (verbatim): "GAP for the complete package; the central repaired deterministic statements are VERIFIED with the qualifications below." REV1_CHECK verbatim: "The central A-REV1 repairs in W6-FIXREV1 check as conditional implications. The downstream package still contains an ERROR repeating the missing q<1 condition, an ERROR in the exact-branch example, and statement/proof qualification GAPs." REV1_CHECK additionally lists: W3-PXN P7 "PROVED for D2-a,b,c; PROOF SKETCH for D2-d"; W3-PGD Theorem W "PROVED (candidate)" with "No blanket cross-family verification of W3-PGD is supplied"; W2-T26 Theorem A "PROVED (composition; all inputs locked)", Theorem B conditional, ORTH Proposition C PROOF SKETCH.

Downstream/locked-source rows from A-REV5 (verdicts verbatim):

| Result | Reviewer | Verdict | Scope / gaps |
|---|---|---|---|
| F-REFINE Card 3(i) | A-REV5 | ERROR | Omits q<1 (counterexample section 2) |
| F-REFINE Card 4 | A-REV5 (REV2_CHECK) | ERROR | Retains nonexhaustive R2 split; omitted category IIa (CEX-1) |
| W3-PXN P7 old 1.925 range | A-REV5 | ERROR | r* = 1.924950591148529; ESS/H<.9 for 77 weights of 1 and 40 of 1.925 |
| W3-PXN PROOF 9.1 (U1) | A-REV5 | ERROR | nu(1.02+1/(n phi^2))/(c_* n)<=1 cannot hold (limit >=8.16; 12.24 at unit parameters) |
| W3-PXN, W3-PGD, W2-PREM, W2-T26 (reconciliation) | A-REV5 | no new status; "do not upgrade random-design/LS0/P7 claims merely from this import audit" | W3-PGD "Whole Theorem W status unchanged"; W2-PREM "CMP, B-sharp and Theorem L are not promoted" |
| W2-T26 PROOF section 1 P1-ex parenthesis (p>=18, n>=22 excludes enumeration) | A-REV5 | ERROR | False at p=18, n=262144 (count 262144 <= threshold 23706288); Theorem A retains P1-ex as premise and survives |
| W4-T38FULL | A-REV5 | superseded by R1 | "Use the replacement's rate/certificate/execution interface, not the unchanged old text" |

### 1b. A-REV6 (later repairs; overall "GAP, with the original ERROR findings preserved and additional ERROR findings in replacement text")

Note: A-REV6 itself says "VERIFIED below means the specified mathematical implication checks under its stated assumptions". Candidates authored by Astra (M-star, EXIT-star, SH-star, NM-R, W2-R, BOOK R1-R5) are "Astra-authored and pending independent Claude verification" and not counted as repairs.

| Result (source task) | Reviewer | Verdict (verbatim) | Exact scope | Open gaps | As-run vs idealised |
|---|---|---|---|---|---|
| W3-PXN P1 actual random blocks (W7-PART Thm B) | A-REV6 | VERIFIED on SIZE and fixed correlation separation | LH-iid, fixed population correlation gap, g<=B<2g, polynomial p including p>>n; bound P(fail)<=[2/(sqrt(pi)(1-rho))] p^2 sqrt(n) exp(-(n-4) I*) | "Only the restricted recovery premise; not the full result"; exact density a cited input; shrinking gap needs new rate | [AS-RUN] partition (X-only) on restricted LH-iid |
| W3-PXN P2, B, Tr, P3-P5, P8 | A-REV6 | VERIFIED in their original scopes | "Tr is not thereby extended to arbitrary fixed dimensions" | | [IDEAL] |
| W3-PXN P6 / Lambda dimension and family count (W5-VMASK R2) | A-REV6 | GAP | R2 fixes U1 not Lambda's Tr(c) range (Tr: j<=16,u<=16, n^(A+1)2^17 variables vs ~p^(s0+2) sets) | generalised tail lemma needed | [IDEAL] |
| W3-PXN P6 U1 arithmetic | A-REV6 | VERIFIED replacement constant | fixed O(1) constant not <=1 | | n/a |
| W3-PXN P7 no-tweak pilot route (W5-VMASK R1/R3/R6) | A-REV6 | GAP | Cap injection, summed tail, Beta shape repaired; P7 prints (n-3-s)/2 vs correct (n-2-s)/2 | Tr dimension still must be generalized; "c=1 restriction remains" (D2 needs Gibbs distance one) | [AS-RUN?] no-LS0 pilot route, c=1 (?) |
| W3 joint T38(b), LS0 route (W5-VMASK R1-R7, W7-PART B) | A-REV6 | GAP | Partition recovery does not close lattice proof bookkeeping or operational assumptions | | [LS0] |
| W4-SHARE D4 | A-REV6 | VERIFIED | Predictable killed Laplace process; fresh independent particle-round randomness; conditional, exact arithmetic | "Neither theorem supplies confinement or terminal repair for BVS" | [ABSTRACT] |
| W4-SHARE D5 | A-REV6 | VERIFIED | Exact retention product | Confinement and TRACK remain inputs | [ABSTRACT] |
| W4 SH(i),(ii), exact (iii) binomial formula | A-REV6 | VERIFIED | | Converse needs vanishing no-outsider probability | [ABSTRACT] |
| W4 SH universal transition wording | A-REV6 | GAP (SH-star: "GAP pending Claude") | | Needs Na,Nb->infinity; rare-outsider counterexample (pi0(o)=1/N gives no-outsider prob -> e^-1) | [ABSTRACT] |
| W4 G oscillation identity / ESS-only obstruction | A-REV6 | VERIFIED | Abstract identity and obstruction only | | [ABSTRACT] |
| W4 G universal BVS/grid extrapolation | A-REV6 | GAP | "Neither proves impossibility for every grid condition on production BVS" (F-SHARE F1, O-BGIBBS BG3 are different conditional routes) | | [ABSTRACT] |
| W4 M(a) | A-REV6 | VERIFIED | Schur/Cauchy bound, normalized Gram eigenvalue | | [ABSTRACT] |
| W4 M(b) quadratic expansion | A-REV6 | ERROR (M-star: "GAP pending Claude; original ERROR retained") | orthogonal theta=1 counterexample: gain/n -> log(2)/2 vs quadratic term/n -> 1/4 | | [IDEAL] |
| W4 M(b) BM-C vanishing crossing | A-REV6 | ERROR | theta^2=C log n/n gives crossing -> 3/C; W5-B2ENV M-LH "VERIFIED for fixed-coefficient M-LH"; M-star "GAP pending Claude" | BM-infinity restriction essential | [IDEAL] |
| W4 M(b) path reaches S0 / automatic repair | A-REV6 | GAP | Addition path ends at S0 plus extras; closure, deletion, traversal separate | | [IDEAL] |
| W4 section 7 conditional B2-W4 | A-REV6 | VERIFIED | product-form inequality; uniform REPAIR on same region, conditional island independence | | [ABSTRACT] |
| W4 section 7 coefficient-one exit-loss simplification | A-REV6 | ERROR (EXIT-star: GAP pending Claude) | Counterexample: one-way a->o mutation, retention 1/2; keep -sum log(1-eta) | | [ABSTRACT] |
| W2-T26 Lemma 1 | A-REV6 | VERIFIED | | | [IDEAL] |
| W2-T26 Lemmas 2-3 | A-REV6 | VERIFIED | terminal-prefix audit; refreshed occupancy | | [IDEAL] |
| W2-T26 actual Theorem A | A-REV6 | VERIFIED | "Keep P1-ex, EX-A/EX-S and output intersection" | | [IDEAL] |
| W2-T26 single-premise shorthand | A-REV6 | VERIFIED replacement; original GAP | | | |
| W2-T26 Theorem B | A-REV6 | VERIFIED | EXP'/VIS/NL and posterior hypotheses retained | | [IDEAL] |
| W2-T26 Prop C (ORTH) | A-REV6 | GAP | "Source remains sketch; ORTH cannot cover p>n-1" | | [IDEAL] |
| W2-T26 exact-branch parenthesis | A-REV6 | GAP pending Claude (original ERROR retained; (?) table label for the repair vs BOOK "ERROR remains") | p=18,n=2^18 selects exact enumeration | | |
| W2-BOOK Lemma RO | A-REV6 | VERIFIED conditional implication; R1 pending Claude | nonnegative potential values, chosen output projection | | [IDEAL] |
| W2-BOOK literal GUARD | A-REV6 | GAP for operational validation; original ERROR | statistical stop-only coupling supported; metadata/allocation excluded; "no returned partial value" is false (v3_run.R assigns HPM before non-completed early return) | | [AS-RUN] static code reading |
| W2-BOOK Prop 2 island formula | A-REV6 | VERIFIED fixed-data identity | E[Zbar Pbar]=Zp/4+3Z E[P1]/4; "never pooled-product unbiasedness" | | [IDEAL] |
| W2-BOOK Prop 2 probability convention / exact extension | A-REV6 | ERROR in W5 full-output expectation | E[1_O Zhat]<=Z P(A) false when exact branch present and A SMC-only | | [IDEAL] |
| BOOK completed wrong HPM means posterior miss | A-REV6 | ERROR (W5 strict scored-competitor certificate VERIFIED restricted) | "Completion alone never proves discovery" | | |
| BOOK size-prior ceiling | A-REV6 | VERIFIED tie-aware criterion; ERROR in W5 paraphrase | equal-likelihood competitor may lose tie order to S0 | | |
| BOOK VAL-FP (W7-SEC T33-Z/H) | A-REV6 | GAP operationally; implication VERIFIED | exact comparator, rounding, useful epsilon still required; W7 "explicitly concedes a vacuous useful epsilon at the study budgets" | "No interval-certified" numerics | [AS-RUN] fp, not certified |
| BOOK numerical/provenance qualifications | A-REV6 | GAP for interval-certified deployment | | | |
| F-DRAFT Prop NM (NM-R candidate) | A-REV6 | ERROR (original); NM-R "GAP pending Claude" | NM-R is a four-state abstract example at p=2 on exact-enumeration size; "not production SMC at p=2"; O_P(sqrt n) fluctuation retained | growing-p normalisation, stage-count OPEN | [IDEAL] |
| F-DRAFT Lemma W1 | A-REV6 | VERIFIED | exact sample-BO identity; "Population orthogonality is insufficient" | | [IDEAL] |
| F-DRAFT Lemma W2 | A-REV6 | ERROR plus uniformity GAP (W2-R "GAP pending Claude") | W2-R(b) ORTH additive uniform expansion, p<=n-1 | | [IDEAL] |
| F-DRAFT Prop W4 | A-REV6 | GAP; TV implication VERIFIED | TV<=max{1-pi(a),1-pi0(a)}; chi-square identity 1+chi2=pi(a)^2/[pi0(a) q2(a)] | "Advertised KL rate and sharp chi-square law remain unproved"; "WS6(e) CONJECTURE" | [IDEAL] |
| A-DRAFT section 2 A/A1 | A-REV6 | VERIFIED | Fixed-data LLN/MSE and numerator identities, "not CLT" | | [IDEAL] |
| A-DRAFT section 2 D/D1 | A-REV6 | VERIFIED conditionally | Explicit favorable premise, contraction/continuity, exact branch, output scope; equality-indicator counterexample excludes bounded-measurable generating values | "does not prove either premise for masked starts or P(output)->1" | [IDEAL] |
| W7-PART Lemma 3 (full-vector conditioning) | A-REV6 | ERROR | Conditioning on both normalized vector collections fixes cross inner products | condition on within-group Gram matrices | |
| W7-PART Theorem C | A-REV6 | GAP | needs corrected Lemma 3 | | |
| W7-PART unequal-size CE2 header | A-REV6 | ERROR | sizes 2 and 5, B=5; equal-size study example survives | | |
| W7-PART A0(c) | A-REV6 | GAP | completed roots already absorbed into full unions | | |
| W5-LOCKBOOK full-output E[1_O Zhat]<=Z P(A) | A-REV6 | ERROR | | | |
| W5-LOCKBOOK "same-size m>=m0" certificate | A-REV6 | ERROR | tie with S0 first in order | | |
| W5-LOCKBOOK T32(c) / W7 confirmation | A-REV6 | GAP | Deterministic count contains (1+4 ell); direct bound O(max(n,p) p log^3(n+p)+p^2 log^2(n+p)); polynomiality survives | | [AS-RUN] cost count |
| F-SHARE Lemma 1.2 pointwise display | A-REV6 | GAP | intermediate-state suprema and neighbour-swap factor absent from display | | |
| F-SHARE section 2 rare-outsider "sharpness" | A-REV6 | ERROR | pi0(o)=1/N leaves prob -> e^-1 of no outsider | | |
| F-SHARE section 5.2 retention inequality | A-REV6 | ERROR | At T=1, eta=1/2, 1-eta<exp(-eta) | | |
| F-SHARE F2/section 4 and O-BGIBBS LH-lock | A-REV6 | GAP | explicit population and/or Gaussian/extra-count hypotheses not discharged by M(b) | | |
| W5-B2ENV M-LH (package verdict) | A-REV6 | "VERIFIED restricted replacement" | Fixed exact-Gram lattice, nonzero fixed coefficients | "no general BM-C or extras repair conclusion" | [IDEAL] |
| O-BGIBBS BG3 (A-REV6 view) | A-REV6 (in SHARE.md) | "VERIFIED as a conditional template" | union-bound initial failure and first exits; product bound (1-beta1)^{N(L+4)} | LH-lock application "remains GAP as a sketch" | [ABSTRACT] |
| F-SHARE F1 | A-REV6 | on LOCKABLE list as "conditional first-exit/terminal-hazard templates only" | | "F-SHARE/O-BGIBBS as unconditional downstream closure: GAP" | [ABSTRACT] |
| O-WSTAB / O-DILUTE as repairs of F-DRAFT | A-REV6 | "VERIFIED cited exact identities only; GAP for the requested general sharp-rate claims" | WS3, exact tilted-normalizer identities, exact size-correction/ranking identities | "not a review of every theorem on those branches"; no all-layer threshold claim | [IDEAL] |
| Package verdicts | A-REV6 | W3-PXN: GAP; W4-SHARE: GAP with ERROR subclaims; W2-T26: "VERIFIED conditional A/B and Lemmas 1-3; GAP package"; W2-BOOK/W5-LOCKBOOK: "GAP with ERROR replacement sentences"; W7-SEC as deployed VAL-FP: GAP; F-DRAFT: "ERROR in NM/W2; GAP in W4; VERIFIED W1"; A-DRAFT section 2: "VERIFIED conditional mathematics"; W7-PART: "VERIFIED B in restricted scope; GAP package with ERROR Lemma 3/CE2 wording" | | | |

A-REV6 PARTITION.md answer to "Does W7-PART close the p>>n random-partition GAP?" (verbatim): "Only the restricted recovery premise; not the full result." Remaining: P6/P7 use "a projection-tail lemma outside its stated dimension/family range; the LS0 route has its method-change/ledger assumptions; and study groups of five can be packed together."

### 1c. A-REV7 (no-LS0 masked regime)

Headline (verbatim): "a no-LS0 masked theorem is available on an explicit exact-Gram LH subfamily. W5-B2ENV's B2-LH confinement/repair argument is VERIFIED conditional on STAB-LH ... D2-LH is also VERIFIED for qualitative consistency, for one linked pair and p/sqrt(n) tending to infinity; its stated unconditional rate is a GAP. Neither result establishes unrestricted LH or the production study's random designs, finite-n accuracy, or probability of successful completion."

| Result | Reviewer | Verdict (verbatim) | Exact scope | Open gaps | As-run vs idealised |
|---|---|---|---|---|---|
| O-BGIBBS BG3 | A-REV7 | VERIFIED | Abstract round-boundary lock and terminal scoring inequality, given EX-A/EX-S/SR | at fixed p it is only "an SMC component result" | [IDEAL] |
| O-BGIBBS LH-lock | A-REV7 | VERIFIED conditional fixed-p implication (source: PROOF SKETCH) | strict C1-C3 and block keep margins, fixed p, fixed LH parameters; Astra-authored completion | "General LH locking is false; do not remove those hypotheses" | [IDEAL] fixed-p component |
| F-SHARE F1 | A-REV7 | VERIFIED | Round-boundary closure given KEEP | "does not itself supply repair" | [ABSTRACT] |
| F-SHARE F2 | A-REV7 | GAP | | Proxy-condition coverage, cap-sensitive mass mapping, erroneous displayed ridge identity (Lemma 3.4 Schur formula off by factor n/(n+1)); "Literal c=1 exemption from DOM: ERROR" | |
| W5-B2ENV D2-LH, c=1 | A-REV7 | VERIFIED for consistency; GAP for stated rate | p/sqrt(n)->infinity, exact Gram, groups equal blocks, no LS0 (pilot scores enter HPM) | "Retain unconditional o(1), not the asserted quantitative unconditional rate" | [AS-RUN?] no LS0, potential pilot, exact arithmetic (?) |
| W5-B2ENV B2-LH | A-REV7 | VERIFIED conditional theorem (source: PROVED under STAB-LH) | uniform bounded-extra confinement; exact Gram, fixed signal units, growing p<=n-1, EX-A/EX-S/SR/CAL, output-potential convention; "small event-bookkeeping correction" (U2 event rate O(n^(-1/3))) | "Its conditional O_P rate is not automatically an unconditional numerical rate" | [AS-RUN] no LS0 on an explicit subfamily (unchanged method), exact arithmetic |
| STAB-LH analytic certificate lambda_0 b_vis^2 > R_M (Astra-authored) | A-REV7 | Astra-authored; "independently checked by a Sol reviewer ... the check agreed" (not Claude-verified) | concrete subfamily g=9,c=2,rho=.4,psi=.2, p_n=9 floor(n/18) | "General LH-iid and parameter choices violating STAB remain outside it" | [AS-RUN] |
| W7-SEP GU | A-REV7 | VERIFIED as a greedy-search theorem; GAP as a standalone no-LS0 growing-p theorem | greedy best-neighbour, not Gibbs | "actual HPM search centre need not lie in its isolated finite relevant set"; "Showing its eligibility, or adding a search from S° (LS0), is still necessary" | [IDEAL] greedy |
| W5-B2ENV M-LH vs A-REV3 | A-REV7 | exact RSS logs (not invalid quadratic) | fixed nonzero LH coefficients; "not a new BM-C-uniform claim" | | [IDEAL] |

### 1d. A-REV8 (XV-MASKED-LS0)

Overall (verbatim): "Overall verdict on the conditional consistency conclusion of Thm 5(b1): VERIFIED. It is a theorem about v3 plus LS0, under (P), (M1)-(M3), the stated execution assumptions and ideal arithmetic. It is not a theorem that the study's original sampler executes LS0, completes with probability tending to one, or works quantitatively at n = 200. The exact-Gram LH consistency instance is VERIFIED under its fixed-parameter hypotheses. The broader printed package retains the GAP and minor ERROR findings below."

| Result | Reviewer | Verdict (verbatim) | Exact scope | Open gaps | As-run vs idealised |
|---|---|---|---|---|---|
| LS-score: truth is scored | A-REV8 | VERIFIED | Feasible progress, complete last scan, emitted initial truth; no local-max premise | | [LS0] |
| LS-score "at most Phi(C0)-1 moves" without exception | A-REV8 | ERROR | E1: n=4, p=1, S0=C0={1}, ell=0; repair max{Phi-1,0}; "does not refute the scoring conclusion" | | [LS0] |
| Lemma M (uniformity, standardisation) | A-REV8 | VERIFIED | Fixed k, polynomial p, fixed positive noise variance, eigenvalue floor on preferred model | "Interpret c0 as a fixed upper envelope ... pointwise in n, not almost-sure eventual" | [IDEAL] |
| ELIG and POP-LAT => discovery | A-REV8 | VERIFIED | Deterministic reference, bounded distance/extras, completed LS0 | | [LS0] |
| Thm 5(b1) consistency conclusion | A-REV8 | VERIFIED | Conditional; joint output-and-error probability: {output and wrong} subset {pi(S0)<=1/2} union {output and truth not scored} | "does not imply P(wrong | output)->0 if output probabilities can vanish" | [LS0] |
| Prop. LH-LAT | A-REV8 | VERIFIED | Fixed exact-Gram LH parameters; m0 valid lower bound, not sharp margin | | [IDEAL] |
| Exact-Gram LH eligibility and posterior premises | A-REV8 | VERIFIED | g<=B<2g, fixed nonzero suppressors, uniform correlation bounds | | [IDEAL] |
| Exact-Gram b1-LH consistency | A-REV8 | VERIFIED | With LS0; c=1 needs only its initial scan | | [LS0] |
| b1-LH assertion c>=2, p->infinity suffices for iid-draw failure | A-REV8 | GAP | "c=2 logarithmic growth issue G1; not needed for LS0 consistency"; "not a demonstrated counterexample to actual production Q_f" | requires n^(1-c/2) p^-c log^2 n -> 0 | [IDEAL] |
| W5-VPGD W_Lat reduction | A-REV8 | VERIFIED | Reduction to cited Theorem W comparison and fixed-extra Lemma S; "no region-wide PGD claimed" | | [IDEAL] |
| W5-VPGD LH-PGD lower bound | A-REV8 | VERIFIED | All nontruth lattice states incl. Phi=1 | "sharpness remains a numerical claim" | [IDEAL] |
| W3-PXN P6 after W5-VMASK | A-REV8 | GAP | R2 repairs constant; general-dimensional uniformity remains | | |
| W3-PXN P7 after R1/R3/R6 | A-REV8 | GAP | peeling and rate substantially repaired; P7 prints (n-3-s)/2 vs (n-2-s)/2; "original sketch is not upgraded" | | |
| W6 formulation vs A-REV1 section 7 | A-REV8 | VERIFIED | strict output, potential execution, rate/delivery interfaces, emitted centre, +1 cost | | |
| Literal GUARD claim "every reported output equals the guard-free output" | A-REV8 | ERROR | E2: RuntimeGuard::check appends a GuardRecord even when not stopping; statistical-output transfer survives | | [AS-RUN] |
| O-LS0 zero-change summary | A-REV8 | VERIFIED | "as a reading of saved aggregate records, not a new replay or bitwise identity certificate": 2,400 matched records, 2,394 completed production fits, 1,829 production-exact, zero HPM changes; six resource-stopped fits excluded | | [LS0] empirical |
| Identifying O-LS0 empirical checks with asymptotic M1-M3 | A-REV8 | GAP | finite-sample D_S not POP-LAT; positive eigenvalue at one n not a uniform floor; "M1 holds 18/2400" uses observed mode mass | | |

### 1e. A-REV9 (certificates, masked outputs, evidence variance, dilution, stages, separation)

Final register (A-REV9 verbatim, "Source statuses ... remain unchanged"). No simulation executed; "Historical numerical claims were not independently reproduced."

| Result (source task) | Reviewer | Verdict (verbatim) | Exact scope | Open gaps | As-run vs idealised |
|---|---|---|---|---|---|
| O-CERT Lemma M | A-REV9 | VERIFIED, exact arithmetic | push-through identity; BB ratio (k+1)/(2p-1-k)<=1 | | [IDEAL] |
| O-CERT C1(a) | A-REV9 | ERROR in self-inclusive gap inequality; deterministic normalizer bound VERIFIED | includes S=HPM in claimed ratio <=exp(-g) | exclude HPM | |
| O-CERT C1(b), R1 | A-REV9 | VERIFIED repaired outside-store implication, conditional on frozen-run unbiasedness and statistical-output coupling; original unscored wording ERROR | | "O-VCERT's optional unscored bound also requires a genuine upper bound on the entire logical scored set" | [IDEAL] frozen run |
| O-CERT C1(c) | A-REV9 | VERIFIED non-implication from first moments | | | |
| O-CERT C2 | A-REV9 | VERIFIED conditional PW2/Cantelli implication | B_T/(B_T+4 eps^2); independent islands, frozen calibration | "does not establish PW2 or completion probability" | [IDEAL] |
| O-CERT C3 | A-REV9 | VERIFIED exact ratios; GAP identifying local returned centre with HPM without identity/tie check | | returned==HPM check under ties | [AS-RUN] code: local_search marks A.returned certified; ledger HPM may update on equal-score neighbour |
| O-CERT C4 | A-REV9 | VERIFIED exact boxes; GAP in claimed FP certification from SC alone | | interval bounds for each ingredient of Phi(L,U) | [IDEAL]; fp is GAP |
| O-CERT C5 | A-REV9 | ERROR tie-insensitive prose; VERIFIED displayed strict-score event inclusion | duplicate columns counterexample | | |
| O-CERT C6 | A-REV9 | GAP original card; repaired exact implication requires conditions | needs R1, FP inflation R2, region certificate validation | "conditional validation contract, not a measured production guarantee" | |
| F-MASKPIP M1(a-c) | A-REV9 | VERIFIED under locked exact frozen-run assumptions | exact frozen SMC component, successful calibration, START, EX-A, EX-S, CAL, independent particle mutations | not floating-point, not calibration success, not completion, not exact-enumeration branch | [IDEAL] |
| F-MASKPIP M2(a-e) | A-REV9 | VERIFIED intersection bounds, not completion-conditioned guarantees | | "PIPs can be wrong only on low-evidence islands" must retain exceptional probability | [IDEAL] |
| F-MASKPIP M3 | A-REV9 | ERROR probability-one counterexample; conditional means VERIFIED for 0<kappa<1 | kappa=1/2, delta=1/10 forces E(W|C)>=1.6 | | [ABSTRACT] |
| F-MASKPIP N-a | A-REV9 | GAP literal finite-index/rate wording; VERIFIED finite-index inequality with actual non-crossing probability | | T03 only gives O_P rate; unit-constant (n/log n)^(1/4) claim unsupported | |
| F-MASKPIP N-b/N-c, Theorem R | A-REV9 (MASKED_PW2_CHECK) | not reviewed ("no approval of F-MASKPIP N-b/N-c or Theorem R") | | | |
| O-PW2 A1-A4 | A-REV9 | VERIFIED | Fact F: fresh orders per particle (methodology) | shared random mutation orders would invalidate | [IDEAL] |
| O-PW2 B1-B3 | A-REV9 | VERIFIED, asymptotic O(N^-3/2) only for fixed inputs/grid or uniform constants | fixed finite input, frozen grid/T/kernels as N grows | "They are not uniform claims along the actual growing n,p,T budgets"; "does not establish study-scale precision"; locked T25(iv) obligation remains | [IDEAL] |
| O-PW2 Theorem C | A-REV9 | not reviewed ("beyond reading it for context") | | | |
| O-DILUTE E | A-REV9 | VERIFIED with feasibility/cap retained | | | [IDEAL] |
| O-DILUTE E1, three-term identity | A-REV9 | VERIFIED for production BF tables; GAP arbitrary-positive-table scope without normalization | needs r_b(empty)=1 | | |
| O-DILUTE E2 | A-REV9 | VERIFIED supporting-line bound with interior-size/end-point conventions | | | |
| O-DILUTE R | A-REV9 | VERIFIED, integer d>=0 and feasible supports | | does not imply small Hamming distance | |
| O-DILUTE N | A-REV9 | VERIFIED under explicit joint independence; ERROR parenthetical implication from zero truth correlation | two correlated Gaussian nulls counterexample | selected-partition conditioning separate | |
| O-DILUTE N1 | A-REV9 | ERROR in pointwise expectation bound (LOCKABLE excludes it) | multi-variable block: expected count (t r1+t r2+2t^2 r12)/(1+...); orthogonal columns x in (0,1/2), r12/r1^2=[(1-x)^2/(1-2x)]^nu | "iid-like heavy-tail rate remains GAP" | |
| O-DILUTE S | A-REV9 | GAP: replacement assignments are not injective | two truths, three null blocks: 12 counted vs 10 distinct supports | "Do not retain the product denominator without a new proof"; weaker ceiling pi0(S0)<=1/(1+max_j M_j) | |
| O-DILUTE DM(i), size sign | A-REV9 | ERROR | p=2,K=s0=1: P_t(N<=K)=3/4, A=4/5, log(5/4)<log(4/3) | o(1) ceiling needs P_t(N<=K)->1 | |
| W7-SEP SEP(A), SEP(B1-B3) | A-REV9 | VERIFIED as implications from its imported tight start-mass and posterior-concentration premises | | "do not independently discharge the LH statistical premises or prove a PIP statement" | [IDEAL] |
| W7-SEP GU | A-REV9 | GAP in this review | descent and superset argument checked; imported uniform score-comparison Lemma M not independently audited here | | |
| W7-PART A1-A4 | A-REV9 | VERIFIED deterministic no-tie statements, with A2's extra premise | | | |
| W7-PART B-exact | A-REV9 | VERIFIED Gaussian pair-law/union-bound statement | | | |
| W7-PART B-explicit, L2 density constants | A-REV9 | GAP in this review | "classical density normalization not independently established; do not lock the explicit constants" | | |
| O-STAGES M | A-REV9 | GAP explicit decimal constants; VERIFIED logarithmic order for ideal two-state exact-frontier grid | lower constant ~ -0.955 not -0.95; uniform A1>=2.2 | "General-family transfer requires PAIR on [0,2]; actual-grid transfer requires pilot/candidate/bisection control" | [IDEAL] two-state, exact frontier; not 60-step bisection |
| O-WSTAB W(a)-W(f) | A-REV9 | VERIFIED under H-ORTH exactly as stated, including W(d)'s stronger upper-side premise | H-ORTH, fixed nonzero signals, bounded blocks, p->infinity, p log p=o(n) | W(g) not included | [IDEAL] |
| O-WSTAB W prime | A-REV9 | VERIFIED ideal full-space grid under H-ORTH; production-grid transfer remains GAP | at most two ideal steps; equality 2Ar=1 unresolved | "neither general correlated-block BO nor the empirical pilot/candidate grid" | [IDEAL] |
| O-SWAP predicted rates | A-REV9 | GAP | PA alone does not give displayed add law; "the displayed event identity is ERROR if asserted under PA alone" (replaces W_S0 by expectation) | data reproduction/provenance audit not done | |
| W7-SEC T05, T33, T32(i) | A-REV9 | GAP in this review (deferred; "no mathematical rejection asserted") | | "I do not endorse 'numerical_failure impossible for every p,y' without its stated FP/NOUF/LIB/SMALL domain" | [AS-RUN] fp |

A-REV9 sub-checks (DILUTE_STAGES_CHECK, MASKED_PW2_CHECK) are analytic helper reports; Astra states "the verdicts here are mine". They reach the same verdicts as the register above. DILUTE_STAGES_CHECK on O-STAGES: finite-precision 60-step bisection and the empirical pilot are not shown to return the exact frontier.

## 2. Explicit refutations and "false as stated" findings (quoted)

A-REV5:
- Lemma U C3 lower: "ERROR ... take orthogonal signal x1 omitted by T=empty and add null x2. RSS doubles, giving limiting improvement Z^2/4 instead of Z^2/2" (REV2_CHECK; A-REV5 "old zero-leakage matching floor stays ERROR").
- Lemma U/EXP' constant: ".52/c is only an eventual ceiling"; correct constant .51/c; "PXN's separate <=1 bound is false".
- U(F,H) arrow: "Printed `1-o(1) ->0` is false; should be ->1."
- F-REFINE Card 3(i): "With n=20, p=2, centered orthogonal columns of norm sqrt(19), y=x2, singleton blocks, and reference {1}, the actual capped normalized mass is 9.441607620478e-14, whereas the printed expression is 1.983334052945e23."
- F-REFINE Card 4: "CEX-1 (n=100, p=12, corr(x1,x2)=.95, mu=3x1-2.8x2, orthogonal noise of squared norm 99) starts at empty below truth, has every singleton gain negative, and certifies empty: F_post<F(truth) and E_LS holds. This is omitted category IIa." (A-REV5 says it did not rerun this matrix experiment.)
- PXN P7 range: "77 weights of 1 and 40 of 1.925 have ESS/H<.9"; r* = 1.924950591148529.
- PXN U1: "cannot hold: c_*<=1/16 gives limiting value >=8.16, and M=sigma^2=phi^2=1 gives 12.24."
- T38-S (b1-LH): "claims Q_f pi0(S0)->0 for c>=2 and merely p->infinity ... Q_f pi0(S0) is bounded below by a constant times (log n)/p^2 times exp(O_P(1)), which diverges in probability" (c=2, p ~ log log n, group size 9).
- T03 replacement onset sentence: "At n=2,116,048 the independent calculation gives q=.499999989 but exp(2 epsilon)=4639.924697>4."
- Cap-free lattice / count: "n=8, p=7, K=4, centered orthogonal G=7I, S0={1,2,3,4}, y=(x1+x2+x3+x4)/2, a=d=1 ... TD-P holds throughout the region. Yet Lat({1,2,3,5}) contains infeasible {1,2,3,4,5}. This also directly refutes the conditional A2 subset claim." Independently also n=4, K=s0=2.
- W2-T26 P1-ex: "fails at p=18, n=262144. K=p, feasible count=262144, whereas the exact-branch threshold is 23706288. The code therefore enumerates."
- Proposition U shorthand, A5 without POS, TD'_P iff strict D_S, "weakest among at-most-Phi-move conditions", Lemma 0(b), V37 R2 dichotomy, growing-leakage iff, V37 R4 Gaussian tail: all original ERRORs, repaired (see table).

A-REV6:
- M(b): "Orthogonal centered p=n-1, theta=1, sigma^2=1 gives exact gain/n -> log(2)/2 but quadratic term/n -> 1/4." With theta^2=C log n/n "the crossing ratio tends to 3/C, not zero."
- Coefficient-one exit: "one-way a-to-o mutation with retention 1/2 per round ... sum eta = T/2 ~ 0.8 log N satisfies the printed criterion ... yet E n_T(a) = N 2^{-T} -> 0, so extinction tends to one."
- SH sharp-transition: "With pi0(o)=1/N, probability of no initial outsider tends to exp(-1), so extinction cannot tend to one at any fitness advantage."
- F-SHARE section 5.2 retention: "At T=1, eta=1/2, 1-eta<exp(-eta), opposite to printed lower bound."
- W7-PART Lemma 3: "Conditioning on both normalized vector collections fixes their cross inner products; a nondegenerate Haar law cannot remain."
- W7-PART CE2 unequal-size: "Groups of sizes 2 and 5, B=5: 2g_min<=B but next-fit cannot merge the groups."
- W5-LOCKBOOK: "Completed exact branch with A defined SMC-only: Z>0 on left, zero right."
- W5-LOCKBOOK/BOOK same-size m>=m0 certificate: "Tie with S0 first in prescribed order."
- W2-T26 exact-branch: "p=18, n=2^18 selects exact enumeration under actual criterion."
- Neutral ESS-only: "Neutral two-state identity mutation with repeated multinomial resampling has perfect ESS and eventually loses a class at fixed N."

A-REV7:
- LH swap locking: "One pair, g=4, rho=.85, psi=.5, beta_a=1.4, beta_b=-.7 ... Delta(V)=.3675, Delta(W)=.3627106863596872. Thus the swap 0<->4 improves the population fit by .004789313640313 ... explicit counterexample to C2 for general LH and to an exponentially small single-step exit bound. It refutes the purported universal two-endpoint locking mechanism. It is not, by itself, a counterexample to an end-of-round bound ... No exact round-end lower bound or failure of the overall algorithm is claimed here." Also reproduced for g=9 (rho=.85, psi=.5, beta_a=1.4).
- "DOM is void when c=1" with visible groups: "one pair, g=4, rho=.4, psi=.2, beta_a=1, and a separate visible hub h=8 with beta_h=.01. From S°={a,h}, swap h->b ... residuals .0384 before and .0001 after." F2's c=1 exemption false with visible groups.
- F2 Lemma 3.4: "n=10, U empty, x_j'x_j=9 and x_j'y=1, the actual increment is .1; the printed expression gives 1.1."
- "General LH locking is false."

A-REV8:
- E1: "n=4, p=1 ... zero is not at most -1" (move-count sentence).
- E2: "RuntimeGuard::check appends a GuardRecord even when elapsed+operation is below allocation; guard-free execution does not append that record."
- G1: c=2 growth gap (not a demonstrated counterexample).

A-REV9:
- C1(a): "take any two scored models with strict gap g>0 and set S=HPM. The displayed inequality becomes 1<=exp(-g)."
- R1 original: "Unscored mass is zero, whereas 1-Z_T/(alpha Z)>0."
- C5 duplicate predictors: tie order lets unscored truth win, so weak score inequality does not exclude a miss.
- M3: "kappa=1/2, delta=1/10 forces E(W|C)>=1.6; W<c<1 almost surely on C is impossible."
- DM(i): "p=2, K=s0=1, singleton table BFs=1, t=1 gives P_t(N<=K)=3/4, A=4/5, and log(5/4)<log(4/3)."
- N parenthetical: "Two correlated Gaussian nulls, both independent of truths and response, refute the parenthetical implication that zero truth correlations imply independence of (y, X_-l)."
- N1: orthogonal columns example above.
- S: "claims at least (1+3)(1+2)=12 distinct supports; only 1+6+3=10 distinct replacement supports exist."
- O-SWAP: "the displayed event identity is ERROR if asserted under PA alone."
- STAGES decimal: "approximately -0.955, ... not the rounded stronger -0.95."

## 3. Reviewer statements about novelty or literature

None found. I grepped all fifteen files for "novel", "literature", "prior art", "published", "textbook", "classical", "well-known", "standard result". The only hits are:
- A-REV9 (and A-REV6 PARTITION): "classical density normalization not independently established" / "The exact density remains a cited mathematical input" (the sample-correlation / Hotelling-type density used by W7-PART B-explicit and L2). This is a dependency flag, not a novelty claim.
- A-REV6 BOOK: "libm assumptions and cited Cholesky success constants are admitted escalation items" (W7 T33-Z).
- A-REV5: "T38 citation ... Locked T21(C1), not nonexistent T11(vii)" (internal-register citation error).
No reviewer comments on whether any result is new relative to the published SMC/BVS/Bayesian variable-selection literature. Novelty is therefore unassessed by these reviews. (The task LIT-PAR and Song-Liang 2015 inputs are outside this digest.)

## 4. Disagreements (between reviewers, or with Claude-side reports), quoted

Between Astra reviews:
1. A-REV9 vs A-REV6/A-REV7 existence. A-REV9: "A-REV6 at ee3f3c68... and A-REV7 at 2d672a08... have no files under their respective review directories (checked with git ls-tree) and no REVIEW.md. Neither supplies a completed review to import." But A-REV6 and A-REV7 REVIEW.md do exist on `origin/theory/A-REV6` and `A-REV7` at the heads I read. Likely A-REV9 inspected earlier commits (?). Consequence: A-REV9 assigned no coverage credit for A-REV6/7 items, so A-REV9 re-reviewed some overlapping items (W7-PART, W7-SEP GU, O-WSTAB/O-DILUTE) independently.
2. W7-SEP GU: A-REV7 "VERIFIED as a greedy-search theorem" (with GAP as standalone); A-REV9 "GAP in this review: ... imported uniform score-comparison Lemma M not independently audited here". Difference of scope, not contradiction (A-REV9 is an incomplete audit, not a rejection).
3. W7-PART Theorem B: A-REV6 "VERIFIED on SIZE and fixed correlation separation" with explicit bound; A-REV9 "B-exact VERIFIED" but "B-explicit, L2 density constants GAP ... do not lock the explicit constants on this review". A-REV6 itself notes the density is a cited input.
4. c=2 iid-budget claim: A-REV5 labels it "ERROR" with an analytic counterexample (p ~ log log n); A-REV8 labels it "GAP" and says "not a demonstrated counterexample to actual production Q_f (which may be much smaller or may not exist on the exact branch)". A-REV5 also says the slow-p sequence "eventually enumerates ... that is an additional branch-qualification GAP". They agree on the sufficient fix n^(1-c/2) p^-c log^2 n -> 0.
5. O-BGIBBS LH-lock: A-REV6 "GAP" (F2/section 4 and LH-lock hypotheses not discharged by M(b)); A-REV7 "VERIFIED conditional fixed-p implication" via an Astra-authored completion, together with "General LH locking is false". Not a contradiction: A-REV7 supplies the missing implication under strict gaps.
6. W2-T26 exact-branch parenthesis: A-REV5 "ERROR"; A-REV6 table "GAP pending Claude" for its own R2 repair while BOOK.md says "ERROR remains; use actual combinatorial branch criterion" (?) label inconsistency within A-REV6.
7. A-REV5 REV2_CHECK vs A-REV2: A-REV2 table shorthand "initial centre already is truth is trivial success" is ERROR (A-REV5: "VERIFIED disagreement").
8. A-REV6 on A-REV5's T26 treatment: A-REV5 says T26 "Theorem A retains P1-ex as a premise and survives"; A-REV6 agrees ("VERIFIED conditional A/B").

With Claude-side reports (quoted):
- A-REV5 vs W6-FIXREV2 REPORT: "Card 1 already has sup_m P, contrary to R2 REPORT."
- A-REV5 vs W6-FIXREV1 downstream table: "R1's downstream table missed this CARDS occurrence."
- A-REV5: "PXN still prints 1.925: source text is not synchronized" (W6 correction not propagated).
- A-REV5 vs W6-FIXREV2 STATEMENTS: three new errors (U(F,H) arrow, T03 replacement onset sentence, cap-free lattice/count).
- A-REV5: "W6's report says candidate, not adopted, and not reviewed after its edits" (REV1_CHECK) -- consistent.
- A-REV5/F-REFINE: "F-REFINE's graph also compresses H24 to [X] and section 4 says 'H24's asymptotic input false'. The precise repaired claim is the failure of the vanishing uniform-exit premise on the explicit CE1-narrow sequence. The locked register still lists H24 as not proved ... not as a universally disproved premise. W6's narrow wording is preferable."
- A-REV6 vs W5-LOCKBOOK: "ERROR in W5 full-output expectation"; "ERROR in paraphrase" (same-size m>=m0 as unrepairable).
- A-REV6 vs W7-PART: "W7's statement that the partition depends only on X does not make its selected blocks independent of X or of y=X theta+epsilon"; "Do not reuse their Beta law after conditioning on successful recovery."
- A-REV6 vs W5-VMASK: W5 reports Lambda and P6 VERIFIED without recording the Tr(c) dimension mismatch ("Preserve A-REV3's original GAP"); A-REV6 and A-REV8 agree P6/P7 remain GAP.
- A-REV7 vs HQ SR_AUDIT.md: "Its blanket wording that no call passes emit=false is too strong: v3_core.cpp:447,610,657 pass false through local_search ... These centres are already-scored ledger HPMs, so the exception does not invalidate the scoring arguments."
- A-REV7 vs W5-B2ENV: B2-LH VERIFIED but "Correct the minor RSS event-rate statement"; D2-LH stated unconditional rate "GAP".
- A-REV8 vs older synthesis: "O-LS0's now-landed report ... the older synthesis says the report was missing and is stale on that point."
- A-REV8 vs O-LS0: "Identifying O-LS0 empirical checks with all asymptotic M1-M3 premises: GAP"; "Matching F(S0) alone is not a uniform perturbation bound."
- A-REV8 vs W6: GUARD literal claim "ERROR"; statistical-output transfer survives.
- A-REV9 vs O-CERT, F-MASKPIP, O-DILUTE, O-SWAP authors: multiple ERRORs listed in section 1e/2.
- A-REV6: "Historical branches and registry files were not edited. Source hashes identify bytes, not mathematical validation."

## 5. Reviewer-noted properties of the method with no guarantee

Collected statements of what is not guaranteed (quoted where possible):
- Completion / output probability: A-REV5 "No vanishing failure probability is inferred" (T38 interface); GUARD "supplies no probability bound for guards, numerical failures or calibration failure". A-REV7: "Neither result establishes ... probability of successful completion." A-REV8: "not a theorem that the study's original sampler ... completes with probability tending to one"; "It does not imply P(wrong | output)->0 if output probabilities can vanish". A-REV6: A-DRAFT D "does not prove either premise for masked starts or P(output)->1"; "removes the no-output event U" not proved.
- Original sampler does not execute LS0: A-REV8 (Thm 5(b1) is for v3 plus LS0); A-REV5 "LS0 remains a method extension"; "production callers' already-scored centres do not implement that extension automatically". A-REV7: "GU alone" needs eligibility of the actual search centre or LS0.
- Delivery (a near-truth centre reaches the local search): A-REV5 "Genuine delivery premise remains OPEN" (DELIV); "No unconditional masked production theorem is locked." A-REV6: "Keep four implications separate: reference start concentration, eligibility of its exact mode, scoring truth by an authorized repair route, and reporting truth when the posterior favours it."
- Unrestricted LH: A-REV7 "General LH locking is false"; the swap counterexample; "The minimal gap for unrestricted LH is control of profitable swaps out of the visible-superset class". The no-LS0 masked result holds only on an explicit exact-Gram LH subfamily satisfying STAB-LH.
- Correlated designs generally: CE1-narrow shows failure of the vanishing-uniform-exit premise on one explicit family; "not universal failure"; H24 not proved.
- p >> n / adaptive packing: A-REV6 "No repair here gives a statistical law for arbitrary adaptively packed study blocks"; study groups of five can be packed together; P6/P7 GAP; A-REV5/A-REV6 "B>=2g packing remains unproved". A-REV8: "A-REV3's p>>n GAP is retained."
- Random designs: A-REV5 random-design EXP'/packing GAP; ".15 universal covariance floor is false for .9 equicorrelation (minimum .1)" (REV2_CHECK).
- Finite n: A-REV8 "does not work quantitatively at n = 200" claim not made; "These few finite-n tests support the algebra, not an asymptotic proof". A-REV5: T03-sharp "not a universal finite-n guarantee"; no finite-n universal onset. A-REV9: "constants can be huge along growing n,p,T; this review does not establish study-scale precision" (PW2); W7 T33-Z "vacuous useful epsilon at the study budgets".
- Floating point / numerics: no floating-point theorem in any review; "interval-certified deployment" GAP (A-REV6); VAL-FP operational GAP; C4 FP certification needs interval bounds per ingredient (A-REV9).
- Fixed p: production eventually takes exact enumeration, so SMC component results at fixed p are not asymptotic SMC results (A-REV7, A-REV8); "The exact-branch state count grows exponentially with p, so the asymptotic algorithm uses SMC" only on the growing-p subfamily with p_n = 9 floor(n/18).
- Growing-budget evidence/PIP precision: A-REV9: PW2 O(N^-3/2) only for fixed inputs; "the finite-state identities alone do not remove the substantive study-scale PW2 obligation in locked T25(iv)"; masked PIP results are intersection bounds, "not statements conditional on observing a high evidence estimate".
- Tie handling: duplicate columns/equal-score models make several posterior-miss and certificate claims tie-sensitive (A-REV5 Lemma T, A-REV6 BOOK, A-REV9 C5, C3/C6 returned vs HPM identity).
- Operational diagnostics: A-REV8 E2: GuardRecord diagnostics differ between guard and guard-free runs; only statistical outputs transfer. A-REV6: "no returned partial value" is false; partial HPM is returned (partial official estimate is not).
- Benchmark classification: A-REV5 "no such extraction was supplied, so section 0/541 forced by monotonicity remains GAP": the per-fit hpm_before_local and truth scores are not yet extracted; the proposed classification of study misses is unverified.
- Mixed-regime: A-REV7 "B2-LH ... conditional O_P rate is not automatically an unconditional numerical rate."

## 6. Numerical/audit evidence (what was actually computed by the reviewers)

- A-REV5: owls scalar and threshold checks (exit 0), cap-witness enumeration of 17 feasible states; deterministic, point/boundary checks, "not a proof that no earlier nonmonotone crossing exists". Did not rerun the CEX-1 matrix experiment.
- A-REV6: no numerical workloads; historical saved outputs not reproductions.
- A-REV7: `reproduce.py` on owls (four noise replicates at n=400, 1600, 6400; BG3 popcheck c=2, p=16, g=4: C1=.217969, C2=.030469, C3=.085793); "No claim is made that four Gaussian replicates estimate an asymptotic probability."
- A-REV8: 40 heterogeneous population cases (zero LH-LAT violations; g=2, p=12 algebra test) and six exact-Gram score experiments (p=108, g=9, c=2, rho=.7, psi=.5, n=200 or 800; LS0 scores truth in all six with two moves); independent Python implementation, "not an invocation of the compiled production engine"; no C++ partition replay or p>>n experiment.
- A-REV9: no experiments.

## 7. LOCKABLE recommendations (as stated by reviewers; not status changes)

- A-REV5 (8 items): finite Theorem B (F', CON section 2) + corrected U' + multi-target P; S', finite D2 with r*/NB', D2-infinity with rate margins; E3' (q<1, centre emission, completed scans); T03-sharp core + exact-tail lemmas (not the onset gloss); Lemma T, POS-repaired A5, Lemma 0(b'), Prop F, Lemma NT (not the cap-free lattice/count); fixed-design EXP' (.51) and deterministic-chain Thms 3/4 with H3; Lemma U budget argument and C3-up / signal-contained C3-low / weak C3-low' (not the printed whole); T38 isolated conditional composition and b1'/b2 interfaces (not the whole T38 statement).
- A-REV6 (10 items): W4-SHARE D4/D5, SH(i)/(ii), G identity, M(a), B2-W4; W3-PXN P1-P5, P8 (original ranges); W2-T26 Theorem A/B and Lemmas 1-3 (retain P1-ex); W2-BOOK fixed-data island identity + qualified output Markov implication; F-DRAFT W1 and TV implication; A-DRAFT section 2 A/A1/D/D1; W5-B2ENV M-LH; W7-PART Theorem B on SIZE; F-SHARE F1 and O-BGIBBS BG3 as templates; O-WSTAB / O-DILUTE exact identities. All Astra-authored candidates excluded until Claude verifies.
- A-REV7: B2-LH with STAB-LH (analytic certificate) as "the no-LS0 masked theorem"; BG3 as fixed-p component lemma; F1 as abstract closure lemma. "Do not cite F2 or GU alone as an unrestricted growing-p no-LS0 guarantee."
- A-REV8: "Retain Thm 5(b1) as a conditional candidate for v3 + LS0 with a concrete, jointly justified exact-Gram LH instance"; no locking language.
- A-REV9: O-CERT Lemma M, deterministic normalizer inequality, C1(c), C1(b) as R1, C2, C3 ratios, C4 inequalities, C5 strict event; F-MASKPIP M1-M2, M3 conditional means 0<kappa<1, N-a corrected; O-PW2 A1-A4, B1-B3; O-DILUTE E, R, E1 (normalized), E2, N (literal joint independence); W7-SEP A/B; W7-PART A, B-exact; O-STAGES ideal two-state log order; O-WSTAB W(a-f), W prime (H-ORTH, ideal grid).
