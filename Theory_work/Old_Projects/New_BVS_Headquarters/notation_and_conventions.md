> **Archive note.** In this archive, "02a" means `02_theory.md` (final state), "02b" means `02b_theory_campaign_history.md` (campaign history), and "REG-A"/"REG-B" or "registry A/B" mean parts A and B of `ID_REGISTRY.md`. Paths like `branch_snapshots/...` and `transcript/...` are relative to this folder.

# Notation and conventions, FINAL STATE (agent A)

Companion of `02_theory.md` (called 02a) and `ID_REGISTRY.md (part A)`. Scope: every symbol, prior, parameterisation and assumption in the final documents (METHOD_v3.1_FINAL with its amendments, the MEET-THM cards, NOTATION.md, the shared definitions), with the file/section where it is defined and the transcript position where it was introduced or ruled on.

**Conventions of this file.** Verbatim blocks are marked `<!-- BEGIN VERBATIM <source>:<lines> -->`; paths are relative to `branch_snapshots/`. "Summary:" marks editor text. **UNCERTAIN:** marks conflicts. **Transcript positions:** this draft read the transcript from position 1040 on. The model itself (g = n, τ = 1, IG(0.01, 0.01), BB(1, p), cap K) is Felipe's own model and was defined before position 1040 (METHODOLOGY_v3 §5 headline: "Felipe's model, unchanged"); in the thread after 1040 it is discussed at [pos 1302] and treated as fixed. Where a symbol appears only in files, the position column says "file only".

## N0 · Felipe's ground rules and the objectives (these fix how every setting is read)

`MEET-v31/DOSSIER.md` §1 "Ground rules (Felipe's words, 2026-11-03; binding on every seat)", summarised (Summary; words quoted in the file): 1 baseline and burden of proof ([pos 1155], [pos 1162]); 2 real issues only; 3 provable or nothing ([pos 1138], [pos 1142]); 4 what parallel means — islands and particles, "We are not trying to parallelize over variables" ([pos 1113], [pos 1117]); 5 local-to-global kept unless "a very serious, irrefutable argument" ([pos 1132]); 6 objectives in order: (1) accuracy in recovering the true posterior, (2) parallel scalability, (3) BVS selection accuracy; 7 theory standard: reach every goal of the Local-to-Global proposal (§5.1–5.4, §13.1) and "extract until the last drop" ([pos 1144], [pos 1150]); 8 re-runs ([pos 1051]); **9 generality in (n, p)** added after Round 1 ([pos 1214], [pos 1226]; `MEET-v31/evidence/AMEND_01_general_np.md`). Theorem-meeting additions: paper 1 at Biometrika level ([pos 1350]); the method is fixed (v3.1) apart from growth rates ([pos 1302], approved [pos 1304]); subscriptions only ([pos 1324], [pos 1326]).

In every card, "Objective (1)/(2)/(3)" refers to the objectives of ground rule 6.

## N1 · Symbol table (NOTATION.md, verbatim)

`MEET-THM/NOTATION.md` (registrar Sonnet 5.5; "The chair accepted the registrar's proposals: every entry marked 'adopted for the HQ charters unless an HQ objects' is the notation the charters use"). **Important caveat (Summary):** the final cards in THEOREM_LIST_FINAL (02a TH01–TH20) are copied verbatim from the seats' Round-3 cards and keep the seats' own symbols (e.g. q_t, T_bd, M₂, R′, d_σ, W as exhibit family and as subset); the registrar's canonical renamings (e.g. π_𝒯, q_φ for the normalised bridge law, d_σ with baseline superscript "bd", D_env, ℛ_α, x̄_max, r_*, 𝒲, Δ_V, n_pilot, ι, Γ_S) govern the HQ charters and future writing but are not applied inside the verbatim cards. Where the table says "adopted … unless an HQ objects", no HQ objection is recorded in the snapshots.

<!-- BEGIN VERBATIM MEET-THM/NOTATION.md §0:3-28 -->
Registrar: Sonnet 5.5 (Claude Work). 2026-11-04, updated after Round 3. Mechanical table: the registrar lists what the sources say and proposes one canonical notation per conflict. **The chair accepted the registrar's proposals: every entry marked "adopted for the HQ charters unless an HQ objects" is the notation the charters use; an HQ that objects raises it with the chair and the registry owner, and the charters of the other HQs are not affected until it does.** Symbols of `AMENDMENT_HQ_02_DEFINITIONS.md` are covered (rows 62–68 and the rows they point to); where the amendment's local names differ from the canonical ones, the mapping is stated in the row. No theorem statement is changed here.

## 0. Conventions

**Sources and tags** (`path:line`; same tags as `REGISTRY_PAPER1.md`):

| Tag | Source |
|---|---|
| `S2:n` | `SYNTH_R2.md` line n |
| `A:n` `B:n` `C:n` `D:n` | `R2_A.md` … `R2_D.md` line n |
| `M:n` | `METHOD_v3.1_FINAL.md` (`origin/theory/MEET-v31:theory_campaign/MEET-v31/`) line n. The file is a diff against METHODOLOGY_v3; its rows quote `M §…` for the base document, and the base document itself is not in this worktree. "Method §3/§5/§6.x" below therefore means the METHOD row that quotes that section. |
| `R0:n` | `R0_DIFF.md` line n (K-ID rows; the guarantee text) |
| `W1PC1:n` `W2PC1:n` `W2PC2:n` | `evidence/…/VERDICTS.md` line n |
| `CHK:n` | `evidence/CHK_INHERITED/REPORT.md` line n |
| `AMEND:n` | `AMENDMENT_HQ_02_DEFINITIONS.md` line n (definitions for HQ, chair; the reporting and growth-rate amendment) |
| `MINUTES §x` | `MINUTES.md` section x (binding Round 3 decisions) |
| `R3_X:n` | `R3_A.md` … `R3_D.md` line n |

**Conflict labels in column 4.**
- **[C] meaning clash:** the same symbol is used for different mathematical objects (across seats, or between a seat and the method). Each meaning is listed with its source.
- **[V] naming variant:** one object, different names or decorations across sources. The numerical definition may differ in a detail; the detail is stated.
- A row with neither label has one meaning in all sources read.

Seats are A (Fable 5.1), B (Fable 5.1), C (gpt-6-astra), D (Fable 5.1). "Seat X" means the R2 card.

**Typography.** `∣x∣` is an absolute value, `‖·‖` a norm, `∣` inside a probability is the conditioning bar; table cells contain no pipe characters.
<!-- END VERBATIM MEET-THM/NOTATION.md §0:3-28 -->

<!-- BEGIN VERBATIM MEET-THM/NOTATION.md §1:30-101 -->
## 1. Table

| Symbol | Meaning | Defined in | Conflicts | Canonical notation (registrar proposal; adopted for the HQ charters unless an HQ objects) |
|---|---|---|---|---|
| π | Exact posterior on Ω: π(S) = ϖ(S)·m(S)/Z. | C:52; target M:298–300 | **[V]** restricted-store law written π_𝒯 (A:89; B:119) and π^𝒯 (C:96; D:72). **[V]** pooled empirical law π̂ (C:53); coarsened π̂_cell (C:226). **[V]** bridge law at φ is called π_φ in K104/K103 (B:179, A:145). | adopted for the HQ charters unless an HQ objects: π_𝒯 (subscript, matching Z_𝒯); π reserved for φ = 1; the bridge law is q_φ (see γ_φ). |
| π₀ | Start law π₀ = γ₀/Z̄₀ of the composite block start. | C:52; M:118 (row 0), M:319–320 | none | keep. |
| γ_φ | Unnormalised bridge target, γ_φ ∝ γ₀·e^{φ·d}; moves are "γ_φ-reversible". | A:44; D:56; γ₀ in C:52 | **[V]** same family written q_φ (normalised, A:153, B:211, C:52) and q_t for real t (C:52) and π_φ (B:179). **[V]** reversibility is stated w.r.t. q_φ in K20 (R0:99) and w.r.t. γ_φ in A:44, D:56. | adopted for the HQ charters unless an HQ objects: γ_φ unnormalised, q_φ := γ_φ/Z̄_φ normalised (Z̄_φ = Σγ_φ, Z̄₀ the start normaliser, K08); drop π_φ; say "q_φ-reversible" (the normalisation does not change reversibility). |
| d | Bridge discrepancy d(S) = log BF(S) − Σ_b log r_b(S_b). | C:52; B:244; D:178; A:198 | **[C]** d = number of interchangeable duplicates in K100 (A:143, B:183: PIP = E[#selected in group]/d). **[C]** d₀ = number of cells in the TV/content corollaries (C:226, C:247). **[C]** D_α is the Rényi divergence in WS6(d) (A:169). | adopted for the HQ charters unless an HQ objects: d only for the discrepancy; duplicate-class size s_dup; cell count n_cell; Rényi divergence ℛ_α. |
| d_σ | σ²-coupling (block-orthogonal-equivalent) discrepancy: d_σ(S) = ν[Σ_b log(1−x_b) − log(1−Σ_b x_b)] ≥ 0. | C:65; S2:119; A:153 ("BO-equivalent discrepancy, WS3"); B:211 ("d computed from G_D with the same z, Y"); D:120 | **[V]** baseline-law objects use superscript σ in A, B, C (χ²^σ, q^σ_t, T^σ: A:162–164, B:216, C:273) and superscript bd in D (d^bd = d_σ, χ²^bd, T^bd, M^bd: D:130–133), while S2:131 writes T_bd. **[C]** σ is also the noise sd (C:54: σ² > 0, fixed). **[V]** B's WS4 split d = d_det + d_fit + d_σ (B:227) vs the two-term split d = d_σ + d_X (A:156; S2:120). | adopted for the HQ charters unless an HQ objects: d_σ for the function; baseline law/objects get superscript bd (q^bd, χ²^bd, T_bd) so that σ always means the noise; d_X := d − d_σ = d_det + d_fit. |
| d_X | Cross-block part, d_X = d − d_σ, with ∣d_X(S)∣ ≤ b_X. | A:156; S2:120; D:120 | **[V]** B decomposes into d_det and d_fit instead (B:227). | as d_σ. |
| C_σ | σ²-coupling constant C_σ = νa²/[2(1−a)] (bounds d_σ). | C:65; S2:116 | **[V]** A, B, D give the same expression without a symbol (A:157; B:215; D:125); in A the quantity a is the different object a := max_Ω x̄_S (see a). | keep C_σ with C's a. |
| b_X | Cross-block constant b_X = (K/2)[−log(1−δ_A) − log(1−δ_H)] − ν·log(1−r). | C:65; S2:117 | **[V]** A and D bound ∣d_X∣ by the per-model η_S, i.e. "2η_Ω" in place of "2b_X" (A:157; D:125: osc d ≤ min{osc d_σ + 2max η_S, D_*}). Different objects (per-model vs global), same role. | keep b_X (global, domain a, δ_A, δ_H, r < 1); η_S per model (see η). |
| D_* | Global range bound D_* = C_σ + 2b_X; osc d ≤ D_*. | C:65; S2:118; B:215 | **[C]** D = osc d in A:133, B:175, C:303. **[C]** D̄_n is a bound on osc d = O_P(1) in A:54(g), A:165, and a deterministic TARGET envelope D̄_n := 2[ν log((2b₀+Y)/(2b₀+Y/(n+1))) + (K/2) log(n+1)] in B:246. **[C]** D_V := osc_V d (C:140; B:139). **[C]** D_n := P(𝒪̄ ∩ {S₀ ∉ 𝒮̄⁺}) is the discovery-failure term in the HPM bound (A:99; D:66). **[C]** D_B is B's design exhibit (B:228). **[C]** D_PEL is island depth (D:103). | adopted for the HQ charters unless an HQ objects: D_* only for C's constant; oscillation written osc d and osc_V d (D_V := osc_V d); B's TARGET envelope D_env; HPM discovery term Δ_disc,n; Rényi ℛ_α; depth D_isl. |
| a | C: a := n·z′H_D⁻¹z/Q̄ < 1 (global domain quantity). | C:64; S2:110 | **[C]** A: a := max_Ω x̄_S (A:153; A:159 "uses a instead of C's a"). **[C]** a = π₀(S₀) in the start-only discovery card (C:118; a_n). **[C]** a_t := q_t(V) restricted-set mass in the coverage identity (C:140, K25). **[C]** A(k) = ϖ(k)·∏B_b/Z̄₀ (C:107), A(S₀) = posterior odds (A:89(f), K95), A_S = block-diagonal part (A:153) — upper-case relatives. | adopted for the HQ charters unless an HQ objects: a only for C's domain quantity; A's max → x̄_max := max_Ω x̄_S (= D's ū); π₀(S₀) written out; coverage mass ω_t := q_t(V). |
| δ_A, δ_H | Domain norms δ_A = ‖A_D^{−1/2} E A_D^{−1/2}‖, δ_H = ‖(n+1) H_D^{−1/2} E H_D^{−1/2}‖, both < 1. | C:64; S2:112–113; B:215 | none for δ_A, δ_H themselves (see δ for the family conflict). | keep. |
| δ (family) | — (δ without subscript or decoration) | — | **[C]** δ := (K−1)·ε̂_×/κ (B:246 T2; D:130); **[C]** δ margin in "PIPs at least δ from ½" (K62: A:54(e), D:56(f), C:70); **[C]** δ_R = 0.05^{1/R} (R0:126, K37); **[C]** δ_𝔛 in K58 (R0 K58 row). | adopted for the HQ charters unless an HQ objects: keep δ_A, δ_H, δ̂, δ₁ (all in S2); MPM margin ι := min_j ∣PIP_j − ½∣; K37's constant δ^(R). |
| δ₁ | δ₁ := 1 − π(S₀) (posterior mass off the truth). | A:54; B:79; D:56; C writes 1 − π(S₀) in full | none | keep. |
| r | C: r = δ_H·a/[(1−δ_H)(1−a)] < 1. | C:64; S2:114 | **[C]** r_b(U) block-table weights (M:320 row 23; C:107). **[C]** r_jl sample correlations (A:200; B:244: r = G/(n−1) the correlation matrix). **[C]** r_n = √(2 log p/n) neighbour threshold (M:321 row 24). **[C]** r (and R̄²) in the exponent of WS6(d), e.g. "r = 4/5" (B:217; C:278). | adopted for the HQ charters unless an HQ objects: C's constant → r_*; keep r_b(U) (table), r_jl (correlation), r_n (threshold); WS6(d) uses R̄². |
| η | Discrepancy-bound family. Per model: η_S := ν ε_S x̄_S/(1−ε_S−x̄_S) + F_S/(4(1−ε_S)); η_W := max_W η_S; η_Ω. | A:153; B:215 (a4); D:124; S2:131 (sandwich with e^{±4η}) | **[C]** D's global η := K log(1/(1−δ)) + ν log(1/(1−δū/((1−δ)(1−ū)))) (D:130, D:182; B:246 T2 "η(ε̂_×)"; S2:219 "derived η̂"): global sup-bound, not per model. **[C]** η is a coverage deficit in "a_u, a_w ≥ 1−η ⇒ ρ_full ≥ 0.9(1−η)²" (C:140). **[C]** η_r is the empirical law of island r (C:53). **[C]** η < 1 in the odds certificate A(S₀) ≤ η (A:89(f); K95). **[C]** η_A and CBL(η) in B's leakage clause (B:109(e)). **[C]** η(Ŝ), η_F scorer error (M:181 e2, M:216). | adopted for the HQ charters unless an HQ objects: η_S, η_W, η_Ω (per model / per set) and η̂ (computed from ε̂_×) only for the discrepancy bound; coverage deficit η_cov; island empirical law ℙ̂_r; odds threshold A_max; B's CBL level ζ_leak; scorer error e_F. |
| ε | Cross-block correlation level (fixed, or a sequence ε_n = 1/(np), n^{−1/2}/p) in the §5.3 package. | C:56, C:271; A:153; S2:159 | **[C]** tolerance in P(∣μ̂ − π(h)∣ > ε) (C:70; A:54(b); B:95(b)). **[C]** ε_S := ‖A_S^{−1/2} E_S A_S^{−1/2}‖ per-model operator norm (A:153; D:120). **[C]** log-mass perturbation ε in K108 (A:141; B:191). **[C]** ε_n = 1/s target error (C:322). **[C]** ε_mach (M:305 row 8). | adopted for the HQ charters unless an HQ objects: ε only for the correlation level (and ε_n); tolerance ε_tol; per-model ε_S stays but is read as "ε_S: leakage norm of S"; perturbation e_pert; machine ε_mach. |
| ε̂_× | Cross-block leakage proxy: ε̂_× := max over b ≠ b′ of ∣r_jl∣ over j ∈ C_b, l ∈ C_b′; label `cross_block_rmax`. | S2:215; B:244; D:182 | **[V]** A writes ε̂ (A:200); C writes ε̂_X and defines it from standardized columns ∣X_j′X_k∣/(n−1) (C:297; W2PC2:148). Same quantity on standardized X. | adopted for the HQ charters unless an HQ objects: ε̂_× (S2:215). AMEND:45 writes the index letters b ≠ c, j ∈ C_b, k ∈ C_c; c clashes with the cancellation depth c (see row c_ρ), so the charters write b ≠ b′, j ∈ C_b, l ∈ C_b′ (the same maximum). |
| κ̂ | κ̂ := min_b λ_min(R_{C_b}), R_{C_b} the within-block correlation matrix (computable). | S2:216; A:200; D:182 | **[V]** C writes κ := min_b λ_min(G_b/(n−1)) (C:304). **[V]** D's κ := min_{∣S∣≤K} λ_min(A_S) over models (D:130); B's T2 uses κ without redefining it and cites D's form (B:246); B's per-model bound uses a lower bound φ₀² (B:215: ε_S ≤ ∣S∣·max∣r_jl∣/φ₀²). **[C]** κ is also the favourable-rate exponent in n^{−κ} (K16; B:109(e)), the fourth cumulant κ₄ (A:198), κ-regularity (STG-L, K28), and a conditioning probability (A:133). | adopted for the HQ charters unless an HQ objects: κ̂ (S2:216) for the computed block eigenvalue; φ₀² → λ_* ; rate exponent κ_rate; fourth cumulant κ⁽⁴⁾_φ; conditioning probability p_off. |
| δ̂ | Computed leakage constant δ̂ := (K−1)·ε̂_×/κ̂; "n/a" unless the domain holds. | S2:217; D:182 | **[V]** A: δ̂ := K·ε̂/κ̂ (A:200). The chair proposes D's (K−1) form (S2:217). | adopted for the HQ charters unless an HQ objects: δ̂ := (K−1)ε̂_×/κ̂ (as S2:217). AMEND:50 and MINUTES §2.2 fix the (K − 1) form; the K form (A:200) is withdrawn. |
| ū | ū := max_S x̄_S < 1 (global). | D:130; B:246 (T2, W2PC1:165) | **[V]** the same quantity is called a in A (A:153). **[C]** ū̂ in D:182 is Σ_b max_{U⊆C_b} x_b(U) from the block tables; S2:218 describes ū̂ as "the maximal fit fraction on V (D:182)" — the two descriptions differ. | adopted for the HQ charters unless an HQ objects: x̄_max := max_Ω x̄_S for the model-space maximum; ū̂ := Σ_b max_{U⊆C_b} x_b(U) (D:182; computable from the tables without V). MINUTES §2.2 adopts D's ū̂ = Σ_b max_{U⊆C_b} x_b(U) (C's objection to a maximum over V adopted); AMEND:51 uses the same. |
| J | Jeffreys divergence J = KL(π‖π₀) + KL(π₀‖π) = E_π d − E_π₀ d = ∫₀¹ Var_{q_φ}(d) dφ. | S2:120, S2:208; C:292; B:246 | **[C]** J = number of blocks in C11 (C:185: ⌈p/B⌉ ≤ J ≤ 2⌈p/B⌉; M:185 e6 "J ≤ p blocks"). **[C]** J_T trapezoid target (A:198). | adopted for the HQ charters unless an HQ objects: J only for Jeffreys; block count N_blk (and N_blk ≤ p for the preflight). |
| Ĵ | Jeffreys run-card estimate Ĵ := Σ_r Ẑ_r·d̄_{r,meas}/Σ_r Ẑ_r − (1/R′)Σ_r d̄_{r,0}. | S2:207–209; B:244; C:293–296; D:178–179 | **[V]** component names: A_r, B_r (C:293–295; W2PC2:146); d̄_{r,0}, d̄_{r,1} = H_r(d) (D:178); d̄₀ pooled (R′N_e)⁻¹ΣΣd and μ̂_w(d) (B:244). **[C]** A's Ĵ is a trapezoid of weighted stage variances (A:198; W2PC1:155 AMBIGUOUS/GAP); B_r clashes with the block cap B. **[C]** Ĵ_r is the island-level trapezoid term in A only. | adopted for the HQ charters unless an HQ objects: S2's definition and component names d̄_{r,0}, d̄_{r,meas} (S2:207–208); A's trapezoid form is withdrawn if R3-6 confirms. MINUTES §2.2/R3-6: the B/C/D form is adopted, A's trapezoid form is withdrawn (A withdrew in Round 3). AMEND:19–20 writes the components as A_r, B_r: see the row "A_r, B_r" below. |
| Ẑ_r | Island r's evidence estimate, unbiased for Z given 𝒞. | C:52; M:158; K35 (R0:124) | **[V]** pooled reported evidence written Ẑ (METHOD "pooled Ẑ over R′", M:142; A:89(d); B:119) and Ẑ̄ for the average over R declared islands (K36, R0:125; B:85(e)). | adopted for the HQ charters unless an HQ objects: Ẑ_r island; Ẑ := (1/R′)Σ_r Ẑ_r pooled (as M:142); drop Ẑ̄. |
| W_r | Island weight W_r := Ẑ_r/Z. | C:52; A:54; B:79 | **[C]** W as a model subset W ⊆ Ω (A:164 "W = Ω"; B:216; D). **[C]** W is the exhibit family name in C (W exhibit, C:56; W2PC2). **[C]** W_K prior normaliser (K04, M:300); w(k) prior weights; w := 2v − u grid point (C:140; B:216; A:109). **[C]** W(2p)^{−k} budget in SHARE-PB (K99). | adopted for the HQ charters unless an HQ objects: W_r island weight only; model subset 𝒲; exhibit family "family-W"; grid point v⁺ := 2v − u; keep W_K, w(k). |
| M₂ | M₂ := E[W_r² ∣ 𝒞] (island second moment). | C:52; B:79; D:56; A:165 | **[V]** A writes M in H(b)–(c) (A:54) and M₂ elsewhere. **[C]** M₁ := max_S q₁(S)/π₀(S) and M_φ Doeblin constant (C:226; B:179; K103). **[C]** M_n random-moment sampler condition (W1PC1:101, ground rule 6). **[C]** M in "∥μ∥² ≤ Mn" (C:150). | adopted for the HQ charters unless an HQ objects: M₂ only for E[W_r²∣𝒞]; Doeblin M_φ (M₁ at φ = 1); signal energy M_μ. |
| R | Default final islands R = 4. | M:315 row 18; M §3 (M:82) | **[V]** the same finite-R bound is written with R (A:54(b)) and with R′ (B:95; C:70; D:56). **[C]** R_S := G_S/(n−1) and R_{C_b} correlation matrices (A:153; A:200; D:120). **[C]** R_eff (M:158). **[C]** R in the region-card item "R (optional)" (M:244). **[C]** R, R1 as hypothesis labels (C:150); R_m tail cutoff (C:151). **[C]** R² and R̄² explained variance (B:217; D:146). | adopted for the HQ charters unless an HQ objects: R = 4 default; R′ in every bound with declared islands; correlation matrices Γ_S := G_S/(n−1), Γ_{C_b}; keep R_eff; region card Reg. |
| R′ | Declared number of final islands, R′ = 4k, declared before stream 10; stacking rates R′_n. | M:142 (#7); S2:234–236 | **[V]** rate formula: A, B write 4⌈log₂(n+p)⌉ (A:206; B:254), D writes 4ℓ with ℓ = ⌈log₂(n+p+1)⌉ (D:192); S2:235 proposes D's form. | adopted for the HQ charters unless an HQ objects: R′_n = 4⌈log₂(n+p+1)⌉ (S2:235). MINUTES §2.3 and AMEND:63–64 fix the two optional rates R′_n = 4⌈log₂(n + p + 1)⌉ and R′_n = 4⌈(n + p)⁶/4⌉ (on families with D_* = O_P(1)); the ⌈log₂(n + p)⌉ form of A and B is withdrawn. |
| N | Per-island population size. | M:311 row 14 (N₀); C:303, C:321 (N_e) | **[V]** N (C:303; M:171), N_e (A, B, C:321, M:142), N₀ (M:311; D:195) for the base, N_r in K59. **[C]** N1–N17 are obligation labels (INP; "Lemma N1" in A:44(c) is the general-h identity), N200 is a composition theorem (R0:K72). | adopted for the HQ charters unless an HQ objects: N_e = final-run population at tier e (N₀ the base value, N₁ = 4N₀); obligations always written "obligation N1" (never bare N1 in a formula). |
| N_e | N_e = 4^e·max(2500, n, p), population at the selected tier e ∈ {0, 1}. | C:321; M:314 row 17; M:142 | **[C]** e as tier index vs e as Euler's number in e^{D_*} vs item ids e1–e8 (M:177). | keep N_e; item ids "item e1–e8". |
| L | Terminal rounds L = max{4, ⌈log₂(n+1)⌉}. | M:310 row 13; C:321 | **[C]** L1, L2, L3 are certificate-card items (M:234–242). **[C]** L_n in the growth clause (D:193); "(L+4)ρ̄" in K57/K58. | adopted for the HQ charters unless an HQ objects: L terminal rounds; certificate items "card item L1 … L3". |
| ℓ | Local-search/rebuild cap ℓ = ⌈log₂(n+p+1)⌉. | M:309 row 12; C:321; D:56, D:192 | **[C]** ℓ₀, ℓ_T are log-odds levels in the restricted-grid stage bound log₂[(ℓ₀+c_ρ)/(ℓ_T+c_ρ)] (A:169; B:217). **[V]** A and B use ⌈log₂(n+p)⌉ for the R′ rate (A:206; B:254) while the shipped ℓ has n+p+1 (M:309; D:192). | adopted for the HQ charters unless an HQ objects: ℓ only the cap; log-odds levels o₀, o_T. |
| T | Realised stage count of the coded grid, T ≤ T_e on success. | C:140; B:139; A:109 | **[C]** T₀ := max(1000, ℓ²) is the stage ceiling in M:313; T_e is used for the tier-e ceiling in M:326–327 and the cards. **[C]** T^σ(θ)/T_bd(θ): baseline count at ESS target θ (A:164; B:216; D:133; S2:131). **[C]** T*(c), T*: ideal-grid stage count (K28, K30). **[C]** T_n: as-coded masked count (Conjecture P). **[C]** T_cal in K89. **[C]** T(ε): the step function of ε (S2:146). | adopted for the HQ charters unless an HQ objects: T realised count; T_e ceiling at tier e (T₀ at e = 0); T_bd(θ) baseline; T* ideal grid; T(ε) always with its argument. |
| T_e | Stage ceiling at tier e (pilot floor 1/T_e). | M:326–327 (rows 29–30); C:141 | see T. | keep. |
| P | Number of pilot targets in T ≤ P + ⌈2/h_V⌉ + 1. | C:140; B:139; A:109 | **[C]** P(·) is probability in every card. **[C]** P_j move kernels in R₂ = (1/m)ΣP_j² (B:179; A:145). **[C]** P as number of processors in Brent's bound W/P + D (K89) and SL §6 (K90). **[C]** P_𝒞(cross) (B: M₂ ≥ 1/P_𝒞(cross)). | adopted for the HQ charters unless an HQ objects: n_pilot for the target count; P only probability; kernels 𝒦_j; processors w (workers, C:129). |
| h | Bounded model-space test function h: Ω → [0,1], from the declared list 𝓗; h_A, h_I, h_d are instances. | M:159 (#12); A:54; C:52 | **[C]** h := 2c_ρ/D_* and h_V := 2c_ρ/D_V, the largest passing grid increment (C:66, C:140; A:109; B:139). | adopted for the HQ charters unless an HQ objects: test function h; increment bound Δ_V := 2c_ρ/D_V (Δ_t denotes stage increments φ_t − φ_{t−1}). |
| c_ρ | c_ρ := √log(10/9), from the ESS threshold ρ̄ = 0.9. | C:66; A:169 (same usage) | **[C]** c = store cap in top_c (C:57; M:151), c₄ = centre of islands 1–4 (M:142), c = cancellation depth in the masking law p^{−c}n^{−c/2} (A:79; B:109), c_h in K51, c in T*(c) (K28). | adopted for the HQ charters unless an HQ objects: c only the cancellation depth; store cap c_st (= 40p+1, M:331); c₄ stays; K51's constant c_h stays; ESS drop c_ESS. |
| V | Calibration candidate set V ⊆ Ω (top 20p by γ₀ ∪ top 20p by γ₁ ∪ {∅}). | M:327 row 30; C:140 | **[C]** V in the dilution identity −log π₀(S₀) = V + C − log A ("truths invisible to their own table", K18; A:79(d); B:109(d)). **[C]** V+ and V/H name Proposition/Theorem (M1; V1–V4 draft ids; V10, V11 obligations). | adopted for the HQ charters unless an HQ objects: V = calibration set; dilution terms V_inv, C_dil, A_pr; the theorem is written "Theorem V/H". |
| 𝒯 | Deduplicated reported top store (40p+1 models); Z_𝒯 = Σ_𝒯 ϖ·m. | M:221, M:331; A:89; C:96 | **[C]** 𝒯 vs T (stage count). **[V]** 𝒯_new = top_c(𝒯_old ∪ 𝒮_added) after LS0 (M:151). | keep 𝒯; stage count T (different glyph). |
| Z_𝒯 | Z_𝒯 = Σ_{S∈𝒯} e^{F(S)} = Σ_𝒯 ϖ(S) m(S) ≤ Z. | M:221 (G1); A:89; C:96 | **[C]** F(S) is the score in M:221 and K63, and F_S := ‖·‖_F² (Frobenius) in A:153, D:120. | adopted for the HQ charters unless an HQ objects: F(S) score; Frobenius quantity Fro_S. |
| 𝒪 | Output event (actual statistical output); results are stated as P{𝒪, ·}. | M:168 (#16); C:51 | **[C]** no-output event is written U or U_n (A:99; B:129; D:66; K82), 𝒰 := 𝒪ᶜ (C:24), 𝒪̄ (D:66). **[C]** O_P(·) and "OP-LS0" (C:57) use the letter O. | adopted for the HQ charters unless an HQ objects: 𝒪 output event, 𝒰 := 𝒪ᶜ with P(𝒰); O_P for orders; the premise is "OP-LS0".  |
| U | Evidence upper envelope U = Z_𝒯 + U_m·[1 − Σ_𝒯 ϖ] ≥ Z, with U_m ≥ max m(S). | A:89(e); C:96; D:72(d) | **[C]** U, U_n as the no-output event (above). **[C]** U(X, y, Ŝ) region rule (M:244). **[C]** Σ_U r_b(U) sums over table subsets U (C:107). **[C]** "Uᶜ" event in T21HPM.lean (L-LEAN STATUS.md). | adopted for the HQ charters unless an HQ objects: envelope U_Z; U_m kept; region rule Reg; subsets of a table S_b. |
| LS0 | Local search from the start mode S̃₀ = argmax γ₀, run after the final search; reads no uniforms. | M:150 (#8) | **[C]** OP-LS0 is an execution premise (C:57), LS-score is the scoring-bound lemma (registry LS-score), "LS0 centre" = e4 centre rule (B:129). | adopted for the HQ charters unless an HQ objects: LS0 = the search; S̃₀ the start mode; OP-LS0 the premise; lemma written Lem LS-sc. |
| B | Block-size cap B = min(⌊√n⌋, ⌊√p⌋, B*), B* = 16. | M:307–308 (rows 10–11) | **[C]** B_b = Σ_U r_b(U) table mass (C:107). **[C]** B_r = (4N)⁻¹ΣΣ d (C:294; W2PC2:146). **[C]** B is a seat label (cards "B.R3"). **[C]** "B&B" and B_q = ΣE₀[R(S,S₀)^q] (K94). **[C]** B, B̄ events (C:206; W1PC1). | adopted for the HQ charters unless an HQ objects: B only for the cap; table mass Tab_b; run-card means d̄_{r,meas}; events 𝔈. |
| K | Model-size cap K = min(p, ⌊n/2⌋); k* = min(K, ⌊p/2⌋). | M:301 row 4; C:129 | **[C]** K_n = number of subsets in Song–Liang's equipartition and K ∈ {2, 4, √p} (A:129; B:159; D:93). **[C]** K01–K108 are the meeting's candidate IDs (R0 header). | adopted for the HQ charters unless an HQ objects: cap K; SL subset count K_SL; candidate ids always written "K-ID K46". |
| Ω | Model space Ω = {S : ∣S∣ ≤ K}. | C:52 | none | keep. |
| S₀, S° | S₀ true support; S° appears in the start-mass bound and as the launch centre. | S₀: C:54; S°: A:79(a), A:99, C:58 | **[C]** S° is a reference model in π₀(S°) ≥ (1−q)^{s+1}/(1+e)^s (K15, R0:89; A:79; B:109) and the launch/start-mode centre in Lat(S°), Φ(S°) (A:99; C:58; C:85). The sources do not say whether the two coincide. | adopted for the HQ charters unless an HQ objects: keep S₀; the centre of the local search is S̃₀ (M:150); S° only if the card states which object. |
| Φ | Φ(S) = ∣S △ S₀∣ lattice distance to the truth. | C:58; A:99 | none | keep. |
| Λ_len | Thermodynamic length Λ_len := ∫₀¹ sd_{q_φ}(d) dφ ≤ √J. | A:145 (renamed); B:195; D:82 | **[V]** earlier cumulant Λ(1) = log E e^d and Λ_V (K28) were conflated (W1PC1:257 AMBIGUOUS); all four seats renamed in R2. | keep Λ_len. |
| ν | ν = a₀ + n/2 (IG shape); IG(0.01, 0.01), a₀ = b₀ = 0.01. | C:63; M:299 | **[C]** ν_L residual distribution in C15-KL (C:236). | residual law ν^res_L. |
| G, G_D, E | Gram G = X′X; G_D block-diagonal part; E = G − G_D; H_D = (n+1)G_D + I; A_D = G_D + I; z = X′y, Y = y′y, Q̄ = 2b₀ + Y. | C:63; B:211 | **[C]** G is the statistical model assumption (C:54; B:217 "under G, ORTH"), G1/G2 certificate items (M:221–232), Theorem G (STG-G). **[C]** E, E_S cross-block part vs E1–E3 diagnostics (M:329), E₀ expectation under truth (D:66), E = p+1 edge count (M:182). **[V]** A_S block-diagonal part of R_S (A:153) vs A_D = G_D + I (B:211; C:63). **[C]** Q_S := Y − n z_S′H_S⁻¹z_S (C:195) vs Q = number of iid draws and Q* = p^c n^{c/2} (A:119; B:149; C:118) vs Q_φ round kernel (B:179) vs Q̄. | adopted for the HQ charters unless an HQ objects: Gram G; model assumption "Mod-G"; certificate items "card G1/G2"; E := G − G_D, E_S := Γ_S − Γ_S^bd; per-model residual Res_S; Q only draws (Q*); round kernel 𝒦_φ. |
| ρ | ESS fraction ρ_V(u,v), ρ_full(u,v); ρ̄ = 0.9 threshold. | C:140; B:139; A:109; M:324 | **[C]** ρ = within-group correlation in LH (A:99; B:109, B:129: ρ = 0.4, ∣ψ∣ < ρ). **[C]** ρ_loc = π(Ŝ ∣ {Ŝ} ∪ 𝒩(Ŝ)) (M:238). **[C]** ρ̄ in K51 "(ρ̄ + u_π)". | adopted for the HQ charters unless an HQ objects: ρ for ESS fractions; LH within-group correlation r_in (cross-group ψ stays); ρ_loc → π_loc. |
| g | Group size in LH exhibits (g_max ≤ B < 2g_min). | A:99; B:109; C:55 | **[C]** g = n prior scale (unit information, M:298; C:50). **[C]** g_add, g_del, g_swap, g_sub certificate gaps (M:235–240). | adopted for the HQ charters unless an HQ objects: g_grp; prior g keeps g; certificate gaps g_gap. |
| s | s = n + p (common budget notation). | C:321 | **[C]** s₀ true sparsity, s in K15 (∣S°∣), s ∈ (0,1) tail parameter in exp{−R(1−s)²/(2M)} (A:54(c); B:95(c)), s̄ mean score cost (K87), s_y² variance of y. | adopted for the HQ charters unless an HQ objects: s_np := n + p; tail parameter s_tail; s₀ kept. |
| q | Bridge law q_φ (see γ_φ). | A:153; C:52 | **[C]** q prior parameter in (1−q)^{s+1} (K15); **[C]** q_b(U) = r_b(U)/B_b table law (C:107); **[C]** contraction factor q = 1 − 1/M₁ (C:226); **[C]** SL/FDR threshold q (A:129; B:159); **[C]** q_FDP in K61; **[C]** q₂(S₀) bridge law at t = 2 (B:216: m = min{π₀(S₀), q₂(S₀)}); q_ξ (A:109). | adopted for the HQ charters unless an HQ objects: q_φ bridge law only; prior q_pr; table law t_b; contraction ϑ_L := 1 − 1/M₁; SL threshold q_FDR; FDP level q_FDP; B's tilt q_{t=2}. |
| φ | Bridge index φ ∈ [0,1]; grid 0 = φ₀ < … < φ_T = 1; t real index in q_t. | A:198; C:52 | **[C]** φ₀² is a minimum-eigenvalue bound (B:215; C:150); **[C]** φ₀ is the first grid point (A:198). | adopted for the HQ charters unless an HQ objects: grid points φ_t (t = 0..T); eigenvalue bound λ_*. |
| Z, Z̄₀ | Z = Σ_Ω ϖ·m (evidence); Z̄₀ = start normaliser (exact, K08). | C:52; K08 (R0:82); K35 (R0:124) | **[V]** Z_φ (K104, R0:233), Z̄_φ (A:163), Z_t^σ (W2PC2:106) for the normaliser of the bridge law. | adopted for the HQ charters unless an HQ objects: Z̄_φ := Σγ_φ; Z the posterior evidence as in K35 (Z = m(∅)·Z̄₀·∏E[e^{Δφ·d}]). |
| 𝒞 | Frozen calibration record (grid, tier, N, L, budgets) before stream 10. | M:170 (#18); C:50 | **[C]** C_b block variable sets C_1..C_J (A:153; C:63); C_σ; C_n prefactor (C:195); C in the dilution identity; C = selected cell union in CI card (C:246); C = the seat. | adopted for the HQ charters unless an HQ objects: 𝒞 record; blocks C_b; credible/selected set Ξ; dilution term C_dil. |
| 𝒮 | Scored set (models scored by the run). | M:151; C:57 | **[C]** 𝒮⁺ post-search scored set (A:99; D:66); S models. | keep 𝒮, 𝒮⁺. |
| x_b, x̄_S | Block fit fractions x_b(S) = n·z_{S_b}′H_{S_b}⁻¹z_{S_b}/Q̄, x̄_S = Σ_b x_b(S). | C:65; A:153; D:120 | **[C]** x_t, x_j are design columns (A:129). C's x_b is the score fraction, not the RSS partial R² (W2PC2:81, CEX-W2frac). | keep x_b; columns X_j. |
| β, θ* | Regression coefficients (β in G; θ* = true coefficients in the hypotheses). | C:54; C:150 | **[V]** β and θ* both used in C; β_j ∈ I in interval functionals (A:54(f)). | adopted for the HQ charters unless an HQ objects: θ* for truth; β for the generic coefficient; interval functionals h_I. |
| I_e, H_e, H₀ | I_e ≤ ℓ rebuilds at tier e; H_e calibration population; H₀ = ⌈512·N₀/2500⌉. | C:129; M:312 | **[C]** I identity matrix in H_S = (n+1)G_S + I; I interval; H_r(h) measured average; H1–H3 hypotheses (B:217). | keep with subscripts; hypotheses "(H1)–(H3)". |
| A_r, B_r | Run-card means of AMEND §A1: A_r = N⁻¹ Σ_{i=1}^{N} d(S^{(0)}_{ri}) (initial iid start particles, not reweighted); B_r = (4N)⁻¹ Σ_{k=1}^{4} Σ_{i=1}^{N} d(S^{(k)}_{ri}) (four measured endpoints, plain discrepancy means, not RB records). | AMEND:19–20, :25; C:293–295; W2PC2:146 | **[V]** S2:207–208 and D:178 name the same means d̄_{r,0}, d̄_{r,meas} (D: d̄_{r,0}, d̄_{r,1}). **[C]** B_r clashes with the block cap B, with B_b = Σ_U r_b(U) (table mass) and with B_q (K94); A_r clashes with A(k), A(S₀) and A_S. | adopted for the HQ charters unless an HQ objects: the charters write d̄_{r,0} (= A_r) and d̄_{r,meas} (= B_r); A_r, B_r are the local names of AMENDMENT_HQ_02 and keep that meaning only there. Ĵ = Σ_r Ẑ_r d̄_{r,meas}/Σ_r Ẑ_r − (1/R′) Σ_r d̄_{r,0}. |
| S^{(k)}_{ri} | Model state of particle i of island r at measured round k: k = 0 the initial iid start particles, k = 1…4 the four prescribed measured endpoints (i = 1…N). | AMEND:19–20 | **[C]** S₀ (true support), S° (reference/launch model), S̃₀ (start mode), S_b (restriction to block b); the superscript (k) is a round index, not a power. | adopted for the HQ charters unless an HQ objects: keep S^{(k)}_{ri} with the parenthesised round superscript; S₀ stays the truth, S̃₀ the start mode; never write S^{(0)} for the truth. |
| D (AMEND §A1) | D := max_Ω d − min_Ω d = osc_Ω d, the range of d in the Ĵ tail bound P(∣Ĵ − J∣ > ε ∣ 𝒞) ≤ min{1, 4(M₂ − 1)/R′ + 16D²M₂/(R′ε²) + D²/(R′Nε²)}. | AMEND:31 | **[C]** same letter as D_* (global range bound C_σ + 2b_X), D_V, D̄_n, D_n, D_B, D_PEL (see row D_*). | adopted for the HQ charters unless an HQ objects: write osc d (or osc_Ω d) in the bound; D remains a local abbreviation of AMENDMENT_HQ_02 §A1 and means osc d there. D_* is used only for C's constant (D_* = C_σ + 2b_X ≥ osc d). |
| r̂ | Computed counterpart of C's r: r̂ = δ̂ū̂/[(1 − δ̂)(1 − ū̂)], on the domain κ̂ > 0, δ̂ < 1, ū̂ < 1, δ̂ū̂ < (1 − δ̂)(1 − ū̂). | AMEND:52, :54 | **[V]** counterpart of r in C:64 (r = δ_H a/[(1 − δ_H)(1 − a)]); r is overloaded (see row r). | adopted for the HQ charters unless an HQ objects: r̂_* (hat on the renamed constant r_*); AMEND writes r̂, with that meaning. η̂ = K·log(1/(1 − δ̂)) + ν·log(1/(1 − r̂_*)) (row η). |
| G_{C_b} | Gram matrix of the columns of block C_b, G_{C_b} = X_{C_b}ᵀX_{C_b}; κ̂ = min_b λ_min(G_{C_b}/(n − 1)). | AMEND:49; S2:216 | **[V]** S2:216 and A:200 write R_{C_b} (the within-block correlation matrix), C:304 writes G_b/(n − 1). **[C]** G also means the model assumption, G1/G2 certificate items, Theorem G (row G, G_D, E). | adopted for the HQ charters unless an HQ objects: Γ_{C_b} := G_{C_b}/(n − 1) (within-block correlation matrix), κ̂ = min_b λ_min(Γ_{C_b}); G_{C_b} the Gram block. |
| 𝓗 | Declared list of bounded model-space summaries h: Ω → [0, 1] (METHOD §6.11b); d becomes a default member: **raw d is recorded**. M1 is applied to its globally range-scaled version (d − min_Ω d)/D with D = max_Ω d − min_Ω d > 0. Zero range is handled separately (Ĵ = J = 0). Fixed before stream 10; reads no uniforms. | AMEND:41; R3_A §S5; R3_B §S5; M:159 | **[C]** H_e (calibration population), H₀ = ⌈512·N₀/2500⌉, H_r(h) (measured average), H1–H3 hypotheses, H_S = (n + 1)G_S + I, H_D (row G, G_D, E; row I_e, H_e, H₀). | adopted for the HQ charters unless an HQ objects: 𝓗 (calligraphic) only for the declared list; H_r(h) the island measured average; calibration population H_e; hypotheses "(H1)–(H3)". |
| 𝔼, E_π, E_{π₀} | Expectations: J = E_π d − E_{π₀} d; E[·∣𝒞] conditional on the calibration record. | AMEND:30; S2:208 | **[C]** E = G − G_D (cross-block part), E_S, E₀ (expectation under the truth, D:66), E = p + 1 (edge count, M:182), item ids E1–E3 (M:329). | adopted for the HQ charters unless an HQ objects: expectation written 𝔼 (or E[·] with its law as a subscript, E_π); the matrix is E := G − G_D (row G, G_D, E); item ids "item E1–E3"; no bare E for an expectation under the truth (write 𝔼_{S₀}). |
<!-- END VERBATIM MEET-THM/NOTATION.md §1:30-101 -->

<!-- BEGIN VERBATIM MEET-THM/NOTATION.md §2:103-108 -->
## 2. Counts

- Rows in the table: **68** (the 61 rows of the first draft + 7 rows for symbols of `AMENDMENT_HQ_02_DEFINITIONS.md`: A_r/B_r, S^{(k)}_{ri}, D (AMEND §A1), r̂, G_{C_b}, 𝓗, 𝔼; some rows cover a symbol family, e.g. δ, G/G_D/E, I_e/H_e/H₀).
- Rows with at least one **[C] meaning clash:** **48** (43 + A_r/B_r, S^{(k)}_{ri}, D, 𝓗, 𝔼). Rows with **[V] only** (naming variants): **14** (π, γ_φ, d_X, C_σ, b_X, ε̂_×, δ̂, Ẑ_r, R′, Λ_len, Z/Z̄₀, β/θ*, r̂, G_{C_b}). Rows with both labels: **11** (10 + A_r/B_r). **Rows with any conflict: 62 of 68.**
- Rows with no conflict: **6** (π₀, δ_A/δ_H, δ₁, T_e, Ω, Φ). Every other symbol that the task lists carries at least one conflict.
- Differences that are not notation but affect the final cards, with their state after Round 3: (i) R′_n rate: A and B ⌈log₂(n+p)⌉ vs D ℓ = ⌈log₂(n+p+1)⌉ (A:206; B:254; D:192; S2:235) — **settled** by MINUTES §2.3 and AMEND:63 (D's form); (ii) δ̂ with K (A:200) vs K−1 (D:182; S2:217) — **settled** by AMEND:50 (K−1); (iii) Jeffreys bound J ≤ osc(d)²/4 (A:158) vs J ≤ osc d (B:215; C:261) vs J ≤ 2·osc d (D:126) — different inequalities, not names. **Settled (chair, final audit #9):** M2(a) uses J ≤ D_*. The other forms are valid corollary bounds, which the M2 / LP-IDENT HQs may cite; (iv) ū̂ as a maximum over V (S2:218) vs the global block-table envelope (D:182) — **settled** by MINUTES §2.2 (D's envelope).
<!-- END VERBATIM MEET-THM/NOTATION.md §2:103-108 -->


## N2 · Model, priors, parameterisations and assumptions: quick reference with locations

Summary table; the formulas are the sources' own (see the verbatim blocks in 02a §A1 for the full text). "pos" = transcript position of introduction or ruling after 1040 ("file only" = no discussion in positions ≥ 1040).

| Item | Definition (copied from the cited source) | File and section | pos |
|---|---|---|---|
| Data / standardisation | "Standardise stably: for each column, divide by its maximum absolute value, compute the mean, centre, then divide by the sample SD (denominator n − 1), so ‖x_j‖² = n − 1. Same for y, recording s_y² = ‖Cy‖²/(n − 1) with C = I − 11ᵀ/n." Input domain v3.1 (proposed): n ≥ 2, p ≥ 1 (e3); current code rejects n < 3 | METH3 §4 rule 4; METH31 §2 #25 (e3), §5 row 5, row 7 | [pos 1251] (n = 2 admitted, `degenerate_n`) |
| Likelihood | "y \| β_S, σ², S ~ N_n(X_S β_S, σ² I_n)   (no intercept; y is centred)" | METH3 §5 | file only; model fixed ([pos 1302]) |
| g-prior | "β_S \| σ², S ~ N_k(0, n σ² (G_S + I_k)⁻¹)   g = n (unit information), τ = 1 (one pseudo-observation)" | METH3 §5; METH31 §5 row 1 ("(a), (b) … keep (Felipe)") | [pos 1302] |
| σ² prior | "σ² ~ IG(a₀, b₀),  a₀ = b₀ = 0.01"; "IG(0.01, 0.01): proper, as the project proofs require." Class (a). Its pairwise effect "is not uniformly negligible relative to the gap (nearly collinear example); negligibility needs residual-scale assumptions" (AMENDMENT_HQ_01 #43). ν = a₀ + n/2; Q̄ = 2b₀ + yᵀy | METH3 §5; METH31 §5 row 2; TLF M2 Setting | [pos 1302], [pos 1480] |
| Size prior BB(1,p) | "ϖ(S) = w(k) 1{k ≤ K} / W_K,   w(k) = B(1+k, 2p−k)/B(1, p) = ½ / C(2p−1, k),   W_K = Σ_{j≤K} C(p, j) w(j)" (METH3 §5); in the cards: "\(w(k)=[2\binom{2p-1}{k}]^{-1}\), \(W_K=\sum_{k\le K}\binom pk w(k)\), \(\varpi(S)=w(\|S\|)/W_K\)" (TLF D0 "Prior") | METH3 §5; TLF line 66 | [pos 1302] |
| Cap | K = min(p, ⌊n/2⌋); Ω = {S : \|S\| ≤ K}; k* = min(K, ⌊p/2⌋) | METH3 §3, §5; METH31 §5 row 4; TLF D0 | [pos 1302] |
| Score | m(S), H_S = (n + 1)G_S + I, Q_S = yᵀy − n z_Sᵀ H_S⁻¹ z_S, log m(S) = log C_n − ½[log det H_S − log det(G_S + I)] − (a₀ + n/2) log(2b₀ + Q_S), C_n = (2b₀)^{a₀} Γ(a₀ + n/2) / (π^{n/2} Γ(a₀)); π(S\|y) = ϖ(S) m(S)/Z, Z = Σ_{\|S\|≤K} ϖ(S) m(S). In the cards: m(U) = c_n[det H_U/det(G_U+I)]^{−1/2}(.02+Q_U)^{−ν}, "The common positive c_n cancels from posterior ratios." | METH3 §5; TLF D0 "Score" (line 65) | file only |
| Analytic envelope | m(S) ≤ U_m := C_n(2b₀ + yᵀy/(n+1))^{−ν}; Q_S ≥ Y/(n+1); 1 ≤ det H_S/det(G_S + I) ≤ (n+1)^{\|S\|} | TH10 (S-TARGET) C12; TH04 (d); OB17 (N17) | [pos 1512] (the "≈ 530 nats loose" claim withdrawn) |
| Contrast reduction | posterior = contrast regression of Uᵀy^r on UᵀX, IG shape a₀ + ½, rate b₀ s_y²; "This is not a claim that the working evidence equals a raw-data marginal likelihood" | METH3 §5 "Reduction statement" | file only |
| Blocks | complete linkage on 1 − \|r_jl\|; size-only cut (≤ B); next-fit packing, whole clusters; J ≥ ⌈p/B⌉; B = min(⌊√n⌋, ⌊√p⌋, B*), B* = 16 (class (c), exhaustive-table budget, e1); no correlation cut (w5); for actual blocks ⌈p/B⌉ ≤ J ≤ 2⌈p/B⌉, Σ_b 2^{\|C_b\|} ≤ p2^B/B (TH11) | METH3 §6.3; METH31 §2 #23, #34; TH11 | [pos 1226] (B* flagged), [pos 1302] |
| Tables and start | r_b(U) = m(U)/m(∅); γ₀(S) = ϖ(S) ∏_b r_b(S ∩ C_b); π₀ = γ₀/Z̄₀ (Z̄₀ exact by convolution of block size profiles) | METH3 §6.3; TLF D0 "Start/bridge" | file only |
| Discrepancy and bridge | d(S) = log BF(S) − Σ_b log r_b(S ∩ C_b); γ_φ(S) = γ₀(S) e^{φ d(S)}; q_t ∝ γ₀e^{td} (cards); Z = m(∅) Σ_S γ₁(S) | METH3 §6.3; TLF D0 | file only |
| Moves | m = p + B + 2 labelled steps in a uniformly random order: p Gibbs updates, one uniform swap, B neighbour swaps, one independence proposal (π₀); each γ_φ-reversible; random-order round self-adjoint. Neighbour threshold r_n = √(2 log p / n); fallback 1-NN graph when p > e^{n/2} (w3) | METH3 §6.4–6.5; METH31 #32 (w3), #30 (w1) | [pos 1550], [pos 1593] (N9) |
| Resampling / ESS | multinomial each stage; ESS threshold 0.90 for pilot and grid (class (c), caveat: defines the law of 𝓒); 60 bisection halvings, snap 10⁻¹² (class (d)) | METH3 §6.6–6.7; METH31 §5 rows 27–28 | [pos 1480] (class labels), file MEET-v31 MINUTES §4 |
| Candidate set / restricted ESS | V = top 20p by γ₀ ∪ top 20p by γ₁ ∪ {∅}; ρ_V(u,v) = exp{2F_V(v) − F_V(u) − F_V(2v − u)}; F_V(t) = log Σ_{S∈V} γ₀(S) e^{t d(S)} | METH3 §6.7 | file only |
| Calibration | tiers e ∈ {0,1}, (N_e, H_e, T_e) = 4^e (N₀, H₀, T₀); ≤ ℓ rebuilds per tier (≤ 2ℓ with escalation); 𝒞 frozen before stream 10; streams 0–9 calibration, 10..9+R′ final | METH3 §3, §6.8; METH31 #7, #18 | [pos 1251] |
| Budgets | ℓ = ⌈log₂(n+p+1)⌉; L = max(4, ⌈log₂(n+1)⌉); N₀ = max(2,500, n, p); H₀ = ⌈512·N₀/2,500⌉; T₀ = max(1,000, ℓ²); R = 4 | METH3 §3; METH31 §5 rows 12–18 | [pos 1302] ("Explicit functions of n, p") |
| Islands, evidence | Ẑ_r unbiased given 𝒞; W_r = Ẑ_r/Z; M₂ = E[W_r² \| 𝒞]; pooled Ẑ = (1/R′)Σ Ẑ_r; 95% lower bound 0.05Ẑ (Markov) | METH3 §6.12; METH31 #14, #17 | [pos 1251] ("Ẑ can fail only downward" false) |
| PIP / MPM / HPM | primary PIP̂_j = Σ_r Ẑ_r PIP̂_rj/Σ_r Ẑ_r; secondary equal-weight; MPM = {j : PIP̂_j > ½}; HPM = strict max of log ϖ + log m over every model ever scored; ties: smallest \|S\|, then lexicographic | METH3 §6.10–6.11; METH31 #11 | [pos 1142], [pos 1251] |
| LS0 | one local search from S̃₀ = argmax γ₀ after the final search; reads no uniforms; own provenance; no E3; tie-DP e4 | METH31 #8–#10, #26 | [pos 1107], [pos 1251] |
| Store, certificate | top store 40p+1 (leader stores 20p); 𝒯 deduplicated; Z_𝒯 = Σ_𝒯 ϖm; 𝒯_new = top_c(𝒯_old ∪ 𝒮_added) under LS0; card items G1, G2, L1–L3, R | METH31 §2.1, #9, §5 row 34 | [pos 1251] |
| General-h accumulator | 𝓗 finite list of bounded functions h: Ω → [0,1] fixed before stream 10; H_r(h) = (4N_e)⁻¹ Σ_{q=1..4} Σ_i h(S_rqi); μ̂(h) = Σ_r Ẑ_r H_r(h)/Σ_r Ẑ_r; default 𝓗: size indicators, joint inclusion on neighbour-graph edges (≤ 2pB pairs); d added (raw) by AMENDMENT_HQ_02 | METH31 #12; AMD2D A1 | [pos 1251]; [pos 1626] |
| Reporting | Ĵ = Σ_r Ẑ_r B_r/Σ_r Ẑ_r − (1/R′)Σ_r A_r; ε̂_× = max \|X_jᵀX_k\|/(n−1) over j ∈ C_b, k ∈ C_c, b ≠ c; κ̂, δ̂ = (K−1)ε̂_×/κ̂, ū̂ = Σ_b max_{U⊆C_b} x_b(U), r̂, η̂ | AMD2D A1–A2 (02a §A1.10) | [pos 1614] (Q4), [pos 1626], [pos 1639] |
| §5.3 domain | a := nzᵀH_D⁻¹z/Q̄ < 1; δ_A, δ_H, r < 1; C_σ = νa²/[2(1−a)]; b_X; D_* = C_σ + 2b_X | TH02 (M2) "H-DOM" row | [pos 1614], [pos 1624] |
| T03♯ hypotheses | R1, G, R, SE_λ(j₀), SE_w(m_n^♯; g₀), BM-∞ or BM(c > c₀), j₀ = ⌈(2A+1)s₀⌉+1 | TH09 hypotheses table (TLF lines 446–451) | [pos 1626] |
| Design families | LH (p = 9⌊n^{1/3}/9⌋, groups of nine, within 0.4, two disjoint cross-group links 0.2, coefficients (1, −0.2), σ² = 1; for n ≥ 9⁶, 9 ≤ B ≤ 16 < 18); W (within 1/4, cross ε_n = 1/(np), two coefficients n^{−1/4}; also ε_n = n^{−1/2}/p); ORTH (XᵀX = (n−1)I, p ≤ n−1); G (sampling model: fixed raw design, Gaussian errors, fixed σ² > 0) | TLF D0 rows (02a §A1.3) | [pos 1626] |
| Premises | EX-A, EX-S/H-U, CAL, IND-T, GUARD-W, SR, OP-LS0, e4, "complete scans", MC contract, output contract; 𝒪 output event; statements are P{𝒪 ∩ ·}, "never conditional on 𝒪" | TLF lines 52–88; METH31 #16, #6 | [pos 1251]; [pos 1626] |


## N3 · The v3.1 settings table (METHOD_v3.1_FINAL.md §5, verbatim)

"Generality in (n, p) (ground rule 9): the required table." Classes: (a) modelling convention with a stated reason; (b) explicit function of (n, p) or X; (c) declared resource budget; (d) numerical tolerance; (e) arbitrary. "No setting is class (e) in the method's law." Position of the request: [pos 1214]; of the first answer: [pos 1226], [pos 1302] (49 settings audited); of the HQ approval: [pos 1557], [pos 1584].

<!-- BEGIN VERBATIM MEET-v31/METHOD_v3.1_FINAL.md §5:285-348 -->
## 5. Generality in (n, p) (ground rule 9): the required table

The settings are merged from R2_A §4, R2_B §4 and R2_C §4.1. Classes are the **final** ones (S2 §3 P-9 + S3 R3-4), using AMEND_01's labels:
- (a) modelling convention with a stated reason;
- (b) explicit function of (n, p) or X;
- (c) declared resource budget;
- (d) numerical tolerance;
- (e) arbitrary.

**No setting is class (e) in the method's law** (S2 §3; all seats). Every (e)-by-label item is resolved by e1–e8 or w1–w7. Numerical boundaries quoted from seats are seat-derived unless marked [chair-checked].

| # | setting (value; source) | class | reason | behaviour as n, p grow | action |
|---|---|---|---|---|---|
| 1 | g = n, τ = 1 (M §5; `v3_score.h:175`) | (a), (b) | unit information; ridge keeps m(S) finite for collinear X_S | p-free; τ matters more for p ≫ n (collinear sub-models) | keep (Felipe) |
| 2 | IG(0.01, 0.01) (M §5) | (a) | proper, as the proofs require | pairwise effect ≤ n·b₀\|1/Q₁ − 1/Q₂\| on standardised data; relative to the gap it is not uniformly negligible (two equal-size, nearly collinear singleton models give a relative rate effect → 0.0142; review check, SOL1 #43); negligibility needs residual-scale assumptions; not negligible at tiny n | keep; no universal "negligible" claim (R2_C) |
| 3 | BB(1, p), w(k) = ½/C(2p−1, k), W_K explicit (M §5) | (a), (b) | sparse, multiplicity-aware; the project theory is for it | defined for every finite p; dense growing truths are not its regime | keep |
| 4 | Cap K = min(p, ⌊n/2⌋) (M §3, §5) | (a), (b) | keeps near-interpolating models out | void for p ≤ n/2; binds for p ≳ n/2; K = 1 at n = 2, 3; s₀ > K unrecoverable by definition | keep |
| 5 | Input domain: n ≥ 2, p ≥ 1 (v3.1, proposed; current code rejects n < 3, `v3_preprocess.R:103–107`) | (b) | standardisation and the target are defined at n = 2 | n = 2 → exact branch (K = B = 1, E = p + 1); n = 1 → `degenerate_n`; n = 0 rejected | **e3** (§2 #25) |
| 6 | Exact-constant column drop; `y_constant`; `no_predictors` (M §4) | (a) | removes undefined scales | regime-free | keep |
| 7 | Standardisation: max-abs, centre, SD (n−1) (M §4) | (a), (b) | affine and permutation invariance | regime-free | keep |
| 8 | Near-constant anchored two-pass route at √ε_mach (`v3_preprocess.R:47`) | (d) | cancellation protection, not screening | regime-free | keep; document (R2_C) |
| 9 | Duplicate report \|r\| ≥ 1 − 10⁻¹⁰ (M §4 rule 5; `v3_core.cpp:722`) | (d) | reporting only; duplicates are kept | regime-free | keep |
| 10 | B = min(⌊√n⌋, ⌊√p⌋, B*) (M §3) | (a), (b) | Felipe's rule; B ≤ K and B ≤ p | √p binds for p < n, √n for p > n; B = 1 at n = 2, 3 | keep |
| 11 | **B* = 16** (M §3, §8.7; `v3_core.cpp:142`) | **(c)** | exhaustive-table budget: ≤ 4,096p scores and 65,536p bytes | binds once n, p ≥ 289; theorem SIZE condition: B = 16 covers groups 9..16 | **e1** (§2 #23) |
| 12 | ℓ = ⌈log₂(n + p + 1)⌉ (M §3) | (b), (c) | local-search move cap and rebuild cap | 10–11 at the study, 20 at n + p ≈ 10⁶; not guaranteed enough for growing support (obligation) | keep |
| 13 | L = max(4, ⌈log₂(n + 1)⌉) (M §3) | (b), (c) | burn-in at φ = 1; floor binds for n ≤ 15 | grows with n, not with p; "L logarithmic versus t_mix possibly polynomial" is V10 OPEN | keep |
| 14 | N₀ = max(2,500, n, p) (M §3) | (b), (c) | floor: the 2,500 is a declared budget. "Per-island RB-PIP MC SD ≤ 0.01" is an iid-sampling benchmark only (1/(2√N)); resampling creates dependence, so it is not a guarantee. Grows with dimension | floor binds at the study; N₀ = max(n, p) above 2,500 ⇒ Θ(p·max(n, p)) move steps per stage, Θ(p²) only when n = O(p); score-size costs extra (preflight reports it) | keep; C6 iff a particle-depth claim or any demonstrated fit with p > 2,500 (§3) |
| 15 | H₀ = ⌈512·N₀/2,500⌉ (M §3) | (b), (c) | declared calibration/final ratio 0.2048 | grows linearly; single-tier calibration/final = 0.0512 + 0.2048·I ≤ ≈ 2.1 at I = ℓ = 10 (seat-derived; ≤ ℓ rebuilds per tier) | keep; print the formula (§2 #19) |
| 16 | T₀ = max(1,000, ℓ²) (M §3) | (b), (c) | finite stage ceiling; exceeding it ⇒ `schedule_limit` | the ℓ² term binds only for n + p ≥ 2³¹; ideal-grid T* = O(log log p); as-coded T_n OPEN (Conjecture P) | keep; **w4** (§2 #33) |
| 17 | Tiers e ∈ {0, 1}, factor 4, ≤ 1 escalation (M §3, §6.9) | (c) | bounded escalation, decided before final randomness | ≤ ≈ 16× bridge work; no unbounded rescue; beyond → `schedule_limit` | keep |
| 18 | R = 4 final islands; optional R′ = 4k at N_e, declared before stream 10 (M §3; §2 #7) | (c) | replication and parallel width | fixed 4 gives no growing-dimension accuracy; stacking at N_e lowers the variance of the averaged evidence exactly ∝ 1/R′; for normalised PIPs and general h, 1/R′ is an asymptotic (delta-method) rate under moment conditions, not finite-R monotonicity | keep; **w7** |
| 19 | 4 diagnostic islands per rebuild (M §6.8) | (c) | E2 is an SD over 4 values | regime-free | keep |
| 20 | 4 measured rounds (M §6.11) | (c) | RB averaging after burn-in | constant; correlated rounds are not 4 replications | keep; general-h accumulator (§2 #12) |
| 21 | Exact branch Σ_{k≤K} C(p, k) ≤ (5H₀ + 4N₀)·p (M §6.2) | (b), (c) | enumerate when it costs about one SMC stage of all populations | fixed p is eventually exact as n grows (N₀ ≥ n); all p at n ≤ 5 [chair-checked]; n = 10: p ≤ 36; n ≥ 22: every p ≤ 17 is exact (a uniform sufficient range; the maximum for n ≤ 2,500, while larger n can admit more, e.g. n = 3,000, p = 18; review check, SOL1 #33); growing p ≪ n need not be exact | keep; **w2** |
| 22 | Clustering: complete linkage on 1 − \|r\|, size-only cut, next-fit packing, lexicographic ties (M §6.3) | (b), (c) | deterministic X-dependent partition under the table budget | no correlation cut; O(p²) memory, O(p²)–O(p³) time; packing can merge separated groups | keep; **w5**; C11 (§3) |
| 23 | Tables (all subsets per block, exponent 1, full y) and start π₀ (M §6.3) | (a), (b) | exactly computable composite step, corrected at φ = 1 | constant B bounds each table; the number of blocks grows with p | keep; item 1 = Outcome 2: no depth or speed claim for the start |
| 24 | Neighbour graph: r_n = √(2 log p / n), strict exceedance, forced best partner, ≤ B outgoing, symmetric union (M §6.4) | (b), (c) | chance-correlation scale of p columns; proposal heuristic | r_n → 0 when log p = o(n); r_n ≥ 1 iff p ≥ e^{n/2} (equality impossible for integer n, p) ⇒ 1-NN graph for p > 1; degrees may exceed B | keep; **w1**, **w3** |
| 25 | `cut_group` diagnostic at ρ = r_n (`v3_core.cpp:760–770`) | (b) | descriptive only | can give large components or none | keep, descriptive |
| 26 | Move round m = p + B + 2, fresh random order; multinomial resampling each stage (M §6.5–6.6) | (b), (c) | reversible, self-adjoint kernel; fixed mutation allocation | Θ(p) sequential steps per particle per round: inherent to the kernel (I1) | keep; changing it is WORKHORSE |
| 27 | ESS threshold 0.90, pilot and grid (M §6.6–6.7; `v3_calib.h:31, 79`) | **(c)**, with B's caveat | one-step dispersion budget (weight CV² ≤ 1/9). Caveat: "defines the law of 𝓒; carried by the theorems as a hypothesis (Theorem G needs the same threshold for pilot and grid)" | dimensionless; does not control accumulated error or omitted mass | keep; S3 R3-4 records (c) over B's (a) |
| 28 | 60 bisection halvings; endpoint snap 10⁻¹² (`v3_calib.h:34–43, 82–94`) | (d) | 2⁻⁶⁰ below double resolution on [0, 1] | at very sharp crossings, progress may not resolve; failure is reported | keep |
| 29 | Pilot floor 1/T_e (M §6.6) | (b), (c) | exploratory progress within the ceiling; forced steps counted and trigger escalation | shrinks as T_e grows | keep |
| 30 | V = top 20p by γ₀ ∪ top 20p by γ₁ ∪ {∅}, \|V\| ≤ 40p + 1 (M §6.7) | (b), (c) | O(p) = size of a 1-flip neighbourhood; caps grid cost 60·\|V\|·T_e | the retained fraction of model space vanishes; omitted mass not controlled | keep |
| 31 | Grid convergence = grid equality; ≤ ℓ rebuilds (M §6.7) | stopping rule (b), a deterministic rule (reclassified from the lead's (a), R2_B row 20, by HQ amendment 01; values unchanged); cap (b)/(c) | a flat posterior keeps V changing by MC noise | convergence and P(S₀ ∈ V) OPEN (obligations) | keep; contract (§2 #18) |
| 32 | E1 > 1 nat, E2 SD > 1 nat, E3, forced steps, grid failure/non-convergence, `local_limit` (M §6.9) | (c) diagnostic criteria (S3 R3-4) | odds factor e; triggers define the law of 𝓒 | scale-free; no positive power as dimension grows | keep; labelled heuristics |
| 33 | Low-ESS flag: final stage < 0.5N (M §2) | (c), (b) | report flag | regime-free | keep |
| 34 | Top store 40p + 1; leader stores 20p (M §6.10) | (b), (c) | HPM survives eviction; near-ties, Z_𝒯 and the card read it | linear in p; may truncate many near-equivalent models; restricted summaries labelled restricted | keep |
| 35 | Score cache 500p, clear when full (M §8.6) | (b), (c) | a hit returns identical bits; no effect on the law | key storage up to O(pK) | keep |
| 36 | Near-tie window 10⁻⁹ nat (M §6.10) | (d) | informational; the HPM uses exact equality | can fall below scorer error at large n; η depends on k, Q and conditioning, not on n alone, so a numerical crossing point needs a specified design and model (η ≈ 6·10⁻¹⁰ at n = 200; seat-derived) | keep + **e2** heuristic list (§2 #24) |
| 37 | HPM tie rule: exact equality, then smallest \|S\|, then lexicographic (M §6.10) | (a) | argmax convention | scale-free | keep |
| 38 | MPM threshold ½; α = 0.05 for the Markov bound (M §6.11–6.12) | (a) | Hamming-loss rule; declared confidence | dimension-free; MPM may exceed K | keep |
| 39 | Q recompute below 10⁻⁸·yᵀy; Cholesky → refactor → augmented QR → `numerical_failure` (M §6.13) | (d) | stable evaluation of one score | conditioning worsens with n, K; failure explicit | keep |
| 40 | Scorer error expression η (64ε…), used by `global_certified` (`v3_score.h:240`) | (d) as an indicator; (e) only if read as rigorous | the source calls it heuristic | no uniform validity established | **e5** (§2 #27) |
| 41 | LS0 start-mode tie enumeration cap 10⁶ (`v3_start.h:183`) | (d)/(c) fast path | DP argmax exact; only the tie choice can truncate | ties can proliferate with duplicates or symmetry | **e4** (§2 #26) |
| 42 | Certificate budget (scores, B&B nodes), region rule U, τ (card) | (c) declared certificate-region settings | PC2: Seat C's correction 6 upheld | "unresolved" on exhaustion; L2 needs 2^{\|Ŝ\|} − 1 scores | new in v3.1 (§2.1) |
| 43 | Default 𝓗: size indicators, neighbour-edge pairs ≤ 2pB (§2 #12) | (b) | fixed from (X, y) via the graph | linear in pB | new in v3.1 |
| 44 | Allocation (default 8 GiB, 24 h), preflight, stop-only wall guard (M §2, §8.6) | **(c) declared input** | decides delivery only (Lemma RO) | a fixed allocation cannot support unrestricted growth (V13, by definition); the setup component alone, 8(3np + 3p²) bytes, gives p ≤ [−n + √(n² + 4·8·2³⁰/24)]/2 at 8 GiB (18,818 at n = 200; 11,398 at n = 20,000; review check, SOL1 #39); this excludes all other allocations and workers and is not a feasible-fit threshold (seat-derived) | **e8**, **e6** (§2 #22, #28) |
| 45 | Seed ∈ [1, 2³¹ − 1]; stream map 0–9 (calibration), 10..9+R′ (final); 53-bit uniforms; integer dimensions | (c), (d) | reproducibility conventions; "bitwise" is per binary and BLAS | integer ranges can be exceeded at huge sizes | **e7** (§2 #29); IND-T for 10..9+R′ (§6) |
| 46 | Workers: processes; worker count (§2 #1–#5) | (c) | delivery only; bitwise to serial | regime-free | new in v3.1 |
| 47 | Archive/export limits: V snapshot all if p ≤ 25, else ≤ 10⁴; R Gram copy only for p ≤ 2,000 (`v3_calib.R:15–20`; `v3_setup.R:9`) | (c) | storage choices; full V still builds the grid | truncation grows with p; never reconstruct a "full" V from a snapshot | keep; expose truncation |
| 48 | Other operational constants: exact-branch timing (200 scores, ≥ 64 columns), duplicate-check chunk 512, compiler-lock waits | (c) | profiling and workspace | hardware-dependent; outside the theory | keep |
| 49 | Gram-based scorer; O(p²) correlations and distances (M §8.1) | (c) implementation of the exact target | — | the dominant practical storage limit of v3.1; integer-dimension, stream and allocation ranges and checked-arithmetic rejection are also hard implementation limits (§2 #29, row 45) | v3.2: C7, C11 (§3) |

Sources for rows: R2_A §4 table; R2_B §4 table (rows 1–34); R2_C §4.1 table and §4.2; S2 §0.5, §3; S3 R3-4.
<!-- END VERBATIM MEET-v31/METHOD_v3.1_FINAL.md §5:285-348 -->

### N3.1 Per regime and theory scope (METHOD_v3.1_FINAL.md §5.1–§5.2, verbatim)

<!-- BEGIN VERBATIM MEET-v31/METHOD_v3.1_FINAL.md §5.1–5.2:350-388 -->
### 5.1 Per regime

- **Tiny n (n ≲ 20).**
  - The method runs. n = 2 is admitted (e3).
  - n ≤ 5 is enumerated exactly for every p; n = 6–21 is exact up to the computed p, with SMC above that (B = 2–4, K ≤ 10). The graph is often 1-NN (w3).
  - Fixed-data guarantees hold: exact-branch exactness, unbiased Ẑ_r given 𝓒, HPM = best scored. No asymptotic theorem applies, and lack of identifiability is not a sampler defect.
  - Sources: R2_A §4; R2_B §4; R2_C §4.5.
- **Fixed p, n → ∞.**
  - Eventually exact, because the exact-branch threshold grows with N₀ ≥ n (R2_C §4.4 calls this PROVED; seat-derived). Output claims then reduce to target-posterior theory (V2–V4) plus numerical and delivery conditions.
  - A fixed-p Gibbs result (V9) is a component result, not a description of the production branch.
- **Growing p ≪ n.** Same rules. K = p eventually, but enumeration can still be infeasible. Polynomial-dimensional target theory applies under its other assumptions. Logarithmic L and ℓ are not automatically enough (obligations).
- **p ≈ n.**
  - The ridge target stays proper and K ≈ n/2.
  - Exact-Gram LH (p ≤ n − 1) is the home of T38(b1-LH)/(b2-LH) under the SIZE hypothesis g_max ≤ B < 2g_min.
  - Proofs that need a positive-definite full Gram cannot extend to p ≥ n. That is a restriction of those proof families, not of the target.
- **p ≫ n, polynomial (p ≤ n^A).**
  - Selection theory T01–T03 applies. T38(b1-LH-iid) has XF GAP. Cost is polynomial (T32(i)).
  - The study generator (g = 5, 2g ≤ B) is the obligation PART-pairing (N8).
  - Costs: in this regime N₀ = p gives Θ(p²) move steps per stage (Θ(p·max(n, p)) in general; score-size costs extra), and setup is about 24p² bytes. Both are declared budgets.
- **p ≤ e^{Cn^α}.**
  - The method is defined for every finite pair. r_n = O(n^{(α−1)/2}) → 0, but N₀ ≥ p and quadratic setup become very large.
  - No current theorem covers this range. Song–Liang's Corollary 1 rests on their own prior, support-size, tail and covariance conditions and cannot be imported.
  - Whether our prior admits this range is **OPEN, not impossible** (R2_C §4.5; S2 §3).
- **Joint growth.**
  - Every budget grows polynomially: N₀ and H₀ linearly, L and ℓ logarithmically, B constant, T₀ eventually ℓ².
  - The by-definition limits are the fixed allocation (row 44), the Θ(p) round (row 26) and finite precision.
  - General consistency or useful precision is OPEN.
  - Sources: R2_B §4; R2_C §4.5.

### 5.2 Theory scope (adopted, S2 §3 / S3 R3-4)

"The p ≤ n^A scope of the selection theorems comes from the target theory (Felipe's prior and the proof technique), not from a sampler choice. Song–Liang's e^{Cn^α} rests on their own prior and conditions and cannot be imported. Whether our prior admits it is OPEN, not impossible."

Method-induced restrictions, stated as such:
- the cap K excludes s₀ > K by definition;
- fixed B limits whole-group recovery to g ≤ B. Here "whole-group" means recovery **as a single block**, not impossibility of posterior support recovery when g > B (R3_C R3-4);
- bounded stores can omit posterior mass;
- logarithmic ℓ and L may be short for some proof routes (theorem obligations);
- N₀ ≥ p and full-coordinate rounds impose real computational growth.
<!-- END VERBATIM MEET-v31/METHOD_v3.1_FINAL.md §5.1–5.2:350-388 -->

## N4 · Budgets of the baseline v3 (METHODOLOGY_v3.md §3, verbatim)

<!-- BEGIN VERBATIM METHODOLOGY_v3.md §3:60-76 -->
## 3. Notation and budgets

| Symbol | Definition | n = 200, p = 500 | n = 200, p = 1,000 |
|---|---|---|---|
| p | number of retained (non-constant) predictors | 500 | 1,000 |
| K | size cap, min(p, ⌊n/2⌋) | 100 | 100 |
| B | block size, min(⌊√n⌋, ⌊√p⌋, B*), B* = 16 (implementation limit) | 14 | 14 |
| ℓ | ⌈log₂(n + p + 1)⌉ (local-search and rebuild budget) | 10 | 11 |
| L | max(4, ⌈log₂(n + 1)⌉) (burn-in rounds at φ = 1) | 8 | 8 |
| N₀ | max(2,500, n, p) final particles per island | 2,500 | 2,500 |
| H₀ | ⌈512·N₀/2,500⌉ calibration particles (pilot and each diagnostic island) | 512 | 512 |
| T₀ | max(1,000, ℓ²) stage ceiling | 1,000 | 1,000 |
| R | 4 islands (final and diagnostic) | 4 | 4 |
| tier e | e ∈ {0, 1}; (N_e, H_e, T_e) = 4^e (N₀, H₀, T₀) | | |

These are **declared resource budgets**, not accuracy guarantees. At the study sizes they equal v2's numbers. Tier 1 multiplies
particles and the stage ceiling by 4, so it permits up to about 16× the bridge work. N₀ = 2,500 unless n or p exceeds 2,500.
<!-- END VERBATIM METHODOLOGY_v3.md §3:60-76 -->

## N5 · Item-9 resolutions e1–e8, wording fixes w1–w7, constants paragraph (METHOD_v3.1_FINAL.md §2, verbatim)

<!-- BEGIN VERBATIM MEET-v31/METHOD_v3.1_FINAL.md §2 item 9:175-210 -->
### Item-9 resolutions: e1–e8 (adopted, with S3 refinements)

| # | id | change | M § | exact new spec text (short) | class | 2,400 fits | decided in |
|---|---|---|---|---|---|---|---|
| 22 | e8 | "Seed alone" versus `resource_limit` | Requirements (1), §2 | Requirement (1) becomes: "Runnable from X, y and one integer seed, with no statistical tuning beyond published defaults. The job's allocation (memory, wall time) is a declared (c) input that decides delivery only. Every estimate on 𝒪 is a function of (X, y, seed, binary)." The literal "seed alone" sentence is corrected. | spec text | none | S2 P-9 e8; S3 R3-4 |
| 23 | e1 | B* = 16 relabelled | §3 table, §8.7, §13 | "B* = 16 is a declared **(c) budget for exhaustive tables**. It keeps table work ≤ 2^{B*}·p/B* = 4,096p scores and memory linear in p. An unbounded B = ⌊√p⌋ would make tables super-polynomial. W7-PART's g_max ≤ B < 2g_min is a hypothesis of one partition theorem (B = 14 covers g ∈ 8..14; B = 16 covers 9..16), not a method parameter. The study's g = 5 is the theorem obligation PART-pairing." §8.7's "implementation limit … C++ start (about B ≤ 20)" is replaced by this text. | spec text | none (B = 14 in all 2,400) | S2 P-9 e1; S3 R3-4 |
| 24 | e2 | Near-tie window | §6.10 | "Keep the 10⁻⁹-nat near-tie list (informational; the HPM uses exact equality). Also print η(Ŝ), the scorer's error expression, and a second near-tie list at max(10⁻⁹, 2η(Ŝ)) labelled **heuristic**. The exact pairwise margin is η(S) + η(Ŝ). The store keeps only (F, S), so 2η(Ŝ) is the labelled proxy." | POST HOC | none to any decision | S2 P-9 e2; S3 R3-4 (A, B) |
| 25 | e3 | Input domain | §4 rule 1, §2 statuses | "Reject n = 0. n = 1 → status `degenerate_n` (centred y is 0; no estimates). Zero predictors → existing `no_predictors`. **n = 2 is admitted**: K = 1, B = 1, E = p + 1, so the exact branch runs. At n = 2 every centred non-constant column is proportional to (1, −1), so all singleton models have exactly equal F. The exact output is ∅, or the lexicographically smallest singleton with a p-fold exact tie, reported as such." This n = 2 output statement is R3B's, **seat-derived, unchecked**. Duplicates are kept and reported, not collapsed (M §4 rule 5; `cpp/v3_core.cpp:715–728`); that chair-checked code fact is not a proof of the n = 2 output. The n = 2 admission is a proposed extension: current preprocessing still rejects n < 3 and raw p = 0 (`v3_preprocess.R:103–107`). | ADDITIVE | none | S2 P-9 e3; S3 R3-4 (e3, chair-checked fact; B's sentence) |
| 26 | e4 | LS0 start-mode tie cap | §6.10 (LS0) | as in #8. The invariant "DP output = the prescribed choice" is an OPEN obligation (N3). A and B sketch a greedy index-by-index route with a feasibility max-plus DP (seat-derived, unchecked). | ADDITIVE | none (0/2,400 truncated) | S2 P-9 e4; S3 R3-4 |
| 27 | e5 | `global_certified` | §2 flags, §6.2, §9 | "The exact-branch comparison against the scorer's error expression (`cpp/v3_score.h:240`, `cpp/v3_core.cpp:535`) is a **heuristic numerical margin**, reported as a labelled numerical flag. 'Certified' is reserved for validated arithmetic." M §2's "with numerical comparisons validated" and M §9's "the exact branch returns the exact HPM, PIPs and Z" stay true in exact arithmetic; the floating-point claim is labelled heuristic. | POST HOC (interface) | none (the study used the SMC branch, where the flag is always FALSE, `v3_run.R:147`) | S2 P-9 e5; PC2 `global_certified` verdict |
| 28 | e6 | Memory preflight | §8.6, §4 rule 6 | "Before setup use J ≤ p blocks (not ⌈p/B⌉); after setup use the actual J. Shared and per-worker memory are accounted separately (each concurrent worker's populations, cache, archive). The result is labelled 'estimate', not 'certified peak'." | ADDITIVE (engineering) | none at study size. J = 46–60 (p = 500) and 95–120 (p = 1,000) versus proxies 36 and 72 [chair-checked]; still well under 8 GiB. | S2 §0.5, P-9 e6 |
| 29 | e7 | Checked arithmetic | §2 statuses, §6.2, §7 | "Integer, stream-id and allocation arithmetic are checked before use. Overflow returns the explicit status `unsupported_size`." (Name fixed in MINUTES §4.) | ADDITIVE (engineering) | none | S2 P-9 e7; S3 R3-4 |

### Item-9 wording fixes w1–w7

| # | id | change | M § | exact new spec text (short) | class | 2,400 fits | decided in |
|---|---|---|---|---|---|---|---|
| 30 | w1 | Neighbour scale in §10 | §10 (design bullet) | Replace "between-cluster correlation at the √(log n / n) scale — the same scale as the neighbour threshold" with "… at the r_n = √(2 log p / n) scale of the neighbour threshold". The two scales agree (up to constants) only when log p = Θ(log n); an upper bound p ≤ n^A alone is not enough. No familywise-screening interpretation of r_n. | spec text | none | S2 P-9 w1; S3 R3-4 |
| 31 | w2 | Exact-branch boundary | §6.2 | "all p ≤ 3,000 at n ≤ 5" → "all p at n ≤ 5" (K ≤ 2, E ≈ p²/2 < 4N₀p) [chair-checked] | spec text | none | S2 §0.5, P-9 w2 |
| 32 | w3 | Neighbour fallback | §6.4 | "When r_n ≥ 1 (equivalently p ≥ e^{n/2}; equality cannot occur for positive integers n, p, so this is p > e^{n/2}) no pair exceeds the threshold, so for p > 1 each j keeps only its forced single largest-\|r\| partner: the graph is the symmetric 1-nearest-neighbour graph." | spec text | none | S2 P-9 w3 |
| 33 | w4 | T₀'s ℓ² term | §3 | "For integer n, p and ℓ = ⌈log₂(n + p + 1)⌉, the ℓ² term exceeds 1,000 exactly when n + p ≥ 2³¹ (inclusive; at equality ℓ = 32). T₀ = 1,000 in every practical case." | spec text | none | S2 P-9 w4; S3 R3-4 (C's text) |
| 34 | w5 | No correlation cut | §6.3 (added sentence) | "The dendrogram is cut by node size only (≤ B). There is no correlation-height threshold." This corrects AMEND_01's and any other text implying a correlation cut. M §6.3 itself already describes a size-only cut. | spec text | none | S2 P-9 w5 |
| 35 | w6 | Stale "up to 20" comment | code comment only | the bound is 16 | none | none | S2 P-9 w6 |
| 36 | w7 | Stream map for R′ | §6.1, §6.8, §7 | "Final streams are 10..9+R′, with R′ declared before stream 10." (= #7) | spec text | none | S2 P-9 w7 |

**Constants paragraph (adopted, S3 R3-4, C's text).** "Retain every listed numerical value. The following are declared (c) effort/storage budgets, combined with their (b) dimension-dependent formulas:
- the population and stage floors;
- the calibration ratio;
- the island and measured-round counts;
- the tier multiplier;
- the store and cache limits;
- the exact-dispatch threshold.

ESS 0.90 is class (c): a one-step dispersion/effort budget, not a modelling convention or a full-posterior accuracy guarantee. The 60 bisection halvings are class (d), a numerical implementation convention. One-nat diagnostic thresholds are declared (c) escalation/diagnostic criteria, not rounding tolerances. These values are conventions, not derived optima; changing them is not automatically law-preserving."

"No separate p ≪ n / p ≫ n rule is needed: K, B, N₀, the exact-branch rule and r_n switch regime by formula" (S2 §3; S3 R3-4).
<!-- END VERBATIM MEET-v31/METHOD_v3.1_FINAL.md §2 item 9:175-210 -->

### N5.1 Declared v3.2 path and rejected changes (METHOD_v3.1_FINAL.md §3–§4, verbatim)

<!-- BEGIN VERBATIM MEET-v31/METHOD_v3.1_FINAL.md §3–4:259-281 -->
## 3. Declared v3.2 path (not shipped in v3.1)

| id | change | class | condition / note | source |
|---|---|---|---|---|
| C6 | Per-particle counter-based random streams, e.g. stream = f(seed, island, stage, particle). This enables particle-parallel islands, so the move-round depth loses the N_e factor; population reductions remain. The serial map stays the default reproducibility mode. | **LAW-PRESERVING** (IND-T restated over distinct (island, stage, particle) triples; a one-line re-proof) | **Implemented and law-checked** (R = 4, two stream maps, 20 seeds, compare log Ẑ and PIP distributions) **iff paper 1 claims particle-parallel depth or demonstrates any fit with p > 2,500.** This is HQ's disposition: the union of the two recorded conditions (Seats A/B: any p > 2,500, R2_A:23, R2_B:21, R3_B:44; Seat C: a particle-parallel depth claim). The narrower trigger was not unanimously adopted. Felipe decided (2026-11-03) that paper 1 claims island-level depth only, and the study has p ≤ 1,000, so neither trigger currently fires. Island-parallel results may be reported with their actual cost. | S2 D3d; MA §4 C6; R2_A D3d; R2_B D3d; R2_C D3d; R3_B; HQ (AMENDMENT_HQ_01) |
| C7 | Gram-free scorer, for p ≳ 3·10⁴ or wherever the 8p² private Gram binds | LAW-PRESERVING in exact arithmetic; floating-point fidelity checked separately (VAL-FP-type η) | Declared path for memory (D6(i), §2 #20). Chunked distance computation with the same ordering rule keeps the blocks bitwise (R2_A §4). | S3 R3-2; MA §4 C7 |
| C11 | Faster exact complete linkage (nearest-neighbour chain, O(p²)). The neighbour-graph sort, grid bisection, convolution and pooling also go into the cost account and the roadmap. | ADDITIVE if blocks are reproduced exactly (tie rule kept) | Roadmap for p ≳ 10⁴. Current clustering is O(p²) memory, O(p²)–O(p³) time (`cpp/v3_blocks.h:46–108`). | S2 D3e; MA §4 C11; R2_A D3e |

---

## 4. Rejected changes

| Change | One-line reason | Source |
|---|---|---|
| Backfit start (API-RESID) | WORKHORSE; it needs a full re-run and has no theorem; no exact sampler with a known normaliser was exhibited for it (why arm D was dropped), so Ẑ unbiasedness is not available; ground rules 1, 5, 8 not met. The earlier "headline gain capped at 6/2,400" rationale is withdrawn: a changed start does not nest scored sets. The backfit start is recorded as future work. | S1 item 1; HQ (AMENDMENT_HQ_01) |
| C8: split N_e into R ≫ 4 smaller islands | Neutral for Ẑ to first order (Cor V), but equal-weight PIP bias grows ∝ R/N_tot and masked delivery per island may fall. In effect WORKHORSE (changes a declared budget). | MA §4 C8; S1 item 3 |
| C9: shorter or shared calibration | WORKHORSE (schedule rule). It touches T38(b1′), Theorem G and (0_H). Calibration depth is addressed by (b) and C6 instead. | MA §4 C9; S1 item 4 |
| C10: parallel-in-particle move kernel (informed or tempered-Gibbs flips) | WORKHORSE (move kernel). It breaks R5(b2), BG3 and V5's self-adjointness proof. The m = p + B + 2 factor is inherent to the chosen kernel and is stated, not fixed. | MA §4 C10; S1 item 3; THEOREM_REVISION_INPUTS I1 |
| HPM–MPM disagreement flag | No provable power. Uninformative at π(Ŝ) ≤ 0.37. HPM stays the only decision rule; MPMs are reported descriptively. | S1 item 2 |
| Truth-based gate for the primary PIP (B's R1 rule) | Closeness to the binary truth is objective 3, not posterior accuracy (objective 1). B withdrew it. | S2 D5; R2_B D5; R2_C D5 |
| Rao–Blackwellised joint estimator | The kernel never computes pair conditionals (`cpp/v3_engine.h:349–364`); it would be new code with its own unverified identity. v3.2 at most. | S3 R3-3(b) |
| PSIS-k̂ / R̂ flags | No positive property. Weight-based diagnostics from the observed record have no universal detection guarantee for never-visited modes (E1c, V12; Chatterjee–Diaconis Thm 2.1). | S1 item 6 |
| Feeding certificates back into calibration | POST HOC is the adopted policy: the card is computed after the run and never feeds back. This is a policy, not a mathematical necessity: a certificate computed only during calibration could in principle be frozen into an enlarged 𝓒, while feedback from final-run information would break the frozen-𝓒 contract (§2 #18). | S1 item 6; R3_A R3-1 |
<!-- END VERBATIM MEET-v31/METHOD_v3.1_FINAL.md §3–4:259-281 -->

### N5.2 Depth/cost statement and §9 limitation wordings (#19–#21, verbatim)

<!-- BEGIN VERBATIM MEET-v31/METHOD_v3.1_FINAL.md §2 #19–#21:171-173 -->
| 19 | **Depth and cost statement at the implemented (island) level** | §8 (new §8.8) | <ul><li>"With island parallelism, the particle-round contribution to depth is N_e·(T + L + 4)·(p + B + 2) **sequential elementary-step slots** per island at tier e (not scorer operations or seconds). Score costs, setup (Gram, correlations, clustering, tables), calibration, grid construction, reductions and finite-worker scheduling are added and counted. If R′ exceeds the worker count, islands run in waves."</li><li>"'Depth free of N, H, R' is **not** claimed for v3.1."</li><li>"For a single tier, calibration trajectory work relative to the final run is (1 + 4I)·H₀ / (4N₀) = 0.0512 + 0.2048·I, with I ≤ ℓ the number of rebuilds in that tier. With escalation (two tiers) it is [H₀(1 + 4I₀) + H₁(1 + 4I₁)] / (4N₁). These ratios count trajectory lengths only; other costs still differ. This is **seat-derived, unchecked** (R2_A D4). It matches 3 designs: predicted 0.46 / 0.67 / 1.69, observed 0.45 / 0.62 / 1.76."</li><li>"Calibration can exceed the final run (S4: 1,184.5 s versus 671.8 s), so any wall-clock claim counts calibration, and W-cal is on its critical path."</li><li>"Island-parallel results may be reported with their actual cost. A particle-parallel depth claim, or any demonstrated fit with p > 2,500, requires C6 (§3; HQ's union trigger)."</li><li>"No speed-up versus sequential MCMC is claimed without a stated comparator at matched accuracy."</li></ul> | spec text | none | S2 D3d, D4; S1 §0.2 [chair-checked]; R2_A D4; R2_C D3d |
| 20 | **D6(i) memory wording** (adopted) | §8.1, §8.6, §9 | "A full-coordinate move round visits all p coordinates and requires scoring access to every predictor, through X or sufficient statistics (8np bytes for X). That access may be local, shared or distributed; its computation and communication costs must be counted. Neither a private copy of all X nor a private 8p² Gram matrix per worker is inherent. C7 is the declared Gram-free scoring path, law-preserving in exact arithmetic, with floating-point fidelity checked separately." | spec text | none | S3 R3-2 |
| 21 | **§9 limitation wordings** (THM-SYNTH A2-type corrections) | §9, §6.12 | <ul><li>**(ii)** Restate M §9's "without a usable upper bound on Z" as what is proved. (1) T31(c) (PROVED-LOCKED; PC2 C1(c)): the properties of Ẑ behind the 95% bound (positive, finitely many values, mean Z, iid islands) imply no two-sided relative-error bound: for every c₀ > 0 and η ∈ (0, 1) some such law has P(Ẑ < c₀Z) ≥ 1 − η, so {Z ≥ αẐ} places no upper limit on Z/Ẑ. This is a non-implication from the estimator's law, not a data-specific impossibility. (2) An analytic bound exists, Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} (PC1 claim 1, PROVED). Its gap to Z is data-dependent; PC1's ν·log(n+1) compares against m(∅), not against Z, and is not a universal looseness. The blanket "no *useful* upper bound on Z from the run's record alone" is **not** claimed.</li><li>**(iii)** "The assumption-free part of the evidence lower bound is Markov. max{Z_𝒯, 0.05Ẑ} keeps 95% coverage on the output event" (PC1 claim 2, PROVED; output form CORRECT WITH AMENDMENT).</li><li>**(iv)** "Masked weight variance: the mechanism is PROVED in kind (E1/E2, SEP-B); its severity on the production grid is OPEN (V11)."</li><li>**Checked:** M §9 and §6.12 do **not** contain the A2 sentence "Ẑ errs/can fail only downward". No deletion is needed in M. If the paper discusses the masked regime, it uses PC1 claim 4's corrected wording: "Ẑ underestimates Z with high probability; the complementary rare event carries compensating overestimates of the same total mean; Markov caps them, P(Ẑ > 20Z) ≤ 0.05; the certificate Ẑ < Z_𝒯 detects underestimation only."</li></ul> | spec text | none | S2 §0.1, D6; PC1 claims 1, 2, 4; THEOREM_REVISION_INPUTS M14 |
<!-- END VERBATIM MEET-v31/METHOD_v3.1_FINAL.md §2 #19–#21:171-173 -->

## N6 · Conventions that CHANGED during the thread (with positions)

Each row: old convention → final convention; source of the change; position(s). All rows are Summary text with the sources' own words in quotes.

| # | Convention | Old → New | Source / ruling | pos |
|---|---|---|---|---|
| C1 | Top-store MPM / retention threshold | "⅓" (Seat B proposal) → **½**, sharp: "If S₀ ∈ 𝒮 and δ₁ < ½ then S₀ ∈ 𝒯 and MPM^𝒯 = S₀; ½ is sharp" (TH04(c)); MEET-v31 MINUTES decision 2: "PC1 claim 5: under δ₁ < ½ the HPM and top-store MPM certificates coincide (the earlier '⅓' was FALSE)". The reporting MPM threshold (PIP > ½) was always ½ | MEET-v31 MINUTES §2 dec. 2; PC1 claim 5 | [pos 1251] ("The top-store MPM threshold is ½, not ⅓"), [pos 1286] |
| C2 | "Ẑ can only fail downward" | claim in the earlier draft list (A2-type) → **withdrawn: literally false**. METH31 #21: "M §9 and §6.12 do **not** contain the A2 sentence 'Ẑ errs/can fail only downward'. No deletion is needed in M." Replacement wording (PC1 claim 4): "Ẑ underestimates Z with high probability; the complementary rare event carries compensating overestimates of the same total mean; Markov caps them, P(Ẑ > 20Z) ≤ 0.05; the certificate Ẑ < Z_𝒯 detects underestimation only." TH16 masked-tail clause is stated only in exception-probability form: Ẑ_r ≤ √δ₁ Z except on an event of probability ≤ 2√δ₁ | METH31 #21(iv); TLF S-Z decision note | [pos 1251], [pos 1492] |
| C3 | Primary PIP | equal-weight over islands (METH3 §6.11) → **Ẑ-weighted primary**, equal-weight "secondary (named)"; both MPMs and R_eff reported; truth-based gate withdrawn | METH31 #11; MEET-v31 MINUTES dec. 8 | [pos 1107], [pos 1251] |
| C4 | "No (useful) upper bound on Z from the run" | inherent limitation → **narrowed to T31(c)**: "the properties of Ẑ behind the 95% bound (positive, finitely many values, mean Z, iid islands) imply no two-sided relative-error bound …"; the analytic bound Z ≤ C_n(2b₀ + yᵀy/(n+1))^{−ν} exists; "loose by ≈ ν log(n+1) nats / ≈ 530 nats" withdrawn; blanket "no useful upper bound" moved to "NOT inherent" | AMENDMENT_HQ_01 #26, #27, HQ answer 7; METH31 #21(ii); LIM05 | [pos 1480], [pos 1512] |
| C5 | Stores nested / bitwise fit under LS0 | "stores nested", "bitwise fit" **struck** → 𝒯_new = top_c(𝒯_old ∪ 𝒮_added); scored set nested; best score cannot fall | METH31 #9 | file only (MEET-v31 MINUTES; not discussed in positions ≥ 1040) |
| C6 | "Depth free of N, H, R" | struck for v3.1; depth counted at island level in sequential step slots; particle-parallel depth needs C6 (per-particle streams, v3.2) | METH31 #19, §3 C6; MEET-v31 MINUTES dec. 6 | [pos 1263] ("claim island-parallel depth only for v1"), [pos 1302] (decision 2), [pos 1304] (approved) |
| C7 | C6 trigger | "iff paper 1 claims particle-parallel depth" → HQ union: "… **or** demonstrates any fit with p > 2,500"; neither fires (island-level depth only, p ≤ 1,000) | AMENDMENT_HQ_01 F03; METH31 §3 | [pos 1467], [pos 1480] |
| C8 | Local-search scan size | p + K(p − K) → p + k*(p − k*), k* = min(K, ⌊p/2⌋), times (ℓ + 1) scans | AMENDMENT_HQ_01 #42 | [pos 1480] |
| C9 | IG(0.01,0.01) "negligible" | "vanishes relative to the gap" → "not uniformly negligible …; needs residual-scale assumptions" | AMENDMENT_HQ_01 #43; METH31 §5 row 2 | [pos 1512] (summary: 45 edits) |
| C10 | N₀ cost | Θ(p²) work per stage → Θ(p·max(n, p)) move steps per stage, Θ(p²) only when n = O(p) | AMENDMENT_HQ_01 #40 | [pos 1480] |
| C11 | 2,500 floor | "per-island RB-PIP MC SD ≤ 0.01" guarantee → declared budget; "iid-sampling benchmark only (1/(2√N))" | AMENDMENT_HQ_01 F08/#41 | [pos 1480] |
| C12 | Requirement (1) "seed alone" | → "Runnable from X, y and one integer seed … The job's allocation … decides delivery only"; every estimate on 𝒪 is a function of (X, y, seed, binary); results stated for the potential run and as P{𝒪, ·}, never P(· \| 𝒪) | METH31 #16, #22 (e8) | [pos 1226] (resource_limit flagged), [pos 1251] (decision list) |
| C13 | Input domain | n ≥ 3 → n ≥ 2 admitted (proposed extension; current code rejects n < 3); n = 1 → `degenerate_n`; the n = 2 p-fold tie statement is "seat-derived, unchecked" | METH31 #25 (e3) | [pos 1251] |
| C14 | `global_certified` | rigorous-sounding → "heuristic numerical margin"; "'Certified' is reserved for validated arithmetic" | METH31 #27 (e5) | file only |
| C15 | B* = 16 | "implementation limit" → class (c) budget for exhaustive tables; W7-PART's g_max ≤ B < 2g_min is a hypothesis of one theorem | METH31 #23 (e1) | [pos 1226] |
| C16 | ESS 0.90 class | Seat B (a) vs chair (c) → (c) "with B's caveat: defines the law of 𝓒; carried by the theorems as a hypothesis" | METH31 §5 row 27; MEET-v31 MINUTES §4 | file only |
| C17 | Growth-rate edits allowed | fixed R = 4, L, ℓ → Felipe allows explicit growth rates in n, p "limited to growth rates only, with no other method change" | [pos 1302] (HQ recommendation 1), [pos 1304] (approved) | [pos 1302], [pos 1304] |
| C18 | R′ growth rates | (i) R′_n = 4⌈log₂(n + p + 1)⌉ adopted as optional stacking configuration; (ii) R′_n = 4⌈(n + p)⁶/4⌉ kept only as a sufficient rate inside M1; the ⌈log₂(n + p)⌉ form of Seats A and B withdrawn in favour of D's n+p+1 (NOTATION row R′) | AMD2D §B; MEET-v31 AMENDMENT_HQ_02; NOTATION row R′ | [pos 1626], [pos 1639] |
| C19 | δ̂ | K·ε̂/κ̂ (Seat A) → (K−1)·ε̂_×/κ̂ | AMD2D A2; NOTATION row δ̂ | [pos 1626] |
| C20 | ū̂ | "maximal fit fraction on V" (SYNTH_R2) → global block-table envelope ū̂ = Σ_b max_{U⊆C_b} x_b(U), "not a maximum over V" (a maximum over V ⊊ Ω does not bound all fits) | MEET-THM MINUTES §2.2 S-REP; NOTATION row ū | [pos 1626] |
| C21 | Ĵ form | Seat A trapezoid-of-weighted-stage-variances form → B/C/D form Ĵ = Σ_r Ẑ_r B_r/Σ_r Ẑ_r − (1/R′)Σ_r A_r (A withdrew in Round 3) | MINUTES §2.3 R3-6 | [pos 1626] |
| C22 | Λ | cumulant Λ(1) / Λ_V conflated → Λ_len := ∫₀¹ sd_{q_φ}(d) dφ ≤ √J (length) | NOTATION row Λ_len; TH13 (S9, S10) | [pos 1626] |
| C23 | Jeffreys bound | J ≤ osc(d)²/4 (A) / J ≤ osc d (B,C) / J ≤ 2 osc d (D) → **M2(a) uses J ≤ D_*** (chair, final audit #9) | NOTATION §2 (iii); TH02 (a2) | [pos 1626] |
| C24 | Stage count "continuous in ε" | Q1(b) wording → "the sandwich, local constancy, a continuous upper envelope"; T is a step function that can jump (PC1 example: T = 3 between {2, 4} at ε = 10⁻⁵); "Stable stage count means the sandwich, and nothing more" | HQ ruling Q5 | [pos 1624] |
| C25 | §5.4 "coverage" | frequentist coverage → posterior-content / MC error \|π(C(π̂)) − nominal\|; frequentist coverage = CJ01 | HQ ruling Q2 | [pos 1614] |
| C26 | §5.3 reading | literal one-shot weight stability → bridge-form package (a)(b)(c) + refutation of one-shot (M2(c)); one-shot refuted "independently of correlation" | HQ ruling Q1 | [pos 1614] |
| C27 | Thesis sentence | "In split-and-merge, correlation breaks correctness. In local-to-global SMC, correlation costs only sequential depth and particles, never correctness." ([pos 1044]) → Thesis CD (K96) remark, scoped, "there is no retained non-corollary thesis sentence" (Seat C wording, chair's choice 5) | MINUTES §2.1; TLF Part III | [pos 1044], [pos 1626] |
| C28 | S-STGI | K29/K30 as a supplement card → dissolved; K30 = M7(d) labelled ideal grid; K29 = FW23 | MINUTES §2.2 (corrected) | [pos 1626] |
| C29 | Draft list size | 19 → 24 entries | `MEET-THM/DOSSIER.md`, registrar | [pos 1492] |
| C30 | N9 closure gate | "None" open method questions → "none, conditional on N9 (running)" (AMENDMENT_HQ_01 F01) → N9 passed | AMENDMENT_HQ_01; N9-KERNEL | [pos 1467], [pos 1550], [pos 1584] |
| C31 | Binding-goal failure branch | "descriptive summary, no theorem" / silent fallback → "the binding goal is not met by withdrawal: HQ escalates to Felipe for a method reconsideration or an explicit scope change" for N1 (§13.1), S4 (§5.3), N9 (§5.1) | AMENDMENT_HQ_01 F02 | [pos 1467], [pos 1480] |
| C32 | Notation canonicalisation | seats' symbols → registrar's canonical set (see N1) | NOTATION.md | [pos 1626] (package list) |
| C33 | Item-1 (block start) | "start ablation rule" Outcome 2: keep, no depth/speed claim; the rule script v1 lacked the absolute 9-design gate → v2 (`apply_rule_v2.py`), same Outcome 2 | MEET-v31 MINUTES §3; AMENDMENT_HQ_01 F04 | [pos 1280], [pos 1467] |
| C34 | Confirmatory start test | licensed claim: prior start underestimates evidence on all three designs (6–13 nats median); cost claim formally "inconclusive" | `theory/ABL-CONF` REPORT (7e12cf5) | [pos 1669] |
| C35 | Credits | $144 API (HQ plan) → "no API", subscriptions → [pos 1673] "remaining $19 of cloud and the remaining $121 of the other credit" | user messages | [pos 1046], [pos 1324], [pos 1673] |

Note on the position column: "[pos 1626]" in rows C19–C23, C28 and C32 means "contained in the package reported at that position"; the thread itself does not discuss those items. "file only" means no discussion in positions ≥ 1040.

**UNCERTAIN (naming).** For "the MPM threshold ⅓ → ½": the transcript statement at [pos 1251] speaks of "The top-store MPM threshold"; MEET-v31 MINUTES dec. 2 ties it to the δ₁ < ½ retention/HPM-MPM-coincidence statement. Both describe the same change; the PIP > ½ reporting rule never changed.

## N7 · Assumption and premise names used in the final cards (definitions)

Defined once in 02a §A1.3 (TLF lines 52–88): D0, Score, Prior, Start/bridge, G, LH (design and non-vacuity), W, EX-A, MC contract, Output contract, EX-S, CAL, IND-T, GUARD-W, SR, OP-LS0, e4, complete scans, 𝒪 and D_n. In addition:
- **H-DOM** (matrix domain of M2): TH02 row "H-DOM (matrix domain)" (TLF line 148).
- **T03♯ hypotheses R1, G, R, SE_λ(j₀), SE_w(m_n^♯; g₀), BM-∞ / BM(c)**: TH09 hypotheses table (TLF lines 446–451).
- **Lemma RO / CEX-guard / GUARD-W**: TH15 (S-OUT) card C13 (TLF lines 980–988): "Under A and stop-only statistical coupling GUARD-W, a potential-run event B satisfying P(B | 𝒞) ≤ α gives P(𝒪 ∩ B | 𝒞) ≤ α. It does not imply P(B | 𝒪, 𝒞) ≤ α." Status: "GUARD-W: not audited."
- **SIZE**: g_max ≤ B < 2g_min; holds on LH for n ≥ 9⁶ with g = 9 (TH05 hypotheses; TH11).
- **N-labels (obligations)**: OB01–OB17 = N1–N17 in 02a §A5.4. Registrar rule (NOTATION row N): "obligations always written 'obligation N1' (never bare N1 in a formula)".
- **K-IDs**: K01–K108 are the meeting's candidate IDs (`MEET-THM/R0_DIFF.md`), written "K-ID K46"; not archive IDs.


---

# Appendix (archive): campaign-era notation and where it is defined

The sections above cover the notation of the FINAL documents (v3.1, MEET-THM). The campaign-era results in `02b_theory_campaign_history.md` use the notation of their own branches. These are the authoritative definitions:

| Scope | Authoritative file | Notes |
|---|---|---|
| Pre-campaign shared definitions (G, R, R1, SE, BM, DX, EX-A, EX-S, CAL, the model and score F(S), D_S, Q_S, w(k), …) | `branch_snapshots/main@c4ef0dc/Docs/Theory/theorems/00_COMMON.md` | Used by T01–T39 and by all wave runs. Copies reviewed by Astra are at `branch_snapshots/A-REV4/snapshots/00_COMMON.md` |
| Method v3 (blocks, tables, start π₀, bridge, moves, calibration, HPM, evidence) | `branch_snapshots/main@c4ef0dc/Docs/Methodology/METHODOLOGY_v3.md` and `.../MASTER_Methodology_and_Plan/` | v3.1 is a diff against this file (`MEET-v31/METHOD_v3.1_FINAL.md`) |
| Paper-1 canonical notation (registrar) | `branch_snapshots/MEET-THM/NOTATION.md` | Governs the HQ charters. The verbatim cards keep the seats' own symbols |
| Linked-hub family LH, LH-iid, exact-Gram LH, LH-LAT | `branch_snapshots/W1-EXP/PROOF.md` §4, `W3-PXN/PROOF.md`, `W5-VMASK/`, `API-PXNGAP/` | "(b1-LH-iid)" means different objects in FW10/K71 and in 02b TH-entries (see 02b theme 2) |
| T38 parts (0), (a), (b1), (b1′), (b2), (c) and the routes D2/LS0/B2 | `branch_snapshots/T38-RECORD/T38_STATEMENT.md` (v3, statement of record) | Earlier versions are in W1-T38E §7, W4-T38FULL and W6-FIXREV1 (see 02b theme 7) |
| Truth dominance TD(d,m), TD′, TD′_P, TD′_∞, PGD, POS | `W1-T37R`, `W3-VT37R`, `W6-FIXREV2/STATEMENTS.md`, `W3-PGD`, `W5-VPGD` | Literal TD is unsatisfiable (Prop 1-TD); see 02b theme 4 |
| Dilution decomposition V, C, A_t, λ_b, η_b | `branch_snapshots/O-DILUTE/THEORY.md` §0–§1 | −log π₀(S₀) = V + C − log A (Theorem E / Cor. E1) |
| Stage laws, Theorem G, T_bd, the Chebyshev schedule | `O-STAGES/`, `API-T26BUD/`, MEET-THM M7 | Theorem G(i) matches Štefankovič–Vempala–Vigoda 2009 (LIT-SMC) |
| Certificates (box certificate, Lemma M, card C1–C6) | `O-CERT/`, `O-VCERT/`, `MEET-v31/evidence/2026-11-03_PC2_certificate_card.md` | |

## Known name collisions (do not confuse)

These are collected from the 02b theme reports:
- "Lemma S": the shift lemma vs the ESS-share lemma (W1-T38E) vs the HPM order-independence lemma (METH-AUDIT `MA-LemmaS`, K63).
- "Lemma U": W2-PREM vs W3-PXN.
- "Prop M": W4-SHARE vs A-DRAFT.
- "Theorem SEP" (W7-SEP) vs "Lemma SEP" (O-WSTAB).
- "BASIN": the T23 hypothesis vs W7-SEP's Proposition BASIN.
- "Lemma R": O-BGIBBS vs W3-PGD (Lemma R-PGD).
- "Theorem B": the restated T24 (W1-T24G) vs W1-T37R's Theorem B (T37(ii)).
- "Theorem A": the refined T37(i) vs the A-DRAFT / O-PW2 / W5-FAVIID / T26 "Theorem A"s.
- "E1/E2": the W1-T03R lemmas vs the API-MASKZPIP theorems.
- "IND": trajectory independence vs independence-move acceptance.
- "C1": registry conflict C1, card C1 (Song–Liang, K97), and certificate clause C1.
- "T05": the oracle-gap result vs the R0_E partition item.

Always resolve through `ID_REGISTRY.md`.
