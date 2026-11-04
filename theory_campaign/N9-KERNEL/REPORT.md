# N9 (V5) report: kernel validity against the production code

Author: Opus 5.5 (N9 task, Claude Work), 2026-11-04. Write-up of the final run and this report: HQ, because the task's
session ended while its check job waited for an Owls slot; the job then ran (owls_run job 20261103-192546-3136516, rc 0,
124 s) and its outputs are committed unchanged in `results/`.

| Sub-claim | Proof (PROOF.md) | Exact numerical check on production engine headers (CHECK.md, results/) |
|---|---|---|
| Gibbs flip γ_φ-reversible (cap rule included) | PROVED (candidate) | detailed balance to ≤ 1e-15 rel., 3 designs × φ ∈ {0, ½, 1} |
| Uniform swap γ_φ-reversible (\|S\| ∈ {0, p} self-loop) | PROVED (candidate) | ≤ 1e-13 rel. |
| Neighbour swap γ_φ-reversible (symmetric graph, unequal degrees, Hastings factor) | PROVED (candidate) | ≤ 1e-13 rel.; 120 of 256 proposals had a non-unit Hastings factor; control without the factor fails (rel. 0.5–0.75) |
| Independence move with π₀ proposal γ_φ-reversible | PROVED (candidate) | ≤ 2.3e-12 rel.; control with symmetric acceptance fails (rel. 1.0) |
| Uniform random order is state-independent and uniform; round self-adjoint | PROVED (candidate) | order map is a bijection onto all m! permutations (m ≤ 8), reversal-closed; round DB ≤ 6e-14 rel.; fixed canonical order fails (rel. ≈ 0.92–0.999) |
| draw_pi0 samples exactly from π₀ (capped size prior, convolution) | PROVED (candidate) | exact law by DFS over consumed uniforms: max rel. error ≤ 2e-13; production-RNG χ² p = 0.51, 0.97, 0.33 |
| Z̄₀ exact | PROVED (candidate) | build_start vs brute force ≤ 4.5e-16; vs independent long-double spec ≤ 1.3e-14 |

**Verdict: N9 holds** (PROVED, candidate; author-only proof, plus exact numerical verification of the production code
with negative controls that fail as they should). Departures are only at floating-point / 2⁻⁵³ RNG-grid level (PROOF §5);
none is an algebraic or modelling error. Scope of the numerical checks: p ≤ 8, B = 2, three designs (AR(1), factor,
factor with cap K = 5); the proofs do not depend on p or B. An independent cross-family proof check remains to be done
(theorem meeting, V1's HQ).
