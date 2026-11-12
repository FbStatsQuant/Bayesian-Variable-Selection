# W3-RM2 numerics — SPEC (sharpness gate; boundary-violation probes)

**Observations only, never proofs.** All theorems are asymptotic; nothing here is evidence about a limit. Local
machine only (R 4.6.1 + Rcpp, 3–7 worker processes); no NOTS.

## Method objects
* From the **production core** (`Scripts/SMC_BVS/core`, compiled locally, not edited; worktree commit 9700e17): the
  standardised context, the partition (`v3_setup`: complete linkage, blocks ≤ 16), the block tables `log_r`, the prior
  `log_w`, the score (`v3_score`).
* Re-implemented in `rm2_common.R`, because the core exports neither and its LS0 rescoring is too slow at start modes
  of 100–300 columns:
  * `start_mode_dp` — the start mode S̃₀ = argmax γ₀ on Ω by the block dynamic programme over the production tables;
  * `ls0_fast` — a re-implementation of the LS0 of `cpp/v3_engine.h:379-419` [SW1-3: with three departures from the
    production routine — (i) a move needs an improvement > 1e-9, production any strict improvement (`v3_engine.h:408`);
    (ii) at the cap it returns the current centre, production returns the best improving neighbour of the last
    completed scan (`v3_engine.h:410`), so `final_size` of a capped probe is the size of the current centre at the
    cap; (iii) ties go to the first maximum, production breaks them lexicographically. The validation runs do not
    exercise these three branches] (one scan = every single flip and every swap; move to the
    best neighbour on a strict F improvement; cap ℓ_n + |centre|), all neighbour scores by exact rank-one updates of
    the production score.
* **Validation against production** (`validate.R` → `validate_out.txt`): 306 scores (centres, additions, deletions,
  swaps; model sizes 0–40) agree with `v3_score` to 3.4e-13; the DP mode has larger production start mass
  (`v3_start_logmass`) than all 600 single flips and 1997 random perturbations; the fast LS0 path equals a
  brute-force LS0 on production scores from 4 centres (same end point, same number of moves).
* Not run: the SMC sampler, calibration, the final local search. "Conclusion held" below means **LS0 from the start
  mode ends at S₀ with a completed scan that finds no strict improvement** (the event 𝒦_n with certification); the
  posterior part of the theorem ([POST]) is not probed.

## Designs (Gaussian rows; the classification of each cell is NOMINAL — defined by the population design)
p = 2n; n ∈ {400, 1600} (10 and 6 seeds per cell) and n = 3200 (B1 only, 3 seeds). σ = 1. Two independent truths,
θ = (3, 1). Leak set: m = ⌈n^b⌉ columns, all weak proxies of truth 1, x_t = r x_1 + √(1 − r²) e_t, with r = r_n such
that the population gain of one proxy given ∅ is 3 × the start-mode entry level:
n r² θ₁²/τ₀² = 3(log n + 2 log p), τ₀² = σ² + ‖θ‖². Q := S₀ ∪ leak set, |Q| = m + 2.
(With all proxies on one truth at most 15 of them can share the truth's block, where they are invisible.)

| id | assumption probed | construction | inside / outside (nominal) |
|---|---|---|---|
| B1 | size of the leak set, (L-size^b): b < ½ (η = 0) | outside columns iid N(0,1); b ∈ {0.25, 0.375, 0.5, 0.625, 0.75} | b ≤ 0.375 inside; b = 0.5 at the boundary; b ≥ 0.625 outside. In this design the leak innovations are independent, so the lattice directions are nearly orthogonal and the width remainder is ≈ m²/n: (W) and the sandwich reach their limit together at b = ½ |
| B2 | lattice width (W) | every outside column loads on the common direction of the leak innovations: x_l = √(1 − s) w_l + √s · m^{−1/2} Σ_t e_t, s = 0.5; b ∈ {0.25, 0.375, 0.5} | the heuristic design of W3-RM SHARPNESS §4: lattice width² ≈ 2 log p + c·m, a heuristic width-stress design: (W) is expected to fail once m ≫ log n, but this is not certified on the realised designs. [SW1-2] Leakage is not exactly preserved either: outside columns are marginally independent of the truths, but given a proxy P_t = rH + √(1 − r²)E_t of a truth H, Cov(O, H \| P_t) = −r√(s(1 − r²)/m) ≠ 0 — a positive leak that vanishes as m grows. B2 is a nominal stress of (W), not an isolated violation |
| B3 | a weak truth: (BM-Q) / finite-n visibility | B1 with θ₂ weak, nθ₂² = 12 log n; b ∈ {0.5, 0.625} | nθ₂² is below the lattice size at b = 0.625 and below the finite-n start-mode entry level (≈ τ²(log n + 2 log p)): BM-Q cannot be isolated from visibility at these n |
| B4 | leak level η against the frontier b < β(η, A) | B1 at b = 0.375 with every outside column leaking from truth 1 at nominal τ-normalised level η ∈ {0.05, 0.2, 1} | β(η, A) = 0.375 at η ≈ 0.007 (A ≈ 1.1): all three cells are nominally outside the frontier |

## Recorded per run (`results_raw.csv`; cell summaries `summary.csv`)
* start mode: size, number of leak columns, of outside columns (`start_out`), of missing truths; `sandwich` =
  S₀ ⊆ S̃₀ ⊆ Q; `feas` = (L-feas) holds for this Q;
* LS0 with the shipped cap: moves, moves that are not deletions of an extra (`n_other`, their types), end point,
  certification; `old_cap_ok` = the same path would end at S₀ within the old cap ℓ_n;
* **path-level no-addition** at every visited lattice centre T: naC = max_l F(T+l) − F(T); naD = max over extras e and
  l of F(T−e+l) − F(T−e); naE = max over extras e of F(T) − F(T−e); `path_NA_ok` = all three < 0 along the path
  (these are the instances of NA(𝓛) that the descent lemma uses);
* **whole-lattice probe**: adversarial lattice sets T_τ = S₀ ∪ {leak columns whose noise coordinate is ≤ τ} (and the
  mirror sets), τ ∈ {−1, −0.5, 0, 0.3, 0.61, 1, 1.5}; `probe_margin` = max over these sets and over l ∉ T of
  F(T+l) − F(T); `probe_NA_violated` = margin > 0, a true violation of NA(𝓛) at a lattice set (a lower bound on how
  often NA(𝓛) fails: only 14 of the 2^m lattice sets are tried).

## Files
`rm2_common.R` (objects, designs, one run), `validate.R`, `validate_out.txt`, `run_all.R` (driver), `summarise.R`,
`results_raw.csv`, `summary.csv`, `RESULTS.md`.
