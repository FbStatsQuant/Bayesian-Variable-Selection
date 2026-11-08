# SL1 · statement lock · disposition (lead, 2026-11-08)

Reviewer: Codex gpt-6.1-sol, reasoningEffort high (fresh delegate_task). Reply verbatim: `SL1_statement_lock_codex.md`.
Verdict: LOCK WITH CHANGES.

| # | Tag | Disposition |
|---|---|---|
| 1 | REQUIRED | ACCEPTED. h now has a deterministic uniform bound sup_{S,c}|h(S;c)| ≤ B_h; data fixed; calibration information used for h must be in 𝓒 (STATEMENT v2 §0, §1). The card class 0 ≤ h ≤ 1 is B_h = 1. |
| 2 | REQUIRED | ACCEPTED. Parameter domains N_e ≥ 1, L ≥ 0, R′ = 4k (k ≥ 1), σ(𝓒)-measurable, frozen before stream 10; identity on 𝒜 ∩ {r ≤ R′}; single-island independence labelled SI, "sufficient, weaker than IND-T, IND-T extension audit not discharged"; MEAS (joint measurability of Φ) made explicit (STATEMENT v2 §1, §2, §3). |
| 3 | REQUIRED | OBJECTION (recorded, not applied). The HQ ticket for this thread states "Lean is optional and out of scope unless trivial"; no Lean toolchain (lean/lake/elan) is installed on this machine (checked 2026-11-08). The Lean handoff stays an open charter item for the registrar (PLAN v2 "Lean"; REPORT §5). |
| 4 | REQUIRED | ACCEPTED. (a) The exact code propagates the evidence-weighted population measure (never the plain law alone); Corollary E: equality part exact, inequality by Monte Carlo on the production engine (stated). (b) Every basis indicator 1{S = s} added; residuals per q; hook validated against production `pip_plain`; tolerance 1e-10 declared, floating-point enumeration not certified arithmetic. (c) Controls specified (NC1 φ = ½ kernel; NC2 truncated bridge followed by φ = 1 rounds; NC3 adaptive h), degeneracy reported; budget 10 design seeds, fixed replicate counts. (PLAN v2.) |
| 5 | OPTIONAL | ACCEPTED: `4L` clarification added (STATEMENT v2 §1). |
| 6 | OPTIONAL | Noted (agrees with the corollary as stated; the S₀ ∉ Ω case is covered since π(S₀) := 0, δ₁ = 1). |
| 7 | OPTIONAL | ACCEPTED: completion now cited to CEX-guard; T12 (iv.e) cited only for the favourable-diagnostic case (STATEMENT v2 §2, §5; PLAN v2). |

Statement v2 is LOCKED.
