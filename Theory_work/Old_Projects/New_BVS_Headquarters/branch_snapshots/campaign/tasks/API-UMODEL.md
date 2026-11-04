# API-UMODEL: referee-response task R7 (U-MODEL)

Copied verbatim from `theory/F-REFEREE:theory_campaign/F-REFEREE/RESPONSE_PLAN.md` §3, task R7. Run `git fetch origin` and read the branches it names; also read the campaign synthesis `theory/W8-SYNTH:theory_campaign/W8-SYNTH/SYNTHESIS.md` for the current state, and the open PR branch `theory/E-SPINE` (the story is now 'moving off the start is needed', not 'tempering is needed').

### R7. U-MODEL: make the no-output event a model event

**Paper role:** Theorem 4 and Theorem 5(0) (m14, M8).

**Claim to prove.** (i) T32(i): a deterministic ceiling N_score(n, p, B, 𝓒) on the number of score evaluations of the
potential run under the v3 budgets (W7-SEC is on this; reuse if done). (ii) Define the guard by a score-count budget
N_max(n, p) ≥ N_score; then U ∈ σ(R̄) and U = ∅ on the potential run under EX-A, so Theorem 4 reads
P(Ŝ ≠ S₀) ≤ 2E₀δ₁ + P(S₀ ∉ 𝒮̄) with no P(U) term. (iii) State what changes if the guard stays wall-clock: the result is
conditional on the operational element Ξ, and the stop rate is an empirical fact outside the model. Check with the code
whether a score-count guard is a one-line change (`v3_runtime.h`).
**Deliverable.** `theory_campaign/U-MODEL/REPORT.md` with T32(i)'s proof (or citation), the restated Theorem 4, and the
code note.
