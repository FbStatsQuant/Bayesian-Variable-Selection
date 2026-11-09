# R02 — Lemma-by-lemma cross-family review of W2-FAC-PKA (L0, L1) + numerics

Reviewer: Claude Opus 5.5 (fresh seat, continuous lemma review; not mid-point, not council). Brief: break the proofs.
Read: Wave2 / Wave1C / Wave1 PROTOCOL.md; PKA STATEMENT.md (v2), PLAN.md, METHOD_REQUIREMENTS.md, lemmas/L0_rank.md,
lemmas/L1_saturation.md, numerics/n1_exact_grid.py, N1_exact_grid.jsonl, n2_checks.py, N2_checks.json;
reviews/R01_statement_lock_claude.md and R01_disposition.md (only to check the required statement fixes).
Source checked directly: FINAL `s7_impl.tex:33-61` (Lemma CAP), `Scripts/SMC_BVS/core/cpp/v3_engine.h:370-418`
(local_search loop), `cpp/v3_core.cpp:456-479` (final search line 456, then LS0, cap `ls0_ell + |m.S|` line 473),
`v3_preprocess.R:19-45` (K, B, ℓ, standardisation with SD (n−1)), SoP `04_theory.tex:68-74` (D0, score, prior,
start, G), W2-FAC-B `numerics/cs_core.py`, `fac_core.py`, `bvs_core.py` (ell_cap, block_size).
Not read: PKA LOG.md, REPORT.md, CHECKPOINT.md, numerics/SIM_REQUEST.md (appeared during the review), anything of
W2-FAC-PK. No git changes; writes only this file and `reviews/R02_scratch/`. All Python run with
`python.exe -B` and `PYTHONPYCACHEPREFIX=reviews/R02_scratch/pyc_none` (no bytecode read or written elsewhere;
`pyc_none` is empty after the runs).

## Verdicts

| Item | Verdict |
|---|---|
| Statement v2 vs R01 fixes | **R01 fixes applied** (S1–S9, P1–P3), with 3 minor wording items (W1–W3 below); none blocks |
| CAP discovery criterion in STATEMENT v2 | **CORRECT** — union of neighbourhoods matches CAP (a) verbatim; "arrival in d ≤ a+1" is correctly sufficient only |
| **L0** (realizability frontier, T0) | **VERIFIED** (no required changes; two optional cosmetic items) |
| **L1** (size saturation, T1a) | **VERIFIED** — proof correct line by line as stated; required fixes are to the *falsification evidence*, not to the proof (F1–F4) plus two minor proof-text items (L1-a, L1-b) |
| Numerical falsification adequacy | L0: **adequate**. L1: **INADEQUATE as filed** (does not test the conclusion; random not adversarial; dense controls never hit the saturated regime). My scratch closes the gap for the tested parameters (see "Reviewer numerics"); the lead must add equivalent evidence to `numerics/` before L1 is used downstream |
| Adapted CS path vs fac_core | **CORRECT where it runs** (216/216 matches incl. 46 size-K starts, 430 swaps); **crashes when the path reaches the empty model** (24 cases) — fix required (F2) |

Status recommendation (verbatim protocol words): L0 and L1 may be recorded as "PROVED (by this seat), lemma check
R02 VERIFIED"; L1 should not be used downstream until F1–F3 are in `numerics/` with outputs. Neither is PROVED-CHECKED.

## 1. Statement fixes (R01) — status

- S1 targets T0–T5 with alternatives: present. T2's criterion is now CAP's union of neighbourhoods, not R01's
  "iff arrival" (R01 was wrong there; the disposition is right). T3 says OP alone is inconclusive on T2-negative;
  nothing claims D_n ↛ 0. ✓
- S2 standalone G, D0, method, P′; FAC-B L3 E2 / L4.0(d) explicitly not inherited; r ≡ 0 at p = n−1 noted. ✓
  D0 citation `04_theory.tex:70-73` checked: line 70 D0, 71 Score, 72 Prior, 73 Start/bridge. ✓
- S3 primary p/n → c ∈ (1/2,1); boundary layers p−K = O(1), n−1−p = o(n) separated; saturation is T1a, proved, not
  presupposed. ✓
- S4 no truth inclusion; refinements separately reviewed; T2 needs truth-in swap bounds. ✓
- S5 no uniqueness / sign symmetry / bulk-centre inheritance. ✓
- S6 uniform over deterministic partitions with blocks ≤ B; exact-CS linkage ties covered. ✓
- S7 rank sentence corrected; iid population CS is a chosen model; p/n fixed > 1 vs → ∞ distinct. ✓
- S8 SMC/final-search discovery is a separate target needing its own bound; T5 = evidence + missing-input list. ✓
- S9 H0 via λ_min ≥ (n−1)(1−ρ), A = 1; score charge 1+(a+1)·max_{k≤K}[p+k(p−k)] (correct upper bound: ≤ p flips,
  k(p−k) swaps per scan, a+1 scans, plus the centre); preflight / archive / Prop. F envelopes flagged. ✓
- P1–P3: in the PLAN supplement. ✓ (P3's "truth-in swaps separately counted" is not yet implementable with the
  current tags: see F5.)

Wording items (minor, not blocking):
- **W1** "lexicographic neighbor ties" is ambiguous. The code (`v3_engine.h:392`) breaks exact F ties by the
  lexicographic order of the resulting model's sorted (internal) index vector, proper prefix first — not scan order.
  Say so.
- **W2** "Column signs can be absorbed": state that θ̄ is computed in the sign frame in which the Gram is exactly CS
  with ρ > 0 (unique up to a global flip, which leaves θ̄ ≠ 0 invariant); the method is invariant under column
  sign flips (score depends on z_Uᵀ H_U⁻¹ z_U and |r̂|).
- **W3** G should cite SoP G (`04_theory.tex:74`: y^r = α1 + X^rβ + ε, standardise afterwards) and record the
  one-line reduction: with raw X already centred with column norm² n−1, standardisation returns X
  (`v3_standardise`: ÷max, centre, ÷SD with n−1 — scale invariant), and centring y^r gives Y = Xθ + Cε, y = Y/s.
- The arrival identity "if the path starts containing truth" — the qualifier is unnecessary (d = |start|−s0+2A+W is
  a counting identity for any start); harmless.

## 2. CAP and the discovery criterion (inspected directly)

CAP (a) (`s7_impl.tex:47-48`): LS0 with cap a makes min(a, m*) moves, scans exactly C_0..C_{min(a,m*)}, scored set
{C_0} ∪ ⋃_{k ≤ min(a,m*)} N(C_k). Code: `v3_engine.h:379-418` — the scan completes before the cap test (line 409)
`if (A.moves >= ell)`, which returns the best neighbour with `local_limit`; additions excluded at |C| ≥ K (line 397); swaps
always scanned. STATEMENT v2's "S0 is the initial centre or a feasible neighbor of C_t for some t ≤ min(a, m*)" is
exactly CAP (a). Arrival at C_d = S0 with 1 ≤ d ≤ a+1 gives S0 ∈ N(C_{d−1}), d−1 ≤ min(a, m*−1): sufficient. Not
necessary: S0 can be scanned (in N(C_t)) without being selected. R01's "iff" was wrong; v2 is right.
Counting: deletions = |start| + A − s0, so d = |start| − s0 + 2A + W; with A = 0, d ≤ a+1 ⟺ W ≤ ℓ + s0 + 1. ✓
`n1_exact_grid.py` implements the union criterion correctly (flip/swap neighbour test at every t ≤ m*, compared
with cap ≤ a, using the uncapped path = prefix property).

## 3. L0 — VERIFIED

Line by line:
- Necessity: 1ᵀX = 0 ⇒ col(X) ⊆ 1^⊥, rank XᵀX ≤ n−1; Σ = (1−ρ)I + ρ11ᵀ has eigenvalues 1−ρ (×(p−1)) and
  1+(p−1)ρ, all > 0 for ρ ∈ (0,1), so rank p ⇒ p ≤ n−1. ✓
- Sufficiency: Q n×p orthonormal in 1^⊥ (dim n−1 ≥ p), R = Σ^{1/2}, X = √(n−1) Q R: 1ᵀX = 0, XᵀX = (n−1)RQᵀQR =
  (n−1)Σ, column norms² n−1 ⇒ SD 1, nonconstant; standardisation of raw X = X returns X (scale-invariant steps). ✓
- Consequences: no p ≥ n sequence has this Gram; nothing else is concluded. K < p ≤ n−1 nonempty iff ⌊n/2⌋ < n−1,
  i.e. n ≥ 3 — this is what n ≥ 3 is for (the iff itself does not need it). ✓
Hidden hypotheses: none. Optional: (i) say n ≥ 3 is only for the nonempty-range remark; (ii) in N2 the fields
`impossible_p16_target_rank` / `centered_rank_bound` are hard-coded constants, not computed — drop or compute.
Falsification: N2 `rank` (n=16, p=15 construction, errors 7e-15 / 9e-15) — adequate for an algebraic fact.

## 4. L1 — VERIFIED (proof); evidence needs F1–F4

Line-by-line check (h = n−1):
1. q_j − (Σθ)_j = x_jᵀε/h (X centred, so XᵀC = Xᵀ) ~ N(0, σ²/h); union bound over p ≤ n: max = O_P(√(log n/n)). ✓
2. v̂ − v = O_P(n^{-1/2}): ‖Xθ‖² = hθᵀΣθ; εᵀCε ~ σ²χ²_{h}; cross-term variance 4σ²hθᵀΣθ. No use of n−1−p. ✓
3. Uniformity over all |U| ≤ 16 is deterministic given the max-coordinate event: ‖e_U‖ ≤ 4 max|e_j|,
   ‖Σ_U⁻¹‖ ≤ 1/(1−ρ), ‖(Σθ)_U‖ ≤ 4((1−ρ)max|θ| + ρ|θ̄|). So R̂_U = R_U + O_P(√(log n/n)) over ~p^16 sets with no
   further union bound. ✓ RSS_U(Y)/h = v̂ − q_UᵀΣ_U⁻¹q_U exactly (X_UᵀX_U = hΣ_U). ✓
4. σ² ≤ R_U ≤ v (R_U = v − bᵀΣ_U⁻¹b, bᵀΣ_U⁻¹b ≤ θᵀΣθ). ✓
5. c_u: Cov(x_l, xᵀθ) = ρθ̄ for null l; Σ_U⁻¹1 = 1/(1+(u−1)ρ)·1, so c_u = ρθ̄[1 − uρ/(1+(u−1)ρ)] =
   ρθ̄(1−ρ)/(1+(u−1)ρ); u = 0 gives ρθ̄. t_u = 1 − ρ²u/(1+(u−1)ρ) = (1−ρ)(1+uρ)/(1+(u−1)ρ) > 0. R_U − R_{U+l} =
   c_u²/t_u is the Schur-complement identity (algebraic, no population sampling needed). R_U/R_{U+l} =
   1 + δ/(R_U−δ) ≥ 1 + δ_min/v. ✓ δ_min > 0 needs θ̄ ≠ 0 and u ≤ 15 (block size ≤ 16; code B ≤ 16). ✓
6. Transfer: ‖G_U⁻¹ − nH_U⁻¹‖ = max_g (g+1)/(g((n+1)g+1)) = O(n⁻²) for g ≥ h(1−ρ); ‖z_U‖ ≤ 4h max|q_j|/s = O_P(n)
   with s² = v̂ ≥ σ²/2 w.p. → 1; hence Q_U = RSS_U(y) + O_P(1) = hR̂_U/v̂ + O_P(1) uniformly; ratio of
   (.02+Q) converges uniformly (both terms ≍ n, denominators ≥ hσ²/(2v̂)). ✓
7. log det H_U − log det(G_U+I) = Σ_i log((n+1) − n/(g_i+1)) = u log(n+1) + O(1/n): increment log n + O(1). ✓
8. Block increment ≥ (n/2)log(1+δ_min/(2v)) − ½log n − O(1); prior increment log((k+1)/(2p−1−k)) ≥ −log(2p) for
   0 ≤ k < K. The block factor r_b(U) = m(U)/m(∅) changes only in l's block. ✓
9. Maximizer: truth blocks ≤ s0, ≤ 16s0 variables; truth-free variables ≥ p−16s0 ≥ K > |S|, so some truth-free l ∉ S;
   U = S ∩ C_b has ≤ 15 elements, truth-free; the strict improvement applies; S is not a maximizer. Holds for every
   maximizer and every partition with blocks ≤ 16 simultaneously, for any exact maximizer (e4′ premise). ✓
No counterexample, uniformity or score error found. Hidden hypotheses: none beyond G (σ > 0 fixed is used in 4 and 6;
θ̄ ≠ 0 in 5; blocks ≤ 16 in 5 and 9; p ≤ n−1 only for existence of the design).

Minor proof-text items:
- **L1-a** Step 6 should state the lower bound on s² (v̂ ≥ σ²/2 w.p. → 1) explicitly; it is used for ‖z_U‖ = O_P(n)
  and for the denominators.
- **L1-b** The worst-case prior bound −log(2p) is what makes the result robust; note in one sentence that near
  k ≈ K the actual increment is log(K/(2p−K)) = O(1), so the onset is governed by (n/2)log(1+δ_min/v) vs ½log n
  (useful for the numerics F1 and for T1b).
- Optional: condition p − 16s0 ≥ K can be written p − B·s0 ≥ K (B = block-size bound); identical asymptotically.

## 5. Numerics — adequacy and required fixes

**F1 (required, L1): the filed falsification does not test L1's conclusion.**
- N2 `increment_samples` draws 20 random U per u (320 pairs) — the claim is a minimum over all U ⊆ truth-free blocks
  and all l; random sampling does not probe the noise-selected adversarial U. Its statistic is negative in 13/18 rows
  (all n ≤ 2000 and n=20000, p=17000, seed 0: −1.84), i.e. at the tested n the uniform event does not yet hold,
  which is consistent with the asymptotic claim but is not evidence for it. No predicted values are saved.
  (My check: observed minima track (n/2)log(1+δ_15/v) − ½log n roughly — e.g. n=2·10⁴, p=10200, seed 0, θ = 2e₁, ρ = .5, σ = 1:
  predicted ≈ 9.8, observed min block increment ≈ 10.4 — but this is not in the file.)
- N1 is not an L1 test: in most rows p − 16s0 < K or the start is unsaturated (start 57–400 vs K = 100–400; K is not
  even printed), so N1 is pre-asymptotic for T1a.
- Required: add a direct start-mode saturation test at n where the bound predicts onset, as in my scratch below
  (closed-form 2^b block tables + size-capped knapsack + w(k)), reporting |start| vs K, the margin
  log γ0(best size K) − max_{k<K} log γ0, and the predicted onset; include a small θ̄ case and p = n−1.

**F2 (required, adapter): crash at the empty model.** `run_path` (inherited from `cs_core.ls0_path_cs`) builds
`isN_in = np.array([j not in S0 for j in idx_in])`; when the path reaches |T| = 0 this is an empty float array and
`~isN_in` raises TypeError. Reproduced 24 times in my 216-case control (every case whose dense final is ()). Not
triggered in N1/N2 as filed, but any small-signal, boundary, or truth-excluded run can hit it. Fix: `dtype=bool`.

**F3 (required, adapter): unchecked source patching and unsaturated dense controls.** `str.replace` silently does
nothing if a target string changes; assert each target occurs exactly once in `inspect.getsource(cs.ls0_path_cs)`
(I did; all three targets are present once). N2's dense controls (n=30, p=22, starts of size 4–6 < K=15) never
exercise the additions-blocked-at-K branch — the regime of the ticket. Add saturated starts. My scratch did: 4
designs (n,p,ρ) ∈ {(30,22,.5),(24,20,.3),(40,39,.7),(31,29,.5)}, 20 seeds, starts of size K, K−1 and random,
half forced to contain truth: 216 cases, 0 mismatches against `fac_core.ls0_path` (final set, move count and
F after every move to 1e-7), 46 size-K starts, 430 swaps, 0 exact ties (plus the 24 crashes of F2). The swap shortcut
(only extreme z_l per outgoing j) is valid: the swap quad is (1−γ_k)z_l² + linear with γ_k < 1/k ≤ 1, convex in
z_l, and F is increasing in quad; equal-z ties are null events.

**F4 (required, provenance):** N1 should record K, the partition actually used (bc.partition_from_corr under exact
CS ties is a floating-point tie convention — fine because L1 is uniform, but record it), and ℓ. N1/N2 must cite
these scripts as falsification for L1 only after F1.

**F5 (T2 bookkeeping, not L0/L1):** tags `sT`/`-T` lump truth-out and truth-in moves (tag "T" if either index ∈ S0);
P3 requires truth-in swaps separately. Split into in/out tags.

Observation for T2 (finite diagnostics only, no verdict): in N1 the null-swap count grows with n (3–8 at n=200,
6–13 at 400, 9–30 at 800) against slack ℓ + s0 + 1 = 16 at n=800, and both n=800, p/n=.85 rows already miss under
cap ℓ+|start| (first scoring scan 420/425 > cap 406/411). Per the STATEMENT, this is not an asymptotic counterexample.

## Reviewer numerics (scratch, `reviews/R02_scratch/`)

- `adapter_check.py` — F2/F3 results above.
- `start_dp.py` → `start_dp_out.json` — independent closed-form exact-CS data (FAC-B L1 reduction, re-derived:
  XᵀCε = σ√h g, ‖Cε‖² = σ²(gᵀΣ⁻¹g + χ²_{n−1−p})), full 2^b enumeration per contiguous block of b = 16, size-capped
  knapsack, prior w(k); ρ = .5, σ = 1, 2 seeds per row:
  - Cross-validation: n=800, p=680, N1 coefficients: start sizes 395 and 400 — identical to N1's `start` column.
  - θ = .5(1.4, 1, 1.8, 1.2) at 2,26,53,75 (θ̄ = 2.7), n=2·10⁴: p=17000 and p=10200 (p/n=.51): saturated (|start| =
    K = 10⁴), margins 131/131 and 42/42.
  - θ = 2e₁ (θ̄ = 2), n=2·10⁴, p=17000 and p = n−1 = 19999: saturated, margins 47/47 and 62/62.
  - θ = .5(1.4, −1, 1.8, −1.2) (θ̄ = .5), n=2·10⁴, p=17000: **not** saturated (8385, 8527; margins −1700, −1330):
    finite-n onset scales like θ̄⁻², not a counterexample.
  - n=10⁵ rows: see the addendum at the end of this file.
  So L1's conclusion is confirmed at feasible n for θ̄ ∈ {2, 2.7} including p/n = .51 and p = n−1; this is the
  evidence F1 asks the lead to reproduce in `numerics/`.

## Exhaustive issue list

| # | Item | Severity | Required? |
|---|---|---|---|
| F1 | L1 falsification does not test the conclusion; add large-n start-DP saturation test | major (evidence) | yes, before downstream use |
| F2 | Adapter crashes at empty model (`~` on empty float array) | moderate | yes |
| F3 | Assert patch targets; add saturated-start dense controls | moderate | yes |
| F4 | N1 provenance: record K, partition, ℓ | minor | yes |
| F5 | Split truth-in / truth-out move tags (T2) | minor | yes for T2 |
| L1-a | State s² ≥ σ²/2 lower bound in transfer step | minor | yes |
| L1-b | Note O(1) prior increment near K / onset scale | minor | recommended |
| W1 | Tie rule wording: lexicographic resulting model, proper prefix first | minor | yes |
| W2 | θ̄ frame under column signs | minor | yes |
| W3 | Cite SoP G and the raw→standardised reduction | minor | yes |
| L0-opt | n ≥ 3 role; hard-coded N2 rank fields | cosmetic | no |

## Addendum — n = 10⁵ rows of `R02_scratch/start_dp.py` (output `R02_scratch/start_dp_out.json`)

p = 85000 (p/n = .85), K = 50000, contiguous blocks of 16, ρ = .5, σ = 1, seeds 0/1:
- θ̄ = .5 (θ = .5(1.4, −1, 1.8, −1.2)): **saturated** in both seeds (|start| = K), margins 18.3 / 18.6 — the case
  that was unsaturated at n = 2·10⁴ crosses the onset between 2·10⁴ and 10⁵, as the θ̄⁻² onset scaling predicts.
- θ̄ = 2.7: saturated, margins 696.9 / 698.9 (≈ 5.3× the n = 2·10⁴ margins of 131, i.e. linear growth in n).
All 10 large-n rows (n ∈ {2·10⁴, 10⁵}) with θ̄ ∈ {2, 2.7}, and both n = 10⁵ rows with θ̄ = .5, are saturated;
margins grow linearly in n. No falsification of L1 found. `pyc_none` is empty (no bytecode written).
