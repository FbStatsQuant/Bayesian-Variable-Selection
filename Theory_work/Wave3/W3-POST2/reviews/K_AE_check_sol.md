# W3-POST2 ? adversarial line-by-line check of A and E

Reviewer: Codex gpt-6.1-sol, high. Statement checked: W3-POST2/STATEMENT.md v1.1. Review scope: A0, A1/1-OS, A2, E1, E2/1-VIS, and the accompanying implications and remarks. Paths/line numbers below refer to the files as read for this review.

## Verdicts

- `lemmas/A_occam.md`: **VERIFIED-WITH-AMENDMENTS**. A0's implication chain and A2 are correct. The A1 proof works after restoring the missing upper summation limit in C5?(a). Its inherited beta-min qualifications must be retained. Two ancillary assertions need correction.
- `lemmas/E_visibility.md`: **VERIFIED-WITH-AMENDMENTS**. E1 and E2 are mathematically sound using the corrected C5?(a). No eigenvalue condition away from S? is hidden in the invoked inequalities. The remarks overstate necessity and what finite numerical evidence establishes.

No FATAL finding. The MAJOR finding is a false intermediate statement with a local repair; it does not require changing the proposed theorem or its hypotheses.

## Numbered findings

### 1. MAJOR ? C5?(a) has an uncapped left-hand sum

Location: `lemmas/A_occam.md:63` (also the proof at lines 66?67).

The displayed assertion is `?_{j>j?} ?_j ? exp(?_n) ??^{>j?}_n`. The right side stops at `min(m?_n,p?s?)`, whereas the left side does not. The inherited definition [P3] `PROOF_v2.tex:227` defines ?_j for **all** j?1 and only declares it zero when s?+j>p. It is strictly positive for every 1?j?p?s?. For p?s?>m?_n, choose j?=m?_n: the right side is zero and the left side is positive, on every data set. This is not justified by the parenthetical at line 67.

Proposed fix: write `?_{j=j?+1}^{min(m?_n,p?s?)} ?_j` (or use upper limit m?_n and the inherited zero convention), with integer j??0. This is exactly the upper limit in [P3] `prop:sup`(a) and [T03R] (C5)(a). All actual uses in C8? and E2 have this intended range and then work.

### 2. MINOR ? the gap remark drops the rank-zero weight

Location: `lemmas/A_occam.md:94`.

The claimed bound `a_J ? (2e C_A m?_n log n)^{d_J/2}` is false: if d_J=0 and j?1, its right side is 1 while a_J=2^{j/2}>1. This is precisely the rank-deficient case the new interface is intended to handle. There is no such error in the bound proved at lines 19?21.

Proposed fix: replace the bound in the remark by the already proved `a_J ? (2e C_A log n)^{j/2}`. Alternatively retain the explicit leading factor `2^{j/2}` in a bound depending on d_J. This does not affect A0 or C5?.

### 3. MINOR ? the strictness remark infers feasibility from an upper bound

Location: `lemmas/A_occam.md:29`?`lemmas/A_occam.md:31`.

The Schur expression and its upper bound `?1+?a??` are correct. But `c_D^j(n+1) ? 1+?a??` does not show that the **actual** Schur factor, multiplied by the preceding determinant factors, meets DG. The preceding j?1 factors are not specified, and an upper bound on the last factor cannot supply a lower bound. The parenthetical j threshold only makes the displayed compatibility condition hold (for 0<c_D<1); it does not prove DG for this J, let alone every required J.

Proposed fix: describe this as a compatibility observation, not a sufficient criterion introduced by ?once.? If strictness of DG versus full rank is being claimed as a proved example, give an explicit growing-circuit design and lower bounds for every required subset. The implication chain itself does not need this remark.

### 4. MINOR ? make A1's inherited beta-min qualifications explicit

Location: `lemmas/A_occam.md:36` and `lemmas/A_occam.md:78`?`lemmas/A_occam.md:81`.

The reference to ?conclusions 1?6 of [W3P] Theorem 1? correctly inherits their qualifications: [W3P]:81?86 require BM for selection and its corollaries. But the assembly states its selection-rate argument without saying that (C10) is now being used **under BM**. (C10) requires BM(c>c?) or BM-? as well as B2; F_? alone is not enough. I interpret the cross-reference as retaining BM, rather than asserting selection without it.

Proposed fix: add ?with each conclusion's beta-min qualifications unchanged? to the statement and ?Under (BM)? before the selection assembly. Retain the separate no-beta-min clauses 5(a), 5(b). No additional hypothesis is needed beyond what the referenced conclusions already require.

### 5. MINOR ? E3's necessity assertions exceed both A2 and the numerical evidence

Location: `lemmas/E_visibility.md:71`?`lemmas/E_visibility.md:72`, and `lemmas/E_visibility.md:76`.

?(ID) is order-necessary? is not proved by observing a finite list of ?_n values near 0.57. Nor does the condition that one same-size underfit has small ?_S by itself prove that it remains competitive: its score ratio also depends on the determinant and the prior, and even comparable determinants allow a likelihood ratio that decays polynomially when ?_S is a small positive multiple of log n. The cited N1 experiment exhibits a particular obstruction; it is not a general converse for ID.

Similarly, ?(OS) ? essentially necessary by Claim A2? is stronger than A2. A2 bounds the **unweighted, capped** sum ???_n. It gives no necessity for the weights a_J, the extension beyond ?, or the amplified j>j? inequality. W3-POST2/STATEMENT.md's A2 discussion expressly makes this distinction.

Proposed fix: replace the first assertion by ?N1 illustrates a small-margin obstruction; no converse to ID is proved here,? and replace the second by ?a superset Occam sum, whose unweighted capped counterpart is necessary by A2.? If an asymptotic necessity claim is desired, prove it for an explicit design sequence and state its scope.

### 6. NIT ? numerical summaries should remain finite-sample summaries

Location: `lemmas/E_visibility.md:69`?`lemmas/E_visibility.md:74`.

The cited output contains ?/r_n=1.175 for N4 c=4,n=100, outside the quoted 0.6?1.0 range. N1 ?=1's recorded IDmargin falls from 0.38449 to 0.22408; the output alone does not establish a limiting margin or ??_n?0.57 not ?0.? In N1 ?=0.5, OS is an asymptotic deterministic claim, whereas the output merely reports finite values of the unamplified weighted ratio.

Proposed fix: quote the actual finite ranges (N4 approximately 0.58?1.18 across c=4,8) and label them numerical observations. Support asymptotic OS and nonconvergence claims with analytic calculations or remove those assertions. These remarks are not used in E1/E2.

## Detailed checks and source audit

All explicitly cited labels/line references used by the two proof arguments were opened in the supplied local sources. In the following, P1/P3 denote the exact `main@c4ef0dc` snapshot files specified in the brief, and T03R denotes the supplied W1-T03R snapshot. No remote source or git operation was used.

### A0 and the replacement of F_w

- P1 `lem:spec`(e), lines 90?110, is stated for arbitrary g>0 and proves the determinant lower bound required by A0(i). DG?ADG follows by averaging. For ADG?OS, the determinant weights have the same prior ratio for fixed j; extracting the maximum a_J before applying the average is legitimate.
- The derivative calculation at A:19?21 is correct, including d=0. It yields the stronger, correct bound `(2e C_A log n)^{j/2}`. P3 `lem:prior`(b) applies up to s?+j=p, including the boundary. The stated q?_n and its factor 1/2 under the square root track correctly. P3 `prop:sup`(b)'s geometric-tail constant K_{s?,i} is valid here. P3 `lem:assemble`'s exponent inequality gives the amplified remainder `O((log n)^{(j?+1)/2}/n)=o(r_n)` for fixed s?,A. Thus n_OS,C_OS can depend only on s?,A,c_D.
- T03R:139 and :143 are indeed B1 and its proof. Inspection of T03R ??4?7 confirms that F_w supplies only B1's full-rank/exact-law/determinant package. B2 uses F_?, B3's upper inequality uses only the floor on the smaller set, and (C3),(C6)(b),(C7),(C10) use F_? rather than F_w. The ?5 T02(ii?) route has the same B1 uses and is replaced by A's direct 5(a) argument.
- P3 `lem:red`, `lem:smoother`(b)?(d), `lem:chi`(a), and `lem:Gprob` support G3? and C4?. A projection increment has rank d_J even when the augmented columns are dependent. For d_J=0 the variable is identically zero. G2 already uses rank?|T|. P3:194's G4 union bound only needs rank(P_{S?}?P_S)?s?, so its exceptional probability remains 1/n without F_w.
- T03R B3 with smaller set S? needs F? only. P3 `lem:ongood`(b)'s proof at :218 uses G1,G2 and the fact that S contains the mean; it imposes no eigenvalue condition on S. Its part (d) uses only the stated denominator bound and the energy bound. Thus C4? preserves ?_n,?_n,?_n, with m_n read as m?_n.
- Lemma M follows from the actual identity in P3 `lem:chi`(b); no stochastic domination of the truncated exponential is being assumed. This matters because that function is not monotone at ?. The d=0 case is separately correct. `e^{j?_n}?2^{j/2}` follows from `?_n?(log 2)/2` uniformly in j, and ?_n?0 follows from m?_n=O(log n). Markov then proves both OS-controlled tightness assertions.
- The union range is sufficient: for each underfit with |S|?m?_n, J?=S?S? has size?min(m?_n,p?s?). S?S? may have size greater than K; P3's setting explicitly defines ? on every subset. Keeping this enlarged range, rather than K?s?, is essential. T03R (C6)(a) and (C8) are algebraic and use no large-set floor. After finding 1's repair, C8? follows with the advertised amplified rate.

### A2 and inherited consequences

P1 `lem:spec`(d) proves Q_S?Q_{S?} without any rank assumption. On valid coded inputs ?(S?)>0; the ratio at A:90 is exact. The S_J are distinct feasible models, and summing yields ??(1??)???, including the empty-sum case s?=K. Thus A2 is verified. LB's proof, lines 20?32, is indeed the j=1 specialization plus P3 `lem:det`'s unconditional upper bound and the prior multiplicity lower bound; LB's feasibility/domain restrictions remain necessary.

W3P ?0 agrees with the target used here, including the random response scale and the common b in contrasts. W3P Theorem 1's conclusions and their qualifications were checked. SL0/SL1 in [SL], especially lines 20?51, give precisely the claimed deterministic/law-free consequences. [POST] step (5), lines 58?68, is the every-deterministic-sequence diagonal argument claimed here; it transfers with common constants and a common onset for OS. The size tail is T03R T02(i?), whose denominator argument uses only F?; L1a? lines 27?42 and Remark 1 also give it using `??*???1.5M/???`. Neither route imposes a floor away from S?.

### E1: constants and every comparison inequality

- E1(a)'s Gaussian variance is exactly ?*??_S. If ?_S=0 the cross term is zero identically, so the same union bound holds without standardizing by zero. The count `2^{s?}(j?+1)p^{j?}`, exceptional bound `(2/e)^{s?}/n?1/n`, and `x_n?C_x log n` are correct.
- The score identity follows from P3 `eq:score`. P3 `lem:prior`(a), `lem:det` and the inequality `2?(n+1)?n` for n?5 give the prefactor `?n^{s?(A+1)}`. Neither determinant bound needs a floor.
- P1 `lem:den`'s first proof paragraph, :337?338, really proves the stronger projected-noise bound quoted at E:29, before replacing it by total noise. It uses only the S? floor. With ?_n?2/(n+1), `R_n?8(M+?*?)` follows from P3 `lem:ongood`(a).
- The invocation of P3 `lem:ongood`(c) at E:31 imports only the bound on E_n, **not** its bound on Q_S for an underfit. Indeed `R_n?2?y_c??/(n+1)` implies `B??E_n`. P3:220 proves `E_n?N?*?(1+??_n)` using G1 and part (a) alone; the earlier SE-dependent sentence in that paragraph is unnecessary here. Constants `(12b?+8)(M+?*?)` track exactly.
- To obtain D's lower bound, combine `Q_S??(I?P_S)y_c??` with `Q_{S?}?Q_{S?}??(I?P_{S?})e??+R_n`. The noise difference equals `?P_{S?}e????P_Se??`, which is at least `??*???_{J?}` by nesting S?S? and S??S?. This proves the sign and every term of E:36 without a floor on S or S?.
- The range assertion at E:35 is valid eventually, including bounded p. One can justify the stated dichotomy uniformly: if m?_n<K and m?_n<j?, then R_{m?_n} contains a q_{m?_n+1}/w(s?) term bounded below by a positive constant depending only on j? (the index is bounded and p?that index). This contradicts the defining threshold tending to zero. Hence eventually m?_n?j? or m?_n=K.
- `log(1+u)?(log 2)min(u,1)` is correct. The D?B? branch is eventually stronger than required. In the other branch, n/N?1 gives the stated lower bound. The function ? is increasing above 2C_x and the given c? is its larger root at level `(2/log 2)[s?(A+1)+2]`. Therefore c>c? supplies strict slack to absorb both ??_n and `8(M+?*?)/(?*? log n)`. The onset must depend on c (or its positive slack), as well as the common model constants. The numerical value is c?=160.7706367 when s?=A=1; 160.8 is correct.

### E2 and the implication from beta-min

E2 rederives the combinatorial portion of P3 `lem:assemble`, using E1 instead of the floor-dependent sharp comparison. Its large-J? part uses only T03R (C6)(a). Each comparison union occurs fewer than 2^{s?} times, the J?=? contribution is 1, and the remaining sums use the corrected capped C5?(a). Thus no use of P3 `lem:SvsSp`, `cor:diff`'s lower half, or the SE-dependent part of `lem:ongood`(c) survives in E2. G4 is unnecessary. The 5/n exceptional bound and the ID_j-only screening argument are correct.

Finally, P3 `lem:signal` is exactly the variational eigenvalue argument needed for E3.1. For S in the ID domain, S?=S??(S?S?) is one of F_?'s anchored sets; BM(c) gives `?_S?N?????*_{S??S}???(1?1/n)c?*? log n`. Thus the implication is verified. To apply the asymptotic theorem with a fixed margin constant, choose any c? strictly between c? and c; then ID(c?) holds eventually. This is already stated correctly in STATEMENT v1.1.
