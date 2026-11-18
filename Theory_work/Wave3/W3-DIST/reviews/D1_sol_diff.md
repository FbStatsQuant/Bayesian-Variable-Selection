D1 diff check — STATEMENT.md sha256 e8503b045fde127a; lemmas/X.md 15d23ee7a05e96a1; lemmas/DIST12.md 9b468ca7d9e4d185
Part B sha256: work/C_size/S.md 956fdbb925c113a5; work/D_output/P6_DISTC.md 5e3f9116a9ce9d36; work/D_output/COR_C.md 55d8b14f968de040; work/E_bridges/B3.md 95ed27da8ba36fa1; work/E_bridges/ASSEMBLY.md e2bb6ed765be030f

Independent mathematical diff check, D1, reasoning effort high. The brief was read first and in full. This review checks the specified repair, amendments and statement changes; it does not repeat the previous line checks of unchanged arguments. No agents, cluster jobs, state-changing git commands or temporary files were used. Small comparison/hash computations ran with nice. Only this output file was written.

## Findings

### D1-01 — MINOR — work/D_output/P6_DISTC.md, amendment A-10, lines 480–483: likelihood dimension and inverse-gamma shape are mixed

The inverse-gamma moment formula is correct, but the argument applies it to the wrong combination of likelihood and prior. The coded working likelihood has the n-dimensional normalization (2πv)^(−n/2), even though the observed response is centered. Its standardized-scale prior has shape 0.01. The equivalent N = n−1 dimensional contrast likelihood instead uses shape 0.51, not 0.01. This is precisely the extra half-power of v in the locked T01(i) identification. Thus a = 0.01, b = 0.01 s_y² and the claimed N-dimensional bound do not together bound the coded marginal likelihood. For small v, the omitted v^(−1/2) factor cannot be bounded by one.

This leaves a short gap in the proposed repair of L2D-05, not a failure of finiteness. Minimal repair: use the contrast likelihood with a = 0.51 and b = 0.01 s_y² > 0. Integrating the proper coefficient prior gives

    m_b^c(S) ≤ (2π)^(−N/2) b^(−N/2) Γ(0.51 + N/2)/Γ(0.51) < ∞.

Then T01(i) gives m(S) = c_n(s_y) m_b^c(S), where 0 < c_n(s_y) < ∞ on a completed run. Alternatively, prove finiteness directly on the standardized scale with the n-dimensional likelihood and IG(0.01, 0.01), using its negative n/2 moment. Either repair uses the existing hypotheses. Positivity and the downstream transfer arguments remain valid.

### D1-02 — MINOR — STATEMENT.md, DIST-C (C-i), lines 293–295: SCR-4 is still missing from the statement

The phrase “on the complementary success event” has not been replaced by the qualified event requested in P6_DISTC.md SCR-4. The complement of the displayed intersection also contains stopped runs and completed runs with π(𝒯) < e^(−λt). On the first, the stated predictive object need not be returned; on the second, the complement supplies no bound on its bad mass. The proof at P6_DISTC.md §6 (C-i) correctly uses a smaller event and does not prove the predictive bound on that literal complement. This is within the statement/proof matching check; the changelog's DIST-C row cites SCR-1 through SCR-5.

Minimal repair: replace the phrase by

    on {completed} ∩ {π(𝒯) ≥ e^(−λt)} ∩ {Π̂^𝒯(B_n) ≤ e^(−(c−λ)t)}.

Then the predictive inequality follows exactly from P6(c), as already proved. No proof-file change or new hypothesis beyond those intended is needed. The probability display and the new arbitrary-threshold transfer are correct.

### D1-03 — MINOR — STATEMENT.md, final bridge bullet, line 413; changelog: an additional range reduction is not recorded

The old v1.3.1 bullet asserted the bridge failure bound uniformly for M ≤ √n; the current bullet asserts it uniformly only for M ≤ √n/log n. This is a literal WEAKER range claim in the bridge summary. It is not the already-recorded v1.3 reduction of the reader theorem's range: that reader reduction is present in both versions compared here. No row from 1.4 onward identifies this additional change to the bridge bullet. The current smaller range is proved in B2.md and ASSEMBLY.md and suffices for the reader theorem.

Minimal repair: add this range change to the 1.4 bridges row as WEAKER, non-target, or restore the larger bridge-summary range with its uniform concentration justification. No target theorem's level range is reduced by the current edit.

### D1-04 — MINOR — STATEMENT.md changelog, 1.4 rows on Corollary C (line 477), reader Remarks (line 478), and bridges (line 483): tags miss literal changes of strength

Three distinctions are needed in a statement-change audit:

1. Corollary C gains the conclusion that the true model is “the model the method reports as most probable.” The old retention sentence concluded only membership and π(𝒯) > 1/2. This is an additional conclusion of that reader corollary and should carry STRONGER, alongside the faithful description corrections. Its proof is correct (COR_C.md C2 and P6_DISTC.md Corollary R1). Its being available from a master result does not make the additional reader conclusion EQUAL; the earlier changelog similarly tags the added reader size conclusion STRONGER.
2. Remark (1) now requires (A3), (A4) on the window of M = n ε_n²/log n. The old remark claimed all those radii without this qualification at each radius. Adding the level-dependent assumption is a WEAKER applicability claim for the remark, even though the remark is outside the protected reader displays and the corrected statement is proved. “EQUAL (remarks)” does not describe this literal change. Constant renaming and the explanatory edits can remain EQUAL.
3. The B2 determinant-to-(ND) implication now covers every m satisfying min{p, s₀ + m} ≤ q, rather than only m ≤ q−s. Since s₀ ≤ s, the old range is contained in the new one; at q = p the new range includes all m, whereas the old one stopped at p−s. That part is STRONGER as a bridge implication. The other parts of the row really are WEAKER: domain restriction for B0, positivity in B3, and withdrawal of false uncapped numerical assertions. A blanket WEAKER tag misses this mixed direction.

Minimal repair: split these rows or use explicit mixed tags with the scopes above. These are tracking findings, not failures of the corrected corollary, remark or bridge proofs. None weakens TC1–TC9.

### D1-05 — NIT — reviews/DIFF_STATEMENT_v131_to_v147.patch, header and entire hunk: this is a deletion snapshot, not the named two-version diff

The artifact says “deleted file mode”, has +++ /dev/null, and deletes all 426 lines of v1.3.1. It contains no v1.4.7 additions. I recovered all deletion-hunk lines, authenticated them against git blob d1277b4, and compared that old text in memory with current STATEMENT.md. This allowed the requested audit to finish. Minimal repair: regenerate an actual v1.3.1-to-v1.4.7 unified diff. This finding does not block any mathematical conclusion here.

## Part A — detailed repair check

**A1, geometric sum.** Let a = e^(s₀)q and j = j₁+1+i. For s₀ ≥ 0 and integer j₁,i ≥ 0,

    j₁+2+i ≤ (j₁+2)(1+i),  j₁+2 ≤ e^(j₁+1),  1+i ≤ e^i,
    (j+1)^s₀ q^j ≤ a^(j₁+1) a^i.

The inequalities remain valid for s₀ = 0; no division by s₀ occurs. Condition (d), using s₀ ≤ s, gives a ≤ n^(−1/8). Condition (a), n ≥ e^8, gives n^(−1/8) ≤ e^(−1) < 1/2. Thus the geometric sum is at most 2a^(j₁+1). Finally j₁ = ceil(32t/log n) gives n^(−(j₁+1)/8) ≤ e^(−4t). The replacement of K_s by 2 is correct at every stated edge case.

**A2, constants throughout X.** M₀ ≥ max{16,(A+1)s}, A≥1 and s₀≤s imply M₀ ≥ (s₀+1)/2, including s=0. Hence (s₀+1)log n ≤ 2t and |S|log n ≤ 34t on the small-model range. Consequently N2 gives C_P = C_A′·34+4, and N3 gives C_x = (A+1)·34+2, as stated. For S empty, the projection is zero, so N2's omission of that set is harmless.

I followed C_d, C_x, C_P, Λ, C_Q, C_β, C_v and C through §§0–8. In §5, the cross-term, projection, reference-cost and likelihood-penalty bounds require only Λ ≥ 32C_x, 8C_P, 8B/σ² and 48/log 2, respectively; none requires C_d≥s+33. The remaining multiplicity is absorbed by n^((A+1)s₀)≤e^t and t≥(s₀+1)log2, both supplied by M₀. In §6, the center, scale and variance bounds use the new constants directly. The coefficient fluctuation uses |S|log n≤34t and log n≥1 to give 2|S|log2+4t≤(2·34+4)t. Thus the final C remains valid after it is decreased for large s.

C_m still depends on s. It bounds m_n(t)+s₀ and enters ε₂, ε₃ and condition (c), hence n₀, through E3. The fractional-moment argument only needs the resulting uniform ε₃≤1/(8A+2); it does not multiply its final radius by C_m. N2 and N3 are unioned over all sizes with summable weights, so their probabilities do not acquire a C_m factor. E1, E2, the above-cutoff tail in §4, and the assembly in §7 introduce no hidden sparsity-dependent radius constant. The s and c_D dependence in condition (d) also enters n₀ only. No unchecked “constant times t” in the affected argument needs the old C_d or a further s-dependent constant in C.

**A3, Markov product.** The three numerical factors are 2·2·2=8. The displayed bound is

    8·4^s₀ exp(3B/(2σ²)) (8A+4)^(s₀/2) e^(−2t)
    ≤ [2·4^(s+1) exp(3B/(2σ²)) (8A+4)^(s/2)] e^(−2t)
    = C₅ e^(−2t) ≤ e^(−t).

The last inequality holds because t≥M₀log n≥log C₅. There is no missing factor two.

**A4, M₀.** For s≥0, log2+(s+1)log4≤2.1(1+s). For A≥1, (1/2)log(8A+4)≤A+1 (the difference is positive at A=1 and increasing). Therefore

    log C₅ ≤ 2.1(1+s)+s(A+1)+3B/(2σ²)
           ≤ 4(1+s)(A+1)+3B/(2σ²).

The same last bound dominates (A+1)s. Taking the maximum with 16 proves exactly M₀≤16+4(1+s)(A+1)+3B/(2σ²). No asymptotic estimate for K_s is left in the proof.

**A5, X′.** Section 9 uses C_m and its own primed constants and M₀′=max{16,(A+1)s}. It uses neither C_d nor K_s nor C₅; its references to §§2,4,5,6 use the specified surviving noise/tail facts or replace the small-model constants by primed ones. In particular its variance step uses C_β′ and C_v′, not the revised unprimed C. The repair does not alter this argument or its admitted sparsity dependence.

**A6, DIST12.** On the D.4 range, M₀≥(A+1)s≥2s, so 2s log n≤t and the ceiling adds at most log n≤t. Thus d₁ log n≤34t, including s=0, and C_T=4[34(A+7)+8] is correct. The entropy estimate's +8 covers 6log n+2t. D.6 uses d₂ and C_T′, not the sharpened d₁ estimate, and therefore needs no extension of this estimate to a different lower-t range.

The actual D.4 radius constant is C=(C_X²+C_X/2+1+C_T)^(1/2), with C_X free of s as just checked. It depends only on (A,σ²,M,M′). The displayed ε_n² upper bound follows by multiplication by C²log n/n. Raw s=s₀^r is essential: the sparse direction is b−β*, which includes true columns dropped from the sample, and is bounded using |S|+s, not |S|+s₀. The deterministic d₁ and d₂ retain the raw sparsity correctly.

**A7, TC3.** Consequence (c)'s explicit bound and its EQUAL-on-TC3 changelog tag are CONFIRMED. It proves M₀=O((1+s₀^r)(A+1)) for fixed (σ²,M,M′), with a radius prefactor C independent of s₀^r. The corresponding (1+s₀^r)log p_raw/n rate is read with A fixed, as stipulated in (RD); the proof does not supply an A-independent radius prefactor, since C depends on A. Likewise this is not a theorem allowing s to grow with n: n₀ may depend strongly on fixed s. These qualifications preserve the stated TC3, and no weakening of TC3 is necessary.

## Part B — hunk-by-hunk results

- **S.md:** A-5 answers L5-01 correctly: the two simulated quantities are dependent, whereas the exact noncentral chi-square law and Step 6's marginal-tail union bound are correct. Withdrawal suffices; rerunning or repairing the simulation is not needed to validate the proof. A-6 answers L5-02 and correctly distinguishes the K-truncated hypothesis from the stronger full-p hypothesis, especially at m=K<p. A-7 answers L5-03; the degenerate residual/signal cases are separately handled. All three hunks leave the proof valid.
- **P6_DISTC.md:** A-8 answers L2D-02: the first initial draw proves nonemptiness, which is all R1 and W need; it does not prove empty-model membership. A-9 answers L2D-03 and matches the conditional v3_unavailable_estimates call and the optional LS0 branch in the code. A-10 answers L2D-05, but needs D1-01's dimension/shape correction before it is a valid finiteness proof. The intended positivity/finiteness result and downstream algebra survive that correction.
- **COR_C.md:** A-3 answers L2D-04 and correctly restricts to nonempty sets. A-4 answers L2D-01 and the completion qualification in L2D-03. Neither changes the data-event division proof or deterministic retention. The two current reader conclusions are proved under EX-A and the consumed Theorem A.
- **B3.md:** A-1 answers E-02 with the correct capped union cardinality. A-2 answers E-05. An admissible deterministic centered, standardized n-by-p completion with exactly s nonzero true coordinates can be chosen when n≥max(3,2s); the interfaces need not hold on the replacement outcomes. It is independent of the noise. Applying item 6 to the fixed-dimensional completed objects and then discarding {p_ret≠p} costs a probability tending to zero. The interface event is measurable and contains the B1/B2 good event. No new population assumption is introduced.
- **ASSEMBLY.md:** A-6 answers E-03: 3+2=5 consumed failures give 5n^(−2cM), and n≥10^(1/c), M≥1 imply it is at most (1/2)n^(−cM); the existing n_R pays for the other half. A-7 answers E-04: c₃>0 suffices to choose the fixed u; enlarging C₃ alone is legitimate. A-8 imports B3's valid completion and answers E-05 for this assembly. Parameter dependencies, the common exceptional set, and the single n₀ over the whole reader range are preserved.

Every Part B hunk answers a listed finding; none is an unexplained addition. The only incorrect repair among them is the normalization in P6 A-10 (D1-01).

## Part C — statement-change audit

The deletion hunk was authenticated against the named old blob and compared in memory with the hashed current statement. The scope of “EQUAL on TC3” and “EQUAL for TC9's mathematics” is respected below; neither is a claim of literal equality of all surrounding explanatory words.

| Changelog row (current STATEMENT line) | Verdict | Reason |
|---|---|---|
| 1.4 — reader Setup (473) | CONFIRMED | EQUAL for the specified TC9 mathematics: retained-dimension description is made faithful to the coded object; the probability of the affected design samples is charged to the existing exceptional bound. Literal priors on those exceptional samples do differ, as the row explicitly admits. |
| 1.4 — identifiability description (474) | CONFIRMED | WEAKER descriptive assertion; formal (A1)–(A5) and reader displays are unchanged. |
| 1.4 — Theorem A/common event, window and Example (475) | CONFIRMED | Joint conclusion is STRONGER and is proved; the fixed-level and joint-Gaussian/common-K qualifications clarify the intended examples and window. No weaker reader theorem results. |
| 1.4 — Theorem B, b_n>0 (476) | CONFIRMED | WEAKER hypotheses, correctly excludes the negative-envelope counterexample. |
| 1.4 — Corollary C (477) | CONTESTED | Faithful description corrections are supported, but the added HPM conclusion is STRONGER; see D1-04. The proof is valid. |
| 1.4 — reader Remarks (478) | CONTESTED | The added window premise is WEAKER applicability for the general-radii remark; see D1-04. Constant bookkeeping is EQUAL. |
| 1.4 — law-free reading and C versus L₀ (479) | CONFIRMED | EQUAL for the named targets: allowed dependencies and formal interface hypotheses remain the same. The corrected explanation accurately distinguishes the rho-prime requirement of X from L₀. |
| 1.4 — DIST-3 constants/direction name (480) | CONFIRMED | Supported normalization and dependencies, with no change to the oracle form or required interfaces. |
| 1.4 — DIST-C (481) | CONFIRMED | EQUAL for the named deterministic transfers: the threshold form follows from C-0 and the same data event; the lower-n qualification is an allowed enlargement of n₀. RM2 is explicitly unused and conditional. SCR-4 still needs implementation (D1-02). |
| 1.4 — Lemma T route and V definitions (482) | CONFIRMED | EQUAL lemma statements; the obsolete unproved route is not a premise of the stated bound. |
| 1.4 — bridges (483) | CONTESTED | Correct repairs, but mixed directions: the B2 implication is STRONGER while the described false-claim/domain repairs are WEAKER (D1-04). Also add the omitted range change D1-03. |
| 1.4.1 — Lemma S upper endpoint (484) | CONFIRMED | EQUAL as a disambiguation of the explicitly K-truncated proof definition. It must not be interpreted as equality of the K-truncated and full-p qualification tests. |
| 1.4.2 — sampler opening (485) | CONFIRMED | EQUAL mathematical corollary; accurate computational description. |
| 1.4.3 — deterministic transfer levels (486) | CONFIRMED | EQUAL Lemma T and master displays; corrected application is exactly D.1–D.6, including intercept event and rounding. |
| 1.4.4 — threshold commentary removed (487) | CONFIRMED | EQUAL statements; removes commentary, not a range restriction or hypothesis. |
| 1.4.5 — NEC/S-FIT (488) | CONFIRMED | NEW-CLAIM and explicitly non-target. This confirms classification, not the independent L7 proof check of NEC. |
| 1.4.6 — mixture description (489) | CONFIRMED | EQUAL mathematical transfers; arbitrary mixtures were already covered. No point-mass premise is introduced or removed. The empirical description is not a universal theorem. |
| 1.4.7 — DIST-1(c)/TC3 (490) | CONFIRMED | EQUAL on TC3; the repaired proof establishes the claimed quantitative level and s-independent radius constant (Part A). |

**C2 — coverage and EQUAL audit: VERIFIED-WITH-AMENDMENTS.** D1-03 is the additional unlogged change. D1-04 identifies meaning changes not captured by the indicated literal tags. Other body edits in the reconstructed comparison are covered by the rows or are references, version/status text, notation, or formatting. In particular the raw-to-retained prior correction is not silently equated on dropped-column data: its EQUAL tag is explicitly scoped to TC9 and the exceptional-event argument. The C-versus-L₀ explanation likewise changes a false explanation without weakening the formal X/DIST-1 hypotheses. The frozen metric, coded prior, display formulas and best-rate target are preserved.

**C3 — current statements versus named proofs: VERIFIED-WITH-AMENDMENTS.** The following are the actual proof matches, conditional on the consumed results already stipulated in those proof files:

- Setup and (A1)–(A5): ASSEMBLY's scale reduction, retained-design good event and finite maximum over true support sizes 0,…,s support the current definition, array setting and law-uniform constants. The normal-noise response exception is null. The retained-column exception is exponentially small and is included in the common exceptional event.
- Theorem A: ASSEMBLY §§1–2, including A-6, prove both current marginal displays on a common set of data, with and without (A4), one n₀, and the required level-window quantifiers. Its Example uses joint Gaussianity or a common independent-coordinate sub-Gaussian constant. Formal (A1)–(A5) themselves have not changed.
- (A6) and Theorem B: with the newly explicit b_n>0, B3 Step 5's squaring is valid. B3 A-1/A-2 and ASSEMBLY A-7/A-8 give the current conclusion, conditional on W3-POST:Thm-1. The proof file's older restatement of (A6) is used here under the stronger current assumption, not to reassert a theorem for negative b_n.
- Corollary C: COR_C C1 and C2, with its amendments, prove the current probability and retention/HPM conclusions. The nonempty list and corrected log-weight interpretation give the exact restricted law. The mixture paragraph does not require an added theorem about selection or posterior concentration on one model.
- Reader Remarks: ASSEMBLY's level substitution and current window condition prove the corrected general-radii assertion. Its two-case maximum supplies the stated size constant. The displayed c_reader and M₀,reader formulas describe the with-(A4) normalization; the final common constants for both variants are the minima/maxima in ASSEMBLY §2. No numerical-threshold statement is needed for these conclusions.
- DIST-C and (C-ii)(γ): P6's arbitrary-Q domination and mixture definition prove that no single model need carry a majority. D-17 is a supporting report of the empirical weight ratio, not a premise of the proof; I checked that the cited decision row records the 0.5–1.2 ratio, but did not reproduce the measurements. The current predictive-success wording still needs D1-02, and the finiteness repair still needs D1-01. All other edited transfers are supported.
- Lemma S: S.md's K-truncated hypothesis and A-6 prove the current cap convention and cutoff qualification.
- B2/B3: B2's interlacing argument and capped union condition prove the expanded (ND) implication; B3's corrected union bounds, positive envelope and fixed-dimensional completion prove the current bridge. The smaller summary range is sufficient but must be logged.
- DIST-1(c): DIST12 D.1/D.4 and X §§0–7 prove exactly the explicit current bound, at raw sparsity, as verified in Part A.

**C4 — TARGET synchronization and protected clauses: VERIFIED-WITH-AMENDMENTS.** The entire reader block from Setup through Corollary C and its notation table is byte-identical in current TARGET §6 and STATEMENT §1R, so there is no difference in meaning between them. TARGET §5 is byte-identical to the d995ec2 snapshot. It contains TC1–TC8; TC9 is written in TARGET §6's additional-target paragraph. The current statements still imply TC1 (joint population metric), TC2 (the same exponential display and range), TC3 (now quantitatively proved), TC4 (the same interface hypotheses), TC5 (coded untuned prior), TC6 (the same slower bound), TC7 (oracle bound), TC8 (the same conditional deterministic transfers, with the predictive sentence read on the event of D1-02), and TC9 (both reader variants). The comparison with v1.3.1 shows no reduction of a protected display's range or rate. D1-03 and D1-04 concern non-target bridge/remark/companion wording and tracking. D1-02 must be applied for literal statement/proof matching of the predictive sentence; it does not require a weaker domination or contraction theorem.

## Verdict lines

Part A item 1: VERIFIED.
Part A item 2: VERIFIED.
Part A item 3: VERIFIED.
Part A item 4: VERIFIED.
Part A item 5: VERIFIED.
Part A item 6: VERIFIED.
Part A item 7: VERIFIED — consequence (c) and EQUAL on TC3 CONFIRMED.
Part A lemmas/X.md — Lemma X: VERIFIED; Lemma X′: VERIFIED.
Part A lemmas/DIST12.md — DIST-1: VERIFIED; DIST-2: VERIFIED.
Part B work/C_size/S.md: VERIFIED.
Part B work/D_output/P6_DISTC.md: VERIFIED-WITH-AMENDMENTS (D1-01).
Part B work/D_output/COR_C.md: VERIFIED.
Part B work/E_bridges/B3.md: VERIFIED.
Part B work/E_bridges/ASSEMBLY.md: VERIFIED.
Part C row 1.4 / Setup: CONFIRMED (scoped to TC9).
Part C row 1.4 / identifiability description: CONFIRMED.
Part C row 1.4 / Theorem A, common event/window/Example: CONFIRMED.
Part C row 1.4 / Theorem B, positive b_n: CONFIRMED.
Part C row 1.4 / Corollary C: CONTESTED (D1-04).
Part C row 1.4 / reader Remarks: CONTESTED (D1-04).
Part C row 1.4 / law-free reading and coefficient-cost explanation: CONFIRMED (scoped to the named targets).
Part C row 1.4 / DIST-3 constants: CONFIRMED.
Part C row 1.4 / DIST-C: CONFIRMED (scoped to TC8; D1-02 still required).
Part C row 1.4 / Lemma T route and V definitions: CONFIRMED.
Part C row 1.4 / bridges: CONTESTED (D1-03, D1-04).
Part C row 1.4.1 / Lemma S: CONFIRMED.
Part C row 1.4.2 / sampler description: CONFIRMED.
Part C row 1.4.3 / deterministic transfer levels: CONFIRMED.
Part C row 1.4.4 / threshold commentary: CONFIRMED.
Part C row 1.4.5 / NEC and S-FIT: CONFIRMED (NEW-CLAIM classification only).
Part C row 1.4.6 / mixture description: CONFIRMED.
Part C row 1.4.7 / DIST-1(c): CONFIRMED (EQUAL on TC3).
Part C item 2 / coverage and EQUAL audit: VERIFIED-WITH-AMENDMENTS (D1-03, D1-04).
Part C item 3 / proof matching: VERIFIED-WITH-AMENDMENTS (D1-01, D1-02).
Part C item 4 / TARGET synchronization and target implication: VERIFIED-WITH-AMENDMENTS (D1-02); reader blocks identical, TC3 confirmed, no protected weakening found.

Limits: unchanged previously checked proof lines and the full proofs/statuses of consumed external results were not independently re-reviewed. I inspected the locked T01 contrast-identification passage only to check D1-01's normalization. NEC's proof belongs to L7 and was not independently checked here. Empirical claims were not recomputed; neither simulation output nor a typical-mixture description is used as proof. TARGET §5 was compared with the available d995ec2 snapshot, not an independently authenticated earlier CP1 TARGET file. The malformed statement diff was fully recoverable using its authenticated old blob plus the current statement. No required Part A algebra, Part B hunk, or listed Part C statement comparison was left unchecked within these limits.

Findings: D1-01 MINOR; D1-02 MINOR; D1-03 MINOR; D1-04 MINOR; D1-05 NIT. No CRITICAL or MAJOR findings.
Overall verdict: VERIFIED-WITH-AMENDMENTS — L6-01's repair and EQUAL on TC3 are CONFIRMED; apply D1-01–D1-04 for literal proof/statement/change-record accuracy and regenerate the comparison artifact for D1-05.
