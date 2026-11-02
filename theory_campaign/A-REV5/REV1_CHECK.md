# Independent check of the A-REV1 repairs and their downstream interfaces

Date: 2026-11-02. Read-only source review; no simulations, benchmarks, or numerical experiments were run. This review writes only this file. Source statuses below are quoted statuses, not promotions to locked or adopted results.

## Sources and scope

| Remote-tracking source | Inspected commit |
|---|---|
| theory/A-REV1 | 26815e841f25cd472a20f8ea251c00b4ffab3e37 |
| theory/W6-FIXREV1 | a7833f3d185d188ca48c7cb4a12faf4397ac63de |
| theory/W4-T38FULL | a0f9cb5e000dedf367e26fd0da019ccd2218fb42 |
| theory/W3-PXN | 4aebea3bf003f5f3c0c7239a24c824ec2d2aa574 |
| theory/W3-PGD | fdeaec34f5a23ced83ccd85b5bf00ee643cbcba0 |
| theory/W2-T26 | 0e4f1e7f5efd1e67330affa4168b69750eaff2f1 |
| theory/F-REFINE | db708ca9f98a616ea16c8ce8e950d8f65238835f |

Read A-REV1 REVIEW; all four W6-FIXREV1 Markdown deliverables; relevant downstream statements/proofs and F-REFINE architecture/cards. Cross-checks used METHODOLOGY_v3, 00_COMMON, LOCKED_PROOFS, and C++ v3_runtime.h, v3_engine.h, v3_ledger.h and the relevant v3_core.cpp call sites. This is an independent check of the REV1 repairs and their propagation, not a new audit of every locked proof or every statistical lemma on these branches. In particular the separate W3-PXN and W3-PGD candidate packages are not promoted by this report.

## Verdicts

**The central A-REV1 repairs in W6-FIXREV1 check as conditional implications. The downstream package still contains an ERROR repeating the missing q<1 condition, an ERROR in the exact-branch example, and statement/proof qualification GAPs.** W6's report says candidate, not adopted, and not reviewed after its edits; those provenance labels remain true of the source version.

| Item | Verdict | Checked substance and limits |
|---|---|---|
| CONSOLIDATED §1 Proposition U′ | VERIFIED | Bad(W) restores all three tests; truth removal is charged for every label. The extra-for-extra phase-1 obstruction is exactly replacement of look-alike by junk at the full junk budget. In the shrinking family, the missing set stays fixed during this swap, so the same calculation applies with current look-alikes. |
| Independence acceptance bound | VERIFIED | Multiply the MH factor by pi0(S′), then bound termwise by pi0(S′) and by pi(S′)pi0(W)/pi(W); sum over the full corrected Bad(W). |
| Theorem B unaffected by the bookkeeping shortcuts | VERIFIED with original qualification | The proof uses the full bad definition, not the false shorthand. A-REV1's finite result is VERIFIED after F′; no statistical premise or delivery follows. |
| CONSOLIDATED §2 beta_H conventions | VERIFIED | Empty phase, empty supremum, nonpositive progress, zero horizon and truth-at-start cases are supplied; capping makes the product interface legitimate. x=S0 must already have been scored, as it is at the terminal boundary used here. |
| B-M and IND-T boundary | VERIFIED | Select by the past; independent future ideal streams/blocks give conditional product laws for uninterrupted trajectories. H′=L+5 is used before the stage-T round; H=L+4 after it. Global first-fresh sets are excluded. No future completion event is conditioned on. |
| CONSOLIDATED §3 multi-target P | VERIFIED | Earliest label in C union D is Good with probability at least s_min |C|/(|C|+|D|). Its arrival time has mean 1/(|C|+|D|+1); the outside-label union bound supplies the printed factor. q_j includes Good-or-change killing, so requiring no outside killing is sufficient even when a Good evaluation leaves the state unchanged. |
| CONSOLIDATED §4 S′ | VERIFIED | Cauchy-Schwarz bound with clipping at zero; positive two-level equality requires f>1-e. Below or at the threshold, weights epsilon on A and 1 off A approach zero share while preserving ESS. Endpoints f=0,1 and e=1 are covered. |
| CONSOLIDATED §5 D2-infinity | VERIFIED as implication | Fixed b0>0.1, bounded dangerous count, Dep bounded below 1 and vanishing NB′ failure kill both exponentials. The general rates explicitly require Ht² and H beta g to diverge. Convergence of bounded capped failures in probability gives convergence of expectations; no conditioning on eventual calibration success is used. |
| CONSOLIDATED §6 E3′ | VERIFIED | q<1 is restored before applying locked T22(i-a); centre emission and completed scans are explicit; cost includes the centre. T27-H3 is correctly retained as an assumption. |
| CONSOLIDATED §7 U constant | VERIFIED | Expand (1/2+0.01/n)(1.02+phi0^-2/n): constant is 0.51, with positive 1/n and 1/n² terms. The decreasing bound and the printed sufficient n1 follow. Family count must include the span with S0 and deterministic envelopes for y-selected families. |
| CONSOLIDATED §8 NL0 quantifiers | VERIFIED as correction | Sum over labels of state suprema is the required quantity; the diagonal array separates it from sup of the sum. PG(a) and the connected-set multiplicity are genuine additional inputs, not consequences of finite B. This check does not independently certify W2-PREM's CMP theorem. |
| CONSOLIDATED §9 CE1-narrow | VERIFIED as the stated candidate implication | The exact Gram sequence exists for large n; Y has d extras and no truths, so Q_T=0; adding proxy 2 exits the original region and has deterministic signal gain r²theta1²(n-1). Fixed-family U(C5) makes its odds exponential. B≤16 and L diverging then refute vanishing uniform exit on this sequence. This is not universal failure for correlated designs. |
| T38 composition (0), (0_H) | VERIFIED under stated GUARD/EX-A and output definitions | Strict output transfers to the potential completed/exact output. Truth scored plus posterior mass>1/2 implies the running best is truth. HPM convention adds the schedule-limit discovery term; guard-partial HPMs are deliberately excluded from both output events. |
| T38 b1′ repair | VERIFIED as conditional rate interface | The potential first pilot is present before later calibration rejection; therefore its failure bound controls both strict and schedule-limit discovery. The masked instance remains PROOF SKETCH because NB′ is unproved. |
| T38 b2 repair | VERIFIED as conditional interface | Eligible set carries actual feasible certificates; minimize beta by a past-measurable index and use the Markov part of IND-T, or use the product part. DELIV remains OPEN. Mere membership in R_d is insufficient. |
| D3(X), T38_PROOF §5.2, printed conditional bound | GAP | SHARE is printed as an unconditioned probability, while the conclusion conditions on calibration C and uses data-dependent pi0(X). The proof requires SHARE/EXIT stated conditional on (data,C), or an unconditional integrated conclusion. See below. |
| T38 part (c), theorem wording | GAP in qualification | Proof §6 says “PROVED UNDER T32(i) (CONJECTURE)”; dependency row k1 says CONJECTURE. Main theorem (c) presents the ceiling without that qualification, and T32 is absent from its standing assumptions. Retain the conditional label or supply an independent complete counting proof. |
| F-REFINE Card 3(i) | ERROR | Omits q<1 in the same mass bound repaired by REV1. Explicit counterexample below. |
| W2-T26 exact-branch example | ERROR in ancillary assertion | “p >= 18 and n >= 22” does not exclude enumeration as n increases. Explicit counterexample below. Main Theorem A separately retains P1-ex. |
| T38 b1-LH masked iid-draw budget clause | ERROR as unqualified component assertion; GAP in branch qualification | For c=2, p->infinity alone need not make Qf pi0(S0) vanish; slow p and actual enumeration must be distinguished. See below. |

## Errors and remaining omissions

### 1. F-REFINE repeats the repaired E3/T22 error

`theory_campaign/F-REFINE/CARDS.md`, Card 3, refined statement (i), says: “The composite start puts mass >= (1-q)^{s+1}/(1+e)^s on any feasible reference model S°” without q<1. This is the exact missing premise identified by A-REV1. W6 CONSOLIDATED §6's downstream table covers W1-T38E, W4, W3-PXN and W2-BOOK, but does not catch F-REFINE.

The existing A-REV1 analytic/model counterexample applies verbatim: n=20,p=2, centred orthogonal columns, y=x2, singleton blocks, reference {1}, s=1. The method's table gives q=r2 approximately 1.9355e12 and e=4/r1 approximately 17.8885. The printed expression is approximately 1.9833e23, while the reference start mass is approximately 9.4416e-14. A probability cannot obey this claimed lower bound. No new computation was needed: this is the source's own saved counterexample and its algebraic consequence.

**Repair:** add 0<=q<1 before the deterministic lower bound in Card 3(i), and propagate it to any paper restatement. Source status “locked T22(i)(ii)(iv)” cannot justify dropping a locked hypothesis. The actual W3-PXN P3 proof explicitly says “if q<1”; P5 uses the >1/2 mass event and E3(i), so these particular PXN uses do not inherit the omission.

### 2. W2-T26 has a false enumeration example

`theory_campaign/W2-T26/PROOF.md`, Theorem A's (P1-ex) parenthesis and §3 “Exact branch hypothesis”, offer p>=18,n>=22 as a regime where the exact branch fails. This assertion is false. Fix p=18 and take n=2^18. Then K=p, so the enumeration count is exactly 2^18. The threshold is (5H0+4N0)p, with N0>=n, hence at least 4np=72n, strictly larger than 2^18. The method therefore enumerates. More generally, for every fixed p the count is bounded by 2^p while this threshold diverges with n; enumeration eventually applies.

This is symbolic arithmetic, not a computational validation run. The counterexample does not refute Theorem A because (P1-ex) is explicitly assumed there. It does refute using that parenthetical to remove (P1-ex), and it matters because P1 is vacuous on the exact branch. **Repair:** delete the numeric threshold example; require an actually sufficient growth condition for eventual nonenumeration, or retain P1-ex, as the theorem already does.

W2-T26's principal source labels remain: Theorem A “PROVED (composition; all inputs locked)”; Theorem B “PROVED as a composition” conditional on the named start/posterior inputs; ORTH Proposition C **PROOF SKETCH**. The REV1 repair does not convert C into a proved source result.

### 3. D3's conditioning is not stated consistently

W6 T38_PROOF §5.2 assumes SHARE as P(A_{t-1} and no eligible resampled particle)<=zeta_t, then concludes a bound for P(A and no terminal eligible particle | C). An unconditional small loss probability does not bound that loss conditional on a particular calibration output; a rare C value may concentrate all losses. Its first term also contains pi0(X), which is data-dependent, so the natural version fixes data and C throughout. This is a missing quantifier/interface, not a BVS counterexample to a correctly conditional D3.

**Repair:** state the SHARE inequality conditional on (data,C), with data/C-measurable zeta_t and the corresponding conditional EXIT bound; prove the conditional union bound and then integrate. Alternatively state the fully integrated bound from the beginning. DELIV must still be proved with the aggregate tending to zero. This omission does not affect b2 when DELIV is directly assumed.

### 4. The c=2 slow-dimension masking claim needs a rate and branch qualification

W6 T38_STATEMENT (b1-LH), inherited from W4, claims Qf pi0(S0)->0 when c>=2 and p->infinity. At c=2 this does not follow from its own stated masking law. Take p_n asymptotic loglog n (rounded to an appropriate multiple of fixed group size); exact Gram exists since p<=n-1. The eventual block-size condition can hold with a fixed group size between 9 and 16, since B eventually reaches 16. Its law gives pi0(S0)=p^-2 n^-1 exp(O_P(1)). For the potential SMC component budget, Qf>=4N_e(L+6)>=4n(L+6), hence

    Qf pi0(S0) >= constant * (log n)/p² * exp(O_P(1)) -> infinity in probability.

The positive tight multiplier does not cure a deterministic divergent factor: its logarithm is O_P(1). Thus c=2 and p->infinity do not suffice for the asserted component limit. This is an analytic asymptotic counterexample, not a numerical experiment.

There is also branch discipline: such slowly growing p is eventually enumerated, since 2^p is polylogarithmic while the exact threshold is at least of order np. A hypothetical final-draw budget should therefore not be presented as an executed production budget on this sequence. **Repair:** identify the component setting or restrict to the SMC branch with a proved relevant growth condition; one direct sufficient rate is n^(1-c/2)p^-c log²n->0, using Qf=O(max(n,p)log²n) in the exact-Gram p<=n regime. At c>=3 with p->infinity this sufficient rate does hold, but the boundary c=2 requires a rate (for example p/log n->infinity is sufficient). This issue does not refute the LS0 discovery implication itself.

### 5. Conditional costs and surviving source statuses

W6 T38_STATEMENT Part II.6 labels T32(i) **CONJECTURE**; T38_PROOF §6 accurately labels its result “PROVED UNDER T32(i) (CONJECTURE)”. The main theorem's part (c) should carry that label. F-REFINE ARCHITECTURE §6 item 11 already warns against promoting the cost corollary to a theorem, so its warning should be retained.

F-REFINE's graph also compresses H24 to “[X]” and §4 says “H24's asymptotic input false”. The precise repaired claim is the failure of the vanishing uniform-exit premise on the explicit CE1-narrow sequence. The locked register still lists H24 as **not proved** and absent from the register, not as a universally disproved premise. W6's narrow wording is preferable.

## Downstream discipline and method compatibility

- W4-T38FULL b1 is explicitly superseded by W6's statement/proof; its old manuscript should not be silently treated as repaired text. W6 incorporates the centre call, rate margins, feasible eligible certificates, matching terminal boundary and output conventions.
- W3-PXN P7 is **PROVED for D2-a,b,c; PROOF SKETCH for D2-d**. Its old NB range still prints 1.925, not the corrected r*. W6's replacement interface uses r* or NB′ correctly, but original PXN numerical/statement text must not be cited as if that edit had been made there. Its final no-method-change conclusion is expressly conditional on the sketch. The old T38(b)-R citation must be read through W6's repaired operational/rate interface.
- W3-PGD Theorem W is **PROVED (candidate)** under PGD and one of H1/H2/H3; its Corollary P6 is “PROVED given a cited concentration bound”. W6 does not discharge those conditions, and CE1-narrow is not a substitute for its separate LD counterexample. F-REFINE accurately marks Theorem W unverified. No blanket cross-family verification of W3-PGD is supplied here.
- W2-T26 is a favourable-regime evidence/PIP result with OUT and realised-stage premise (T+1)Delta->0, not a masked-discovery theorem. Removing the old (L+4)rho* premise uses repeated locked occupancy identities, not a claim of future-completion independence. The exact-branch P1-ex premise remains necessary unless separately implied.
- `RuntimeGuard::check` uses elapsed time/operation duration and updates operational records, without RNG consumption or statistical tuning. The inspected engine/core call sites stop or label partial outputs on exceedance. This supports GUARD as a stop-only coupling for the examined computation; GUARD supplies no probability of completion and is not a floating-point score-validity proof.
- `local_search` scans before testing the move limit, and executes `eval(C, ME_LOCAL, emit_centre)` at entry. The ledger updates stores on fresh score events. Thus centre-first emission (or explicit ledger insertion) is necessary for the LS0 extension; production's false default alone is insufficient for a new unscored centre. Existing callers use already-scored centres. LS0 remains a method change, not an adopted C++ feature in this review.
- Locked T21 supplies the direct scored-plus-ranking set argument, but H24 remains open in the register. Locked T22 requires q<1. T03's T02 closure is regime-specific. None of the finite algebra, candidate repairs, or old numerical checks establishes terminal delivery, NB′ on a masked family, vanishing calibration failure, or vanishing resource-stop probability.

## Disposition

Retain the substantive REV1 repairs as conditional candidate results. Correct F-REFINE Card 3(i), remove W2-T26's false enumeration example, qualify the c=2 iid-draw masking budget limit, state D3's conditioning consistently, and mark the main cost clause conditional on T32(i). Preserve all source labels: **candidate/unadopted**, **PROOF SKETCH** for NB′/masked D2 and Theorem L, **OPEN** for DELIV, and **CONJECTURE** for T32(i). No locked file or source branch was edited, and no source status was upgraded.
