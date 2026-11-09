# R13 — Independent council seat, round 2: Theorem FAC-CS-iid

**Overall score: 9.2 / 10. All six gates PASS. Required fixes: none.**

I accept this deliverable as is. This is one independent seat's verdict; the joint council decision still requires the other seat's score and gates in this round.

Scope reviewed: locked `STATEMENT.md` v3, claims (C1)–(C4); `lemmas/X1_representation.md` through `X6_assembly.md`; `REPORT.md` §§1–4 and §6. Target 2, REPORT §5, X7 and T2 are outside this verdict. I applied the binding asymptotic scope rule: asymptotics and the size of the onset are not defects.

## Gate verdicts

| Gate | Verdict | Reasons |
|---|---|---|
| **G1 — Correctness of every step** | **PASS** | The rotation/RSS/Schur algebra, ridge corrections, structured-set perturbation estimate, deterministic crossing and containment arguments, path induction, start-mode increments, and consistency/delivery assembly survive independent re-derivation and the checks below. Round 1's incorrect REPORT §6 generalisation has been corrected. Issue 1 below is a presentation improvement to the new audit table, not a gap in the proof. |
| **G2 — Hypotheses used = hypotheses stated** | **PASS** | Fixed positive rho, Gaussian CS rows, independent Gaussian noise with fixed positive variance, fixed nonzero sign-corrected raw coefficients, fixed s0 >= 1, (FS), and limsup log p/log n < 1/2 supply the inputs actually used. K=p eventually. (FS) is used for the start-mode argument; the path proof does not assume masked-truth (FS-prime) or a condition on the realised partition. The implementation and additional delivery premises are explicit. |
| **G3 — No hidden assumptions** | **PASS** | X4 uses a single event simultaneously for every omitted set of at most 15 nulls. It does not assume that the selected N0 is independent of xi or W. X5–X6 condition on the raw design, which determines column scales and theta-star. The established-prefix induction, probability-one nondegeneracy, bounded/oscillating p, empty null sets, one-sided end states, hypothetical best-deletion candidates, and exceptional sets of size 16/17 are handled. |
| **G4 — Cited lemmas have adequate status** | **PASS** | I inspected CITECHECK.txt, reran its five path/line checks (5 OK, 0 MISS), and checked the substantive statements and status qualifications against the listed sources. FAC-B and FAC-A are checked packages; their individual lemma headers are not silently upgraded. T03-sharp, T38-(0), [OP], CAP, CR, Proposition F and A2 are used with the qualifications reproduced below. Unchecked Target-2 work is not an input. |
| **G5 — Constants and rates tracked** | **PASS** | The single scale varpi = 6 C_X Hbar sqrt(p log n/n) + n^(-1/3) closes the ordering error and band absorption. The second-order term, D6/D7/D8, density condition, bulk addition/swap separation, and end-phase errors have the asserted asymptotic signs. D3 gives kappa=kappa_infinity+o(1), so c_D remains positive. All errors in the end-phase score comparisons are o(1), whereas the relevant score separations have order log n; the majority-side statistic separation also dominates the rule slack. |
| **G6 — Fidelity to the method as coded/specified** | **PASS** | The D0 score, BB(1,p) prior, centring/standardisation, full-response block tables, absolute-correlation partition, complete flip/swap scans, strict improvement rule, neighbour tie rule, emitted centre, and MR1 cap agree with FAC-B §1, SoP and the inspected production code. The extra scan at the cap and the distinction between scoring and endpoint certification are respected. Delivery includes the total tier-1 fallback, amended resource envelopes, and LS0 preflight terms. No replacement score or changed search is used. |

## Round-1 required item and dispositions

**R08 issue 1 is fixed in substance.** `REPORT.md:106` now explicitly distinguishes the posterior inputs from X4.6's need for a residual-variance floor after conditioning on the large visited models, including one-move enlargements for swaps. It states that a log-size floor alone does not suffice and records the redundant-truth obstruction. This matches X4.6: its truth residual is bounded below using the available full-design floor, not a log-size condition.

I checked the obstruction independently at the linear-algebra level: for a truth equal to the normalised sum of m orthogonal null columns, the correlation matrix on that truth and q nulls has minimum eigenvalue 1-sqrt(q/m), while the truth residual given all nulls is zero. Thus the repaired distinction is necessary, and the theorem's own CS-iid hypotheses do supply the stronger floor. Nothing in the repair adds an unstated hypothesis to FAC-CS-iid.

The other round-1 dispositions are present: the Gaussian-row ingredient now carries the provenance of iid Gaussian xi and sign symmetry; Gaussian noise has its actual separate uses; unequal diagonal idiosyncratic variances and the near-CS extension are labelled Target 2/outside this verdict; `STATEMENT.md:71` specifies C0=6 C_X with C_X=C_X(rho); the eigenvalue attribution is Davidson–Szarek; the four-row end-phase audit table has been added; and the extreme-rho exact-perturbation evidence is identified as numerical evidence. None of these changes supplies a substitute for the proof checks below.

## Independent adversarial proof checks

**X1: exact representation and production-score corrections.** Conditional Gaussian coordinates in the noise/factor frame give the claimed mutual independence, including xi independent of W. Sherman–Morrison gives RSS_T=||e||²/(1+q_T); the Schur identity gives q_T-q_(T-j)=omega_j². Column standardisation preserves the projection spaces but not the ridge score, and X1.4 correctly controls the latter separately. I re-derived the determinant increment, ridge partial statistic, deletion multiplier, addition factor, and reference swap identity. The swap's multiplier ratio depends on the q values as stated; the ridge and determinant remainders are small enough for the later comparisons.

**X2: adaptive sets and the exponent restriction.** D5 unions over a xi-measurable interval family while W is independent of xi. A path-selected T is not treated as one of those independent Gaussian sums: its symmetric difference from the interval-complement reference is paid for using the entrywise Wishart bound and the band count. The resolvent's common first-order part, coordinate part, second-order remainder and normalisation error fit the stated estimate. In particular, p^(3/2)/n <= sqrt(p/n) uses p<=sqrt(n), which follows here. Feeding D6 into the estimate requires p Hbar sqrt(log n/n)->0 and Hbar(log n)^(3/2)/(sqrt(n) varpi)->0; the strict exponent and the floor supply both. The exceptional-set allowance covers all statistics used by the swap comparisons.

**X3: crossings and prefixes.** I checked both cases of the crossing proof: the bound is on d_i, not necessarily the side opposite the deleted point. The general constant 2+4/(kappa-prime-1) handles the final small kept sets. The narrow-phase counting contradiction uses only the established prefix. Since Q<=|K0| and kappa-prime>1, its denominator is positive. Non-crossing endpoint monotonicity and the 4.1-to-4.3 slack give the stated containment. Sparse-case spacing excludes overshoots as well as crossings.

**X4: induction, bulk and end phase.** I checked the dependency order rather than assuming that every approximately greedy deletion path is already the production path. Prefix geometry supplies the perturbation bound, then the candidate rule, then the gain comparisons identifying the actual move. D7 controls the adaptive band contribution in B3; B1 uses the previous centre bound, and B2/B3 then close at the current state. Bulk swaps are bounded through an addition at T-j with the enlarged exceptional set, not through an unproved no-addition statement on all structured sets.

At end-phase entry, D7 places the finite band endpoints in the separated extreme tails; D8 then eliminates the band defects. The sign/separation invariant also covers one-sided configurations. At each subsequent state the best-deletion candidate can be tested hypothetically before being identified with the chosen move. The four transferred FAC-B L4.4 comparisons remain valid with tau-hat: the quadratic errors are O(Hbar varpi+varpi²+Hbar^6/n+1/n)=o(1). For swaps with |I|>=2, use E-del's stronger half-log-n deletion bound; for |I|<=1, the swap bound is o(log n) and c_D>0 suffices. The truth-move proof separately uses the full-design floor and a projection bound uniform over the large conditioning sets. It does not need (FS).

**X5–X6: partition, posterior and delivery.** Conditioning on Z=X^r is essential and is done explicitly. The finite population partial-covariance list is uniformly separated by (FS), while zero pairs have exactly zero signal and occur only in the single block containing all truths. Their two-sided conditional Gaussian bound is over a bounded number of pairs. The sample scales and signal energy are controlled with common constants. The resulting fixed-design instances satisfy every T03-sharp hypothesis, including the anchored eigenvalue conditions and a common beta-min envelope. The every-sequence contradiction justifies the uniform conditional expectation limit; boundedness of posterior error justifies convergence of its expectation without asserting an expectation rate.

[OP] bounds D_n in the direction used. Delivery uses the directly proved discovery event K_n together with D-prime's scored-set inclusion, rather than inferring discovery from D_n->0. Lemma S's nonconstant-input and positive-Q arguments extend conditional on the raw design; A2's resource and exit arguments need no CS-specific statistical assumption. All extra allocation and fallback premises remain attached to the conclusion.

## Source and method verification

The source qualifications retained in this verdict are:

- FAC-B Theorem FAC-CS and FAC-A Theorem FAC-L: **"PROVED-CHECKED"** at package level. Their individual proof files retain their author/check labels.
- T38-(0): **"PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))"**.
- T03-sharp: **"PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"**.
- [OP]: **"PROVED (by this seat, unchecked)"** inside the checked GEN package.
- CAP: **"PROVED (by this seat)"**, with its recorded council checks.
- Lemma CR: **"PROVED (by this seat); XF VERIFIED (R19, Codex gpt-6.1-sol)"**.
- F-GROW: **"PROVED (A2), checked by A3"**. Proposition F retains A1's corrected allocation, A4's subsequent preflight qualification, and the original code-reading audit qualifications. These are not upgraded into binary implementation guarantees.

Read sources include FAC-B STATEMENT and L1–L5; FAC-A L5; CR; FINAL s3, s6 and s7; A2; SoP's D0/shared premises and local-search specification; and the Wave-2 protocol and inherited protocols. I also inspected production `cpp/v3_score.h`, `cpp/v3_engine.h`, the LS0 integration in `cpp/v3_core.cpp`, `v3_fit.R` preflight and `v3_calib.R` fallback. The search, integration and preflight files have no diff against `4676af6`. The specified ideal-arithmetic and operational premises are still premises, as the theorem states.

## Independent computational falsification

Python 3.13 was run through stdin in `reviews/R13_scratch/`; no numerical script or output file was written, and no ticket scorer was imported. These checks test algebra and deterministic geometry, not the asymptotic event probabilities.

1. **Raw-row identities:** 12 fresh centred Gaussian designs, p=6, n in {75,160,340}, rho in {0.002,0.1,0.65,0.995}, with two nonzero raw coefficients. Exhausted all 16 models containing the two truths in each design: **192 model checks, 384 null-deletion edges, 576 null swaps**. Compared direct projection RSS with the representation, Schur differences, exact production-score deletion and swap gains, and reference swap algebra. Maximum discrepancies: rotation 1.34e-15, relative RSS 2.49e-15, Schur 3.54e-15, deletion gain 2.98e-13, swap gain 2.38e-13, reference identity 2.67e-15. **No violation.**
2. **Adversarial soft gaps:** 20 seeds and kappa-prime in {1.01,1.2,2,7}; 600 distinct coordinates per run, including a deliberately tight central cluster and separated outer coordinates. Verified X3's initial-density hypothesis, then repeatedly chose the farthest eligible deletion under R_varpi. Across **80 full sequences, 48,000 steps and 80 actual crossings**, checked crossing-distance/width inequalities, non-crossing endpoint monotonicity and the 4.3-varpi containment. The X3(vii)–(viii) prefix hypotheses apply through the state with two remaining points; the last two deletions were checked additionally as direct geometry. **No violation.**
3. **Citation check:** reran `reviews/citecheck.py` without redirecting or changing CITECHECK.txt: **5 OK, 0 MISS**. Status strings and substantive theorem hypotheses were checked separately against the sources above.

## Numbered issues

1. **MINOR, presentation — NOT REQUIRED for a pass.**

   **Location:** `lemmas/X4_path.md:267`, the new audit table's E-swap row.

   **Issue:** The row juxtaposes the swap upper bound 8 epsilon_b log n for |I|>=2 with only the deletion lower bound c_D log n. Those two displayed bounds alone do not establish dominance uniformly in fixed rho: for s0=1, c_D can be smaller than 8 epsilon_b. The actual proof is sound because E-del at line 249 gives the stronger half-log-n bound whenever I is nonzero, and the surrounding E-swap argument invokes FAC-B's correct case split. The table should display the same split to make its advertised margin independently auditable.

   **Fix:** In that row compare |I|>=2 swaps with G_del >= (1/2-o(1)) log n, and compare |I|<=1 swaps with G_del >= (c_D-o(1)) log n. Keep the existing o(log n) terms where applicable. This changes no statement or proof conclusion.

**Required fixes: none. Score: 9.2 / 10. G1–G6: PASS.**
