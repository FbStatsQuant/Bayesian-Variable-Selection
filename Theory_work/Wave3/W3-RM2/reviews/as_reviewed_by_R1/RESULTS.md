# W3-RM2 numerics — RESULTS (sharpness gate; boundary-violation probes)

**Observations only, never proofs.** All theorems are asymptotic; these counts say nothing about a limit. Design,
objects, validation and column definitions: `SPEC.md`. Local machine, no NOTS. 207 runs, 0 failed
(n = 400: 130 runs, 10 seeds per cell; n = 1600: 77 of 78 runs, 6 seeds per cell — one run of the cell
B4/η = 1 was still running when this file was frozen; the n = 3200 layer had not started). p = 2n throughout.
"Conclusion held" = **LS0 from the start mode ends at S₀ with a completed scan finding no strict improvement**
(shipped cap ℓ_n + |S̃₀|). The sampler and the posterior input [POST] are not probed. The classification of each cell
(inside/outside an assumption) is **nominal** (population design); the fixed-design conditions were not certified
on the realised X.

## 1. Cell summaries (from `summary.csv`)

`start` = start-mode size, median [min, max]; `out` = outside columns (not in Q) in the start mode, mean [min, max];
`sand` = S₀ ⊆ S̃₀ ⊆ Q; `end S₀` = conclusion held; `all del` = every move deletes an extra; `other` = total number of
moves that are not deletions of an extra; `path NA` = no path-level no-addition margin is positive at any visited
lattice centre; `probe` = runs in which the adversarial probe found a true violation of NA(𝓛) at a lattice set;
`old cap` = the path would also end at S₀ within the old cap ℓ_n.

| id | b (η) | n | m = ⌈n^b⌉ | √n | start | out | sand | end S₀ | all del | other | path NA | probe | old cap |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B1 | 0.25 | 400 | 5 | 20 | 2 [2,4] | 0 | 10/10 | 10/10 | 10/10 | 0 | 10/10 | 1/10 | 10/10 |
| B1 | 0.375 | 400 | 10 | 20 | 3 [2,7] | 0 | 10/10 | 10/10 | 10/10 | 0 | 10/10 | 1/10 | 10/10 |
| B1 | 0.5 | 400 | 20 | 20 | 10 [7,11] | 0 | 10/10 | 10/10 | 10/10 | 0 | 10/10 | 3/10 | 10/10 |
| B1 | 0.625 | 400 | 43 | 20 | 22 [18,26] | 0 | 10/10 | 10/10 | 8/10 | 2 | 7/10 | 6/10 | 0/10 |
| B1 | 0.75 | 400 | 90 | 20 | 50 [47,55] | 0.2 [0,1] | 8/10 | 10/10 | 4/10 | 8 | 3/10 | 9/10 | 0/10 |
| B1 | 0.25 | 1600 | 7 | 40 | 7 [6,8] | 0 | 6/6 | 6/6 | 6/6 | 0 | 6/6 | 0/6 | 6/6 |
| B1 | 0.375 | 1600 | 16 | 40 | 14 [9,15] | 0 | 6/6 | 6/6 | 6/6 | 0 | 6/6 | 0/6 | 6/6 |
| B1 | 0.5 | 1600 | 40 | 40 | 32 [27,34] | 0 | 6/6 | 6/6 | 5/6 | 1 | 5/6 | 1/6 | 0/6 |
| B1 | 0.625 | 1600 | 101 | 40 | 89 [88,94] | 0.5 [0,1] | 3/6 | 6/6 | 3/6 | 3 | 5/6 | 3/6 | 0/6 |
| B1 | 0.75 | 1600 | 253 | 40 | 239 [236,241] | 0.3 [0,1] | 4/6 | 6/6 | 1/6 | 12 | 2/6 | 5/6 | 0/6 |
| B2 | 0.25 | 400 | 5 | 20 | 2 [2,4] | 0 | 10/10 | 10/10 | 10/10 | 0 | 10/10 | 2/10 | 10/10 |
| B2 | 0.375 | 400 | 10 | 20 | 2 [2,2] | 0 | 10/10 | 10/10 | 10/10 | 0 | 10/10 | 6/10 | 10/10 |
| B2 | 0.5 | 400 | 20 | 20 | 9 [8,11] | 0.4 [0,2] | 7/10 | 10/10 | 10/10 | 0 | 10/10 | 8/10 | 10/10 |
| B2 | 0.25 | 1600 | 7 | 40 | 3 [2,6] | 0.2 [0,1] | 5/6 | 6/6 | 6/6 | 0 | 6/6 | 1/6 | 6/6 |
| B2 | 0.375 | 1600 | 16 | 40 | 7 [4,9] | 0.3 [0,1] | 4/6 | 6/6 | 6/6 | 0 | 6/6 | 3/6 | 6/6 |
| B2 | 0.5 | 1600 | 40 | 40 | 30 [27,33] | 0.5 [0,1] | 3/6 | 6/6 | 5/6 | 1 | 6/6 | **6/6** | 0/6 |
| B3 | 0.5 | 400 | 20 | 20 | 8 [6,10] | 0 | 0/10 | 10/10 | 0/10 | 10 | 9/10 | 3/10 | 10/10 |
| B3 | 0.625 | 400 | 43 | 20 | 22 [20,28] | 0.1 [0,1] | 0/10 | 10/10 | 0/10 | 13 | 6/10 | 6/10 | 0/10 |
| B3 | 0.5 | 1600 | 40 | 40 | 31 [29,35] | 0 | 0/6 | 6/6 | 0/6 | 7 | 5/6 | 1/6 | 0/6 |
| B3 | 0.625 | 1600 | 101 | 40 | 90 [88,98] | 0.3 [0,1] | 0/6 | 6/6 | 0/6 | 8 | 4/6 | 3/6 | 0/6 |
| B4 | 0.375 (η = 0.05) | 400 | 10 | 20 | 3 [2,8] | 0.1 [0,1] | 9/10 | 10/10 | 10/10 | 0 | 10/10 | 1/10 | 10/10 |
| B4 | 0.375 (η = 0.05) | 1600 | 16 | 40 | 14 [12,15] | 0.3 [0,1] | 4/6 | 6/6 | 6/6 | 0 | 6/6 | 0/6 | 6/6 |
| B4 | 0.375 (η = 0.2) | 400 | 10 | 20 | 5 [2,10] | 0.9 [0,3] | 5/10 | 10/10 | 10/10 | 0 | 10/10 | 1/10 | 10/10 |
| B4 | 0.375 (η = 0.2) | 1600 | 16 | 40 | 19 [17,23] | 4.0 [2,6] | 0/6 | 6/6 | 6/6 | 0 | 6/6 | 0/6 | 0/6 |
| B4 | 0.375 (η = 1) | 400 | 10 | 20 | 107 [72,126] | 97 [66,119] | 0/10 | 10/10 | 1/10 | 24 | 10/10 | 1/10 | 0/10 |
| B4 | 0.375 (η = 1) | 1600 | 16 | 40 | 615 [522,634] | 586 [505,617] | 0/5 | **2/5** | 0/5 | 96 | 5/5 | 0/5 | 0/5 |

Overall: the conclusion held in **204 of 207** runs. The three failures are all in the cell B4, η = 1, n = 1600.

## 2. Readings

**B1 — size of the leak set (b < ½ in the statement).** Inside (b ≤ 0.375): sandwich, path-level no-addition and
deletion-only descent in every run (32/32). At and above b = ½ (start modes of 27–34 columns at √n = 40; up to 241
at b = 0.75): the three ingredients of the route start to fail — an outside pure-noise column in the start mode
(sandwich fails in 3/6 and 2/6 runs at b = 0.625, 0.75, n = 1600); a positive no-addition margin at a visited lattice
centre (1/6, 1/6, 4/6 runs at b = 0.5, 0.625, 0.75, n = 1600; 0, 3, 7 of 10 at n = 400); moves that are not deletions
(swaps of an extra for an outside column, which is deleted later) — yet LS0 ended at S₀ in 18/18 runs with b ≥ 0.5 at
n = 1600 and 30/30 at n = 400. The number of non-deletion moves per run was at most 1, 1, 4 (b = 0.5, 0.625, 0.75,
n = 1600); the cap leaves ℓ_n + s₀ = 15 spare moves. Flag: **`improvable`** — the conclusion survives above b = ½ at
these sizes although the route's events do not; the margin that protects it is the cap slack, and the number of
non-deletion moves grows with b. The old cap ℓ_n fails as soon as the start mode has more than ℓ_n extras (0/6 from
b = 0.5 at n = 1600).

**B2 — lattice width (W).** The adversarial probe finds a true violation of NA(𝓛) (an addition that strictly
improves F at a lattice set) in 6/6 runs at b = 0.5, n = 1600 (median margin +5.7), 8/10 at n = 400, and in 3/6 and
6/10 runs already at b = 0.375 — against 1/6 and 3/10 in the matching B1 cells: the common-direction loading makes
the whole-lattice event fail, as the width heuristic predicts. Along the actual LS0 path no margin was positive at a lattice centre
(48/48 runs) and LS0 ended at S₀ in 48/48 runs, by deletions only in 47. Flag: **`improvable`** for the conclusion
(whole-lattice no-addition is observed to fail while the greedy path is unaffected) — consistent with (W) being a
condition of the route (Lemma W-conv), not of the conclusion.

**B3 — a weak truth.** The weak truth (nθ₂² = 12 log n) is missing from the start mode in 32/32 runs; LS0 brings
it in by a swap or an addition and ends at S₀ in 32/32. This probes visibility at finite n together with (BM-Q);
the two cannot be separated at these sizes (a truth strong enough to enter the start mode has nθ² of several
hundred, above |Q| for every b ≤ ½ here). Flag: `improvable` for (V) (as in W3-RM); **no information on (BM-Q)**.

**B4 — leak level outside Q.** All three levels are nominally beyond the frontier β(η, A) = b. η = 0.05 and 0.2:
outside columns enter the start mode (sandwich fails in 2/6 and 6/6 runs at n = 1600; mean 0.3 and 4.0 outside
columns) and LS0 deletes them: conclusion in 32/32 runs — `improvable` near the frontier. **η = 1: the conclusion
fails.** At n = 1600 the start mode has 522–634 columns, 505–617 of them outside Q; LS0 makes 6–35 swaps of an extra
for an outside column on top of the deletions; the cap allows only ℓ_n + s₀ = 15 moves beyond the deletions, and in
**3 of 5 runs LS0 stops at the move cap** (`local_limit`) at a model of 6–22 columns, not at S₀ (runs with 19, 24, 35
swaps; the two successes had 6 and 12, one of them with 3 moves to spare). At n = 400 the same cell succeeds in
10/10 runs (at most 6 swaps; slack 13). This is the mechanism of W2-FAC-PK's Theorem NEG (a long swap phase against
a cap with additive slack) appearing in a weak-leak design. Reading: **the leak condition is not only a proof
device** — far outside it the coded LS0 fails under the shipped cap — but the failure is a cap event (the path was
still improving), not a wrong local optimum; nothing here is known about the full method (sampler + final search).

## 3. What the numerics do not show
* No fixed-design condition was certified on a realised design; no asymptotic statement is supported or refuted.
* p = 2n only; s₀ = 2; one leak mechanism (weak proxies of one truth); Gaussian rows.
* The probe tries 14 of the 2^m lattice sets, so "probe found no violation" is not "NA(𝓛) held".
* The start mode and LS0 are re-implementations validated against production scores and start masses (`SPEC.md`),
  not the production routines themselves; ties are broken by first maximum. [SW1-3] The LS0 re-implementation
  departs from production in three boundary branches (improvement tolerance 1e-9; the current centre is returned
  at the cap, so `final_size` of a capped probe is the current centre's size; first-maximum ties) — `SPEC.md`. The
  four capped probes stopped at centres far from S₀ (sizes well above s₀ = 2), so one more production move could
  not have reached S₀.
* [SW1-2] B2 is a nominal width-stress design: (W) is not certified to fail on the realised designs, and its
  leak is small but not exactly zero (`SPEC.md`). "NA violated" means an improving addition was found at a probed
  lattice set.

## 4. Addendum after the better-theorem round (2026-11-11; not seen by review BT1)

Sections 1–3 above are the text frozen for the better-theorem review (207 runs). Afterwards:
* **The 78th run of the n = 1600 layer** (B4, η = 1, seed 1) finished: start mode 743 columns (727 outside Q), 73
  swaps, LS0 stopped at the move cap (756 moves) at a model of 60 columns, not S₀. The cell B4/η = 1/n = 1600 therefore
  reads **2 of 6** (not 2/5), with start sizes 522–743 and 6, 12 (successes), 19, 24, 35, 73 (failures) swaps; the
  overall count is **204 of 208**. `results_raw.csv` and `summary.csv` now contain all 208 runs.
* The n = 3200 layer was started and stopped before any run finished (too slow locally): **not run**.
* Scope reminder: every count in this file concerns the validated LS0 re-implementation started from the start
  mode. The sampler, the posterior input and the full method's reported model were not tested.

## 5. Lemma checks (falsification numerics for `lemmas/L0–L2`; `lemma_checks.R` → `lemma_checks_out.txt`; `check_identity.R` → `check_identity_out.txt`)

Each block tries to break one deterministic step of a proof, or illustrates a probabilistic statement at small n.
No violation was found.

| id | lemma step | test | outcome |
|---|---|---|---|
| K1 | L0 (T3): score remainder R_A ∈ [−0.52/c_E, \|A\|/((n − 1)φ₀²)] | exact D0 score for random sets of size up to 400 (n = 1600) | holds in 120/120; R_A ∈ [−7.9, −0.01] while κ_E ≈ 77 (the constant is very conservative) |
| K2 | L0 (E6-tab) on **production** block tables; L1 Fact 2 | 1428 nested pairs in 25 production blocks | remainder difference in [−0.28, 0.01] (allowed ±140); min RSS_U/((n − 1)τ²_U) = 0.94 at n = 400 |
| K3 | L2 NA-conv and W-conv: the score increment of an addition at a lattice set equals (Z² − a⁰(k)²)/2 up to the proved constants | 9600 lattice pairs, set sizes up to 255, n = 1600, p = 3200, exact score | D := [F(T + l) − F(T)] − (Z² − a⁰²)/2 ∈ [−0.69, 0.34]; 0 pairs outside the proved bounds; 0 pairs with Z² ≤ c_n(k) and no decrease of F |
| K4 | L2 (3.1): (u_{T,l}ᵀg)² ≤ (u_{Q_l,l}ᵀg)² + ‖(P_Q − P_{S₀})g‖² | 8704 directions of an enumerated lattice × 200 draws | max(lhs − rhs) = −0.76 ≤ 0 |
| K5 | L2 §3(v): decomposition of u_{T,l} into a local reference and ℓ¹ atoms; variance ratio | 300 random (T, l, N_l) | reconstruction error 8e-16; variance-ratio bound holds |
| K6 | L2 NA-W / W-conv, illustration at n = 240 | Monte Carlo width gap for three designs (orthogonal, iid, common-direction) | gaps −0.44, −0.39, +0.07; frequency of a level crossing 0.14, 0.18, 0.53 — ordered as the lemmas say; at this n all gaps are of order 1, so nothing asymptotic is tested |
| K7 | L2 Lemma d: d_n ≤ √(q + 1) + √(2 log p) | 1080 truth-removal directions (deletions and swaps) | MC lower estimate 1.71 ≤ bound 6.03 |
| — | L2 (4.1): the two-square identity for truth removal | 400 comparisons, correlated columns, signed coefficients | max relative error 1.2e-14 |

Reading of K3: the lower end −0.69 ≈ −log 2 is the exact prior ratio (k + 1)/(2p − 1 − k) ≈ (k + 1)/(2p) against the
level a⁰ defined with p; the remainders themselves are a fraction of a unit. So the level at which an addition
starts to pay is a⁰_n(k) up to an additive O(1/√log n), as Lemmas NA-W and W-conv state.

## 6. Form R and examples: lemma checks for `lemmas/L4–L6` (`formR_checks.R` → `formR_checks_out.txt`; 2026-11-11)

Design for K8–K10: Gaussian rows, p = 80, Σ_jk = 0.35(1 + |j − k|)^{−2.5} off the diagonal, one truth, leak set of
radius 12, reference neighbourhoods of radius 3. Falsification attempts at small n; nothing asymptotic is tested.
No violation was found.

| id | lemma step | test | outcome |
|---|---|---|---|
| K8 | L4 (★): Cov(W_l, W_j \| W_U) = Cov(W_l, W_j \| W_{U₀}) − c_lᵀS_VV⁻¹c_j (the product form) | 2000 random (l, U), \|U\| ≤ 15 | max error 5e-20 |
| K9 | L4 Lemma 2: \|ẑ_U − ẑ_{U₀}\| ≤ C(ℓ + r h_n + h_n²) on the sample | n = 4000, 5 designs × 200 (l, U); ℓ, r = population leak and localisation levels of each tested pair | max ratio 0.95; max \|ẑ_{U₀}\|/h_n = 1.1. (At these sizes the ratio to the older norm-product scale r² + h_n² is 1.08, so the test does not separate the two forms; it only fails to break the bound) |
| K10 | L4 Lemma 3: tail of h_{U₀,l} at a deterministic reference set | n = 300, 40 000 draws, t = 4, 8, 12 | P(h ≥ t)/P(χ²₁ ≥ t) = 1.04, 0.96, 1.17 (the leak of the tested pair is 4e-5, so the mean shift is not exercised) |
| K11 | L5 §3: closed form of F({1}) − F(∅) at p = 1 | 200 random data sets, direct evaluation of the D0 definition | max difference 1.2e-13 |
| K12 | L6 E4 (one truth, weak proxies): Gram floor; (W-loc) exact | n = 900, q = 15, p = 300; 500 (T, l) | min eigenvalue 0.72; regression of a proxy on any lattice set = (r, 0, …, 0) exactly (deviation 0) |
| K13 | L6 E5 (equicorrelated group): regression coefficient A_t, residual norm v_t, bound (5.1) | a = 0.5, q = 15; 300 (T, l) | errors 2e-16; max(lhs − rhs) of (5.1) = −1.57 ≤ 0 |

(A first run of K12–K13 reported spurious failures caused by R's `sample()` on a length-one vector in the test
script — it drew l inside T; fixed with index sampling, re-run, results above.)
