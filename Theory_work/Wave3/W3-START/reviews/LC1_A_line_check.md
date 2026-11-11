MANIFEST 867e1c933d6fbbcbfd47b5deccf3b7f132d156fef1a29113de20e55eb5fefe38
Verdict: VERIFIED-WITH-AMENDMENTS — lemmas/L1_AGG_FLOOR.md

## Findings

1. **MINOR — lemmas/L1_AGG_FLOOR.md:19–23 (P3 domain).** The standalone quantifier only requires k >= D >= 0 and k-D+a <= p. It does not put k in the domain 0,...,2p-1 on which line 11 defines w. For example, k=D=2p and a=0 meets those written conditions but w(k) is undefined, and the first invocation of P2 is outside its range. **Exact repair:** replace the opening quantifier by “For integers 0 <= D <= k <= p and a >= 0 with k-D+a <= p”. This narrower form suffices for every application: k=|T|<=K<=p in L1.1 and k=s0<=K<=p in L1.4. Alternatively k<=2p-1 suffices for the stated proof. This is a domain clarification; no downstream inequality, constant, or locked target needs changing.

2. **MINOR — numerics/lemmas/falsify_L1.R:18 (sampling outside the advertised hypotheses).** `K <- sample(mb:p, 1)` has the length-one numeric-vector trap when mb=p. In the present generator this can occur at p=mb=4. R interprets `sample(4:4, 1)` as sampling from 1:4, so it can generate K<mb and hence a block larger than K. Line 22 does not catch this. These trials test a broader positive-table identity but cannot all be described as instances satisfying the block-size hypothesis. **Exact repair:** use `K <- mb + sample.int(p - mb + 1L, 1L) - 1L`, add `stopifnot(mb <= K, K <= p)`, and rerun the reported seeds. I confirmed the trap directly: with seed 33117, `sample(4:4, 20, replace=TRUE)` begins 3,1,1,1,3,2. This affects numerical coverage accounting, not the proof. I did not modify the script or its recorded results.

No CRITICAL or MAJOR finding. Subject to the two local amendments above, I verified the displayed inequalities in L1 and their agreement with STATEMENT.md (C0) and (T0).

## Checks performed

### Frozen inputs and scope

Read L1 in full, line by line, against STATEMENT.md sections 1–2, 5.1, and the T0 display in section 5.3. Ran the authorized manifest verifier: `verify: OK MANIFEST 867e1c933d6fbbcbfd47b5deccf3b7f132d156fef1a29113de20e55eb5fefe38`. Read the permitted L1 numerical script, shared helpers, and results summary. Read the pinned scorer's prior construction, factor construction, finish routine, and nonnegative-Q routine. No other ticket or registry assertion was used as a premise. L1 cites no result from another lemma file that is needed for its proof.

### L1.0: elementary inequalities and constants

- P1 follows by the adjacent binomial-coefficient ratio. Its upper bound needs k<=p-1, exactly the range used when adding to a model of final size at most p. P2 has the stated range, upper bound 2p, and lower bound p/k for k<=p. The products in P3 have those ranges at every actual application; finding 1 concerns its standalone wording.
- P4 is applied with c=kappa0+1, cQ+1, s0+1, or |Q|+1, all strictly positive. P5 follows by counting the distinct ordered tuples inside the full power. The chain bound only visits conditioning sets containing the block truth and excluding the coordinate being added; all corresponding table entries exist since the entire block has size at most K.

### L1.1: decomposition and fibre sum

- T(S)=(S intersect Q) union S0 is a feasible lattice element. For a bad block, T_b=(U_b intersect Q) union U*_b, d_b counts precisely the missing reference coordinates, and a_b counts precisely the coordinates outside Q. Thus |U_b|=|T_b|-d_b+a_b. A bad block contains at least one reference coordinate, so a_b<=16-|U*_b|<=15. There are at most s0 bad blocks.
- Good blocks have U_b=T_b disjoint-union N_b. Once T, the bad-block family, their U_b, and the good-block outside set N are given, S is recovered block by block. The fibre map is injective. Permitting N to run over all outside-Q subsets, including coordinates in bad blocks, only enlarges the summation domain of nonnegative terms; it does not compromise this injection.
- D=sum(d_b-a_b)_+ <= sum d_b <= s0 <= |T|, E=sum(a_b-d_b)_+ <=15s0, and |T|-D+E+a'=|S|<=K<=p. Hence P3 applies with a=E+a'. Splitting (x)_(E+a')=(x)_E(x+E)_(a') gives (x)_E<=cQ^E and (x+E)_(a')<=(cQ+1)_(a'), since x+E-1=|T|-D+E<=cQ. In the no-bad-block case D=E=0, giving the sharper (|T|+1)_(a'). When bad blocks exist, s0>=1 and cQ>0, so no problematic zero power is introduced.
- Since Q contains S0, U minus (Q union S0)=U minus Q: the exponents in line 53 agree exactly with section 2's omega^Q. The good-block factors are bounded by CH. P5 cancels p^(-a') against (p U_Q)^(a'). For each bad block the prescribed T intersect C_b lies between U*_b and C_b intersect Q, so its bracket is bounded by the correct maximum defining Xi_b(Q), rather than by a maximum over an inadmissible family.

### L1.2: AGG-a

Summing the fibre bound first over a', then bad-block families, then T gives Z<=F Z_lattice. All sums are nonnegative and the original model space is finite; extending the a' sum is valid when U_Q<1. F>=1. Consequently lattice mass is at least 1/F, and outside mass is at most 1-1/F<=F-1. This is the locked claim, with a stronger intermediate bound.

### L1.3: AGG-b

- At Q=S0 the lattice is a singleton and cQ=16s0. All one-addition models are feasible when s0<K, distinct, and contribute exactly the stated T1, including the denominator 2p-1-s0. P1 and CH give T1<=(s0+1)U.
- The no-bad-block cases of outside size at least two contribute at most (1-U)^(-s0-1)-1-(s0+1)U=R2. The nonempty bad-block families contribute at most [product(1+Xi_b)-1](1-U)^(-16s0-1). The reference model is the sole zero-addition/no-bad-block term. No overlap or missing term occurs in this split.
- For the lower bound, fixing b makes U -> (S0 minus U*_b) union U injective. The resulting model differs from S0 and has size s0-d+a<=s0+15<=K under the target's stronger condition s0+16<=K. Other blocks retain their reference configurations, so their table factors cancel.
- If d>=a, e=d-a<=min(s0,16), the prior ratio is at least (p/s0)^e=(2p)^e(2s0)^(-e)>=(2p)^e(2s0)^(-16). If a>d, e=a-d<=15, the ratio is at least ((s0+1)/(2p))^e>=(16s0/p)^e 32^(-15). Every denominator in these products is positive because the final model size is at most p. Both losses are bounded below by (64s0)^(-16). Summing within each fixed block and then taking the maximum proves o0>=c_s Xi; there is no erroneous summation of different blocks' lower bounds.

### L1.4: AGG-c and AGG-d

- For every block, the truth-deletion factor is bounded by (e_n/(2p))^d_b using precisely a'=d_b>=1 in the definition of e_n. When d_b=0 that factor is exactly one. The restoration/augmentation chain starts at U*_b and therefore uses admissible m_l even if the original U_b omitted truths.
- With d=|S0 minus S|, a=a_Q+a_o, P3's final size is |S|<=p. Monotonicity in the rising-factorial base gives (s0-d+1)_a <= (s0+1)_(a_Q)(s0+a_Q+1)_(a_o). Every factor in the first product is at most |Q|, and the second product is at most (|Q|+1)_(a_o), since s0+a_Q<=|Q|. This yields exactly the |Q|m_l/p factors and exponent |Q|+1 claimed in AGG-c. Summing deletion subsets gives (1+e_n)^s0; summing the two addition subsets gives the product and binomial series. Dropping the feasibility restriction only enlarges the sum.
- In AGG-d, U union U*_b=T' disjoint-union N. Each m_l for l outside Q is at most their sum pU_Q, including when U has additions. Multiplication by omega^Q gives e_n^d(U_Q/2)^a in the d>=a case and e_n^d(cQ U_Q)^(a-d)(U_Q/2)^d in the a>d case. A truth block implies cQ>=1, so cQ U_Q<=1 implies U_Q<=1. Both residual factors are at most one. Here 1<=d<=16, so e_n^d<=max(e_n,e_n^16) regardless of which side of one e_n lies. There are at most 2^16 subsets; taking the maximum over T' preserves the bound.

### L1.5: FLOOR and T0; pinned-code comparison

- In v3_score.h:175–183 the factors are those of H=(n+1)G+I and A=G+I. At lines 214–217 the forward solve's squared norm is z' H^(-1) z; lines 212 and 223 give the claimed determinant and score formula. Constants b0>0 and nu>0 are set at lines 14 and 57. The fallback at lines 145–159 is also algebraically equal to Q: its quadratic criterion is y'y-2z'beta+beta'(H/n)beta, minimized at beta=n H^(-1)z, with minimum y'y-n z'H^(-1)z. EX-A therefore makes the fallback consistent with the same score.
- For lambda=1/(n+1), completing the square gives rho_S=y'y-z'(G+lambda I)^(-1)z and Q_S=y'y/(n+1)+n rho_S/(n+1). Extending S allows zero coefficients on new columns, so rho and Q cannot increase. No inverse of an unregularized Gram matrix is taken.
- The two Schur complements yield D_(S+l)/D_S=(n+1)s(1/(n+1))/s(1). Positive definiteness gives s>0, and differentiation gives s'=1+g'(G+lambda I)^(-2)g>0. Thus the ratio is at most n+1 even for rank-deficient X_S. Combining this determinant bound with the decreasing Q and nu>0 proves the full-model one-step score ratio, not merely its block-table version.
- Applying the same ratio inside the coordinate's block and summing the p-k distinct one-addition competitors yields odds at least f_n(k). The displayed arithmetic difference is k(2(p-k)-1)+1>0 for 0<=k<p, so f_n(k)>=1/(2 sqrt(n+1)). With f=1/(2 sqrt(n+1))<=1/2, f/(1+f)>=2f/3. This gives the exact constants 1/3 in the mass bound and 1/2 in T0's odds bound. The prior denominator stays positive, including p=1,k=0. Every invocation has k<K<=p.

### Edge cases and target comparison

s0=0 has no bad blocks, Xi=e_n=0, and the deletion factors are empty products. For Q=S0=empty, the rising-factorial base is still one; AGG-b becomes the one-addition term plus the geometric-series remainder. In AGG-c with Q empty, a_Q=0 and the finite product is empty, so no positive exponent of |Q|=0 is needed. For Q=[p] with |Q|<=K, U_Q=0 and all positive-size outside subsets disappear. The same reasoning covers a truth block wholly inside S0 and singleton blocks (which have no positive a_b). At s0=K the AGG-b and T0 premises fail, as intended, while AGG-a/c/d remain valid. At K<p all prior products still end at size at most K. For p=s0+1 and an unsaturated reference, the sole one-addition model is feasible and the same T1 and f_n formulae apply. Near U_Q=1 the binomial bounds can be huge but remain valid; no proof assumes a fixed distance below one. The inequalities proved match the hypotheses, quantifiers, and constants of STATEMENT.md:183–195 and 227–229. Its asymptotic commentary is read in the stated fixed-s0 regime; I do not infer an unclaimed growing-s0 consequence from limits of unweighted functionals.

### Numerical falsification

1. Reran the supplied script read-only: `Rscript --vanilla Theory_work/Wave3/W3-START/numerics/lemmas/falsify_L1.R 1000 60 33117`. It reported **zero violations**. Table check counts: AGG-a 814, AGG-b upper 680, T1 lower/upper 877, c_s lower 459, AGG-c 814, AGG-d 260, and assembly e2 135. Real-data checks: 9,763 one-step ratios, 2,364 unsaturated-model floors, 60 T0 chains; minimum ratio times sqrt(n+1)=1.012989 and minimum floor/claimed-floor=1.0775. R printed locale warnings but completed successfully. Finding 2 limits the interpretation of the random-table coverage. The c_s test deliberately uses the sufficient feasibility condition s0+mb<=K for its smaller blocks; this tests a valid stronger extension, rather than literally drawing cases with s0+16<=K. The p<=11 table runs cannot cover the latter nonempty-reference condition or a full size-16 block.
2. Independently implemented subset enumeration and table functionals inline in Python, with no repository script writes or helper imports. Across 140 cases at p=1,...,7, used valid blocks of size <=K, varied K,S0,Q, arbitrary positive rational tables, and singleton cases arranged to have U_Q=999/1000. Exact rational checks passed for **1,733 individual fibre sums**, **118 AGG-a bounds**, **89 pairs of T1 bounds**, and **45 AGG-b upper bounds**. AGG-c (118 checks) and AGG-d (27 checks) used a floating root for e_n with relative tolerance 1e-12; those were not exact-arithmetic checks. Zero violations.
3. Independently checked the lower prior inequality by exact fractions for **39,680** tuples with p=17,...,40, 1<=s0<=p-16, 1<=d<=min(s0,16), 0<=a<=15, and feasible final size. These include a superset of actual block configurations and both prior cases. Also checked the integer arithmetic underlying f_n(k) for all **5,050** pairs 1<=p<=100, 0<=k<p. Zero violations.
4. Added an independent full-size-16 block example: p=K=32, n=64, s0=1, one size-16 truth block with nonmultiplicative positive rational tables, plus sixteen singleton null blocks. Enumerated all 65,536 truth-block configurations and obtained the global normalizer by exact size-profile convolution. The target feasibility s0+16<=K holds. Exact comparison gave o0>=c_s Xi (approximately 3.31635 versus 4.16357e-29). Zero violations. This is a genuine full-block feasible lower-bound case, although the constant is deliberately very conservative.

## Not checked

- Proofs of L2–L5, their numerical outputs, or any probabilistic/asymptotic theorem beyond the deterministic T0 claim; these are outside this review's object.
- End-to-end equivalence of every preprocessing, partitioning, start-convolution, and dispatch branch to the stated setup. The pinned score/prior formulae relevant to L1 were checked directly; the setup's partition and start definitions were taken as given.
- Floating-point guarantees, compiled-core execution, or numerical stability. EX-A is essential to this review's scope; the numerical scorer runs are falsification attempts, not machine-arithmetic proofs.
- No exhaustive empirical check over every size-16 positive table or arbitrarily large p. The analytical argument covers those cases; the finite experiments supplement it.

Only this review file was written. No git operation, repository edit elsewhere, subagent, or external premise was used.
