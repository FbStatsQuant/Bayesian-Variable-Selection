"""Render progressively maintained review rows; does not change any other directory."""
from pathlib import Path
from collections import Counter
import json

HERE=Path(__file__).resolve().parent
GROUPS=[]
def group(title):
    GROUPS.append((title,[]))
def row(card,claim,truth,design,route,repair,flags,evidence):
    GROUPS[-1][1].append([card,claim,truth,design,route,repair,flags,evidence])

group('Seat A · item 1 · §R3 / main M3, WS-ε')
row('A.R3(a)', 'Discrepancy and divergences include explicit shared-variance and cross-block terms.',
    'TRUE-AS-WRITTEN: reuse CHK §§3–4 and W1 finite-law calculus.',
    'DESIGN-VERIFIED: revised p=16 groups and C’s asymptotic family.', 'PLAUSIBLE',
    'REPAIRED: nondegeneracy wording; actual-partition exhibit replaced.', 'S-WS; EX-A',
    'CHK §§3–4; W1-PC1 §16; reproduction A; E-partition.')
row('A.R3(b)(i),(ii),(v)', 'Transfer 1+χ², normalized first-stage variance, and Doeblin constants.',
    'TRUE-AS-WRITTEN: four-normalizer comparison; inherited first-stage identity.',
    'DESIGN-VERIFIED: A’s 9 cases, ε>0.', 'PLAUSIBLE',
    'REPAIRED: transfer 1+N_e Var, not Var; common comparison start.', 'S-WS; V≠Ω needs coverage',
    'CHK §4; W1-PC1 §4; reproduction A has zero transfer violations.')
row('A.R3(b)(iii) · sandwich', 'Common-target greedy counts lie between tightened and relaxed baseline counts.',
    'TRUE-AS-WRITTEN for exact frontiers; coded resolution caveat must include snap/validation.',
    'DESIGN-VERIFIED: E-pilot has 16 applicable cases, zero violations.', 'PLAUSIBLE',
    'REPAIRED: threshold order, common V/targets, upper threshold below one.', 'c: fixed V/targets; d: exact-frontier comparison',
    'E-pilot; W1-PC1 §4. The quoted A script uses target {1}, not retained pilot targets.')
row('A.R3(b)(iii) · zero range', 'A uniform full-space grid uses ceil(range bound / constant) stages.',
    'COUNTEREXAMPLE: BO, z=0 gives range=0 and claimed zero stages.',
    'DESIGN-VERIFIED: n=8,p=2,G=7I; nonconstant centered y orthogonal to X.', 'PLAUSIBLE: use max{1,ceil(…)}.',
    'REPAIRED: W=Ω. New zero-range omission remains.', 'new boundary error',
    'E-zero; a bridge from 0 to 1 requires at least one interval.')
row('A.R3(b)(iv) / guarantee', 'Actual-island second moments and all bridge quantities transfer continuously from BO.',
    'NEEDS-HYPOTHESIS: the M₂ upper bound is valid; it is not an e^{cη} comparison to actual BO M₂.',
    'DESIGN-VERIFIED: C’s filed actual-grid exhibit; finite correlated A exhibit.', 'GAP: retain upper envelope; qualify integer-count continuity away from jumps.',
    'REPAIRED DIFFERENTLY: actual-grid upper bound replaces missing moment route.', 'S-C; c: threshold margin needed for local constant counts',
    'W1-PC2 D14 actual-grid moment; E-jump refutes unconditional count continuity.')
row('A.R3(c)', 'Zero-dependence and masked one-shot refutations ship with inherited amendments.',
    'TRUE-AS-WRITTEN: cite CHK §§1,2,6; no re-proof.',
    'DESIGN-VERIFIED: CHK p=n−1, β=2, σ²=1, bounded blocks.', 'PLAUSIBLE',
    'REPAIRED: bounded-block TV; initial/later support distinction; set-mass/endpoint qualifications.',
    'S-WS; c: masking mass conclusions need LH model/design instantiation',
    'CHK §§1–2; ε=0 is allowed for HQ(c); LH verified in W1-PC2.')
row('A.R3 · N-d', 'Fixed-ε discrepancy has the displayed multiplicative first-order asymptotic lower bound.',
    'COUNTEREXAMPLE: ε=.1, β=(.8,.6), σ²=1; actual/claimed limit=.856466.',
    'DESIGN-VERIFIED: p=2, B=1, two truth blocks; ε<1−x̄.', 'GAP: require ε→0 and controlled signal/noise; keep higher-order terms.',
    'New clause; not inherited.', 'fixed-ε Taylor error',
    'E-A-NEC: sup|d_X|/n→.05602475; claimed lower bound/n→.06541387.')
row('A.R3 · scale / growth exhibit', 'Shrinking cross-correlation makes A’s fixed-signal exhibit suitable for bounded oscillation.',
    'NEEDS-HYPOTHESIS: also control the σ² term, e.g. shrinking signal energy.',
    'DESIGN-FAILS for this claimed asymptotic example; C’s family remains valid.', 'PLAUSIBLE after using C’s family.',
    'REPAIRED: “iff” removed; new bounded-oscillation example still fails.', 'νa² need not be bounded when η is bounded',
    'E-growth: ε_n=n^−2, d(S₀)/n→about .0545. Raw-correlation scale also carries K/κ.')
row('A.R3 · IC3 / scripts', 'The method’s own size cut and packing return four groups of four.',
    'TRUE-AS-WRITTEN: source script rerun and independent method-partition check.',
    'DESIGN-VERIFIED: n=64,p=16,B=4; ε=10^−4,10^−3,10^−2.', 'PLAUSIBLE',
    'REPAIRED: old p=8 four-variable-group exhibit replaced.', 'd: component example; production dispatches exact',
    'Reproduction A: all 9 partition/bound cases pass; sandwich applies only at 10^−4. C family eventually dispatches SMC.')

group('Seat B · item 1 · §R3 / main M3, WS')
row('B.R3(a)', 'D_* and η bounds control divergence with the explicit σ²-coupling term.',
    'TRUE-AS-WRITTEN: cite W1-PC2 D14 and CHK §§3–4.',
    'DESIGN-VERIFIED: 40/40 rebuilt-pair cases, ε>0; C family eventually.', 'PLAUSIBLE',
    'REPAIRED: no claim that favourable start alone controls q₂.', 'S-C; S-WS',
    'Reproduction B1: D_* .068–5.020, osc/D_* .066–.701; all hypotheses hold.')
row('B.R3(b)(1)–(4)', 'Perturbation compares stage divergences, normalized variance, stage counts, and minorization.',
    'TRUE-AS-WRITTEN: inherited inequalities plus corrected exact-frontier count order.',
    'DESIGN-VERIFIED: Dε and E-pilot.', 'PLAUSIBLE',
    'REPAIRED: variance offset; order; same V/targets; upper threshold below one.',
    'c: fixed targets; d: normalize the stage-1 evidence variance',
    'CHK §4; W1-PC1 §4; E-pilot has 16 applicable comparisons, zero violations.')
row('B.R3(b) · continuity sentence', 'Every constant in (b1)–(b5), including stage count, tends to its BO value.',
    'NEEDS-HYPOTHESIS: integer counts require a noncritical threshold; numerical snap needs its own qualification.',
    'DESIGN-VERIFIED: E-jump is actual BVS with ε>0.', 'PLAUSIBLE for continuous envelopes and locally constant noncritical counts.',
    'REPAIRED: old comparison hypotheses; new continuity overstatement remains.',
    'c: margin at baseline decision boundaries',
    'E-jump: exact-frontier T(0)=2, small positive perturbations give T=3; envelope constants still converge.')
row('B.R3(b)(5),(6)', 'Pathwise moments and nonperturbative leakage bounds replace a uniform q₂-tail lemma.',
    'TRUE-AS-WRITTEN: cite filed actual-grid and leakage checks; m≥π₀(S₀)e^{−2 osc d} follows pointwise.',
    'DESIGN-VERIFIED: W1 D_B and C family; informative constants require their stated scale.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: false (N) withdrawn; q₂ route withdrawn; data-dependent m bound retained.',
    'S-C; WS53F remains PROVED-UNDER, not independently proof-verified',
    'W1-PC1 §4 (F),(S); W1-PC2 D14. The m bound may be tiny; no uniform efficiency conclusion.')
row('B.R3(c)', 'One-shot refutation includes bounded-block TV and qualified masked support/stage conclusions.',
    'TRUE-AS-WRITTEN: use inherited cross-family check.',
    'DESIGN-VERIFIED: CHK explicit orthogonal example and W1 LH family.', 'PLAUSIBLE',
    'REPAIRED: inherited amendments explicitly adopted.', 'S-WS; c: mass premises distinguished from model conditions',
    'CHK §§1,2,6. The optional assumption π₀(S₀)→1 is not a model/design hypothesis; bounded B is the valid shipped scope.')
row('B.R3 · NEC', 'SE and two nonzero truths imply the displayed relative fit-term expansion.',
    'COUNTEREXAMPLE: β_n=(1/n,1/n), ε=.01; noise dominates the claimed ε/n signal term.',
    'DESIGN-VERIFIED: Gaussian exact Gram, λ_min=.99, B=1.', 'GAP: add effective beta-min and scale-dependent remainder.',
    'New clause; cancellation caveat is useful but does not supply beta-min.', 'c: no signal/noise margin stated',
    'E-B-NEC: median actual/claimed ratios 2.47×10³ and 2.38×10⁵ at n=10⁴,10⁶.')
row('B.R3 · scale / IC3', 'Built pairs verify finite ε>0 bounds; useful full D_* constants need νa² and b_X bounded.',
    'TRUE-AS-WRITTEN: reproduced 40 cases and checked actual partition.',
    'DESIGN-VERIFIED: n=40,p=8,B=2; C family for asymptotic SMC.', 'PLAUSIBLE',
    'REPAIRED: actual-block and eventual B≥9 conditions stated.', 'd: finite example dispatches exact; operator ε differs from raw entry ε',
    'Reproductions B1/B2; E-partition. Full useful scale n^−1/2/p assumes a≈n^−1/2, κ bounded below.')

group('Seat D · item 1 · §R3 / main WS′')
row('D.R3(a)', 'Discrepancy bounds separate σ²-coupling and cross-block dependence.',
    'TRUE-AS-WRITTEN using each bound only where its hypotheses hold.',
    'DESIGN-VERIFIED: Dε and C’s filed correlated family.', 'PLAUSIBLE',
    'REPAIRED: exact decomposition and constants retained.', 'S-WS; S-C; do not evaluate an unavailable side of min{…,D_*}',
    'CHK §§3–4; W1-PC2 D14. η-form and D_*-form are alternative sufficient hypotheses.')
row('D.R3(b)(i),(ii),(iv)', 'Global discrepancy, four-normalizer transfer, and Doeblin constants have explicit ε bounds.',
    'TRUE-AS-WRITTEN: use W1-PC1 §4 and CHK §4.',
    'DESIGN-VERIFIED: 15/15 D replica cases; independent built-pair check.', 'PLAUSIBLE',
    'REPAIRED: exhibit and finite hypotheses, rather than arbitrary groups.', 'S-WS; c: V nonempty; restricted claims do not imply coverage',
    'Reproduction D; inherited W1 D.M10(i),(ii),(iv).')
row('D.R3(b)(iii) · sandwich', 'Exact-frontier common-target stage counts obey the corrected threshold order.',
    'TRUE-AS-WRITTEN: feasibility inclusion and constrained greedy optimality; E-pilot search found no violation.',
    'DESIGN-VERIFIED: Dε; 16 applicable new common-target cases.', 'PLAUSIBLE',
    'REPAIRED: reversed order and threshold hypothesis; alias in CD removed.', 'd: code also has 10^−12 snap/validation, not just 2^−60 bisection',
    'W1-PC1 §4; E-pilot. D’s quoted greedy routine has no retained pilot targets.')
row('D.R3(b)(iii) · jump corollary', 'At a baseline threshold jump, perturbed T is one of the two one-sided counts.',
    'COUNTEREXAMPLE: baseline counts {2,4}; perturbed count 3 at ε=10^−5.',
    'DESIGN-VERIFIED: actual n=40,p=2,B=1; all η hypotheses hold.', 'IMPLAUSIBLE: sandwich permits intermediate integers.',
    'New overstatement after a correctly repaired sandwich.', 'c: multiple simultaneous threshold equalities',
    'E-jump: η=.000307301, .9e^{4η}=.901107. Replace two-point set by the integer interval; use margins for continuity.')
row('D.R3(b)(v)', 'Bounded perturbation preserves divergence of the baseline one-shot χ².',
    'TRUE-AS-WRITTEN: two-sided normalizer comparison; bounded η prevents cancellation of logarithmic divergence.',
    'DESIGN-VERIFIED: finite Dε; asymptotic statement is a conditional transfer.', 'PLAUSIBLE',
    'REPAIRED: sup_n η_n<∞; blanket H-ORTH transfer removed.', 'S-WS; c: η_n must be verified on the proposed design family',
    'W1-PC1 §4 D.M10(v); CHK §4. No upgrade of WS6(e) or WS8(d).')
row('D.R3(c)', 'One-shot refutation uses bounded blocks, initial support, and amended restricted-grid lower bounds.',
    'TRUE-AS-WRITTEN: cite CHK §§1–2,6.',
    'DESIGN-VERIFIED: inherited explicit orthogonal example; W1 masked LH.', 'PLAUSIBLE',
    'REPAIRED: inherited amendments explicitly retained.', 'S-WS; c: LH must discharge masking mass premises',
    'No re-proof of filed inherited checks; Q1(c) has the required independent pass with amendments.')
row('D.R3 · NEC', 'At fixed R² the total discrepancy oscillation is bounded below at order nε.',
    'COUNTEREXAMPLE: ε=.1, β_1=β_2=.47377937 gives osc(d)/n→0.',
    'DESIGN-VERIFIED: p=2,B=1,R²=.3305785, Gaussian noise.', 'GAP: shared-variance and cross-block terms can cancel.',
    'New clause. First-order expansion alone does not imply the claimed consequence.', 'distinguish d_X from total osc(d)',
    'E-D-NEC; also exact ridge formula uses ε_H=(1−n^−2)ε, not ε. Leading expansion may survive an amended remainder.')
row('D.R3 · scale / IC3', 'Dε has the built pairs and positive ε; useful η scales as nKεx̄/κ.',
    'TRUE-AS-WRITTEN on the stated small-ε, bounded-residual-margin family.',
    'DESIGN-VERIFIED: ε=10^−5; larger ε can invalidate the stage comparison.', 'PLAUSIBLE',
    'REPAIRED: finite η, built partition, and non-applicable cases disclosed.', 'd: component example; production exact branch; raw ε versus operator ε',
    'Reproduction D: η .0020–.0048 at 10^−5; at 10^−4 two of five seeds violate .9e^{4η}<1. E-partition.')

group('Seat A · item 2 · ranked main-list cards, §R2')
row('A.M1 · V+', 'Validity, general-h identities, declared islands, and output-intersection bounds.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§1,3; CHK §5 for amended N9.',
    'DESIGN-VERIFIED: filed finite-state checks, arbitrary valid X.', 'PLAUSIBLE',
    'REPAIRED: adaptive rules “need not” preserve identities; h normalized; N9 amendments retained.',
    'c: EX-A/H-U/CAL/IND-T/GUARD-W; N1 remains PROOF SKETCH',
    'No re-proof. Stationarity is not required of the ordinary terminal population for the evidence-weighted identity.')
row('A.M2(a)–(f) · H', 'Bounded functionals, finite-R bounds, joint inclusions, margins, and finitely declared intervals.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§2,14,16.',
    'DESIGN-VERIFIED: filed finite positive systems; nontrivial bounds under stacking.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: interval claim narrowed to finite declared probabilities; bounded-h normalization explicit.',
    'c: N1; d: R′=4 bound is vacuous; no quantile theorem',
    'The earlier “any/exact interval” assertion is withdrawn, not proved. This is a valid narrower statement.')
row('A.M2(g) · H', 'Explicit logarithmic stacking yields truth-anchor consistency on bounded-oscillation families.',
    'TRUE-AS-WRITTEN: filed moment bound plus finite-R error bound.',
    'DESIGN-VERIFIED: C’s family; A’s fixed-signal extra example fails as noted in item 1.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: explicit permitted R′(n,p) replaces random-M premise; liminf form.',
    'c: conditional computational model; d: stacking amendment must be recorded',
    'W1-PC2 D14 budget consequence; R′=4ceil(log₂(n+p)); no masked-family rate inferred.')
row('A.M3 · repair audit', 'Old variance, count-order, domain, and exhibit defects are addressed separately.',
    'TRUE-AS-WRITTEN as a repair inventory; new defects are item-1 rows.',
    'DESIGN-VERIFIED: revised groups and positive ε.', 'GAP: full guarantee needs the item-1 amendments.',
    'REPAIRED: variance offset, threshold/order, common targets, Ω scope, nondegeneracy; new zero-range/necessity issues remain.',
    'S-WS; S-C', 'Item 1 contains the clause-level verdicts for this main card; not a blanket approval.')
row('A.M4 · START', 'Exact start masses, masked law, dilution, and shared-variance discrepancy.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §5 and CHK §3.',
    'DESIGN-VERIFIED: W1-PC2 shared LH family and BO designs.', 'PLAUSIBLE',
    'REPAIRED: “never trivial” replaced by at least two positive block fits.',
    'c: H2/H3 outside LH; known-σ² comparison is a different working model',
    'T22/T27 qualifiers retained; Thm5-LH remains SAME-FAMILY-ONLY. No refuted DIL-DM/SHARE-M input.')
row('A.M5 · Z𝒯/CARD', 'Stored mass, TV/KL/PIPs, retention, confidence bounds, and odds certificate.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§3,16,20; W1-PC2 D5.',
    'DESIGN-VERIFIED: filed finite stores and LH.', 'PLAUSIBLE',
    'REPAIRED: reverse KL requires omitted positive mass; η<1 retained; output is joint.',
    'c: GUARD-W; MZ-P3 AUTHOR-ONLY; numerical certificate needs SC+VAL-FP',
    'Envelope U=Z_𝒯+U_m[1−sum_𝒯ϖ] is valid for a normalized common prior and valid U_m.')
row('A.M6 · HPM', 'Composition, finite search, LH consistency, variants, SIZE, and correct liminf delivery.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§6–7 and W1-PC2 D4.',
    'DESIGN-VERIFIED: full LH family already filed by PC2.', 'GAP: integrated LS0, emitted centre/N3, GUARD-W audits remain.',
    'REPAIRED: SIZE; arbitrary-centre search budget/completed scan; liminf; iid/no-LS0 variants labelled; K71 deferred.',
    'c: SR/OP-LS0/e4/scans; d: variants distinct from shipped run',
    'TheoremA/LS-score/T38-b1-LH filed checks reused; no new delivery theorem or global-greedy claim.')
row('A.M7 · STG', 'Restricted ESS, coverage, coded target refinement, count bound, and ideal crossing laws.',
    'TRUE-AS-WRITTEN for these clauses; zero-range existence omission is item 1.',
    'DESIGN-VERIFIED: filed grid examples and E-pilot; ideal family is a comparison object.', 'PLAUSIBLE',
    'REPAIRED: unconstrained “exact/minimal” removed; P included; resolution≤h/2; Ω scope; favourable LL moved to supplement.',
    'c: common threshold/targets; d: ideal laws; K31 remains OPEN',
    'W1-PC1 §9; W1-PC2 D7. Retain success/snap qualification; use max{1,ceil(…)} for zero range.')
row('A.M8 · SEP/KL', 'IID discovery and specified one-shot atom losses have the masking scale.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §8 and CHK §2.',
    'DESIGN-VERIFIED: inherited LH, with correct blocks.', 'PLAUSIBLE',
    'REPAIRED: universal algorithmic lower bound withdrawn; comparison loss explicitly restricted.',
    'd: iid/one-shot comparison, not production SMC; SEP-taska respected',
    'SEP-A/SEP-B remain PROVED (SF: none; XF: VERIFIED (A-REV9)); Lemma KL remains PROOF SKETCH (NEW-SYNTH).')

group('Seat B · item 2 · ranked main-list cards, §R2')
row('B.M1(b) · V+ RB wording', 'The evidence-weighted RB identity is qualified by a stationary round start.',
    'AMBIGUOUS: stationary-start qualification belongs to the unweighted N9 corollary, not the FK weighted identity.',
    'DESIGN-ASSERTED for literal stationary terminal starts in nontrivial finite runs.', 'GAP: separate the two statements.',
    'REPAIRED DIFFERENTLY: N9 qualifier added, but attached to the wrong claim.',
    'c: stationary-start assumption is an extra sampler condition',
    'CHK §5 last amendment; W1-PC1 §1. Use the weighted marginal identity without claiming terminal stationarity.')
row('B.M1(a),(c)–(e) · V+', 'Unnormalized identities, bounded declared h, output intersection, and pooling covariance.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§1,3,14.',
    'DESIGN-VERIFIED: filed finite FK/pooling examples.', 'PLAUSIBLE',
    'REPAIRED: N9 sufficient/need-not wording and frozen-output contract retained.',
    'c: ideal uniforms/CAL/IND-T/GUARD-W; N1 PROOF SKETCH',
    '“Not generally unbiased” correctly allows zero-covariance exceptions. Expectations remain potential-run identities.')
row('B.M2 · H', 'Normalized finite-R bounds, fixed-data SLLN, and explicit-rate consistency.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §2; composition with filed moment bound.',
    'DESIGN-VERIFIED: C family for growing dimensions; finite systems otherwise.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: explicit log stacking plus design-verified oscillation bound; liminf form.',
    'c: computational contract; d: stacking; R′=4 bound vacuous',
    'No useful masked M₂ rate follows from this card. Fixed-data SLLN does not imply triangular-array consistency by itself.')
row('B.M3 · repair audit', 'Old (N), q₂, variance, and count defects are replaced or withdrawn.',
    'TRUE-AS-WRITTEN as an inventory; item 1 records the new NEC/continuity defects.',
    'DESIGN-VERIFIED: Dε and D_B.', 'GAP: new unqualified continuity/necessity wording remains.',
    'REPAIRED DIFFERENTLY: (N) and uniform q₂-tail lemma withdrawn, not proved; weaker explicit m bound used.',
    'S-WS; S-C', 'Item 1 gives all §R3 clause verdicts; fallback without a stage-count clause alone would not satisfy HQ(b).')
row('B.M4 · START', 'Exact start, masked chain, positive block-fit criterion, and conditional favourable rate.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §5; CHK §3; filed leakage clause.',
    'DESIGN-VERIFIED: LH and D_B.', 'PLAUSIBLE',
    'REPAIRED: “active” clarified as positive fit; H1–H3 and conditional rate scope retained.',
    'c: mass/expansion conclusions outside the exhibited families; WS53F PROVED-UNDER',
    'Known-σ² statement requires recomputed known-precision tables; Thm5-LH remains SAME-FAMILY-ONLY.')
row('B.M5 · Z𝒯/CARD', 'Stored-posterior functional error scales with h and the output certificate is joint.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§3,16 and W1-PC2 D5.',
    'DESIGN-VERIFIED: finite-store examples and LH.', 'PLAUSIBLE',
    'REPAIRED: missing ‖h‖∞ included; retention/eviction rule explicit.',
    'c: GUARD-W; AUTHOR-ONLY MZ-P3; exact arithmetic and SC+VAL-FP gate',
    'The old h=(0,100) counterexample is repaired. No conditional-on-completion 95% guarantee asserted.')
row('B.M6 · HPM', 'LH search/output consistency, finite composition, margin transfer, and labelled variants.',
    'TRUE-AS-WRITTEN: reuse W1-PC1 §§6–7 and W1-PC2 D4.',
    'DESIGN-VERIFIED: filed shared LH family.', 'GAP: integrated LS0/N3/GUARD-W audits.',
    'REPAIRED: SIZE and liminf; K71 deferred; no-LS0 variant labelled.',
    'c: prescribed centre and complete scans; polynomial cost keeps its registry rate GAP',
    'T38-b1-LH qualified filed check reused; no delivery convergence inferred.')
row('B.M7 · STG', 'Target-constrained coded count includes P, range, and fine-enough bisection.',
    'TRUE-AS-WRITTEN: cite W1-PC2 D7 with resolution typo corrected.',
    'DESIGN-VERIFIED: filed grids and E-pilot.', 'PLAUSIBLE',
    'REPAIRED: exact/minimal dropped; D_V on all tilts; ≤h/2; absence of snap/ceiling failure; LL supplement.',
    'd: ideal crossing/fine-grid limits; c: D_V>0 explicit',
    'The zero-range issue in A is excluded here by D_V>0; a flat bridge can separately use retained pilot targets.')
row('B.M8 · SEP/KL', 'Masking-scale lower bounds concern iid discovery and explicitly specified one-shot estimators.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §8 and CHK §2.',
    'DESIGN-VERIFIED: filed LH.', 'PLAUSIBLE',
    'REPAIRED: universal one-shot/algorithmic wording withdrawn.',
    'd: comparison variants only; no production SMC lower bound',
    'The formal relative-variance identity χ²/Q is distinguished from its lower bound.')

group('Seat D · item 2 · ranked main-list cards, §R2')
row('D.H′(a)–(c),(e),(f)', 'Weighted identities, bounded finite-R errors, finite interval grid, and margin transfer.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§1–3,14,16.',
    'DESIGN-VERIFIED: filed finite laws and interval kernels.', 'PLAUSIBLE',
    'REPAIRED: expectations stay potential-run; output intersections transfer; finite declared endpoints and union bound replace “any interval”.',
    'c: EX-A/EX-S/CAL/IND-T/GUARD-W; N1 remains PROOF SKETCH',
    'No terminal stationarity, conditional-output expectation, quantile accuracy, or frequentist coverage is asserted.')
row('D.H′(d′)', 'Logarithmic declared stacking gives consistency on a model/design-verified bounded-oscillation family.',
    'TRUE-AS-WRITTEN: filed M₂ bound and finite-R inequality.',
    'DESIGN-VERIFIED: C’s asymptotic family.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: random-M hypothesis replaced by explicit R′(n,p) plus exhibited family.',
    'c: computational contract; d: optional stacking, not default four islands',
    'Dε alone is finite; use C’s family for the triangular-array non-vacuity claim.')
row('D.5′ · HPM/Theorem A', 'Composition, completed-search certification, and qualified LH output consistency.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§6–7 and W1-PC2 D4.',
    'DESIGN-VERIFIED: full shared LH family.', 'GAP: emitted-centre, integrated LS0/N3/GUARD-W audits.',
    'REPAIRED: ℓ≥τ(C), final scan, SIZE, liminf, extra c₄ search, labelled variants.',
    'c: OP-LS0/SR/e4/scans; d: iid/no-LS0 variants',
    'The overbarred potential-run notation in D_n is not set complement. Filed TheoremA/LS-score checks reused.')
row('D.M3′ · Z𝒯/MASK-PIP', 'Retention and envelope certificates give a masked-family PIP/MPM accuracy statement.',
    'TRUE-AS-WRITTEN: deterministic retention plus event containment.',
    'DESIGN-VERIFIED: W1-PC2 LH family.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: unverified regional U_rest replaced by valid global U_m envelope.',
    'c: GUARD-W/HPM gates; b: MZ-C1 also needs candidate/AUTHOR-ONLY qualifiers',
    'W1-PC1 §3; W1-PC2 D5/D4. PIP failure event is contained in HPM error or π(S₀)≤1/2.')
row('D.WS′ · repair audit', 'Prior count-order and H-ORTH transfer defects are repaired, but new corollaries fail.',
    'TRUE-AS-WRITTEN as a repair inventory; item 1 gives the adverse new clauses.',
    'DESIGN-VERIFIED: revised Dε.', 'GAP: amend jump corollary and necessity claims.',
    'REPAIRED: order; bounded η for divergence; actual blocks; blanket H-ORTH transfer withdrawn.',
    'S-WS; S-C', 'Do not label the entire package TRUE-AS-WRITTEN based on its inherited components.')
row('D.M6 · START', 'Start mass, masked law, dilution, and BO shared-variance discrepancy.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §5 and CHK §3.',
    'DESIGN-VERIFIED: filed LH and BO families.', 'PLAUSIBLE',
    'REPAIRED: positive fit fractions replace “active blocks”; other checked clauses unchanged.',
    'c: H2/H3 outside LH; Thm5-LH SAME-FAMILY-ONLY',
    'Uses the actual start tables; no DIL-DM(i) or SHARE-M(b) proof substitution.')
row('D.STG′', 'Coded acceptance/coverage and explicitly ideal crossing/length laws.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §9 and W1-PC2 D7/D13.',
    'DESIGN-VERIFIED: filed finite grids and ideal two-state comparison.', 'PLAUSIBLE',
    'REPAIRED: optimality restricted to retained targets; favourable LL moved to supplement; Λ_len renamed.',
    'd: ideal/fine-grid clauses; finite snap validation remains a code qualification',
    'K31 stays OPEN; T≤T_e is success accounting, not a masked stage-count rate.')
row('D.SEP′', 'IID masking lower bounds and ideal crossing comparison do not claim total work.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §8 and CHK §2.',
    'DESIGN-VERIFIED: filed LH.', 'PLAUSIBLE',
    'REPAIRED: universal one-shot scope and logarithmic-total-work sentence withdrawn.',
    'd: iid/one-shot and ideal-grid comparisons',
    'Evidence relative variance is χ²/Q; the atom bound is a lower bound, not an accuracy-matched SMC cost theorem.')
row('D.SL′(a)', 'Equipartition isolation tends to one for a fixed neighbourhood when K_n diverges.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §10 hypergeometric calculation.',
    'DESIGN-VERIFIED: fixed-size LH groups; K_n≈√p with p→∞.', 'PLAUSIBLE',
    'REPAIRED: population rather than observed cancellation used in (b).',
    'c: fixed c,g; require feasible equipartitions and distinguish fixed K examples',
    'Kn=2 or 4 are finite illustrations, not sequences making isolation probability tend to one.')
row('D.SL′(b)', 'SL’s actual prior gives uniform-in-iteration vanishing PIP and exclusion at fixed threshold.',
    'NEEDS-HYPOTHESIS: specify λ_s, its odds, slab scale, subset-size growth, and justify the uniform null BF bound.',
    'DESIGN-ASSERTED: no full SL-prior/iteration demonstration or promised LH replay filed.', 'GAP',
    'NOT REPAIRED: prior/rate named; iteration-uniform bound asserted rather than established on a model/design family.',
    'c: an algorithmic posterior/BF conclusion is not a model/design assumption; d: fixed PIP threshold variant',
    'W1-PC1 §10; local Song–Liang §§2.3,3.1: λ_s=|s|^−γ, odds λ_s/(1−λ_s). Singleton/reselected-subset cases need explicit handling.')
row('D.SL′(c),(d)', 'Exact-target and LS0 consistency hold on the same qualified LH family.',
    'TRUE-AS-WRITTEN: cite filed T03♯ and T38-b1-LH checks.',
    'DESIGN-VERIFIED: shared LH with SIZE eventually.', 'GAP: code gates inherited from 5′.',
    'REPAIRED: liminf and method-scope wording; this does not establish SL exclusion.',
    'Thm5-LH remains SAME-FAMILY-ONLY; c: LS0/code premises',
    'W1-PC2 shared LH / D4 / D8. D’s one-wave fallback for an unclosed SL-prior lemma should be enforced.')

group('Seat A · item 3 · §R4 masked accuracy')
row('A.R4 · Z𝒯 / weighted h', 'Masked LH yields joint-output restricted-posterior accuracy and a regime-free weighted-h bound.',
    'TRUE-AS-WRITTEN: retention plus HPM error tending to zero; cite filed weighted-h bound.',
    'DESIGN-VERIFIED: shared masked LH, π₀(S₀)=p^−c n^−c/2 exp(O_P(1)).', 'PLAUSIBLE',
    'REPAIRED: one named masked statement; no conditional-on-output claim; reverse KL has support condition.',
    'c: implementation premises inherited; does not prove P(output)→1',
    'W1-PC2 LH/D4/D5; W1-PC1 §§2–3. All HQ fallback metrics acknowledged; FW2 cites V11/N10 OPEN.')

group('Seat B · item 3 · §R4 masked accuracy')
row('B.R4 · Z𝒯/CARD', 'Stored-posterior TV/PIP/MPM accuracy holds jointly with output on masked LH.',
    'TRUE-AS-WRITTEN: event containment and filed LH/retention results.',
    'DESIGN-VERIFIED: shared LH, c=2; bounded blocks eventually.', 'PLAUSIBLE',
    'REPAIRED: named statement and support obstruction; all fallback metrics retained.',
    'c: LS0/N3/GUARD-W gates; no delivery theorem',
    'Interpret “with probability→1 jointly with output” as vanishing P(output and error), not conditional success or P(output)→1.')
row('B.R4 · M₂ aside', 'Masking forces the actual multistage island second moment M₂ to diverge.',
    'NEEDS-HYPOTHESIS: the cited χ² obstruction concerns one-shot weights; it gives no such actual-SMC implication.',
    'DESIGN-ASSERTED: no lower bound for actual coded-grid M₂ supplied here.', 'GAP',
    'New explanatory overstatement; core stored-posterior theorem does not need it.',
    'a: do not substitute one-shot χ² for actual-kernel variance (OPW2-cex)',
    'CHK §6 explicitly distinguishes one-shot failure from multistage performance; W1-PC2 D14 is an upper-bound result.')

group('Seat D · item 3 · §R4 masked accuracy')
row('D.R4 · MASK-PIP', 'On masked LH, joint-output PIP/MPM error vanishes through retention and LS0.',
    'TRUE-AS-WRITTEN: stated event containment is valid.',
    'DESIGN-VERIFIED: shared LH family; start misses polynomially.', 'PLAUSIBLE',
    'REPAIRED: named masked accuracy clause; support obstruction; FW2 and fallback set explicit.',
    'c: operational premises retained; no claim conditional on delivery',
    'W1-PC2 D4/D5 and W1-PC1 §3; inequality adds P(π(S₀)≤1/2), which vanishes under T03♯.')

group('Seat A · item 4 · §R5 run card')
row('A.R5(i) · Ĵ definition / T-J1', 'Weighted stage variances estimate a fixed-grid trapezoidal Jeffreys target.',
    'AMBIGUOUS: specify pre-resampling particles with their incremental weights; post-mutation particles are already at q_φt.',
    'DESIGN-VERIFIED: necessary pre-stage d and weights exist during each run.', 'GAP: fix timing and define the weighted mean explicitly.',
    'New definition; LLN plausible after timing is fixed.',
    'c: frozen grid; d: prospective deterministic accumulator, not available from saved study output',
    'Engine run_island_s computes lw before resampling, then discards populations; measured rounds occur only at φ=1. Reweighting post-move states again targets q_{2φt−φt−1}.')
row('A.R5(i) · T-J2,T-J3', 'Trapezoid error uses κ₄; J has range and masked lower bounds.',
    'TRUE-AS-WRITTEN: composite trapezoid remainder and κ₄ bound; inherited J/KL identities.',
    'DESIGN-VERIFIED: finite discrepancy on each valid input.', 'PLAUSIBLE',
    'New deterministic clauses; no finite-N concentration claim made.',
    'No RNG or feedback; label J_hat_T as a quadrature target',
    'Var″=κ₄, |κ₄|≤osc(d)^4; error ≤sup|κ₄| sum Δ³/12. W1-PC1 §16 supplies J/KL bounds.')
row('A.R5(ii) · leakage', 'Maximum cross-block correlation and a block eigenvalue bound control per-model perturbations.',
    'TRUE-AS-WRITTEN with positive κ̂ and a maximum over V when used as η_V.',
    'DESIGN-VERIFIED: revised built blocks; η̂ computable deterministically.', 'PLAUSIBLE',
    'REPAIRED: leakage is a reporting proxy, not a power claim; V restriction explicit.',
    'No RNG/feedback; c: finite domain and uniform maximum required for transfer',
    'CHK §4; W1-PC1 §4. Inputs X/blocks/tables/V already exist. Singular κ̂ or failed residual-margin tests must print n/a.')

group('Seat B · item 4 · §R5 run card')
row('B.R5(i) · Ĵ', 'Evidence-weighted endpoint mean minus iid-start mean estimates Jeffreys divergence.',
    'TRUE-AS-WRITTEN for T1–T4: finite bounded d, envelope scaling, and filed SLLN.',
    'DESIGN-VERIFIED: finite correlated systems; C family for useful stacking bounds.', 'PLAUSIBLE',
    'New definition; d must be declared before stream 10 as the seat requests.',
    'No RNG/feedback; c: N1; prospective start/end accumulators needed',
    'Existing particles carry d; add deterministic initial-mean and measured-d sums. Initial variance≤osc²/(4R′N_e). Saved study records lack these sums.')
row('B.R5(i) · T5 interpretation', 'Masked lower bound on J means the displayed Ĵ detects large divergence.',
    'AMBIGUOUS: target J lower bound is valid; detection/large-Ĵ claim needs an estimator-error bound in that regime.',
    'DESIGN-ASSERTED for diagnostic power; target masked family is verified.', 'GAP: no informative masked error rate supplied.',
    'New wording; retain T5 only as a statement about J.',
    'a: record-blindness obstruction still applies; no flag-power theorem',
    'A large true divergence does not force its finite-run estimate to be large. The displayed T3 bound is often vacuous under masking.')
row('B.R5(ii) · leakage T1–T6', 'Cross-block proxy, explicit η, regularized norms, and V-only transfers are design-computable.',
    'NEEDS-HYPOTHESIS: T2 needs κ>0, δ<1, ū<1 and δū<(1−δ)(1−ū), with failure reported n/a.',
    'DESIGN-VERIFIED: Dε meets these conditions at the stated small ε.', 'PLAUSIBLE after stating domains.',
    'New reporting clause omits the finite-domain conditions present in §R3.',
    'No RNG/feedback; c: V-only transfers remain V-only',
    'CHK §4; W1-PC1 D.M10(i). For T3, δ_H’s Gershgorin numerator includes the extra (n+1) factor. ε̂=0⇔BO is valid.')

group('Seat D · item 4 · §R5 run card')
row('D.R5(i) · Ĵ,T1–T3', 'Endpoint-minus-start Jeffreys estimate has an explicit finite-budget error bound.',
    'TRUE-AS-WRITTEN using the actual global oscillation in T3.',
    'DESIGN-VERIFIED: finite d and iid starts; C family for informative stacking.', 'PLAUSIBLE',
    'New bound: split ε/2 between ratio and iid mean; no independence between them needed.',
    'No RNG/feedback; c: N1/declared d; prospective deterministic accumulators',
    'The ratio term is 4(M₂−1)/R′+16M₂ osc²/(R′ε²); start Chebyshev term osc²/(R′N_eε²). Union bound gives T3.')
row('D.R5(i) · V rescaling', 'Enumerating V supplies global d_min and osc d for a bounded N1 test function.',
    'COUNTEREXAMPLE: V={∅,{0}} has d=0; Ω also contains d=.34492652.',
    'DESIGN-VERIFIED: n=40,p=2,B=1, positive cross-correlation.', 'PLAUSIBLE: use global analytic envelopes or enumerate Ω.',
    'New clause; finite-budget theorem survives with a valid global range.',
    'c: h must be bounded on Ω; restricted calibration set is not full support',
    'E-V: range on V is zero while range on Ω is positive. V-only normalization may be undefined or exceed [0,1].')
row('D.R5(ii) · ε̂,η̂,T4,T5', 'Proxy and block-table bound supply global perturbation constants or n/a.',
    'TRUE-AS-WRITTEN on the positive-κ̂ finite domain; treat the empty model separately as zero.',
    'DESIGN-VERIFIED: Dε; per-block maxima bound capped-model fit sums.', 'PLAUSIBLE',
    'New deterministic report; stage-count qualification remains as in item 1.',
    'No RNG/feedback; c: κ̂>0; singleton/empty conventions',
    'CHK §4 supplies the norm bound; η̂ uses a conservative global ū̂. n/a on invalid margins is correct; V≠Ω is not used for a global η̂.')
row('D.R5(ii) · T6', 'Every two-signal-block family has |d_X(S₀)| of order nε̂|β_1β_2|/σ².',
    'COUNTEREXAMPLE: ε=.1, β=(.8,−.04010050) gives d_X/n→0 with positive claimed order.',
    'DESIGN-VERIFIED: Gaussian exact Gram, two singleton blocks, κ=1.', 'GAP: first-order expansion permits cancellation; add a signal/alignment margin.',
    'New clause; the upper bound in T5 is unaffected.',
    'distinguish a sufficient upper envelope from a universal lower bound',
    'E-D-T6: β_2/β_1=(−1+sqrt(1−ε²))/ε; full and BO fitted gains agree to leading order.')

group('Seat A · item 5 · changed supplement cards')
row('A.S2 · SL', 'Population isolation plus an assumed uniform null BF bound gives fixed-threshold exclusion.',
    'NEEDS-HYPOTHESIS: specify prior odds and subset-size domain; a uniform null BF bound alone does not give PIP→0.',
    'DESIGN-ASSERTED: no uniform SL-prior/iteration demonstration filed.', 'GAP',
    'REPAIRED: population cancellation and fixed threshold. NOT REPAIRED: uniform BF/rate obligation moved into hypotheses.',
    'c: assumed Bayes-factor conclusion is not a model/design hypothesis',
    'W1-PC1 §10; E-SL: literal λ_1=1 gives PIP=1 despite BF→0. Numerical LH rerun is promised, not present.')
row('A.S3 · D', 'Trajectory/search accounting and same-units SL comparison replace a speed claim.',
    'TRUE-AS-WRITTEN as corrected counting and comparison scope.',
    'DESIGN-VERIFIED: actual budget loops and finite runs.', 'GAP: integrated execution DAG/rate audit remains.',
    'REPAIRED: each T/search counted separately; workers, n/p, T, score cost, loss named; no exact-π claim.',
    'c: execution model; MA-PropD author-only; Cost-T38 XF GAP',
    'W1-PC1 §13; W1-PC2 D6. No new speed-up theorem or particle-parallel depth assertion.')
row('A.S4 · Z', 'Terminal-off bound allows exceptions and crude variance uses global oscillation.',
    'TRUE-AS-WRITTEN: retain filed source exception-probability statement.',
    'DESIGN-VERIFIED: finite full-space d; inherited masked family.', 'PLAUSIBLE',
    'REPAIRED: exception≤2sqrt(δ₁), conditional division by κ, deterministic full-space D.',
    'FMP-Na XF GAP; exact-refresh formula not substituted',
    'W1-PC1 §15. OPW2-ThmA stays PROVED (SF: none; XF: VERIFIED (A-REV9)); T26 overall remains CONJECTURE.')
row('A.S5 · TARGET; S7 · POOL', 'Target equivariance, IG constant, normalized h, and one-record marginal scopes are corrected.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§14,20.',
    'DESIGN-VERIFIED: filed finite designs, ties, and recording laws.', 'PLAUSIBLE',
    'REPAIRED: target-only invariance; tie-free algorithm qualifier; 2νb₀; h∈[0,1]; uniform recording-state marginal; “iff” dropped.',
    'No new algorithmic symmetry or unweighted-population exactness claim',
    'Prop2(c) filed check reused. K76 remains seat-proved, unchecked; T01 qualifier retained.')
row('A.S8 · CERT', 'Weak local maxima, per-search scans, exact certificate completion, and deterministic score perturbations.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §17 and checked certificate lemmas.',
    'DESIGN-VERIFIED: filed duplicate-tie example and finite scan arithmetic.', 'PLAUSIBLE',
    'REPAIRED: ties allowed; unsupported rounding K107 deferred; exact perturbation K108 retained.',
    'N16 OPEN; numerical card still needs SC+VAL-FP',
    'Returned unscanned local_limit point gets no local certificate; unresolved region search gives no outside-region guarantee.')
row('A.S9 · duplicate numeric limit', 'Two duplicate columns under the ridge/BB target have limiting PIP 2/3.',
    'COUNTEREXAMPLE without p=2 qualification: add one orthogonal null; duplicate PIP→3/5.',
    'DESIGN-VERIFIED: p=3, fixed signal/noise; actual BB prior and singular Gram allowed.', 'PLAUSIBLE: label 2/3 as the W1 p=2 example.',
    'REPAIRED DIFFERENTLY: symmetry formula is correct; new numeric paraphrase overgeneralizes the example.',
    'prior odds depend on p and selected background size',
    'E-duplicates: PIP=.601942,.600627,.600199 at n=400,4000,40000. Pair/single prior ratio=1/(p−1).')
row('A.S10 · KL/TV/BLOCKS', 'Thermodynamic length, minorization, squared-kernel mixture, graph, and SIZE qualifications.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§16,19.',
    'DESIGN-VERIFIED: filed finite kernels and built-block designs.', 'PLAUSIBLE',
    'REPAIRED: Λ_len renamed; 1/M; R₂=(1/m)sum P_j²; p≥2; SIZE.',
    'c: positive minimum/range constants; no general mixing-rate conclusion',
    'The graph p=1 exception is now explicit. Preservation and equality of groups are distinguished.')
row('A.S11 · STG-ideal', 'Favourable ideal depth is conditional on LL or the over-tilted truth-mass bound.',
    'TRUE-AS-WRITTEN as a conditional statement.',
    'DESIGN-ASSERTED: no newly verified LL family supplied.', 'GAP: LL/upper-tilt input still needs a design route.',
    'REPAIRED: unconditional favourable inference removed; crossings require separated pair-dominance.',
    'c: LL is not itself a model/design condition; d: ideal grid',
    'W1-PC1 §9. STG-F remains PROVED (SF: none; XF: none); W′ production-grid transfer remains GAP.')

group('Seat B · item 5 · changed supplement cards')
row('B.S1 · SL', 'Population nullity and fixed-threshold exclusion are posed under SL’s actual prior.',
    'NEEDS-HYPOTHESIS: uniform-in-iteration BF control and prior odds are unclosed; fixed FDR level is not a fixed PIP threshold.',
    'DESIGN-ASSERTED for the exclusion theorem; finite g=5,p=60 partition is verified.', 'GAP',
    'REPAIRED: population covariance and SIZE. NOT REPAIRED: iteration-uniform prior/FDR step, acknowledged as GAP.',
    'c: specify λ_s/(1−λ_s) and subset growth; d: fixed PIP threshold is a variant',
    'E-partition verifies B=7 at n=100,p=60. Song–Liang §§2.3,3.1 and W1-PC1 §10; promised numerical fallback is not a theorem.')
row('B.S3 · D; S4 · Z', 'Per-trajectory accounting, same-units comparison, tail exceptions, and global-range variance scope.',
    'TRUE-AS-WRITTEN: use corrected W1 scopes.',
    'DESIGN-VERIFIED: actual finite budget loops and inherited finite laws.', 'GAP: integrated DAG/rate audit remains.',
    'REPAIRED: own T/search counts; worker/n-p/T/score/loss accounting; exception-probability form; deterministic full-space D.',
    'Cost-T38 XF GAP; FMP-Na XF GAP; no exact-refresh substitution',
    'W1-PC1 §§13,15; W1-PC2 D6. Imported exponential-tail clause must retain all named source hypotheses, as B stipulates.')
row('B.S5 · KERNEL; S9 · IDENT', 'Sufficient reversibility, graph exception, squared-mixture minorization, and thermodynamic length.',
    'TRUE-AS-WRITTEN for the revised mathematical scopes.',
    'DESIGN-VERIFIED: filed finite kernels and built blocks.', 'PLAUSIBLE',
    'REPAIRED: need-not fixed order; p≥2; 1/M; squared R₂; Λ_len.',
    'c: N3 tie-DP is still OPEN; do not convert its assumption into a code fact',
    'CHK §5; W1-PC1 §§16,19. No new implementation proof is supplied for tie-aware DP.')
row('B.S6 · withdrawals', 'Quantitative barrier and flag-power claims are withdrawn; qualitative limitations remain.',
    'TRUE-AS-WRITTEN: cite filed counterexamples and corrected scope.',
    'DESIGN-VERIFIED: inherited barrier/genealogy/oracle constructions.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: implausible k-way bound and Gaussian flag formula withdrawn, not proved.',
    'K99 quantitative/K80 FUTURE_WORK; no universal detection claim',
    'W1-PC1 §18. The stated qualitative SHARE-PB remark does not imply the withdrawn W(2p)^−k rate.')
row('B.S6 · duplicate numeric limit', 'Two duplicates under the ridge/BB target have limiting PIP 2/3.',
    'COUNTEREXAMPLE without p=2 qualification: p=3 with an orthogonal null gives 3/5.',
    'DESIGN-VERIFIED: actual fixed-p BB target and duplicate design.', 'PLAUSIBLE: restrict the numerical example.',
    'REPAIRED DIFFERENTLY: general symmetry formula correct; unqualified numeric limit remains false.',
    'same issue as A.S9; not an estimator effect',
    'E-duplicates. General two-duplicate/orthogonal-null limit is p/(2p−1); background selected predictors change the odds further.')
row('B.S7 · TARGET; S8 · CERT', 'Target-only symmetry, η<1 odds, weak local maximum, and exact perturbation certificates.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§17,20.',
    'DESIGN-VERIFIED: filed duplicate/tie and finite-law examples.', 'PLAUSIBLE',
    'REPAIRED: tie caveat, η<1, ties allowed; unsupported rounding bound withdrawn to K107.',
    'T01 external review queued; N16 OPEN; SC+VAL-FP gate retained',
    'The weak-local-maximum statement repairs the tie counterexample. Exact B&B gives unresolved on budget exhaustion.')
row('B.S10 · PIP-eq', 'TV bias uses a uniform recording-state marginal; splitting is an exact-refresh comparison.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §14.',
    'DESIGN-VERIFIED: filed finite recording law.', 'PLAUSIBLE',
    'REPAIRED: population-versus-state type error; split clause explicitly idealized.',
    'd: exact refresh; general LH locking remains XF ERROR',
    'MA-CorV remains PROOF SKETCH. No four-round finite-R variance ordering is asserted.')

group('Seat D · item 5 · changed supplement cards')
row('D.M13 · D', 'Work/depth accounting and SL comparison use own trajectories and matched units.',
    'TRUE-AS-WRITTEN as corrected accounting, not a speed theorem.',
    'DESIGN-VERIFIED: finite actual-budget loops.', 'GAP: integrated DAG and displayed rate audit remain.',
    'REPAIRED: per-T/search counts; workers, n/p, T, score cost, loss scope; no exact-π output.',
    'MA-PropD author-only; Cost-T38 XF GAP', 'W1-PC1 §13 and W1-PC2 D6.')
row('D.S1,S2,S4 · target/graph/output', 'Target symmetry, graph p≥2, SIZE, and adaptive islands “need not preserve” wording.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§3,19,20.',
    'DESIGN-VERIFIED: filed finite/tie/block examples.', 'PLAUSIBLE',
    'REPAIRED: target-only symmetry; p≥2; preservation versus equality; adaptive wording.',
    'c: IND-T/GUARD-W/N3 audits remain; approved n=2 extension is not an implemented fact',
    'Unchanged target/worker lemmas are not re-proved. Fixed-p dispatch stays seat-proved, unchecked.')
row('D.S6 · evidence / envelope', 'Tail exceptions and global pathwise variance replace an unsupported regional bracket.',
    'TRUE-AS-WRITTEN: Var(W)≤e^{2 osc_Ω d}−1 follows from the filed pathwise range.',
    'DESIGN-VERIFIED: finite full-space discrepancy; N17 provides a global envelope.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: valid global envelope replaces regional covering; global D and exception form retained.',
    'S-C; no 1/N rate claimed by the replacement bound',
    'W1-PC2 D14/D5; W1-PC1 §15. The bound is conservative and may be uninformative.')
row('D.S8 · terminal-law TV', 'Shipped logarithmic burn-in is useful iff M₁=O(1).',
    'AMBIGUOUS: bounded M₁ is sufficient; item 7 correctly gives the broader L/M₁→∞ criterion.',
    'DESIGN-VERIFIED: C family has M₁=O_P(1).', 'PLAUSIBLE with item-7 wording.',
    'New “iff useful” wording should be replaced by the explicit rate criterion.',
    'c: M₁ is a target/start ratio, not an observed mixing diagnostic',
    'E.g. M₁≈sqrt(log n) still gives (1−1/M₁)^{L_n}→0. Filed minorization itself is unchanged.')
row('D.S9,S11 · rounding/duplicates', 'Unsupported rounding is deferred; duplicate symmetry uses expected group size.',
    'TRUE-AS-WRITTEN: cite W1-PC1 §§17–18.',
    'DESIGN-VERIFIED: filed finite duplicate and score-perturbation examples.', 'PLAUSIBLE',
    'REPAIRED: K107 removed; K108 retained; PIP=E[group size]/d; 1/d needs one selected asymptotically.',
    'N16 OPEN; no unqualified 2/3 numeric limit inserted here',
    'D’s general duplicate correction is sound. Rigorous numerical certificates still require SC+VAL-FP.')

group('Seat A · item 6 · §R6 item 7 growth rates')
row('A.growth · R′,ℓ,L,N,T', 'Stacking rate is explicit; other main-card budgets remain the shipped functions.',
    'TRUE-AS-WRITTEN for consistency on C’s verified family.',
    'DESIGN-VERIFIED: C family has bounded D_* and target concentration.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: R′_n=4ceil(log₂(n+p)) replaces sampler-M premise.',
    'c: implementation gates; d: stacking edit must be recorded',
    'ℓ=ceil(log₂(n+p+1)) suffices for fixed c on LH; L,N already depend on n,p. The separate fixed-data N→∞ LLN is an auxiliary limit, not a new shipped budget.')

group('Seat B · item 6 · §R6 item 7 growth rates')
row('B.growth · R′ and summaries', 'Explicit logarithmic or polynomial stacking controls fixed or polynomially many declared summaries.',
    'TRUE-AS-WRITTEN: finite-R bound and filed C budget union bound.',
    'DESIGN-VERIFIED: C family; at most (n+p)² summaries.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: R′=4ceil(log₂(n+p)); simultaneous R′=4ceil((n+p)^6/4).',
    'd: optional stacking, not particle splitting; IND-T extension audit pending',
    'Rates are explicit in n,p; no random realized M is used as a budget hypothesis.')
row('B.growth · T_e,L,ℓ,N', 'Stage success is budget-conditional; terminal-TV rates require sufficient burn-in.',
    'TRUE-AS-WRITTEN as a conditional accounting/remark, not a model/design success theorem.',
    'DESIGN-VERIFIED: C family supplies useful L via bounded global oscillation.', 'PLAUSIBLE',
    'REPAIRED: no masked coded-T or universal delivery rate claimed.',
    'c: T_e≥reported bound is a sampler-budget condition; exp(osc d) can be replaced by design envelope',
    'A sufficient declared rate is L≥exp(D_bound)log(1/ε) when such a global bound is available. No rate claimed for masked families.')

group('Seat D · item 6 · §R6 item 7 growth rates')
row('D.growth · R′,L,ℓ,N', 'Logarithmic stacking and shipped burn-in/search budgets have explicit consistency scopes.',
    'TRUE-AS-WRITTEN: under L_n→∞, the displayed contraction bound vanishes iff L_n/M₁→∞.',
    'DESIGN-VERIFIED: C family; fixed c LH for search.', 'PLAUSIBLE',
    'REPAIRED DIFFERENTLY: R′=4ceil(log₂(n+p+1)); no unknown-M budget premise.',
    'c: non-model computational gates remain; d: stacking configuration',
    'Bounds use design-computable d/D_*; their growth is verified on C’s family, not asserted uniformly over masked designs.')

def render():
    rows=[r for _,rs in GROUPS for r in rs]
    counts=[Counter(r[i].split(':')[0].split(' for ')[0].split(' using ')[0] for r in rows) for i in (2,3,4)]
    # Canonical verdicts are prefixes; prose follows a colon or explanatory clause.
    classes=[['TRUE-AS-WRITTEN','COUNTEREXAMPLE','NEEDS-HYPOTHESIS','AMBIGUOUS'],
             ['DESIGN-VERIFIED','DESIGN-ASSERTED','DESIGN-FAILS'],['PLAUSIBLE','GAP','IMPLAUSIBLE']]
    counts=[{v:sum(r[i].startswith(v) for r in rows) for v in vs} for i,vs in zip((2,3,4),classes)]
    intro=['# MEET-THM · Check wave 2 · Proof checker 1','',
           'Scope: Seats A, B and D. TRUE-AS-WRITTEN means no counterexample found in the stated search, not a proof. Filed checks are cited rather than re-proved; no registry status is upgraded.','',
           f'Summary counts ({len(rows)} clause-review rows):','',
           '| Dimension | Counts |','|---|---|']
    for name,c in zip(['True','Non-vacuous','Route'],counts):
        intro.append('| '+name+' | '+'; '.join(f'{v}: {n}' for v,n in c.items())+' |')
    repair_counts=Counter('NOT REPAIRED' if 'NOT REPAIRED' in r[5] else
                         'REPAIRED DIFFERENTLY' if r[5].startswith('REPAIRED DIFFERENTLY') else
                         'REPAIRED' if r[5].startswith('REPAIRED') else
                         'NEW / NO PRIOR REPAIR' for r in rows)
    intro.append('| Repair status | '+'; '.join(f'{k}: {v}' for k,v in sorted(repair_counts.items()))+' |')
    intro+=['','Every COUNTEREXAMPLE / NEEDS-HYPOTHESIS / DESIGN-FAILS / IMPLAUSIBLE / NOT REPAIRED row:','']
    for r in rows:
        if any(v in r[i] for i,v in [(2,'COUNTEREXAMPLE'),(2,'NEEDS-HYPOTHESIS'),(3,'DESIGN-FAILS'),(4,'IMPLAUSIBLE'),(5,'NOT REPAIRED')]):
            parts=[r[i] for i in (2,3,4,5) if any(v in r[i] for v in ['COUNTEREXAMPLE','NEEDS-HYPOTHESIS','DESIGN-FAILS','IMPLAUSIBLE','NOT REPAIRED'])]
            intro.append('- **'+r[0]+'** — '+' '.join(parts))
    intro+=['','Evidence and scope:','',
        '- Fetched origin. Read the brief, all assigned R2 sections, R1 references for retained cards, both W1 verdicts, SYNTH_R1 §0.1/§3, HQ Q1–Q4, CHK_INHERITED, amended METHOD on origin/theory/MEET-v31, and relevant production headers. Only W2_PC1 was written; no commit or push.',
        '- Reproductions A/B1/B2/D are verbatim copies of the four original scratch scripts, with SHA-256 and source paths in scripts/REPRODUCTION_MANIFEST.tsv. Logs are scripts/seat_a_ic3_p16.txt, seat_b_chk1.txt, seat_b_chk2.txt, seat_d_r2d_check.txt. All printed numerical results reproduce to rounding. A uses 9+4 settings; B uses 40+16; D uses 15+16 (48 seed-level necessity enumerations).',
        '- New checks: scripts/new_checks.py and new_checks.json/.txt. E-jump, E-A-NEC, E-B-NEC, E-D-NEC, E-growth, E-zero, E-partition, E-pilot and E-V refer to the corresponding named JSON constructions. Local Python 3; fixed seeds from 0–12 only; every script finished in under one minute. No network computation or cluster job.',
        '- JSON key map: E-jump=D_jump_counterexample; E-A-NEC=A_Nd_fixed_eps_counterexample; E-B-NEC=B_NEC_weak_signal_counterexample; E-D-NEC=D_NEC_fixed_R2_counterexample (plus D_ridge_formula); E-D-T6=D_T6_dX_cancellation; E-V=D_V_envelope_counterexample; E-growth=A_fixed_signal_growth_exhibit; E-zero=A_zero_range_grid; E-partition=revised_partitions; E-pilot=common_pilot_sandwich_search; E-duplicates=AB_duplicate_limit_scope; E-SL=SL_singleton_prior_boundary.',
        '- Revised finite exhibits are component checks: A has n=64,p=16,B=4; B/D have n=40,p=8,B=2. All recover their proposed groups and have ε>0. Production dispatches exact there. The already-filed C family (groups of nine, ε_n=1/(np), shrinking signals) supplies an eventual SMC-dispatched example, with blocks=groups for n≥9^6.',
        '- Flag c identifies computational/implementation premises: EX-A, H-U/EX-S, frozen CAL, declared R′, IND-T, GUARD-W, OP-LS0, emitted centre/N3, complete scans, fixed V/targets, moment/concentration conclusions. These are not all model/design conditions. Statistical non-vacuity does not close their code audits. Flag d marks ideal grids, iid discovery, no-LS0 variants, stacking, and component tests.',
        '- Registry ledger: S-WS = OWS-WS3/4 and OWS-WS6d/WS7: “PROVED (SF: none; XF: none)”; CHK adds “VERIFIED (PC1, cross-family, line by line)” for WS3/4 and “VERIFIED WITH AMENDMENT” for WS6d/WS7. AREV9-OWSTAB remains “VERIFIED under H-ORTH exactly as stated, including W(d)\'s stronger upper-side premise”; W′ remains “VERIFIED ideal full-space grid under H-ORTH; production-grid transfer remains GAP”.',
        '- S-C = C’s D_* / actual-grid moment argument remains “PROOF SKETCH (NEW-COMP)”; W1-PC2 TRUE-AS-WRITTEN is statement sanity. N1 remains “PROOF SKETCH”; A1new “PROOF SKETCH (NEW-SYNTH)”; PC1c3 “PROVED (PC1 claim 3)”, with “E[W_r ĥ_r] = π(h) is still a premise”.',
        '- Other registry qualifiers: N9K “PROVED (candidate)” plus CHK “VERIFIED WITH AMENDMENT”; Prop2(a,b,d,e) “PROVED (SF: VERIFIED (W5-LOCKBOOK); XF: GAP (A-REV4))”; Thm5-LH “PROVED (SF: VERIFIED (W3-VEXP); XF: none)” (SAME-FAMILY-ONLY); MZ-P3 “PROVED (P3 top store, deterministic); P3′ conditional on T03 + discovery”, “candidate: not reviewed, not adopted”, AUTHOR-ONLY; MZ-C1 “PROVED (C1-C3 per-fit, deterministic)”, candidate/not reviewed, AUTHOR-ONLY; T01–T03 “PROVED-LOCKED (wave 3; external review queued)”. D.M3′ omits MZ-C1’s candidate/AUTHOR-ONLY qualifier; restore it. These are separate from newer checks.',
        '- No repaired card is licensed to reuse index-§4 false claims: CEX-guard, OPW2-cex, general LH locking XF ERROR, SEP-taska, C3-PGD/CEX-localmax, T33-errbound, or the old unconditional STG-Wp interpretation. Their exclusions remain necessary. New adverse clauses below are not rescued by inherited registry labels.','']
    out=intro
    for title,rs in GROUPS:
        out+=['## '+title,'','| card · clause | claim (≤25 words) | true | non-vacuous | route | repair status | flags | evidence |','|---|---|---|---|---|---|---|---|']
        for r in rs:
            out.append('| '+' | '.join(s.replace('|','\\|') for s in r)+' |')
        out.append('')
    out+=['Disposition for the chair:','',
          '- HQ Q1(a) and Q1(c) have usable packages on their stated scopes. Q1(b) has a credible route through the corrected common-target sandwich and continuous discrepancy/divergence/moment envelopes, with a noncritical-threshold qualification for local constancy of integer stage counts. The revised text is not clean as written: remove D’s two-value jump corollary and amend the necessity/continuity statements. A fallback omitting stage count entirely would not meet binding Q1(b).',
          '- Every main-list card was examined at its §R2 scope. Most wave-1 repairs are implemented; the SL prior/iteration obligation is still open in all three seats. Treat the SL separation as conditional or future work until the specific model/design and prior-odds argument is filed; naming the prior does not close it.',
          '- HQ Q3 is met by the masked reported-store PIP/MPM/TV statement, with the named implementation premises. Q4 can use deterministic online reporting accumulators without new RNG or feedback, but needs the timing/global-envelope repairs above. None of these definitions establishes retrospective availability on the 2,400 saved study fits.',
          '- Growth rates are explicit optional-stacking rates on C’s verified family. A’s additional fixed-signal shrinking-ε example fails bounded oscillation. No shipped-four-island consistency, masked actual-M₂ divergence theorem, unconditional coded-stage continuity, validated floating-point certificate, or delivery theorem is added by this review.',
          '', 'Review complete. Only theory_campaign/MEET-THM/evidence/W2_PC1/ was written. No commit or push.','']
    HERE.parent.joinpath('VERDICTS.md').write_text('\n'.join(out))
    HERE.joinpath('verdict_rows.json').write_text(json.dumps(GROUPS,indent=2)+'\n')
    print(f'Wrote {len(rows)} rows; counts: {counts}')

if __name__=='__main__': render()
