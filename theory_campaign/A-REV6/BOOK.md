# A-REV6 bookkeeping review and candidate repairs

Reviewer: GPT-6 Astra, 2026-11-02. This is a source/proof review, not adoption. Every original status below is preserved. New proofs are **Astra-authored candidates**, not changes to the locked register. No numerical workload was run, locally or remotely; later saved numerical claims are read as source reports, not independently certified here.

## Sources and scope

Read using `git show` on the following immutable branch heads:

| Ref | Commit SHA |
|---|---|
| `origin/theory/A-REV4` | `b95948c3f350a225647f110937c3dea403b8443a` |
| `origin/theory/W2-BOOK` | `57eb3d0f6699d76c0796e8b389415dacb182c231` |
| `origin/theory/W2-T26` | `0e4f1e7f5efd1e67330affa4168b69750eaff2f1` |
| `origin/theory/A-DRAFT` | `dbf47f7abfe9940ec7914f89bbe5f28071ad9871` |
| `origin/theory/W5-LOCKBOOK` | `a65392bffd4594fff57842287c56ff1ad743064e` |
| `origin/theory/W7-SEC` | `7e33e8a16f4ad0bbbd91f9b125ac885350027971` |

Principal files: A-REV4 `REVIEW.md` (including its final exact-branch correction) and `BOOK_CHECK.md`; original W2 `PROOF.md`/reports; A-DRAFT `REPORT.md` §2; W5 `REPORT.md`, `AUDIT.md`, `PROOF.md`, `STATEMENTS.tex`; W7 `REPORT.md`, `PROOF_T33.md`. W5 task instructions and W7-SEC task instructions were read. Local source was used to inspect `v3_runtime.h` and the output assembly in `v3_run.R`; neither was edited. This report does not review all of T05 or independently certify T33's numerical constants or cited backward-error theorems.

VERIFIED means an implication checks under its explicit hypotheses, never that a candidate has been adopted. ERROR denotes a false assertion; GAP denotes a missing proof, scope condition or validation. “Repair verified” describes the replacement only and does not erase the original finding.

## Original versus repair verdicts

| Original item and A-REV4 finding | Later repair/evidence | A-REV6 disposition |
|---|---|---|
| T26 Lemmas 1–3: VERIFIED | W5 §R2 confirms terminal-prefix use of T12(i.b) and fresh-round departure argument | VERIFIED conditional mathematics; original candidate status retained |
| T26 fully written A and conditional B: VERIFIED | W5 retains realised-T premise and exact-branch clause | VERIFIED with all idealisations, feasibility, P1 and P1-ex; no masked-start or completion result |
| T26 “p≥18,n≥22 implies no exact branch”: ERROR (A-REV4 §7) | W5 repeats the original premise-scan interpretation; no valid replacement sufficient condition supplied | ERROR remains; use actual combinatorial branch criterion |
| T26 single-SMC-premise shorthand: GAP | W5 Thm 6 retains P1-ex | Repaired statement verified; shorthand remains GAP |
| T26 ORTH Proposition C: GAP / PROOF SKETCH | W5 explicitly retains sketch; A-REV4 supplies chi-square detail | Proposed proof can close missing detail, but original remains sketch and cannot cover p>n−1 |
| BOOK RO: VERIFIED with potential-value sign/bounds and output projection | W5 RO still writes expectation for “g≥0” without spelling out potential nonnegativity | Candidate repair R1 below makes hypotheses exact |
| BOOK literal GUARD: ERROR; same-arithmetic statistical interpretation statically checks | W5 narrows to statistical outputs and lists all stop sites, partial HPM/archive exceptions | Substantive repair; exclude allocation and all operational metadata explicitly. No replay validation supplied here |
| BOOK Prop 2 island identity/covariance: VERIFIED | W5 confirms four diagonal/twelve off-diagonal terms | VERIFIED at fixed data, frozen calibration, potential islands; never pooled-product unbiasedness |
| BOOK Prop 2 fixed-data convention: GAP | W5 still lacks explicit fixed-data convention in paper fragment | GAP persists in integration; R2 supplies exact conditioning |
| BOOK exact-branch extension: GAP | W5 corrects zero contribution to failure event, but keeps `E[1_O Zhat]≤Z P(A)` with A SMC-only | **ERROR in W5 replacement**: exact evidence is positive on exact outputs; R2 separates branches |
| BOOK “completed wrong HPM implies posterior miss”: ERROR | W5 certificate changes to an exactly scored strict competitor | Replacement certificate verified; original implication remains ERROR |
| BOOK size-prior ceiling: VERIFIED for tie-aware maximiser criterion | W5 Prop 1(iii) additionally calls any same-size `m(S)≥m(S0)` an unrepairable error | **ERROR in that paraphrase** at an equal likelihood where S0 wins tie order; R3 repairs |
| BOOK VAL-FP: GAP operationally; scalar-contract implication VERIFIED | W5 demands exact calibration/status agreement; W7 constructs exact final comparator on fp calibration | W7's comparator idea is sufficient under exact-start/frozen-schedule hypotheses. Its score-error/log-recursion constants and useful exceptional probability remain unvalidated here; R4 gives clean sufficient contract |
| BOOK numerical provenance/certification: GAP in source | A-REV4 records Owls reproduction; W5 reports higher precision independent reproduction | Recorded high-precision enumeration is corroboration, not interval-certified real arithmetic; W5/W7 results are not newly reproduced here |
| BOOK output split T11/T14/T15/T25/T31/T34: VERIFIED with scope | W5 identifies returned incomplete HPM/partial archive and restricts T23(ii-d) to SMC | Correct repair direction. Must treat aborts/no usable HPM as no output; retain exact-branch error term if combining branches |
| A-DRAFT §2 A/A1: VERIFIED | W5 stream audit supports ideal conditional independence despite sequential reads | VERIFIED LLN/MSE and islandwise numerator identities; no T16 CLT/status upgrade |
| A-DRAFT §2 D/D1: VERIFIED | W5 confirms T26 machinery; A-DRAFT's sharper occupancy proof is independent | VERIFIED with bounded h, data-measurability, P1/P1-ex, OUT; continuous generating-value claims additionally need contraction and uniform continuity |
| W5 T32-a deterministic evaluation count | W7 independently confirms, corrects one slack arithmetic inequality | Candidate count supported by loop accounting; no source adoption |
| W5 T32(c) `O(max(n,p)p log²(n+p)+p²log²(n+p))` | W7 confirms without detecting calibration-iteration factor | **GAP in stated rate proof**, repaired to log³ for calibration contribution in R5; polynomial conclusion survives |
| W7 score margins/VAL-FP deployment claims | T33-H uses common scored set; T33-Z ε is explicitly vacuous at study budgets | Common-set margin implication verified under validated per-score envelopes. Production path agreement and libm/backward-error constants are not established by this review |

## R1. Projected stop-only coupling and RO (Astra candidate proof)

Define a projection P of the returned record onto explicitly chosen statistical estimates, scored-model/discrete algorithm records and their availability indicators. Exclude allocation, elapsed times, memory readings, guard records, cache-performance timings and every hardware/load-dependent diagnostic. The potential record is the **same arithmetic algorithm** with operational preflight/guard stops suppressed, driven by the same data and ideal random streams. It is not the exact-real comparator unless the actual algorithm already uses exact arithmetic.

Assume every check either leaves the projected state unchanged or terminates the fit, and untriggered checks consume no randomness. Induction over the executed instruction sequence gives equality of projected states until the first terminating check. On no-stop paths, actual and potential projected records agree through completion. W5's inventory C1–C7 and the `check` source support this assumption statically: the check updates clock records/sticky exceeded status; an untriggered check does not change particles, RNG state, schedule or score cache. A same-seed replay would test implementation behaviour; it is not a substitute for this qualification.

Let G include operational stops and any aborts for which no usable output exists. For a selected statistic let Obar be its potential availability event, define actual availability by O=G^c∩Obar, and exclude incomplete HPMs/partial archive statistics from this definition. If a non-guard abort requires separate treatment, use G=G_guard∪G_abort rather than equating G to the returned resource status. On O, g=gbar. Thus, for every measurable B,

`P(O,g∈B) ≤ P(Obar,gbar∈B)`.

If gbar is nonnegative on **all of Obar**, extending both statistics by zero outside their availability events gives pointwise `1_O g ≤ 1_Obar gbar`, hence the expectation inequality. Actual nonnegativity only on O is insufficient. For signed bounded statistics use the event inclusion for error bounds or an absolute-value statistic; do not assert expectation monotonicity for signed g. Conditional error probabilities are bounded by the corresponding joint bound divided by P(O)>0; conditional unbiasedness does not follow. This establishes the corrected RO without any independence or small-probability assumption on G.

W5's incomplete HPM and `partial_final` observations are essential: `v3_run.R` assigns HPM before the non-completed early return, but assigns official evidence/PIP fields only afterward. Thus “no partial **official estimate**” checks; “no returned partial value” is false.

## R2. Fixed-data Prop 2 with exact-branch accounting (Astra candidate proof)

Fix data D. Let A be successful SMC calibration; E be the exact branch, disjoint from A. Let C include all calibration-dependent schedule/algorithm settings and inherited records, and assume exact final start draws, invariant kernels, ideal independent final streams, exact arithmetic and the locked frozen-run identities. For potential island variables Zr,Pr, conditional on D,C,A,

`E Zr=Z(D)`, `E[Zr Pr]=Z(D) p_j(D)`.

The four islands are iid conditionally on this sigma-field. Set Zbar=(ΣZr)/4, Pbar=(ΣPr)/4 and μ=E Pr. Expanding sixteen terms yields

`E[Zbar Pbar]=(1/4)Zp_j+(3/4)Zμ`,

so the difference from Zp_j is `−(3/4)Cov(Z1,P1)`. The unbiased numerator is `(Σ Zr Pr)/4`; neither normalised Pbar nor pooled-product Zbar Pbar is asserted unbiased.

Let O_S=O∩A and O_E=O∩E. Define potential SMC evidence only on A. By R1 and nonnegativity,

`E[1_(O_S) Zhat | D] ≤ Z(D) P(A|D)`.

On exact outputs Zhat=Z(D), so the full-output expectation instead satisfies

`E[1_O Zhat | D] ≤ Z(D){P(A|D)+P(O_E|D)}`.

This directly refutes W5's unchanged full-output expectation with SMC-only A: take data for which enumeration is used and completes surely, giving left side Z>0 and proposed right side zero. Alternatively define Astar=A∪E and use the weaker bound `Z P(Astar|D)`. One must say which convention is used.

For 0<α<1 exact outputs contribute **zero to the failure event**, so Markov gives

`P(O,α Zhat>Z(D)|D) ≤ α P(A|D)`.

That zero-event contribution must not be confused with zero contribution to the evidence expectation. Under joint data probability integrate the event bound; the expectation formula becomes `E[1_O Zhat] ≤ E[Z(D){1_A+1_(O_E)}]`. Z is not pulled outside the expectation over random data. Jensen's log bound concerns potential evidence conditional on D,C,A, where positive finite state-space factors provide integrability. It is not a completion-conditioned bound.

The exact branch is determined by its actual budget/state-count inequality. The original p≥18,n≥22 parenthetical fails: p=18,n=2^18 has K=p, 2^18 states, and a threshold at least 4np>2^18. Enumeration is selected. Keeping P1-ex is therefore necessary even along some fixed-p large-n sequences.

## R3. Tie-aware size-prior certificate (Astra candidate proof)

On finite Ω with positive marginal likelihood m, let S*_k be the tie-order-first maximiser among size k. A positive size-only prior can select S0 as global tie-broken HPM iff S*_(s0)=S0. Necessity follows because the size multiplier cancels within that layer, including tie order. For sufficiency give size s0 multiplier 1, all others ε>0 smaller than `m(S0)/max_Ω m`; all other layers then score strictly below S0, and the within-layer tie rule selects S0.

An equal-likelihood same-size competitor does not defeat S0 when S0 precedes it. Hence replace W5's `m(S)≥m(S0)` paraphrase by “strictly larger likelihood, or equal likelihood and a competitor preceding S0 in the prescribed tie order.” In data use a validated interval: if `Fhat(S')−Fhat(S0)>e(S')+e(S0)` for same-size S', with actual rigorous envelopes e, the exact score is strictly larger and no size-prior retuning recovers S0. A heuristic engine error field is not such an envelope. Completion alone supplies no posterior-miss certificate: a scored set containing only a lower-scoring wrong support can miss a uniquely optimal S0.

## R4. VAL-FP comparator and sufficient transfer contract (Astra candidate proof)

Fix stored data D, and let C_fp be the complete calibration object computed using streams 0–9. On successful fp calibration A_fp, construct an auxiliary exact final SMC run using that frozen object as algorithm settings, **recomputing exact target/start probabilities and exact start normaliser from D**. Its start sampler must draw from that exact π0; merely reusing fp categorical probabilities would not satisfy START. The selected grid is allowed to be any valid finite increasing grid ending at one and the frozen final kernels must be invariant for their exact intermediate targets. Verify those properties rather than assuming arbitrary fp output is admissible.

Under these hypotheses C_fp is independent of streams 10–13, so conditional on D,C_fp,A_fp the auxiliary potential evidence Zex has mean Z(D). The whole exact calibration need not match the fp calibration or its status: only the auxiliary frozen final algorithm must meet T12. This is the useful part of W7's proposal and avoids W5's stronger sufficient condition of complete calibration replay agreement.

Suppose deterministic η≥0 and an event H satisfy

`P(O∩H^c | D)≤ε`, and on `O∩H∩A_fp`, `Zfp≤exp(η) Zex`.

Then event inclusion and conditional Markov give

`P(O∩A_fp, α Zfp>Z(D)|D) ≤ α exp(η) P(A_fp|D)+ε`.

If η is calibration-dependent the correct term is `α E[1_(A_fp) exp(η(C_fp))|D]`, or use a uniform deterministic bound. For exact-branch **floating** evidence add its separate failure probability or a validated exact-enumeration error envelope; it is not automatically zero as in R2's EX-A case. The scalar inequality is sufficient; path agreement is only one way to establish it. Score accuracy on a common scored set alone does not establish it or equality of sampled paths.

W7 T33-Z supplies a path-agreement strategy and explicitly concedes a vacuous useful ε at the study budgets. This review does not certify its detailed constants: libm assumptions and cited Cholesky success constants are admitted escalation items, and grid-valued production uniforms must not silently replace continuous EX-S uniforms while retaining exact categorical/invariance identities. Separate a continuous ideal comparator, finite-grid perturbation and all rounding terms explicitly if using that bound. Replays can estimate path-disagreement frequencies with confidence intervals; finite samples do not prove a distribution-free ε for all data/calibrations. No validated deployed VAL-FP parameters are established here.

## R5. T32 count and corrected asymptotic corollary (Astra candidate proof)

W5's T32-a adds the identifiable costs: block tables; one pilot and at most 4ℓ diagnostic islands per tier; at most two tiers; four final islands; ≤2ℓ+3 local searches; V rebuild and inherited-model rescores. A round evaluates at most m=p+B+2 new/proposed models; held Gibbs states are logical events, not additional evaluations. At most ℓ+1 full local-search scans follow from scanning before the move-limit test. These arguments support the count in the exact-arithmetic scope stated by W5. They neither give wall-time bounds nor adopt arithmetic/storage claims.

But its asymptotic proof drops `(1+4ℓ)` in the island term. Put q=n+p+1 and M=max(n,p), absorbing the fixed lower budget 2500 into constants. Then H_e=O(M), m=O(p), T_e=O(log²q), L=O(log q), ℓ=O(log q). Therefore

`Σ_e(1+4ℓ) H_e [1+m(T_e+L+4)] = O(M p log³q)`.

Final islands cost O(Mp log²q). Local searches cost O(p²log²q), because their number and scans per search each contribute one log factor; rebuilds cost O(p log q), tables O(p) since B≤16. Thus the directly proved corollary is

`C_eval = O(M p log³q + p²log²q)`.

Under p≤n^A, A≥1, this is O(n^(2A)log³n), still polynomial. The smaller log² claim is not proved by this count; an additional amortisation argument, absent from W5/W7, would be needed to improve it. Also fix W5's slack step `1+4ℓ≥5ℓ` to `1+4ℓ≥4ℓ`; W7 correctly detects that slip. W7's fp pilot addendum has additional floating-step hypotheses and is not needed for this EX-A corollary.

## A-DRAFT §2 independent boundary check

The fixed-data theorem uses finite Ω and positive potentials: reweighting is Lipschitz, multinomial resampling plus independent mutation gives conditional empirical variance O(1/N), and finitely many stages preserve the bound. A random-order pre-label kernel is a state-independent mixture of products of invariant kernels. Sequential consumption of one iid stream per island gives the same conditional laws by the fresh-tail property at finite stopping times; it does not assert that actual xoshiro output is iid. Theorem A/A1 remain candidate LLN/MSE and unnormalised-identity results, not a CLT.

For D write W=Zhat/Z and X=η(S0^c)∈[0,1]. T12 gives E_C(WX)=δ, whence E_C X≤δ+E_C|W−1|. This proves the reported occupancy sharpening and, for |f|≤M, E_C|ηf−πf|≤2M(2δ+b). Reapply at each measured-round start, then pay one round's departure probability ≤(B+3)δ/(1−δ); no accumulated L factor is necessary. Under `(T+1)Δ→0` on successful SMC calibration and the exact-branch δ clause, Markov and output intersection prove the stated consistency. The argument does not prove either premise for masked starts or P(output)→1.

Weighted conditional parameter draws need vanishing squared weights; A-DRAFT proves this using m0/N→1 truth copies and v_out→0, giving Σw_i²≤1/m0+v_out². Exact enumeration instead uses integrated conditional expectations. D1 needs posterior contraction and uniform local continuity; the equality-indicator counterexample correctly excludes all bounded-measurable generating-value consistency. These qualifications remain essential after the bookkeeping repairs.

## Integration status

Retain the original A-REV4 verdicts and append the repair verdicts above. The core conditional mathematics survives. Do not import W5's literal full-output expectation or tie paraphrase, its unproved log² cost rate, W7's numerical-failure deployment headline, or an operational VAL-FP guarantee into the paper without their separate obligations. No locked theorem, methodology, engine source or historical run snapshot was changed by this report.
