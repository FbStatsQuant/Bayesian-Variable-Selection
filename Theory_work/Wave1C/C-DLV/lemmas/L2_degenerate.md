# L2 — Lemma S: input, degenerate and numerical paths are empty (a.s.) on the classes

Status: PROVED (by this seat); R02: S.1, S.2 and D2 survive; S.3 list extended per R02 #5. Paths refer to INVENTORY.md; code = `Scripts/SMC_BVS/core/`.

## S.1 Inputs (A1–A7)
Setting: model G (fixed or random design X with p ≥ 1 columns, y = α1 + Xβ + ε, ε ~ N(0, σ²I), σ² > 0), n ≥ 3, the
seed a declared integer in [1, 2³¹ − 1], the allocation a declared list of two finite positive numbers.
- A1 (`v3_fit.R:63-64`), A2 (`v3_fit.R:66-69`): excluded by the declared seed and allocation (class (d)).
- A3 (`v3_preprocess.R:97-107`): X is a numeric matrix with finite entries (fixed design: by the class definition D0;
  LH-iid: Gaussian rows are finite a.s.), y = α1 + Xβ + ε is finite a.s., n ≥ 3 and p ≥ 1. So P(A3) = 0.
- A4 (`v3_preprocess.R:111-114`): a column is dropped only if all its entries are exactly equal. Exact-Gram LH and the
  GEN fixed designs are standardised with ‖x_j‖² = n − 1 > 0 and centred, hence nonconstant; for random designs with a
  nonsingular Gaussian row law each column is nonconstant a.s. (n ≥ 2). So no column is dropped (p unchanged) and
  P(A4) = 0.
- A5 (`v3_preprocess.R:115`): y constant means ε ∈ {c1 − α1 − Xβ : c ∈ ℝ}, a line in ℝⁿ, which has Lebesgue measure 0
  for n ≥ 2; so P(A5) = 0.
- A6 (`degenerate_n`, spec e3): requires n = 1; excluded by n ≥ 3. A7 (`unsupported_size`, spec e7): excluded by
  IDEAL-W.

## S.2 Numerical failures (C1–C5) are impossible under EX-A
The only source of `NumericalFailure` is `Scorer::score` (`cpp/v3_score.h:226-238`), thrown only if all three routes
fail. Route 1 (`try_chol`, `cpp/v3_score.h:175-188`) on a model S with 1 ≤ k = |S| ≤ K forms H = (n+1)G_S + I_k and
A = G_S + I_k with G_S = X_SᵀX_S ⪰ 0, so H, A ⪰ I_k are positive definite. In exact arithmetic the Cholesky recursion
`chol_inplace` (`cpp/v3_score.h:76-90`) produces pivots d_j = (L_jj)² > 0 for a positive definite matrix (they are
ratios of leading principal minors), so its failure test `!(d > 0) || !isfinite(d)` (:80) never fires. In
`finish_from_factors` (:204-224) the log-determinants are finite, and
  Q = yᵀy − n zᵀH⁻¹z ≥ yᵀy − (n/(n+1)) yᵀy = yᵀy/(n+1) > 0,
because X_S((n+1)X_SᵀX_S + I)⁻¹X_Sᵀ ⪯ (n+1)⁻¹I (singular values σ²/((n+1)σ² + 1) ≤ 1/(n+1)) and yᵀy = n − 1 > 0 after
standardisation (S.1). If the code recomputes Q by `q_nonneg` (when Q < 10⁻⁸yᵀy, possible only for n + 1 > 10⁸), the
recomputed value equals Q exactly: with β = nH⁻¹z, ‖y − X_Sβ‖² + (‖X_Sβ‖² + ‖β‖²)/n = yᵀy − 2βᵀz + n⁻¹βᵀHβ =
yᵀy − n zᵀH⁻¹z. Hence 2b₀ + Q > 0, log m(S) is finite (:222-223), `try_chol` returns true, and `score` returns at
:233. For k = 0 the score is log m(∅) directly (:232). The k > K throw (:230) is an internal invariant: every caller
passes models of size ≤ K (additions at |S| = K are excluded: Gibbs `o_j = 0`, local search `continue`,
`cpp/v3_engine.h:390`; π₀ draws have size ≤ K; tables have B ≤ K for n ≥ 3, SoP/02_method.tex:193-194). So C1–C5
are empty under EX-A. (No claim is made for floating point; VAL-FP is a separate engineering check.)

## S.3 Unreachable paths (D2, X2)
- D2 `grid_failure_no_escalation` (`v3_calib.R:153`) requires status ok, last tier without a grid, and e = 0. A tier
  without a grid had a failed construction, which sets `trig$grid_failure` (`v3_calib.R:82, :114`); then
  `fired = TRUE` (:145) and, since e = 0, the loop either escalates (:149) or stops with `resource_limit` (:148). So
  the final tier is 1 whenever a tier-0 grid failed and status is ok: D2 is unreachable.
- X2 (call-graph invariant argument; R01 #9, extended after R02 #5). The internal error sites reachable from `v3_fit`
  and the invariant that excludes each:
  (i) block-size check in `cpp_setup` (`cpp/v3_core.cpp:143-145`, from :269-311): blocks come from the size cut "until
      every retained cluster has at most B members" and next-fit packing "into blocks of at most B members"
      (SoP/02_method.tex:189-192) with B ≤ 16 = B_MAX, so every block has 1..B members;
  (ii) `setup required` (:390): `cpp_final_run` is called only after `v3_setup` built the graph (`v3_fit.R:106-116`);
  (iii) retained-index / duplicate / NA validation of models (`cpp/v3_core.cpp:24-35`), reached by inherited-model
      conversion (:413, :425): inherited models are calibration-scored models, i.e. sorted distinct retained indices
      exported by the same conversion (`to_orig`), so they validate; their size is ≤ K (:416);
  (iv) provenance enum validation (:54-55, reached at :427-430): the provenance was exported by `event_to_list` from
      the declared enum names (`cpp/v3_ledger.h:9-16`), so the lookup succeeds;
  (v) `nth_nonmember out of range` (`cpp/v3_engine.h:143`, called at :151): it is called with an index drawn below the
      current count of non-members (swap proposals), and models keep bits consistent with members (set/add/del
      operations update both);
  (vi) the scorer's k > K throw (`cpp/v3_score.h:230`): S.2;
  (vi″) the equal-length check of `cpp_build_grid` (`cpp/v3_core.cpp:546`): `cpp_cal_V` fills lg0 and d with one entry
      per model of V (:679-683); and the seed re-checks (`v3_calib.R:137`, `v3_run.R:173`) pass by the declared seed;
  (vi′) the context assertions of `v3_context` (`v3_setup.R:8`: X a matrix, length(y) = nrow(X), length(orig) =
      ncol(X), orig strictly increasing), reached from `v3_fit.R:91` and from the exact-branch timing submatrix
      (`v3_fit.R:12`, columns 1..m_t with orig defaulting to 1..m_t): preprocessing returns a standardised numeric matrix,
      a response of length n and `kept` strictly increasing (`which`), and the timing submatrix keeps these properties;
  (vii) the frozen-grid checks (`v3_run.R:78-80`) and class assertions (`v3_run.R:172`): the grid is a successful
      construction (L3 Lemma 3.4: starts at 0, strictly increasing, ends at 1), the objects are built by
      `v3_setup`/`v3_frozen` with their classes.
  Validation errors of auxiliary public entry points (e.g. `cpp/v3_core.cpp:109, :209-216`) are not on the call graph.
  This is a code-reading claim; R02 #5 judged these invariants "appear sufficient".

## S.4 Consequence
On the classes, with n ≥ 3 and under EX-A and IDEAL-W: P(A1 ∪ … ∪ A7 ∪ C1 ∪ … ∪ C5 ∪ D2 ∪ X2) = 0.
