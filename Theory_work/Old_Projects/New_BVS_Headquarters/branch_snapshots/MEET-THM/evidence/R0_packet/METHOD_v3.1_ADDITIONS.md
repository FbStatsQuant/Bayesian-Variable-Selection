# SMC-BVS v3.1: what is added to v3

v3.1 is the method in `METHOD_v3.md` unchanged as a statistical method: the same target posterior, blocks and composite start, tempering bridge, move round, resampling, calibration, budgets, HPM decision rule and evidence estimator. The code in `code/` is v3; the additions below are specified but not all coded yet.

## 1. Parallel execution layer (the parallel axis is islands/particles, never variables)
- (a) The R final islands run as concurrent process workers, each with its own score cache and ledger. Their stores and running HPM are merged before the final local search. Output is designed to be bitwise identical to serial execution.
- (b) The 4 diagnostic islands of each calibration rebuild also run concurrently, merged before each local search and before the candidate set V is rebuilt.
- (c) Each local-search scan scores its candidates (all flips and swaps) in parallel; the best strict improvement is chosen by a max-reduction that keeps the lexicographic tie rule, so the search path equals the serial one.
- (h) The block tables are scored in parallel over blocks and sub-models.
- Any worker stop, LS0 stop or guard stop means the fit returns no output (an "unavailable" status with every estimate field NA), never a partial estimate.

## 2. Optional stacking
R′ = 4k final islands (default R′ = 4) at unchanged per-island population N_e, declared before any final-run randomness. Final islands use streams 10, …, 9 + R′. N_e is never split across more islands. With R′ > 4, an extra local search runs from the centre of islands 1–4. Two records are kept: the expanded record (all R′ islands) and the baseline record (islands 1–4).

## 3. LS0
After the final local search, one more local search (same rules as §6.10) runs from the start mode S̃₀ = argmax of the start distribution π₀, computed exactly by dynamic programming over the blocks (ties: smallest size, then lexicographic). LS0 reads no random numbers. Every model it scores joins the scored set and the stores.

## 4. Reporting
- **Primary PIP:** Ẑ-weighted over islands, PIP̂_j = Σ_r Ẑ_r PIP̂_rj / Σ_r Ẑ_r. **Secondary:** the equal-weight mean over islands. Both MPMs ({j : PIP̂_j > ½}) and R_eff = (Σ_r Ẑ_r)² / Σ_r Ẑ_r² are reported.
- **General posterior summaries:** for a finite list 𝓗 of bounded functions h of the model (default: model-size indicators and joint inclusion of pairs joined in the neighbour graph), each island accumulates H_r(h) = (4N_e)⁻¹ Σ over the 4 measured rounds and all particles of h(S), after each complete measured round. Reported: the Ẑ-weighted and equal-weight pools. h must be fixed before final-run randomness.
- **Run card (computed after the run, never fed back):** Z_𝒯 = Σ_{S∈𝒯} e^{F(S)} over the deduplicated reported top store 𝒯 (size ≤ 40p + 1); the bound max(Z_𝒯, 0.05Ẑ); the score gaps of the returned model Ŝ to its single flips/swaps and to its proper subsets; the gap between the best and second-best scored models; optionally a branch-and-bound over a declared region around Ŝ, under a declared budget ("unresolved" on exhaustion).
- On every return without complete output, every estimate field is NA.

## 5. Generality fixes
- Input domain n ≥ 2 (n = 2 is run by the exact branch; n = 1 returns `degenerate_n`; zero predictors returns `no_predictors`).
- Neighbour-graph threshold r_n = √(2 log p / n); when r_n ≥ 1 (p > e^{n/2}) the graph falls back to each variable's best partner.
- Clustering cut is by size only (no correlation cut).
- B* = 16 is a declared budget for the exhaustive block tables.
- Checked integer/stream/allocation arithmetic (status `unsupported_size`); memory preflight uses the actual number of blocks.
- The wall-time and memory allocation is a declared input: it decides only whether output is delivered.

## 6. Declared future path (not in v3.1)
Per-particle counter-based random streams (particle-parallel islands) and a scorer that does not need the p × p Gram matrix.
