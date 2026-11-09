# C-DLV council round 2 — Claude Opus 5.5 seat (fresh; judged the files as they stand; C1_* not read)

Read: STATEMENT.md, INVENTORY.md, METHOD_REQUIREMENTS.md, lemmas/L1–L5, numerics/SUMMARY_dlv.md, N1_psi_{F,M}.txt,
N2_grid_lemmas.txt, N2b_pilot_and_counts.txt, N3_SUMMARY.md, N4_SUMMARY.md (header), dlv_constructions.csv / N4_constructions.csv
(recounted), REPORT.md, LOG.md, CHECKPOINT.md, reviews/CITECHECK.txt (tail). Code: production core `Scripts/SMC_BVS/core/`
— v3_fit.R, v3_calib.R, v3_run.R, v3_preprocess.R, v3_setup.R, cpp/v3_calib.h, cpp/v3_runtime.h, cpp/v3_score.h (scorer),
cpp/v3_engine.h (island loop, local search), cpp/v3_start.h (start_mode), cpp/v3_core.cpp (pilot, diag, V, final run,
exact enumeration). Spec: SoP/02_method.tex:300-410. Cited: W1-GEN STATEMENT/REPORT/L5_assembly, W1-PXN STATEMENT
and LS_P6_repair, W1-N3 L7.

## What I re-derived independently
- L3 Lemma 3.1 (identity), Lemma 3.2 (Peano kernel, monotonicity of ρ(u,·)), Cor 3.2′, Lemma 3.3 (k ≤ T_e: checked against
  `pilot_next_phi`, v3_calib.h:30-46, and the adaptive loop, v3_engine.h:303-341, incl. an unforced lo in the snap band
  followed by a forced step to 1), Lemma 3.4 (read line by line against `build_grid`, v3_calib.h:68-98: the
  "smallest dyadic mid" characterisation of `non_progress`, validation never failing for unsnapped points, the
  post-append `too_many_intervals` check), Prop 3.5(a) both versions.
- L5 Lemma 5.0 (h = (j+1)δ ≤ 2jδ), Lemma 5.1 (closed form; maximiser a = 1/c; (i)–(iii)), Lemma 5.2 (perturbation
  factor (1−r_u)(1−r_{2v−u})/(1−r_v)²; conditions (A)–(C); Phase-1 contraction y′ < 3y/4; Phase-2 packing count
  ⌈W/(s_θ/2)⌉; numerical constants θ = 0.918273, s_θ = 0.588143, λ_θ = 2.419118, 20.45 → 21, hence 22), Lemma 5.2′
  (Type-II contraction of z, count ⌈log_{4/3}((1+η)/η)⌉), Cor 5.3(b).
- L4 Theorem D walk of `v3_fit` → `v3_calibrate` → `v3_cal_tier` → `v3_final_run` (every `fail()` branch, the
  escalation `repeat`, the status rule at v3_calib.R:153, `v3_assemble_final` setting estimates at v3_run.R:166).
  (β) arithmetic: 2√c₀·2⁶⁰ = 7.4846·10¹⁷; Remark D.1 at n = 2.277·10⁸ gives ≈ 7.483·10¹⁷ (just below), and d's
  definition (v3_core.cpp:683: d = log BF − Σ_b log r_b, priors cancel) supports the crude bound.
- L2 S.2: Q = yᵀy − n zᵀH⁻¹z (v3_score.h:217-219) ≥ yᵀy/(n+1), yᵀy = n−1 after `v3_standardise`; q_nonneg identity.
- Corollary D′ pathwise claim; W1-PXN STATEMENT:52-53 explicitly says (T), (P) concern the data and the deterministic
  LS0 only, which supports "CAL not used".
- Inventory completeness: I grepped every `stop(`, `stopifnot`, `throw`, `Rcpp::stop` in the core (37 sites) and every
  returned `status`. All are listed, excluded by a declared premise, or off the `v3_fit` call graph, except one
  trivially-unreachable on-graph site (finding 3).
- Numerics claims: 220/236 (N-runs) and 146/146 (N4) constructions have N_b > 0; Remark 3.6 and Remark 5.4(0)
  numbers match N1/N3 outputs; "134 fits, no tier-0 trigger" matches SUMMARY_dlv (all `t0:` empty) and N4.

## Gate verdicts
- **G1 correctness — PASS.** Every step claimed as proved that I checked is correct (list above). No counterexample
  found. The code-audit parts (P1, L2 S.3, L1's per-loop caps) are correct to the extent checkable by reading; see
  finding 1 on their label.
- **G2 hypotheses used = stated — PASS.** EX-A, IDEAL-W, MACH, CONFIG, TDP-IMPL enter Lemma R / Cor R; EX-A Lemma S;
  GUARD-W the guard paths and D′; OP-LS0, e4, EX-S, SR only through the cited D′ inputs. CAL is genuinely not used
  (finding 4 asks for the citation that makes this checkable). IND-T correctly marked unused.
- **G3 no hidden assumptions — PASS (minor gaps).** Unit-cost exp/log in EX-A, exact-branch preflight bytes, and
  stack depth are implicit but harmless (finding 5).
- **G4 cited results: status and scope — PASS (minor).** W1-GEN (C1)+(C2), T03♯, W1-PXN (T),(P) used within scope;
  the LH-exact-Gram route inherits an instance-level status nuance not carried (finding 4). W1-N3 L7:20 cost bound
  cited correctly; the storage bound is honestly marked as a requirement.
- **G5 constants/rates — PASS.** Envelopes are explicit polynomial shapes with uninstantiated implementation
  constants, stated as such; preflight byte formula matches v3_fit.R:27-32 term by term; insertion bounds exact;
  (β) threshold and n_β recomputed. One display slip (finding 6).
- **G6 fidelity — PASS.** Calibration, escalation, `schedule_limit`, snapping, validation, pilot floor and the
  frozen-grid check match code and SoP/02_method.tex:303-354; spec-only components (LS0, e4 fallback, R′ = 4k,
  general-h, certificates, workers) are carried via CONFIG/TDP-IMPL and flagged; `start_mode` is confirmed off the
  production call graph (only defined, cpp/v3_start.h:183), consistent with INVENTORY G3.
- **Classification honesty — PASS.** (T) explicitly not claimed; C1/C2 conditional; F1 correctly a finding on a
  shipped component; the measured status in C1 is candid (two-model hypothesis fails at tested sizes; tier 1 never
  reached). **(O) is stated exactly:** under Theorem D and D′, (T) ⟺ P(𝒮ℒ_n) → 0 ⟺ P(E_n ∩ F¹_n) → 0, and (O-a),
  (O-b) are correctly labelled sufficient routes, with the forced-pilot caveat (k = T_e attainable, N2b) that blocks a
  naive unconditioned tier-1 argument.

## Score: 8.9 / 10 (uncapped)
Careful, correct, and honest PARTIAL result: the reduction of delivery to one explicit event is tight and verified
against code, the grid lemmas are sound with exact constants, and the open item is precisely the right one. Deductions
are for labelling code audits as proofs, a few documentation/citation precision gaps, and stale report text — none
affects a claimed conclusion.

## Findings (no FATAL, no MAJOR)

1. **MINOR — code-audit claims labelled "proved".** STATEMENT.md:50-56 lists P1 (inventory completeness) and P3's
   "remaining internal error sites are unreachable" under "proved"; L2_degenerate.md:206 itself concedes "This is a
   code-reading claim". Theorem D (P4) inherits both. *Fix:* label P1 and L2 S.3 "AUDITED (code reading; R01/R02/R05/
   R06)" in STATEMENT §3 and REPORT §3, and state in P4 that it holds relative to that audit. Attach the mechanical
   site list (all `stop`/`stopifnot`/`throw`/`Rcpp::stop`/status returns with on-graph/off-graph classification) as an
   appendix to INVENTORY so the completeness claim is checkable.

2. **MINOR — (P5)(a) failure rate is inferred, not measured.** STATEMENT.md:70 "(P5)(a) fails in almost all
   constructions": the dominance condition is not tabulated anywhere (dlv_constructions.csv has only `Lambda_V`); the
   claim is true by contrapositive of Prop 3.5(a) (it forces N_b = 0), and N_b > 0 in 220/236 and 146/146
   constructions. *Fix:* say "by Prop 3.5(a) ⇒ N_b = 0, (P5)(a) fails in every construction with N_b > 0 (220/236;
   N4 146/146); the remaining 16 were not tested for dominance".

3. **MINOR — one on-graph internal error site missing from X2.** `cpp/v3_core.cpp:546`
   (`cpp_build_grid`: "logg0_V and d_V must have equal length") is reached from `v3_build_grid` in every construction
   (v3_calib.R:6, :68) and is not in INVENTORY X2 or L2 S.3. It is unreachable (cpp_cal_V returns lg0 and d of equal
   length n, v3_core.cpp:679-683), so no conclusion changes. Similarly the seed re-checks `v3_check_seed` at
   v3_calib.R:137 and v3_run.R:173 are covered by A1's premise but not listed as sites. *Fix:* add them to X2 / A1
   with the one-line invariant.

4. **MINOR — citation precision for D′.** (a) L4_delivery.md:72 "CAL is not used": both cited theorems list CAL among
   their premises (W1-GEN STATEMENT.md:42-43; W1-PXN STATEMENT.md:45). The claim is right because only data/
   deterministic clauses are used; cite W1-PXN STATEMENT.md:52-53 ("(S), (E), (T), (P) concern the data and the
   deterministic LS0") and note W1-GEN (C1),(C2) are data-level, while the CAL-bearing step [M5-0] is replaced by
   C-DLV's own pathwise Claim. (b) L4_delivery.md:62-66 routes LH exact Gram through W1-GEN (C5)(a) and quotes the
   report-level status "PROVED-CHECKED"; the instance row (W1-GEN REPORT.md:64) records its input "W1-EXP Lemma 4.2 …
   SAME-FAMILY-ONLY". *Fix:* carry the instance-level status for LH exact Gram.

5. **MINOR — implicit cost-model details.** (a) EX-A as a cost model must include exp/log as unit-cost operations
   (ρ_V, LSE, pilot ESS are built from them; v3_calib.h:11-23, :49-58); say so in STATEMENT §1. (b) Corollary R
   (L1_resources.md:128-129) requires mem_n ≥ max{βM̄ + β₀, P₀, P₁} but P₀, P₁ are only displayed for the SMC sums;
   the exact-branch preflight bytes 8(3np + p²) + 8(40p + 1)(k* + 8) + 32p (v3_fit.R:23-24) are ≤ P₀ term by term —
   state it. (c) Recursion stack of the exact enumeration (depth ≤ K, v3_core.cpp:505-524) and of `start_mode`/TDP is
   not an M̄ term; it is O(p) words and covered by MACH's stack clause — one sentence suffices.

6. **MINOR (editorial) — stale or garbled text.** REPORT.md:74 "Council round 1: [to be filled]" although round 1 ran
   (LOG.md 22:52); REPORT §2 (C1) omits the E_n ∩ factor present in STATEMENT (equivalent, but align). STATEMENT.md:1
   still reads "v2, locked after R01" while carrying post-council edits (Opus C1 #1, #2) — bump the version and log
   it. L1_resources.md:136 "P̄_t = O(N₀p(n³ + pn + n m_t²)/1)" — drop "/1". L3_grid.md:78 "already at n ≥ 1600 the
   start mode differs from S₀ (masked design M …)" — for M it already differs at n = 400 (N1_psi_M.txt); reword.

## Not findings (checked and survive)
- Lemma 3.4(b)'s N_p′ ≤ k with a snapped final point; Lemma 5.2's terminal-trial "+1"; Cor 5.3(c)'s (γ)
  counterexample band; Prop F's fallback grid passes `v3_check_grid` (v3_run.R:77-82), is frozen before stream 10,
  and changes the law only on the shipped no-output event; Corollary R's guard bound (elapsed + operation ≤
  2(τW̄ + τ₀), v3_runtime.h:21-27); D2 unreachability; final-run statuses (v3_core.cpp:388-480) limited to completed /
  resource_limit / numerical_failure; Remark D.1's bound on d.
