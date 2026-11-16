# Pre-check P7 — a claimed counterexample: the exponential distance clause fails without the non-degeneracy condition
Read `Theory_work/Wave3/W3-DIST/briefs/PRECHECK_COMMON.md` first. Output file: `Theory_work/Wave3/W3-DIST/reviews/P7_opus_precheck_NEC.md`.
Object: `Theory_work/Wave3/W3-DIST/work/api_attempts/dist1b/F-b-r2.md` (an API proof attempt; proof material, unchecked). It
claims: for an explicit fixed design with s₀ = 0, μ = 0, p = ⌊√n⌋ + 1 (an anchor column and ⌊√n⌋ near-copies at
τ² ≍ log n/n²), for every integer k ≥ 1 and n ≥ n₄(k), with P_e-probability ≥ 0.6,
Π(‖μ̂ − μ‖² ≥ (k/24)σ*² log n | y) ≥ c₄(k)/(2n); hence the conclusion of Lemma X (STATEMENT §3) cannot hold under (E), (C)
alone, i.e. without (ND), for any constants — while Lemma X′ (radius tℓ_n) is not contradicted.
Context: STATEMENT §0, §3 (Lemma X, Lemma X′), API_CARDS "Common definitions" and card F; the locked [P1] =
`Theory_work/Old_Projects/New_BVS_Headquarters/branch_snapshots/main@c4ef0dc/Docs/Theory/proofs/T01_T02_contrast_dimension/PROOF_v3.tex`.
Duties: (1) check §1–§7 line by line: the design (centred columns of squared norm N; K = p for large n), the exact
spectra and determinants of §2, the plug-in bound (2.3), every event of §3 and the total P(𝓔) ≥ 0.6, Step A (π(∅) ≥ ½),
Step B (the lower bound (5.1), including the elementary-symmetric-polynomial bound and the prior ratio), Step C, and
the contradiction in §7 (choice of M, t, k; that the design satisfies (E; 0), (C; 0), p ≤ n^A and violates (ND)).
(2) Confirm or refute numerically, with a short Python script kept **outside the repo** (your scratchpad) or by exact
computation: at n ∈ {400, 1600, 6400} build the design, draw ≥ 200 noise vectors, compute the exact posterior over a
family large enough to be conclusive (e.g. all models of size ≤ 3, since larger sizes carry negligible mass by Step A)
and report the frequency of {Π(‖M_Se‖² ≥ (k/24) log n) ≥ c/n} for k = 1, 2 — say whether the n⁻¹ scaling of the far mass is
visible. (3) Does the proposition contradict Lemma X′ or display (1.2) of STATEMENT (radius C√(tℓ_n/n), t ≥ M₀ log n)? It
should not; verify. (4) State precisely what is established: which clause of which statement fails without (ND), in
the exponential form only or also in probability; and what remains open (§8, GAP 1, GAP 2).
Verdict per section and overall: VERIFIED / VERIFIED-WITH-AMENDMENTS / NOT VERIFIED.
