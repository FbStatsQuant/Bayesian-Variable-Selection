# R02 — fresh STATEMENT-LOCK review

**Verdict: LOCK-WITH-CHANGES.**

The intended target is appropriate and plausible: the merged method is unchanged, rows are iid Gaussian with signed compound-symmetric population covariance, raw coefficients are fixed, and probabilities are joint in design and noise. The strict limsup hypothesis supplies an eventual fixed exponent below one half. Nonempty support and the population FS conditions are explicit. C1 and the posterior/delivery assembly C3–C4 have viable routes through conditional block estimates and the every-sequence argument. I found no counterexample to the intended statistical theorem. This is a statement/architecture lock conditional on the changes below, not a verification of the unchecked lemma drafts.

Read: STATEMENT v2, PLAN, R01 and its disposition, X1–X4, FAC-B STATEMENT and L1–L5, FAC-A L5_random_instances §L5.1, all three protocols, N1X_summary, N3X_out and n3x_softgap.py. Only this file was written. The numerical outputs were read as evidence; I did not rerun them.

## Required changes

1. **Make X3 a prefix lemma before using it in the self-consistency induction; repair the off-by-one proof and the crossing case in B1.**

   X3(vii) assumes I > Q. At induction step i, H(i) supplies approximate deletions only through step i−1. For i ≤ Q it does not supply the long sequence required by (vii)/(viii). X4.4's justification “I > Q since the bulk has m0−m1 ≫ Q steps” uses future approximate deletions whose validity is precisely what is being established. The intended mechanism can be made noncircular, but the current invocation is not valid.

   State and prove the following prefix version: for every already established prefix, either the first wide hole has occurred, or all its deletions lie in [x0−4.1ϖ,x0+4.1ϖ] and its centres move by at most ϖ/10; the latter alternative cannot survive Q+1 deletions. This gives the band at T_i from H(i), including i=0, without assuming any future search move. In the present proof of (vii), the assertion that the displacement bound with factor Q also holds at i=Q+1 is false arithmetic: there are Q+1 increments. Only x_0,…,x_Q are needed to locate the first Q+1 deleted points. Bound those centres, obtain Q+1 points in an 8.2ϖ interval, and reach the contradiction before asserting a bound for x_{Q+1}.

   Also repair X4.4 B1's statement that deleting the last point on a side is the “only way a side empties.” During a crossing a side can empty when a point on the opposite side is deleted. Before the first wide hole, use the confined deletion window and the retained far points of both signs to prove B1. After the first wide hole, noncrossing makes the existing last-point argument applicable. Then explicitly use the dependency order B1(i), B2(i), B3(i), B4(i).

   This does not require a wider band. X3(iii) is correct under its stated |K|≥3 and κ′>1: a crossing implies L(|K|−2+κ′)<2ϖ, L<ϖ, R<3ϖ, hence ω<4ϖ. For the final one/two-null steps use the separately displayed c1ϖ bound, rather than citing (iii) outside its domain. The density condition controls cumulative movement, not merely a single crossing: while the hole is narrow, each deletion is within 4ϖ of its current centre and there can be at most Q such deletions in the confined window. It therefore excludes R01's accumulation construction. The repair is substantive formal closure of a viable argument, not a replacement by another unproved invariant.

2. **Repair X2's deterministic event implications for bounded or slowly growing p. The stated Proposition X2 is false on its current event.**

   D3 and D4 bound η and truth coordinates by L_n=log log n; they do not bound them by H̄=O(sqrt(L_n)) when p is bounded. Nevertheless X2.1 asserts H̄+2|η|/ℓ≤2H̄, X2.3(i) drops |η| from its estimate, and (iv) explicitly uses L_n≤H̄ for truth coordinates. These implications fail on E_n.

   Here is a counterexample to the proposition's on-event bound, using its exact representation. Take p=2, S0={1}, ρ=1/2, φ²=N, W=NI, η=t=L_n/2, ξ1=t−1, ξ2=1, and a1=a2=h=sqrt(log n). Then κ=1, ϱ=t, x_{\{1,2\}}=0. All D1–D6 conditions hold for sufficiently large n (take a permitted typical noise norm); off-diagonal row sums are zero. The full set is structured with empty interval part and no exceptions. Put d=1+h/sqrt(N). Its actual inverse numerator at null 2 is

   ```text
   (B^{-1} ṽ1)_2 = 1+t − 3t d²/(1+2d²)
                    = 1 − (2/3)t h/sqrt(N) + O(t h²/N).
   ```

   The normalization in τhat is 1+O(h/sqrt(N)), so |δ2| is of order t h/sqrt(N). Proposition X2's right side is only O(C_X H̄ sqrt(log n/n)). Their ratio grows as sqrt(L_n). No fixed C_X repairs this assertion. Small open perturbations preserve the failure, so this is not an objection based only on a measure-zero Wishart matrix. A separate choice of large allowed η and bounded ξ also refutes the claimed global |x_T|≤2H̄.

   A simple repair is to strengthen the high-probability event so that η and the finitely many truth coordinates are bounded by H̄ (up to fixed rho-dependent constants), and retain those constants in |x_T| and the budget. Since H̄→∞ even for fixed p, this costs o(1) probability. Alternatively retain L_n throughout the sparse regime and show its errors are absorbed by n^(−1/3). Reconcile the p-based H̄ in X2 with the null-count-based H̄ in STATEMENT/X4. The target's inclusion of bounded p should remain intact.

3. **Bind the path-dependent notation locally under the universal quantifier in C2.**

   STATEMENT §3 defines S*, N* and m0 using the realized N0, and defines a_T,b_T only for T⊆that S*. C2 then quantifies over every N with |N|≤15, while (iii) still uses N* and (iv) still says exactly m0 moves. Explicitly introduce S*(N)=[p]−N, N*(N)=([p]−S0)−N and m0(N)=p−s0−|N|, and define the edges for all the corresponding visited sets. Restrict the subsequent LS0/cap consequence to N=N0. Section 1's informal “in place of N0” indicates this intention, and X4.2 does rebind these quantities, but the theorem should do so too. With the literal global m0, two starts whose excluded sets differ by one null cannot both reach S0 in exactly that many pure deletions.

4. **Finish the gain-error conversion with valid bounds, rather than the displayed loose estimates.**

   X4.1's displayed square bound contains C n^(−1)(1+H̄²); taking square roots of that estimate alone gives O(H̄/sqrt(n)), not the asserted C_g/sqrt(n). Retain the sharper form: determinant errors contribute C/n to the squared-statistic comparison, the epsilon-d term contributes C|τhat_{j′}|^4/n, and ridge errors are smaller. Then the absolute-statistic slack is bounded by C/sqrt(n)+C H̄³/n=O(n^(−1/2)), or state the larger slack and explicitly absorb it into ϖ. Either is sufficient for C2(i).

   In X4.5 E-add, |δ|≤ϖ does not directly imply the displayed bound with (1−γ_{k+1})(|ξ_l−x_T|+ϖ)²: factoring out 1−γ_{k+1} also divides δ by that factor. Use a uniform constant times ϖ, which is harmless since k+1≥s0+1≥2. In the bulk the existing 3ϖ/4 estimate and γ=o(1) can justify the tighter expression, but say so. Spell out end-phase preservation with the small-cardinality crossing bound and the affine-centre estimates; replace the unfinished “(H̄−2δ_e−|x_i|)·…” sentence. In particular, one-sided persistence should follow from the extreme-value structure and centre formula, rather than importing the exact-argmin lemma for an approximate rule without explanation.

   These are sufficient-error obligations from R01 item 3. They appear repairable with the existing polynomial error budget and strict move margins, but the written calculations do not yet prove them.

5. **Correct the remaining frontier “iff” claim.**

   STATEMENT §5 and X2's final remark identify vanishing p H̄ sqrt(log n/n) with limsup log p/log n<1/2. The latter is sufficient, not necessary. For example p=floor(sqrt(n)/(log n)^2) has limsup exponent 1/2 and p H̄ sqrt(log n/n)=O(1/log n)→0. Keep the locked strict-exponent target, but state the actual absorption criterion separately and remove “iff”/“i.e.” equivalences. The total band-bound ratio also has the additive O(H̄(log n)^(3/2)/(sqrt(n)ϖ)) term, which tends to zero because of the n^(−1/3) floor; use an upper bound rather than claiming a general asymptotic equivalence from an occupancy upper bound. X2's assertion that all other terms work for every A1<1 is also unsupported by its displayed second-order p^(3/2)/n bound; retain the proved range or identify additional estimates needed beyond it.

## R01 repair audit and targeted checks

1. **R01 item 1 — repaired mechanism, incomplete implementation.** The density hypothesis genuinely prevents the accumulated drift. The crossing constant 4 is valid in its stated domain. Required change 1 resolves the remaining prefix and indexing gaps. N3X has only 48 runs satisfying the density condition; its script does not check the centre-displacement conclusion of (vii), and it does not exercise short-prefix use in an induction.

2. **R01 item 2 — substantively repaired.** Family-wide no-addition is removed. Bulk additions use |x_T|≤ε_b H only at visited T, and swap comparisons use the explicit intermediate T−j, whose centre changes by O(H̄/m1). X2's exceptional set grows by at most two indices, within 17. End-phase swaps use the direct V identity, not an unjustified intermediate balance claim. R01's unbalanced top-tail configuration is consequently outside the asserted visited-path balance argument. Required changes 1 and 4 concern completing that argument, not reinstating the false uniform assertion.

3. **R01 item 3 — principal repairs present.** The normalization/sign of the first-order term are corrected; the RSS reference is distinguished from the ridge score; X1 gives separate absolute errors. Required changes 2 and 4 remain before their advertised uniform consequences can be relied on.

4. **R01 item 4 — random selection handled correctly in principle.** D5 conditions only on xi-defined intervals and separates the diagonal; adaptive N and band members use crude uniform bounds. E5 is applied to the deterministic full null sample, with removal errors ≤15H̄ and ≤15. Conditional-on-X zero-pair bounds are the right treatment for the actual block. No union bound over all N is needed once these deterministic simultaneous implications are established. Required change 3 makes the theorem's notation match this construction.

5. **R01 item 5 — fixed.** s0≥1 is explicit. FS is a finite population condition and FS-prime is not part of the claims. I find no residual random-partition hypothesis smuggled into C1 through FS-prime.

6. **R01 item 6 — principal algebra fixed, boundary wording still wrong.** The band error is now compared to its budget and leave-one-out is only proposed. Required change 5 removes the remaining false equivalence.

**B3 and entry, specifically.** D7 compares the outer deleted band to an even farther tail which is kept, so its epsilon-prime times kept-count bound has the correct direction. In B3 Case A, extra deleted negatives increase the signed kept sum by at most their count times H̄+w; the D7 correction therefore has the correct sign and size. E5 then gives J-double-prime≤5m and a centre bound with room under epsilon-b H. In Case B the omitted calculation is w times the near-zero count = O(pϖ²+ϖ log n)=o(1) under the locked exponent. At entry, (4.1) and m<m1 exclude a finite edge on the wrong side of zero; D7 bounds the number of points beyond each finite edge by 2m1, and D8 then removes the outward band defects. For an infinite edge the corresponding outside band is empty. The centre entry bound uses only B3 at the previous bulk step. I found no additional obstruction here once the prefix induction is repaired; the same full-sample estimates are uniform in N. These conclusions are viability checks, not a completed line check of X4.

## Optional suggestions

1. Add a deterministic test specifically for every conclusion of X3(vii), including short prefixes, the Q/Q+1 boundary and initial holes already wider than 4ϖ. Keep it separate from evidence about the statistical theorem.
2. In X4, record a small dependency table: prefix structure → occupancy → X2 at current/one-move sets → gain ordering; B1(i) → B2(i) → B3(i) → move comparison. It would make the absence of future-step assumptions inspectable.
3. Preserve the explicit distinction between empirical fitted δhat in N1X and the exact reference δ of X1–X2; neither the fitted perturbation nor 121 successful paths certifies the constants in the theorem.
