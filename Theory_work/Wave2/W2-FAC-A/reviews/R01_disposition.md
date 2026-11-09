# R01 disposition (statement lock, Codex gpt-6.1-sol high: LOCK-WITH-CHANGES)

All ten required changes applied in STATEMENT.md v1.1 (now LOCKED) and PLAN.md:

1. Hypotheses per clause made explicit ((L2)–(L5)); Sand_n named; H0 retained as an assumption (AG supplies only the
   eigenvalue part; energy and BM-∞ follow for fixed bounded nonzero θ*). PLAN item 4 corrected.
2. L1 stated with the coupling, empty-set conventions, uniformity, κ' term (ξ₀ kept) and the transfer error
   O_P(δ_n√(p log log n)); lemmas/L1_uniform_add.md already proves the split with the √s_T/(1+s_T) ≤ 1/√(c_min h)
   step (κ := κ'/√c_min absorbs a small c_min, as the reviewer notes) and the Lipschitz/perturbation bounds with
   constants depending only on ψ₀ (U(d)).
3. TL: lemmas/L3_NA_TL.md L3.2 bounds the cross term by 2|θ_i|σ√(n−1)(|Z₁| + |Z₂|) with |Z| = O(√log n) uniformly
   (L1), i.e. o(θ²_i(n−1)φ²) under BM-∞ — a θ-weighted bound, not a generic O(√(n log p)); the uniform expansion
   (E1)/(E2)/E_Y is a new lemma (L3.0) without the polynomial-family toolkit.
4. α₀ derivation, κ ≥ 1, and the BB-ratio remark inserted in §2; "sharp"/"iff" language restricted to Part II (exact
   CS); (P) stated as the strict limsup condition.
5. Sandwich: re-proved for the Q = [p], K = p branch in lemmas/L2_sandwich.md (not cited as GROW L3 verbatim); GROW
   L1 descent reused verbatim (needs only S₀ ⊆ Q, |Q| ≤ K); p = o(n) ⇒ K = p eventually stated in §3 (P).
6. (TV-pop) now uses a deterministic block family 𝔅_n and a design event 𝓔'_n covering the realised blocks
   (𝔅_n = all sets of size ≤ 16 allowed).
7. (GC-CS) written out; (I)(b) retains it; (I)(c) names the layouts with file pointers and requires either a proof of
   the whole-group block structure or a certificate over all sets of size ≤ 16; κ = 1 for block CS recorded with the
   reviewer's closed form.
8. SHARP witness specified (m = ⌈log p⌉), separate small-model score argument, retained assumptions, no claim at 1/6.
9. (D) lists Proposition F's premises explicitly, the A4 allocation addition, the audit qualifications, p = p_raw a.s.,
   and the 𝒦_n route.
10. Unsupported numerics claims replaced: the lattice-NA violation claim now cites numerics/D2_lattice.md (new
    summary of the d_exact.py fields lat_adv_*; the D2_summary table column read a different field name and showed
    0/0); Part III states the exact rows with swaps/path-NA failures at n = 10⁴; the k ≥ 2 claim and the
    "every null is visible" generalisation removed or qualified.

Optional suggestions: existential representation adopted in §2; adversarial L1 tests extended in fu_check.py
(random sign-changing loadings, random PD blocks — class "RND"; further tests with shrinking c_min and bounded p
added in F-U5, see FU_out.txt).
