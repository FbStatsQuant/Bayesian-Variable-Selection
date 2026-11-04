# API-N200: a quantitative finite-n theorem that speaks to the study's n = 200 (Fable)

**Why.** The simulated JRSS-B referee (`theory/F-REFEREE` REFEREE_REPORT.md, point 1) and the synthesis (`theory/W8-SYNTH` BRIEF.md: "still open: anything quantitative at n = 200") agree this is the paper's biggest weakness: every statistical theorem is asymptotic (T03's thresholds ≈ 2·10⁶) while the simulations are at n = 200. The campaign now has finite-n ingredients that were never assembled:
- T21 (exact composition, every n; Lean-verified on `theory/L-LEAN`);
- O-CERT's per-fit certificates (`theory/O-CERT`, verified by `theory/O-VCERT`);
- O-SWAP's closed-form predicted posterior-miss rates, compared with the observed counts (`theory/O-SWAP`);
- S-ELS: at n = 200 the 2,394 completed fits had 0 search misses and S₀ was scored in every fit (`theory/S-ELS`);
- O-DILUTE's exact three-term identity for the start deficit (`theory/O-DILUTE`).

**Goal.** Assemble and prove a **finite-n theorem** of the form: for a fixed (n, p, design, β), P(wrong report) ≤ P(no output) + [explicit posterior-miss term computable from (X, β, σ²)] + [discovery term], with the discovery term bounded by quantities that are certified or measurable per fit; then evaluate every term numerically at the study's designs (n = 200, p ∈ {500, 1000}, S1–S6, c ∈ {1, 0.5}) and compare with the observed miss counts (`Results/SMC_BVS_v3_production/`). Be honest about which terms are rigorous bounds and which are computed approximations; never upgrade a status. If the posterior-miss term is only an approximation (O-SWAP), say exactly where rigor stops and give the best rigorous bound you can alongside it.

**Deliverable:** `theory_campaign/API-N200/REPORT.md` (+ PROOF.md, scripts via owls_run): the theorem, proof, the n = 200 table (predicted vs observed per cell), confidence card, and a draft paragraph for the paper's n = 200 section.
