# S1 fidelity review — W3-READER

Reviewed the frozen `READER_VERSIONS.md` (RV), `NOTATION.md` (N), and `CLAIMS_CARD.md` (CC), against the cited masters and the current registry status column. All three SHA-256 hashes match `S1_frozen/MANIFEST_S1.txt`. Theorem 9 was excluded. No source or git state was changed.

The mathematical reductions mostly work. The delivery assembly is incomplete, several quantifiers need repair, and the card loses material qualifications. Findings below distinguish an actual false statement from a hypothesis that the listed reduction does not supply. The literal sign omission in F1 is easily repaired; it does not challenge the intended positive-constant theorem.

## Findings

### F1 — FATAL — Theorem 1: the stated beta-min condition permits a negative constant

**Location:** [RV:45–46, B1.4:94](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:45).

The first alternative says only that a fixed `C_beta` satisfies `C_beta^2 phi_0^2 > c_0`. It never requires `C_beta > 0`. For a negative constant satisfying that inequality, the lower bound on `theta_min` is automatic, and squaring it in B1.4 is invalid. The master instead requires the positive squared-signal lower bound in [POST:74–75](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-POST/STATEMENT.md:74).

For example, take `p=2`, an orthogonal standardised design, `s_0=1`, fixed noise variance, and `theta_1=n^{-1}`. All floors and the coefficient bound hold. A sufficiently negative `C_beta` makes reader (A6) hold, while the signal is asymptotically indistinguishable from zero; its Bayes factor is `n^{-1/2} exp(O_P(1))`, so its posterior probability tends to zero, contradicting the conclusion.

**Minimal fix:** write “a fixed `C_beta > 0` such that …”, or state the squared beta-min inequality directly. With this repair, B1.4 and the headline conclusion are faithful.

### F2 — MAJOR — Theorems 6 and 7: B6.6/B7.4 do not discharge delivery's implementation premises

**Location:** [RV:396 (B6.6)](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:396), [RV:472 (B7.4)](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:472), [N:123–127](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/NOTATION.md:123); conclusions at RV:351–356, 442–445 and CC rows 6–7.

F-UNI requires its **entire** method/premise/allocation paragraph, [L5_delivery:8–13](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave2/W2-UNI/lemmas/L5_delivery.md:8), in addition to (V), (S), (P). S3 states exact score arithmetic, shipped configuration, and allocation preventing the resource guard from stopping the run. These do not supply:

- IDEAL-W (unbounded integer/index/address arithmetic), or EX-A's unit-cost interpretation;
- MACH, including successful allocations/build/dependencies, worker success and absence of external interruption;
- the declared CONFIG restrictions, fixed `R'=4k` and worker count, default summary list and certificate budgets;
- EX-S, SR, GUARD-W, valid declared seed, and the full e4/TDP-IMPL execution/cost contract retained by delivery;
- the explicit memory/time **and preflight** inequalities, including the extra LS0 archive/time terms, evaluated at `(n,p_raw)`.

These are independent operational assumptions, not consequences of a population eigenvalue floor or of switching LS0 on. Their definitions are explicit in [C-DLV:21–46](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave1C/C-DLV/STATEMENT.md:21); the amended allocation and qualifications are in [FINAL s6:29–62](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave1C/FINAL/sections/s6_delivery.tex:29). In particular, “guard does not stop the run” does not exclude an allocation failure or `unsupported_size`. E4 proves a maximiser property subject to its encoding and execution conditions; it does not establish this delivery cost contract ([RM:219–230](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-RM/STATEMENT.md:219)).

What **does** check: (V) follows from the stated positive definiteness / retained nonconstant fixed columns; (S) follows by the union bound; (P) is [POST]. LS0's cap matches, and the tier-1 fallback is indeed default-on ([code:141–144](/home/fb31/BVS-wt/W3-READER/Scripts/SMC_BVS/core/v3_calib.R:141)). These checks alone are insufficient for unconditional delivery.

**Minimal fix:** explicitly incorporate the full F-UNI operational premises and amended allocation as standing conventions, retaining the P1/S.3 “AUDITED (code reading)” qualifications. Restrict seeds/runs to admissible ones and the finite-sample statement to every **admissible `n >= 3`**. Fill in the premise table rather than leaving “Must also check …” as the assembly. Without those additions, retain only the RM2 conclusion conditional on output, with RM's admissibility premises carried.

### F3 — MAJOR — Theorem 6: common uniform envelopes are missing from two population conditions

**Location:** [RV:341–349, B6.2–B6.4](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:341).

In (A4)(ii), convergence is expressly uniform over `v,j`, but no common bound over the growing family of `l,U` is stated. RM2's (L-loc-R) requires **one deterministic** `r_n -> 0` bounding every such covariance ([RM2:182–184](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-RM2/STATEMENT.md:182)). Pointwise convergence for each column/conditioning-set sequence is insufficient for that uniform event.

Likewise “for every `l` … `|N_l|=o(log n)`” does not explicitly require the common cardinality envelope used by (D-loc). The master requires `max_l |N_l| <= nu_n = o(log n)` ([RM:154–156](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-RM/STATEMENT.md:154)). The reference count is `sum_l 2^{|N_l|}`; the needed `log p + o(log n)` bound does not follow from a merely fixed-index interpretation.

**Minimal fix:** require deterministic sets and common deterministic sequences `r_n -> 0`, `nu_n=o(log n)`; bound both locality covariances by `r_n` for **all** `l,U,v,j`, and `|N_l| <= nu_n` for **all** `l`. Then B6.2–B6.4 follow. B6.3's variance proof itself is correct (see checks below).

### F4 — MAJOR — Theorem 5: the deterministic floor loses its size and validity restrictions

**Location:** [RV:289, B5.2:314](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:289).

The reader asserts the floor “for every data set”. FLOOR only gives it for valid data with `n >= 4` and `|S| < K` ([START:241–243](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-START/STATEMENT.md:241)). Fixed `s_0` and `p>s_0` give `s_0<K` **eventually**, not at every sample size. B5.2 itself acknowledges exactly this limitation. This is a stronger finite-sample claim than the listed input supplies, irrespective of the correct asymptotic optimality conclusion.

**Minimal fix:** “For every valid data set with `n >= 4` and `s_0<K` (hence for all sufficiently large `n`), …”. The concentration conclusion and exponent optimality then follow.

### F5 — FATAL — Theorem 3's card statement omits the domain of the universal bound

**Location:** [CC:17 (row 3)](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/CLAIMS_CARD.md:17); related overbroad consequences at [RV:177–180](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:177) and RV:67–68.

The card says “On every design, `pi(S|y) <= ...`” without `|S| <= min(K-1,p/2)`. The primary statement includes this restriction and is faithful. The card's unrestricted assertion is false. Take `n=1000`, `p=2`, orthogonal standardised columns, and `y=(x_1+x_2)/sqrt(2)`. For `S={1,2}= [p]`, `K=2`. Direct substitution in the stated score gives

```
log[2*pi({1}|y)/pi({1,2}|y)] = -3093.827605...
log[pi(empty|y)/pi({1,2}|y)] = -3436.039034...
```

Thus `pi(S|y)` is essentially one, whereas the card's bound is `0.96934657...`. More generally, full orthogonal truth with fixed nonzero coefficients has exponentially small underfit mass, so the unqualified remark “no design gives a rate faster than n^{-1/2}” also needs the domain inherited from (a). The master's consequences explicitly retain that domain ([PSHARP:98–110](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-PSHARP/STATEMENT.md:98)).

**Minimal fix:** restore the size restriction in the card and prefix the consequences with it. Do not turn a sparse-model obstruction into an unrestricted statement over all feasible models.

### F6 — MINOR — Theorem 3: arbitrary lower-bound witnesses need not satisfy the upper-bound hypotheses

**Location:** [RV:179–180](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:179).

“These designs … satisfy the assumptions of Theorems 1–2” is too broad. (N-orth)/(N-gauss) constrain the **null** columns; the truth block can be ill-conditioned, and the signal can violate beta-min. The master supplies particular upper-and-lower-bound witness sequences, not that implication for every lower-bound witness ([PSHARP:79–87](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-PSHARP/STATEMENT.md:79)).

**Minimal fix:** name those witnesses: fully orthogonal designs and fully iid Gaussian designs, with fixed nonzero coefficients and the appropriate dimension ranges; alternatively say “when the corresponding upper-bound assumptions also hold”.

### F7 — MAJOR — Theorem 5's card gives the no-leakage exponent to growing leakage sets

**Location:** [CC:19 (row 5)](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/CLAIMS_CARD.md:19).

The row attaches “for every `c<1/2`” to both mass on `S_0` and mass on the lattice of a set `|Q| <= n^{1/2-epsilon}`. The master and RV:291–294 give only `c<epsilon` in the latter case ([START2:136–139](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-START2/STATEMENT.md:136)): the displayed bound has the factor `|Q|+1`.

**Minimal fix:** separate the cases: `c<1/2` for `Q=S_0`; `c<epsilon` for the stated growing-`Q` bound. The primary leakage remark already has the correct exponent.

### F8 — MINOR — Theorem 8: the reader's full floor does constrain null-column correlations

**Location:** [RV:500–505](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:500).

“No condition … on correlations among null columns is used” conflicts with (A1), which includes null-only subsets. Whenever `q_n+s_0 >= 2`, it excludes duplicate null columns, for example. That freedom belongs to the master's weaker directional-floor/visibility formulation, not to this stronger sufficient full-floor version. The actual screening display is faithful.

**Minimal fix:** say “No additional condition … beyond (A1)” or remove the null-correlation phrase. Also specify the master's `q_n in {0,...,K-1}` rather than just the upper bound.

### F9 — MINOR — Theorems 1 and 4: two inherited status quotations are incomplete/misattributed

**Location:** [RV:82–85](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:82), [RV:247–251](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:247), CC:15.

The short quote in §1 is exactly `W3-POST:Thm-1`'s status, but **not the complete status of `SOP:TH09`**, although the two are presented together. Its registry status continues:

> T03♯: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2). T02(i♯), T02(ii♯): PROVED; SF/XF VERIFIED. T01–T03: PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY

Section 4 says `SOP:TH128` is “as in §1”, but §1 never quotes it. Its actual status is:

> PROVED (candidate) (W1-T03R); SF VERIFIED (W2-VT03R, no GAP/ERROR in the mathematics); XF VERIFIED under exactly its hypotheses (A-REV2); VERIFIED core (A-REV5, onset gloss ERROR); LIT-STAT: modest extension of Rossell 2022, clause (iii) known; final card: PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)

**Minimal fix:** attribute the short §1 quote only to `W3-POST:Thm-1`, or mark the SOP truncation with an ellipsis; quote TH128 separately. Other quoted status text matches [claims.tsv](/home/fb31/BVS-wt/W3-READER/Theory_work/INFRA/registry/claims.tsv), allowing the explicitly marked omissions. The conditional lists on MISR/RM2 are retained. No listed EXISTS-UNCHECKED input is incorrectly labelled EXISTS-CHECKED. F-UNI's registry/file-header discrepancy is accurately disclosed.

### F10 — MINOR — NOTATION: centring is not the claimed flat-intercept-prior equivalence

**Location:** [N:66–69, 78](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/NOTATION.md:66).

The coded working likelihood and score use `nu=a_0+n/2`. Integrating a raw Gaussian likelihood against a flat intercept prior instead contributes `(sigma^2)^{-(n-1)/2}`, giving `a_0+(n-1)/2` with the stated IG prior. Thus the parenthetical “equivalent to a flat prior on the intercept” does not describe this working posterior. The master's explicit **n-dimensional working likelihood**, despite the standardised response lying in the contrast space, is correct ([POST:26–29](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-POST/STATEMENT.md:26)).

**Minimal fix:** remove that parenthetical; retain centring as preprocessing and the supplied working-likelihood definition. The displayed prior, score, `K`, determinant and quadratic-form formulas otherwise match the master.

### F11 — MINOR — NOTATION: certificate definition omits the exact-enumeration branch

**Location:** [N:113–116](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/NOTATION.md:113).

Certification is described only through a completed local-search endpoint. The master also certifies the exact-enumeration maximiser, which need not be such an endpoint ([SCR:31–37](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-SCR/STATEMENT.md:31)).

**Minimal fix:** include that branch and identify certification with the public `local_certified` flag. Keep distinct the LS0 archive's certificate and the public reported-model flag; RM-0 explicitly makes that distinction.

### F12 — MINOR — Theorem 4: the bridge summary adds an unrelated unchecked dependency

**Location:** [RV:147](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/READER_VERSIONS.md:147), RV final bridge-summary row B2.2; [CC:35](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-READER/reviews/S1_frozen/CLAIMS_CARD.md:35).

These say Theorem 4 depends on `W2-APP:POST`. The listed master Cor-G(b) uses its own Gaussian-design transfer, `C-MIS:GD(b)` and the listed POST2 inputs; its conditional registry list does not contain APP:POST. The expectation transfer uses a design-event failure bound of order `1/n + log(n)/n^2`, not merely APP's `P(A_n^c)->0` ([G_corollaries:45–61](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-MISR/lemmas/G_corollaries.md:45)).

**Minimal fix:** remove Theorem 4/“4b” from the APP bridge dependency summaries. Do not use B2.2 alone to justify the expectation rate. Theorem 4's actual master-plus-B4.1 reduction is sound.

## Positive line checks and hypothesis coverage

These checks concern the intended positive constants, uniform envelopes and admissible-run conventions identified above. Existing input claims were checked for what they state; an unchecked input is not promoted to checked status by this review.

| Theorem | Hypothesis and conclusion check |
|---|---|
| 1 | S1/S2, fixed support and `p>=s_0` give POST's regime and `s_0<=K` eventually. B1.1 gives energy. B1.2 covers `s_0+j_0`. B1.3 covers the **anchored** weak-floor sets, not just unanchored sets. With F1 repaired, beta-min is exactly BM(c)/BM-infinity. The rate, joint HPM/MPM event and deterministic PIP inequality are no stronger than POST items 1–3. The no-beta-min remark correctly concerns strict supersets, not arbitrary false positives. |
| 2 | B2.1 supplies both LSF floors with a fixed `psi_n=phi^2`; its required asymptotic lower bound is automatic. APP explicitly covers fixed raw coefficients through the sample-SD event, and its diagonal argument supplies common constants and the joint design/noise law ([APP:12–18, 28–33, 58–68](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave2/W2-APP/lemmas/L1_POST.md:12)). No expectation rate has been inferred from `O_P`. APP remains EXISTS-UNCHECKED. |
| 3 | Primary (a) exactly uses PSHARP:B's domain and bound. In (b), set `N_n=p-s_0`; fixed `s_0` and `p->infinity` ensure `s_0+1<=K` eventually. N-orth is W-orth. Gaussian nulls become independent uniform centred-sphere directions; conditional on the truth design/coefficient vector, W-sph holds. Polynomial `p` supplies both logarithmic restrictions, and the master's uniform conditional-to-joint clause covers random truth designs. The energy/coefficient bounds are carried. Corollary A1 supplies the stated lower bound. F5/F6 concern the summaries/remarks. |
| 4 | The Gaussian conditional-law reduction, positive residual variance, fixed projected support, population energy and relative beta-min all coincide with Cor-G(b). B4.1 covers `s+max(j_0,m_sharp)`. No extra fixed-variance assumption is needed. Both the **expectation** rate and HPM error rate are explicitly in the master ([MISR:164–174](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-MISR/STATEMENT.md:164)); the KL remark is correctly restricted to the candidate conditional law. |
| 5 | Setting R is correctly standardised-signal, not fixed-raw-coefficient. A3/A4 match FL-R16/V-R. A5 has the common leakage/locality rate and reference-size conditions of L-R-plus; `Q=S_0` is feasible eventually. START-R supplies the concentration and the growing-Q primary remark with its stated exponent. Only the universal finite-sample floor and card exponent need F4/F7. |
| 6 | A2 and B6.1 give T1-R/FL-R; A3 is V-R; A4 carries leakage size and feasibility. With F3's common envelopes, B6.2 is L-R-b, and B6.3/B6.4 give W-R. RM2 then supplies SAND/NA/TL/POST, and RM-0 supplies a **single data event**, independent of seed/calibration, for admissible output runs. That common-event quantifier is faithful. It does not itself supply delivery; F2 remains. |
| 7 | B7.1 supplies T1-F, A2 gives both sample floors, A3 is V, and A4 is L-gain/L-feas. In case (a), `|Q|=O(log n)` permits a small positive `b<beta(eta,A)`, W-chi gives W, and the truth-removal width is `O(log n)`, so BM-infinity suffices. In case (b), B7.3 matches W-loc with common `h,L_n`; its variance clause follows under the floor, and BM-Q implies BM-W. RM2-F/RM-0 supply the common event and conditional-on-output conclusion. Delivery still needs F2. |
| 8 | The full sparse floor is the explicit sufficient case of A1, and the signal, budget and `c_1` match verbatim ([SCR:158–163](/home/fb31/BVS-wt/W3-READER/Theory_work/Wave3/W3-SCR/STATEMENT.md:158)). The conclusion is the correct **unconditional intersection-event** guarantee; it does not assert recovery conditional on a rare certification event, nor guarantee output/certification. F8/F11 repair only explanatory/definition scope. |

### NEW arithmetic bridges

The advertised set-size constants are sufficient, analytically, not merely over the numerical grid. Write `s=s_0`, `t=log n>=log 3>1`, `a=1/log 2<1.45`, `d=1/log(3/2)`.

- **B1.2:** `s+j_0 <= (2A+2)s+2` by the ceiling bound, including noninteger `A`.
- **B1.3:** POST:39 gives `s+m_sharp <= 2s+1+a(As+s/2+1)t <= [(2s+1)+1.45(As+s/2+1)]t`. The difference between `3(A+1)(s+1)` and the last coefficient is `1.55As+0.275s+3A+0.55>0`. Thus A5 covers every `S_0 union J` required by F-w. The cutoff bound is used only when `s<=K`, as required; that is eventual in this regime.
- **B2.1:** `s+m_bar <= d(As+s/2+1)t+(1+d log 2)(s+1)`. Hence it is at most `(2.47As+3.7s+5.9)t`; the exact respective coefficient bounds are `2.466304`, `3.699456`, `4.932607`. Also `s+j_0 <= [(2A+2)s+2]t`. Both coefficients are below `5(A+1)(s+1)` for `A,s>=1`.
- **B4.1:** combine B1.3 with the bound for `s+j_0` to cover `s+max(j_0,m_sharp)`.
- **B6.1:** B2.1 supplies T1-R. The additional small-set floor follows since `5(A+1)(s+1)log 3 >= 10(s+1)log 3 > s+16` for `s>=1`. The Q-union-singleton floor is explicitly assumed.

### NEW regression and assembly bridges

**B6.3 passes.** With `A=T intersect N_l`, the population regression residual on T is orthogonal to `W_T`. Thus the smaller-regression residual variance is `v_T+d' Sigma_TT d`. Unit diagonal gives `d' Sigma_TT d <= ||d||_1^2 <= L_n^2`. The floor on `Q union {l}` gives `v_T>=c` by interlacing and the residual coefficient vector's squared norm being at least one. Therefore the ratio is at most `1+L_n^2/c`, uniformly, which tends to one. The analogous normalised sample calculation justifies the variance clause invoked in B7.3. The extra `L_n->0` is correctly stronger than the master's polylogarithmic alternative.

**B6.6/B7.4 pass only for (V)/(S)/(P), not yet as full delivery assemblies.** The union bound is valid and [POST] is already an expectation-consistency statement; alternatively `0<=delta_n<=1` upgrades posterior convergence in probability to `E delta_n->0` without claiming an expectation rate. The operational premises in F2 remain separate. The common-data-event conclusion is precisely RM-0's conclusion over admissible output runs, not a new uniformity claim over arbitrary software invocations.

### Other notation checks

Apart from F10/F11 and the missing operational conventions, definitions agree: retained columns, centring/sample standardisation, `theta=D beta`, unscaled mean signal/noise quantities, model space and cap, beta-binomial weight, ridge g-prior, IG constants, score, PIPs/HPM/MPM, block-factorised start law, sample/population regressions, leakage lattice and reported score maximiser. Theorems 5–6 explicitly choose deterministic standardised coefficients, as their masters do; this is not silently replaced by deterministic raw slopes. The raw-signal extension is correctly left unclaimed.

## Per-theorem verdicts

`FAITHFUL-WITH-FIXES` means the primary mathematical implication is intact but a summary, definition or status/citation needs repair. `NOT-FAITHFUL` means the primary statement has a false literal alternative, a dropped hypothesis, or an unjustified stronger quantifier. None of these verdicts upgrades an input's registry status.

| Theorem | Verdict | Reason |
|---|---|---|
| 1 | NOT-FAITHFUL | Negative `C_beta` is allowed as written (F1); intended positive-constant version passes. |
| 2 | FAITHFUL | All hypotheses and joint-law conclusions transfer; APP's unchecked status is disclosed. |
| 3 | FAITHFUL-WITH-FIXES | Primary displays pass; card bound is false without its domain, and remarks overgeneralise (F5/F6). |
| 4 | FAITHFUL-WITH-FIXES | Mathematical reduction passes; repair inherited status references and dependency summary (F9/F12). |
| 5 | NOT-FAITHFUL | Finite-sample floor silently drops `s_0<K`/validity (F4); card also overstates growing-Q exponent (F7). |
| 6 | NOT-FAITHFUL | Delivery premises and common uniform envelopes are not fully carried (F2/F3). |
| 7 | NOT-FAITHFUL | Statistical/search reduction passes; delivery premises are not fully carried (F2). |
| 8 | FAITHFUL-WITH-FIXES | Screening implication passes; repair null-correlation wording, integer budget and certificate definition (F8/F11). |

S1-VERDICT: NOT-FAITHFUL AS WRITTEN — repair F1–F7 before acceptance; the set-size arithmetic and B6.3 are valid, and the remaining mathematical reductions pass subject to the explicitly identified premises and inherited statuses.
