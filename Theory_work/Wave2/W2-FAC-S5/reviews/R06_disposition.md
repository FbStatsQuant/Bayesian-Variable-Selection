# R06 disposition (exhaustive sweep, Codex Sol xhigh): 0 fatal / 1 major / 11 minor / 7 editorial — all fixed

1 (MAJOR) E_S block-local quantifier — FIXED (L3: S₀ ⊆ U ⊆ C_b ∖ {l}, l ∈ C_b ∖ S₀ in the unique block ⊇ S₀).
2 G_add small-argument condition — FIXED (L1.4, "provided x ≤ ν/2"; L4.2 gives x = O(log n)).
3 determinant remainder n/(n−1) — FIXED (L1.4: ≤ 2n^α/((n−1)d) ≤ 4n^{α−1}/d).
4 multiplier limit ≍ vs ∼ — FIXED (L3: p/n → c gives M_{[p]} → 1/(2(1 − c))).
5 SHARP over-citation — FIXED (L4.6 remark 2: SHARP proves failure of full-lattice NA by an addition witness only).
6 S3 gain-error count — FIXED (L1 status: 15 paths with n ≥ 10⁶, ≤ 1.8e−3 log n; 3 paths at n = 10⁴ up to 0.043 log n).
7 leakage experiment — FIXED: l1_leak.py rewritten (stable σ_j = a⁻¹β̃ᵀϑ^R; reports n^{3/2}·leak ≈ 0.00746, leak/bound ≤ 2e−4,
  total |ε|/two-term rate ≤ 0.0099, reconstruction ≤ 7e−11); l1_leak_out.txt regenerated; L1 wording narrowed.
8 identity count — FIXED (l1_identities.py reports generated 400 / tested 361; output regenerated; L1 wording).
9 tie rule in simulators — FIXED: s1_path.py / s3_cc.py pick, among exactly tied best deletions, the largest index (lex-smallest
  set) and count exact ties of any type; complete-scan rerun numerics/s1_exh2/ (S1X2_summary.txt): 15/15 pure null deletion to
  S₀, 0 exact ties, worst swap margin −0.4361 log n, worst addition −0.3629 log n. bcs_core docstring corrected.
10 sampler randomness — FIXED (STATEMENT §3 restricted to deterministic statistical quantities; algorithmic uniforms noted).
11 s_max undefined — FIXED (L2.2 defines s²_max := 2[(1 + s₀)‖ϑ‖² + σ²], s²_min := σ²/2, via L3 (c1)).
12 S4 provenance — FIXED (L2 status: FACB Python replica with its tie tolerances, not the production routine).
13 premise list — FIXED (STATEMENT §1 adds IND-T and the c₄ search for R′ > 4).
14 G_n clash — FIXED (J_n = group count in STATEMENT; G_n^obs = random maximum; G_n = deterministic envelope in L3).
15 undefined symbols — FIXED (quad_T, H_T defined in L1.4; the end-phase heuristic in STATEMENT §0 now defines H and is marked
   as not used in any proof).
16 sufficiency sentence — FIXED (L1.3(i): observed group means m_g = h + ȳ_g).
17 empty-set conventions — FIXED (L1.2(a)).
18 measurability wording — FIXED (L5.2: "defined on the enlarged space and not assumed data-measurable").
19 self-test docstring — FIXED (bcs_selftest.py: every flip gain and the best exhaustive swap gain).
STATEMENT edits 10, 13, 14, 15 are wording/notation (v2.3, post-lock, flagged); no hypothesis or claim changed.
