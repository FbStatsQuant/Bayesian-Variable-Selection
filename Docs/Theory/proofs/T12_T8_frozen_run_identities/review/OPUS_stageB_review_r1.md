# Opus 5.5 (xhigh) Stage B reviewer, round 1 reply on PROOF_v3. Copied by the lead from the agent's reply; the original is verbatim, but this copy is condensed where marked.

**Verdict: not verified.** Every conclusion except one holds as written. The exception is the numerical component example in (iv.b) and its reuse in (iv.e), which rest on a marginal-likelihood formula that is not defined anywhere in the proof or in the packet (G1). If the formula, hyperparameters and prior are confirmed against 00_COMMON §1, I expect the verdict to become verified. G2 is a minor unstated regularity assumption.

**What I did:** read STATEMENT.md, REPORT_FORMAT.md, proof/PROOF_v3.tex, the PDF text (it matches the tex), both helpers and the saved log, and checked every lemma and step by hand. Three local computations, terminal output only (`-B`, no files written; folder verified unchanged):
1. Re-ran `python -I -B certify_instance.py iv`: it reproduces `certify_iv.log` in all four configurations. Max enclosure width < 2e-53 < 1e-52, as stated.
2. Independent float implementation: built the kernels from STATEMENT §1 (general p, detailed balance verified for all 5 kernels) and tracked the pre-Gibbs-1 state with a marking step instead of the proof's prefix/suffix J. Used the generic beta-binomial BB(1,p) prior; only `log_bf` and `standardise` were taken from the helper. Results: primary bias −0.173974177850 (1+L′=6, method) and −0.212065526919 (1+L′=5); secondary bias −0.159677356166 and −0.194638440548; (E[Ẑ₁PIP̂₁|F] − Z·PIP₁)/Z₀ = −95.609622724 and −95.648818292. All are identical with the stage-0 flag set or unset. E[Ẑ] − Z and E[ẐPIP̂₁] − Z·PIP₁ are ~1e-12. All match the proof's table and §8.5.
3. Monte Carlo of the literal algorithm (seed 12345, 200,000 islands, 1+L′=6, random orders and accept/reject coded from STATEMENT §1–2): E[PIP̂₁] − PIP₁ = −0.1752 ± 0.0008, consistent with −0.17397.

## Findings

**G1.** Location: §8.2 "The instance" and the interval-computation paragraph; §8.5; helpers/p2_exact.py `log_bf` (lines 58–84) and `setup` (line 98). Severity: **gap**.
Claim: The (iv.b) bias bounds (−0.17 / −0.15) and the (iv.e) result E[Ẑ_r PIP̂_{r1}|F] ≠ Z·PIP₁ depend on the exact formula for m(S), on a₀ = b₀ = 0.01 and on the prior weights w(k). None of these is stated or justified in the proof or in STATEMENT.md, so I cannot verify that the computation is about the v3 target.
Evidence: the formula exists only in code: log BF(S) = −½ log(det H/det(G+I)) − ν[log(2b₀+yᵀy−n zᵀH⁻¹z) − log(2b₀+yᵀy)], with H = (n+1)G+I and ν = a₀+n/2, justified only by the comment "for the v3 target". STATEMENT §0 defers to 00_COMMON §1 (not in the packet) and says "only m > 0 and ϖ > 0 are used", which is false for this instance. The prior values w(0)=½, w(1)=w(2)=1/6, W_K=1 match the standard BB(1,2) beta-binomial (recomputed), but that definition is also not in the packet. The margins are small: 0.0040 (primary) and 0.0097 (secondary) at the method column. Diagnostic only: with ν = a₀+(n−1)/2 the bounds still hold (primary −0.179106, secondary −0.164769, D = 7.7534), so the conclusion may survive, but I could not verify the formula itself. The qualitative (iv.e) facts (P(F)>0, E[Ẑ_r|F] < Z, E[Ẑ|F] < Z) need only D > 4/√3 and a < ½, and both numbers come from the same unverified formula.

**G2.** Location: §6, the paragraph after Lemma 6.1 ("the joint measurability of Φ is part of the stream model"). Severity: **gap (minor)**.
Claim: The proof assumes Φ is jointly measurable in (c,u). STATEMENT.md does not state this; EX-S, CAL and Success only say that Φ(c,·) realises I(c).
Evidence: Lemma 6.1 is applied to g(Φ(c,u₁),…,Φ(c,u₄))·1_𝒜(c), which must be E×Υ-measurable, and the (iv.c) characterisation needs c ↦ law of I(c) to be a kernel. The assumption is standard and true for any algorithmic implementation, but it is imported rather than given.

**E1.** §8.2 (tex line 199): broken cross-reference. The source has `Appendix~ef{app:code}` (the `\r` of `\ref` was lost) and the PDF prints "Appendix efapp:code". Appendix A contains only the listings; the log exists only as helpers/certify_iv.log. Exposition.

**E2.** §8.1 (P_c(E_U) bound) and §4 Step 2: ε_U is defined in Lemma 1.4(a) at a single temperature, but (ε_U/m)^{NT} combines rounds at φ₀,…,φ_{T−1}. This is correct if ε_U is taken at |φ| = 1 (since e^{−|φ|R_d} ≥ e^{−R_d} on [0,1]), but the proof does not say so. Exposition.

**E3.** §8.3 "None of the hypotheses restricts…": the step from "the island law depends on c" to "none of the hypotheses ensure a constant conditional law" is implicit. It needs a valid input where d has a unique maximiser (the (iv.b) instance supplies one: d = (0,0,0,D), D ≈ 8.15) and a CAL-admissible law of 𝓒 with positive mass on both (grid,N) and (grid,4N). Not stated, although the STATEMENT disclaims the stronger claim anyway. Exposition.

**E4.** §8.4, last two sentences: "only the averaged form holds" is not backed by an example where the un-averaged form fails. The averaged form is proved correctly, but the negative reading is not, and the STATEMENT's "in general random" is not exemplified either. Exposition.

**E5.** §8.2: "each retained cluster has at most one member" and "largest-|r| partner" justify the block structure and neighbour graph by method rules that are not in the packet. Harmless, because the STATEMENT appendix itself asserts B=1, blocks {1},{2}, N(1)={2}, N(2)={1}, K=2, m=5, L=5. Exposition.

**E6.** helpers/p2_exact.py, cosmetic: `IvArith.show` prints whole 60-digit intervals because `.mid` is itself an interval; the `__main__` block uses an unrelated n=6 dataset; the comment "w(k) = 1/2 / C(3,k)" is an unexplained p=2 shortcut. These affect no certified value. Exposition.

## Conclusion-by-conclusion

- (i.a)–(i.c) yes; (i.d) yes; (ii) yes; (iii) yes given G2.
- (iv.a) yes (E2).
- (iv.b): the covariance formula yes; the component example not verified (G1). The computation itself is reproduced three ways; π₀K₀ = π₀ makes the flag readings agree; the uniform and neighbour swaps coincide at p=2 (checked); the 10⁴-term sum for P̃₁ is checked.
- (iv.c) yes (G2, E3); (iv.d) yes (E4).
- (iv.e): the qualitative parts follow from D > 4/√3 and a < ½; the (ii)-inequality is not verified (G1). Extension from r=1 to every r by exchangeability is implicit.
- (iv.f) yes.

**Verdict: not verified.** The only blocker is G1. Everything else checks out apart from the minor unstated assumption G2.
