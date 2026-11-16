# W3-MISR-R — PLAN (v1.0, 2026-11-15)

Tier B rider, NORMAL mode. Targets: `BRIEF.md` items 1–3; statement: `STATEMENT.md` v1.0 (delta over W3-MISR v1.3).
No new key lemma: every proof is a short composition of checked or registered statements (BASE Lemma R′, MIS-R (i),
(ii), Cor-G(b) proof G.2, the freezing step M.3; [POST2] Claim D(a), D(b); [POST2] bridge A0). Kill budget 3 (BRIEF).

## 1. Lemma files and proof sketches

| file | claim | proof sketch | depends on |
|---|---|---|---|
| `lemmas/G1_min.md` | CorG-min (a)–(e) | (a) W := Uᵀ(ξ̃ + ε)/σ_𝒞(X), ξ̃ := X_𝓜β_𝓜 − Xγ(X) (α1 and a1 vanish: Uᵀ1 = 0). By (N), ε ⊥ (X, ξ̃); the conditional characteristic function of Uᵀ(ξ̃ + ε) given X is e^{−(τ²(X)+σ²)‖t‖²/2}, at X-measurable arguments t = s/σ_𝒞(X) too (disintegration form of the §1 convention); so for every Borel D, Q_D(·) := P(W ∈ ·, X ∈ D)/P(X ∈ D) has cf e^{−‖s‖²/2}: W ~ N_N(0, I) independent of σ(X). κ_n Borel in X; null event handled as BASE G.1 (`G_corollaries.md:32-34`). (b) Uᵀ applied to (OV); convolution with (N) for the conditional law of y^r. (c) Divide conditional cfs (Gaussian cf never vanishes): E[e^{itᵀUᵀξ̃} | X] = e^{−(v(X)−σ²)‖t‖²/2}; \|cf\| ≤ 1 forces v ≥ σ²; a regular conditional law of Uᵀξ̃ given X exists (ℝ^N Polish), its cf agrees on a countable dense set of t a.s., hence everywhere by continuity. (d) For a.e. x, tᵀUᵀξ̃ and tᵀUᵀε are independent given X = x with Gaussian sum: Cramér's decomposition theorem ⇒ tᵀUᵀε Gaussian for every t ⇒ Uᵀε ~ N(b, Σ_ε) (Cramér–Wold); then divide cfs as in (c). (e) (E1) Gaussian conditioning with the Moore–Penrose inverse (range(Σ_𝒞𝓜) ⊆ range(Σ_𝒞𝒞) for a PSD joint covariance, so the residual is uncorrelated with, hence independent of, x_𝒞); (E2), (E3) direct. | BASE G.1, §0 (GR^c), §4 (GR^c \| 𝓕_n), MIS-R (ii) by statement |
| `lemmas/G2_corr.md` | CorGb-plus | Copy of BASE G.2 (`G_corollaries.md:36-65`) with changed lines marked [R-#]: [R-1] column rescaling x_j ↦ x_j/√Σ_jj leaves X = CxD_x⁻¹, hence π_𝒞, unchanged, maps Σ_𝒞𝒞 ↦ R, β^𝒞_j ↦ √Σ_jj β^𝒞_j, (OV) to (OV) with γ_j ↦ √Σ_jj γ_j, and leaves supp β^𝒞, β^𝒞ᵀΣβ^𝒞 and ρ_n^{BM} unchanged; so run G.2 with (c_pop, C₀) = (c_R, 1), φ₀² = c_R/8; [R-2] Σ_𝒞𝒞 ≻ 0 replaced by the floor on supp β^𝒞 in step 3; [R-3] step 4 with c := c₀ + 1 if L := liminf ρ = ∞, c := (c₀ + c_R L/16)/2 otherwise; eventually (c_R/16)ρ_n ≥ c; [R-4] G.1 replaced by CorG-min (a) (deterministic γ, τ²); [R-5] the bound read off the last display (`:59-61`). | BASE G.2, MIS-R (ii)(a), POST2:A0, CorG-min |
| `lemmas/H1_plus.md` | CorH-plus | (a′) as BASE G.3 (a) (`G_corollaries.md:83-87`) with the margin step replaced by the premise: by Lemma R′(b) (BASE `:90-93`, parameter part) the law of δ_n under P_{κ_n} equals its law in the unit-noise model, so δ̃_n → 0 in P̃-probability; the unit-noise array (x_n, β_n/√v_n, 1) satisfies R1 (s fixed, 2 ≤ p ≤ n^A, s ≤ K, σ*² = 1, G), (E; M), (F₀; φ₀): the hypotheses of [POST2] D(a) (`:107-111`); the scaling map T sends B^a_n, H^a_n to the unit-noise bad sets (BASE G.3 lines 74-87). K^a: off B^a_n(κ; M′_n) with M′_n := min(M_n^{1/2}/2, n^{1/4}) → ∞, the (KL) bound gives k̄_n ≤ M′_n²/n + M′_n/(2n) ≤ M_n/n for n ≥ 16, M_n ≥ 1. (b) BASE G.3 (b) verbatim, plus K^b: off B^b_n with M_n := (log n)^{1/2}, k̄_n ≤ log n/n + C_H log n/(2n). (KL) closed form of KL between normals; x − 1 − log x ≤ 2(x − 1)² for x ≥ ½ (Taylor, second derivative 1/ξ² ≤ 4). Reading (i): the true contrast law is in the working contrast family. | BASE R′(b), G.3; POST2:D |
| `lemmas/H2_uniform.md` | CorH-U | **H0 (fillers).** For s ≥ 1, A ≥ 1 and n ≥ n_f(s, A): p_f := max(s, 2) orthogonal centred columns with ‖x_j‖² = n − 1, β := 1_{[s]}, v := 1. This κ^f_n lies in 𝒦^λ_n(s, A, s, 1, C_f, c) for every c (for n large), with C_f := C_OS(s, A, c_D = ½) of [POST2] A0 ((F_w; 1) holds: all Gram eigenvalues are n − 1). **(U-b)** If the claim fails there are ε > 0, s ≤ s̄ and n_k → ∞ with κ_{n_k} ∈ 𝒦⁰_{n_k}(s, …) and P_{κ_{n_k}}(Π(B) > η) > ε. Put κ_n := κ_{n_k} at n = n_k, κ^f_n elsewhere: an array with (E; max(M, s)), (F₀; φ₀), (OS; max(C_OS, C_f)) for all large n; CorH-plus (b) (C_H depends on (s, A) only) contradicts the subsequence. **(U-a)** Same, with CorH-plus (a′): along n_k, P(δ > η′) ≤ sup_{𝒦^♭} → 0 by (UP); along the fillers E δ ≤ C r_n by BASE MIS-R (i) on 𝒦^λ_n. **(RD)** Π(· \| x, y^r) is a function of (x, Uᵀy^r) ([POST2] `:101-103`; `D_hellinger.md:8-11`: it uses y_c = Uᵀy^r and s_y = ‖Uᵀy^r‖/√N); g_n(κ, w) := Π(B_n(κ) \| x, Uᵀxβ + √v w) is Borel on 𝔎_n × ℝ^N (Tonelli on each stratum, as BASE `M_misr.md:134-138`); freezing (`M_misr.md:143-149`): P(Π(B_n(κ_n)) > η \| 𝓕_n) = Ĝ_n(κ_n) with Ĝ_n(κ) = P_κ(Π(B_n(κ)) > η) ≤ ε_n on 𝒜_n; then the tail bound and the η-family as BASE M.3 (c). | CorH-plus, MIS-R (i), POST2:A0, BASE M.3 |

Numerics: `numerics/N1_boundary.py` (exact enumeration of the coded target π_𝒞, formula of [W3P] §0, p = 5): inside
CorG-min with a non-Gaussian (Bernoulli, dependent-row) candidate design; just outside (OV^c) — (i) heteroscedastic
omitted part (covariance not scalar), (ii) omitted part non-linear in the candidates (no γ), (iii) non-Gaussian
(Rademacher-mixture) omitted part. Reports E δ and P(HPM ≠ target) for n ∈ {100, 400, 1600}. Run with `nice`, one core,
TMPDIR under `/home/fb31/SMC_Theory_Department/tmp/`.

## 2. Chain and hours (Opus hours, lead)

| step | what | hours |
|---|---|---|
| 1 | PLAN, STATEMENT, TARGET (incl. N1), READER_DELTA draft | 1.0 |
| 2 | Sol statement lock (blind, fresh) → fixes → lock; CP1 | 0.3 + wait |
| 3 | lemmas G1, G2, H1, H2 (after CP1 go) | 1.0 |
| 4 | one Sol line-check batch (4 lemmas; a second agent only if the first finds a repair) | 0.3 + wait |
| 5 | REPORT (+ DIST HEURISTIC/OPEN pointer), DEPS.tsv, citecheck (copy of BASE `citecheck.py`) | 0.4 |
| 6 | council R1: Sol (OpenAI seat) + Opus 5.5 high (Claude seat), fresh, blind; diff round if needed | 0.3 + wait |
| 7 | CP3 | 0.2 |
Total lead ≈ 3.5 h. OpenAI reviews: lock, line check, council seat (3; 4–5 with a re-check or diff round).
Cut-off: CP3 by Wed 2026-11-18 18:00 CT. Clause to drop first if time runs short: CorGb-plus (BRIEF item 3, "only if
trivial") → named open item.

## 3. Risks
- (U-a)/(U-b) rest on the subsequence-with-fillers argument; H0 must give configurations in a class with constants
  independent of n (checked in the line check). If a reviewer rejects it, fall back to (RD) and (U) for the
  (a)-type sets only via a direct uniform re-run of [POST2] D2 (short: every term there has a class-uniform law) —
  that would be a copied lemma with [R-#] marks, not a new key lemma.
- §2(d) uses Cramér's decomposition theorem (Cramér 1936; e.g. Linnik & Ostrovskii 1977); stated as a remark-level clause.
- Everything conditional on W3-POST2:D, :C, :A0 (unaccepted) as in BASE.
