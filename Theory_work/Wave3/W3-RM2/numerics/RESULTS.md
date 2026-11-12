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
  not the production routines themselves; ties are broken by first maximum.
