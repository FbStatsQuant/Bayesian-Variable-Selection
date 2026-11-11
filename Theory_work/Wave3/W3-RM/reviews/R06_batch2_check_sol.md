# R06 — Batch 2 independent lemma check (Sol, high)

Review date: 2026-11-09. Read-only review of the requested batch; no git operations, no delegates, no source edits. Verdicts concern the new arguments and their stated scope; inherited source statuses are not upgraded. SAND-R/SAND-R′ are treated as given, as requested. Line numbers refer to the files inspected.

| Item | Verdict |
|---|---|
| 1. L1b_rss: Lemma τ and B2τ | VERIFIED-WITH-AMENDMENTS |
| 2. L1_fixed: B1′ and updated RM-F assembly | VERIFIED-WITH-AMENDMENTS |
| 3. L2_NAF: [P1], [R03-1] | VERIFIED |
| 4. L0_core: archive corollary | VERIFIED |
| 5. L4_formR | VERIFIED-WITH-AMENDMENTS |
| 6. L7_examples | WRONG (E-F2 as written; overbroad exclusions); the principal R examples and E-F1 verify |
| 7. Statement/proof consistency | VERIFIED-WITH-AMENDMENTS |

No FATAL finding. MAJOR findings: 5 (missing energy hypothesis in E-F2), 6 (polynomial-decay exclusion), 7 (factor scope/exponent), 8 (FAC-PK qualifications). These do not refute RM-F or RM-R under their full listed hypotheses.

## 1. Lemma τ and B2τ — VERIFIED-WITH-AMENDMENTS

Checked the full cited GROW L3_sandwich.md, L0_toolkit.md and GEN L1_lemmaE.md, including GEN:13,19–38,42–50,57–85,92–100 and GROW L3:15–93. The new proof is mathematically sound for sufficiently large n.

The AM–GM calculation gives exactly
`2σ h_n sqrt(Λ_A) ≤ h_n/sqrt(n−1) · ((n−1)σ²+Λ_A)`.
The D1/D2 loss is bounded by `τ_A²(4n^(2/3)+t_n)`, using τ_A²≥σ². Thus the proposed lower bound follows. The nested likelihood ratio uses the lower bound for **A′**, so the denominator really is `2τ²_A′`; ν=(n+0.02)/2 gives the displayed prefactor. On the block family, both ω^τ log n and ϑ^τ log n vanish: their largest displayed contribution is O(n^(−1/3)log n), with the additional O((log n)^(3/2)/sqrt(n)) term also vanishing.

Every intermediate U_(s−1) in step (i) is a subset of C_b excluding l_s and contains S0∩C_b. In particular it has size ≤15 even when the selected block has size 16. Successive mean gains telescope because these are nested orthogonal projectors. Monotonicity of Λ gives the claimed sum bound. Consequently τ²_Ũ≥τ²_U(1−ζ_n), ζ_n=16ηlog n/(n−1), and ζ_n log n→0. The W_b bound remains σ²dW_b≤τ²_UdW_b. Division gives the source (3.3), with the harmless weakening 4κ_E/d≤4κ_E and with ϑ replaced by ϑ″. The choice of ε1 and the geometric ladder remain valid with fixed positive margins. For junk exclusion, |δ+σZ|/τ_U≤sqrt(ηlog n)+(σ/τ_U)|Z| is correct, including signed δ. The denominator replacement has the same vanishing error.

No hidden NEG use was found. GROW L3:47 and :89 are its only substantive uses. Truth inclusion (:78–84) uses visibility and the **RSS ceiling**, GEN L1.4(b); the old noise floor can remain available for the score expansion and does not impose a σ-normalised leakage hypothesis. W_b's χ² rank/tail and the event Z depend only on fixed-design projections and the within-block floor. They are unchanged. The implication from the old σ-form to the τ-form and the quantifier arguments in B1/B1′ are valid.

1. **MINOR — L1b_rss.md:8–9.** τ²_A is called “the population value of RSS_A/(n−1)”. Literally its conditional expectation is `τ²_A − σ² rank(P_A)/(n−1)`, since the residual noise rank is n−1−rank(P_A). **Fix:** call τ² the population residual energy scale (or its asymptotic value for bounded-size A), and give the exact expectation if desired. This does not change the proved floor.

2. **MINOR — L1b_rss.md:14–15.** “The implication is strict whenever some block leaves a non-vanishing part of the mean energy unexplained” is too categorical. Positive residual energy does not force a leakage constraint to distinguish the two forms; η=0 is an immediate counterexample, and orthogonal truth/null groups have δ=0 outside Q under both conditions even with positive unexplained energy. **Fix:** say the replacement is weakly weaker and can be strictly weaker; residual energy enlarges the permissible positive threshold. Do not assert strictness from residual energy alone.

## 2. B1′ and updated RM-F assembly — VERIFIED-WITH-AMENDMENTS

B1′'s partition construction is correct, with common constants and common Q essential. Any T of size ≤16 can be one block with singleton complement. For leakage, C=U∪{l} has S0∩C=S0∩U because l∉Q⊇S0. Hence its restricted quantifier includes precisely the requested U. The same argument works for τ-normalisation without any change of constants.

The RM-F paragraph at L1_fixed.md:98–104 correctly uses B2τ for the new leakage condition. Under N-χ, BM-∞ supplies BM-Q; under N-D it is assumed explicitly. All four interface properties then assemble through RM-0. No missing premise was found in this assembly.

3. **MINOR — L1_fixed.md:12–19,38–43,56–57; L1b_rss.md:14–16,66–67.** The symbol `(L-gain)`/`(L_b)` now means the τ-form in STATEMENT:92–95,111, but the earlier text still identifies it with GROW G3c (which explicitly has σ²), and B2's old proof calls its statement exactly the source statement with only the size condition changed. B2τ and RM-F resolve the mathematics, but the names have become inconsistent. **Fix:** explicitly label the old hypotheses `(L-gain^σ)`, `(L_b^σ)` in the inherited lemmas; state B1/B1′ for either normalisation; replace the dangling “B2 applies” at :56 with B2τ for the v1.2 convention. In particular τ-form leakage does not imply GROW G3c verbatim.

## 3. [P1] and [R03-1] in NA-F — VERIFIED

Read GROW L2_NA_TL.md:11–22,38–46,50–69 and LOC2 L1_toolkit.md:9–42. Step 3 has the uniform deterministic bound
`max Z² ≤ 2log p+2h log n+o(log n)`.
The approximation cross term is o(log n), since a_n²=O(log n) and ρ²G_n=o(log n). For each **fixed** h<1/2 the gap is `(1−2h)log n−o(log n)−O(log log n)>0`. There is no uniform-in-h claim near 1/2, and none is needed.

Step 4 does not spend another positive fraction of log n. LOC2:37–42 explicitly preserves GROW's score reduction because ω_n log n→0 on the polylog lattice. Inserting c_n leaves exactly −1/2 after bounding the likelihood-ratio excess by 1/2 (GROW:43–46). Thus the entropy relaxation and score conversion are compatible for every fixed h<1/2.

For N-loc, a⊥b gives the exact normalised-direction distance `2(1−1/sqrt(1+t²))≤t²`. The approximants belong to span(X_(Q∪{l})), are deterministic, and their count is ≤p2^ν. A strict limsup below 1/(2log 2) permits a fixed h<1/2 eventually. Special case (a) is correct and has exact directions. The empty-family equivalence is correct: if any null or any outside column exists, T=S0 already supplies a pair, so the family is empty exactly when Q=S0=[p]. NA is then vacuous; a deterministic singleton avoids log 0. No amendment required for these changes.

## 4. Archive corollary — VERIFIED

Read v3_engine.h:370–420 and the LocalArchive defaults at :46–52. Each iteration appends exactly one completed scan at :407; a strict improving move increments moves at :412; absence of improvement sets returned=C.S and local_certified=true at :414. local_limit starts false and is set only at :410. RM-0(a)'s deletion path has d=|S̃0\S0| moves. The cap is at least |S̃0|>d because s0≥1, so the cap branch cannot occur. There are exactly d+1 scans, including the last scan at S0. The corollary's explicit qualification that enumeration branches refer to the hypothetical search is necessary and present at L0_core.md:65–66. No public reported-model certification is inferred.

## 5. Form R bridges and assembly — VERIFIED-WITH-AMENDMENTS

S1 follows from the triangle inequality and column standardisation; S2 is part of Setting R. S3 is LOC2 L1_toolkit.md:45–50 with an envelope exponent κ′>κ to absorb the +1 in |Q∪{l}|. Only population floors on the displayed sets are used; a global floor or upper spectral bound is not smuggled into B8a/B8b.

B8a matches LOC2 L2_NAR.md:15–41, including the independent Gaussian extension and deterministic objects. D-loc supplies frames with **one functional each**, not a frame containing all residuals for one l. There are ≤p2^ν such frames. N∪{l}⊆Q∪{l} supplies the inverse and positive residual variance by interlacing/Schur complement. Atoms are coordinate functionals of variance 1, permissible under the exact source condition “Var a ≤ 1”. The difference of zero-padded regression vectors is supported on T⊆Q, its subtraction has the correct sign, and its maximum ℓ1 norm is bounded by the stated envelope L_n. If the source reserves L_n for the exact maximum, rename the envelope and take that maximum; the rate follows by domination. R3 is precisely the assumed variance ratio. No latent variables or data-dependent coefficients are needed.

B8b uses fixed beta-min to dominate O(q+log n) fluctuation costs, as LOC2:33–36 requires. Its conditional Gaussian bounds are uniform on the floor event, then integrated. The lattice family has a Gram floor by interlacing on Q∪{l}. B9 is an exact match, not merely an appeal to a global floor: APP L1_POST.md:23–25 states

> “(i) λ_min(Σ_{n,S}) ≥ φ² for every S with |S| ≤ min(p, s₀ + j₀), for a fixed φ ∈ (0, 1]; and (ii) λ_min(Σ_{n,S}) ≥ ψ_n for every S with |S| ≤ k̄_n, where ψ_n √n/(log n)^{3/2} → ∞.”

The j0, mbar and kbar formulas at APP:20–21 agree with STATEMENT:122–124. The bound φ≤1 is automatic for nonempty unit-diagonal principal matrices. APP(b) gives joint-law posterior concentration and boundedness converts it to [POST]. With SAND-R/SAND-R′ taken as given, RM-R assembly consumes exactly the four interfaces and deterministic feasible Q. No independent mathematical gap found.

4. **NIT — L4_formR.md:44; L7_examples.md:26.** Citation drift: UNI L2_k0.md:151–153 is the end of NA and the TL heading; the TL argument is :154–155. UNI STATEMENT:172–175 is delivery/OBS-k, not the corollary table; the relevant entries are :182–184. **Fix:** update the ranges. The intended source contents do exist and were read.

## 6. Examples — WRONG as currently stated

**Verified portions.** E-R1 is correct: because T⊆Q, `T∩[Q∩(B(l,r)\{l})]=T∩B(l,r)`. UNI L2_k0.md:139–149 therefore supplies D-loc exactly, including o(log n) neighbourhood size, fixed ℓ1 bound, unit-variance atoms and η→0. Its relevance-set enlargement, leakage and localisation bounds at :66–77,97–109 give the other assumptions after enlarging κ. E-R2's latent extension and frames match LOC2 L4_LOCd.md:70–114, including frame dimension 2, ℓ1 envelope 1/b_lo, variance ratio η=0 and exact independent-group covariances. S0⊆Q0 ensures H_l contains the truths. The class includes VN sequences by APP L5_VN.md:74 onward; the claim is existential, appropriately.

E-F1 genuinely has the needed universal-partition source statement: GROW STATEMENT:119–123 says “any block partition with blocks of size ≤16”. More strongly, GROW L5_instances.md:58–65 proves visibility and leakage for **any U**, not only sets inside one chosen block; constants and Q are partition-independent. The Markov-direction count :66–68 is p(|Q|+1)². H0 is verified at :50–52 with fixed coefficients. Thus B1′ and the BM-Q implication are legitimate. E-F3's **positive** block-relative instance is supported by GROW STATEMENT:127–137 and the written certificate in L5_instances.md:79 onward; fixed-p enumeration is acknowledged.

5. **MAJOR — L7_examples.md:55–66,89 (E-F2).** “Signal condition: BM-∞ only” does not establish (T1-F)'s energy bound ‖μ‖²≤Mn. Floors give SE_λ and SE_w for every size; bounded Q gives L-size, L-feas and N-χ; the calculations of V and δ=0 are correct. But BM-∞ is only a lower bound on the smallest coefficient, and Setting F does not bound coefficients above.

   **Explicit counterexample to the missing implication (and to the unqualified example):** let p=floor(n/4), take centred orthogonal columns with XᵀX=(n−1)I, singleton groups, S0={1,2}, θ1=n, θ2=1, σ²=1. All written E-F2 structural assumptions and BM-∞ hold, as do V and zero leakage outside Q={1,2}. Yet ‖μ‖²=(n−1)(n²+1), so no fixed M works. For the actual D0 score this is consequential: after normalising Y, the second column explains only O_P(1/n) response energy, whereas the ridge residual after fitting column 1 stays of order 1. Adding column 2 improves the log likelihood by only O_P(1); its determinant penalty is (1/2)log n+o(1), and its BB prior ratio is 2/(2p−2). Hence `F({1,2})−F({1})=−(1/2)log n−log(p−1)+O_P(1)→−∞`; posterior concentration on S0 fails. This calculation uses the exact D0 formula in GEN L1_lemmaE.md:54–55, not the bounded-energy expansion outside its scope.

   **Fix:** explicitly assume ‖μ‖²≤Mn in the class, equivalently impose bounded coefficient energy here. A fixed upper bound on |θj| suffices since s0 and group sizes are fixed. Retain BM-∞ to allow coefficients tending to zero. Add this condition to row 4 of table 7.4. Under that amendment all the displayed E-F2 verifications establish RM-F.

6. **MAJOR — L7_examples.md:73–77.** The polynomial-decay row changes a proof envelope into a necessary size and falsely excludes the whole class. LOC2 STATEMENT:91–93 explicitly says |Q|=O(n^(1/(2α))) is “an upper bound; the decay is an envelope”. **Counterexample:** Σ=I with fixed nonzero truth coefficients and polynomial p satisfies the polynomial-decay hypotheses for every α>17/2 and PTV, and is also a UNI-0/RM-R instance with bounded Q (enlarged when necessary). Nothing forces a polynomial leakage set. **Fix:** say the particular L6 proof uses a polynomial-size envelope, which is outside the polylog-Q bridge as stated; the class overlaps RM-R and is not universally excluded.

7. **MAJOR — L7_examples.md:78; STATEMENT.md:218–219.** The one-factor row says p is not polylogarithmic without such a growth assumption, and replaces UNI-1's strict exponent condition by p<n^α0. UNI STATEMENT:113 requires **limsup log p/log n<α0(κbar)**; pointwise inequality does not imply this (p=floor(n^α0/2) is a counterexample to that implication). STATEMENT:219 further advertises the broader p<n/2 range as if it were the general UNI-1 range; UNI:138 and :187 explain that FACB's exact-CS result beyond the exponent cutoff is a separate family-specific result.

   **Counterexample to the universal non-instance label:** fixed-ρ compound symmetry, one truth, p=ceil(log log n) is both a UNI-1 structural example (Ψ=(1−ρ)I, singleton exposure groups, κbar=1, strict exponent limit 0) and a LOC-BF/RM-R example, using Q=[p] with polylog size. Thus even when every null leaks, this does not violate L-size. **Fix:** retain the exact UNI exponent and visibility/exposure assumptions, qualify the exclusion by super-polylog p and the needed leakage/noncancellation conditions, and distinguish FACB's separate larger-range theorem. Do not infer an all-factor p<n/2 theorem.

8. **MAJOR — L7_examples.md:80.** The FAC-PK row quotes NEG for generic “compound symmetry with p>K”. The cited REPORT.md:7–9,24–31 restricts it to **exact Gram K<p≤n−1**, fixed ρ, nonzero sign-corrected total signal, (PK) liminf p/K>16/15 and (PB) all but boundedly many blocks of size 16, with execution premises. p>K alone is not the theorem's hypothesis; p≫n is explicitly open. Saturation by itself also is not the definition of L-feas. **Fix:** include those restrictions, state Q=[p] is infeasible when p>K, and quote only the qualified LS0 negative result. Do not claim full-method failure. No counterexample to the properly qualified source NEG is asserted.

9. **MINOR — L7_examples.md:41,70–71.** Two negative membership claims overreach their arguments. A latent construction for LOC-BF does not prove the class cannot satisfy D-loc: bounded independent groups satisfy it with N_l=Q∩(G(l)\{l}), bounded ν and exact residuals. Likewise a within-block certificate for S5 proves the block-relative instance but does not by itself prove failure of all partition-free visibility inequalities. **Fix:** say “the supplied construction uses D-R directly; D-loc is not needed” and “partition-free membership is not established by this certificate”, unless a masking conditioning set is exhibited for S5.

## 7. Consistency with v1.2 — VERIFIED-WITH-AMENDMENTS

The operative bridge table matches the proved interfaces: B2 explicitly points to B2τ, B5 permits fixed h<1/2 and uses the polylog toolkit, B7 points to the separate rate delta, B8a's D-loc statement in the locked statement is a sufficient **fixed-L special case** of L4's broader envelope form, and T1-R matches APP LSF exactly. The updated RM-F/RM-R assembly paragraphs use these versions. The archive claim includes the hypothetical-enumeration qualification in the lemma; it should be retained whenever restated. No missing proof file was found for the listed bridges (E4 has its own L5 file; its existing check is not repeated here).

10. **MINOR — STATEMENT.md:183; L1_fixed.md:12–19; ASSUMPTION_MAP.md:23,27–28,42–44.** The statement's B1 row is valid if its target means the newly defined τ-form, but L1_fixed still equates that target with σ-form G3c (finding 3). The companion assumption map, referenced by the statement, still describes σ-normalised leakage, only p n^o(1) approximants, n^−2 localisation, and lists the already adopted τ change as a candidate. **Fix:** synchronise terminology and mark old forms as sufficient v1.1 cases; update the map to P1/P2/P3a. The active §3 hypotheses and B2/B5/B7 table entries themselves do carry the new weakenings.

The examples/scope sentences in STATEMENT:215–219 inherit findings 5–8 and need the same qualifications. The statement's input map is otherwise a many-to-many summary, not a claim of minimal hypotheses: for example T1 supplies energy to several bridges as well as POST, and SAND uses L-size only through its weaker consequence log|Q|=o(log n). No additional theorem-level gap was found in the reviewed material.
