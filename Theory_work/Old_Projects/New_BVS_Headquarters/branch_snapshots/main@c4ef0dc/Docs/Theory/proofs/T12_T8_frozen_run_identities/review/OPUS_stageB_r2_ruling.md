# Opus 5.5 (xhigh) Stage B reviewer, round 2 reply on PROOF_v4 / STATEMENT v2.2. Copied by the lead from the agent's reply (condensed: tables flattened).

**Verdict: verified.** All three claims accepted, and every fix works. There are no fatal or gap findings in PROOF_v4; only minor exposition remains.

## Rulings on CLAIMS_OF_FATAL_FLAWS.md

**Claims 1 & 2 (target formula = my G1): agree, and the fix works.** STATEMENT v2.2 §0 now states H_S, D_S, Q_S, m(S) with C_n, BF(S), ν = a₀ + n/2, a₀ = b₀ = 0.01, w(k) and W_K. The positivity remark is restricted to everything except the instance.
- `log_bf` (lines 70–96) checked term by term against §0: H = (n+1)G + I, D = det H/det(G+I), Q = yᵀy − n zᵀH⁻¹z, and the 2×2 inverse. An independent numpy det/solve evaluation of the §0 formula agrees with `log_bf` to ~1e-14: log BF({1}) = −1.49623, log BF({2}) = −0.74626, log BF({1,2}) = 5.90427. `standardise` gives squared norm n − 1, as §0 requires.
- Prior identity B(1+k, 2p−k)/B(1,p) = ½/C(2p−1, k) verified in general (both sides equal k!(2p−1−k)!/(2·(2p−1)!)) and numerically for p ≤ 11. At p = 2 it gives w = (½, 1/6, 1/6), W_K = 1, matching §8.2.
- The new §0 positivity justification is true: Q_S ≥ yᵀy/(n+1), because the eigenvalues of n·X_S((n+1)G_S + I)⁻¹X_Sᵀ are n·s/((n+1)s + 1) < n/(n+1). A random-matrix check gave a minimum ratio of 1.0000003.
- The new "The scores" paragraph is correct (ν = 10.01).
- Certificate: unchanged values, now with exact comparisons. A re-run of `python -I -B certify_instance.py iv` is byte-identical to the new certify_iv.log. Its values equal the round-1 log (e.g. −0.1739741778498905057033109, −95.60962272447696730115704). The CHECK lines compare full-precision endpoints (203-bit mantissas). Converting the endpoints to exact rationals in all four configurations: primary < −17/100, secondary < −15/100, D > 8 (so 3D² > 16), a < ½, and the (iv.e)/(ii) quantity < 0.
- Scope note (not a finding): faithfulness of §0 to METHODOLOGY_v3 §5 / 00_COMMON §1 cannot be checked from the packet; by its own rule the STATEMENT is the reference, and the proof is verified against it.

**Claim 3 (joint measurability = my G2): agree, and the fix works.** EX-S v2.2 states that (c, u) ↦ Φ(c, u) is jointly measurable with values in a Polish space, and PROOF_v4 §6 cites it. This covers Lemma 6.1 applied to g(Φ(c,u₁),…,Φ(c,u₄))·1_𝒜(c) and the kernel/π-system step in (iv.c). It is standard regularity implicit in "ideal uniform streams", and no conclusion changes.

**Exposition items E1–E6 and (iv.e) exchangeability: all fixed and checked.** E1: the reference renders as "Appendix B", which reproduces the log with its CHECK lines. E2: ε_S = π₀(S)e^{−R_d}, valid on [0,1], is used consistently in §4 Step 2, §8.1 and §8.3. E3: the added sentences are correct; the (iv.b) instance has a unique maximiser, d = (0,0,0,D) with D > 8 certified. E4: the (iv.d) remark is precise and proved; Z_t q_t(1{S}) = m(∅)γ₀(S)e^{φ_t d(S)} differs at u ≠ u′ when d(S) ≠ 0. E5: the proof now cites the STATEMENT appendix. E6: endpoint display, prior comment and `__main__` are fixed. (iv.e): the islands are iid and F is permutation-invariant, so the extension to every r is now explicit and correct.

## Review of PROOF_v4

The diff of PROOF_v3 → v4 shows only the listed changes. Each changed passage was re-checked by hand; the unchanged passages keep the round-1 step-by-step verification. The PDF text matches the tex (16 pages). Round-1 cross-checks still apply (identical values): an independent float re-implementation agreed to ~12 digits, and a single-seed MC with 200,000 runs gave −0.1752 ± 0.0008. The STATEMENT v2.1 → v2.2 diff shows only §0, EX-S and the (iv.d) remark changed.

Findings (exposition only):
- **X1** (CLAIMS_OF_FATAL_FLAWS.md, E6 entry): it says the previous log is kept as helpers/certify_iv_v1.log, but that file is not in the packet. Packaging only; "identical values" was confirmed against the recorded round-1 values instead.
- **X2** (PROOF_v4 §8.2, "(The method's preliminary division by the maximum absolute value cancels in exact arithmetic.)"): refers to a method step not defined in STATEMENT.md. The remark is true (a positive column rescaling is undone by centring and scaling to squared norm n − 1) but unnecessary, since §0 defines the standardised data by that end result.

Conclusion by conclusion: (i.a)–(i.d), (ii), (iii), (iv.a)–(iv.f) all hold.

**Verdict: verified.** Every conclusion of STATEMENT v2.2 is correctly proved in PROOF_v4. G1 (Claims 1–2) and G2 (Claim 3) are closed; X1 and X2 do not affect any conclusion.
