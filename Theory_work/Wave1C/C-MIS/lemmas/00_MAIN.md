# C-MIS — proof map

| Claim (STATEMENT.md v1.1) | File | Inputs (verbatim statuses) | Checks | Numerics |
|---|---|---|---|---|
| Lemma R (exact reduction under GR) | L1 §L1.1 | — | R02 VERIFIED | N1b |
| Theorem MIS (i) fixed candidate design | L1 §L1.2 | T03♯ "PROVED; SF VERIFIED (W2-VT03R); XF VERIFIED (A-REV2)"; T01–T03 "PROVED-LOCKED (wave 3; external review queued), SAME-FAMILY-ONLY" | R02 VERIFIED | N1b, N4 |
| Corollary N (naive targets fail) | L1 §L1.2 | MIS (i) | added after R04; R05 V-W-A (applied) | N1, N4, N7 |
| Lemma DR (uniform tightness) | L1 §L1.3 | — (extends GEN L5.3) | R02 VERIFIED | — |
| Theorem MIS (ii), (ii′) random candidate design | L1 §L1.4 | T03♯ | R02 V-W-A (applied) | N1 |
| Proposition P (Gaussian rows; SL's s̃; precision of the marginal (x_𝒞, x_𝓜)) | L2 | — | R02 VERIFIED; R04 #1–2 wording fixed | N1, N2 |
| Lemma GD(a) (p_𝒞 fixed) / GD(b) (optional, p_𝒞 ≤ n^A, fixed σ_𝒞²) | L2 | GD(b): Vershynin Cor 5.35 / Davidson–Szarek (cited) | R02 VERIFIED / V-W-A (applied) | N1 |
| Example E1 (analytic target separation) | L2 end | GD(a), MIS (ii) | added after R04; R05 V-W-A (applied) | N7 |
| Corollary H (M5(0) with any feasible T) | L3 | T38-(0) "PROVED (SF: VERIFIED (W3-VT38E); XF: VERIFIED* (A-REV5))" | R02 VERIFIED | — |
| Corollary D (GEN transfer) / D′ (W proxy instance, optional) | L3 | Theorem GEN "PROVED-CHECKED" (Wave 1), premises incl. e4 (N3 "OPEN" as general invariant) | R02 VERIFIED / V-W-A (applied) | — |
| Theorem F (EP, cutoff form with TAIL^𝒞(m_n)) | L4 §§L4.0–L4.7, L4.9 cutoff remark | T03R (C1)–(C10); [P3] lemmas | R03 V-W-A (applied) | N3, N3b, check_L4 |
| Corollary F(a) (bounded p_𝒞) | L4 §L4.8 | — | R03 VERIFIED | N3, N3b |
| Lemma T, Corollary F(b) (TAIL^𝒞 under (TL)) | L4 §L4.9 | [P3] lem:det, lem:prior(b), lem:chi | R03 VERIFIED | check_L4 (C4a, C4b) |
| Lemma Z (null projection, bounded p_𝒞) | L6 | [P3] lemmas | added after R04; R05 V-W-A (applied) | N6 |
| Lemma O1, Lemma O2 (frontier); Examples E2, E3 (GR / EP cannot be deleted) | L5 | [P1] lem:num, T03R den′ | R03 V-W-A (O2 consequence paragraph replaced); E2/E3 added after R04, R05 VERIFIED | — |

## Hypothesis-to-step table (R04 request)

| Hypothesis / device | Where it is used | Where it is NOT used |
|---|---|---|
| True noise variance σ² | exact χ² laws, (G1)–(G4), lower bounds on 2b + Q (L4.4(b), L4.5), Lemma T's denominator | — |
| Effective variance σ_𝒞² (GR) / σ²_{𝒞,n} = σ² + Δ_n (EP) | GR: everything (it is the noise of the reduced model). EP: upper bound E_n^𝒞 (L4.4(c)), (C6)(b) second line, signalgain, beta-min BM^𝒞 and J_n^{𝒞,F}(c) | EP: χ² laws, superset bounds |
| Candidate-only rerun (p_𝒞, w(·) with 2p_𝒞 − 1, K = min(p_𝒞, ⌊n/2⌋), candidate standardisation, response-dependent b) | all of L1–L6 (Lemma R transfers the whole run) | no conditioning of the full-p posterior anywhere |
| (G5) \|rᵀe\| ≤ σ‖r‖√(2 log n) | L4.2, L4.4(b),(c), Lemma T | GR results (r absent) |
| Auxiliary models beyond the cap (S ∪ S₀^𝒞, size up to K + s) | (C6)(a), (C8), Lemma T (score-comparison devices, [P3] remark "the cap") | never as posterior states |
| SE_w at the enlarged cutoff m_n = min(K, max(m♯_n, m^T_n)) | Corollary F(b) | Lemma T itself (needs eigenvalue bound on S₀^𝒞 only) |
| SE_λ(j₀) | (B2) for underfitting S with #J′(S) ≤ j₀; EP uniqueness of θ^𝒞 | Lemma T, Lemma Z |
| BM-∞ (vs BM(c)) | Corollary D (GEN's (H0)); MIS(ii) envelope M_n | MIS (i)/(ii) and F also allow BM(c), c > c₀ unchanged |
| TAIL^𝒞 | Theorem F Step 0 replacement | discharged by Cor F(a) (bounded p_𝒞) and Cor F(b) (TL) |
| GEN operational premises (EX-A, EX-S, CAL, SR, GUARD-W, OP-LS0, e4, complete scans; IND-T/c₄ if R′ > 4) | Corollary D, D′ | MIS, F, H (H uses only the M5(0) output/coupling premises) |
| s₀^𝒞 ≥ 1 | MIS, F (via TH09's R1) | Lemma Z (s₀^𝒞 = 0, bounded p_𝒞) |
